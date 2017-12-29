var selectedGJs = [];//选择的构件与任务，危险源
var selectedText = [];//选择的构件名称
$(document).ready(function(){

	$('#guanlianyuansumajor').change(function() {
		var major = $("#guanlianyuansumajor").val();
		if(major!='0'){
			init_tree(major,'');
	}

	});
	
});

function chooseGLYS(){
	selectedGJs = [];
	selectedText = [];
	//获取关联元素类型 0 构件 1任务 分类条目
//	var yuansuType = $(".chooseGLYS li.active").index();
	var tempText = ' ';
	$(".choosegoujian option").each(function(){
		selectedGJs.push({"typetable":"构件","relatedid":$(this).val()});
		selectedText.push({"typetable":"构件","relatedText":$(this).text()});
	});
	
	$(".chooserenwu option").each(function(){
		selectedGJs.push({"typetable":"任务","relatedid":$(this).val()});
		selectedText.push({"typetable":"任务","relatedText":$(this).text()});

	});
	$(".choosekongjian option").each(function(){
		selectedGJs.push({"typetable":"空间结构","relatedid":$(this).val()});
		selectedText.push({"typetable":"空间结构","relatedText":$(this).text()});

	});
	$("#fenleixinxi_right option").each(function(){
		selectedGJs.push({"typetable":"分类信息","relatedid":$(this).val()}); 
		selectedText.push({"typetable":"分类信息","relatedText":$(this).text()});
	});
	$('#guanlianyuansu').modal('hide');
	for( i = 0;i < selectedText.length; i++){
			tempText += '<p style="border-bottom:1px solid #ccc;padding-bottom: 10px;">'+selectedText[i].typetable+' : '+selectedText[i].relatedText+'</p>';
	}
	$('#selectText').html( tempText );
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
	    $(".goujianselect option").remove();
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
	$('#jstree_renwu').bind("select_node.jstree", function (obj, e) {
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
				url:"/task/goujian/glrw",
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

	    var node = e.node;
	    
	    if(node.id=="rootelevationtree"){
	    	return;
	    }
	    
	    var isselect = node.state.selected;//选中还是取消

		if (isselect){
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
$("#jstree_fenleixinxi").jstree("destroy");
	$("#jstree_fenleixinxi").jstree({
	   		"core": {
	   			'data': {
	   				'url': '/task/modelview/getpbtypetree/'+urlend,
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
	$('#jstree_fenleixinxi').bind("activate_node.jstree", function (obj, e) {

	    var node = e.node;//
	    if(node.id=="pbtypetree"){
	    	return;
	    }
	    
	    var isselect = node.state.selected;//选中还是取消

		if (isselect){
			var option = "<option "+ "class='"+ node.id +"' value='"+ node.id  +"'>"+node.text+"</option>";
			
			$("#fenleixinxi_right").append(option);
	
		}
		else{
			$("."+node.id).remove();
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
	else if(ty=='rw'){
		moveOption( $('.renwuselect'),$('.chooserenwu'))
	}
	else if(ty=='pbgrp'){
		moveOption( $('#pbgrp_left'),$('#pbgrp_right'))
	}

}
function moveleft(ty){
	if(ty=='gj'){
		moveOption($('.choosegoujian'), $('.goujianselect'))
	}
	else if(ty=='rw'){
		moveOption($('.chooserenwu'), $('.renwuselect'))
	}
	else if(ty=='pbgrp'){
		moveOption( $('#pbgrp_right'),$('#pbgrp_left'))
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

