function calcAmount() {
    const quantity = $('#quantity').val().trim()
    const rate = $("#rate").val().trim()
    const gst = $("#gst").val()
    const loading_unloading = $('#loading_unloading').val()
    const transportation = $('#transportation').val()
    const amount = parseFloat(rate) * parseFloat(quantity) 
    const total = ((gst / 100 ) * amount) + amount;
    const total_with_other_expenses = total + parseFloat(loading_unloading) + parseFloat(transportation)
    $("#total_amount").val(total_with_other_expenses)
}

$('.dropdown ').on('show.bs.dropdown', function () {
    $('.main-wrapper').css('zIndex','-1')
})
$('.dropdown ').on('hide.bs.dropdown', function () {
    $('.main-wrapper').css('zIndex','0')
})

$("#gst").on("change",  calcAmount)
$("#rate").on("keyup", calcAmount)
$("#quantity").on("keyup", calcAmount)
$("#transportation").on("keyup", calcAmount)
$("#loading_unloading").on("keyup", calcAmount)