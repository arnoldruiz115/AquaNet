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
        $("#thumb" + $(this).val()).hide();
        var activeSlide = $carousel.find('.carousel-item.active');
        activeSlide.remove();
        var nextSlide = $carousel.find('.carousel-item').first();
        nextSlide.addClass('active');
        var i = 0;
        $('#sortable > li').each(function(){
            $(this).attr('data-slide-to', i)
            i++;
            slideNum = $(this).attr('data-slide-to');
        });

    });

    $( "#sortable" ).on( "sortupdate", function( event, ui ) {
            $("#sortable").sortable("refresh");
            var i = 0;
            $('#sortable > li').each(function(){
                $(this).attr('data-slide-to', i)
                i++;
                slideNum = $(this).attr('data-slide-to');
                imageId = $(this).children().attr('img-id');
                image_url = $(this).children().attr('src');
                $("#image"+slideNum).attr("src", image_url);
                $("#delete"+slideNum).val(imageId);
            });
        } );
    $("#saveImages").click(function(){
        var new_order = $( "#sortable" ).sortable('toArray', {attribute: "order-id"});
        $("#saveImages").val(new_order);
    });
 });
