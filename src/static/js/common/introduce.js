
function combinElement(index,picName,content){
	var html = ""
	if(index==0){
		html+='<div class="item active"><img src="/img/' + picName + '" alt="' + picName + '">'
	}
	else{
		html+='<div class="item"><img src="/img/' + picName + '" alt="' + picName + '">'
	}
	
	if(content.length > 40)
		html+='<br><label style="width:60%; text-align: left;">' + content + "</label></div>";
	else
		html+='<br><label style="width:60%;">' + content + "</label></div>";
	return html;
}

function combinIndicator(len){
	var html = "";
	var i=0;
	while(i<len){
		if(i==0)
			html+='<li data-target="#mycarousel" data-slide-to="0" class="active"></li>';
		else
			html+='<li data-target="#mycarousel" data-slide-to="' + i.toString() + '"></li>';
		i++;	
	}
	document.getElementById("indicatorID").innerHTML=html;
}


var loaded = false; 
$(document).ready(function(){
  if (loaded){ 
   	return true;
  }
  
  loaded=true;
  winWidth = window.innerWidth;	
  var hgh = document.body.clientHeight / 1.5;
  var wid = document.body.clientWidth / 1.5;
  
  $.ajax({
	  type:"post",
	  url:"/photoResize/",
	  cache:false,
	  dataType:"json",
	  data:{"width":parseInt(wid).toString(), "height": parseInt(hgh).toString()},
	  success: function(data){
	  	if(data.status=="Succeed"){
	  		combinIndicator(data.fileList.length);
	  		html = "";	  		  		
	  		for(index in data.fileList){
	  			html += combinElement(index,data.fileList[index],data.contentList[index]);	
	  		}
	  		
	  		leftObj = $("#carousel_left").css("display","inline");
	  		rightObj = $("#carousel_right").css("display","inline");
	  		document.getElementById("carousel_left").outerHTML=leftObj.prop('outerHTML');
	  		document.getElementById("carousel_right").outerHTML=rightObj.prop('outerHTML');
	  		
	  		$("#mycarouselID").html(html);
	  		
	  		$('#mycarousel').carousel()  
	  	}
	  	return true;
	  },
	  error:function(data){
	  	alert("image load error");
      	return false;
      },
      complete:function(data){
		}
	});

});

  
