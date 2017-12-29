// LoadModel.js
var _viewer = null; // the viewer
var _savedGlobalCamera = null;
var _loadedDocument = null;

var _overlayMap = {};
var _colorPbsearch = null;

var nodesToProcess = [];

var _isWholeModel = false;
var _curUnitId = "";
var _curMajor = "";
var _selElevations = "";
var _selZones = "";
var _selPbtypes = "";

var _lastSelectDbid = 0;

var mapIssueId2DbId = {};

//pgb 注释掉暂时不做本地缓存
var _needLoadStorage = false;

var _selectedId = 0;
var _pbDbidList = [];

var _alarmDbidList = [];

var _objIssueList = [];

// add the two overlays to the system
function initOverlays() {

	_colorPbsearch = new THREE.Vector4(0, 1, 0, 0.5); // r, g, b, intensity
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
			


			_viewer.getObjectTree(function(objTree) {
				getpbstatuslist();
				window.setInterval(alarmticker,1000);
			});

			customViewer();
		}
	});

	_viewer.addEventListener(Autodesk.Viewing.SELECTION_CHANGED_EVENT, onSelectedCallback);

	_viewer.setGhosting(true);
	
	_viewer.unloadExtension('Autodesk.ADN.Viewing.Extension.SampleSheShi'); 
	_viewer.loadExtension('Autodesk.ADN.Viewing.Extension.SampleSheShi');
	
	_viewer.unloadExtension('Autodesk.ADN.Viewing.Extension.Color'); 
	_viewer.loadExtension('Autodesk.ADN.Viewing.Extension.Color');  
}


function transViewCustom() {
	var newCamPos = new THREE.Vector3(-149715.3552195181, -119243.66328031197, 34681.408770079055);
	var target = new THREE.Vector3(0, 0, 0);
	var cam = _viewer.navigation.getCamera();
	_viewer.navigation.setRequestTransition(true, newCamPos, target, cam.fov);
}

var _timeindex = 0;

function alarmticker() {

	_timeindex = (_timeindex + 1) % 2;

	//restore to original color 
	_viewer.restoreColorMaterial(_alarmDbidList);

	//for( i=0;i<_alarmDbidList.length;i++)
	{
		switch(_timeindex) {
			case 0:
				//_viewer.setThemingColor(_alarmDbidList[i], new THREE.Vector4(1, 0, 0, 0.5));
				_viewer.setColorMaterial(_alarmDbidList, 0xff0000, true);

				break;
			case 1:
				//_viewer.setThemingColor(_alarmDbidList[i], new THREE.Vector4(0, 1, 0, 0.5));
				_viewer.setColorMaterial(_alarmDbidList,0x00FF00,true);  
				break;
		}
	}

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

function onSelectedCallback(event) {
	// display a message if an element is selected
	var msg = "";

	if(event.dbIdArray.length > 0) {
		_selectedId = event.dbIdArray[0];
		//FilterIssueByDbid(_selectedId);
	} else {
		_selectedId = null;
	}
}

function getColorByStr(strColor) {
	var color = null;
	if(strColor != undefined && strColor.length == 7) {
		var r = (parseFloat(parseInt(strColor.substr(1, 2), 16) / 255).toFixed(2));
		var g = (parseFloat(parseInt(strColor.substr(3, 2), 16) / 255).toFixed(2));
		var b = (parseFloat(parseInt(strColor.substr(5, 2), 16) / 255).toFixed(2));

		color = new THREE.Vector4(r, g, b, 0.5); // r, g, b, intensity
	}
	return color;
}

function setChildThemingColor(root,color) {

	var it = _viewer.model.getData().instanceTree;

	it.enumNodeChildren(root, function(dbId) {
		_viewer.setThemingColor(dbId, color);
	}, true);

}
function getpbstatuslist() {
	$.ajax({
		type: "get",
		url: "/task/anquan/jiancha/getpbstatuslist/",
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
			if(data.issuc == "true") {
				_viewer.restoreColorMaterial(_alarmDbidList);
				_pbDbidList = [];
				_alarmDbidList = [];
				for(var each in data.pbstatuslist) {
					var color = getColorByStr(data.pbstatuslist[each].color);
					for(var eachpb in data.pbstatuslist[each].pblist) {
						_viewer.setThemingColor(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid), color);
	
						setChildThemingColor(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid), color);
						
						_pbDbidList.push(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid));

						if(data.pbstatuslist[each].type == "needtick") {
							_alarmDbidList.push(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid));
						}

					}
				}

				updateObjIssue(data);

			}
		}
	});
}

function updateObjIssue(data) {
	
		for(var each in data.jianchapblist) {

			mapIssueId2DbId[data.jianchapblist[each].issueId]=data.jianchapblist[each].pblist;

		}

}

function FilterIssueByDbid(dbid){
	var issueIds=[];
	for(var issue in mapIssueId2DbId) {
   		 for(var each in mapIssueId2DbId[issue]){
   		 		if(mapIssueId2DbId[issue][each]==dbid){
   		 			issueIds.push(issue);
   		 			break;
   		 		}
   		 }
	} 
	
	$(".issuetable tr").each(function(){
		$(this).css("display","");
		if(issueIds.length>0){
			var issId = $(this).attr("id").split("_")[1];
			if($.inArray(issId, issueIds)==-1){
				$(this).css("display","none");
			}	
		}

	});
}



  function filterPblistByIssue(issuetype,issueId) {
 	
  	$.ajax({
		type: "get",
		url: "/task/anquan/getpbstatuslist/",
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
			"issuetype":issuetype,
  			"issueId":issueId
		},
		success: function(data) {
			if(data.issuc == "true") {
				_viewer.restoreColorMaterial(_alarmDbidList);

				_viewer.clearThemingColors();

				_pbDbidList = [];
				_alarmDbidList = [];
				var dbids = [];
				for(var each in data.pbstatuslist) {
					var color = getColorByStr(data.pbstatuslist[each].color);
					for(var eachpb in data.pbstatuslist[each].pblist) {
						//_viewer.show(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid));
						dbids.push(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid));

						_viewer.setThemingColor(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid), color);
						setChildThemingColor(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid), color);
						_pbDbidList.push(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid));

						if(data.pbstatuslist[each].type == "needtick") {
							_alarmDbidList.push(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid));
						}
					}
				}
				_viewer.isolateById(dbids);

				updateObjIssue(data);
			}
		}
	});
  	
  }