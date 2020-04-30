from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Q
from .models import Profile, ProfileImage
from .forms import SpeciesProfileForm, SpeciesImageForm


# Create your views here.
class IndexView(ListView):
    template_name = 'speciesprofile/index.html'
    context_object_name = 'species_list'

    def get_queryset(self):
        return Profile.objects.order_by('-publish_date')[:4]


class SearchResultView(ListView):
    template_name = 'speciesprofile/searchresults.html'
    context_object_name = 'result_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchResultView, self).get_context_data(**kwargs)
        context.update({'search': self.kwargs['common_name']})
        return context

    def get_queryset(self):
        search = self.kwargs['common_name']
        return Profile.objects.filter(Q(common_name__contains=search) | Q(species__contains=search))


@require_http_methods(["POST"])
def search_form_page(request):
    if request.method == 'POST':
        search = request.POST['SearchSpecies']
        if not search:
            messages.warning(request, 'Can not search empty string.')
            return render(request, 'speciesprofile/searchresults.html')
        return redirect('speciesprofile:search', search)


def search_advanced(request):
    if request.method == 'GET':
        return render(request, 'speciesprofile/advancedsearch.html')
    if request.method == 'POST':
        search = "Advanced Search"
        result_list = Profile.objects.all()

        # If min size is input
        if request.POST.get('minsize'):
            min_size = request.POST.get('minsize')
            result_list = result_list.filter(Q(max_size__gte=min_size))

        # If max size is input
        if request.POST.get('maxsize'):
            max_size = request.POST.get('maxsize')
            result_list = result_list.filter(Q(max_size__lte=max_size))

        # If water type is input
        water_type = request.POST.get('waterSelect')
        if not water_type == "Any":
            result_list = result_list.filter(water_type=water_type)

        # If price is input
        if request.POST.get('minprice') or request.POST.get('maxprice'):
            result_list = result_list.filter(Q(for_sale=True))
            if request.POST.get('minprice'):
                min_price = request.POST.get('minprice')
                result_list = result_list.filter(Q(price__gte=min_price))
            if request.POST.get('maxprice'):
                max_price = request.POST.get('maxprice')
                result_list = result_list.filter(Q(price__lte=max_price))

        context = {
            'result_list': result_list,
            'search': search
        }
        return render(request, 'speciesprofile/searchresults.html', context)


class SpeciesDetailView(DetailView):
    model = Profile
    template_name = 'speciesprofile/detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SpeciesDetailView, self).get_context_data(**kwargs)
        profile = self.get_object()
        images = ProfileImage.objects.filter(profile=profile.pk).order_by('order')
        context.update({'images': images})
        return context


class SpeciesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = 'speciesprofile/update.html'
    form_class = SpeciesProfileForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class SpeciesImagesFormset(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Profile
    template_name = 'speciesprofile/_updateimagesformset.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SpeciesImagesFormset, self).get_context_data(**kwargs)
        image_form = SpeciesImageForm()
        profile_images = self.get_image_list()
        context.update({'form': image_form, 'profile_images': profile_images})
        return context

    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        image_form = SpeciesImageForm(request.POST, request.FILES, instance=profile)

        if request.POST.get("saveImages") or request.POST.get("uploadImage"):
            # Save changes in order and return
            new_order_list = request.POST.get("orderList")
            new_order_list = new_order_list.split(',')
            order_list = []
            if not new_order_list == ['']:
                for element in new_order_list:
                    order_list.append(int(element))
            counter = 0
            thumbnail_changed = False
            image_list = self.get_image_list()

            # Add "deleted" images to new image order list to the back
            for img in image_list:
                if img.order not in order_list:
                    order_list.append(img.order)

            # If image.order not equal to new order list, change the order to match the new order list
            for image in image_list:
                if image.image:
                    if not image.order == order_list.index(image.order):
                        if image.order == 0:
                            thumbnail_changed = True
                        image.order = order_list.index(image.order)
                        image.save()
                counter += 1

            # If first image.order was changed make the new image with order = 0 the new profile preview/thumbnail
            if thumbnail_changed:
                first_image = ProfileImage.objects.get(profile=profile.pk, order=0)
                profile.thumbnail = first_image.image
                profile.thumbnail_aspect_ratio = first_image.aspect_ratio
                profile.save()

            # Delete images marked for deletion
            if request.POST.get("deleteList"):
                delete_data = request.POST.get("deleteList")
                delete_list = delete_data.split(',')
                image_ids = []
                for element in delete_list:
                    image_ids.append(int(element))

                for image_id in image_ids:
                    if image_id in self.get_image_ids():
                        image = ProfileImage.objects.get(id=image_id)
                        image.delete()
                    else:
                        return HttpResponseForbidden()

            if image_form.is_valid():
                clean_data = image_form.cleaned_data
                image = clean_data['image']
                if image:
                    photo = ProfileImage(profile=profile, image=image)
                    photo.save()

            if request.POST.get("uploadImage"):
                return redirect('speciesprofile:images-formset', profile.id)

        return redirect('speciesprofile:detail', profile.id)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_image_list(self):
        profile = self.get_object()
        images = ProfileImage.objects.filter(profile=profile.pk).order_by('order')
        return images

    def get_image_ids(self):
        profile = self.get_object()
        images = ProfileImage.objects.filter(profile=profile.pk)
        image_ids = []
        for image in images:
            image_ids.append(image.id)
        return image_ids


class SpeciesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'speciesprofile/delete.html'

    def get_success_url(self):
        return reverse('users:profile', kwargs={'username': self.request.user.username})

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
