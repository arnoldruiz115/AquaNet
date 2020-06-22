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

    $('#messageUser').dialog({
        autoOpen: false,
        modal: false,
        resizable: false,
        draggable: false,
        height: 450,
        width: 500,
        title: 'Send a message',
        show: {
            effect: "fade",
            duration: 150
        },
        hide: {
            effect: "fade",
            duration: 150
        }
    });

    $('#messageBtn').click(function(){
        $('#messageUser').dialog("open");
        $('#messageForm').load('/message/')
    });
});