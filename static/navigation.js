$(document).ready(function () {


    $('.create_project_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');
        $.ajax({
            url: '/erp/create_project',
            type: "GET",        
            success: function (data) {                
                $('.main-wrapper').html(data)
            },
        });
    })

});