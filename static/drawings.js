drawings_list = []
var actionBtn;
var action;
var project_id;
var drawing_name;
var drawing_link;

$('th').each(function(index, element) {
    if (index!=0)
        drawings_list.push(element.innerHTML)
})

$('.status-action').on('click', function() {
    $('.current-status').text('')
    actionBtn = $(this).find('div')
    $('.upload-drawing-form').addClass('d-none')

    drawing_link = $(this).attr('data-link').toString()

    if (drawing_link == 'None' || drawing_link == '0' || drawing_link == '') {
        $('.drawing-link-section').addClass('d-none')
    }
    else {
        $('.drawing-link-section').removeClass('d-none')
        $('.drawing-link').attr('href', '/files/'+$(this).attr('data-link').toString())
    }

    project_name = $($(this).parents('tr').find('td').get(0)).text()
    project_id = $($(this).parents('tr').find('td').get(0)).attr('data-project-id')

    $('#project_id').val(project_id)
    $('.project_name').text(project_name)

    index = $(this).attr('data-index')
    drawing_name = drawings_list[index]
    $('.drawing_name').text(drawing_name)
    $('#drawing_name').val(drawing_name)
})

$('.drawing-complete').on('click', function(){
    action = 'Complete';
    $('.current-status').text('Changing status to '+action)
    $('.upload-drawing-form').removeClass('d-none')
})

$('.drawing-in-progress').on('click', function(){
    action = 'In progress';
    $('.current-status').text('Changing status to '+action)
    $('.upload-drawing-form').addClass('d-none')
})

$('.drawing-pending').on('click', function(){
    action = 'Pending';
    $('.current-status').text('Changing status to '+action)
    $('.upload-drawing-form').addClass('d-none')
})


$('.approve_drawing_btn').on('click', function(){

    if (action == "Complete") {
        actionBtn.find('.status').addClass('d-none')
        actionBtn.find('.bg-success').removeClass('d-none')
        if ($('#drawing').val().length) {
            $('.upload-drawing-form').submit()
        } else {
            alert('You must upload the drawing to mark it as complete')
        }
    } else if (action == "In progress") {
        actionBtn.find('.status').addClass('d-none')
        actionBtn.find('.bg-warning').removeClass('d-none')

        $.ajax({
        type: "POST",
        url: "/erp/mark_drawing_in_progress",
        success: function (data) {
            window.location.href = '/erp/drawings'
        },
        error: function (error) {
            console.log(error)
            // handle error
        },
        async: true,
        data: {'project_id': project_id, 'drawing_name': drawing_name},
    });
    } else if (action == "Pending") {
        actionBtn.find('.status').addClass('d-none')
        actionBtn.find('.bg-danger').removeClass('d-none')
    }
})