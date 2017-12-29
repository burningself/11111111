 /**********************************yxh*********************/
   /*********************** 项目概况页面 js 开始****
    * 添加快捷功能模块*
    * ******************************/


     
$(function(){
	
			
		
/*页面加载实现,请求全部并请求打勾的选项
 * 此处为刚进页面全部功能模块显示接口
 * 并实现可取消的模块出现打勾的图片
 */

onloadmodern();

			 
			 
/*实现加载页面完成,显示全部的方块
 * 此处调用已有功能板块
 */
$.ajax({
	type: 'get',
	url: '/assist/shortcut/getusershortcutlist/',
	dateType: 'json',
	success: function(data) {
		console.log('获取数据成功');
		console.log(data);
		for (var i = 0; i < data.shortcutlist.length; i++) {
			var html = '<a href="' + data.shortcutlist[i].url + '"style="background:' + data.shortcutlist[i].color + ';" class="shortcut drag-item" id="shortcut_' + data.shortcutlist[i].name + '" >' + '<i class="' + data.shortcutlist[i].icon + '" style="font-size:32px;">' + '</i>' + '<span class="shortcut-label">' + data.shortcutlist[i].name + '</span>' + '</a>'
			$("#plus_more").before(html);
			
			/***********实现鼠标悬停时颜色改变***********/
			$("#shortcut_"+data.shortcutlist[i].name).hover(function() {
				colorstr = $(this).css("background-color");
				$(this).css('background-color', '#C3BC69');
			}, function() {

				$(this).css('background-color', colorstr);

			})

		}

	},
	error: function(data) {
		console.log('调用失败');
	}
})

/*页面加载完成
 * 此处调用左边模块管理列表接口
 */
	$.ajax({
			type: 'get',
			url: '/assist/shortcut/getcategorylist/',
			dateType: 'json',
			success: function(data) {
				for(var i = 0;i<data.categorylist.length;i++){
				var str = '<li class="iconColor">'
				+'<a>'
				+'<i class="'+data.categorylist[i].icon+'" id="'+data.categorylist[i].categoryname+'" onclick="senddata(this)" style="font-size:20px;" class="bgcolor">'+data.categorylist[i].categoryname+'</i>'
				+'</a>'
				+'</li>'
				$("#tab").append(str);
				}
				
				
				
				console.log('获取数据成功');
				console.log(data);
				
				
			},
			error: function(data) {
				console.log('调用失败');
			}
		});

	/*点击全部********
	 * 此处为点击全部实现全部功能模块显示接口
	 **************************/
	$("#alls_modal").click(function(){
		$("#changyong").html("");
		onloadmodern();

	})


})


//
/******实现点击左边列表出现相应模块功能的内容，查询********
 * 此处为切换功能模块接口
 */
function senddata(obj){
		  var obj2 = obj.id
		 
			$.ajax({
			type: 'get',
			url: '/assist/shortcut/getcategoryfunction/',
			data: {
				'categoryname': obj2,
			},
			dateType: 'json',
			
			success: function(datas) {
				console.log('获取数据成功');
				console.log(datas);
				var html = '';
				html+='<div class="name">'+obj2+'</div>'
				for(var i = 0;i<datas.functionlist.length;i++){
				
					
				html+='<li class="box1 bgs" onclick="ischeckpic(this);" id="'+datas.functionlist[i].name+'" style="background:'+datas.functionlist[i].color+'"data-url="'+datas.functionlist[i].url+'">'
			       
					+'<dl class="photos">'
					if(datas.functionlist[i].isselect=="true"){

					html+='<div class="ischeck bgpic"></div>'
			}else{
				html+='<div class="ischeck bgpics"></div>'
			}	
						html+='<dt class="distence"><i class="'+datas.functionlist[i].icon+' " style="font-size:50px;color:#fff;"></i></dt>'
						
						+'<dd class="title_text">'+datas.functionlist[i].name +'</dd>'
						
					+'</dl>'

				+'</li>';
				}
				$("#changyong").html(html);

				
			},
			error: function(data) {
				console.log('调用失败');
			}
		/*})*/
	})
}



/********实现点击添加删除功能***********
 * 此处为添加删除功能模块接口
 */
function ischeckpic(obj){
	
	/*alert(obj.id)*/
	var mask;
	 var functionname=obj.id; 
	 
	/*mask=1; */ 
	  
	if( $("#"+obj.id+" div").hasClass("bgpic")){
		$("#"+obj.id+" div").removeClass("bgpic").addClass("bgpics");
	   mask=0;
	}else{
		$("#"+obj.id+" div").removeClass("bgpics").addClass("bgpic");
		
		 mask=1;
		 
	}



          $.ajax({
			type: 'get',
			url: '/assist/shortcut/setusershortcut/',
			data: {
				'functionname': functionname,
				"ischeck":mask
			},
			dateType: 'json',
			success: function(data) {
                console.log('获取响应数据成功123');
				console.log(data);

				var html ='<a href="#"  class="shortcut drag-item" id="shortcut_'+functionname+'">'
					+'<i class="shortcut-icon">'
					+'</i><span class="shortcut-label" >'+functionname+'</span>'
					+'</a>'
					

				if(mask==1){
					/***********获取当前的颜色***********/
					var bgs = $("#"+functionname).css("background-color");
					/***********给当前的li标签添加一个i图片标签***********/
					var colorClass = $("#"+functionname+" i").attr('class');
					/***********获取当前存取的url***********/
					var urls = $("#"+functionname).attr("data-url");
					
					$("#plus_more").before(html);
					/***********把取出的颜色赋值给新增加的元素***********/
					$("#shortcut_"+functionname).css("background-color",bgs);
					/***********把增加的i标签添加到新增加的元素上***********/
					$("#shortcut_"+functionname+" i").addClass(colorClass);
					/***********为新增加的元素设置url属性***********/
					$("#shortcut_"+functionname).attr("href",urls);
					
					
					
					/***********实现鼠标悬停时颜色改变***********/
					$("#shortcut_"+functionname).hover(function() {

		       	  			$("#shortcut_"+functionname).css("background","#C3BC69");
	               }, function() {

		           		$("#shortcut_"+functionname).css('background-color', bgs);

	                 })

				}else if(mask==0){
					id="#shortcut_"+functionname;
					$(id).remove();
					
				
				}
				
		     
			/*$(".bg").css("background",rc());*/	
			},
			error: function(data) {
				console.log('调用失败');
				$(".shortcuts").append("");
			}
		})
          
          
 
          
          
 }

/*页面加载实现,请求全部并请求打勾的选项
 * 此处为刚进页面全部功能模块显示接口
 * 并实现可取消的模块出现打勾的图片
 */
function onloadmodern(){
	$.ajax({
			type: 'get',
			url: '/assist/shortcut/getcategoryfunction/',
			dateType: 'json',
			success: function(data) {
				console.log('获取数据成功');
				console.log(data);
				for(var i = 0;i<data.functionlist.length;i++){			
			var html ='<li class="box1 bg" style="float:left;background:'+data.functionlist[i].color+'" onclick="ischeckpic(this);" id="'+data.functionlist[i].name+'" data-url="'+data.functionlist[i].url+'">'
			if(data.functionlist[i].isselect=="true"){
					html+='<div class="ischeck bgpic"></div>'
					/*mask=1;*/
			}else{
				html+='<div class="ischeck bgpics"></div>'
			}
		
						html+='<dl class="photos">'
							+'<dt class="distence"><i class="'+data.functionlist[i].icon+' " style="font-size:50px;color:#fff;"></i></dt>'
							+'<dd class="title_text">'+data.functionlist[i].name +'</dd>'
							
						+'</dl>'
					+'</li>'		
			$(".box1").css("background-color","+data.functionlist[i].color+");
			$("#changyong").append(html);
			

			}
				

			},
			error: function(data) {
				console.log('调用失败');
			}
		})
}






 /**********************************yxh*********************/
   /*********************** 项目概况页面 js结束****
    * 添加快捷弹窗功能模块结束*
    * ******************************/


	







