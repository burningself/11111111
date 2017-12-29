$(document).ready(function() {
	$('#calendar').fullCalendar({
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'listMonth,month,agendaWeek,agendaDay'
		},
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
					
					$('#calendar a').attr("target","_blank");
					
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
	
	$("#selectdefaultunitprj").change(function() {
	var defaultunitId = $("#selectdefaultunitprj option:selected").val();
	$.ajax({
		type: "get",
		url: "/task/modelview/setinitialmodel/",
		cache: false,
		//async: false,
		dataType: "json",
		data: { "defaultunitId": defaultunitId, },
		success: function(data) {
			if(data.issuc == "true") {
				var r = confirm("设置成功！是否重新加载默认单位工程？");
				if(r == true) {
					loadInitialModel();
				}

			} else {
				alert(data.error);
				return;
			}

		}
	});
});

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

$(window).ready(function() {

	// Load Weather
	loadWeather();

	//adjust css
	adjust_ccs();

	//load Table Data
	//	loadTableData("areaTable",0);
	//  loadTableData("jishuTable",1);
	loadTableData("zhiliangTable", 2);
	loadTableData("anquanTable", 3);
	// load configuration
	loadConfig();

	//  init datePicker
	//	initDate_Picker();
	//init BIM
	//  initializeBIM();
});

//Load weather
function loadWeather() {
	$('.skycons-element').each(function() {
		var canvasId, skycons, weatherSetting;
		skycons = new Skycons({
			color: "#337AB7"
		});
		canvasId = $(this).attr('id');
		weatherSetting = $(this).data('skycons');
		skycons.add(canvasId, Skycons[weatherSetting]);
		return skycons.play();
	});
}

// configuration modal
function customPage() {
	$('#configPage').modal('show');
}

function chooseAll() {
	$('input[name="configBox"]').each(function() {
		$(this).click();
	});
}

function chooseNone() {
	$('input[name="configBox"]').each(function() {
		$(this).removeAttr("checked");
	});
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
					if(typeof(data.list_items_head[each]) == 'string') {
						tmpHtml = tmpHtml + "<th>" + data.list_items_head[each] + "</th>";
					}
				}
				$("." + tableName + "> thead > tr").html(tmpHtml);
				zongji = data.list_items.pop()
				var tmp = "<tr>";
				tmp += "<td>";
				//tmp += '<i class="fa fa-trophy" style="color: rgb(255, 0, 0);"></i>'
				tmp += "</td>";
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
					//						tmp += '<i class="fa fa-trophy" style="color: rgb(255, 0, 0);"></i>'
					tmp += "</td>";
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
				donut(tableName, donut_data);
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

function donut(tablename, d) {
	var ele;
	if(tablename == 'anquanTable') {
		ele = 'anquan_donut';
	} else if(tablename == 'zhiliangTable') {
		ele = 'zhiliang_donut';
	}
	ceshi = {
		element: ele,
		data: d,
		colors: ["rgb(255, 0, 0)", "rgb(0, 153, 153)","rgb(255, 116, 0)",  "rgb(0, 204, 0)"],
		formatter: function(y) { return y },
		resize: true
	}
	Morris.Donut(ceshi);
}

function loadConfig() {
	var username = $('#username').attr('class');
	var pagePath = window.location.pathname;
	var pro = window.location.hostname;
	$.ajax({
		type: "get",
		url: "/user/costomPage/",
		cache: false,
		dataType: "text",
		data: {
			"user": username,
			"pagePath": pagePath,
			"pro": pro
		},
		success: function(data) {
			if(data != "Failed" && data != "Succeed") {
				var configArray = data.split(":");
				console.log(configArray);
				if(configArray) {
					for(var i in configArray) {
						$("#" + configArray[i]).css("display", 'none');
					}
				}

				$('input[name="configBox"]').each(function() {
					if($.inArray($(this).val(), configArray) >= 0) { $(this).attr("checked", "checked"); }
				});
			}
			return true;
		},
		error: function(data) {
			//		  	alert("无法获取配置信息！");
			return false;
		},
		complete: function(data) {}
	});
}

function submitConfig() {
	var username = $('#username').attr('class');
	var saveName = $("#saveName").val();
	var configData = [];
	var pagePath = window.location.pathname;
	var pro = window.location.hostname;
	$('input[name="configBox"]:checked').each(function() {
		configData.push($(this).val());
	});

	if(pagePath && pro && username) {
		$.ajax({
			type: "post",
			url: "/user/costomPage/",
			cache: false,
			dataType: "text",
			data: {
				"user": username,
				"savename": saveName,
				"configData": configData.join(":"),
				"pagePath": pagePath,
				"pro": pro
			},
			success: function(data) {
				if(data == "Succeed") {
					$('#configPage').modal('hide');
					$('input[name="configBox"]').each(function() {
						if($(this).val() == 'weather_notice') {
							$("#" + $(this).val()).css("display", "block");
						} else {
							$("#" + $(this).val()).css("display", "inline-block");
						}
					});
					for(var i in configData) {
						$("#" + configData[i]).css("display", 'none');
					}

				}
				return true;
			},
			error: function(data) {
				alert("信息不全！");
				return false;
			},
			complete: function(data) {}
		});
	} else { alert("信息不全！"); }
}

//adjust css
function adjust_ccs() {
	if($(window).height() > 450) {
		var stdH = ($(window).height() - 450) / 2;
		$(".row-fluid").height(263);
		

		$(".row-fluid .draw_row").height(stdH - 70);
		$(".row-fluid .list_row").height(stdH - 45);

		//		if(stdH<=250){
		//			$(".table-filters tbody tr td ").css("padding",(35/12).toString()+ "px");
		//		}
		//		else if(stdH>250 && stdH <=350){
		//			$(".table-filters tbody tr td ").css("padding",((stdH-215)/12).toString()+ "px");
		//		}
		//		else{
		//			$(".table-filters tbody tr td ").css("padding",((350-215)/12).toString()+ "px");
		//		}
	}
}

function initDate_Picker() {
	$('#dateConfig').datetimepicker({
		format: 'yyyy-mm',
		language: 'zh-CN',
		todayBtn: 0,
		autoclose: 1,
		todayHighlight: 1,
		startView: 3,
		minView: 3,
		forceParse: 1,
		initialDate: new Date(),
		endDate: new Date(),
	}).on("changeDate", function(dateStr) {
		var ins = new Date();
		var chooseMonth = dateStr.date.getMonth();
		var chooseYear = dateStr.date.getFullYear();
		var curMonth = ins.getMonth();
		var curYear = ins.getFullYear();
		var dis = curYear * 12 + curMonth - chooseYear * 12 - chooseMonth + 1;
		ins.setMonth(chooseMonth);
		ins.setYear(chooseYear);
		var chooseIns = ins.valueOf();

		ins = new Date();
		if(ins.getMonth() > 5) {
			ins.setMonth(ins.getMonth() - 5);
		} else {
			ins.setMonth(ins.getMonth() - 5 + 12);
			ins.setYear(ins.getFullYear() - 1);
		}
		var latest = ins.valueOf();

		ins = new Date();
		ins.setYear(ins.getFullYear() - 1);
		var earlest = ins.valueOf();

		if(dis < 5 || dis > 12) {
			$('#datetConfig').datetimepicker('hide');
			alert("可用时间范围：距今5-12个月！");
			return 0;
		} else {
			pbtype = $(".month-filter").children('option:selected').val();
			eleClass = $(this).attr("class");
			$(".month-duration").html(dis);

			$.ajax({
				type: "post",
				url: "/index/data/",
				cache: false,
				dataType: "json",
				data: { 'reqType': 'line', "keyword": pbtype, "duration": dis },
				success: function(data) {
					if(data.status == "Succeed") {
						var monthData = new Array();
						for(var i = 0; i < data.monthCountList.length; i++) {
							var tmpDic = new Array();
							tmpDic["month"] = data.monthCountList[i].date;
							tmpDic["jihua"] = data.monthCountList[i].jihua;
							tmpDic["anzhuang"] = data.monthCountList[i].anzhuang;
							monthData[i] = tmpDic;
						}

						if($('#month-line').length) {
							$("#month-line").html('');
							Morris.Line({
								element: "month-line",
								data: monthData,
								xkey: 'month',
								ykeys: ['jihua', 'anzhuang'],
								labels: ['计划安装完成', '安装完成'],
								hideHover: true,
								gridTextColor: "black",
								lineWidth: 2,
								pointSize: 4,
								lineColors: ["lightgreen", "#67BDF8"],
								fillOpacity: 0.5,
								smooth: true,
								ymax: 'auto',
								parseTime: false,
								resize: true
							});
						}
					} else {
						alert("没有匹配构件信息！");
					}
				},
				error: function(data) {
					//		  	alert("服务器错误");
					return false;
				},
				complete: function(data) {}
			});
		}

	});

	$('#datetimeselect').datetimepicker({
		language: 'zh-CN',
		weekStart: 1,
		todayBtn: 1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 2,
		minView: 2,
		forceParse: 0
	}).on("changeDate", function(dateStr) {
		var cdate = dateStr.date;
		var chooseDate = cdate.getFullYear() + "/" + (cdate.getMonth() + 1) + "/" + cdate.getDate();
		var weekData = new Array();
		pbtype = $(".week-filter").children('option:selected').val();
		eleClass = $(this).attr("class");
		$.ajax({
			type: "post",
			url: "/index/data/",
			cache: false,
			dataType: "json",
			data: { 'reqType': 'line', "keyword": pbtype, "chooseDate": chooseDate },
			success: function(data) {
				if(data.status == "Succeed") {
					for(var i = 0; i < data.weekCountList.length; i++) {
						var tmpDic = new Array();
						tmpDic["day"] = data.weekCountList[i].date;
						for(var j = 0; j < data.weekCountList[i].countlist.length; j++) {
							tmpDic[data.weekCountList[i].countlist[j].key] = data.weekCountList[i].countlist[j].value;
						}
						weekData[i] = tmpDic;
					}

					var ykeysValues = new Array();
					var labelsValues = new Array();
					var ColorsValues = new Array();
					for(var i = 0; i < data.weekCountTypeList.length; i++) {
						ykeysValues[i] = data.weekCountTypeList[i].key;
						labelsValues[i] = data.weekCountTypeList[i].name;
						ColorsValues[i] = data.weekCountTypeList[i].color;

					}

					if($('#week-line').length) {
						$("#week-line").html('');
						Morris.Line({
							element: "week-line",
							data: weekData,
							xkey: 'day',
							ykeys: ykeysValues,
							labels: labelsValues,
							hideHover: true,
							gridTextColor: "black",
							lineWidth: 2,
							pointSize: 4,
							lineColors: ColorsValues,
							fillOpacity: 0.5,
							smooth: true,
							ymax: 'auto',
							parseTime: false,
							resize: true,
						});
					}
				} else {
					alert(data.error);
				}
			},
			error: function(data) {
				//		  	alert("服务器错误");
				return false;
			},
			complete: function(data) {}
		});

	});
}
