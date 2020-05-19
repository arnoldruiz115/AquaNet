$(document).ready(function(){
    $("#show-upload-button").click(function(){
        $('#upload-form-id').show();
        $("#show-upload-button").hide();
    });

    var imagePreview  = $("#img-prev-id");
    var defaultText = $("#default-prev-state");

    $(document).on('change', '#id_form-0-image', function(){
        var img = $("#id_form-0-image").prop('files')[0];
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
