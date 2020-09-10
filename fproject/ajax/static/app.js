$(document).ready(function() {

    $('.updateButton').on('click', function() {

        req = $.ajax({
            url : '/random',
            type : 'POST',
        });

        req.done(function(data) {

            $('#random').text(data.random_num);


        });
    

    });

});