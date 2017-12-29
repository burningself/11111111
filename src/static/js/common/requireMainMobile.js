require.config({
	waitSeconds: 30,
    paths: {
        'raphael':'/js/morris.js-0.5.1/raphael-min',
        'morris':'/js/morris.js-0.5.1/morris.min',
        'swiper':'/js/swiperjs/swiper.min',
    },
    
    shim : {
    	'morris': '/css/project/morris.css',
        'swiper': '/css/swipercss/swiper.min.css',
        
    }
});

$(window).ready(function() {
	//  init datePicker
    initDate_Picker();
});

require(['raphael','morris','swiper'], function() {
    //draw_chart
    draw_line_chart();
    //draw_donut_chart();
    initSwiper();
});

//footer configure
function footerconfig() {
	$(window).scroll(function(){
		if ($(window).scrollTop() < 100) {
	    	$( "footer" ).stop().animate({
	    		marginBottom : 0, 
			 }, 100);
	    } else {
	    	$( "footer" ).stop().animate({
	    		marginBottom : '-90px', 
			 }, 100);
			 
//			$( ".nav_tool" ).stop().animate({
//	    		opacity: 1
//			 }, 200);
	    }
	});
}


function loadConfig(){
	var username=$('#username').attr('class');
	var pagePath = window.location.pathname;
	var pro = window.location.hostname;
	$.ajax({
		  type:"get",
		  url:"/user/costomPage/",
		  cache:false,
		  dataType:"text",
		  data:{"user": username,
		  		"pagePath": pagePath,
		  		"pro": pro},
		  success: function(data){
		  	if(data!="Failed"){
		  		var configArray= data.split(":");
		  		if(configArray){
					for(var i in configArray){
						$("#" + configArray[i]).css("display",'none');
					}
				}
		  		
		  		$('input[name="configBox"]').each(function(){  
					 if($.inArray($(this).val(), configArray) >= 0 ){ $(this).attr("checked","checked");} 
				 }); 
		  	}
		  	return true;
		  },
		  error:function(data){
		  	alert("无法获取配置信息！");
	      	return false;
	      },
	      complete:function(data){
			}
		});
}

function submitConfig(){
	var username=$('#username').attr('class');;
	var saveName = $("#saveName").val();
	var configData =[];  
	var pagePath = window.location.pathname;
	var pro = window.location.hostname;
	$('input[name="configBox"]:checked').each(function(){    
		 configData.push($(this).val());    
	 });    
	
	if(pagePath && pro && username){
		$.ajax({
		  type:"post",
		  url:"/user/costomPage/",
		  cache:false,
		  dataType:"text",
		  data:{"user": username,
		  		"savename": saveName, 
		  		"configData":configData.join(":"), 
		  		"pagePath": pagePath,
		  		"pro": pro},
		  success: function(data){
		  	if(data=="Succeed"){
				$('#configPage').modal('hide');
				$('input[name="configBox"]').each(function(){   
					$("#" + $(this).val()).css("display","inline-block");
				}); 
				for(var i in configData){
					$("#" + configData[i]).css("display",'none');
				}
				
		  	}
		  	return true;
		  },
		  error:function(data){
		  	alert("信息不全！");
	      	return false;
	      },
	      complete:function(data){
			}
		});
	}else{alert("信息不全！");}
}

// Morris Area Chart
function draw_donut_chart(){
	$.ajax({
		  type:"post",
		  url:"/index/data/",
		  cache:false,
		  dataType:"json",
		  data:{'reqType':'donut-pb'},
		  success: function(data){
		  	if(data.status=="Succeed"){
		  		for(each in data.categorys){
		  			if(each==0){
		  				$(".swiper-wrapper-pb").append('<div class="swiper-slide tab-pane fade in active"> </div>');
		  			}else{
		  				$(".swiper-wrapper-pb").append('<div class="swiper-slide tab-pane fade in"> </div>');
		  			}
		  			$($(".swiper-wrapper-pb .swiper-slide")[each]).append( '<div class="donut_unit pb_unit"></div>');
		  			$($(".pb_unit")[each]).append("<h4>" + data.categorys[each].description + "</h4>");
		  			$($(".pb_unit")[each]).append('<div class="donut-draw pb-donut-draw" id="pb-donut_' + each.toString() + '"></div>');
					
					var donutData = new Array();
					donutData= data.categorys[each].data;
					console.log(donutData);
			  		Morris.Donut({
				        element: 'pb-donut_' + each.toString(),
				        data: donutData,
				        colors: ["#89C589","grey","lightskyblue"],
				        formatter: function (y) { return y.toString() + "%"},
				        resize: true
				    });
				}
		  		var pbSwiper = new Swiper ('.swiper-container-pb', {
					initialSlide: 0,
				    slidesPerView: 'auto',
				    spaceBetween: 0,
				    speed:500,
				    autoplay:3000,
				    grabCursor: true,
				    freeMode: true,
				});
		  		
		  	}
		  	else{
		  		alert(data.msg);
		  	}
		  },
		  error:function(data){
		  	alert("服务器错误");
	      	return false;
	      },
	      complete:function(data){
		  }
	})
	if($(".donut-task-row").length > 0){
		$.ajax({
			  type:"post",
			  url:"/index/data/",
			  cache:false,
			  dataType:"json",
			  data:{'reqType':'donut-task'},
			  success: function(data){
			  	if(data.status=="Succeed"){
			  		for(each in data.categorys){
			  			if(each==0){
			  				$(".swiper-wrapper-task").append('<div class="swiper-slide tab-pane fade in active"> </div>');
			  			}else{
			  				$(".swiper-wrapper-task").append('<div class="swiper-slide tab-pane fade in"> </div>');
			  			}
			  			
			  			$($(".swiper-wrapper-task .swiper-slide")[each]).append( '<div class="donut_unit task_unit"></div>');
			  			$($(".task_unit")[each]).append("<h4>" + data.categorys[each].description + "</h4>");
			  			$($(".task_unit")[each]).append('<div class="donut-draw task-donut-draw" id="task-donut_' + each.toString() + '"></div>');
						
						var donutData = new Array();
						donutData= data.categorys[each].data;
				  		Morris.Donut({
					        element: 'task-donut_' + each.toString(),
					        data: donutData,
					        colors: ["#89C589","lightskyblue","grey",],
					        formatter: function (y) { return y.toString() + "%"},
					        resize: true
					    });
					}
			  		var taskSwiper = new Swiper ('.swiper-container-task', {
						initialSlide: 0,
					    slidesPerView: 'auto',
					    spaceBetween: 0,
					    speed:500,
					    autoplay:3000,
					    grabCursor: true,
					    freeMode: true,
					});
			  	}
			  	else{
			  		alert(data.msg);
			  	}
			  },
			  error:function(data){
			  	alert("服务器错误");
		      	return false;
		      },
		      complete:function(data){
			  }
		})	
	}
	$.ajax({
		  type:"post",
		  url:"/index/data/",
		  cache:false,
		  dataType:"json",
		  data:{'reqType':'donut-area'},
		  success: function(data){
		  	if(data.status=="Succeed"){
		  		for(each in data.categorys){
		  			if(each==0){
		  				$(".swiper-wrapper-factory").append('<div class="swiper-slide"> </div>');
		  			}else{
		  				$(".swiper-wrapper-factory").append('<div class="swiper-slide"> </div>');
		  			}
		  			
		  			$($(".swiper-wrapper-factory .swiper-slide")[each]).append( '<div class="donut_unit factory_unit"></div>');
		  			$($(".factory_unit")[each]).append("<h4>" + data.categorys[each].description + "</h4>");
		  			$($(".factory_unit")[each]).append('<div class="donut-draw factory-donut-draw" id="factory-donut_' + each.toString() + '"></div>');
					
					var donutData = new Array();
					donutData= data.categorys[each].data;

			  		Morris.Donut({
				        element: 'factory-donut_' + each.toString(),
				        data: donutData,
				        colors: ["#89C589","grey","lightskyblue"],
				        formatter: function (y) { return y.toString() + "%"},
				        resize: true
				    });
				}
		  		
		  		var factorySwiper = new Swiper ('.swiper-container-factory', {
					initialSlide: 0,
				    slidesPerView: 'auto',
				    spaceBetween: 0,
				    speed:500,
				    autoplay:3000,
				    grabCursor: true,
				    freeMode: true,
				}); 
		  		
		  	}
		  	else{
		  		alert(data.msg);
		  	}
		  },
		  error:function(data){
		  	alert("服务器错误");
	      	return false;
	      },
	      complete:function(data){
		  }
	})
}

function draw_line_chart(){
     	
	var monthData = new Array();
	var weekData = new Array();
    $.ajax({
		  type:"post",
		  url:"/index/data/",
		  cache:false,
		  dataType:"json",
		  data:{'reqType':'line',"keyword": '',},
		  success: function(data){
		  	if(data.status=="Succeed"){
				for (var i = 0; i < data.monthCountList.length; i++){
					var tmpDic = new Array(); 
					tmpDic["month"]=data.monthCountList[i].date;
					tmpDic["jihua"]=data.monthCountList[i].jihua;
					tmpDic["anzhuang"]=data.monthCountList[i].anzhuang;
					monthData[i]=tmpDic;
				}
				
				for (var i = 0; i < data.weekCountList.length; i++){
					var tmpDic = new Array(); 
					tmpDic["day"]=data.weekCountList[i].date;
					tmpDic["anzhuang"]=data.weekCountList[i].anzhuang;
					weekData[i]=tmpDic;
				}
				
				if ($('#month-line').length) {
			        Morris.Line({
			        	element: "month-line",
			        	data: monthData,
			            xkey: 'month',
			            ykeys: ['jihua', 'anzhuang'],
				            labels: ['完成构件', '计划完成'],
				          hideHover: true,
						  gridTextColor: "black",	
				          lineWidth: 2,
				          pointSize: 4,
				          lineColors: ["#67BDF8", "lightgreen"],
			          fillOpacity: 0.5,
			          smooth: true,
					  ymax:'auto',
					  parseTime: false,
					  resize: true
			        });
			   }
				
				if ($('#week-line').length) {
			        Morris.Line({
			        	element: "week-line",
			        	data: weekData,
			            xkey: 'day',
			            ykeys: ['anzhuang'],
				            labels: ['完成构件'],
				          hideHover: true,
						  gridTextColor:"black",	
				          lineWidth: 2,
				          pointSize: 4,
				          lineColors: ["#67BDF8"],
			          fillOpacity: 0.5,
			          smooth: true,
			          ymax:'auto',
			          parseTime: false,
			          resize: true,
			        });
			   }
			}
		  	else{
		  		alert(data.msg);
		  	}
		  },
		  error:function(data){
		  	alert("服务器错误");
	      	return false;
	      },
	      complete:function(data){
		  }
	});
    
    
}

function initSwiper(){
	var monthSwiper = new Swiper ('.swiper-container-produce' , {
	    initialSlide: 0,
	    effect : 'flip',
		flip: {
	            slideShadows : true,
	            limitRotation : true,
	      },
		onSlideChangeEnd: function(swiper){
		    }
	  })     
	
	var problemSwiper = new Swiper ('.swiper-container-problem' , {
	    initialSlide: 0,
	    effect : 'flip',
		flip: {
	            slideShadows : true,
	            limitRotation : true,
	      },
		onSlideChangeEnd: function(swiper){
		    }
	 }) 
	 
	 var pbSwiper = new Swiper ('.swiper-container-pb' , {
		initialSlide: 0,
	    effect : 'flip',
		flip: {
	            slideShadows : true,
	            limitRotation : true,
	      },
		onSlideChangeEnd: function(swiper){
		    }
	 }) ;
	 
	 var taskSwiper = new Swiper ('.swiper-container-task' , {
		initialSlide: 0,
	    slidesPerView: 'auto',
	    spaceBetween: 0,
	    speed:500,
	    grabCursor: true,
	    freeMode: true,
	 }) ;
	 
	var factorySwiper = new Swiper ('.swiper-container-factory', {
		initialSlide: 0,
	    slidesPerView: 'auto',
	    spaceBetween: 0,
	    speed:500,
	    autoplay:1000,
	    grabCursor: true,
	    freeMode: true,
	}); 
	 
}

function loadTableData(tableName,type){
	$.ajax({
	  type:"post",
	  url:"/index/table/",
	  cache:false,
	  dataType:"json",
	  data:{"type":type},
	  success: function(data){
	  	if(data.status == "Succeed"){
	  		var tmpHtml="";
	  		for(each in data.list_items_head){
	  			if(typeof(data.list_items_head[each])=='string'){
	  				tmpHtml=tmpHtml + "<th>" + data.list_items_head[each]+ "</th>";
	  			}
	  		}
	  		$("." + tableName + "> thead > tr").html(tmpHtml);
	  		
	  		for(each in data.list_items){
				tmpHtml=$("." + tableName + "> tbody > tr")[each].innerHTML;
				for(eachIndex in data.list_items_head){					
					if(typeof(data.list_items_head[eachIndex])=='string' && data.list_items_head[eachIndex]!=""){
						if(data.list_items[each][data.list_items_head[eachIndex]] !="/" || data.list_items[each][data.list_items_head[eachIndex]] == 0 ){
							tmpHtml=tmpHtml + "<td>" + data.list_items[each][data.list_items_head[eachIndex]] + "</td>" ;
						}
					}
				}
				$("." + tableName + "> tbody > tr")[each].innerHTML=tmpHtml;
	  		}
	  		return true;
	  	}
	  },
	  error:function(data){
//		  	alert("无法获取配置信息！");
      	return false;
      },
      complete:function(data){
		}
	});
	
}

function initDate_Picker(){
	$('#datetimeselect').datetimepicker({
			language:'zh-CN',
			weekStart: 1,
			todayBtn:  1,
			autoclose: 1,
			todayHighlight: 1,
			startView: 2,
			minView: 2,
			forceParse: 0
	}).on("changeDate",function(dateStr){	
		var cdate = dateStr.date;
		var chooseDate = cdate.getFullYear()+"/"+(cdate.getMonth()+1)+"/"+cdate.getDate();
		
		var weekData = new Array();
		pbtype=$(".week-filter").children('option:selected').val();
		eleClass=$(this).attr("class");
		$.ajax({
			  type:"post",
			  url:"/index/data/",
			  cache:false,
			  dataType:"json",
			  data:{'reqType':'line',"keyword": pbtype,"chooseDate": chooseDate},
			  success: function(data){
				if(data.status=="Succeed"){				
					for (var i = 0; i < data.weekCountList.length; i++){
						var tmpDic = new Array(); 
						tmpDic["day"]=data.weekCountList[i].date;
						for (var j = 0; j < data.weekCountList[i].countlist.length; j++){
							tmpDic[data.weekCountList[i].countlist[j].key]=data.weekCountList[i].countlist[j].value;
						}
						weekData[i]=tmpDic;
					}
					
					var ykeysValues = new Array();
					var labelsValues = new Array();
					var ColorsValues = new Array();
					for (var i = 0; i < data.weekCountTypeList.length; i++){
						ykeysValues[i] = data.weekCountTypeList[i].key;
						labelsValues[i] = data.weekCountTypeList[i].name;
						ColorsValues[i] = data.weekCountTypeList[i].color;
						
					}
					
				
					if ($('#week-line').length) {
						$("#week-line").html('');
						Morris.Line({
							element: "week-line",
							data: weekData,
							xkey: 'day',
							ykeys: ykeysValues,
							labels: labelsValues,
						  hideHover: true,
						  gridTextColor:"black",	
						  lineWidth: 2,
						  pointSize: 4,
						  lineColors: ColorsValues,
						  fillOpacity: 0.5,
						  smooth: true,
						  ymax:'auto',
						  parseTime: false,
						  resize: true,
						});
					}
				}
				else{
					alert(data.error);
				}
			  },
			  error:function(data){
	//		  	alert("服务器错误");
				return false;
			  },
			  complete:function(data){
			  }
		});
		   
	});
}