function calcAmount() {
    const quantity = $('#quantity').val().trim()
    const rate = $("#rate").val().trim()
    const gst = $("#gst").val()
    const loading_unloading = $('#loading_unloading').val()
    const transportation = $('#transportation').val()
    const amount = parseFloat(rate) * parseFloat(quantity) 
    const total = ((gst / 100 ) * amount) + amount;
    const total_with_other_expenses = amount + parseFloat(loading_unloading) + parseFloat(transportation)
    $("#total_amount").val(total_with_other_expenses)
}

$("#gst").on("change",  calcAmount)
$("#rate").on("keyup", calcAmount)
$("#quantity").on("keyup", calcAmount)
$("#transportation").on("keyup", calcAmount)
$("#loading_unloading").on("keyup", calcAmount)