$(document).ready( function() {
    $('.langcode').click( function(){
        var selected_lang = $(this).attr('rel');

        $.ajax({
            url: '/set/lang/',
            type: 'POST',
            data: {lang: selected_lang},
            success: function(data){
                console.log("Received: " + data);
                var current_href = window.location.href;
                if (data == 'ok') window.location.href = current_href;
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log('Ajax error:' + errorThrown);
            },
        });
    });
});
