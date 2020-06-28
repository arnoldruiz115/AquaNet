$(document).ready(function(){
    $threadsContainer = $('#threads-container');

    var url_thread = getUrlParameter('thread');
    if(url_thread){
        console.log('running');
        $('#conversation-container').load('messages/'+url_thread , function(){
            $.getScript('static/userschat/js/socket.js');
            $('#chat-container').scrollTop( $('#chat-container').prop('scrollHeight') );
        });
    }

    function getUrlParameter(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;
    
        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');
    
            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : sParameterName[1];
            }
        }
    };

    $('.thread-box').click(function(){
        currentActive = $threadsContainer.find('.thread-box.active');
        if(currentActive){
            currentActive.removeClass('active');
        }
        var unread = $(this).find('.unread-notification')
        if (unread.length){
            // Decrease notification counter by one
            var counter = parseInt($("#navbar-notif").text());
            if (counter == 1){
                $(document).find('.unread-notification-nav').remove()
            }
            else{
                $("#navbar-notif").text(counter - 1);
            }
            unread.remove();
        }
        $(this).addClass('active');
        var thread = $(this).attr('data-thread-id');
        $('#conversation-container').load('messages/'+thread , function(){
            $.getScript('static/userschat/js/socket.js');
            $('#chat-container').scrollTop( $('#chat-container').prop('scrollHeight') );
        });
    });
});
