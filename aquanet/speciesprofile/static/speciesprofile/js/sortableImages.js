$( function() {
    $( "#sortable" ).sortable({
      revert: false,
      axis: "x"
    });
    $( "ul, li" ).disableSelection();

    var $carousel = $('#carousel');

    
    function refreshSortables(){
        var i = 0;
        $('#sortable > li').each(function(){
            $(this).attr('data-slide-to', i);
            imageId = $(this).children().attr('img-id');
            image_url = $(this).children().attr('src');

            $("#image"+String(i)).attr("src", image_url);
            $("#delete"+String(i)).attr("data-img-id", imageId);
            $("#delete"+String(i)).attr('delete-img', $(this).attr('order-id'));

            // check image orientation/object fit
            // make the new image element match the image orientation/fit 
            slideTo = $(this).attr('data-slide-to');
            targetImage = $('#image'+slideTo);

            if ($(this).children().attr("data-img-type") == 'h'){
                targetImage.attr("width", "800");
                targetImage.removeAttr("height");
            }
            else if ($(this).children().attr("data-img-type") == 'v'){
                targetImage.attr("height", "580");
                targetImage.removeAttr("width");
            }
            else{
                targetImage.attr("height", "580");
                targetImage.attr("width", "800");
            }
            i++;
        });
    }

    $('.deleteBtn').click(function(){
        // append the id of image to the list of images to be deleted
        var deleteList = $("#deleteList").val();
        if (deleteList == ""){
            // if list is empty don't add a comma
            addedValue = deleteList + $(this).attr("data-img-id");
            $("#deleteList").val(addedValue);
        }
        else{
            addedValue = deleteList + "," + $(this).attr("data-img-id");
            $("#deleteList").val(addedValue);
        }
        // Make next image active image
        currentActive = $carousel.find('.carousel-item.active');
        currentThumbnail = $carousel.find('.ui-sortable-handle.active')
        // make the next image the active, if last image is deleted make the previous the active
        if (typeof currentThumbnail.next().attr('id') !== "undefined"){
            currentThumbnail.next().addClass('active');
            currentActive.next().addClass('active');
        }
        else{
            currentThumbnail.prev().addClass('active');
            currentActive.prev().addClass('active');
        }

        // remove the image from the carousel and hide the thumbnail indicator
        $("#thumb" + $(this).attr('delete-img')).remove();
        $(this).parent().remove();

        // update the data slide to attribute for each thumbnail after deleting an image from the list
        var i = 0;
        $('#carousel-inner > div').each(function(){
            $(this).attr('id', "inner-img"+String(i));
            $(this).children("img").attr('id', "image"+String(i));
            $(this).children("a").attr('id', "delete"+String(i));
            $(this).children("a").attr('delete-img', i);
            i++;
        });

        refreshSortables();
    });

    // Make changes when changing images order
    $( "#sortable" ).on( "sortupdate", function( event, ui ) {
        refreshSortables();

        //After the sort update make the recently clicked the active image
        // clear active thumbnail and make the most recently moved thumbnail active
        $(this).children().removeClass('active');
        last_moved = ui.item;
        last_moved.addClass('active');

        // clear active image and make the slide corresponding to the recently moved thumbnail active
        currentActive = $carousel.find('.carousel-item.active');
        currentActive.removeClass('active');
        slideTo = last_moved.attr('data-slide-to');
        $("#inner-img"+slideTo).addClass("active");
    });

    $("#uploadImage").click(function(){
        var new_order = $( "#sortable" ).sortable('toArray', {attribute: "order-id"});
        $("#orderList").val(new_order);
    });

    $("#saveImages").click(function(){
        var new_order = $( "#sortable" ).sortable('toArray', {attribute: "order-id"});
        $("#orderList").val(new_order);
    });

    var imagePreview  = $("#img-prev-id");
    var defaultText = $("#default-prev-state");

    $("#id_image").on('change', function(){
        var img = $("#id_image").prop('files')[0];
        if (img){
            defaultText.hide();
            imagePreview.show();
            $("#img-preview").attr("src", window.URL.createObjectURL(img));
        }

        else{
            imagePreview.hide();
            defaultText.show();
        }
    });
 });
