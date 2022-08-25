$(document).ready(function () {


    $('.create_project_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');
        $.ajax({
            url: '/erp/create_project',
            type: "GET",        
            success: function (data) {                
                $('.main-wrapper').html(data);
                $('.select2').select2();
                $('.select2').on('click', function(){
                    setTimeout(() => {
                        if($('.select2-search__field').length) $('.select2-search__field').get(0).focus()
                    }, 0)
                })
            },
        });
    })
    

});