// In your Javascript (external .js resource or <script> tag)
$(document).ready(function() {
    $('.select2').select2();

    $(".update_trades_for_project").on('change', function(){
        const project_id = $(this).val()

        if (project_id) {
            $('.select_trade_for_bill').removeClass('d-none')
            $.ajax({
              url: '/material/update_trades_for_project',
              type: "POST",
              dataType: 'json',
              data: {'project_id': project_id},
              success: function(data){
                  console.log(data)
                  for(const trade of data) {
                    $(".select_trade_for_bill select").append($("<option></option>")
                    .attr("value", trade)
                    .text(trade))
                  }
              }
            });
        } else {
            $('.select_trade_for_bill').addClass('d-none')
        }
         $(".select_trade_for_bill select").select2()
   })

   $(".select_trade_for_bill select").on('change', function(){
        const trade = $(this).val()
        if (trade) {
            project_id = $("#project").val()
            $('.select_payment_stage').removeClass('d-none')
            $.ajax({
              url: '/material/update_payment_stages',
              type: "POST",
              dataType: 'json',
              data: {'project_id': project_id, 'trade': trade},
              success: function(data){
                  console.log(data)
                  console.log(data['stages'])
                  for(const stage of Object.keys(data['stages'])) {
                    $(".select_payment_stage select").append($("<option></option>")
                    .attr("value", stage)
                    .text(stage))
                  }
              }
            });
        } else {
            $('.select_payment_stage').addClass('d-none')
        }
   })

});

