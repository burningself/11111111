
var datatable_options = {
	  "iDisplayLength": 15,
      "searching": true,
      "ordering":  false,
      "bLengthChange":false,
      "bInfo":true,
      //"bStateSave": true, //保存状态到cookie *************** 很重要 ， 当搜索的时候页面一刷新会导致搜索的消失。使用这个属性就可避免了
      //"pagingType": "input",
      "oLanguage": {
      	 	"sEmptyTable": "没有相关记录",
            "sLengthMenu": "每页显示 _MENU_ 条记录",
            "sZeroRecords": "对不起，查询不到相关数据",
            "sInfo": "当前显示 _START_ 到 _END_ 条，共 _TOTAL_ 条记录",
            "sInfoEmpty": "第 0 到 0 条记录，共 0 条",
            "sInfoFiltered": "数据表中共为 _MAX_ 条记录",
            "sProcessing": "正在加载中...",
            "sSearch": "搜索",
            "sUrl": "", //多语言配置文件，可将oLanguage的设置放在一个txt文件中，例：Javascript/datatable/dtCH.txt
            "oPaginate": {
                "sFirst":    "首页",
                "sPrevious": " 上一页 ",
                "sNext":     " 下一页 ",
                "sLast":     " 尾页 "
            }
        }, //多语言配置
        dom: 'Bftirp',
        "bDestroy" : true,  
        "retrieve": true,//保证只有一个table实例  
        "aLengthMenu": [[15, 25, 50, -1, 0], ["每页5条", "每页25条", "每页50条", "显示所有数据", "不显示数据"]]
};

$(function(){
	//调用登录接口
	$.ajax({
			type:'post',
			url:'http://1716a0w046.imwork.net:21639/vms-guilinroad-webapp/appDataInterface/gettoken.do',
			dateType:'json',
			cache: false,
			data:{
				"param":"sijian/sijian",
			},
		  success: function(data){
			  	sessionStorage.setItem('token', data.token);
				console.log(data);
				//调用区域信息接口
				$.ajax({
					type: 'get',
					url: 'http://1716a0w046.imwork.net:21639/vms-guilinroad-webapp/appDataInterface/getzones.do',
					dateType: 'json',
					cache: false,
					data:{
						"param":sessionStorage.getItem('token'),
					},
					success: function(data) {
						console.log('获取数据成功'+"获取区域信息");
						
						var html = ""
						if(data.message == "查询区域失败"){
                            console.log(data);
						}else {
//                          for(var i = 0;i<data.zones.length;i++){
//                              html += '<tr>'+
//                                  '<td>'+data.zones[i].id+'</td>'+
//                                  '<td>'+data.zones[i].name+'</td>'+
//                                  '<td>'+data.zones[i].count+'</td>'
//
//                              if(data.zones[i].types.length>0)
//                              {
//                                  for(var j =0;j<data.zones[i].types.length;j++){
//                                      html+='<td>'+data.zones[i].types[j].name+'</td>'+
//                                          '<td>'+data.zones[i].types[j].count+'</td>';
//                                  }
//                              }
//                              else{
//                                  html+='<td>—</td>'+
//                                      '<td>—</td>';
//                              }
//
//                              html+='</tr>';
//
//                          }
//                          $("#data").append(html);
//                          $('#tab1').dataTable(datatable_options);
									console.log(data);
								    var c = document.getElementById("myCanvas");
								    var ctx = c.getContext("2d");
										var img = new Image();
										img.src="dist_vue/images/qu-bg.png";
								    img.onload = function() {
								    	ctx.drawImage(img,10,10,980,700);
								      ctx.font="30px Arial";
								    	for(var i = 0;i<data.zones.length;i++){
								    		if(data.zones[i].name=="闸口区域"){
								    			ctx.fillText(data.zones[i].count+"人",310,410);
								    		}else if(data.zones[i].name=="区域一"){
								    			ctx.fillText(data.zones[i].count+"人",465,450);
								    		}else if(data.zones[i].name=="区域二"){
								    			 ctx.fillText(data.zones[i].count+"人",670,450);
								    		}else if(data.zones[i].name=="区域三"){
								    			ctx.fillText(data.zones[i].count+"人",620,300);
								    		}
								    	}   
								    }

						}
					},
					error: function(data) {
						console.log('调用失败');				
					}
		
				});
		
		
				//调用所有人员信息接口
				$.ajax({
					type: 'get',
					url: 'http://1716a0w046.imwork.net:21639/vms-guilinroad-webapp/appDataInterface/getallpeople.do',
					dateType: 'json',
					cache: false,
					data:{
						"param":sessionStorage.getItem('token'),
						
					},
					success: function(data) {
					console.log('获取数据成功+"所有人员"');
					console.log(data);
					var str="";
					for(var i = 0;i<data.people.length;i++){
					  var id = true, name =false;
					  str +=  '<tr>'+
							'<td id="'+data.people[i].id+'" name="check">'+data.people[i].name+'</td>'+
								'<td>'+displaydealQuyu(data.people[i].zone)+'</td>'+
								'<td>'+data.people[i].type+'</td>'+
						    '<td>'+data.people[i].company+'</td>'+
						    '<td>'+displaydeal(data.people[i].entrance_time)+'</td>'+
						    '<td>'+'<a class="btn btn-info btn-xs" style="margin-left:10px;"  onclick="getpeople_imformation(this);">'+'人员追踪'+'</a>'+'</td>'+
							'</tr>'
						
						
						
					}
					$("#data2").append(str);
					$('#tab2').dataTable(datatable_options);
				},
					error: function(data) {
						console.log('调用失败');				
					}
		
				});	
		
			
		  }
	});

		
		
		
	   //获取工种列表接口
		/*$.ajax({
			type: 'get',
			url: 'http://1716a0w046.imwork.net:21639/vms-guilinroad-webapp/appDataInterface/gettypes.do',
			dateType: 'json',
			data:{
				"param":sessionStorage.getItem('token'),
			},
			
			success: function(data) {
				console.log(data);
				console.log('获取数据成功3');
				for(var i = 0;i<data.types.length;i++){
					
					var str = '<option>'+data.types[i]+'</option>';
				              
				              
					$("#word_kind").append(str);
				}
				
			},
			error: function(data) {
				console.log('调用失败');				
			}

		});*/
		
		
		
		
		
		
		//调用人员位置跟踪记录接口
	resultDataTable  = null;
	$("#search").click(function() {
		var datetimeStart = $("#inpstart").val();
		var end_tTime = $("#inpend").val();
		
		console.log(datetimeStart);
		console.log(end_tTime);

		$.ajax({
			type: 'get',
			url: 'http://1716a0w046.imwork.net:21639/vms-guilinroad-webapp/appDataInterface/getlogbytime.do',
			dateType: 'json',
			cache: false,
			data: {
				"param": sessionStorage.getItem('token')+"/"+datetimeStart+"/"+end_tTime,
			},
			success: function(data) {
				console.log(data);
				console.log('获取人员位置跟踪记录数据');
				var htmls="";
				for(var i = 0;i<data.logs.length;i++){
					 htmls+= '<tr>'+
						     /* '<td>'+data.logs[i].label_num+'</td>'+*/
						      '<td>'+displaydeal(data.logs[i].person_name)+'</td>'+
						     '<td>'+ displaydealQuyu(data.logs[i].zone)+'</td>'+
						      '<td>'+getLocalTime(data.logs[i].time)+'</td>'+
						      '<td>'+data.logs[i].type+'</td>'+
						      '</tr>'

				}
   				
   				if (resultDataTable) {
			        resultDataTable.fnClearTable();
			        resultDataTable.fnDestroy();
			    }  
			    $("#data3").html(htmls);
				resultDataTable  = $('#tabrecord').dataTable(datatable_options);
			},
			error: function(data) {
				console.log('调用失败');
			}

		});
	})
		
})

//获取人员详情接口
function getpeople_imformation(obj){

		var obj2 = $(obj).parent().siblings("td[name='check']").attr("id");
		console.log(obj2);
		$.ajax({
			type: 'get',
			url: 'http://1716a0w046.imwork.net:21639/vms-guilinroad-webapp/appDataInterface/getpersondetail.do',
			dateType: 'json',
			data:{
				"param":sessionStorage.getItem('token')+"/"+obj2,
				/*"id":obj2,*/
			},
			success: function(data) {
				console.log(data);
				console.log('获取数据成功5');
				
					sessionStorage.setItem('id',data.id);
					sessionStorage.setItem('name',data.name);
					sessionStorage.setItem('contract',data.contract==""?"无":data.contract);
					sessionStorage.setItem('type',data.type);
					sessionStorage.setItem('company',data.company);
					sessionStorage.setItem('lab_num',data.lab_num);

				if(data.logs.length>0){
					//for(var i = 0;i<data.logs.length;i++){
						
						///sessionStorage.setItem('time_second',data.logs[i].time);
						sessionStorage.setItem('list',JSON.stringify(data.logs));
						console.log(sessionStorage.getItem('list'));
						/*sessionStorage.setItem('type_second',data.logs[i].type);
						sessionStorage.setItem('name_second',data.logs[i].zone.name);
						sessionStorage.setItem('id_second',data.logs[i].zone.id);*/
					//}
				}
				if(data.logs.length==0){
					sessionStorage.setItem('list',"");
						/*sessionStorage.setItem('time_second',"—");
						sessionStorage.setItem('type_second',"—");
						sessionStorage.setItem('name_second',"—");
						sessionStorage.setItem('id_second',"—");*/
				}
				window.open("../personnel_details/");
				
					
			},
			error: function(data) {
				console.log('调用失败');				
			}

		});
	
	}	
/*没有数据即显示"-"    处理函数*/	
function displaydeal(data,id){
	id=id||false; 
	if(data ==null) 
		return "—";
	if(data.name == null)
		return data;
	if(data=="undefined")
		return "未知"
	return id==false ? data.name : data.id;	
}

/*没有数据即显示"-"    处理函数*/	
function displaydealQuyu(data){
	if(data ==null) 
		return "工地现场";
	if(data.name == null)
		return "工地现场";
	if(data=="undefined")
		return "工地现场"
	if(data.name=="")
		return "工地现场"
	return data.name;	
}

/*时间戳转换为时间 年月日时间的JS函数*/
function getLocalTime(nS) {     
   return new Date(parseInt(nS)).toLocaleString().replace(/:\d{1,2}$/,' ');     
}     



