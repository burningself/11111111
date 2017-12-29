function changestatus(obj){
	var sdate={
		'hazardid':obj.parentNode.parentNode.getAttribute('value'),
		'status':obj.getAttribute('value')
	}
	
    $.ajax({
		type:"post",
		url:"/task/anquan/hazard/list/",
		dataType:"json",
		async:true,
		data:sdate,
		success: function(data){
			obj.innerHTML=data.status
			obj.setAttribute('value',data.statusid)
		},
		error: function(e){
			if(e.status==403){
				alert("您没有权限编辑危险源，请联系管理员！");
			}
		}
	});
}