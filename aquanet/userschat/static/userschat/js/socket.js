$(document).ready(function(){
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
    
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if(data.sender == "self"){
            var user_class = 'justify-content-end mb-4 mr-3';
            var new_message = $('<div class="d-flex justify-content-end mb-4 mr-3"><div class="chat-message-box">' + data.message + '<span class="chat-time-stamp sender">' + data.time_now + '</span></div></div>');
        }
        else{
            var new_message = $('<div class="d-flex justify-content-start mb-4 ml-3"><div class="chat-user-img"><img src="' + data.sender_img_url + '"></div><div class="chat-message-box">' + data.message + '<span class="chat-time-stamp reciever">' + data.time_now + '</span></div></div>');
        }
        $("#chat-container").append(new_message);
    };
    
    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
    
    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };
    
    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    };
});
