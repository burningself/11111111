// LoadModel.js
var _viewer = null; // the viewer
var _savedGlobalCamera = null;
var _loadedDocument = null;

var _overlayMap = {};
var _colorPbsearch = null;
var _colorSelected = null;

var nodesToProcess = [];

var _isWholeModel = false;
var _curUnitId = "";
var _curMajor = "";
var _selElevations = "";
var _selZones = "";
var _selPbtypes = "";

var _lastSelectDbid = 0;

var mapElemId2DbId = {};
var mapDbId2ElemId = {};

var mapElemId2DbIdSql = "";

//pgb 注释掉暂时不做本地缓存
var _needLoadStorage = false;

var _selectedId = null;
var _pbDbidList = [];

// add the two overlays to the system
function initOverlays() {

	_colorPbsearch = new THREE.Vector4(0, 1, 0, 0.5); // r, g, b, intensity
	_colorSelected = new THREE.Vector4(0.4, 0.6, 1, 1.0); 
}

// initialize the viewer into the HTML placeholder
function initializeViewer() {

	if(_viewer !== null) {
		//_viewer.uninitialize();
		_viewer.finish();
		_viewer = null;
		_savedGlobalCamera = null;
		_savedViewerStates = [];
	} else {
		initOverlays(); // set up the Overlays one time
	}

	//var viewerElement = document.getElementById("viewer");  // placeholder in HTML to stick the viewer
	//_viewer = new Autodesk.Viewing.Private.GuiViewer3D(viewerElement, {});
	_viewer = new Autodesk.Viewing.Private.GuiViewer3D($("#viewer")[0], {}); // With toolbar

	var retCode = _viewer.initialize();
	if(retCode !== 0) {
		alert("ERROR: Couldn't initialize viewer!");
		console.log("ERROR Code: " + retCode); // TBD: do real error handling here
	}

}

// load a specific document into the intialized viewer
function loadDocument(urnStr) {

	_loadedDocument = null; // reset to null if reloading

	if(!urnStr || (0 === urnStr.length)) {
		alert("You must specify a URN!");
		return;
	}

	initializeViewer();

	var fullUrnStr = urnStr;

	_viewer.load(fullUrnStr);
	

	_viewer.addEventListener(Autodesk.Viewing.GEOMETRY_LOADED_EVENT, function(e) {
		if(_viewer.model) {
			
			
			setContextMenu();
			customViewer();
			
			//注释掉 需要做匹配的时候再打开 pgb
			//getAllNodes();

			if(_needLoadStorage) {
				getSelectPbTypes();
				_needLoadStorage = false;
			}
			getSelectElevations();

			_viewer.getObjectTree(function(objTree) {
				getpbstatuslist();
			});


			changepage2Page();
			
		}
	});

	_viewer.addEventListener(Autodesk.Viewing.SELECTION_CHANGED_EVENT, onSelectedCallback);

	_viewer.setGhosting(true);
	
	_viewer.unloadExtension('Autodesk.ADN.Viewing.Extension.SampleTaskStatus'); //显示属性页 !!!!!!
	_viewer.loadExtension('Autodesk.ADN.Viewing.Extension.SampleTaskStatus'); //显示属性页 !!!!!!
	_viewer.createSamplePanel(_curUnitId,_curMajor,_isWholeModel);
}


function isPrebeamNode(dbId) {
	var isPrebeam = false;
	for(var i = 0; i < _pbDbidList.length; ++i) {
		if(dbId == _pbDbidList[i]) {
			isPrebeam = true;
			break;
		}
	}

	return isPrebeam;
}



function setContextMenu() {
	Autodesk.ADN.Viewing.Extension.AdnContextMenu = function(viewer) {
		Autodesk.Viewing.Extensions.ViewerObjectContextMenu.call(this, viewer);
	};

	Autodesk.ADN.Viewing.Extension.AdnContextMenu.prototype =
		Object.create(Autodesk.Viewing.Extensions.ViewerObjectContextMenu.prototype);

	Autodesk.ADN.Viewing.Extension.AdnContextMenu.prototype.constructor =
		Autodesk.ADN.Viewing.Extension.AdnContextMenu;

	Autodesk.ADN.Viewing.Extension.AdnContextMenu.prototype.buildMenu =

		function(event, status) {

			var menu = Autodesk.Viewing.Extensions.ViewerObjectContextMenu.prototype.buildMenu.call(
				this, event, status);

			if(_selectedId) {
				menu.push({
					title: "关联本地文件",
					target: function() {
						
						pbrelatefile(_selectedId,"local");
						
					}
				});
//				menu.push({
//					title: "关联云端文件",
//					target: function() {
//						
//						pbrelatefile(_selectedId,"cloud");
//					}
//				});
			}
			return menu;
		};

	_viewer.setContextMenu(new Autodesk.ADN.Viewing.Extension.AdnContextMenu(_viewer));

}

function pbrelatefile(dbId,type) {
	$.ajax({
		type: "get",
		url: "/task/modelview/getpbproperty",
		cache: false,
		dataType: "json",
		data: {
			"dbId": dbId,
			"_curUnitId": _curUnitId,
			"_curMajor": _curMajor,
		},
		success: function(data) {
			if(data.issuc == "true") {
				
				if(type=="local"){
					getrelatefilelist("构件",data.pbid);
					window.open("/task/ziliao/uploadview/");
				}else{
					//window.open("/task/ziliao/cloudfilerelate/");
				}
			} 
		}
	});
}

//混泥土："IFCRAMP","IFCBEAM","IFCCOLUMN","IFCWALLSTANDARDCASE","IFCSLAB","IFCFOOTING"
//安全设施："IFCCOLUMN","IFCRAILING","IFCBUILDINGELEMENTPROXY"
//钢结构：IFCELEMENTASSEMBLY
var _ModelPbType = ["IFCRAMP","IFCBEAM","IFCCOLUMN","IFCWALLSTANDARDCASE","IFCSLAB","IFCFOOTING","IFCWALL",
					"IFCBUILDINGSTOREY","IFCWALLSTANDARDCASE","IFCBOOLEANCLIPPINGRESULT","IFCRAILING","IFCBUILDINGELEMENTPROXY","IFCELEMENTASSEMBLY","IFCROOF",
					"IFCPROJECT","IFCSITE","IFCBUILDING","IFCBUILDINGSTOREY","IFCWALLSTANDARDCASE","IFCSHAPEREPRESENTATION",
					"IFCEXTRUDEDAREASOLID","IFCBOOLEANCLIPPINGRESULT","IFCRAMPFLIGHT","IFCSTAIR","IFCSTAIRFLIGHT","IFCMAPPEDITEM",'IFCFLOWCONTROLLER','IFCFLOWSEGMENT'];
var tmp = {};
function getElementIdFromPropNameIFC(props) {

	var isBeam = false;
	for(var each in props.properties){
		
		if(props.properties[each].displayCategory=="Item" && props.properties[each].displayName=="Type"){
			if (!tmp[props.properties[each].displayValue]){
				tmp[props.properties[each].displayValue]=true;
				console.log(props.properties[each].displayValue);
			}
		}
		
		if(props.properties[each].displayCategory=="Item" && props.properties[each].displayName=="Type"&&
			_ModelPbType.indexOf(props.properties[each].displayValue)!=-1){
			isBeam = true;
		}

		
		if(props.properties[each].displayCategory=="IFC" && props.properties[each].displayName=="GLOBALID"&&isBeam)
		{
			//console.log(props.properties[each].displayValue);
			return props.properties[each].displayValue;
		}
	}

	return "";
}


var dddd = 0;

function makeDbidWithElemIdMap() {

	var sumofNode = nodesToProcess.length;

	for(var i = 0; i < sumofNode; ++i) {
		_viewer.getProperties(nodesToProcess[i], function(props) {
			var ElemId = getElementIdFromPropNameIFC(props);
			//var ElemId = getElementIdFromPropName(props);
			dddd = dddd + 1;

			if(ElemId != "") {
				var sql = "update taskandflow_precastbeam set lvmdbid = " + props.dbId + " WHERE guid= '" + ElemId + "' and pbtype_id in (SELECT id from taskandflow_pbtype WHERE major_id=" + _curMajor + ");\r\n";
				mapElemId2DbIdSql += sql;
				//mapElemId2DbId.put(ElemId,props.dbId);
				//mapDbId2ElemId.put(props.dbId,ElemId);
			}



			if(dddd == sumofNode) {
				$("#sqllist").val(mapElemId2DbIdSql);
				$("#sqllist").attr('style', 'display:inline');
			}

		});
	}
}


function getallPb2Sql() {

	var sumofNode = nodesToProcess.length;

	for(var i = 0; i < sumofNode; ++i) {
		_viewer.getProperties(nodesToProcess[i], function(props) {
			
			dddd = dddd + 1;
			var number = "CS"+dddd;
		
				var sql = "INSERT into taskandflow_precastbeam(id,guid,revitfilename,elementid,lvmdbid,number,sign,drawnumber,elevation_id,pbtype_id) VALUES (NULL,'','','',"+props.dbId +",'"+number+"','"+number+"','"+number+"',268,30);\r\n";
				
				mapElemId2DbIdSql += sql;
			



			if(dddd == sumofNode) {
				$("#sqllist").val(mapElemId2DbIdSql);
				$("#sqllist").attr('style', 'display:inline');
			}

		});
	}
}


function getAllNodes(root) {

	nodesToProcess = [];

	_viewer.getObjectTree(function(objTree) {
		var root = objTree.getRootId();
		objTree.enumNodeChildren(root, function(dbId) {

			nodesToProcess.push(dbId);
			
		}, true);
		//注释掉需要计算时再打开
		makeDbidWithElemIdMap();
		
		//getallPb2Sql();
	});
	
}


function onSelectedCallback(event) {
	// display a message if an element is selected
	var msg = "";

	if(event.dbIdArray.length > 0) {
		_selectedId = event.dbIdArray[0];
		console.log(_selectedId);
		getpbproperty(_selectedId);

	} else {
		_selectedId = null;
	}
	
}

function getpbproperty(dbId) {
	$.ajax({
		type: "get",
		url: "/task/modelview/getpbproperty/",
		cache: false,
		dataType: "json",
		data: {
			"dbId": dbId,
			"_curUnitId": _curUnitId,
			"_curMajor": _curMajor,
		},
		success: function(data) {
			if(data.issuc == "true") {
				$("#pbnumber").text(data.pbnumber);
				$("#pbtype").text(data.pbtype);
				$("#pbstatus").text(data.pbstatus);
				$("#statuspercent").text(data.curstatuspercent+"%");
				$("#pbelevation").text(data.pbelevation);
				$("#statusdesc").text(data.statusdesc);
				
				
				var traceurl = "javascript:TracePbStatus(" + data.pbid + ");";
				
				var qrcodeurl = "javascript:PrintPbQrcode(" + data.pbid + ");";
				getrelatefilelist("构件",data.pbid);
	
				$("#pbqrcode").attr('href', qrcodeurl);
				$("#pbtrace").attr('href', traceurl);
			} else {
				$("#pbnumber").text("无构件信息");
				$("#pbtype").text("");
				$("#pbstatus").text("");
				$("#pbelevation").text("");
				$("#statuspercent").text("");
				$("#pbqrcode").attr('href', '#');
				$("#pbtrace").attr('href', '#');
			}

		}
	});
}




function getpbstatuslist() {
	$.ajax({
		type: "get",
		url: "/task/modelview/getpbstatuslist/",
		cache: false,
		dataType: "json",
		data: {
			"_selElevations": _selElevations,
			"_selPbtypes": _selPbtypes,
			"_curUnitId": _curUnitId,
			"lastSelectDbid": _lastSelectDbid,
			"_selZones": _selZones,
			"_curMajor": _curMajor,
			"_isWholeModel": _isWholeModel,
		},
		success: function(data) {
			if(data.issuc = "true") {
				_pbDbidList = [];
				for(var each in data.pbstatuslist) {
					var color = getColorByStr(data.pbstatuslist[each].color);
					for(var eachpb in data.pbstatuslist[each].pblist) {
						_viewer.setThemingColor(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid), color);
						
						//todo 特殊处理 pgb
						//if(_curMajor==2)
						{
							setChildThemingColor(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid), color);
						}
						
						_pbDbidList.push(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid));
					}
				}
				
				_viewer.isolate(_pbDbidList);
			}
		}
	});
}

function getpbstatus() {
	$.ajax({
		type: "get",
		url: "/task/modelview/getpbstatus/",
		cache: false,
		dataType: "json",
		data: {
			"_curUnitId": _curUnitId,
			"lastSelectDbid": _lastSelectDbid,
		},
		success: function(data) {
			if(data.issuc = "true") {
				for(var each in data.pbstatuslist) {

					for(var eachpb in data.pbstatuslist[each].pblist) {
						//var dbids = [];
						//dbids.push(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid));
						//overrideColorOnObj(dbids, _overlayMap.get(data.pbstatuslist[each].name));
						var color = _overlayMap[data.pbstatuslist[each].name];
						_viewer.setThemingColor(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid), color);
					}
				}
			}
		}
	});
}



