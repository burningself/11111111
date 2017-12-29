var selTasks=[];

$(document).ready(function(){

	  $('#guanlianyuansumajor').change(function() {
		var major = $("#guanlianyuansumajor").val();
		if(major!='0'){
			init_tree(major);
		}

    });
	
	

	
	$("#btnSelectTask").click(function(){
		  selTasks = [];
		  var desc = "";
		  var selNodes = getCurrentTreeSelectedObjs();
  		  $.each(selNodes, function(num, treeNode) {
  		  	if(treeNode.id!="#"){
  		  		selTasks.push(treeNode.id);
  				desc+=treeNode.text+"\r\n";
  		  	}
  		});
  		
  		$("#goaldescribe").val(desc);
	});
	
});
	
function init_tree(major){
	var urlend='';
	if(major){
		urlend = "?major="+major;
	}
	
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
	   		"plugins": ["themes", "json_data","checkbox"],
	 		"checkbox": {
	 			"three_state": false
	 		}
	});

	
}

  function getCurrentTreeSelectedObjs() {
  	var tree = $.jstree.reference("#jstree_renwu"); //get tree instance
  	var selNodes = tree.get_selected(true);

  	return selNodes;
  }

function FunGuanLianYuanSu() {

	$('#guanlianyuansu').modal('show');
};

