$( function() {
    $( "#sortable" ).sortable({
      revert: true,
      axis: "x"
    });
    $( "ul, li" ).disableSelection();
     $("#testBtn").click(function(){
        alert( $( "#sortable" ).sortable('toArray', {attribute: "order-id"}));
    });
    $( "#sortable" ).on( "sortchange", function( event, ui ) {
        } );
    $("#saveImages").click(function(){
        var new_order = $( "#sortable" ).sortable('toArray', {attribute: "order-id"});
        $("#saveImages").val(new_order);
    });
 });
