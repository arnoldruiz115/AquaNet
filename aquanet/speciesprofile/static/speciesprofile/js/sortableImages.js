$( function() {
    $( "#sortable" ).sortable({
      revert: false,
      axis: "x"
    });
    $( "ul, li" ).disableSelection();

    var $carousel = $('#carousel');
    $('.deleteBtn').click(function(){
        // append the id of image to the list of images to be deleted
        var deleteList = $("#deleteList").val();
        if (deleteList == ""){
            // if list is empty don't add a comma
            addedValue = deleteList + $(this).val();
            $("#deleteList").val(addedValue);
        }
        else{
            addedValue = deleteList + "," + $(this).val();
            $("#deleteList").val(addedValue);
        }

        // remove the image from the carousel and hide the thumbnail indicator
        $("#thumb" + $(this).attr('delete-img')).remove();
        $(this).parent().remove();

        // Make new active image after deleting
        $carousel.find('.carousel-item').first().addClass('active');
        $carousel.find('.ui-sortable-handle').first().addClass('active');
        var i = 0;
        $('#sortable > li').each(function(){
            $(this).attr('data-slide-to', i)
            i++;
            slideNum = $(this).attr('data-slide-to');
        });
    });

    $( "#sortable" ).on( "sortupdate", function( event, ui ) {
        var i = 0;
        $('#sortable > li').each(function(){
            $(this).attr('data-slide-to', i)
            i++;
            slideNum = $(this).attr('data-slide-to');
            imageId = $(this).children().attr('img-id');
            image_url = $(this).children().attr('src');
            $("#image"+slideNum).attr("src", image_url);
            $("#delete"+slideNum).val(imageId);
            $("#delete"+slideNum).attr('delete-img', $(this).attr('order-id'));
        });

        //After the sort update make the recently clicked the active image
        // clear active thumbnail and make the most recently moved thumbnail active
        $(this).children().removeClass('active');
        last_moved = ui.item;
        last_moved.addClass('active');

        // clear active image and make the slide corresponding to the recently moved thumbnail active
        $('.carousel-inner').children().removeClass('active');
        slideTo = last_moved.attr('data-slide-to');
        $("#inner-img" + slideTo).addClass('active');

    });

    $("#saveImages").click(function(){
        var new_order = $( "#sortable" ).sortable('toArray', {attribute: "order-id"});
        $("#saveImages").val(new_order);
    });
 });
