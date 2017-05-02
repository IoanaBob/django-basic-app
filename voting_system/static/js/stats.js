function UpdateGraphs()
{
var election_id = '34';
var region_id = $("#region_filter").val();

if(region_id != "")
{
        $.ajax({
      url: '/administration/statistics/get_graph/' + election_id + '/' + region_id,
      
      success: function(data) {
        $('#graph_container').html(data);
       
      }
    });
}
}