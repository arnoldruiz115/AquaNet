$("document").ready(function(){
    const roomName = JSON.parse(document.getElementById('room-name').textContent);
    var wsStart = 'ws://'
    if (window.location.protocol == 'https:'){
        wsStart = 'wss://'
    } 
    
    const chatSocket = new WebSocket(
        wsStart
        + window.location.host
        + '/ws/messages/'
        + roomName
        + '/'
    );

    chatSocket.onopen = function(e){
        chatSocket.send(JSON.stringify({
            'message_type': 'init'
        }));
    }
    
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.is_typing){
            if(data.sender == "other"){
                if(data.is_typing == "True"){
                    $('#isTyping').show();
                }
                else{
                    $('#isTyping').hide();
                }
            }
        }
        else if (data.init){
            initialTypingCheck();
        }
        else{
            if(data.sender == "self"){
                var new_message = $('<div class="d-flex justify-content-end mb-4 mr-3"><div class="chat-message-box">' + data.message + '<span class="chat-time-stamp sender">' + data.time_now + '</span></div></div>');
            }
            else{
                var new_message = $('<div class="d-flex justify-content-start mb-4 ml-3"><div class="chat-user-img"><img src="' + data.sender_img_url + '"></div><div class="chat-message-box other">' + data.message + '<span class="chat-time-stamp reciever">' + data.time_now + '</span></div></div>');
            }
            $("#chat-container").append(new_message);
        }
        $('#chat-container').animate({ scrollTop: $('#chat-container').prop('scrollHeight') }, "slow");
    };
    
    chatSocket.onclose = function(e) {
        console.log('Chat socket closed.');
    };
    
    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };

    var empty_chat_warning = false;
    
    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;

        if (message == ''){
            messageInputDom.classList.add('is-invalid');
            empty_chat_warning = true;
            return false;
        }

        chatSocket.send(JSON.stringify({
            'message_type': 'message',
            'message': message
        }));
        messageInputDom.value = '';
        checkTyping();
    };

    var is_typing = '';
    $('#chat-message-input').on('change textInput input', function(){
        checkTyping();
    });

    function checkTyping(){
        var send_message = true;

        if ( $('#chat-message-input').val() == ""){
            if (is_typing == 'False'){
                send_message = false;
            }
            is_typing = 'False';
        }
        else{
            if (is_typing == 'True'){
                if(empty_chat_warning){
                    document.querySelector('#chat-message-input').classList.remove('is-invalid');
                }
                send_message = false;
            }
            is_typing = 'True';
        }

        if (send_message == true){
            chatSocket.send(JSON.stringify({
                'message_type': 'typing',
                'is_typing': is_typing
            }));
        }
    }

    function initialTypingCheck(){
        if ( $('#chat-message-input').val() == ""){
            is_typing = 'False';
        }
        else{
            is_typing = 'True';
        }
        chatSocket.send(JSON.stringify({
            'message_type': 'typing',
            'is_typing': is_typing
        }));
    }

    $('.thread-box').click(function(){
        if (chatSocket){
            chatSocket.close();
        }
    });
});