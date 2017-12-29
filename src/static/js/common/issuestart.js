var IssueRelateFileDocIds = [];

$(function() {

	// 初始化插件
	$("#faqi_uploadfile").zyUpload({
		itemWidth: "60px", // 文件项的宽度
		itemHeight: "50px", // 文件项的高度
		url: "/uploadfile_conc2/", // 上传文件的路径
		multiple: true, // 是否可以多个文件上传
		dragDrop: false, // 是否可以拖动上传文件
		del: true, // 是否可以删除文件
		finishDel: false, // 是否在上传文件完成后删除预览
		/* 外部获得的回调接口 */
		onSelect: function(files, allFiles) { // 选择文件的回调方法
			console.info("当前选择了以下文件：");
			console.info(files);
			console.info("之前没上传的文件：");
			console.info(allFiles);
		},
		onDelete: function(file, surplusFiles) { // 删除一个文件的回调方法
			console.info("当前删除了此文件：");
			console.info(file);
			console.info("当前剩余的文件：");
			console.info(surplusFiles);
		},
		onSuccess: function(file) { // 文件上传成功的回调方法
			console.info("此文件上传成功：");
			console.info(file);
		},
		onFailure: function(file) { // 文件上传失败的回调方法
			console.info("此文件上传失败：");
			console.info(file);
		},
		onComplete: function(responseInfo) { // 上传完成的回调方法
			console.info("文件上传完成");
			console.info(responseInfo);
		}
	});

	$('#deadline').datetimepicker({
		language: 'zh-CN',
		weekStart: 1,
		todayBtn: 1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 2,
		minView: 2,
		forceParse: 0
	});

	

});

var flag = 1;

function FunFaqiwentiDlg() {
	g_CurOprType = "发起问题";
	$("#addbiaodan").html("点击增加表单");
	$('#faqiwentidlg').modal('show');
	flag = 1;
	$.ajax({
		type: "get",
		url: "/task/issue/createconfig/",
		cache: false,
		dataType: "json",
		data: {
			"issuetype": "{{issuetype}}",
		},
		success: function(data) {
			if(data.issuc = "true") {} else {

			}

		}
	});

};
var id;

function biaodanDlg() {
	//		$('#biaodan').modal('show');
	flag = 1;
	$("#biaodanback").css("display", "inline-block");
	addTableSuc();
	var exp = new Date();
	id = "zlwt" + exp.getTime();
	window.open('/task/issue/biaodan3?id=' + id, 'newwindow')
};

function addTableSuc() {
	var obj = new TipBox({
		type: 'load',
		str: "正在操作表格..",
		hasBtn: true,
		setTime: 1500,
		callBack: function() {
			var cval = getCookie(id);
			if(cval) {
				var exp = new Date();
				exp.setTime(exp.getTime() - 1000);
				document.cookie = id + "=succ" + "';path=/;expires=" + exp.toGMTString();
				new TipBox({
					type: 'success',
					str: '操作成功',
					hasBtn: true
				});
				$("#addbiaodan").html("已添加");
				$("#biaodanback").css("display", "none");

			} else {
				if(flag == 0) {
					$("#addbiaodan").html("点击增加表单");
					$("#biaodanback").css("display", "none");
					obj.destroy();
				} else {
					addTableSuc();
				}

			}
		}
	});
}

function getCookie(name) {

	var arr, reg = new RegExp("(^| )" + name + "=succ");
	if(arr = document.cookie.match(reg))
		return unescape(arr[0]);
	else
		return null;
}

function delCookie(name) {
	var exp = new Date();
	exp.setTime(exp.getTime() - 1000);
	var cval = getCookie(name);
	if(cval != null)
		document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
}

function RelateTypeChange() {
	$("#RelateElement").val(null).trigger("change");;
	$("#RelateElement:selected").remove();
	$("#RelateElement").empty();
	//var relatetype = $("input[name=optionsRadiosRelateType]:checked").val();
	//
	//$.ajax({
	//  type:"get",
	//  url:"/task/issue/getrelatetype/",
	//  cache:false,
	//  dataType:"json",
	//  data:{"relatetype":relatetype,},
	//  success: function(data){
	//	if(data.issuc="true")
	//	{
	//		for(var each in data.RelateElementList){
	//			$("#RelateElement").append("<option value=" + data.RelateElementList[each].id + ">" + data.RelateElementList[each].name+ "</option>");
	//		}
	//	}
	//	else
	//	{
	//		
	//	}
	//
	//  }
	//});
};

function Funfaqiwenti() {
	var docIds = "";
	for(i = 0; i < IssueRelateFileDocIds.length; i++) {
		docIds += IssueRelateFileDocIds[i] + ",";
	}

	$('#RelateFileList').val(docIds);

	var jsonobj = $('#faqiwentiForm').serializeJSON();
	var jsonString = JSON.stringify(jsonobj);
	console.log(jsonString);

	$.ajax({
		type: "post",
		url: "/task/issue/createissue/",
		cache: false,
		dataType: "json",
		data: jsonobj,
		success: function(data) {
			if(data.issuc == "true") {
				var r = confirm("发起问题成功！");
				window.location.reload(true);
			} else {
				var r = confirm(data.error);
			}

		}
	});
	$('#faqiwentidlg').modal('hide');
};

function FunfaqiwentiUploadFile(issueId) {

	IssueRelateFileDocIds = [];

	$(".upload_btn").click();
};