
var uploaddocs=[];
var mapfileRelatedir={};
var fileuploadcmp = true;
var diruploadcmp = true;

$(document).ready(function() {
	
		var templates={
        box: '<ul class="jFiler-items-list jFiler-items-grid"></ul>',
        item: '<li class="jFiler-item">\
                    <div class="jFiler-item-container">\
                        <div class="jFiler-item-inner">\
                            <div class="jFiler-item-thumb">\
                                <div class="jFiler-item-status"></div>\
                                <div class="jFiler-item-info">\
                                    <span class="jFiler-item-title"><b title="{{fi-name}}">{{fi-name | limitTo: 25}}</b></span>\
                                    <span class="jFiler-item-others">{{fi-size2}}</span>\
                                </div>\
                                {{fi-image}}\
                            </div>\
                            <div class="jFiler-item-assets jFiler-row">\
                                <ul class="list-inline pull-left">\
                                    <li>{{fi-progressBar}}</li>\
                                </ul>\
                                <ul class="list-inline pull-right">\
                                    <li><a class="icon-jfi-trash jFiler-item-trash-action"></a></li>\
                                </ul>\
                            </div>\
                        </div>\
                    </div>\
                </li>',
        itemAppend: '<li class="jFiler-item">\
                        <div class="jFiler-item-container">\
                            <div class="jFiler-item-inner">\
                                <div class="jFiler-item-thumb">\
                                    <div class="jFiler-item-status"></div>\
                                    <div class="jFiler-item-info">\
                                        <span class="jFiler-item-title"><b title="{{fi-name}}">{{fi-name | limitTo: 25}}</b></span>\
                                        <span class="jFiler-item-others">{{fi-size2}}</span>\
                                    </div>\
                                    {{fi-image}}\
                                </div>\
                                <div class="jFiler-item-assets jFiler-row">\
                                    <ul class="list-inline pull-left">\
                                        <li><span class="jFiler-item-others">{{fi-icon}}</span></li>\
                                    </ul>\
                                    <ul class="list-inline pull-right">\
                                        <li><a class="icon-jfi-trash jFiler-item-trash-action"></a></li>\
                                    </ul>\
                                </div>\
                            </div>\
                        </div>\
                    </li>',
        progressBar: '<div class="bar"></div>',
        itemAppendToEnd: false,
        removeConfirmation: true,
        _selectors: {
            list: '.jFiler-items-list',
            item: '.jFiler-item',
            progressBar: '.bar',
            remove: '.jFiler-item-trash-action'
        }
   };
   
   var captions={
		    button: "选择添加文件夹",
		    feedback: "",
		    feedback2: "个文件已选择",
		    drop: "拖放文件到这里",
		    removeConfirmation: "是否移除文件？",
		    errors: {
		        filesLimit: "只能同时上传 {{fi-limit}}个文件 。",
		        filesType: "只能上传MicrosoftProject文件",
		        filesSize: "{{fi-name}} 太大! 最大允许上传 {{fi-fileMaxSize}} MB。",
		        filesSizeAll: "Files you've choosed are too large! Please upload files up to {{fi-maxSize}} MB。",
		        folderUpload: "不允许上传文件夹。"
		    }
		};
	

	var fileinput = $('#filer_input_file').filer({
    	changeInput: '<div class="jFiler-input-dragDrop"><div class="jFiler-input-inner"><div class="jFiler-input-icon"><i class="icon-jfi-cloud-up-o"></i></div><div class="jFiler-input-text"><h3>拖放文件到这里</h3> <span style="display:inline-block; margin: 15px 0">或者</span></div><a class="jFiler-input-choose-btn blue">选择添加文件</a></div></div>',
    	showThumbs: true,
    	theme: "dragdropbox",
		fileMaxSize:500,
		limit:5000,
		addMore: true,
		allowDuplicates: false,
		captions:captions,
		templates:templates,
	    dragDrop: {
	        dragEnter: null,
	        dragLeave: null,
	        drop: null,
	    },
	    uploadFile: {
	        url: "/uploadfile_conc2/",
	        data: null,
	        type: 'POST',
	        enctype: 'multipart/form-data',
	        beforeSend: function(item, listEl, parentEl, newInputEl, inputEl){
	        	this.data = {"ceshi":'11111'};
	        },
	        success: function(data, el){
	        	if (data.issuc=="true"){
	        		el.attr("value",data.docId)
	        		uploaddocs.push(data.docId);
	        	}
	            
	        },
	        error: function(el){
	        },
	        statusCode: null,
	        onProgress: function(Percent,listEl, parentEl, newInputEl, inputEl, jqXHR, textStatus) {
	        	$(listEl).find(".bar").html(Percent+"%");
			},
	        onComplete: function(listEl, parentEl, newInputEl, inputEl, jqXHR, textStatus) {
	        	info_prompt("所有文件上传完成!");
				fileuploadcmp = true
			},
	    },
	    onSelect: function(item, listEl, parentEl, newInputEl, inputEl) {
	    	fileuploadcmp = false
		},
		beforeSelect: function(files, listEl, parentEl, newInputEl, inputEl) {
			
			var bSuc = checkfileExist(files);
			
			return bSuc;
		},
	    onRemove: function(itemEl, file){
	    	var fileid = itemEl.attr("value")
	        // var file = file.name;
	        uploaddocs.splice(uploaddocs.indexOf(fileid),1)
	        $.post('/del_uploadfile/', {fileid: fileid});
	    }
	});
	
	var firstDir = {};
	var fileindex=0;
	var filerdir = $('#filer_input').filer({
		showThumbs: true,
		fileMaxSize:500,
		limit:5000,
		addMore: true,
		allowDuplicates: false,
		captions:captions,
		templates:templates,
		uploadFile: {
	        url: "/uploadfile_conc2/",
	        data:firstDir,
	        type: 'POST',
	        enctype: 'multipart/form-data',
	        beforeSend: function(item, listEl, parentEl, newInputEl, inputEl) {
				if(fileindex>=inputEl[0].files.length){
					return true;
				}
				var mapName2Dir={};
		   		mapName2Dir["filedir"] = inputEl[0].files[fileindex].webkitRelativePath;  
				console.log(mapName2Dir);
				fileindex = fileindex + 1;
				this.data = mapName2Dir;
				return true;
			},
	        success: function(data, el){
	        	if (data.issuc=="true"){
	        		el.attr("value",data.docId)
	        		uploaddocs.push(data.docId);
	        		if(data.filedir){
	        			mapfileRelatedir[data.docId]=data.filedir;
	        		}
	        	}
	            
	        },
	        error: function(el){
	        },
	        statusCode: null,
	        onProgress: null,
	       	onComplete: function(listEl, parentEl, newInputEl, inputEl, jqXHR, textStatus) {
	       		info_prompt("所有文件上传完成!");
				diruploadcmp = true;
			},
	    },
	   onSelect: function(item, listEl, parentEl, newInputEl, inputEl) {
			diruploadcmp = false;
		},
		beforeSelect: function(files, listEl, parentEl, newInputEl, inputEl) {
			fileindex=0;
			var mapName2Dir={};
		   	mapName2Dir["filedir"] =  files[fileindex].webkitRelativePath;  
			this.uploadFile.data = mapName2Dir;
			fileindex = fileindex + 1;
			console.log(files);

			var bSuc = checkfileExist(files);
			
			return bSuc;
		},
	    onRemove: function(itemEl, file){
	    	var fileid = itemEl.attr("value")
	        // var file = file.name;
	        delete mapfileRelatedir[fileid];
	        uploaddocs.splice(uploaddocs.indexOf(fileid),1)
	        $.post('/del_uploadfile/', {fileid: fileid});
	    }
	});
	
	
	function checkfileExist(files){
		var bSuc = true;
				
		var jsonobj = {"uploaddir":$("#hidden_uploaddir").val()};
			for(var i=0;i<files.length;i++)
			{	
				jsonobj.filename = files[i].name;
				jsonobj.docRelatedir=files[i].webkitRelativePath
				$.ajax({
					type: "get",
					url:"/task/ziliao/checkexist/",
					cache: false,
					async: false,
					dataType: "json",
					data: jsonobj,
					success: function(data) {
						if(data.issuc == "true" && data.isexist == "true" ) {
							if(!confirm("该目录已存在文件:"+data.filename+",版本:"+data.version+",是否上传新版本？")){
								bSuc = false;
							}
//					        zeroModal.confirm({
//					            content: '确定上传新版本文件吗？',
//					            contentDetail: "该目录已存在文件:"+data.filename+",版本:"+data.version+",是否上传新版本？",
//					            okFn: function() {
//					               bSuc = false;
//					            },
//					            cancelFn: function() {
//					                bSuc = true;
//					            }
//					        });

						} 
					}
				});
				
				if(!bSuc){
					break;
				}
			}
			
		return bSuc;

	}
	
//	$(".jFiler-input").css("width","340px");
	$(".jFiler-input").css("margin","5px 5px 10px 5px");

	$("	.jFiler-input-dragDrop").css("width","100%");

	$("#dirtree_div").jstree({
	   		"core": {
	   			'data': {
	   				'url': '/task/ziliao/getdirtree/',
	   				'data': function(node) {
	   					return {
	   						'id': node.id
	   					};
	   				}
	   			}
	   		},
	   		"plugins": ["themes", "json_data"],
	// 		"checkbox": {
	// 			"three_state": false
	// 		}
	});
	$('#dirtree_div').bind("activate_node.jstree", function (obj, e) {
	    var node = e.node;//
	    var isselect = node.state.selected;//选中还是取消
	    
		if (isselect){
			$("#hidden_uploaddir").val(node.id)
			var parents = node.parents;
			var tree = $.jstree.reference("#dirtree_div"); 
			var treetext="/"+node.text+"/";
			for(var i=0;i<parents.length-1;i++)
			{
				var pa = node.parents[i]
				treetext = "/" + tree.get_node(pa).text + treetext;
			}
			
			$("#uploaddirtree").html(treetext);
		}
	});


});



function FunSaveFileAndRelate()
{
	if(!(fileuploadcmp && diruploadcmp)){
		zeroModal.alert("还有文件没准备好,请稍等……");
		return;
	}
	
	if(uploaddocs.length==0){
		zeroModal.alert("请添加上传文件。");
		return;
	}
	
	if(selectedGJs.length==0){
		zeroModal.confirm("没有选择关联元素，是否继续上传？", function() {
			if(  $("#remarkFile").val() == ''){
					zeroModal.confirm("没有添加备注信息，是否继续上传？",function(){
						uploadFile_method();
				});
			}else{
						uploadFile_method();
			}
           
           	
        });
	}else{
			if(  $("#remarkFile").val() == ''){
				zeroModal.confirm("没有添加备注信息，是否继续上传？",function(){
						uploadFile_method();
				});
			}else{
						uploadFile_method();
			}
		   
	}


}

function uploadFile_method(){
		var remark = $("#remarkFile").val();
		var jsonobj = {"uploaddir":$("#hidden_uploaddir").val()};
			jsonobj.docs= JSON.stringify(uploaddocs)
			jsonobj.docsRelatedir= JSON.stringify(mapfileRelatedir)
			jsonobj.selectedGJs= JSON.stringify(selectedGJs)
			jsonobj.remark = remark;
			
			$.ajax({
				type: "post",
				cache: false,
				dataType: "json",
				data: jsonobj,
				success: function(data) {
					if(data.issuc == "true") {
						  zeroModal.success({
				            content: '保存成功!',
				            okFn: function() {
				                window.close();
				            }
				        });
					} else {
						 zeroModal.error(data.error);
					}
		
				}
			});
}
function FunSelectDir()
{
	$("#uploaddirdlg").modal("show");
}

function FunSetUploadDir()
{
	$("#uploaddirdlg").modal("hide");
}
