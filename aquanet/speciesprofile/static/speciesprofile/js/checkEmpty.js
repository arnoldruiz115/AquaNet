$(document).ready(function(){
    $("#searchButton").click(function(){
        if ($("#SearchSpecies").val() == ""){
            $("#SearchSpecies").addClass('is-invalid');
            return false;
        }
    });
});
