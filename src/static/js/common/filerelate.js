$("#filetree_div").jstree({
	"core": {
		'data': {
			'url': 'task/ziliao/getfiletree/',
			'data': function(node) {
				return {
					'id': node.id
				};
			}
		}
	},
	"plugins": ["themes", "json_data", "checkbox"],
});

function getFileTreeSelectedObjs() {
	var tree = $.jstree.reference("#filetree_div"); //get tree instance
	var selNodes = tree.get_selected(true);

	return selNodes;
}

function FunCommonRelateFile() {
	
	var selNodes = getFileTreeSelectedObjs();
	
	$.each(selNodes, function(num, treeNode) {
		
		if(treeNode.id!="#") {
			var type =  treeNode.id.split('_')[0];
			console.debug(type);
			if(treeNode.id!="dir") {
				var newRow = "<tr> \
								<td>"+treeNode.text+"</td> \
								<td ><a href='#' title='删除文件' onclick='funDelFileRelate(this)' style='cursor: pointer;'>[删除]</a></td> \
				       		 </tr>";
				$("#file_relate_table tr:last").after(newRow);
			}
		}
	});
	
	//todo 发送ajax请求到服务器,保存构件和文件的关联 pangubing
	
	var tree = $.jstree.reference("#filetree_div"); //get tree instance
	tree.deselect_all();
	 
	$('#relatefiledlg').modal("hide");
}

function funDelFileRelate(obj)
{
	$(obj).parents("tr").remove();
}
