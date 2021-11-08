$('#get_procurement').on('click', function(){
    const project = $("#project").val()
    const material = $("#material").val()
    if(project.length && material.length)
    window.location.href = '/material/view_inventory?project_id='+project.toString()+'&material='+material.toString()
})