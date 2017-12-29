function delStatusRecord(id){
	var delID=id;
	if(confirm("确认删除状态记录吗？")){
    	$.ajax({ 
    	type:"POST",
        url: "pbstatusrecord/delete/", 
        cache:false,    
        dataType: "json",
        data: {"id":delID},
        success: function(data) { 
            if (data.status=="Succeed") {
        		alert("删除成功!");
        		location.reload();
            }
            else{
            	alert("删除不了,服务器问题！");
            }
            
            
        },
        error: function(){
    		alert("连不上服务器,网络错误！");
   		}
   		
    	});
    }
    
};

function delStatusRecord(id){
	var delID=id;
	if(confirm("确认删除状态记录吗？")){
    	$.ajax({ 
    	type:"POST",
        url: "pbstatusrecord/delete/", 
        cache:false,    
        dataType: "json",
        data: {"id":delID},
        success: function(data) { 
            if (data.status=="Succeed") {
        		alert("删除成功!");
        		location.reload();
            }
            else{
            	alert("删除不了,服务器问题！");
            }
            
            
        },
        error: function(){
    		alert("连不上服务器,网络错误！");
   		}
   		
    	});
    }
    
};

function openPB(){
	var keyword = $("#pbKey").val();
	if(keyword ==""){alert("不能为空!"); return false;}
	
	$.ajax({
	  type:"post",
	  url:"/task/goujian/search/",
	  cache:false,
	  dataType:"json",
	  data:{"keyword": keyword},
	  success: function(data){
	  	if(data.status=="Succeed"){
	  		window.location.href=data.rePath;
	  	}
	  	else{
	  		alert("没有匹配元素！");
	  	}
	  },
	  error:function(data){
	  	alert("服务器错误");
      	return false;
      },
      complete:function(data){
	  }
	});
}