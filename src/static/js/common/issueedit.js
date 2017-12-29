
var IssueRelateFileDocIds = [];
var bdid;
var _stepid="";

$(function(){
	// 初始化插件
		$('#uploadfile_chuli').filer({
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
	
	$(".jFiler-input").css("width","100%");
	
});		
			  
function FunUpdateWenti(operId)
{
	var feedback = $("#chuli_qfeedback").val();
	if(!feedback){
		alert("问题反馈不能为空！");
		return;
	}
	
	
	$.ajax({
		  type:"POST",
		  url:"/task/issue/update/",
		  cache:false,
		  dataType:"json",
		  data:{"operId": operId,"feedback":feedback,"RelateFileList":JSON.stringify(IssueRelateFileDocIds)},
		  success: function(data){
			if(data.issuc=="true")
			{
				var r=confirm("更新问题成功！");
				window.close();
			}
			else
			{
				alert(data.error);
				
			}

		  }
		});
}
		

function delrelatefile(fileid,obj){
	$.post('/del_uploadfile/', {fileid: fileid});
	$(obj).parent().remove();
}

 
var flag = 1;

var biaodantype;
var biaodan_btn;
function openuedit(ty,obj) {
	
	var stepParam = "";
	if(_stepid&&_stepid!="undefined"){
		stepParam = "&step="+_stepid;
	}
	
	flag = 1;
	biaodan_btn = obj;
	addTableSuc();
	var exp = new Date();
	biaodantype = ty + exp.getTime();
//	if(ty == 'zlwt') {
////		window.open('/assist/issue/biaodan1?biaodantype=' + biaodantype, 'newwindow')
	window.open('/assist/biaodanedit/?mbId='+ty+'&biaodantype=' + biaodantype+stepParam, Date.parse(new Date()))
//	} else {
//		window.open('/assist/biaodanedit/?mbId=42&biaodantype=' + biaodantype, 'newwindow')
//	}

};

function chakanBbiaodan(bdid){
	var stepParam = "";
	if(_stepid&&_stepid!="undefined"){
		stepParam = "&step="+_stepid;
	}
	
	window.open('/assist/biaodanedit/?bdid=' + bdid+stepParam, Date.parse(new Date()))
}



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



