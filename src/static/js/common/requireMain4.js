require.config({
	waitSeconds: 30,
    paths: {
		'Sample': '/js/web3d/Extension/Autodesk.ADN.Viewing.Extension.Sample/Autodesk.ADN.Viewing.Extension.Sample',
		'loadmodlegeneral': '/js/web3d/scripts/LoadModelGeneral',
        'raphael':'/js/morris.js-0.5.1/raphael-min',
        'morris':'/js/morris.js-0.5.1/morris.min',
    }
});
 
require(['Sample','loadmodlegeneral'], function(v3d) {
	loadInitialModel();
});

 
require(['raphael','morris'], function() {
    //draw_chart
    draw_donut_chart();
    draw_line_chart();
});

// Morris Donut Chart
function draw_donut_chart(){		
	var monthData = new Array();
	var weekData = new Array();
    $.ajax({
		  type:"post",
		  url:"/index/data/",
		  cache:false,
		  dataType:"json",
		  data:{'reqType':'eventlist'},
		  success: function(data){
		  	if(data.status=="Succeed"){
		  		if((data.anquan_jieshu+data.anquan_chuli) == 0){
					Morris.Donut({
				        element: 'anquan_donut',
				        data: [
				            {label: '已结束安全问题', value: 100},
				            {label: '处理中安全问题', value: data.anquan_chuli},
				        ],
				        colors: ["#89C589","#D9534F"],
				        formatter: function (y) { return y + "%"},
				        resize: true
				    });
				}else{
					Morris.Donut({
				        element: 'anquan_donut',
				        data: [
				            {label: '已结束安全问题', value: data.anquan_jieshu},
				            {label: '处理中安全问题', value: data.anquan_chuli},
				        ],
				        colors: ["#89C589","#D9534F"],
				        formatter: function (y) { return y},
				        resize: true
				   });
				}
				
				if((data.zhiliang_jieshu+data.zhiliang_chuli) == 0){
					Morris.Donut({
				        element: 'zhiliang_donut',
				        data: [
				            {label: '已结束质量问题', value: 100},
				            {label: '处理中质量问题', value: data.zhiliang_chuli},
				        ],
				        colors: ["#89C589","#D9534F"],
				        formatter: function (y) { return y +"%"},
				        resize: true
				    });
				}else{
					Morris.Donut({
				        element: 'zhiliang_donut',
				        data: [
				            {label: '已结束质量问题', value: data.zhiliang_jieshu},
				            {label: '处理中质量问题', value: data.zhiliang_chuli},
				        ],
				        colors: ["#89C589","#D9534F"],
				        formatter: function (y) { return y},
				        resize: true
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

// Morris Area Chart
function draw_line_chart(){
	$('.month-filter').change();
	$('.week-filter').change();
}	
$('.month-filter').change(function(){ 
	var monthData = new Array();
	pbtype=$(this).children('option:selected').val();
	if($(".month-duration").html() != ""){
		dis = $(".month-duration").html();
	}else{
		dis = 6;
	}
	eleClass=$(this).attr("class");
	$.ajax({
		  type:"post",
		  url:"/index/data/",
		  cache:false,
		  dataType:"json",
		  data:{'reqType':'line',"keyword": pbtype,"duration":dis},
		  success: function(data){
		  	if(data.status=="Succeed"){
				for (var i = 0; i < data.monthCountList.length; i++){
					var tmpDic = new Array(); 
					tmpDic["month"]=data.monthCountList[i].date;
					tmpDic["jihua"]=data.monthCountList[i].jihua;
					tmpDic["anzhuang"]=data.monthCountList[i].anzhuang;
					monthData[i]=tmpDic;
				}
				
				if(eleClass.indexOf("month")){
					if ($('#month-line').length) {
						$("#month-line").html('');
				        Morris.Line({
				        	element: "month-line",
				        	data: monthData,
				            xkey: 'month',
				            ykeys: ['jihua', 'anzhuang'],
				            labels: ['计划安装完成', '安装完成'],
				          hideHover: true,
						  gridTextColor: "black",	
				          lineWidth: 2,
				          pointSize: 4,
				          lineColors: ["lightgreen","#67BDF8" ],
				          fillOpacity: 0.5,
				          smooth: true,
						  ymax:'auto',
						  parseTime: false,
						  resize: true
				        });
				   }
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
	
$('.week-filter').change(function(){ 
	var weekData = new Array();
	pbtype=$(this).children('option:selected').val();
	eleClass=$(this).attr("class");
	$.ajax({
		  type:"post",
		  url:"/index/data/",
		  cache:false,
		  dataType:"json",
		  data:{'reqType':'line',"keyword": pbtype,},
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
				
				if( eleClass.indexOf("week")){
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



 