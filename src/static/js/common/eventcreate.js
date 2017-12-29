
var _stepid="";
var fileuploadcmp = false;

	$(document).ready(function() {
			$('#deadline').datetimepicker({
		language: 'zh-CN',
		weekStart: 1,
		todayBtn: 1,
		autoclose: 1,
		startDate:new Date(),
		todayHighlight: 1,
		startView: 2,
		minView: 2,
		forceParse: 0
	}).on('hide',function(e) {
	   $('#faqiwentiForm').data('bootstrapValidator')
	   .updateStatus('deadline', 'NOT_VALIDATED',null)
	   .validateField('deadline');
	});



	$('#dealTemplate').click(function() {

		if($("#dealTemplate option").size()==0){
			zeroModal.alert("用户没有设置处理流程，请联系系统管理员设置！");
		}
	});
		
		
		init_uploadfile();
		formValidator();
		init_tree(null,'');
	});


	function Funfaqiwenti() {
		//判断是否可以提交表单
		$('#faqiwentiForm').bootstrapValidator('validate');
			if(!($('#faqiwentiForm').data('bootstrapValidator').isValid())){
			return ;
		}

		if(IssueRelateFileDocIds.length==0){
			 zeroModal.alert("新增事件附件不能为空！");
			return ;
		}
		
		if(!$("#dealTemplate").val()){
			 zeroModal.alert("请选择处理流程，如果没有流程可选请联系系统管理员设置！");
			return ;
		}
		
	
		$("#btnFaqiWenTi").attr("disabled","true");

		var docIds = "";
		for (i = 0; i < IssueRelateFileDocIds.length; i++) {
			docIds += IssueRelateFileDocIds[i] + ",";
		}

		var jsonobj = $('#faqiwentiForm').serializeJSON();
		jsonobj.RelateFileList = docIds;
		jsonobj.selectedGJs = JSON.stringify(selectedGJs);
		jsonobj.selectedKJ = selectedKJ;

		var jsonString = JSON.stringify(jsonobj);

		$.ajax({
			type: "post",
			url: "/task/issue/createissue/",
			cache: false,
			dataType: "json",
			data: jsonobj,
			success: function(data) {
				if (data.issuc == "true") {
					zeroModal.success("新增成功！");
					window.opener.location.reload();
					window.close();
				} else {
					 zeroModal.error(data.error);
					 $("#btnFaqiWenTi").removeAttr("disabled");
				}

			}
		});
	};


	
	

	function formValidator(){
		$('#faqiwentiForm').bootstrapValidator({
			message: 'This value is not valid',
			feedbackIcons: {
				valid: 'glyphicon glyphicon-ok',
				invalid: 'glyphicon glyphicon-remove',
				validating: 'glyphicon glyphicon-refresh'
			},
			fields: {
				qtitle: {
					validators: {
						notEmpty: {
							message: '标题不能为空'
						},
						stringLength: {
							min: 5,
							max: 60,
							message: '标题5-60个字'
						}
					}
				},
				qdescribe: {
					validators: {
						notEmpty: {
							message: '描述不能为空'
						},
						stringLength: {
							min: 5,
							max: 200,
							message: '描述5-200个字'
						}
					}
				},
				deadline: {
					validators: {
						notEmpty: {
							message: '截止时间不能为空'
						},
						regexp: {
							regexp: /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/,
							message: '日期格式不正确'
						}
					}
				}
			}
		});
	}



var IssueRelateFileDocIds=[];
function init_uploadfile() {

	$('#uploadfile').filer({
		showThumbs: true,
		addMore: true,
		allowDuplicates: false,
		fileMaxSize:100,
		limit:5,
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
	        onProgress: function(Percent,listEl, parentEl, newInputEl, inputEl, jqXHR, textStatus) {
	        	$(listEl).find(".bar").html(Percent+"%");
			},
	        onComplete: function(listEl, parentEl, newInputEl, inputEl, jqXHR, textStatus) {
	        	info_prompt("所有文件上传完成!");
			},
	    },
	    onRemove: function(itemEl, file){
	    	var fileid = itemEl.attr("value")
	        // var file = file.name;
	        IssueRelateFileDocIds.splice(IssueRelateFileDocIds.indexOf(fileid),1)
	        $.post('/del_uploadfile/', {fileid: fileid});
	    }
	});


};

function FunfaqiwentiUploadFile() {
	//	IssueRelateFileDocIds = [];
	var flag = true;
	$("#qdescribe").focus(function() {
		$(".qdescribe").css("color", "red").text("请输入不大于200个字");
	}).blur(function() {
		if ($("#qdescribe").val() != "" && $("#qdescribe").val().length <= 200) {
			$(".qdescribe").css("color", "green").text("输入成功");
		} else {
			$(".qdescribe").css("color", "red").text("输入错误");
			flag = false;
		}
	});
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

	Funfaqiwenti();
};
$(function() {
	$("#deadline").focus(function() {
		$(".prompt").text("");
	});
});
