// LoadModel.js
$(function() {
	_shiijindu.loadInitialModel();

	_jihuajindu.loadInitialModel();

	
});

var _shiijindu = {
	_viewer: null,// the viewer
	_savedGlobalCamera:null,
	_loadedDocument:null,
	
	_isWholeModel:false,
	_curUnitId:"",
	_curMajor: "",
	_selElevations:"",
	_selZones:"",
	_selPbtypes:"",
	
	
	// initialize the viewer into the HTML placeholder
	initializeViewer:function () {
		var that = this;
		if(that._viewer !== null) {
			//_viewer.uninitialize();
			that._viewer.finish();
			that._viewer = null;
			that._savedGlobalCamera = null;
			that._savedViewerStates = [];
		} else {
			//initOverlays(); // set up the Overlays one time
		}
	
//		var viewerElement = document.getElementById("viewer");  // placeholder in HTML to stick the viewer
//		that._viewer = new Autodesk.Viewing.Private.GuiViewer3D(viewerElement, {});
		that._viewer = new Autodesk.Viewing.Private.GuiViewer3D($(".viewer")[0], {}); // With toolbar
	
		var retCode = that._viewer.initialize();
		if(retCode !== 0) {
			alert("ERROR: Couldn't initialize viewer!");
			console.log("ERROR Code: " + retCode); // TBD: do real error handling here
		}
	
	},
	
	// load a specific document into the intialized viewer
	loadDocument:function (urnStr) {
		var that = this;
		that._loadedDocument = null; // reset to null if reloading
	
		if(!urnStr || (0 === urnStr.length)) {
			alert("You must specify a URN!");
			return;
		}
	
		that.initializeViewer();
	
		var fullUrnStr = urnStr;
	
		that._viewer.load(fullUrnStr);
	
		that._viewer.addEventListener(Autodesk.Viewing.GEOMETRY_LOADED_EVENT, function(e) {
			if(that._viewer.model) {
				that.transViewCustom();
				//if (_curMajor==2)
				{
					that._viewer.setSelectionMode(Autodesk.Viewing.SelectionMode.FIRST_OBJECT);
				}
	
				that._viewer.getObjectTree(function(objTree) {
					that.getpbstatuslist();
				});
				setTimeout (function () {   that._viewer.autocam.setCurrentViewAsHome();}, 1000) ;
				
				//toolbar custom -------------[pgb]
			    var viewerToolbar = that._viewer.getToolbar(true);
			    var settingsTools = viewerToolbar.getControl(Autodesk.Viewing.TOOLBAR.SETTINGSTOOLSID);
			    viewerToolbar.removeControl(settingsTools);
				var navTools = viewerToolbar.getControl(Autodesk.Viewing.TOOLBAR.NAVTOOLSID);
				//navTools.removeControl("toolbar-cameraSubmenuTool");
				navTools.removeControl("toolbar-zoomTool");
				
			    var modelTools = viewerToolbar.getControl(Autodesk.Viewing.TOOLBAR.MODELTOOLSID);
				modelTools.removeControl("toolbar-explodeTool");
			}
		});
	
		that._viewer.setBackgroundColor(48, 153, 225, 255,255, 255);
		that._viewer.setGhosting(false);
		
		that._viewer.unloadExtension('Autodesk.ADN.Viewing.Extension.SampleTaskStatus'); 
		that._viewer.loadExtension('Autodesk.ADN.Viewing.Extension.SampleTaskStatus');
		that._viewer.createSamplePanel(that._curUnitId,that._curMajor,that._isWholeModel);
		that._viewer.addEventListener(Autodesk.Viewing.SELECTION_CHANGED_EVENT, that.onSelectedCallback);
		
	},
	onSelectedCallback:function (event) {
		var that = this;
		var msg = "";
		
		if (event.dbIdArray.length > 0) {
			_shiijindu.getpbproperty(event.dbIdArray[0]);
		} 
	},
	
	transViewCustom:function (){
		var that = this;
		var newCamPos = new THREE.Vector3(-149715.3552195181,-119243.66328031197,34681.408770079055);
		var target = new THREE.Vector3(0,0,0);
		var cam=that._viewer.navigation.getCamera();
		that._viewer.navigation.setRequestTransition(true,newCamPos,target,cam.fov);
	},
	
	
	getColorByStr:function (strColor) {
		var that = this;
		var color = null;
		if(strColor != undefined && strColor.length == 7) {
			var r = (parseFloat(parseInt(strColor.substr(1, 2), 16) / 255).toFixed(2));
			var g = (parseFloat(parseInt(strColor.substr(3, 2), 16) / 255).toFixed(2));
			var b = (parseFloat(parseInt(strColor.substr(5, 2), 16) / 255).toFixed(2));
	
			color = new THREE.Vector4(r, g, b, 0.5); // r, g, b, intensity
		}
		return color;
	},
	
	setChildThemingColor:function (root,color) {
		var that = this;
		var it = that._viewer.model.getData().instanceTree;
		
		if(it!=undefined){
				it.enumNodeChildren(root, function(dbId) {
				that._viewer.setThemingColor(dbId, color);
			}, true);
		}
	
	},
	
	getpbproperty:function (dbId){
		var that = this;
		$.ajax({
		  type:"get",
		  url:"/task/modelview/getpbproperty/",
		  cache:false,
		  dataType:"json",
		  data:{"dbId": dbId,"_curUnitId": that._curUnitId,"_curMajor": that._curMajor,},
		  success: function(data){
			if(data.issuc=="true")
			{
				$("#pbnumber").text(data.pbnumber);
				$("#pbstatusinfo").text(data.pbstatus+"    "+data.curstatuspercent+"%");
				
				var traceurl="/task/goujian/trace_front/?pbid="+data.pbid;
				$("#pbtraceframe").attr("src",traceurl);
			}
			else
			{
				$("#pbnumber").text("无构件信息");	
				$("#pbstatusinfo").text("");
				$("#pbtraceframe").attr("src","");
			}
	
		  }
		});
	},
	
	getpbstatuslist:function () {
		var that = this;
		$.ajax({
			type: "get",
			url: "/task/modelview/getpbstatuslist/",
			cache: false,
			dataType: "json",
			data: {
				"_selElevations": that._selElevations,
				"_selPbtypes": that._selPbtypes,
				"_curUnitId": that._curUnitId,
				"_selZones": that._selZones,
				"_curMajor": that._curMajor,
				"_isWholeModel": that._isWholeModel,
			},
			success: function(data) {
				if(data.issuc = "true") {
					for(var each in data.pbstatuslist) {
						var color = that.getColorByStr(data.pbstatuslist[each].color);
						for(var eachpb in data.pbstatuslist[each].pblist) {
							that._viewer.setThemingColor(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid), color);
							
							//todo 特殊处理 pgb
							//if(_curMajor==2)
							{
								that.setChildThemingColor(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid), color);
							}
							
						}
					}
				}
			}
		});
	},
	
	 filterPblist:function () {
	 	var that = this;
	  	$.ajax({
	  		type: "get",
	  		url: "/task/modelview/filterPblist/",
	  		cache: false,
	  		dataType: "json",
	  		data: {
	  			"_selElevations": that._selElevations,
	  			"_selPbtypes": that._selPbtypes,
	  			"_curUnitId": that._curUnitId,
	  			"_selZones": that._selZones,
	  			"_curMajor": that._curMajor,
	  		},
	  		success: function(data) {
	
	  			that._viewer.clearThemingColors();
	
	  			//HideAllModelsObject();
					var dbids=[];
	  			for(var each in data.pblist) {
	  				dbids.push(parseInt(data.pblist[each].lvmdbid));
	  				//_viewer.show(parseInt(data.pblist[each].lvmdbid));
	  			}
	  			that._viewer.isolateById(dbids);
	  			that.getpbstatuslist();
	  		}
	  	});
	 },
	 
	
	
	// called when HTML page is finished loading, trigger loading of default model into viewer
	loadInitialModel:function () {
		var that = this;
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
					that._curUnitId = data.unitid;
					that._curMajor = data.majorid;
					that._isWholeModel = data.iswhole
	
					Autodesk.Viewing.Initializer(options, function() {
						that.loadDocument(options.document); // load first entry by default
					});
				}
				
			}
		});
	},
	
	getModelFile:function () {
		var that = this;
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
					that._isWholeModel = data.iswhole
					that._curUnitId = data.unitid;
					that._curMajor = data.majorid;
					
					that.loadDocument("http://"+window.location.host+data.modelfile); // load first entry by default
				} else {
					alert("没有对应单位工程专业模型！");
				}
			}
		});
	},
	
}


var _jihuajindu = {
	_viewer: null,// the viewer
	_savedGlobalCamera:null,
	_loadedDocument:null,
	
	_isWholeModel:false,
	_curUnitId:"",
	_curMajor: "",
	_selElevations:"",
	_selZones:"",
	_selPbtypes:"",
	
	
	// initialize the viewer into the HTML placeholder
	initializeViewer:function () {
		var that = this;
		if(that._viewer !== null) {
			//_viewer.uninitialize();
			that._viewer.finish();
			that._viewer = null;
			that._savedGlobalCamera = null;
			that._savedViewerStates = [];
		} else {
			//initOverlays(); // set up the Overlays one time
		}
	
		//var viewerElement = document.getElementById("viewer");  // placeholder in HTML to stick the viewer
		//_viewer = new Autodesk.Viewing.Private.GuiViewer3D(viewerElement, {});
		that._viewer = new Autodesk.Viewing.Private.GuiViewer3D($(".viewer")[1], {}); // With toolbar
	
		var retCode = that._viewer.initialize();
		if(retCode !== 0) {
			alert("ERROR: Couldn't initialize viewer!");
			console.log("ERROR Code: " + retCode); // TBD: do real error handling here
		}
	
	},
	
	// load a specific document into the intialized viewer
	loadDocument:function (urnStr) {
		var that = this;
		that._loadedDocument = null; // reset to null if reloading
	
		if(!urnStr || (0 === urnStr.length)) {
			alert("You must specify a URN!");
			return;
		}
	
		that.initializeViewer();
	
		var fullUrnStr = urnStr;
	
		that._viewer.load(fullUrnStr);
	
		that._viewer.addEventListener(Autodesk.Viewing.GEOMETRY_LOADED_EVENT, function(e) {
			if(that._viewer.model) {
				that.transViewCustom();
				//if (_curMajor==2)
				{
					that._viewer.setSelectionMode(Autodesk.Viewing.SelectionMode.FIRST_OBJECT);
				}
	
				that._viewer.getObjectTree(function(objTree) {
					that.getpbstatuslist();
				});
				setTimeout (function () {   that._viewer.autocam.setCurrentViewAsHome();}, 1000) ;
				
				//toolbar custom -------------[pgb]
			    var viewerToolbar = that._viewer.getToolbar(true);
			    var settingsTools = viewerToolbar.getControl(Autodesk.Viewing.TOOLBAR.SETTINGSTOOLSID);
			    viewerToolbar.removeControl(settingsTools);
				var navTools = viewerToolbar.getControl(Autodesk.Viewing.TOOLBAR.NAVTOOLSID);
				//navTools.removeControl("toolbar-cameraSubmenuTool");
				navTools.removeControl("toolbar-zoomTool");
				
			    var modelTools = viewerToolbar.getControl(Autodesk.Viewing.TOOLBAR.MODELTOOLSID);
				modelTools.removeControl("toolbar-explodeTool");
			}
		});
	
		that._viewer.setBackgroundColor(48, 153, 225, 255,255, 255);
		that._viewer.setGhosting(false);
		
		that._viewer.loadExtension('Autodesk.ADN.Viewing.Extension.SampleTaskGoal');
	},
	
	transViewCustom:function (){
		var that = this;
		var newCamPos = new THREE.Vector3(-149715.3552195181,-119243.66328031197,34681.408770079055);
		var target = new THREE.Vector3(0,0,0);
		var cam=that._viewer.navigation.getCamera();
		that._viewer.navigation.setRequestTransition(true,newCamPos,target,cam.fov);
	},
	
	
	getColorByStr:function (strColor) {
		var that = this;
		var color = null;
		if(strColor != undefined && strColor.length == 7) {
			var r = (parseFloat(parseInt(strColor.substr(1, 2), 16) / 255).toFixed(2));
			var g = (parseFloat(parseInt(strColor.substr(3, 2), 16) / 255).toFixed(2));
			var b = (parseFloat(parseInt(strColor.substr(5, 2), 16) / 255).toFixed(2));
	
			color = new THREE.Vector4(r, g, b, 0.5); // r, g, b, intensity
		}
		return color;
	},
	
	setChildThemingColor:function (root,color) {
		var that = this;
		var it = that._viewer.model.getData().instanceTree;
		
		if(it!=undefined){
				it.enumNodeChildren(root, function(dbId) {
				that._viewer.setThemingColor(dbId, color);
			}, true);
		}
	
	},
	
	getColorByStr:function(strColor) {
		var color = null;
		if(strColor != undefined && strColor.length == 7) {
			var r = (parseFloat(parseInt(strColor.substr(1, 2), 16) / 255).toFixed(2));
			var g = (parseFloat(parseInt(strColor.substr(3, 2), 16) / 255).toFixed(2));
			var b = (parseFloat(parseInt(strColor.substr(5, 2), 16) / 255).toFixed(2));
	
			color = new THREE.Vector4(r, g, b, 0.8); // r, g, b, intensity
		}
		return color;
	},
	
	getpbstatuslist:function () {
		var that = this;
		var goal = $("#build-goal").val();
	
		if(!goal){
			return;
		}
		
		var mapStatus={
			"weiwancheng":"#3A84C3",
			"wancheng":"#50C13A",
		}
		$.ajax({
		  type:"get",
		  url:"/task/projecttask/getgoalstatus/",
		  cache:false,
		  dataType:"json",
		  data:{"curUnitId": that._curUnitId,"curMajor": that._curMajor,"goal": goal},
		  success: function(data){
			if(data.issuc=="true")
			{
				that._viewer.clearThemingColors();
				
				for(var each in data.pbstatuslist){ 
					for(var eachpb in data.pbstatuslist[each].pblist){
			
						var color = that.getColorByStr(mapStatus[data.pbstatuslist[each].name]);
						
						that._viewer.setThemingColor(parseInt(data.pbstatuslist[each].pblist[eachpb]), color);
						
						//todo 特殊处理 pgb
						//if(_curMajor==2)
						{
							that.setChildThemingColor(parseInt(data.pbstatuslist[each].pblist[eachpb]), color);
						}
							
					}
				}
			}
			else
			{
				alert(data.error);
			}
		  }
		});
	},
	
	 filterPblist:function () {
	 	var that = this;
	  	$.ajax({
	  		type: "get",
	  		url: "/task/modelview/filterPblist/",
	  		cache: false,
	  		dataType: "json",
	  		data: {
	  			"_selElevations": that._selElevations,
	  			"_selPbtypes": that._selPbtypes,
	  			"_curUnitId": that._curUnitId,
	  			"_selZones": that._selZones,
	  			"_curMajor": that._curMajor,
	  		},
	  		success: function(data) {
	
	  			that._viewer.clearThemingColors();
	
	  			//HideAllModelsObject();
					var dbids=[];
	  			for(var each in data.pblist) {
	  				dbids.push(parseInt(data.pblist[each].lvmdbid));
	  				//_viewer.show(parseInt(data.pblist[each].lvmdbid));
	  			}
	  			that._viewer.isolateById(dbids);
	  			that.getpbstatuslist();
	  		}
	  	});
	 },
	 
	
	
	// called when HTML page is finished loading, trigger loading of default model into viewer
	loadInitialModel:function () {
		var that = this;
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
					that._curUnitId = data.unitid;
					that._curMajor = data.majorid;
					that._isWholeModel = data.iswhole
	
					Autodesk.Viewing.Initializer(options, function() {
						that.loadDocument(options.document); // load first entry by default
					});
				}
				
			}
		});
	},
	
	getModelFile:function () {
		var that = this;
		var defaultunitId = $("#selUnitproject2 option:selected").val();
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
					that._isWholeModel = data.iswhole
					that._curUnitId = data.unitid;
					that._curMajor = data.majorid;
					
					that.loadDocument("http://"+window.location.host+data.modelfile); // load first entry by default
				} else {
					alert("没有对应单位工程专业模型！");
				}
			}
		});
	},
	
}
