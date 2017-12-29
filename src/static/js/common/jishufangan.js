var weixianyuanid;
var jiaodidocs=[];
var xiugaidocs=[];
var genzongdocs=[];
var shenpidocs=[];
var shangchuandocs=[];
var dlg='';
$(function() {

	$('#uploadfile_xiugai').filer({
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
	        		xiugaidocs.push(data.docId);

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
	        xiugaidocs.splice(xiugaidocs.indexOf(fileid),1)
	        $.post('/del_uploadfile/', {fileid: fileid});
	    }
	});

	$('#uploadfile_jiaodi').filer({
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
	        		jiaodidocs.push(data.docId);

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
	    	jiaodidocs.splice(jiaodidocs.indexOf(fileid),1)
	        $.post('/del_uploadfile/', {fileid: fileid});
	    }

	});

	$('#uploadfile_genzong').filer({
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
	        		genzongdocs.push(data.docId);

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
	    	genzongdocs.splice(genzongdocs.indexOf(fileid),1)
	        $.post('/del_uploadfile/', {fileid: fileid});
	    }

	});

	$('#uploadfile_shenpi').filer({
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
	        		shenpidocs.push(data.docId);

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
	    	shenpidocs.splice(jiaodidocs.indexOf(fileid),1)
	        $.post('/del_uploadfile/', {fileid: fileid});
	    }

	});

	$('#uploadfile_shangchuan').filer({
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
	        		shangchuandocs.push(data.docId);

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
	    	shangchuandocs.splice(jiaodidocs.indexOf(fileid),1)
	        $.post('/del_uploadfile/', {fileid: fileid});
	    }

	});

	$('.datetimepic').datetimepicker({
		language: 'zh-CN',
		weekStart: 1,
		todayBtn: 1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 2,
		minView: 2,
		forceParse: 0,
	}).on("hide",function(){
		var id = this.id;
		var formid = document.getElementById(this.id).form.id
		$('#'+formid).data('bootstrapValidator')
	    .updateStatus(id, 'NOT_VALIDATED',null)
	    .validateField(id);

	});

	formValidator();
	//Modal验证销毁重构
	$('#btnAddFangAnDlg').on('hidden.bs.modal', function() {
		$("#addfagnanForm").data('bootstrapValidator').destroy();
		$('#addfagnanForm').data('bootstrapValidator', null);
		formValidator();
	});
	$('#xiugaidlg').on('hidden.bs.modal', function() {
		$("#xiugaiForm").data('bootstrapValidator').destroy();
		$('#xiugaiForm').data('bootstrapValidator', null);
		formValidator();
	});

	$("#btnAddFangAnDlg").on('click', function() {
		weixianyuanid='';
		$("#addfagnandlg").modal('show');
	});

	$(".ajiaodidlg").on('click', function() {
		$(".icon-jfi-trash").click();//清空附件插件
		$(".qid").val(this.parentNode.parentNode.parentNode.firstElementChild.innerHTML);
		$("#jiaodidlg").modal('show');
	});

	$(".ashenpilg").on('click', function() {
		$(".icon-jfi-trash").click();//清空附件插件
		$(".qid").val(this.parentNode.parentNode.parentNode.firstElementChild.innerHTML);
		$("#shenpidlg").modal('show');
	});

	$(".ashangchuandlg").on('click', function() {
		$(".icon-jfi-trash").click();//清空附件插件
		$(".qid").val(this.parentNode.parentNode.parentNode.firstElementChild.innerHTML);
		$("#shangchuandlg").modal('show');
	});

	$(".agenzongdlg").on('click', function() {
		$(".icon-jfi-trash").click();//清空附件插件
		$(".qid").val(this.parentNode.parentNode.parentNode.firstElementChild.innerHTML);
		$("#genzongdlg").modal('show');
	});

	$(".achakandlg").on('click', function() {
		$("#chanumber").attr('placeholder',this.parentNode.parentNode.parentNode.children[1].innerHTML)
		jsonobj={'opt':'chakan'};
		jsonobj.chaid = this.parentNode.parentNode.parentNode.firstElementChild.innerHTML;
		$.ajax({
			type: "post",
			cache: false,
			dataType: "json",
			data: jsonobj,
			success: function(data) {
				if(data.issuc == "true") {
					$(".ul_fujian").children("li").remove();
					$.each(data.docs, function(){
						$(".ul_fujian").append('<li class="list-group-item li-magright" value="'+this.docid+'"><a target="_blank" href="/upload/'+this.name+'">'+this.shortname+'</a></li>');
					})

					$("#chakandlg").modal('show');
				} else {
					confirm(data.error);
				}

			}
		});

	});
	$(".axiugaidlg").on('click', function() {
		// $(ZYFILE.funReturnNeedFiles()).each(function(){
		// 	ZYFILE.funDeleteFile(this.index,true)
		// })
		// docs=[];
		$(".icon-jfi-trash").click();//清空附件插件
		$(".qid").val(this.parentNode.parentNode.parentNode.firstElementChild.innerHTML);
		$("#xiugaidlg").modal('show');

		// $("#chanumber").attr('placeholder',this.parentNode.parentNode.parentNode.children[1].innerHTML)
		jsonobj={'opt':'chakan'};
		jsonobj.chaid = this.parentNode.parentNode.parentNode.firstElementChild.innerHTML;
		$.ajax({
			type: "post",
			cache: false,
			dataType: "json",
			data: jsonobj,
			success: function(data) {
				if(data.issuc == "true") {
					console.log(data);
					$("#qsubmit_date").val(new Date(data.technicalitem.submit_date*1000).format('yyyy-MM-dd'));
					if(data.technicalitem.approve_date==null){
						$("#qapprove_date").val(new Date().format('yyyy-MM-dd'));
					}else{
						$("#qapprove_date").val(new Date(data.technicalitem.approve_date*1000).format('yyyy-MM-dd'));
					}
					// $(".ul_fujian").children("li").remove();
					// $.each(data.docs, function(){
					// 	$(".ul_fujian").append('<li class="list-group-item li-magright" value="'+this.docid+'"><a target="_blank" href="/upload/'+this.name+'">'+this.shortname+'</a></li>');
					// })

					// $("#chakandlg").modal('show');
				} else {
					// confirm(data.error);
				}

			}
		});
	});

	$("#jstree_weixianyuan").jstree({
		"core": {
			'data': {
				'url': '/task/modelview/gethazardtypetree/',
				'data': function(node) {
					return {
						'id': node.id
					};
				}
			}
		},
		'multiple': false,
		"plugins": ["themes", "json_data", "checkbox"],
		"checkbox": {
			"three_state": false
		}
	});
	$('#jstree_weixianyuan').bind("activate_node.jstree", function(obj, e) {
		// 处理代码
		// 获取当前节点

		var node = e.node; //
		var isselect = node.state.selected; //选中还是取消
		weixianyuanid='';
		if(isselect) {
			var ref = $('#jstree_weixianyuan').jstree(true);
			ref.uncheck_all();
			ref.check_node(node);
			weixianyuanid=node.id;
		}
	});

});

function formValidator(){
	$('#addfagnanForm').bootstrapValidator({
		fields: {
			qnumber:{
				validators:{
					notEmpty:{
						message:'方案编号不能为空'
					}
				}
			},
			qname:{
				validators:{
					notEmpty:{
						message:'方案名称不能为空'
					}
				}
			},
			qcomment:{
				validators:{
					notEmpty:{
						message:'方案批注不能为空'
					},
					stringLength: {
						min: 5,
						max: 120,
						message: '批注在5-120个字之间'
					}
				}
			},
			qcreate_date:{
				validators:{
					notEmpty:{
						message:'计划日期不能为空'
					},
					regexp: {
						regexp: /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/,
						message: '日期格式不正确'
					},
					// callback: {
					// 	message: '交底日期不能小于计划日期',
					// 	callback:function(value, validator,$field){
					// 		var end = $('#qdisclosure_date').val();
					// 		$('#qdisclosure_date').keypress();
					// 		validator.updateStatus('qdisclosure_date', 'VALID');
					// 		return new Date(value)<=new Date(end);
					// 	}
					// }
				}
			},
			qdisclosure_date:{
				validators:{
					notEmpty:{
						message:'交底日期不能为空'
					},
					regexp: {
						regexp: /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/,
						message: '日期格式不正确'
					},
					// callback: {
					// 	message: '交底日期不能小于计划日期',
					// 	callback:function(value, validator,$field){
					// 		var begin = $('#qcreate_date').val();
					// 		$('#qcreate_date').keypress();
					// 		validator.updateStatus('qcreate_date', 'VALID');
					// 		return new Date(value)>=new Date(begin);
					// 	}
					// }
				}
			},
			qfuzeren: {
				validators: {
					notEmpty: {
						message: '负责人不能为空'
					}
				}
			}
		}
	});

	$('#xiugaiForm').bootstrapValidator({
		fields: {
			qsubmit_date:{
				validators:{
					notEmpty:{
						message:'上报日期不能为空'
					},
					regexp: {
						regexp: /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/,
						message: '上报日期格式不正确'
					},
				}
			},
			qapprove_date:{
				validators:{
					notEmpty:{
						message:'审批通过日期不能为空'
					},
					regexp: {
						regexp: /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/,
						message: '日期格式不正确'
					},
				}
			}
		}
	});
}

function addfangan(){
	//判断是否可以提交表单
	$('#addfagnanForm').bootstrapValidator('validate');
		if(!($('#addfagnanForm').data('bootstrapValidator').isValid())){
		return ;
	}
	var jsonobj = $('#addfagnanForm').serializeJSON();
	jsonobj.weixianyuanid = weixianyuanid;
	jsonobj.opt='create';
	jsonobj.qfuzeren=$("#qfuzeren").val();
	var jsonString = JSON.stringify(jsonobj);
	console.log(jsonString);

	$.ajax({
		type: "post",
		cache: false,
		dataType: "json",
		data: jsonobj,
		success: function(data) {
			if(data.issuc == "true") {
				confirm("添加方案成功");
				window.location.reload(true);
			} else {
				confirm(data.error);
			}

		}
	});
	$('#faqiwentidlg').modal('hide');

}

function filesubmit(){

	$("#fileSubmit").click();
}
function jiaodi(){
	var jsonobj = $('#jiaodiForm').serializeJSON();
	jsonobj.docs= JSON.stringify(jiaodidocs)
	jsonobj.opt='jiaodi';
	jsonobj.qdisclosure_date=(new Date()).format('YYYY-MM-dd')
	$.ajax({
		type: "post",
		// url: "/task/jishu/fangan/",
		cache: false,
		dataType: "json",
		data: jsonobj,
		success: function(data) {
			if(data.issuc == "true") {
				confirm("交底方案成功");
				$('#jiaodidlg').modal('hide');
				window.location.reload(true);
			} else {
				confirm(data.error);
			}

		}
	});

}

function xiugaifangan(){
	//判断是否可以提交表单
	$('#xiugaiForm').bootstrapValidator('validate');
		if(!($('#xiugaiForm').data('bootstrapValidator').isValid())){
		return ;
	}
	var jsonobj = $('#xiugaiForm').serializeJSON();
	jsonobj.docs= JSON.stringify(xiugaidocs)
	jsonobj.opt='xiugai';
	$.ajax({
		type: "post",
		// url: "/task/issue/createissue/",
		cache: false,
		dataType: "json",
		data: jsonobj,
		success: function(data) {
			if(data.issuc == "true") {
				confirm("修改方案成功");
				$('#xiugaidlg').modal('hide');
				window.location.reload(true);
			} else {
				confirm(data.error);
			}

		}
	});
}

function genzongfangan(){
	var jsonobj = $('#genzongForm').serializeJSON();
	jsonobj.docs= JSON.stringify(genzongdocs)
	jsonobj.opt='genzong';

	$.ajax({
		type: "post",
		// url: "/task/issue/createissue/",
		cache: false,
		dataType: "json",
		data: jsonobj,
		success: function(data) {
			if(data.issuc == "true") {
				confirm("跟踪成功");
				$('#genzongdlg').modal('hide');
				window.location.reload(true);
			} else {
				confirm(data.error);
			}

		}
	});
}

function shangchuan(){
	var jsonobj = $('#shangchuanForm').serializeJSON();
	jsonobj.docs= JSON.stringify(shangchuandocs)
	jsonobj.opt='shangchuan';
	jsonobj.qsubmit_date=(new Date()).format('YYYY-MM-dd')
	$.ajax({
		type: "post",
		// url: "/task/issue/createissue/",
		cache: false,
		dataType: "json",
		data: jsonobj,
		success: function(data) {
			if(data.issuc == "true") {
				confirm("上传成功");
				$('#shangchuandlg').modal('hide');
				window.location.reload(true);
			} else {
				confirm(data.error);
			}

		}
	});

}

function shenpi(){
	var jsonobj = $('#shenpiForm').serializeJSON();
	jsonobj.docs= JSON.stringify(shenpidocs)
	jsonobj.opt='shenpi';
	jsonobj.qapprove_date=(new Date()).format('YYYY-MM-dd')
	$.ajax({
		type: "post",
		// url: "/task/issue/createissue/",
		cache: false,
		dataType: "json",
		data: jsonobj,
		success: function(data) {
			if(data.issuc == "true") {
				confirm("审批成功");
				$('#shenpidlg').modal('hide');
				window.location.reload(true);
			} else {
				confirm(data.error);
			}

		}
	});

}
