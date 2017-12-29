var selectedGJs=[];
var selectedDesc=[];
var gjType = "";
var inputId="";
var DescId="relateYuanSu";
var NeedClearOther = false;


var selCfg = {
disableIfEmpty: true,
buttonWidth:'100%',
nonSelectedText : '请选择元素', 
nSelectedText: ' - 元素',
allSelectedText: '全选',
maxHeight : 445,   
numberDisplayed : 3,
enableFiltering: true,
includeSelectAllOption: true,
selectAllText: '全选',
onInitialized: function(select, container) {
        $(".multiselect").click();
   }
};

$(document).ready(function(){

	if(navigator.userAgent.match(/(iPhone|iPod|Android|ios)/i)){
		selCfg.maxHeight=350;
	}

	   $('#choosepbgrp').multiselect(selCfg);
	   $('#choosesheshi').multiselect(selCfg);
	   $('#chooseshigongjixie').multiselect(selCfg);
	   $('#choosegoujian').multiselect(selCfg);
	   $('#chooserenwu').multiselect(selCfg);
	   
	  $('#guanlianyuansumajor').change(function() {
		var major = $("#guanlianyuansumajor").val();
		if(major!='0'){
			init_tree(major,'');
		}

	});
	
});
	   

	
function chooseGLYS(){
	$("#"+inputId).val("");
	$("#"+DescId).val("");
	selectedGJs = [];
	selectedDesc = [];
	
	while (true){
		
		$(".choosegoujian option:selected").each(function(){
			selectedGJs.push({"typetable":"构件","relatedid":$(this).val()});
			selectedDesc.push($(this).text());
		});

		
		$("#choosekongjian option").each(function(){
			selectedGJs.push({"typetable":"空间","relatedid":$(this).val()});
			selectedDesc.push($(this).text());
	    });
	    
		
		$(".choosesheshi option:selected").each(function(){
			selectedGJs.push({"typetable":"构件","relatedid":$(this).val()});
			selectedDesc.push($(this).text());
		});

		
		$(".chooseshigongjixie option:selected").each(function(){
			selectedGJs.push({"typetable":"施工机械","relatedid":$(this).val()});
			selectedDesc.push($(this).text());
		});


		$(".chooserenwu option:selected").each(function(){
			selectedGJs.push({"typetable":"任务","relatedid":$(this).val()});
			selectedDesc.push($(this).text());
		});

		break;
	}

	$("#"+DescId).val(selectedDesc);
	$("#"+inputId).val(JSON.stringify(selectedGJs)).change();

	$('#guanlianyuansu').modal('hide');
}



function clearAllselect()
{
	if(NeedClearOther){
		$("#choosegoujian").empty();
		$("#choosegoujian").multiselect("destroy");
		
		$("#choosesheshi").empty();
		$("#choosesheshi").multiselect("destroy");
		
		$("#chooseshigongjixie").empty();
		$("#chooseshigongjixie").multiselect("destroy");
		
		$("#chooserenwu").empty();
		$("#chooserenwu").multiselect("destroy");
		
		$("#choosekongjian").empty();
	}

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
	
	$('#jstree_goujian').bind("select_node.jstree", function (evt, evtdata) {
		clearAllselect();
		
		
	    // 处理代码
	    if(evtdata.node.id != "#" && evtdata.node.id!="rootelevationtree") {
	    	var parents = evtdata.node.parents;//父节点是否是unitprj
	    	var major = $("#guanlianyuansumajor").val();
			var sdate = {"id":evtdata.node.id,"parents":JSON.stringify(parents),"major":major};
			$.ajax({
				type:"get",
				url:"/task/goujian/glys",
				dataType:"json",
				async:true,
				data:sdate,
				success: function(data){	
					for(var i=0;i<data.goujians.length;i++)
					{
						var option = "<option  value='"+ data.goujians[i].id  +"'>"+data.goujians[i].sign+"</option>";
						$(".choosegoujian").append(option);
					}
					$("#choosegoujian").multiselect("destroy").multiselect(selCfg);  
				}
			});
	    }

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
	    // 获取当前节点
	    var node = e.node;//
	    var isselect = node.state.selected;//选中还是取消
		if(node.id=="rootelevationtree"){
			return;
		}
		
		if (isselect){
			if($("#choosekongjian option").size()==0){
				clearAllselect();
			}
			
			var tree = $.jstree.reference("#jstree_kongjian"); 
			var patext='';
			if(node.parents.length==3){
				var pa = node.parents[0]
				patext = tree.get_node(pa).text;
			}
			var option = "<option class='"+ node.id +"' value='"+ node.id +"' selected>"+ patext+node.text+"</option>";
			
			$("#choosekongjian").append(option);
	
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
		clearAllselect();
		
	    // 处理代码
	    if(data.node.id != "#" && data.node.id!="pbtypetree"&& data.node.id.indexOf("major_")==-1) {
			var sdate = {"id":data.node.id};
			$.ajax({
				type:"get",
				url:"/task/goujian/glys_pbtype",
				dataType:"json",
				async:true,
				data:sdate,
				success: function(data){	
					for(var i=0;i<data.glys.length;i++)
					{
						var option = "<option  value='"+ data.glys[i].id  +"'>"+data.glys[i].name+"</option>";
						$(".choosesheshi").append(option);
					}
					$("#choosesheshi").multiselect("destroy").multiselect(selCfg);  
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
	    clearAllselect();
	    
	    var node = e.node;//
	    var parents = node.parents;//父节点是否是unitprj

		var sdate = {"id":node.id,"parents":JSON.stringify(node.parents)};
		$.ajax({
				type:"get",
				url:"/task/goujian/glrw",
				dataType:"json",
				async:true,
				data:sdate,
				success: function(data){
					for(var i=0;i<data.renwu.length;i++)
					{
						var option = "<option value='"+ data.renwu[i].id  +"'>"+data.renwu[i].name+"</option>";
						$(".chooserenwu").append(option);
					}
					$("#chooserenwu").multiselect("destroy").multiselect(selCfg);  
				}
		});


	});


}




function FunGuanLianYuanSu(RelatedId,DescId,NeedClearOtherIn) {
	inputId = RelatedId;
	DescId = DescId;
	NeedClearOther=NeedClearOtherIn||false; 

	
	$('#guanlianyuansu').modal('show');
};
