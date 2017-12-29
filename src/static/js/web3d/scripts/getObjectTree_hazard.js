  function getSelectElevations() {
  	url = window.location.href;
  	var valueSelElevations = localStorage.getItem(url + "-unitprjtreeSelElevations" + curUnitId);
  	if(valueSelElevations) {
  		//selElevations = valueSelElevations;
  		console.log(valueSelElevations + 'selElevations datas are restored');

  		var Elevations = valueSelElevations.substr(0, valueSelElevations.length - 1).split(",");
  		for(var each in Elevations) {
  			$('#jstree_div').jstree('select_node', Elevations[each]);
  		}
  	}

  }

  function deSelectElevations(unitId) {
  	url = window.location.href;
  	var valueSelElevations = localStorage.getItem(url + "-unitprjtreeSelElevations" + unitId);
  	if(valueSelElevations) {
  		//selElevations = valueSelElevations;
  		console.log(valueSelElevations + 'selElevations datas are restored');

  		var Elevations = valueSelElevations.substr(0, valueSelElevations.length - 1).split(",");
  		for(var each in Elevations) {
  			$('#jstree_div').jstree('deselect_node', Elevations[each]);
  		}
  	}

  }

  function saveSelectPbTypes() {
  	url = window.location.href;
  	localStorage.setItem(url + "-pbtypetreeSelPbtypes", selPbtypes);
  }

  function getSelectPbTypes() {
  	url = window.location.href;

  	var valueSelPbtypes = localStorage.getItem(url + "-pbtypetreeSelPbtypes");
  	if(valueSelPbtypes) {
  		selPbtypes = valueSelPbtypes;
  		console.log(selPbtypes + 'selPbtypes datas are restored');

  		var PbTypes = selPbtypes.substr(0, selPbtypes.length - 1).split(",");
  		for(var each in PbTypes) {
  			$('#jstree_div_pbtype').jstree('select_node', PbTypes[each]);
  		}
  	}
  }

  function LoadAllCustomTrees() {

  	// initialize the tree
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
  		"plugins": ["themes", "json_data", "checkbox"],
  		"checkbox": {
  			"three_state": false
  		}
  	});

  	// event for when a node in the tree is selected
  	$("#jstree_div_hazard").on("select_node.jstree", function(evt, data) {
  		var node = data.node;
  		var ji;
  		if(node.parents.length >= 3) {
  			if(data.node.parents[data.node.parents.length - 3] == '1')
  				ji = '一级';
  			else if(data.node.parents[data.node.parents.length - 3] == '2')
  				ji = '二级';
  			else if(data.node.parents[data.node.parents.length - 3] == '3')
  				ji = '三级';
  		}

  		var newRow = "<tr class='"+ +">"
  		newRow += "<td style='width:80px;'>" + ji + "</td>";
  		newRow += "<td>" + data.node.text + "</td>";
  		newRow += "<td>5天</td>";
  		newRow += "<td><a href='#'>选择空间</a></td>";
  		newRow += "<td>"+$('#selectmajor').html()+"</td>"; //专业
  		newRow += "<td>"+$('#selectshoukong').html()+"</td>"; //是否受控
  		newRow += "<td><input type='text' /></td>";
  		newRow += "<td>检查</td>";
  		newRow += "</tr>";
  		$("#today_hazard_table").append(newRow);

  	});

  	$("#jstree_div").on("deselect_node.jstree", function(evt, data) {
  		//console.debug(data.node.data);
  		if(data.id != "#") {
  			if(data.node.data) {
  				return;
  			}
  			parent_node_id = $('#jstree_div').jstree('get_parent', data.node.id);
  			parent_node = $('#jstree_div').jstree('get_node', parent_node_id);

  			if(!$('#jstree_div').jstree('is_selected', parent_node_id)) {
  				return;
  			}

  			var selNodes = getCurrentTreeSelectedObjs();

  			var curSelElevations = "";
  			var bChangeModel = false;
  			var modelfile;
  			var curSelUnitId;
  			var selectedModel = 0;

  			$.each(selNodes, function(num, treeNode) {
  				if(!treeNode.data) {
  					curSelElevations += treeNode.id + ",";
  				} else {

  				}
  			});

  			{
  				selElevations = curSelElevations;
  				filterPblist();
  				changepage2Page(1);
  			}

  		}

  		saveSelectElevations();
  	});

  	// event for when a node in the tree is selected
  	$("#jstree_div_pbtype").on("select_node.jstree", function(evt, data) {
  		console.debug(data.node.id);
  		var selNodes = getCurrentPbtypeTreeSelectedObjs();
  		selPbtypes = "";
  		$.each(selNodes, function(num, treeNode) {
  			if(!treeNode.data)
  				selPbtypes += treeNode.id + ",";
  		});

  		saveSelectPbTypes();

  		filterPblist();
  		changepage2Page(1);
  		//_viewer.select(data.node.data.dbId);   // selecting interferes with ability to do HIDE in context menu
  	});

  	$("#jstree_div_pbtype").on("deselect_node.jstree", function(evt, data) {
  		console.debug(data.node.id);
  		var selNodes = getCurrentPbtypeTreeSelectedObjs();
  		selPbtypes = "";
  		$.each(selNodes, function(num, treeNode) {
  			if(!treeNode.data)
  				selPbtypes += treeNode.id + ",";
  		});

  		saveSelectPbTypes();

  		filterPblist();
  		changepage2Page(1);
  		//_viewer.select(data.node.data.dbId);   // selecting interferes with ability to do HIDE in context menu
  	});

  };

  // recursively add all the nodes in the Model Structure of LMV to the jsTree
  function recursiveAddChildrenToTree(tree, rootNode, children) {
  	if(!children)
  		return;

  	$.each(children, function(num, obj) {
  		// create a new object to attach to the tree node
  		var myObj = {};
  		myObj.text = obj.name; // text displayed in the tree
  		myObj.data = obj; // keep track of the original object so we can retrieve it later

  		var newNode = tree.create_node(rootNode, myObj);
  		recursiveAddChildrenToTree(tree, newNode, obj.children);
  	});
  };

  // callback function onSuccess when trying to retrieve Properties for a given object
  function propsDisplayFunc(data) {
  	if((data.properties == null) || (data.properties.length == 0)) {
  		alert("There are no properties for this node.");
  		return;
  	}
  	// iterate over the properties and just build a simple name value pair in a big string.
  	var tblStr = "";
  	$.each(data.properties, function(num, obj) {
  		var propPairStr = obj.displayName + ":     " + obj.displayValue + "\n";
  		tblStr += propPairStr;
  	})
  	alert(tblStr);
  }

  // callback function onError when trying to retrieve Properties for a given object
  function propsErrorFunc(data) {
  	alert("ERROR: Could not get properties for the selected object.");
  }

  // get the items in the tree that are currently selected
  function getCurrentTreeSelectedObjs() {
  	var tree = $.jstree.reference("#jstree_div"); //get tree instance
  	var selNodes = tree.get_selected(true);

  	return selNodes;
  }

  // this function is called from jsTree to provide the menu items for a right-click context menu on a tree node
  function customRightClickTreeMenu(node) {

  	if(node.id == "model")
  		return;
  	if(node.data) {
  		var items = {
  			"load": {
  				"label": "加载BIM模型",
  				"action": function(obj) {
  					var selNodes = getCurrentTreeSelectedObjs();

  					// if (selNodes.length > 1) {
  					//     alert("只能同时查看一个模型！");
  					// }
  					// else {
  					//	loadDocument(selNodes[0].data.urn);
  					// }
  					selPbtypes = "";
  					selElevations = "";
  					$("#pbtable tbody").html("");
  					$("#pagebar").html("");
  					$("#pbnumber").text("");
  					$("#pbtype").text("");
  					$("#pbstatus").text("");
  					$("#pbvolume").text("");
  					$("#pbelevation").text("");
  					$("#pbqrcode").attr('href', '');
  					$("#pbtrace").attr('href', '');

  					$.each(selNodes, function(num, treeNode) {
  						if(treeNode.data) {
  							curUnitId = treeNode.data.unitid;
  							loadDocument(treeNode.data.modelfile);
  						}
  					});
  				}
  			},
  			"select": {
  				"label": "查看构件",
  				"action": function(obj) {
  					var selNodes = getCurrentTreeSelectedObjs();
  					selElevations = "";
  					$.each(selNodes, function(num, treeNode) {
  						if(!treeNode.data)
  							selElevations += treeNode.id + ",";
  					});
  					filterPblist();
  					changepage2Page(1);
  				}
  			},
  		};
  		return items;
  	} else {
  		var items = {
  			"select": {
  				"label": "查看构件",
  				"action": function(obj) {
  					var selNodes = getCurrentTreeSelectedObjs();
  					selElevations = "";
  					$.each(selNodes, function(num, treeNode) {
  						if(!treeNode.data)
  							selElevations += treeNode.id + ",";
  					});
  					filterPblist();
  					changepage2Page(1);
  				}
  			},
  		};
  		return items;
  	}

  }

  function filterPblist() {
  	$.ajax({
  		type: "get",
  		url: "/task/modelview/filterPblist/",
  		cache: false,
  		dataType: "json",
  		data: {
  			"selElevations": selElevations,
  			"selPbtypes": selPbtypes,
  			"curUnitId": curUnitId,
  		},
  		success: function(data) {

  			_viewer.clearThemingColors();

  			HideAllModelsObject();

  			for(var each in data.pblist) {
  				_viewer.show(parseInt(data.pblist[each].lvmdbid));
  			}
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

  function customRightClickPbTypeTreeMenu(node) {
  	if(node.id == "model")
  		return;

  	var items = {
  		"select": {
  			"label": "产看类型",
  			"action": function(obj) {
  				var selNodes = getCurrentPbtypeTreeSelectedObjs();
  				selPbtypes = "";
  				$.each(selNodes, function(num, treeNode) {
  					if(!treeNode.data)
  						selPbtypes += treeNode.id + ",";
  				});
  				filterPblist();
  				changepage2Page(1);
  			}
  		},
  	};
  	return items;
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
  			"curUnitId": curUnitId,
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