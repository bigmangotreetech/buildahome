$('#get_procurement').on('click', function(){
    const project = $("#project").val()
    window.location.href = '/material/view_inventory?project_id='+project.toString()
})