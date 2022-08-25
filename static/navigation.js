$(document).ready(function () {

    function initSearchProject() {
        console.log('initSearchProject')
        $('.search-project-field').on('keydown', function() {
            let searchValue = $('.search-project-field').val();
            if(searchValue.trim().length == 0) $('.project-card').parent().addClass('d-none')
            else {
                $('.project-card').parent().addClass('d-none')
                $('.project-card').each(function(index, element) {
                    if($(element).find('.project-name').text().toLowerCase().trim().includes(searchValue.toLowerCase().trim())) {               
                        $(element).parent().removeClass('d-none')
                    }
                })
            }
        })
    }


    $('.create_project_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');
        $('.main-wrapper').html('')
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

    $('.unapproved_projects_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $.ajax({
            url: '/erp/unapproved_projects',
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

    $('.archived_projects_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $.ajax({
            url: '/erp/archived_projects',
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

    $('.projects_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $.ajax({
            url: '/erp/projects',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.select2').select2();
                initSearchProject()
                $('.select2').on('click', function(){
                    setTimeout(() => {
                        if($('.select2-search__field').length) $('.select2-search__field').get(0).focus()                        
                    }, 0)
                })
            },
        });
    })
    

});