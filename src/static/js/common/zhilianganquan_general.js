function getissuelist(issuetype){
	//issuetype = 质量问题 质量验收 安全问题 危险源
	$.ajax({
		type:"get",
		url:"/task/issue/list/general/",
  		cache: false,
  		dataType: "json",
  		data: {
  			"_selElevations": _selElevations,
  			"_selPbtypes": _selPbtypes,
  			"_curUnitId": _curUnitId,
  			"_selZones":_selZones,
  			"_curMajor":_curMajor,
  			"_selectedId":_selectedId,
  			"issuetype":issuetype
  		},
		success: function(data){
			if(data.res=='succ'){
				if(issuetype=='zhiliang'||issuetype=='anquan'){
					$(".issuetable tr").remove();
					$.each(data.ilist, function() {
						var tmp  = '<tr id="trissue_'+this.issueId+'">';
							tmp += 		'<td style="width:64%;text-align: left;word-break:break-all;"><a href="#" onclick="filterPblistByIssue(\''+issuetype+'\','+this.issueId+')" >'+this.number+'</a></td>';
							tmp += 		'<td style="vertical-align:middle;background:'+ this.dangqianjieduan.color +'; color:ghostwhite; cursor:pointer; " title="点击处理">';
							tmp += 		'<a href="/task/issue/issuedeal/'+this.issueId+'/" style="color:white;" target="_blank">'+this.dangqianjieduan.jianduan+'</a>';
							tmp += 		'</td>';
						 	tmp += '</tr>';

						$(".issuetable").append(tmp);
					}); 
				}
				else if(issuetype=='zhiliangyanshou'){
					$(".yanshoutable tr").remove();
					$.each(data.ilist, function() {
						if(this.status=='3'){
							return true;
						}
						var tmp  = '<tr>';
							tmp += '<td style="width:64%;text-align: left;word-break:break-all;"><a href="#" onclick="filterPblistByIssue(\''+issuetype+'\','+this.id+')" >'+this.kjys+'</a></td>';
							if(this.status=='1'){
								tmp += '<td style="background: #DE0404;color: white;vertical-align:middle;">';
								tmp += '<a href="/task/zhiliangyanshou/yanshou/'+this.id+'/" style="color:white;" target="_blank">未处理</a>';
							}else if(this.status=='2'){
								tmp += '<td style="background: #fa800a;color: white;vertical-align:middle;">';
								tmp += '<a href="/task/zhiliangyanshou/yanshou/'+this.id+'/" style="color:white;" target="_blank">处理中</a>';
							}

							tmp += '</td>';
							tmp += '</tr>';
						
						$(".yanshoutable").append(tmp);
					});	
				}
				else if(issuetype=='weixianyuan'){
					$(".weixianyuantable tr").remove();
					$.each(data.ilist, function() {
						var tmp  = '<tr>';
							tmp +='<td style="width:64%;text-align: left;word-break:break-all;"><a href="#" onclick="filterPblistByIssue(\''+issuetype+'\','+this.id+')" >'+this.name+'</a></td>'
							if(this.curstatus=='受控'){
								tmp += '<td style="background:#008040; color:ghostwhite; cursor:pointer;vertical-align:middle; text-align: center; ">'
							}else{
								tmp += '<td style="background:#DE0404; color:ghostwhite; cursor:pointer;vertical-align:middle; text-align: center;">'
							}
							tmp += '<a style="color:ghostwhite;" href="#" onclick="changestatus(this,'+this.id+')" >'+this.curstatus+'</a>'
							tmp += '</td>'
							tmp += '</tr>';
						$(".weixianyuantable").append(tmp);
					});	
				}
				
			}
		},
	});
}

function changestatus(obj,haid){
	var sdate={
		'hazardid':haid,
	}
    $.ajax({
		type:"post",
		url:"/task/anquan/hazard/list/",
		dataType:"json",
		async:true,
		data:sdate,
		success: function(data){
			obj.innerHTML=data.status;
			if(data.status=='受控'){
				obj.parentNode.style.background='#008040';
			}else{
				obj.parentNode.style.background='#DE0404';
			}
			
		}
	});
}