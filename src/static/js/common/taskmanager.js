var _selVersionId = null;
var g = null;
var uploaddocs=[];
var uploaddocsQianZheng=[];

$(function() {
	wgetFit();




	$.myloading({
		title: "进度计划比对中，请稍后……"
	});

	g = new JSGantt.GanttChart(document.getElementById('GanttChartDIV'), 'month');
	if(g.getDivId() != null) {

		initGantChart(g);

		$.ajax({
			type: "get",
			url: "/task/projecttask/getprojecttasklist",
			cache: false,
			// async: false,
			dataType: "json",
			data: {},
			success: function(data) {
				if(data.issuc == "true") {
					for(var each in data.projecttasklist) {
						if(each == "remove")
							continue;
						g.AddTaskItem(new JSGantt.TaskItem(data.projecttasklist[each].pID, data.projecttasklist[each].pName, data.projecttasklist[each].pStart, data.projecttasklist[each].pEnd, data.projecttasklist[each].pStyle, "", 0,
							"", data.projecttasklist[each].pComp, data.projecttasklist[each].pGroup, data.projecttasklist[each].pParent, data.projecttasklist[each].pOpen,
							"", "", "", "g"));
					}
					g.Draw();
					$.myloading("hide");

					//$('#divProgressAnimateTitle').hide();
					//$('#divProgressAnimate').hide();

					
				} else {
					alert(data.error);
				}
			}
		});
	} else {
		$.myloading("hide");
		alert("Error, unable to create Gantt Chart");
	}

	$('.datetimeselect').datetimepicker({
		language: 'zh-CN',
		weekStart: 1,
		todayBtn: 1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 2,
		minView: 2,
		forceParse: 1
	});

		$('#filer_input').filer({
		showThumbs: true,
		fileMaxSize:100,
		limit:5,
		addMore: false,
		extensions: ["mpp", "jpg"],
		allowDuplicates: false,
		captions:{
		    button: "选择MicrosoftProject文件",
		    feedback: "",
		    feedback2: "个文件已选择",
		    drop: "拖到文件到这里",
		    removeConfirmation: "是否移除文件？",
		    errors: {
		        filesLimit: "只能同时上传 {{fi-limit}}个文件 。",
		        filesType: "只能上传MicrosoftProject文件",
		        filesSize: "{{fi-name}} 太大! 最大允许上传 {{fi-fileMaxSize}} MB。",
		        filesSizeAll: "Files you've choosed are too large! Please upload files up to {{fi-maxSize}} MB。",
		        folderUpload: "不允许上传文件夹。"
		    }
		},
		uploadFile: {
	        url: "/uploadfile_conc2/",
	        data: null,
	        type: 'POST',
	        enctype: 'multipart/form-data',
	        beforeSend: function(){},
	        success: function(data, el){
	        	if (data.issuc=="true"){
	        		el.attr("value",data.docId)
	        		uploaddocs.push(data.docId);
	        	}
	            
	        },
	        error: function(el){
	        },
	        statusCode: null,
	        onProgress: null,
	        onComplete: null
	    },
	    onRemove: function(itemEl, file){
	    	var fileid = itemEl.attr("value")
	        // var file = file.name;
	        uploaddocs.splice(uploaddocs.indexOf(fileid),1)
	        $.post('/del_uploadfile/', {fileid: fileid});
	    }
	});
	
	$('#filer_input_qianzheng').filer({
		showThumbs: true,
		fileMaxSize:50,
		limit:5,
		addMore: true,
		allowDuplicates: false,
		captions:{
		    button: "添加签证文件",
		    feedback: "",
		    feedback2: "个文件已选择",
		    drop: "拖到文件到这里",
		    removeConfirmation: "是否移除文件？",
		    errors: {
		        filesLimit: "只能同时上传 {{fi-limit}}个文件 。",
		        filesType: "只能上传MicrosoftProject文件",
		        filesSize: "{{fi-name}} 太大! 最大允许上传 {{fi-fileMaxSize}} MB。",
		        filesSizeAll: "Files you've choosed are too large! Please upload files up to {{fi-maxSize}} MB。",
		        folderUpload: "不允许上传文件夹。"
		    }
		},
		uploadFile: {
	        url: "/uploadfile_conc2/",
	        data: null,
	        type: 'POST',
	        enctype: 'multipart/form-data',
	        beforeSend: function(){},
	        success: function(data, el){
	        	if (data.issuc=="true"){
	        		el.attr("value",data.docId)
	        		uploaddocsQianZheng.push(data.docId);
	        	}
	            
	        },
	        error: function(el){
	        },
	        statusCode: null,
	        onProgress: null,
	        onComplete: null
	    },
	    onRemove: function(itemEl, file){
	    	var fileid = itemEl.attr("value")
	        // var file = file.name;
	        uploaddocsQianZheng.splice(uploaddocsQianZheng.indexOf(fileid),1)
	        $.post('/del_uploadfile/', {fileid: fileid});
	    }
	});
	
	$(".jFiler-input").css("width","100%");

	$("#btnLoadHisVerDlg").on('click', function() {

		$("#tbl_hisPrjTask tr:gt(0)").remove();
		$.ajax({
			type: "get",
			url: "/task/projecttask/getprjversiionlist",
			cache: false,
			dataType: "json",
			data: {},
			success: function(data) {
				if(data.issuc == "true") {
					for(var each in data.prjversiionlist) {
						if(each == "remove")
							continue;
	
						var newRow = "<tr> \
					          		<td>" + data.prjversiionlist[each].id + "</td> \
					          		<td>" + data.prjversiionlist[each].version_code + "</td> \
					          		<td>" + data.prjversiionlist[each].update_time + "</td> \
					          		<td>" + data.prjversiionlist[each].description + "</td> \
							  		<td><ul>";
						for(var eachfile in data.prjversiionlist[each].filelist) {
							newRow = newRow + "<li> <a href='/" + data.prjversiionlist[each].filelist[eachfile].filepath + data.prjversiionlist[each].filelist[eachfile].name + "' target='_blank'>" + data.prjversiionlist[each].filelist[eachfile].shortname + "</a></li>";
						}
	
						newRow = newRow + "</ul></td></tr>";
						$("#tbl_hisPrjTask tr:last").after(newRow);
	
					}
	
					$("#tbl_hisPrjTask tr:gt(0)").click(function(obj) {
						$("#tbl_hisPrjTask tr:gt(0)").removeClass("trSelected");
						$(obj.currentTarget).addClass("trSelected");
						_selVersionId = obj.currentTarget.children[0].innerText;
					});
	
					$("#taskHisVersionDlg").modal('show');
				} else {
					alert(data.error);
				}
			}
		});

});

$("#btnUploadTaskPrjFileDlg").on('click', function() {
	$("#imporTaskPrjFiledlg").modal('show');
});


$("#btnPrintQrcode").on('click', function() {
	zeroModal.alert("该功能暂时不支持！");
	return ;
});



});

function wgetFit() {
	var minheight = $(window).height() - 170;
	$(".row").css('min-height', minheight);
}

function initGantChart(g) {
	var vLangsCn = {
		'format': '显示样式',
		'hour': 'Hour',
		'day': '天',
		'week': '周',
		'month': '月',
		'quarter': '季度',
		'hours': 'Hours',
		'days': '天',
		'weeks': 'Weeks',
		'months': 'Months',
		'quarters': 'Quarters',
		'hr': 'Hr',
		'dy': '天',
		'wk': 'Wk',
		'mth': 'Mth',
		'qtr': 'Qtr',
		'hrs': 'Hrs',
		'dys': '天',
		'wks': '周',
		'mths': '月',
		'qtrs': 'Qtrs',
		'resource': 'Resource',
		'duration': '工期',
		'comp': '完成百分比',
		'completion': '完成百分比',
		'startdate': '开始时间',
		'enddate': '结束时间',
		'moreinfo': '更多信息',
		'notes': '描述',
		'january': 'January',
		'february': 'February',
		'march': 'March',
		'april': 'April',
		'maylong': 'May',
		'june': 'June',
		'july': 'July',
		'august': 'August',
		'september': 'September',
		'october': 'October',
		'november': 'November',
		'december': 'December',
		'jan': '1月',
		'feb': '2月',
		'mar': '3月',
		'apr': '4月',
		'may': '5月',
		'jun': '6月',
		'jul': '7月',
		'aug': '8月',
		'sep': '9月',
		'oct': '10月',
		'nov': '11月',
		'dec': '12月',
		'sunday': 'Sunday',
		'monday': 'Monday',
		'tuesday': 'Tuesday',
		'wednesday': 'Wednesday',
		'thursday': 'Thursday',
		'friday': 'Friday',
		'saturday': 'Saturday',
		'sun': '星期天',
		'mon': '星期一',
		'tue': '星期二',
		'wed': '星期三',
		'thu': '星期四',
		'fri': '星期五',
		'sat': '星期六'
	};

	g.addLang('zh_CN', vLangsCn);
	g.setLang('zh_CN');
	g.setCaptionType('Name'); // Set to Show Caption (None,Caption,Resource,Duration,Complete)
	g.setQuarterColWidth(36);
	//g.setDateTaskDisplayFormat('day dd month yyyy'); // Shown in tool tip box
	g.setDateTaskTableDisplayFormat("yyyy/mm/dd"); //Date format used for start and end dates in the main task list. Defaults to 'dd/mm/yyyy'.
	g.setDateTaskDisplayFormat('yyyy/mm/dd day'); // Shown in tool tip box
	g.setDayMajorDateDisplayFormat('yyyy mon') // Set format to display dates in the "Major" header of the "Day" view
	g.setWeekMinorDateDisplayFormat('mon dd 号') // Set format to display dates in the "Minor" header of the "Week" view
	g.setShowTaskInfoLink(0); //Show link in tool tip (0/1)
	g.setShowEndWeekDate(0); // Show/Hide the date for the last day of the week in header for daily view (1/0)
	g.setUseSingleCell(10000); // Set the threshold at which we will only use one cell per table row (0 disables).  Helps with rendering performance for large charts.
	g.setFormatArr('Day', 'Week', 'Month', 'Quarter'); // Even with setUseSingleCell using Hour format on such a large chart can cause issues in some browsers

	g.setShowTaskInfoRes(0);

	g.setShowRes(0);
	g.setWeekColWidth(60); //Width of Gantt Chart columns in pixels when drawn in "Week" format. Defaults to 36.
}

function LoadMajorPrjTask() {
	var MajorId = $("#selMajor").val();

	$.myloading({
		title: "进度信息比对中，请稍后……"
	});

	var parentdiv = $('#GanttChartDIV').parent();
	$("#GanttChartDIV").remove();
	var gantdiv = "<div style='position:relative;overflow=hidden;' class='gantt' id='GanttChartDIV' ></div>";
	$(parentdiv).append(gantdiv);

	g = new JSGantt.GanttChart(document.getElementById('GanttChartDIV'), 'month');
	if(g.getDivId() != null) {

		initGantChart(g);

		$.ajax({
			type: "get",
			url: "/task/projecttask/getprojecttasklist",
			cache: false,
			// async: false,
			dataType: "json",
			data: {
				"MajorId": MajorId
			},
			success: function(data) {
				if(data.issuc == "true") {
					for(var each in data.projecttasklist) {
						if(each == "remove")
							continue;
						g.AddTaskItem(new JSGantt.TaskItem(data.projecttasklist[each].pID, data.projecttasklist[each].pName, data.projecttasklist[each].pStart, data.projecttasklist[each].pEnd, data.projecttasklist[each].pStyle, "", 0,
							"", data.projecttasklist[each].pComp, data.projecttasklist[each].pGroup, data.projecttasklist[each].pParent, data.projecttasklist[each].pOpen,
							"", "", "", "g"));
					}
					g.Draw();
					$.myloading("hide");

					//$('#divProgressAnimateTitle').hide();
					//$('#divProgressAnimate').hide();

				} else {
					$.myloading("hide");
					alert(data.error);
				}
			}
		});

	} else {

		alert("Error, unable to create Gantt Chart");
	}
}



function LoadTaskHisVersion() {
	if(!_selVersionId) {
		alert("请先选择要载入的版本！");
		return;
	}

	$.myloading({
		title: "进度信息比对中，请稍后……"
	});

	var parentdiv = $('#GanttChartDIV').parent();
	$("#GanttChartDIV").remove();
	var gantdiv = "<div style='position:relative;overflow=hidden;' class='gantt' id='GanttChartDIV' ></div>";
	$(parentdiv).append(gantdiv);

	g = new JSGantt.GanttChart(document.getElementById('GanttChartDIV'), 'month');
	if(g.getDivId() != null) {

		initGantChart(g);

		$.ajax({
			type: "get",
			url: "/task/projecttask/gethisprojecttasklist",
			cache: false,
			// async: false,
			dataType: "json",
			data: {
				"_selVersionId": _selVersionId
			},
			success: function(data) {
				if(data.issuc == "true") {
					for(var each in data.projecttasklist) {
						if(each == "remove")
							continue;
						g.AddTaskItem(new JSGantt.TaskItem(data.projecttasklist[each].pID, data.projecttasklist[each].pName, data.projecttasklist[each].pStart, data.projecttasklist[each].pEnd, data.projecttasklist[each].pStyle, "", 0,
							"", data.projecttasklist[each].pComp, data.projecttasklist[each].pGroup, data.projecttasklist[each].pParent, data.projecttasklist[each].pOpen,
							"", "", "", "g"));
					}
					g.Draw();
					$.myloading("hide");

					//$('#divProgressAnimateTitle').hide();
					//$('#divProgressAnimate').hide();

				} else {
					alert(data.error);
				}
			}
		});

	} else {

		alert("Error, unable to create Gantt Chart");
	}
}


function bindContextMenu() {
	$("#gtasktableId tbody tr").on("mousedown", (function(e) {

		$(this).removeClass("gitemhighlight");
		$(this).addClass("trSelected").siblings("tr").removeClass("trSelected");

		if(e.which == 3) {

			var opertion = {
				name: "",
				offsetX: 2,
				offsetY: 2,
				textLimit: 10,
				beforeShow: $.noop,
				afterShow: $.noop,
			};

			var imageMenuData = [
				[{
					text: "新建子任务",
					func: function() {
						funNewChildTask();
					}
				}, {
					text: "修改任务",
					func: function() {
						funEditTask();
					}
				}
//				, {
//					text: "任务追踪",
//					func: function() {
//						funTraceTask();
//					}
//				}
				, {
					text: "删除任务",
					func: function() {
						funDeleteTask();
					}
				}],
//				[{
//					text: "关联本地文件",
//					func: function() {
//						//window.location.href = "/task/ziliao/uploadview/?uploaddir=1";
//						var href = "/task/ziliao/uploadview/?uploaddir=1";
//						window.open(href);
//					}
//				}, {
//					text: "关联云端文件",
//					func: function() {
//						//window.location.href = "/task/ziliao/cloudfilerelate/";
//						var href = "/task/ziliao/cloudfilerelate/";
//						window.open(href);
//					}
//				}],
//				[{
//					text: "打印二维码",
//					func: function() {
//						funTaskQrcode();
//					}
//				}],
//				[{
//					text: "发起质量问题",
//					func: function() {
//						alert("todo 发起质量问题 pangubing");
//					}
//				}],
			];

			$(this).smartMenu(imageMenuData, opertion);

		}
	}));
}

function funNewChildTask() {
	var bHasSelected = false;

	var $table = $("#gtasktableId");
	var $trs = $table.find("tr");
	for(var i = 0; i < $trs.length; i++) { //循环获取每一行
		var $tr = $trs.eq(i);
		if($tr.hasClass('trSelected')) {
			var taskid = $tr.attr("id").split("_")[1];
			task = g.GetTaskItem(taskid);
			//alert(task.getName());
			$('#taskparentname').val(task.getName());
			$('#taskparentId').val(taskid);
			bHasSelected = true;
		}
	}

	if(!bHasSelected) {
		alert("请先选择一个父节点！");
		return;
	}

	$("#addtaskdlg").modal('show');
}

function funEditTask() {
	var bHasSelected = false;

	var $table = $("#gtasktableId");
	var $trs = $table.find("tr");
	for(var i = 0; i < $trs.length; i++) { //循环获取每一行
		var $tr = $trs.eq(i);
		if($tr.hasClass('trSelected')) {
			var taskid = $tr.attr("id").split("_")[1];
			task = g.GetTaskItem(taskid);
			//alert(task.getName());

			bHasSelected = true;
		}
	}

	if(!bHasSelected) {
		alert("请先选择一个任务！");
		return;
	}

	$.ajax({
		type: "get",
		url: "/task/projecttask/gettask/",
		cache: false,
		//async: false,
		dataType: "json",
		data: {
			"taskid": taskid,
		},
		success: function(data) {
			if(data.issuc == "true") {
				$('#edittaskId').val(data.task.taskId);
				$('#editname').val(data.task.name);
				$('#edittaskparentname').val(data.task.parentname);
				$('#edittaskparentId').val(data.task.parentid);
				$('#editmajor').val(data.task.editmajor);
				$('#editplanstart').val(data.task.editplanstart);
				$('#editplanfinish').val(data.task.editplanfinish);
				$('#editactualstart').val(data.task.editactualstart);
				$('#editacutalfinish').val(data.task.editacutalfinish);
				$('#edicompletion').val(data.task.percentage);
				$('#editdescription').val(data.task.description);
			} else {
				alert(data.error);
				return;
			}

		}
	});

	$("#edittaskdlg").modal('show');
}

function funDeleteTask() {
	var bHasSelected = false;

	var $table = $("#gtasktableId");
	var $trs = $table.find("tr");
	for(var i = 0; i < $trs.length; i++) { //循环获取每一行
		var $tr = $trs.eq(i);
		if($tr.hasClass('trSelected')) {
			var taskid = $tr.attr("id").split("_")[1];
			task = g.GetTaskItem(taskid);
			//alert(task.getName());

			bHasSelected = true;
		}
	}

	if(!bHasSelected) {
		alert("请先选择一个任务！");
		return;
	}

	var r = confirm("确认删除任务？")
	if(r != true) {
		return;
	}

	$.ajax({
		type: "get",
		url: "/task/projecttask/deltask/",
		cache: false,
		//async: false,
		dataType: "json",
		data: {
			"taskid": taskid,
		},
		success: function(data) {
			if(data.issuc == "true") {
				var r = confirm("删除任务成功！是否刷新？");
				if(r == true) {
					window.location.reload(true);
				}

			} else {
				alert(data.error);
				return;
			}

		},		
		error: function(e){
			if(e.status==403){
				alert("您没有权限删除任务，请联系管理员！");
			}else{
				alert("服务器错误！")
			}
		}
	});
}

function funTraceTask() {
	var bHasSelected = false;
	var taskid = 0;
	var $table = $("#gtasktableId");
	var $trs = $table.find("tr");
	for(var i = 0; i < $trs.length; i++) { //循环获取每一行
		var $tr = $trs.eq(i);
		if($tr.hasClass('trSelected')) {
			taskid = $tr.attr("id").split("_")[1];
			task = g.GetTaskItem(taskid);
			//alert(task.getName());
			bHasSelected = true;
		}
	}

	if(!bHasSelected) {
		alert("请先选择一个任务！");
		return;
	}

	var href = "/task/projecttask/trace/?taskid=" + taskid;
	window.open(href);
}

function funTaskQrcode() {
	var bHasSelected = false;
	var taskid = 0;
	var $table = $("#gtasktableId");
	var $trs = $table.find("tr");
	for(var i = 0; i < $trs.length; i++) { //循环获取每一行
		var $tr = $trs.eq(i);
		if($tr.hasClass('trSelected')) {
			taskid = $tr.attr("id").split("_")[1];
			task = g.GetTaskItem(taskid);
			//alert(task.getName());
			bHasSelected = true;
		}
	}

	if(!bHasSelected) {
		alert("请先选择一个任务！");
		return;
	}

	PrintTaskQrcode(taskid);
}

function AddTask2Server() {
	var jsonobj = $('#addtaskForm').serializeJSON();
	var jsonString = JSON.stringify(jsonobj);
	console.log(jsonString);

	$.ajax({
		type: "post",
		url: "/task/projecttask/create/",
		cache: false,
		dataType: "json",
		data: jsonobj,
		success: function(data) {
			if(data.issuc == "true") {
				var r = confirm("创建任务成功！是否刷新？");
				if(r == true) {
					window.location.reload(true);
				}
			} else {
				alert(data.error);
			}
		},		
		error: function(e){
			if(e.status==403){
				alert("您没有权限编辑任务，请联系管理员！");
		    }else{
				alert("服务器错误！")
			}
		}
	});

	$("#addtaskdlg").modal('hide');
};

function EditTask2Server() {
	if(!$('#editplanstart').val() || !$('#editplanfinish').val())
	{
		alert("计划开始、结束时间不能为空！");
		return;
	}

	var jsonobj = $('#edittaskForm').serializeJSON();
	var jsonString = JSON.stringify(jsonobj);
	console.log(jsonString);

	$.ajax({
		type: "post",
		url: "/task/projecttask/edit/",
		cache: false,
		dataType: "json",
		data: jsonobj,
		success: function(data) {
			if(data.issuc == "true") {
				var r = confirm("修改任务成功！是否刷新？");
				if(r == true) {
					window.location.reload(true);
				}
			} else {
				alert(data.error);
			}

		},		
		error: function(e){
			if(e.status==403){
				alert("您没有权限编辑任务，请联系管理员！");
		    }else{
				alert("服务器错误！")
			}
		}
	});

	$("#edittaskdlg").modal('hide');
};

function importTaskPrjFile(){
	
	if(uploaddocs.length==0){
		alert("请添加进度文件。");
		return;
	}
	
	if(uploaddocsQianZheng.length==0){
		if(!confirm("没有选择签证文件，是否确认更新？")){
			return;
		}
	}
	
	var jsonobj = $('#imporTaskPrjForm').serializeJSON();
	jsonobj.docs= JSON.stringify(uploaddocs)
	jsonobj.qianzhengdocs= JSON.stringify(uploaddocsQianZheng)

	$.ajax({
		type: "post",
		cache: false,
		url: "/task/projecttask/updatetaskplan/",
		dataType: "json",
		data: jsonobj,
		success: function(data) {
			if(data.issuc == "true") {
				alert("更新成功！");
			} else {
				alert("更新失败！");
			}
			$('#imporTaskPrjFiledlg').modal('hide');
		}
	});
	
}
