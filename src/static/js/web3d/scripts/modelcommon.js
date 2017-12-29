var _isWholeModel = false;
var _curUnitId = "";
var _curMajor = "";
var _selectionmode = "";
var _homeview = [];

// called when HTML page is finished loading, trigger loading of default model into viewer
function loadInitialModel() {

	$.ajax({
		type: "get",
		url: "/task/modelview/getinitialmodel/",
		cache: false,
		dataType: "json",
		data: {},
		success: function(data) {
			if(data.issuc == "true") {
				var options = {};
				options.env = "Local"; // AutodeskProduction, AutodeskStaging, or AutodeskDevelopment (set in global var in this project)
				options.document = "http://"+window.location.host+data.modelfile;
				_curUnitId = data.unitid;
				_curMajor = data.majorid;
				_isWholeModel = data.iswhole
				_selectionmode = data.selectionmode
            	_homeview = eval(data.homeview)
            	_extdata = eval(data.extdata)
            
				Autodesk.Viewing.Initializer(options, function() {
					loadDocument(options.document); // load first entry by default
				});
			}
			
			LoadAllCustomTrees();
		}
	});
}

function getModelFile() {
	if(_curUnitId == "" || _curMajor == "") {
		return;
	}
	
	$.ajax({
		type: "get",
		url: "/task/modelview/getmodelfile/",
		cache: false,
		dataType: "json",
		data: {
			"_curMajor": _curMajor,
			"_curUnitId": _curUnitId,
		},
		success: function(data) {
			if(data.issuc == "true") {
				_isWholeModel = data.iswhole
				_selectionmode = data.selectionmode
            	_homeview = eval(data.homeview)
            	_extdata = eval(data.extdata)
				loadDocument("http://"+window.location.host+data.modelfile); // load first entry by default
			} else {
				alert("没有对应单位工程专业模型！");
			}
		}
	});
}

function getModelFile2() {
	var defaultunitId = $("#selUnitproject option:selected").val();
	
	$.ajax({
		type: "get",
		url: "/task/modelview/getmodelfile/",
		cache: false,
		dataType: "json",
		data: {
			"_modelfile": defaultunitId,
		},
		success: function(data) {
			if(data.issuc == "true") {
				_isWholeModel = data.iswhole
				_curUnitId = data.unitid;
				_curMajor = data.majorid;
				
				_selectionmode = data.selectionmode
            	_homeview = eval(data.homeview)
            	_extdata = eval(data.extdata)
				loadDocument("http://"+window.location.host+data.modelfile); // load first entry by default
			} else {
				alert("没有对应单位工程专业模型！");
			}
		}
	});
}


function transViewCustom(){
	if(_homeview.length>=3){
		//var newCamPos = new THREE.Vector3(-149715.3552195181,-119243.66328031197,34681.408770079055);
		var newCamPos = new THREE.Vector3(_homeview[0],_homeview[1],_homeview[2]);
		
		var target = new THREE.Vector3(0,0,0);
		var cam=_viewer.navigation.getCamera();
		_viewer.navigation.setRequestTransition(true,newCamPos,target,cam.fov);
	}
}

var _modeindex = 0;
function customViewer() {
	
	if(_selectionmode=="FIRST_OBJECT"){
		_viewer.setSelectionMode(Autodesk.Viewing.SelectionMode.FIRST_OBJECT);
	}
	
	//
	transViewCustom();
	setTimeout (function () {   _viewer.autocam.setCurrentViewAsHome();}, 1000) ; 
	
	//custom background color-----[pgb]
	_viewer.setBackgroundColor(48, 153, 225, 255,255, 255);
	//_viewer.setBackgroundColor(60, 141, 188, 255,255, 255);
	
	//toolbar custom -------------[pgb]
    var viewerToolbar = _viewer.getToolbar(true);
    var settingsTools = viewerToolbar.getControl(Autodesk.Viewing.TOOLBAR.SETTINGSTOOLSID);
    //viewerToolbar.removeControl(settingsTools);
	var navTools = viewerToolbar.getControl(Autodesk.Viewing.TOOLBAR.NAVTOOLSID);
	//navTools.removeControl("toolbar-cameraSubmenuTool");
	navTools.removeControl("toolbar-zoomTool");
	
    var modelTools = viewerToolbar.getControl(Autodesk.Viewing.TOOLBAR.MODELTOOLSID);
	modelTools.removeControl("toolbar-explodeTool");
   	  
	var changmodelBtn = new Autodesk.Viewing.UI.Button("changmodelBtn");
    changmodelBtn.icon.style.backgroundImage = 'url(img/swapmodel3.png)';
    changmodelBtn.setToolTip("切换模型显示");
    changmodelBtn.onClick =  function (e){
        _modeindex = (_modeindex+1)%2;
		
       	 switch (_modeindex)
		{
		case 0:
			getpbstatuslist();
		  break;
		case 1:
		  	_viewer.clearThemingColors();
			_viewer.showAll();
		  break;
		}
      };
	 modelTools.addControl(changmodelBtn, {index:3});
	
}


function getMeshPosition(fragId) {

	var mesh = _viewer.impl.getRenderProxy(_viewer.model, fragId);

	var pos = new THREE.Vector3();

	pos.setFromMatrixPosition(mesh.matrixWorld);

	return pos;
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

function setChildThemingColor(root, color) {

	var it = _viewer.model.getData().instanceTree;

	it.enumNodeChildren(root, function(dbId) {
		_viewer.setThemingColor(dbId, color);
	}, true);

}

function getOriginalWorldBoundingBox(fragIds) {

	var fragBoundingBox = new THREE.Box3();
	var nodeBoundingBox = new THREE.Box3();

	var fragmentBoxes = _viewer.model.getFragmentList().boxes;

	fragIds.forEach(function(fragId) {

		var boffset = fragId * 6;

		fragBoundingBox.min.x = fragmentBoxes[boffset];
		fragBoundingBox.min.y = fragmentBoxes[boffset + 1];
		fragBoundingBox.min.z = fragmentBoxes[boffset + 2];
		fragBoundingBox.max.x = fragmentBoxes[boffset + 3];
		fragBoundingBox.max.y = fragmentBoxes[boffset + 4];
		fragBoundingBox.max.z = fragmentBoxes[boffset + 5];

		nodeBoundingBox.union(fragBoundingBox);
	});

	return nodeBoundingBox;
}

function getModifiedWorldBoundingBox(fragIds) {

	var fragbBox = new THREE.Box3();
	var nodebBox = new THREE.Box3();

	fragList = _viewer.model.getFragmentList();
	fragIds.forEach(function(fragId) {

		fragList.getWorldBounds(fragId, fragbBox);
		nodebBox.union(fragbBox);
	});

	return nodebBox;
}

function getFragmentIdByDbIds(objectIds) {
	var FragmentIds = [];

	var it = _viewer.model.getData().instanceTree;
	for(var i = 0; i < objectIds.length; i++) {

		var dbid = objectIds[i];

		it.enumNodeFragments(dbid, function(fragId) {

			FragmentIds.push(fragId);

		}, true);
	}

	return FragmentIds;
}