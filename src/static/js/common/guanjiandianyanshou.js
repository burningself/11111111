var bdcontents=[];
var formids = [];
function getForms(){
	$.ajax({
		type:"post",
//		url:"/task/zhiliangyanshou/guanjiandian/8/",
//		async:true,
		dataType: "json",
//		data: jsonobj,
		success: function(data) {
			$(".bdname").append("<li class='active' ><a  data-toggle='tab' href='#' onclick='changeeditcontent(this)' value='0'>"+ data[0].name +"</a></li>")
			bdcontents.push(data[0].content);
			formids.push(data[0].id);
			for(var i=1;i<data.length;i++){
				$(".bdname").append("<li><a data-toggle='tab' href='#' onclick='changeeditcontent(this)' value='"+ i +"'>"+ data[i].name +"</a></li>")
				bdcontents.push(data[i].content);
				formids.push(data[i].id);
			}
			setContent(data[0].content);
		}
	});
}

var index=0;
function changeeditcontent(obj){
	bdcontents[index] = getContent();
	index = $(obj).attr('value');
	setContent(bdcontents[index]);
}

function initUE(){
	ue = UE.getEditor('editor',{
		initialFrameHeight:600,
	    autoHeightEnabled: true,
	    autoFloatEnabled: true
	});
}
function yanshousaveallform(){
	for(var i=0;i<formids.length;i++){
		if(i==index){
			yanshousaveoneform(formids[i],getContent())
		}else{
			yanshousaveoneform(formids[i],bdcontents[i])
		}
		
	}
	window.opener.location.reload();
	window.close();
}


function yanshousaveoneform(sid,sc){
	var dat = {
		"id":sid,
		"content":sc
	}
 	$.ajax({
 	  type:"post",
 	  url:"/assist/biaodan/",
 	  async: false,
 	  data:JSON.stringify(dat),
 	  success: function(data){
 	  	if(data.res='succ'){
 	  		// confirm('保存成功')
 	  	}
 	  }
 	  
 	  
 	});
}
