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

    function initBlockProject() {
        $('.block-project').on('click', function() {
            project_id = $(this).attr('data-project-id')
            $('.project_id').val(project_id)
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
                initBlockProject()
                $('.select2').on('click', function(){
                    setTimeout(() => {
                        if($('.select2-search__field').length) $('.select2-search__field').get(0).focus()                        
                    }, 0)
                })
            },
        });
    })

    $('.create_user_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $.ajax({
            url: '/erp/create_user',
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

    $('.view_users_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $.ajax({
            url: '/erp/view_users',
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


    $('.vendor_registration_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $.ajax({
            url: '/erp/vendor_registration',
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

    $('.view_vendors_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $.ajax({
            url: '/erp/view_vendors',
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

    
    $('.kyp_for_material_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $.ajax({
            url: '/erp/kyp_material',
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

    $('.enter_material_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $.ajax({
            url: '/erp/enter_material',
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

    $('.shifiting_entry_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $.ajax({
            url: '/erp/shifting_entry',
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

    $('.view_inventory_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $.ajax({
            url: '/erp/view_inventory',
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