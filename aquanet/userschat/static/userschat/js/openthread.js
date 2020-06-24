$(document).ready(function(){
    $threadsContainer = $('#threads-container');

    $('.thread-box').click(function(){
        currentActive = $threadsContainer.find('.thread-box.active');
        if(currentActive){
            currentActive.removeClass('active');
        }
        $(this).addClass('active');
        var thread = $(this).attr('data-thread-id');
        $('#conversation-container').load('messages/'+thread);
    });
});
