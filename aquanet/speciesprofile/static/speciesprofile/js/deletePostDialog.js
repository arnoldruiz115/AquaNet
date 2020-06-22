$( document ).ready(function() {
    $('#deletePopup').dialog({
        autoOpen: false,
        modal: true,
        resizable: false,
        draggable: false,
        title: 'Delete',
        show: {
            effect: "fade",
            duration: 150
        },
        hide: {
            effect: "fade",
            duration: 150
        }
    });
    
    $('#deletePost').click(function(){
        $('#deletePopup').dialog("open");
        $('#deletePopup').load('delete/', function(){
            $('#cancelDeleteBtn').click(function(){
                $('#deletePopup').dialog("close");
            });
        });
    });
});