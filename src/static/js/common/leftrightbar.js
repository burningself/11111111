var flagLeft = true;
var flagRight = true;

function adjustViewer(a){
	$("#viewerContent").animate({
			width: $("#viewerContent").width() + a
	}, 500);
	
	$(".canvas-wrap > canvas").animate({
		width: $(".canvas-wrap > canvas").width() + a
	}, 500);
}

$(".left-control").click(function() {
	if(flagLeft) {
		$("#left").animate({
			marginLeft: "-240px"
		}, 500);
		$(".left-control").html("<i class='fa fa-caret-right'></i>");
		$(".left-control").animate({
			left: "0px"
		}, 500);
		
		adjustViewer(242);
		
		flagLeft = false;
	} else {
		adjustViewer(-238);
		
		$("#left").animate({
			marginLeft: "0px"
		}, 500);
		$(".left-control").html("<i class='fa fa-caret-left'></i>");
		$(".left-control").animate({
			left: "240px"
		}, 500);

		flagLeft = true;
	}
})

$(".right-control").click(function() {
	if(flagRight) {
		$(".more").css("display", "none");
		$("#right").animate({
			marginRight: "-240px"
		}, 500);
		$(".right-control").html("<i class='fa fa-caret-left'></i>");
		$(".right-control").animate({
			right: "0px"
		}, 500);
		
		adjustViewer(242);
		
		flagRight = false;
	} else {
		adjustViewer(-238);
		
		$("#right").animate({
			marginRight: "0px"
		}, 500);
		$(".right-control").html("<i class='fa fa-caret-right'></i>");
		$(".right-control").animate({
			right: "240px"
		}, 500);
		$(".more").css("display", "inline-block");

		flagRight = true;
	}
})