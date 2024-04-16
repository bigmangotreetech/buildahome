$('#get_procurement').on('click', function(){
    const project = $("#project").val()
    const material = $("#material").val()
    const vendor = $("#vendor").val()
    url = ''
    if(project.length) {
        url = '/view_inventory?project_id='+project.toString()
    } else {
        url = '/view_inventory?project_id=All'
    }
    if(material.length) {
        url += '&material='+material.toString()        
    }
    if (vendor.length) {
        url += '&vendor='+vendor.toString().replaceAll('&',encodeURIComponent('&'))
    } else {
        url += '&vendor='+'All'
    }

    window.location.href = url
})



$("#update_kyp_material").on('click', function(){
    const project = $("#project").val()
    if (project.length) {
        window.location.href = '/kyp_material?project_id='+project.toString()        
    }
})

function runBalances() {
    const total_quantity = {}

    $('.item_quantity').each(function(index, element){
        material = $(element).parent('tr').find('.material').text()
        if(!Object.keys(total_quantity).includes(material)) total_quantity[material] = parseInt($(element).text().trim())
        else total_quantity[material] += parseInt($(element).text().trim())
    })
    console.log(total_quantity)
    $('.material').each(function(index, element){
        if(Object.keys(total_quantity).includes($(element).text())) {
            if ($(element).parents('tr').find('.total_quantity').text().trim() != '') 
            $(element).parents('tr').find('.balance_quantity').text(parseInt($(element).parents('tr').find('.total_quantity').text().trim()) - parseInt(total_quantity[$(element).text()]))
        }
    })

}

runBalances()
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