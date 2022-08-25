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

    function initKypMaterial() {
        $("#update_kyp_material").on('click', function(){
            const project = $("#project").val()
            if (project.length) {
                $.ajax({
                    url: '/erp/kyp_material?project_id='+project.toString(),
                    type: "GET",        
                    success: function (data) {     
                        $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
                        $('.select2').select2();
                        initKypMaterial();
                        $('.select2').on('click', function(){
                            setTimeout(() => {
                                if($('.select2-search__field').length) $('.select2-search__field').get(0).focus()
                            }, 0)
                        })
                    },
                });
            }
        })
    }

    function initViewInventory() {
        $('#get_procurement').on('click', function(){
            const project = $("#project").val()
            const material = $("#material").val()
            if(project.length && material.length) {
                $.ajax({
                    url: '/erp/view_inventory?project_id='+project.toString()+'&material='+material.toString(),
                    type: "GET",        
                    success: function (data) {        
                        $('.main-wrapper').html(data);
                        $('.main-wrapper').css('background','white')
                        $('.select2').select2();
                        initViewInventory();
                        $('.select2').on('click', function(){
                            setTimeout(() => {
                                if($('.select2-search__field').length) $('.select2-search__field').get(0).focus()
                            }, 0)
                        })
                    },
                });
            }
        })
    }

    function initEnterMaterial() {
        $(".material-select").on('change', function() {
            $(".vendor-select").empty()
            $(".vendor-select").append($("<option></option>"))
            const material_selected = $(this).val().trim()
            $.ajax({
                    url: '/erp/get_vendors_for_material',
                    type: "POST",
                    dataType: 'json',
                    data: { 'material_selected': material_selected },
                    success: function (data) {
                        for (const vendor of data) {
                            $(".vendor-select").append($("<option></option>")
                                .attr("value", vendor[0])
                                .text(vendor[1]))
                        }
                    }
                });
        })
    }


    $('.create_project_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');
        $('.main-wrapper').html('')
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/create_project',
            type: "GET",        
            success: function (data) {         
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
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
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/unapproved_projects',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
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
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/archived_projects',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
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
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/projects',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
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
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/create_user',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
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
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/view_users',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
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
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/vendor_registration',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
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
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/view_vendors',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
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
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/kyp_material',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
                $('.select2').select2();
                initKypMaterial();
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
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/enter_material',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
                initEnterMaterial();
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
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/shifting_entry',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
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
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/view_inventory',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
                $('.select2').select2();
                initViewInventory();
                $('.select2').on('click', function(){
                    setTimeout(() => {
                        if($('.select2-search__field').length) $('.select2-search__field').get(0).focus()
                    }, 0)
                })
            },
        });
    })

    $('.view_qs_approval_indents_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/view_qs_approval_indents',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
                $('.select2').select2();
                $('.select2').on('click', function(){
                    setTimeout(() => {
                        if($('.select2-search__field').length) $('.select2-search__field').get(0).focus()
                    }, 0)
                })
            },
        });
    })

    $('.view_approved_indents_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/view_approved_indents',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
                $('.select2').select2();
                $('.select2').on('click', function(){
                    setTimeout(() => {
                        if($('.select2-search__field').length) $('.select2-search__field').get(0).focus()
                    }, 0)
                })
            },
        });
    })

    $('.view_approved_POs_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/view_approved_POs',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
                $('.select2').select2();
                $('.select2').on('click', function(){
                    setTimeout(() => {
                        if($('.select2-search__field').length) $('.select2-search__field').get(0).focus()
                    }, 0)
                })
            },
        });
    })

    
    $('.view_ph_approved_indents_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/view_ph_approved_indents',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
                $('.select2').select2();
                $('.select2').on('click', function(){
                    setTimeout(() => {
                        if($('.select2-search__field').length) $('.select2-search__field').get(0).focus()
                    }, 0)
                })
            },
        });
    })
    
    $('.view_deleted_indents_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/view_deleted_indents',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
                $('.select2').select2();
                $('.select2').on('click', function(){
                    setTimeout(() => {
                        if($('.select2-search__field').length) $('.select2-search__field').get(0).focus()
                    }, 0)
                })
            },
        });
    })

    $('.contractor_registration_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/contractor_registration',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
                $('.select2').select2();
                $('.select2').on('click', function(){
                    setTimeout(() => {
                        if($('.select2-search__field').length) $('.select2-search__field').get(0).focus()
                    }, 0)
                })
            },
        });
    })

    $('.view_contractors_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/view_contractors',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
                $('.select2').select2();
                $('.select2').on('click', function(){
                    setTimeout(() => {
                        if($('.select2-search__field').length) $('.select2-search__field').get(0).focus()
                    }, 0)
                })
            },
        });
    })

    $('.create_work_order_nav_btn').on('click', function(){
        $('.nav-link').removeClass('active');
        $(this).addClass('active');        
        $('.main-wrapper').html('')
        $(".main-wrapper").css({background:'linear-gradient(90deg, rgba(173,173,173,1) 0%, rgba(255,255,255,1) 70%)'});
        $.ajax({
            url: '/erp/create_work_order',
            type: "GET",        
            success: function (data) {        
                $('.main-wrapper').html(data);
                $('.main-wrapper').css('background','white')
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