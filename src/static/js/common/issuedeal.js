	
var	 g_CurChuliWentiOprId = 0 ;
var	g_CurChuliWentiissueId = 0;
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
			  
function FunChuliwenti()
{
	var feedback = $("#chuli_qfeedback").val();
	if(!feedback){
		alert("问题反馈不能为空！");
		return;
	}
	
	if(Needfile && IssueRelateFileDocIds.length==0){
		alert("处理附件不能为空！");
		return;
	}
	
	var docIds="";
	for(i=0;i<IssueRelateFileDocIds.length;i++)
	{
		docIds+=IssueRelateFileDocIds[i]+",";
	}
				
	var Chuli_RelateFileList = $('#Chuli_RelateFileList').val(docIds);
			
	
	$.ajax({
		  type:"get",
		  url:"/task/issue/dealissue/",
		  cache:false,
		  dataType:"json",
		  data:{"operId": g_CurChuliWentiOprId,"issueId": g_CurChuliWentiissueId,"feedback":feedback,"Chuli_RelateFileList":docIds,"bdid":bdid},
		  success: function(data){
			if(data.issuc=="true")
			{
				var r=confirm("处理成功！");
				window.opener.location.reload();
				window.close();
			}
			else
			{
				alert(data.error);
				
			}

		  }
		});
}
		
function FunChuliwentiUploadFile(issueId,OprId) { 

	   g_CurChuliWentiOprId = OprId ;
	   g_CurChuliWentiissueId = issueId;
	
	   // IssueRelateFileDocIds = [];
			
	   FunChuliwenti();
}

var Needfile = true;
function FunChuliwentiConfig(issueId)
{
	$.ajax({
		  type:"get",
		  url:"/task/issue/dealconfig/",
		  cache:false,
		  dataType:"json",
		  data:{"issueId": issueId,},
		  success: function(data){
			if(data.issuc=="true")
			{
				
				$("#issuenumber").html(data.issue.number);
				$("#faqiren").html(data.issue.faqiren);
				$("#faqishijian").html(data.issue.faqishijian);
				$("#dangqianjieduan").html(data.issue.dangqianjieduan.jianduan);
				$("#dangqianjieduan").css("backgroundColor",data.issue.dangqianjieduan.color)
				$("#dangqianbuzhou").html(data.issue.dangqianbuzhou)
				$("#jiezhishijian").html(data.issue.deadline);
				$("#youxianji").html(data.issue.priority);
				$("#describe").html(data.issue.describe);
				$("#zhuanye").html(data.issue.major);
				$("#guanlianyuansu").html(data.issue.guanlianyuansudis);
				$("#chuli_qfeedback").val(data.issue.defaultcomment);
				
				Needfile = data.issue.needfile;
				
				if(data.issue.issave=="True"){
					$("#chuli_qfeedback").html(data.issue.describe);
				}
				
				_stepid = data.issue.stepid;
				
				
				for(var each in data.RelateFormList){
					if (data.RelateFormList[each].type=="biaodan") {
						$(".ul_biaodan").append('<li  class="list-group-item li-magright"><a  href="#" onclick="chakanBbiaodan('+data.RelateFormList[each].id+',this)">'+'修改'+data.RelateFormList[each].name+'</a></li>');
//						$(".ul_biaodan").append('<li class="list-group-item li-magright"><a  href="/assist/biaodanedit/?bdid='+data.RelateFormList[each].id+'"  target="_blank">填写'+data.RelateFormList[each].name+'</a></li>');
					} else{
						$(".ul_biaodan").append('<li  class="list-group-item li-magright"><a  href="#" onclick="openuedit('+data.RelateFormList[each].id+',this)">'+'填写'+data.RelateFormList[each].name+'</a></li>');
//						$(".ul_biaodan").append('<li class="list-group-item li-magright"><a  href="/assist/biaodanedit/?mbId='+data.RelateFormList[each].id+'"  target="_blank">填写'+data.RelateFormList[each].name+'</a></li>');
					}
				}
				
				if(data.RelateFormList.length==0){
					$(".div_biaodan").css("display","none");
				}

				var output = '';
				for(var each in data.StepOperation){
					output = output + '<button class="btn btn-primary"  style="margin-right:20px;" onclick="FunChuliwentiUploadFile('+issueId+','+data.StepOperation[each].id+')" >'+data.StepOperation[each].name+'</button>';
				}
				var output = output + '<button class="btn btn-default-outline" onclick="javascript:window.close()" >取消</button>';
				
				$("#chuli_dlgfooter").html(output);
			}
			else
			{
				alert("获取问题信息失败!");
			}

		  }
		});
		
}

 

//////

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
	//			$("#RelateElement").append("<option value=" + data.RelateElementList[each].biaodantype + ">" + data.RelateElementList[each].name+ "</option>");
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




$(function() {
	function initTableCheckbox() {
		var $thr = $('table-checkbox thead tr');
		var $checkAllTh = $('<th><input type="checkbox" id="checkAll" name="checkAll" /></th>');
		/*将全选/反选复选框添加到表头最前，即增加一列*/
		$thr.prepend($checkAllTh);
		/*“全选/反选”复选框*/
		var $checkAll = $thr.find('input');
		$checkAll.click(function(event) {
			/*将所有行的选中状态设成全选框的选中状态*/
			$tbr.find('input').prop('checked', $(this).prop('checked'));
			/*并调整所有选中行的CSS样式*/
			if($(this).prop('checked')) {
				$tbr.find('input').parent().parent().addClass('warning');
			} else {
				$tbr.find('input').parent().parent().removeClass('warning');
			}
			/*阻止向上冒泡，以防再次触发点击操作*/
			event.stopPropagation();
		});
		/*点击全选框所在单元格时也触发全选框的点击操作*/
		$checkAllTh.click(function() {
			$(this).find('input').click();
		});
		var $tbr = $('.table-checkbox tbody tr');
		var $checkItemTd = $('<td><input type="checkbox" name="checkItem" /></td>');
		/*每一行都在最前面插入一个选中复选框的单元格*/
		$tbr.prepend($checkItemTd);
		/*点击每一行的选中复选框时*/
		$tbr.find('input').click(function(event) {
			/*调整选中行的CSS样式*/
			$(this).parent().parent().toggleClass('warning');
			/*如果已经被选中行的行数等于表格的数据行数，将全选框设为选中状态，否则设为未选中状态*/
			$checkAll.prop('checked', $tbr.find('input:checked').length == $tbr.length ? true : false);
			/*阻止向上冒泡，以防再次触发点击操作*/
			event.stopPropagation();
		});
		/*点击每一行时也触发该行的选中操作*/
		$tbr.click(function() {
			$(this).find('input').click();
		});
	}
	initTableCheckbox();
});



