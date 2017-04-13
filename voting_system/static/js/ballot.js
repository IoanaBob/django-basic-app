function ToggleVoteX(vote_box)
{
	candidate_id = vote_box.id.replace("candidate_box_","");

	current_value = $("#candidate_rank_"+candidate_id).val();

	if(current_value == 0)
	{
		$(".ballot_rank").val(0);
		$(".vote_x_img").css("display","none");

		$("#candidate_rank_"+candidate_id).val(1);
		$("#candidate_x_"+candidate_id).css("display","block");
	}
	else
	{
		$("#candidate_rank_"+candidate_id).val(0);
		$("#candidate_x_"+candidate_id).css("display","none");
	}
}


function CollectVoteData()
{
	var ranks = $(".ballot_rank");
	var rank_dict = {};
	for (let rank of ranks)
	{
		if(rank.value > 0)
		{	
			candidate_id = rank.id.replace("candidate_rank_","");
			rank_dict[candidate_id] = rank.value;
		}
	}


	var rank_string = JSON.stringify(rank_dict);

	$("#rank_data").val(rank_string);
}