var selectedGJs = [];//选择的构件与任务，危险源
var selectedKJ;//选择的空间结构

function chooseGLYS(){
	selectedGJs = [];
	var yixuanyuansu = 0;
	//获取关联元素类型 0 构件 1任务 分类条目
//	var yuansuType = $(".chooseGLYS li.active").index();
	$(".choosegoujian option").each(function(){
		selectedGJs.push({"typetable":"构件","relatedid":$(this).val()});
		yixuanyuansu += 1;
	});
	
	$(".chooserenwu option").each(function(){
		selectedGJs.push({"typetable":"任务","relatedid":$(this).val()});
		yixuanyuansu += 1;
	});
	$("#sheshi_right option").each(function(){
		selectedGJs.push({"typetable":"构件","relatedid":$(this).val()});
		yixuanyuansu += 1;
	});
	$(".choosekongjian option").each(function(){
		selectedKJ = $(this).val();
		yixuanyuansu += 1;
	});
	$("#weixianyuan_right option").each(function(){
		selectedGJs.push({"typetable":"危险源","relatedid":$(this).val()}); //危险源id
		yixuanyuansu += 1;
	});
	$('#guanlianyuansu').modal('hide');
	$("#yixuanyuansu").text("已选"+yixuanyuansu+"个关联元素");
}


function init_tree(major,liuchengid){
	var urlend='';
	if(major){
		urlend = "?major="+major;
	}else if(liuchengid){
		urlend = "?liuchengid="+liuchengid;
	}
	
	
	$("#jstree_goujian").jstree("destroy");
	$("#jstree_goujian").jstree({
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
	   		"plugins": ["themes", "json_data"],
	// 		"checkbox": {
	// 			"three_state": false
	// 		}
	});
	$('#jstree_goujian').bind("select_node.jstree", function (obj, e) {
	    // 处理代码
	    // 获取当前节点
	    var node = e.node;//
	    var isselect = node.state.selected;//选中还是取消
	    var parents = node.parents;//父节点是否是unitprj
	    $(".goujianselect option").remove()
	//	    node.parents ["unitprj_1", "model", "#"]
		if (isselect){
			var major = $("#guanlianyuansumajor").val();
			var sdate = {"id":node.id,"parents":JSON.stringify(node.parents),"major":major};
			$.ajax({
				type:"get",
				url:"/task/goujian/glys",
				dataType:"json",
				async:false,
				data:sdate,
				success: function(data){
					
					for(var i=0;i<data.goujians.length;i++)
					{
						var option = "<option "+ "class='"+data.goujians[i].class+"'" +" value='"+ data.goujians[i].id  +"'>"+data.goujians[i].sign+"</option>";
						$(".goujianselect").append(option);
					}
				}
			});
	
		}
//		else{
//			$("."+node.id).remove()
//		}
	});

	$("#jstree_renwu").jstree("destroy");
	$("#jstree_renwu").jstree({
	   		"core": {
	   			'data': {
	   				'url': '/task/modelview/renwutree/'+urlend,
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
	$('#jstree_renwu').bind("activate_node.jstree", function (obj, e) {
	    // 处理代码
	    // 获取当前节点
	    var node = e.node;//
	    var isselect = node.state.selected;//选中还是取消
	    var parents = node.parents;//父节点是否是unitprj
	//	    node.parents ["unitprj_1", "model", "#"]
		$(".renwuselect option").remove()
		if (isselect){
			var sdate = {"id":node.id,"parents":JSON.stringify(node.parents)};
			$.ajax({
				type:"get",
				url:"/task/goujian/glrw/",
				dataType:"json",
				async:false,
				data:sdate,
				success: function(data){
					for(var i=0;i<data.renwu.length;i++)
					{
						var option = "<option value='"+ data.renwu[i].id  +"'>"+data.renwu[i].name+"</option>";
						$(".renwuselect").append(option);
					}
				}
			});
	
		}
//		else{
//			$("."+node.id).remove()
//		}
	});
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
			var ref = $('#jstree_kongjian').jstree(true);
		    ref.uncheck_all();
		    $(".choosekongjian option").remove();
		    ref.check_node(node);
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
	$("#jstree_weixianyuan").jstree("destroy");
	$("#jstree_weixianyuan").jstree({
	   		"core": {
	   			'data': {
	   				'url': '/task/modelview/gethazardeventtree/'+urlend,
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
	$('#jstree_weixianyuan').bind("activate_node.jstree", function (obj, e) {
	    // 处理代码
	    // 获取当前节点
	    var node = e.node;//
	    
	    var isselect = node.state.selected;//选中还是取消
//	    var parents = node.parents;//父节点是否是unitprj
	//	    node.parents ["unitprj_1", "model", "#"]
		if (isselect){
			var ref = $('#jstree_weixianyuan').jstree(true);
//		    ref.uncheck_all();
//		    $("#weixianyuan_right option").remove();
		    ref.check_node(node);
//			var sdate = {"id":node.id,"parents":JSON.stringify(node.parents)};
			var option = "<option "+ "class='"+ node.id +"' value='"+ node.id  +"'>"+node.text+"</option>";
			
			$("#weixianyuan_right").append(option);
	
		}
		else{
			$("."+node.id).remove();
		}
	});
	$("#jstree_anquanwenmingsheshi").jstree("destroy");
	$("#jstree_anquanwenmingsheshi").jstree({
	   		"core": {
	   			'data': {
	   				'url': '/task/modelview/getpbtypetree/?major='+17,
	   				'data': function(node) {
	   					return {
	   						'id': node.id
	   					};
	   				}
	   			}
	   		},
	   		'multiple':false,
	   		"plugins": ["themes", "json_data"],
//	 		"checkbox": {
//	 			"three_state": false
//	 		}
	});

	$('#jstree_anquanwenmingsheshi').bind("select_node.jstree", function (evt, data) {
		
		if(data.node.id != "#" && data.node.id!="pbtypetree"&& data.node.id.indexOf("major_")==-1) {
			var sdate = {"id":data.node.id};
			$.ajax({
				type:"get",
				url:"/task/goujian/glys_pbtype",
				dataType:"json",
				async:false,
				data:sdate,
				success: function(data){	
					for(var i=0;i<data.glys.length;i++)
					{
						var option = "<option  value='"+ data.glys[i].id  +"'>"+data.glys[i].name+"</option>";
						$("#sheshi_left").append(option);
					}
				}
			});
	    }
	});


}

function moveOption(obj1, obj2)
{
	var isHave = false;
	obj2.find("option").each(function(){
		console.log($(this).html());
		if($(this).html()==obj1.find("option:selected").html()){
			isHave = true; 
			return;
		}
	});
	
	if(!isHave){
		obj2.append(obj1.find("option:selected"));
		obj1.find("option:selected").remove();
	}
}
function moveright(ty){
	if(ty=='gj'){
		moveOption( $('.goujianselect'),$('.choosegoujian'))
	}
	else if(ty=='pbgrp'){
		moveOption( $('#pbgrp_left'),$('#pbgrp_right'))
	}
	else if(ty=='rw'){
		moveOption( $('.renwuselect'),$('.chooserenwu'))
	}
	else if(ty=='wxy'){
		moveOption( $('#weixianyuan_left'),$('#weixianyuan_right'))
	}
	else if(ty=='ss'){
		moveOption( $('#sheshi_left'),$('#sheshi_right'))
	}
}
function moveleft(ty){
	if(ty=='gj'){
		moveOption($('.choosegoujian'), $('.goujianselect'))
	}
	else if(ty=='pbgrp'){
		moveOption( $('#pbgrp_right'),$('#pbgrp_left'))
	}
	else if(ty=='rw'){
		moveOption($('.chooserenwu'), $('.renwuselect'))
	}
	else if(ty=='kj'){
		moveOption( $('.choosekongjian'),$('.kongjianselect'))
	}
	else if(ty=='wxy'){
		moveOption( $('#weixianyuan_right'),$('#weixianyuan_left'))
	}
	else if(ty=='ss'){
		moveOption( $('#sheshi_right'),$('#sheshi_left'))
	}
	
}



function FunGuanLianYuanSu() {

	$('#guanlianyuansu').modal('show');
};

function guolvgj(){
	var guolvtj =  $("#guolvgj").val();
	$(".goujianselect option").each(function(){
		var txt = $(this).html();
		if(txt.indexOf(guolvtj)==-1){
			$(this).remove();
		}
	});

}
function guolvrw(){
	var guolvtj =  $("#guolvrw").val();
	$(".goujianselect option").each(function(){
		var txt = $(this).html();
		if(txt.indexOf(guolvtj)==-1){
			$(this).remove();
		}
	});
	$(".renwuselect option").each(function(){
		var txt = $(this).html();
		if(txt.indexOf(guolvtj)==-1){
			$(this).remove();
		}
	});

}

$(document).ready(function() {

	$('#guanlianyuansumajor').change(function() {
		var major = $("#guanlianyuansumajor").val();
		if(major!='0'){
			init_tree(major,'');
		}

	});
});