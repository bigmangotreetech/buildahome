$('#get_procurement').on('click', function(){
    const project = $("#project").val()
    if(project.length)
    window.location.href = '/material/view_inventory?project_id='+project.toString()
})