var uploaddocs=[];
$(function () {
	$('#create_date').datetimepicker({
		language: 'zh-CN',
		weekStart: 1,
		todayBtn: 1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 3,
		minView: 3,
		forceParse: 0
	});
	
		$('#filer_input').filer({
		showThumbs: true,
		fileMaxSize:100,
		limit:1,
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
});

$("#btnUploadTaskPrjFileDlg").on('click',function(){
	$("#imporTaskPrjFiledlg").modal('show');
});

function importTaskPrjFile()
{	
 	var monthplan_desc = $("#monthplan_desc").val();
 	var create_date = $("#create_date").val();
 	var docs= JSON.stringify(uploaddocs)
 	
 	if(uploaddocs.length<1){
 		 alert("请添加月度计划文件！");
 		return;
 	}
 	
 	if (!monthplan_desc || !create_date) {
 		alert("备注和日期都要填写！");
 		return;
 	}
 	

 	$.ajax({
 	  type:"post",
 	  url:"/task/projecttask/savemonthplan/",
// 	  cache:false,
 	  async: false,
 	  dataType:"json",
 	  data:{
 	  	"docs":docs,
 	  	"monthplan_desc":monthplan_desc,
		"create_date":create_date
 	  },
 	  success: function(data){
 	  	if (data.issuc=="true") {
 	  		alert("保存成功");
 	  		window.location.reload();
 	  	}
 	  	else{
 	  		alert(data.error);
 	  	}

 	  },		
 	  error: function(e){
			if(e.status==403){
				alert("您没有权限编辑工作目标，请联系管理员！");
			}
		}
 	  
 	  
 	});
	
}

