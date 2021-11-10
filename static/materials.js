function calcAmount() {
    const quantity = $('#quantity').val().trim()
    const rate = $("#rate").val().trim()
    const gst = $("#gst").val()
    const amount = parseFloat(rate) * parseFloat(quantity)
    const total = ((gst / 100 ) * amount) + amount;
    $("#total_amount").val(total)
}

$("#gst").on("change",  calcAmount)
$("#rate").on("keyup", calcAmount)
$("#quantity").on("keyup", calcAmount)