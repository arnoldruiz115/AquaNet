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
        document.querySelector('#chat-log').value += (data.message + '\n');
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

    $('#testBtn').click(function(){
        $("#chat-container").append('<div class="d-flex justify-content-end mb-4 mr-3"><div class="chat-message-box">{{message}}<span class="chat-time-stamp sender">{{timenow}}</span></div></div>')
    });
});
