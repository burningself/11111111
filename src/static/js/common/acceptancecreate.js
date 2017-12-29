var IssueRelateFileDocIds = [];
var bdids = [];

var bdid;
var biaodantype;
var biaodan_btn;
function openuedit(ty,obj) {
	//		$('#biaodan').modal('show');
	flag = 1;
	biaodan_btn = obj;
	$("#biaodanback").css("display", "inline-block");
	addTableSuc();
	var exp = new Date();
	biaodantype = ty + exp.getTime();
//	if(ty == 'zlwt') {
////		window.open('/assist/issue/biaodan1?biaodantype=' + biaodantype, 'newwindow')
		window.open('/assist/biaodanedit/?mbId='+ty+'&biaodantype=' + biaodantype+"&kj="+selectedKJ,
			Date.parse(new Date()))
//	} else {
//		window.open('/assist/biaodanedit/?mbId=42&biaodantype=' + biaodantype, 'newwindow')
//	}

};

function init_uploadfile() {

	$('#uploadfile').filer({
		showThumbs: true,
		addMore: true,
		allowDuplicates: false,
		captions:{
		    button: "添加文件",
		    feedback: "",
		    feedback2: "个文件已选择",
		    drop: "拖到文件到这里",
		    removeConfirmation: false,
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
	        		IssueRelateFileDocIds.push(data.docId);

	        	}
	            
	        },
	        error: function(el){
	            // var parent = el.find(".jFiler-jProgressBar").parent();
	            // el.find(".jFiler-jProgressBar").fadeOut("slow", function(){
	            //     $("<div class=\"jFiler-item-others text-error\"><i class=\"icon-jfi-minus-circle\"></i> Error</div>").hide().appendTo(parent).fadeIn("slow");    
	            // });
	        },
	        statusCode: null,
	        onProgress: null,
	        onComplete: null
	    },
	    onRemove: function(itemEl, file){
	    	var fileid = itemEl.attr("value")
	        // var file = file.name;
	        IssueRelateFileDocIds.splice(IssueRelateFileDocIds.indexOf(fileid),1)
	        $.post('/del_uploadfile/', {fileid: fileid});
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
		startDate:new Date(),
		forceParse: 0
	});


}
function FuntianjiaguanjiandianUploadFile(issueId) {

	//	IssueRelateFileDocIds = [];
	var flag = true;
	var time = /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/;
	var data = $("#deadline").val();
	if (time.test(data)) {
		flag = true;
	} else {
		$(".prompt").css("color", "red").text("请输入正确日期格式");
		flag = false;
	}
	
	if(!flag){
		return;
	}


	Funtianjiaguanjiandian();

};
$(function() {
	$("#deadline").focus(function() {
		$(".prompt").text("");
	});
});

function addTableSuc() {
	var obj = new TipBox({
		type: 'load',
		str: "正在操作表格..",
		hasBtn: true,
		setTime: 500,
		callBack: function() {
			var cval = getCookie(biaodantype);
			if(cval) {
				bdid = getCookie('bdid');
				bdids.push(bdid)
				delCookie('bdid');
				delCookie(biaodantype);
				new TipBox({
					type: 'success',
					str: '操作成功',
					hasBtn: true
				});
				var fun = "chakanBbiaodan(" + bdid + ")"
				$(biaodan_btn).attr('onclick',fun);
				$(biaodan_btn).html("查看表单");
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

	var arr, reg = new RegExp("(^| )" + name+"=([^;]*)(;|$)");
	if(arr = document.cookie.match(reg))
		return unescape(arr[2]);
	else
		return null;
}

function delCookie(name) {
	var exp = new Date();
	exp.setTime(exp.getTime() - 1000);
	document.cookie = name + "=succ" + "';path=/;expires=" + exp.toGMTString();

}

function chakanBbiaodan(bdid){
	window.open('/assist/biaodanedit/?bdid=' + bdid, Date.parse(new Date()))
}