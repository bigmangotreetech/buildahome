function calcAmount(gst, amount) {
    const total = ((gst / 100 ) * amount) + amount;
    $("#total_amount").val(total)
}

$("#gst").on("change", function(){
    const gst = $(this).val()
    if(gst) {
        const amount = $("#amount").val()
        if (amount) {
           calcAmount(gst, amount)
        }
    }
})

$("#amount").on("change", function(){
    const amount = $(this).val()
    if(gst) {
        const gst = $("#gst").val()
        if (gst) {
           calcAmount(gst, amount)
        }
    }
})