$('#get_procurement').on('click', function(){
    const project = $("#project").val()
    const material = $("#material").val()
    if(project.length && material.length) {
        $.ajax({
            url: '/erp/view_inventory?project_id='+project.toString()+'&material='+material.toString(),
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
    }
})



$("#update_kyp_material").on('click', function(){
    const project = $("#project").val()
    if (project.length) {
        $.ajax({
            url: '/erp/kyp_material?project_id='+project.toString(),
            type: "GET",        
            success: function (data) {     
                console.log(data)   
                $('.main-wrapper').html(data);
                $('.select2').select2();
                $('.select2').on('click', function(){
                    setTimeout(() => {
                        if($('.select2-search__field').length) $('.select2-search__field').get(0).focus()
                    }, 0)
                })
            },
        });
    }
})

if($('#total_item_quantity').length) {
    let current_quantity = 0;
    let total_quantity = parseFloat($('#total_item_quantity').text().trim())
    $('.item_quantity').each(function(index, element){
        current_quantity += parseFloat($(this).text().trim())
    })
    let balance = total_quantity - current_quantity;
    $('#total_current_quantity').text('Current : '+current_quantity.toString())
    $('#total_balance_quantity').text('Balance : '+balance.toString())
}

if($('.item_difference_cost').length) {
    let total_cost = 0;
    $('.item_cost').each(function(index, element){
        total_cost += parseFloat($(this).text().trim())
    })
    $("#total_cost").text(total_cost)

    let total_difference_cost = 0;
    $('.item_difference_cost').each(function(index, element){
        total_difference_cost += parseFloat($(this).text().trim())
    })
    $("#total_difference_cost").text(total_difference_cost)
}