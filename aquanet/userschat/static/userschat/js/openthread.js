$(document).ready(function(){
    $('.thread-box').click(function(){
        var thread = $(this).attr('data-thread-id');
        $('#conversation-container').load('messages/'+thread);
    });
});
