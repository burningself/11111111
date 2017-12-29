  function getSelectElevations() {
  	url = window.location.href;
  	var valueSelElevations = localStorage.getItem(url + "-unitprjtreeSelElevations" + _curUnitId);
  	if(valueSelElevations) {
  		//_selElevations = valueSelElevations;
  		console.log(valueSelElevations + '_selElevations datas are restored');

  		var Elevations = valueSelElevations.substr(0, valueSelElevations.length - 1).split(",");
  		for(var each in Elevations) {
  			$('#jstree_div').jstree('select_node', Elevations[each]);
  		}
  	}

  }
  
    	function saveSelectElevations() {
  		url = window.location.href;
  		localStorage.setItem(url + "-unitprjtreeSelElevations" + _curUnitId, _selElevations);
  	}

  function deSelectElevations(unitId) {
  	url = window.location.href;
  	var valueSelElevations = localStorage.getItem(url + "-unitprjtreeSelElevations" + unitId);
  	if(valueSelElevations) {
  		//_selElevations = valueSelElevations;
  		console.log(valueSelElevations + '_selElevations datas are restored');

  		var Elevations = valueSelElevations.substr(0, valueSelElevations.length - 1).split(",");
  		for(var each in Elevations) {
  			$('#jstree_div').jstree('deselect_node', Elevations[each]);
  		}
  	}

  }

  function saveSelectPbTypes() {
  	url = window.location.href;
  	localStorage.setItem(url + "-pbtypetreeSelPbtypes", _selPbtypes);
  }

  function getSelectPbTypes() {
  	url = window.location.href;

  	var valueSelPbtypes = localStorage.getItem(url + "-pbtypetreeSelPbtypes");
  	if(valueSelPbtypes) {
  		_selPbtypes = valueSelPbtypes;
  		console.log(_selPbtypes + '_selPbtypes datas are restored');

  		var PbTypes = _selPbtypes.substr(0, _selPbtypes.length - 1).split(",");
  		for(var each in PbTypes) {
  			$('#jstree_div_pbtype').jstree('select_node', PbTypes[each]);
  		}
  	}
  }

  function initJsTree() {
  	// initialize the tree
  	$("#jstree_div").jstree({
  		"core": {
  			'data': {
  				'url': '/task/modelview/getelevationtree/?major=' + _curMajor,
  				'data': function(node) {
  					return {
  						'id': node.id
  					};
  				}
  			}
  		},
  		"plugins": ["themes", "json_data", "checkbox"],
  		"checkbox": {
  			"three_state": false
  		}
  	});
  	
  	
  	 	$("#jstree_div").on("ready.jstree", function() {
  		$('#jstree_div').jstree('select_node', "unitprj_" + _curUnitId);
  	});

  		// event for when a node in the tree is selected
  	$("#jstree_div").on("select_node.jstree", function(evt, data) {
  		//console.debug(data.node.data);
  		if(data.id != "#" && data.id != "model") {
  			var bChangeModel = false;
  			var modelfile;
  			var curSelUnitId;
  			var selectedModel = 0;

  			var nodetype = data.node.id.split('_')[0];
  			if(nodetype == "unitprj") {
  				if(data.node.data.unitid == _curUnitId) {
  					return;
  				}

  				var selNodes = getCurrentTreeSelectedObjs();
  				var lastUnitId = _curUnitId;
  				$.each(selNodes, function(num, treeNode) {
  					if(treeNode.data) {
  						if(treeNode.data.unitid == lastUnitId) {
  							$('#jstree_div').jstree('deselect_node', treeNode.id);
  							//deSelectElevations(treeNode.data.unitid);
  							$('#jstree_div').jstree('close_node', treeNode.id);
  						}
  					}
  				});

  				//取消选择的楼层
  				if(_selElevations.length > 1) {
  					var PbElevations = _selElevations.substr(0, _selElevations.length - 1).split(",");
  					for(var each in PbElevations) {
  						$('#jstree_div').jstree('deselect_node', PbElevations[each]);
  					}
  				}

  				//取消选择的分区
  				if(_selZones.length > 1) {
  					var PbZones = _selZones.substr(0, _selZones.length - 1).split(",");
  					for(var each in PbZones) {
  						$('#jstree_div').jstree('deselect_node', PbZones[each]);
  					}
  				}

  				_curUnitId = data.node.data.unitid;
  				bChangeModel = true;

  			}else if(data.node.parents.indexOf("unitprj_"+_curUnitId)==-1){
  				return;
  			}else if(nodetype == "floor") {
  					_selElevations = _selElevations + data.node.id.split('_')[1] + ",";
  			} else if(nodetype.indexOf("zone") != -1) {
  					_selZones = _selZones + data.node.id.split('_')[1] + ",";
  			} else {

  				return;
  			}

  			if(bChangeModel) {
  				_selElevations = "";
  				_selZones = "";

  				//getSelectElevations();

//				$("#pbtable tbody").html("");
//				$("#pagebar").html("");
//				$("#pbnumber").text("");
//				$("#pbtype").text("");
//				$("#pbstatus").text("");
//				$("#pbvolume").text("");
//				$("#pbelevation").text("");
//				$("#pbqrcode").attr('href', '');
//				$("#pbtrace").attr('href', '');

  				getModelFile();

  			} else {

  				filterPblist();
  				changepage2Page(1);

  				saveSelectElevations();
  			}

  		}

  	});

  	$("#jstree_div").on("deselect_node.jstree", function(evt, data) {
  		if(data.id != "#" && data.id != "model") {

  			var nodetype = data.node.id.split('_')[0];
  			if(nodetype == "unitprj") {
  				return;

  			}else if(data.node.parents.indexOf("unitprj_"+_curUnitId)==-1){
  				return;
  			}
  			else if(nodetype == "floor") {
  				var selNodes = getCurrentTreeSelectedObjs();
  				_selElevations = "";
  				$.each(selNodes, function(num, treeNode) {
  					var nodetype2 = treeNode.id.split('_')[0];
  					if(nodetype2 == "floor")
  						_selElevations += treeNode.id.split('_')[1] + ",";
  				});

  			} else if(nodetype.indexOf("zone") != -1) {
  				var selNodes = getCurrentTreeSelectedObjs();
  				_selZones = "";
  				$.each(selNodes, function(num, treeNode) {
  					var nodetype2 = treeNode.id.split('_')[0];
  				  if(nodetype2.indexOf("zone") != -1) {
  						_selZones += treeNode.id.split('_')[1] + ",";
  						}
  				});
  			} else {

  				return;
  			}

  			saveSelectElevations();

  			filterPblist();
  			changepage2Page(1);
  		}

  	});
  }
  
function initPbTypeTree() {
// initialize the tree
  	$("#jstree_div_pbtype").jstree({
  		"core": {
  			'data': {
  				'url': '/task/modelview/getpbtypetree/',
  				'data': function(node) {
  					return {
  						'id': node.id
  					};
  				}
  			}
  		},
  		"plugins": ["themes", "json_data", "checkbox"],
  		"checkbox": {
  			"three_state": false
  		}
  	});

 
  	$("#jstree_div_pbtype").on("ready.jstree", function() {
  		$('#jstree_div_pbtype').jstree('select_node', "major_" + _curMajor);
  	});



  

  	// event for when a node in the tree is selected
  	$("#jstree_div_pbtype").on("select_node.jstree", function(evt, data) {
  		console.debug(data.node.id);
  		if(data.id != "#" && data.id != "pbtypetree") {
  			var bChangeModel = false;
  			var curSelMajorId;
  			var selectedModel = 0;

  			var nodetype = data.node.id.split('_')[0];
  			if(nodetype == "major") {
  				if(data.node.data.majorid == _curMajor) {
  					return;
  				}

  				var selNodes = getCurrentPbtypeTreeSelectedObjs();
  				var lastMajorId = _curMajor;
  				$.each(selNodes, function(num, treeNode) {
  					if(treeNode.data) {
  						if(treeNode.data.majorid == lastMajorId) {
  							$('#jstree_div_pbtype').jstree('deselect_node', treeNode.id);
  							//取消选择的构件类型
  							if(_selPbtypes.length > 1) {
  								var PbTypes = _selPbtypes.substr(0, _selPbtypes.length - 1).split(",");
  								for(var each in PbTypes) {
  									$('#jstree_div_pbtype').jstree('deselect_node', PbTypes[each]);
  								}
  							}
  							$('#jstree_div_pbtype').jstree('close_node', treeNode.id);
  						}
  					}
  				});

  				_curMajor = data.node.data.majorid;
  				bChangeModel = true;
					reLoadJsTree();
  			} else if(nodetype == "type") {
  				if(data.node.parent.split('_')[1] == _curMajor) {
  					_selPbtypes = _selPbtypes + data.node.id.split('_')[1] + ",";
  				} else {
  					return;
  				}

  			} else {

  				return;
  			}

  			if(bChangeModel) {

  				_selPbtypes = "";

//				$("#pbtable tbody").html("");
//				$("#pagebar").html("");
//				$("#pbnumber").text("");
//				$("#pbtype").text("");
//				$("#pbstatus").text("");
//				$("#pbvolume").text("");
//				$("#pbelevation").text("");
//				$("#pbqrcode").attr('href', '');
//				$("#pbtrace").attr('href', '');

  				getModelFile();
  			} else {
  				saveSelectPbTypes();
  				filterPblist();
  				changepage2Page(1);
  			}

					//getPbStatusByMajor();
  		}
  		//_viewer.select(data.node.data.dbId);   // selecting interferes with ability to do HIDE in context menu

  	});

  	$("#jstree_div_pbtype").on("deselect_node.jstree", function(evt, data) {
  		console.debug(data.node.id);

  		if(data.id != "#" && data.id != "pbtypetree") {
  			var nodetype = data.node.id.split('_')[0];
  			if(nodetype == "type") {
  				var selNodes = getCurrentPbtypeTreeSelectedObjs();
  				_selPbtypes = "";
  				$.each(selNodes, function(num, treeNode) {
  					var nodetype2 = treeNode.id.split('_')[0];
  					if(nodetype2 == "type")
  						_selPbtypes += treeNode.id.split('_')[1] + ",";
  				});

  				saveSelectPbTypes();

  				filterPblist();
  				changepage2Page(1);
  			}
  			
  			//getPbStatusByMajor();
  			
  		}
  		//_viewer.select(data.node.data.dbId);   // selecting interferes with ability to do HIDE in context menu
  	});

}

  function LoadAllCustomTrees() {
  	initJsTree();

  	initPbTypeTree();

  };


  // get the items in the tree that are currently selected
  function getCurrentTreeSelectedObjs() {
  	var tree = $.jstree.reference("#jstree_div"); //get tree instance
  	var selNodes = tree.get_selected(true);

  	return selNodes;
  }

  function filterPblist() {
  	$.ajax({
  		type: "get",
  		url: "/task/modelview/filterPblist/",
  		cache: false,
  		dataType: "json",
  		data: {
  			"_selElevations": _selElevations,
  			"_selPbtypes": _selPbtypes,
  			"_curUnitId": _curUnitId,
  			"_selZones":_selZones,
  			"_curMajor":_curMajor,
  		},
  		success: function(data) {

  			_viewer.clearThemingColors();

				var dbids=[];
  			for(var each in data.pblist) {
  				dbids.push(parseInt(data.pblist[each].lvmdbid));
  				//_viewer.show(parseInt(data.pblist[each].lvmdbid));
  			}
  			_viewer.isolateById(dbids);
  			getpbstatuslist();
  		}
  	});
  }

  // get the items in the tree that are currently selected
  function getCurrentPbtypeTreeSelectedObjs() {
  	var tree = $.jstree.reference("#jstree_div_pbtype"); //get tree instance
  	var selNodes = tree.get_selected(true);

  	return selNodes;
  }


  function reLoadJsTree() {

  	var parentdiv = $('#jstree_div').parent();
  	$("#jstree_div").remove();
  	var jstreediv = '<div id="jstree_div" > </div>';
  	$(parentdiv).append(jstreediv);
  	initJsTree();
  }


function getPbStatusByMajor()
{
//	  	$.ajax({
//		type: "get",
//		url: "/task/modelview/getstatuslist",
//		cache: false,
//		dataType: "json",
//		data: {
//			"_selPbtypes": _selPbtypes,
//			"_curMajor":_curMajor,
//		},
//		success: function(data) {
//
//			$("#pbstatussel").empty();
//			
//			for(var each in data.statuslist) {
//				$("#pbstatussel").append("<option value='"+data.statuslist[each].id+"'>"+data.statuslist[each].name+"</option>");
//			}
//		}
//	});
	
	
}

  $("#btnPbsearch").click(function() {
  	var pbstatus = $("#pbstatussel").val();
  	var timerange = $("#timerange").val();

  	$.ajax({
  		type: "get",
  		url: "/task/modelview/getpblisttimerange/",
  		cache: false,
  		dataType: "json",
  		data: {
  			"pbstatus": pbstatus,
  			"timerange": timerange,
  			"_curUnitId": _curUnitId,
  		},
  		success: function(data) {
  			_viewer.clearThemingColors();

  			for(var each in data.pblist) {
  				_viewer.setThemingColor(parseInt(data.pblist[each].lvmdbid), _colorPbsearch);
  			}

  		}
  	});

  	changepage2PageStatus(1);
  });

  $("#btnRestore").click(function() {
  	_viewer.showAll();
  	getpbstatuslist();
  });
  
function changepage2Page(page)
{
	
}
