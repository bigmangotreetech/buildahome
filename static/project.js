// In your Javascript (external .js resource or <script> tag)
$(document).ready(function() {
    $('.select2').select2();

    $(".update_trades_for_project").on('change', function(){
        const project_id = $(this).val()
        $(".select_trade_for_bill select").select2()
        if (project_id) {
            $('.select_trade_for_bill').removeClass('d-none')
            $.ajax({
              url: '/material/update_trades_for_project',
              type: "POST",
              data: {'project_id': project_id},
              success: function(data){
                  console.log(data);
              }
            });
        } else {
            $('.select_trade_for_bill').addClass('d-none')
        }

    })

});

