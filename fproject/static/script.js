$(document).ready(function() {

    $('.updateButton').on("submit", function() {
        

        req = $.ajax({
            url : '/login',
            type : 'POST',
        });

        req.done(function(data) {

            $('#random').text(data.ran_num);

        });
    

    });

});