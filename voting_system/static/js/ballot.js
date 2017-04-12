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