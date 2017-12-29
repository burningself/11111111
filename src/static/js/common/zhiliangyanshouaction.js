var yanshouFileDocIds = [];
$(function(){
	// 初始化插件
		$('#uploadfile_yanshou').filer({
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
	        		yanshouFileDocIds.push(data.docId);

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
	        yanshouFileDocIds.splice(yanshouFileDocIds.indexOf(fileid),1)
	        $.post('/del_uploadfile/', {fileid: fileid});
	    }
	});
	
	$(".jFiler-input").css("width","100%");
	
});

function chakanBbiaodan(bdid){
	window.open('/assist/biaodanedit/?bdid=' + bdid, Date.parse(new Date()))
}

function yanshouButton(){
	var rdata={};
	rdata.comment = $('#qdescribe').val();
	rdata.RelateFileList = JSON.stringify(yanshouFileDocIds);
	if(yanshouFileDocIds.length==0){
		 zeroModal.error('请添加验收附件!');
		 return;
	}
	
	$.ajax({
		type:"post",
//		url:"",
		async:true,
		data:rdata,
		success: function(data){
			if(data.res=='succ'){
				window.opener.location.reload();
				window.close();
			}
		}
	});
}
