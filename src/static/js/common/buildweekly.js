var weeklyid="";
$(function() {
	weeklyid = $("#weeklyid").val();
	intVue();
	_app.loadData();
	_app.loadItem();
	
		$("#selFloor").change(function() {
				var selFloor = $("#selFloor option:selected").val();
				if(selFloor!=""){
					_shiijindu._selElevations = selFloor+",";
				}else{
					_shiijindu._selElevations = "";
				   
				}
				 _shiijindu.filterPblist();
	});
	
	

		$("#selFloor2").change(function() {
				var selFloor = $("#selFloor2 option:selected").val();
				if(selFloor!=""){
					_jihuajindu._selElevations = selFloor+",";
				}else{
					_jihuajindu._selElevations = "";
				   
				}
				 _jihuajindu.filterPblist();
	});
});

function intVue(){
	//Vue.component('pagination');
	var wysihtml5cfg = {
		locale: 'zh-CN',
		toolbar: {
			"font-styles": true, // Font styling, e.g. h1, h2, etc.
			"emphasis": true, // Italics, bold, etc.
			"lists": true, // (Un)ordered lists, e.g. Bullets, Numbers.
			"html": false, // Button which allows you to edit the generated HTML.
			"link": false, // Button to insert a link.
			"image": false, // Button to insert an image.
			"color": false, // Button to change color of font
			"blockquote": false, // Blockquote
		}
	};
	
    _app = new Vue({
        el:"#tbl_exception",
        delimiters:["[[", "]]"],
        data :{
        	 zongbao:false,
        	 jianli:false,
        	 needfile:false,
        	 curtype:'',
             anquan : [],
             zhiliang : [],
             anquan_jianli : [],
             zhiliang_jianli : [],
             newItem:{
             	id:'',
             	desc:'',
             	status:'',
             	readurl:'',
             }
          },
        methods:{
        		loadData:function(){
        			var that = this;
					 $.ajax({
						url: "/task/projecttask/buildweekly2_data/",
						type: 'get',
						async: false,
						cache: false,
						dataType:"json",
						data:{"weeklyid":weeklyid},
						success: function(data) {
							if(data.issuc == "true") {
								for(var each in data.content) { //不使用过滤
									try{
										$('#' + each).html(unescape(data.content[each].replace(/\\u/g, '%u')));
									}catch(e){
										//TODO handle the exception
									}
							
								}
								
								if(data.zongbao=="true"){
									that.zongbao = true;
									that.initZongbao();
								}
								if(data.jianli=="true"){
									that.jianli = true;
									that.initJianli();
								}
								
								if(data.needfile=="true"){
									that.needfile = true;
								}
								
							}
							
						},
						error: function() {
							alert("获取数据失败！");
						}
					});
	           },
	           initZongbao:function(){
	           		$('#shijijinduDesc').editable({
					url: '/task/projecttask/buildweekly2/',
					type: "wysihtml5",
					wysihtml5: wysihtml5cfg,
					title: '输入进度目标实际情况',
					placement: 'middle'
				});
			
				$('#anquanshigongDesc').editable({
					url: '/task/projecttask/buildweekly2/',
					type: "wysihtml5",
					wysihtml5: wysihtml5cfg,
					title: '输入安全文明施工情况',
					placement: 'bottom'
				});
			
				$('#jishuzhiliangDesc').editable({
					url: '/task/projecttask/buildweekly2/',
					type: "wysihtml5",
					wysihtml5: wysihtml5cfg,
					title: '输入质量技术情况',
					placement: 'bottom'
				});
			
				$('#jihuajinduDesc').editable({
					url: '/task/projecttask/buildweekly2/',
					type: "wysihtml5",
					wysihtml5: wysihtml5cfg,
					title: '输入进度计划目标',
					placement: 'middle'
				});
			
				$('#jihuaanquanDesc').editable({
					url: '/task/projecttask/buildweekly2/',
					type: "wysihtml5",
					wysihtml5: wysihtml5cfg,
					title: '输入安全文明施工计划',
					placement: 'bottom'
				});
			
				$('#jihuazhiliangDesc').editable({
					url: '/task/projecttask/buildweekly2/',
					type: "wysihtml5",
					wysihtml5: wysihtml5cfg,
					title: '输入技术质量保障计划',
					placement: 'bottom'
				});
			
				$('#jihuaotherDesc').editable({
					url: '/task/projecttask/buildweekly2/',
					type: "wysihtml5",
					wysihtml5: wysihtml5cfg,
					title: '输入其他措施计划',
					placement: 'bottom'
				});
			
				$('#xietiaoshiyiDesc').editable({
					url: '/task/projecttask/buildweekly2/',
					type: "wysihtml5",
					wysihtml5: wysihtml5cfg,
					title: '输入协调事宜',
					placement: 'top'
				});
	           },
	           initJianli:function(){
					$('#luoshijinduDesc').editable({
						url: '/task/projecttask/buildweekly2/',
						type: "wysihtml5",
						wysihtml5: wysihtml5cfg,
						title: '输入工程进度情况',
						placement: 'top'
					});
				
					$('#loushiotherDesc').editable({
						url: '/task/projecttask/buildweekly2/',
						type: "wysihtml5",
						wysihtml5: wysihtml5cfg,
						title: '输入其他事宜',
						placement: 'top'
					});
	           },
		       loadItem:function(){
	                var that = this;

	                $.ajax({
	                    url : "/task/projecttask/buildweekly2_item/",
	                    type:"post",
	                    dataType:"json",
						data:{"opr":"getall","weeklyid":weeklyid},
	                    error:function(){alert('请求列表失败')},
	                    success:function(res){
	                        if (res.issuc == "true") {
	                            that.anquan = eval(unescape(JSON.stringify(res.anquan).replace(/\\u/g, '%u')));
	                            that.zhiliang = res.zhiliang;
	                            that.anquan_jianli = res.anquan_jianli;
	                            that.zhiliang_jianli = res.zhiliang_jianli;
	                        }
	                    }
	                });
	          },
	           additemDlg:function(type){
	           		var that = this;
	           		that.curtype=type;
	           		$("#additemdlg").modal('show');
	           },
	           addItem: function(){
	           		var that = this;
	           	
	           		if(that.newItem.desc==''){
	           			that.newItem = {id:'',desc: '', status: '',readurl:''}
	           			return;
	           		}
	           		that.newItem.id="custom_"+Date.parse(new Date());
	           	
	           	 	if(that.curtype=="anquan")
	           	 	{
	           	 		that.anquan.push(that.newItem);
	           	 	}
	           	 	else if(that.curtype=="zhiliang")
	           	 	{
	           	 		that.zhiliang.push(that.newItem);
	           	 	}
	           	 	else if(that.curtype=="anquan_jianli")
	           	 	{
	           	 		that.anquan_jianli.push(that.newItem);
	           	 	}
	           	 	else if(that.curtype=="zhiliang_jianli")
	           	 	{
	           	 		that.zhiliang_jianli.push(that.newItem);
	           	 	}else{
	           	 		return;
	           	 	}
	           	 	
	           	 	$.ajax({
	                    url : "/task/projecttask/buildweekly2_item/",
	                    type:"post",
	                    dataType:"json",
						data:{"opr":"addone","curtype":that.curtype,"item":JSON.stringify(that.newItem),"weeklyid":weeklyid},
	                    error:function(){alert('请求列表失败')},
	                    success:function(res){
	                        if (res.issuc == "true") {
								
	                        }
	                    }
	                });

                    // 添加完newPerson对象后，重置newPerson对象
                    that.newItem = {id:'',desc: '', status: '',readurl:''}
                },
               deleteItem: function(type,index){
                    // 删一个数组元素
                    var that = this;
                    var id = '' ;
                    if(type=="anquan")
	           	 	{
	           	 		id = that.anquan[index].id;
	           	 		that.anquan.splice(index,1);
	           	 	}
	           	 	else if(type=="zhiliang")
	           	 	{
	           	 		id = that.zhiliang[index].id;
	           	 		that.zhiliang.splice(index,1);
	           	 		
	           	 	}
	           	 	else if(type=="anquan_jianli")
	           	 	{
	           	 		id = that.anquan_jianli[index].id;
	           	 		that.anquan_jianli.splice(index,1);
	           	 		
	           	 	}
	           	 	else if(type=="zhiliang_jianli")
	           	 	{
	           	 		id = that.zhiliang_jianli[index].id;
	           	 		that.zhiliang_jianli.splice(index,1);
	           	 		
	           	 	}else{
	           	 		return;
	           	 	}
	           	 	
	           	 	$.ajax({
	                    url : "/task/projecttask/buildweekly2_item/",
	                    type:"post",
	                    cache: false,
	                    dataType:"json",
						data:{"opr":"deleteone","curtype":type,"id":id,"weeklyid":weeklyid},
	                    error:function(){alert('请求列表失败')},
	                    success:function(res){
	                        if (res.issuc == "true") {

	                        }
	                    }
	                });
                    
               },
               showissue:function(href){
					$("#readframe").attr("src","");
					$("#readframe").attr("src",href);
					$("#readissuredlg").modal("show");
					
				},
               tracepb:function(){
					$("#tracepbdlg").modal("show");
					
				}

          },

    })
}


function guid() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
    return v.toString(16);
  });
}

//function showissue(href) {
//	var dwidth = window.screen.width * 1 / 2;
//	var dheight = window.screen.height * 2 / 3;
//	var top = 200;　　
//	var left = window.screen.width * 1 / 4;
//	window.open(href, 'newwindow', "width=" + dwidth + ",height=" + dheight + "," + "top=" + top + ",left=" + left + ",toolbar=no,menubar=no,scrollbars=no, resizable=no,location=no, status=no");
//}

function captureAndUpload() {
	$("#shotviewer").css("display", "block");
	$("#viewer").css("display", "none");

	$("#shotviewer2").css("display", "block");
	$("#viewer2").css("display", "none");

	html2canvas($("#tbl_exception"), {
		onrendered: function(canvas) {
			//var url = canvas.toDataURL();
			//以下代码为下载此图片功能
			//var triggerDownload = $("<a>").attr("href", url).attr("download", "异常信息.png").appendTo("body");
			//triggerDownload[0].click();
			//triggerDownload.remove();

			var imagedata = canvas.toDataURL('image/png');
			var imgdata = imagedata.replace(/^data:image\/(png|jpg);base64,/, "");
			//ajax call to save image inside folder
			$.ajax({
				url: '/uploadfile_blob/',
				data: {
					imgdata: imgdata
				},
				type: 'post',
				success: function(response) {
					if(response.issuc == "true") {
						alert("归档成功！");
						location.reload(); 
					} else {
						alert("保存失败！");
					}
					//$('#image_id img').attr('src', response);
				}
			});

			$("#shotviewer").css("display", "none");
			$("#viewer").css("display", "");

			$("#shotviewer2").css("display", "none");
			$("#viewer2").css("display", "");
		}
	});
}

function SaveWeeklyFile() {
	var $container = $(_shiijindu._viewer.container);
	var width = $container.width();
	var height = $container.height();

	_shiijindu._viewer.getScreenShot(width, height, function(newBlobURL) {

		var xhr = new XMLHttpRequest();
		xhr.open('GET', newBlobURL, true);
		xhr.responseType = 'blob';
		xhr.onload = function(e) {
			if(this.status == 200) {
				var myBlob = this.response;
				var data = new FormData();
				data.append('file', myBlob);

				$.ajax({
					url: "/uploadfile_conc2/",
					type: 'POST',
					async: false,
					data: data,
					contentType: false,
					processData: false,
					success: function(data) {

						$("#imgshotviewer").attr("src", data.url);

					},
					error: function() {
						alert("保存失败！");
					}
				});
			} else {
				alert("保存失败！");
			}
		};

		xhr.send();
	});

	var $container = $(_jihuajindu._viewer.container);
	var width = $container.width();
	var height = $container.height();
	_jihuajindu._viewer.getScreenShot(width, height, function(newBlobURL) {

		var xhr = new XMLHttpRequest();
		xhr.open('GET', newBlobURL, true);
		xhr.responseType = 'blob';
		xhr.onload = function(e) {
			if(this.status == 200) {
				var myBlob = this.response;
				var data = new FormData();
				data.append('file', myBlob);

				$.ajax({
					url: "/uploadfile_conc2/",
					type: 'POST',
					async: false,
					data: data,
					contentType: false,
					processData: false,
					success: function(data) {

						$("#imgshotviewer2").attr("src", data.url);
						captureAndUpload();
					},
					error: function() {
						alert("保存失败！");
					}
				});
			} else {
				alert("保存失败！");
			}
		};
		xhr.send();

	});

}



