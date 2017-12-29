
var _stepid="";
var fileuploadcmp = false;
function changeliucheng() {
	//根据选择流程obj.value,发ajax得到流程关联表单，id与name

	$.ajax({
		type: "get",
		url: "/task/flowtemplatestep/list/form?liuchengid=" + $("#dealTemplate").val(),
		cache: false,
		dataType: "json",
		success: function(data) {
			var id = data.formtempid;
			var name = data.formtempname;
			$(".form-group-biaodan").css("display", "none");
			if (id != null) {
				$(".ul_biaodan").children("li").remove();
				$(".form-group-biaodan").css("display", "block");
				$(".ul_biaodan").append('<li class="list-group-item li-magright"><a  href="#" onclick="zhenggaiDlg(' + id + ',this)">' + '填写' + name + '</a></li>');
			}
			
			_stepid=data.stepid;
			init_tree('',$("#dealTemplate").val());

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
	        onProgress: null,
	        onComplete: function(listEl, parentEl, newInputEl, inputEl, jqXHR, textStatus) {
	        	alert("所有文件上传完成!");
				fileuploadcmp = true
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
