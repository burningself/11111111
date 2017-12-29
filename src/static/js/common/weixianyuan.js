function intweixianyuan() {
	$("#jstree_div_hazard").jstree({
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
		"plugins": ["themes", "json_data"],
		"checkbox": {
			"three_state": false
		}
	});

	// event for when a node in the tree is selected
	$("#jstree_div_hazard").bind("activate_node.jstree", function(obj, e) {
		var node = e.node;
		if(node.parents.length < 3)
			return;
		var isselect = node.state.selected;
		if(!isselect) {
			$(".weixianku_" + node.id).remove();
			return;
		}

		var tree = $.jstree.reference("#jstree_div_hazard"); 
		var pa = node.parents[node.parents.length - 3]
		ji = tree.get_node(pa).text;


		var newRow = "<tr class='weixianku_" + node.id + "'>"
		newRow += "<td style='width:80px;'>" + ji + "</td>";//等级
		newRow += "<td>" + node.text + "</td>";//内容
		newRow += "<td ><div title='点击输入持续天数' contentEditable='true'>&nbsp;</div></td>";
		newRow += "<td><a href='#' onclick='ChooseKJ(this,"+node.data.majorid+")' val='model'>选择空间</a></td>";
		newRow += "<td>" + node.data.major + "</td>"; //专业
		newRow += "<td>" + $('#selectshoukong').html() + "</td>"; //是否受控
		newRow += "<td ><div title='点击输入危险源备注' contentEditable='true'>&nbsp;</div></td>";
		newRow += "<td>"
//		newRow += '<a href="#" onclick="saveonetr(this)"  style="cursor: pointer;">[保存]</a>'
		newRow += '<a href="#" onclick="delerow(this)" title="" style="cursor: pointer;">[删除]</a>'
		newRow += "</td>";
		newRow += "</tr>";
		$("#today_hazard_table").append(newRow);

	});

}

function init_tree(major){
	var urlend='';
	if(major){
		urlend = "?major="+major;
	}
	
	$("#jstree_kongjian").jstree("destroy");
	$("#jstree_kongjian").jstree({
	   		"core": {
	   			'data': {
	   				'url': '/task/modelview/getelevationtree/'+urlend,
	   				'data': function(node) {
	   					return {
	   						'id': node.id
	   					};
	   				}
	   			}
	   		},
	   		'multiple':false,
	   		"plugins": ["themes", "json_data","checkbox"],
	 		"checkbox": {
	 			"three_state": false
	 		}
	});
	$('#jstree_kongjian').bind("activate_node.jstree", function (obj, e) {
	    // 处理代码
	    // 获取当前节点
	    var node = e.node;//
	    
	    var isselect = node.state.selected;//选中还是取消
//	    var parents = node.parents;//父节点是否是unitprj
	//	    node.parents ["unitprj_1", "model", "#"]
		if (isselect){
//			var sdate = {"id":node.id,"parents":JSON.stringify(node.parents)};
			var tree = $.jstree.reference("#jstree_kongjian"); 
			var patext='';
			if(node.parents.length==3){
				var pa = node.parents[0]
				patext = tree.get_node(pa).text;
			}
			var option = "<option nodep='"+ node.parents+ "' class='"+ node.id +"' value='"+ node.id +"'>"+ patext+node.text+"</option>";
			
			$(".choosekongjian").append(option);
	
		}
		else{
			$("."+node.id).remove();
		}
	});
}


function tongjiClosedHazard(){
	$.ajax({
		type:"post",
		url:"/task/anquan/hazard/",
		dataType:"json",
		async:true,
		data: {"opt":"tongjiClosedHazard"},
		success:function(data){
			if(data.res=='succ'){
				for(var i=0;i<data.data.length;i++)
				{
					var tmp  = "<tr>"
						tmp += "<td>"+data.data[i].hazard+"</td>"
						tmp += "<td>"+data.data[i].closedate+"</td>"
						tmp += "<td>"+data.data[i].受控+"</td>"
						tmp += "<td>"+data.data[i].不受控+"</td>"
						tmp += "</tr>"

					$("#tongjiClosed").append(tmp);
				}
				
			}
		},
		error: function(e){
			alert(e)
		}
	});
}

function qingkong(obj){
	$("#today_hazard_table tr").slice(1).remove()
}

function delerow(obj) {
	if(!confirm("删除不可恢复，确认么？")){
		return;
	}
	id = $(obj).parent().parent().attr('id')
	$.ajax({
		type:"post",
		url:"/task/anquan/hazard/",
		cache: false,
		dataType:"json",
		async:false,
		data: {"opt":"delone",'id':id},
		success:function(data){
			if(data.res=='succ'){
				alert("删除成功");
				$(obj).parent().parent().remove();
			}
		},
		error: function(e){
			if(e.status==403){
				alert("您没有权限删除危险源，请联系管理员！");
			}
		}
	});
}

function deleall(){
	$.ajax({
		type:"post",
		url:"/task/anquan/hazard/",
		cache: false,
		dataType:"json",
		async:false,
		data: {"opt":"del"},
		success:function(data){
			if(data.res=='succ'){
				saveall();
			}
		},
		error: function(e){
			alert(e)
		}
	});
}

var isok=0;
var weiyi=[];
function saveall(){
	isok = $("#today_hazard_table tr").length-1;
	weiyi=[];
	$("#today_hazard_table tr").each(function(i){
		if(i==0){
			return true;
		}
		
		if(!saveonetr(this)){
			return false;
		}
	});
	
	
}

function saveonetr(obj){
	var tr = $(obj);
	var tdlist = tr.children();
	var hardid = tr.attr('class').split('_')[1]
	var kongjian = $(tdlist[3].children[0]).attr('val')
	if(kongjian=='model'){
		alert('空间不允许为空');
		return;
	}
	var id = tr.attr('id');
	
	var pdata={};
	if(id){
		pdata.id = id
	}
	var str = tdlist[2].innerText.trim();//天数
	var n = Number(str);
	if (isNaN(n))
	{
	    alert("持续天数必须是数字");
	    return false
	}
	if (n<0)
	{
	    n=0;
	}
	if (n>500)
	{
	    alert("持续天数必须小于500");
	    return false
	}

	pdata.days = n;//天数
	if(weiyi.indexOf(kongjian+hardid)!=-1){
		isok -=1;
		if(isok==0){
			window.location.reload();
		}
	    return true;
	}
	weiyi.push(kongjian+hardid);
	
	pdata.hardid = hardid
	pdata.opt='create';
	
	pdata.kj = kongjian;//空间
//	pdata.majorid = tdlist[4].children[0].value;//专业
	pdata.isctr = tdlist[5].children[0].value;//受控
	pdata.describ = tdlist[6].innerText;//描述
	if (pdata.describ.length>256)
	{
	    alert("备注最多256个字");
	    return false
	}
	
	
//	var jsonString = JSON.stringify();
	var res = false;
	$.ajax({
		type:"post",
		url:"/task/anquan/hazard/",
//		async:true,
		dataType: "json",
		data: pdata,
		success:function(data){
			if(data.res=='succ'){
				
				//不受控发起安全问题
				if(data.rid!=0){
					isunctr = tdlist[5].children[0][tdlist[5].children[0].options.selectedIndex].text
					if(isunctr=="不受控"){
						 if(confirm(tdlist[1].innerText+":不受控，是否自动发起安全问题？"))
						 {
						 	var issuedata={};
						 	issuedata.issuetype="anquan";
						 	issuedata.autotype="weixianyuan";
						 	issuedata.autotypeId=data.rid;
						 	 $.ajax({
								type:"post",
								url:"/task/issue/createauto/",
								async:false,
								dataType: "json",
								data: issuedata,
								success:function(data){
									if(data.issuc=='true'){
										
									}
									else{
										alert(data.error);
									}
								}
							});
						 }
					}
				}

				isok -=1;
				if(isok==0){
					alert("保存成功！");
					window.location.reload();
				}
			}
			else{
				res = false;
			}
		},
		error: function(e){
			if(e.status==403){
				alert("您没有权限编辑危险源，请联系管理员！");
				res = false;
			}
		}
	});
	return res;
}

var kjtd;

function ChooseKJ(obj,major) {
	if(major!=0){
		console.log(major)
		$("#guanlianyuansumajor").val(major);
		$("#guanlianyuansumajor").change();
	}
	
	kjtd = obj;
	var ref = $('#jstree_kongjian').jstree(true);
	ref.uncheck_all();
	$(".choosekongjian option").remove();
	$('#guanlianyuansu').modal('show');
}

function chooseKJfromTree() {
//	var kj = $(".choosekongjian option")[0];
//	if(!kj){
//		$('#guanlianyuansu').modal('hide');
//		return;
//	}
	
	var number=1;
	$(".choosekongjian option").each(function(){
		var kj = this;
		
		var hardid =  $(kjtd).parent().parent().attr('class').split('_')[1]
		var kongjian = kj.className
		if(isrepeat(kongjian,hardid))
		{
			alert('存在重复危险源，已经忽略！');
		}
		else{
			if(number>1){
				var newRow =  $(kjtd).parent().parent().clone();
				newRow.appendTo("#today_hazard_table");
				kjtd = newRow.children()[3].children[0];
			}
				
			$(kjtd).html(kj.innerHTML);
			$(kjtd).attr('val',kj.className);
			number += 1;
		}
		
		
	});
	
	$('#guanlianyuansu').modal('hide');

}

//false 不重复，true 重复
function isrepeat(k,h){
	var res=false;
	$("#today_hazard_table tr").each(function(i){
		var tr = $(this);
		if(i==0||tr.index()==$(kjtd).parent().parent().index()){
			return true;
		}
		
		var tdlist = tr.children();
		var hardid = tr.attr('class').split('_')[1]
		var kongjian = $(tdlist[3].children[0]).attr('val')
		if (k==kongjian && h==hardid){
			res = true;
			return false;//跳出each 循环
		}
	});
	return res;
}
