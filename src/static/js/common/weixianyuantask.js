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
		newRow += "<td ><a href='#' onclick='ChooseTask(this)' val='model'>选择任务</a></td>";
		newRow += "<td><a href='#' onclick='ChooseKJ(this)' val='model'>选择空间</a></td>";
		newRow += "<td><a href='#' onclick='ChooseFangan(this)' val='model'>选择方案</a></td>";
		newRow += "<td>"
//		newRow += '<a href="#" onclick="saveonetr(this)"  style="cursor: pointer;">[保存]</a>'
		newRow += '<a href="#" onclick="delerow(this)" title="" style="cursor: pointer;">[删除]</a>'
		newRow += "</td>";
		newRow += "</tr>";
		$("#task_hazard_table").append(newRow);

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
//任务


	$("#jstree_renwu").jstree({
	   		"core": {
	   			'data': {
	   				'url': '/task/modelview/renwutree/',
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
	$('#jstree_renwu').bind("activate_node.jstree", function (obj, e) {
	    // 处理代码
	    // 获取当前节点
	    var node = e.node;//
	    
	    var isselect = node.state.selected;//选中还是取消
//	    var parents = node.parents;//父节点是否是unitprj
	//	    node.parents ["unitprj_1", "model", "#"]
		if (isselect){
//			var sdate = {"id":node.id,"parents":JSON.stringify(node.parents)};
			var tree = $.jstree.reference("#jstree_kongjian"); 

			var option = "<option nodep='"+ node.parents+ "' class='"+ node.id +"' value='"+ node.id +"'>"+ node.text+"</option>";
			
			$(".chooserenwu").append(option);
	
		}
		else{
			$("."+node.id).remove();
		}
	});






}


function qingkong(obj){
	$("#task_hazard_table tr").slice(1).remove()
}

function delerow(obj) {
	$(obj).parent().parent().remove();
}

function deleall(){
	$.ajax({
		type:"post",
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
			if(e.status==403){
				alert("您没有权限编辑危险源，请联系管理员！");
				res = false;
			}
		}
	});
}

var isok=0;

function saveall(){
	isok = $("#task_hazard_table tr").length-1;

	$("#task_hazard_table tr").each(function(i){
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
		return false;
	}
	var renwu = $(tdlist[2].children[0]).attr('val')
	if(renwu=='model'){
		alert('任务不允许为空');
		return false;
	}
	var fangan = $(tdlist[4].children[0]).attr('val')

	var pdata={};

	
	pdata.hardid = hardid
	pdata.opt='create';
	
	pdata.kj = kongjian;//空间
	pdata.renwu = renwu;//任务
	pdata.fangan = fangan;//方案

//	var jsonString = JSON.stringify();
	var res = false;
	$.ajax({
		type:"post",
//		async:true,
		dataType: "json",
		data: pdata,
		success:function(data){
			if(data.res=='succ'){
				isok -=1;
				if(isok==0){
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

var tasktd;
function ChooseTask(obj){
	tasktd = obj;
	var ref = $('#jstree_renwu').jstree(true);
	ref.uncheck_all();
	$(".chooserenwu option").remove();
	$('#guanlianrenwu').modal('show');
}

function chooseTaskfromTree(){
	var number=1;
	$(".chooserenwu option").each(function(){
		var tk = this;
		var hardid = $(tasktd).parent().parent().attr('class').split('_')[1]
		var task = tk.className
		if(isrepeat('',hardid,task))
		{
			alert('存在重复，已经忽略！');
		}
		else{
			if(number>1){
				var newRow =  $(tasktd).parent().parent().clone();
//				newRow.appendTo("#task_hazard_table");
				$(tasktd).parent().parent().after(newRow);
				kjtd = newRow.children()[3].children[0];
			}
				
			$(tasktd).html(tk.innerHTML);
			$(tasktd).attr('val',tk.className);
			number += 1;
		}
		
		
	});
	
	$('#guanlianrenwu').modal('hide');
}

function ChooseFangan(obj){
	tasktd = obj;
	$('#fangandlg').modal('show');
}

$(document).ready(function(){

	$("#btnSelectFangAn").click(function(){
		
		$(tasktd).html($('#fanganSel option:selected').text());
		$(tasktd).attr('val',$('#fanganSel option:selected').val());	
		$('#fangandlg').modal('hide');
		
	});
});

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
		if(isrepeat(kongjian,hardid,''))
		{
			alert('存在重复，已经忽略！');
		}
		else{
			if(number>1){
				var newRow =  $(kjtd).parent().parent().clone();
				$(kjtd).parent().parent().after(newRow);
//				newRow.appendTo("#task_hazard_table");
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
// 空间 危险源 任务 都不重复
function isrepeat(k,h,t){
	var res=false;
	if(k){
		$("#task_hazard_table tr").each(function(i){
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
	}
	else if(t){
		$("#task_hazard_table tr").each(function(i){
			var tr = $(this);
			if(i==0||tr.index()==$(kjtd).parent().parent().index()){
				return true;
			}
			
			var tdlist = tr.children();
			var hardid = tr.attr('class').split('_')[1]
			var task = $(tdlist[2].children[0]).attr('val')
			if (t==task && h==hardid){
				res = true;
				return false;//跳出each 循环
			}
		});
	}

	return res;
}
