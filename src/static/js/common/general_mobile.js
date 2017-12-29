$(document).ready(function() {
	$('#calendar').fullCalendar({
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'listMonth,month,agendaWeek,agendaDay'
		},
//		displayEventTime: false, // don't show the time column in list view
		defaultDate: getNowFormatDate(),
		defaultView: 'listMonth',
		locale: 'zh-cn',
		navLinks: true, // can click day/week names to navigate views
		businessHours: true, // display business hours
		editable: true,
		eventOrder: 'order',
		events: {
			url: "/assist/todolist/",
			type: 'post'
		},
		events: function(start, end, timezone, callback) {
			$.ajax({
				url: "/assist/todolist/",
				dataType: 'json',
				data: {
					start: start.unix(),
					end: end.unix()
				},
				type: 'post',
				success: function(data) {

					callback(data.todolist);
					
					//滚动到当天
			 		var curDate = getNowFormatDate();
			        var offsettop = $(".fc-list-heading[data-date='"+curDate+"']").offset().top;
					$(".fc-scroller").scrollTop($(".fc-scroller").scrollTop() + offsettop - $(".fc-scroller").offset().top); 
				}
			});
		},
		eventMouseover: function(calEvent, jsEvent, view) {
			var fstart = moment(calEvent).format('YYYY/MM/DD HH:mm');
			var fend = moment(calEvent).format('YYYY/MM/DD HH:mm');
			$(this).attr('title', calEvent.contant);
			//				$(this).attr('title', calEvent);
			//				$(this).css('font-weight', 'normal');
			//				$(this).tooltip({
			//					effect: 'toggle',
			//					cancelDefault: true
			//				});
		},

	});
	loadTableData("zhiliangTable", 2);
	loadTableData("anquanTable", 3);
	
	loadPbCount();
	
	loadPersonCount();
	
});


function getNowFormatDate() {
	var date = new Date();
	var seperator1 = "-";
	var seperator2 = ":";
	var month = date.getMonth() + 1;
	var strDate = date.getDate();
	if(month >= 1 && month <= 9) {
		month = "0" + month;
	}
	if(strDate >= 0 && strDate <= 9) {
		strDate = "0" + strDate;
	}
	var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate
	return currentdate;
}

function loadTableData(tableName, type) {
	donut_data = [];
	weichulizongshu = '';
	$.ajax({
		type: "post",
		url: "/index/table/",
		cache: false,
		dataType: "json",
		data: { "type": type },
		success: function(data) {
			if(data.status == "Succeed") {
				var tmpHtml = "";
				for(each in data.list_items_head) {
					if(data.list_items_head[each] != '') {
						tmpHtml = tmpHtml + "<th>" + data.list_items_head[each] + "</th>";
					}
				}
				$("." + tableName + "> thead > tr").html(tmpHtml);
				zongji = data.list_items.pop()
				var tmp = "<tr>";
				tmp += "<td>";
				tmp += zongji.专业;
				tmp += "</td>";
				tmp += "<td>";
				tmp += zongji.已处理;
				tmp += "</td>";
				tmp += "<td>";
				tmp += zongji.未处理;
				tmp += "</td>";
				tmp += "</tr>";
				$("." + tableName + "> tfoot ").append(tmp);
				var weichulizongshu = zongji.未处理;
				var donut_data = [];
				$.each(data.list_items, function() {

					var tmp = "<tr>";
					tmp += "<td>";
					tmp += this.专业;
					tmp += "</td>";
					tmp += "<td>";
					tmp += this.已处理;
					tmp += "</td>";
					tmp += "<td>";
					tmp += this.未处理;
					tmp += "</td>";
					tmp += "</tr>";
					$("." + tableName + "> tbody ").append(tmp);

					if(this.未处理 != '0') {
						var ddata = {}
						ddata.label = this.专业;
						ddata.value = this.未处理 + "/" + weichulizongshu;
						donut_data.push(ddata);

					}

				});
//				donut(tableName, donut_data);
				return true;
			}
		},
		error: function(data) {
			//		  	alert("无法获取配置信息！");
			return false;
		},
		complete: function(data) {}
	});
}

function loadPbCount(){
	
		$.ajax({
		type: "get",
		url: "/task/goujian/pbcountdesc/",
		cache: false,
		dataType: "json",
		success: function(data) {
		   if(data.issuc == "true") {
					
				var weekly='';
				for(var major in data.list_obj_weekly){
					weekly+=' <div class="weui_media_box weui_media_text">';
					weekly+=' <h4 class="weui_media_title">'+ major +'</h4>';
					
					for(var status in data.list_obj_weekly[major]){
						weekly+=' <p class="weui_media_desc_custom">';
						for(var pb in data.list_obj_weekly[major][status]){
							if(pb!=(data.list_obj_monthly[major][status].length-1)){
								weekly+=data.list_obj_weekly[major][status][pb]+"、"
							}else{
								weekly+=data.list_obj_weekly[major][status][pb]
							}
						}
						weekly+=status;
						weekly+='</p>';
					}
					weekly+=' </div>';
				}
				$("#weeklydate").html(data.weekstartdate+"-"+data.weektenddate);
				$("#pbweekly").html(weekly);
			
					
				var monthly='';
				for(var major in data.list_obj_monthly){
					monthly+=' <div class="weui_media_box weui_media_text">';
					monthly+=' <h4 class="weui_media_title">'+ major +'</h4>';
					
					for(var status in data.list_obj_monthly[major]){
						monthly+=' <p class="weui_media_desc_custom">';
						for(var pb in data.list_obj_monthly[major][status]){
							if(pb!=(data.list_obj_monthly[major][status].length-1)){
								monthly+=data.list_obj_monthly[major][status][pb]+"、"
							}else{
								monthly+=data.list_obj_monthly[major][status][pb]
							}
						}
						monthly+=status;
						monthly+='</p>';
					}
					monthly+=' </div>';
				}
				$("#monthlydate").html(data.monthstartdate+"-"+data.monthenddate);
				$("#pbmonthly").html(monthly);
				
			}else{
				console.log(data.error);
			}
		},
		error: function(data) {
			
		},
		complete: function(data) {}
	});
}

function loadPersonCount(){
		$.ajax({
			type:'post',
			url:'http://1716a0w046.imwork.net:21639/vms-guilinroad-webapp/appDataInterface/gettoken.do',
			dateType:'json',
			cache: false,
			data:{
				"param":"sijian/sijian",
			},
		  success: function(data){
			  	sessionStorage.setItem('token', data.token);
				console.log(data);
				//调用区域信息接口
				$.ajax({
					type: 'get',
					url: 'http://1716a0w046.imwork.net:21639/vms-guilinroad-webapp/appDataInterface/getzones.do',
					dateType: 'json',
					cache: false,
					data:{
						"param":sessionStorage.getItem('token'),
					},
					success: function(data) {
						console.log('获取数据成功'+"获取区域信息");
						
						var html = ""
						if(data.message == "查询区域失败"){
                            console.log(data);
						}else {
							
							var total = 0;
							for(var i = 0;i<data.zones.length;i++){
								total+= data.zones[i].count;
						    } 
							html +=`<div class="weui_cell">
						            <div class="weui_cell_bd weui_cell_primary">
						                    现场总人数
						            </div>
						            <div class="weui_cell_ft weui-badge">`+total+`人</div>
					          </div>`
							
                            for(var i = 0;i<data.zones.length;i++){
                            	var name = '其他区域总人数'
                            	if(data.zones[i].name=="闸口区域"){
								    			name = "欢迎区总人数"
								    		}else if(data.zones[i].name=="区域一"){
								    			name = "BIM区总人数"
								    		}else if(data.zones[i].name=="区域二"){
								    			name = "VR区总人数"
								    		}else if(data.zones[i].name=="区域三"){
								    			name = "平台区总人数"
								    		}
                            	
                                html +=`<div class="weui_cell">
						            <div class="weui_cell_bd weui_cell_primary">
						                    `+name +`
						            </div>
						            <div class="weui_cell_ft">`+data.zones[i].count+`人</div>
					          	</div>`

                            }
                            
                            $("#personcount").html(html);
     
                           

						}
					},
					error: function(data) {
						console.log('调用失败');				
					}
		
				});
		
			
		  }
	});

}
