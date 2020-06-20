$(document).ready(function(){
    var imagePreview  = $("#img-prev-id");
    var defaultText = $("#default-prev-state");

    $("#id_user_image").on('change', function(){
        var img = $("#id_user_image").prop('files')[0];
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
