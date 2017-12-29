
$().ready(function(){
	$("#searchPb").bind("input", function() { 
		var keyword=$("#searchPb").val();
		$(".positionNum").each(function(){
			$(this).css("color","black");
		})
		if(keyword==""){
			return;
		}
		$.ajax({
		  type:"POST",
		  url:"/task/factoryarea/pblist/search/",
		  cache:false,
		  dataType:"json",
		  data:{ "keyword": keyword },
		  success: function(data){
		  	if(data.status!="Failed"){
		  		if(data.positionList.length){
		  			for(each in data.positionList){
			  			$("#"+data.positionList[each] + " .positionNum").css("color","red");
			  		}
			  	}
		  	}
		  	return true;
		  },
		  error:function(data){
	      	return false;
	      },
	      complete:function(data){
			}
		});	
	});
});

function fetchPB(id){
	if($("#pbList")){ $("#pbList").modal('show'); }
	$.ajax({
	  type:"POST",
	  url:"/task/factoryarea/pblist/",
	  cache:false,
	  dataType:"json",
	  data:{ "fpid": id },
	  success: function(data){
	  	if(data.status!="Failed"){
	  		var optContent="";
	  		if(data.headerList.length && data.pbList.length){
	  			var html="<thead>";
	  			for(each in data.headerList){
		  			html = html + "<th>" + data.headerList[each] + "</th>";
		  		}
	  			
	  			html=html + "</thead><tbody>";
	  			
		  		for(each in data.pbList){
		  			html = html + "<tr>";
		  			for(eachIndex in data.headerList){
		  				if(eachIndex==0){
		  					html = html + "<td><a href='/task/goujian/trace/?pbid=" + data.pbList[each]["pbid"].toString() + "' >" + data.pbList[each][data.headerList[eachIndex]] + "</a></td>";
		  				}
		  				else{
		  					html = html + "<td>" + data.pbList[each][data.headerList[eachIndex]] + "</td>";
		  				}
		  			}
		  			html = html + "</tr>";
		  		}
		  		
		  		html=html + "</tbody>";
		  		$("#pbTable").html(html);
		  	}
	  		else{
	  			$("#pbTable").html('<p style="font-size:20px; text-align:center; margin:50px; text-decoration: underline;">没有关联构件信息！</p>');
	  			
	  		}	
	  	}
	  	return true;
	  },
	  error:function(data){
      	return false;
      },
      complete:function(data){
		}
	});
}
