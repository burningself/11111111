// LoadModel.js
var _viewer = null;     // the viewer

var selElevations="";
var selPbtypes="";
var _lastSelectDbid=0;


// initialize the viewer into the HTML placeholder
function initializeViewer() {
    
    if (_viewer !== null) {
        //_viewer.uninitialize();
        _viewer.finish();
        _viewer = null;
    }

    //var viewerElement = document.getElementById("viewer");  // placeholder in HTML to stick the viewer
    //_viewer = new Autodesk.Viewing.Private.GuiViewer3D(viewerElement, {});
   _viewer =new Autodesk.Viewing.Private.GuiViewer3D ($("#viewer") [0], {}) ; // With toolbar
   
    var retCode = _viewer.initialize();
    if (retCode !== 0) {
        alert("ERROR: Couldn't initialize viewer!");
        console.log("ERROR Code: " + retCode);      // TBD: do real error handling here
    }
    
}




// load a specific document into the intialized viewer
function loadDocument(urnStr) {
    
	 selElevations="";
	 selPbtypes="";
	
    if (!urnStr || (0 === urnStr.length)) {
        alert("You must specify a URN!");
        return;
    }
	
	initializeViewer();
	
    var fullUrnStr =  urnStr;
    
    _viewer.load(fullUrnStr);

	_viewer.addEventListener(Autodesk.Viewing.GEOMETRY_LOADED_EVENT, function(e) {
		if (_viewer.model) {
			
			customViewer();
			
			_viewer.getObjectTree(function(objTree) {
				getpbstatuslist();
			});
			
			
			
	 }
	});
	_viewer.navigation.toPerspective();
	_viewer.addEventListener(Autodesk.Viewing.SELECTION_CHANGED_EVENT, onSelectedCallback);
	_viewer.setGhosting(true); 

}

var selIndex=false;
function onSelectedCallback(event) {

	if(!selIndex){
		
		selIndex = true;
	}else{
		selIndex=false;
		_viewer.removeEventListener(Autodesk.Viewing.SELECTION_CHANGED_EVENT, onSelectedCallback);
		_viewer.select(_selectedId);
		_viewer.addEventListener(Autodesk.Viewing.SELECTION_CHANGED_EVENT, onSelectedCallback);
		return;
	}

	if(event.dbIdArray.length > 0) {
		_selectedId = event.dbIdArray[0];
		console.log(_selectedId);
		getpbproperty(_selectedId);

	} else {
		_selectedId = null;
	}
	
	return false;
}


	
var _panel = null;
function setpbproperty(data){
	if(_panel==null){
					Autodesk.ADN.AdnPanel = function(
					parentContainer,
					id,
					title,
					options) {
					Autodesk.Viewing.UI.PropertyPanel.call(
						this,
						parentContainer,
						id, title);
					};
			
					Autodesk.ADN.AdnPanel.prototype = Object.create(
						Autodesk.Viewing.UI.PropertyPanel.prototype);
			
					Autodesk.ADN.AdnPanel.prototype.constructor =
						Autodesk.ADN.AdnPanel;
			
					_panel = new Autodesk.ADN.AdnPanel(
						_viewer.container,
						'AdnPropStockPanelId',
						"构件属性");
				}
				
				var properties = [];
				var tmp1 = {"displayCategory":"构件属性","displayName":"编号","displayValue":data.pbnumber};
				properties.push(tmp1);
				var tmp2 = {"displayCategory":"构件属性","displayName":"类型","displayValue":data.pbtype};
				properties.push(tmp2);
				var tmp3 = {"displayCategory":"构件属性","displayName":"状态","displayValue":data.pbstatus};
				properties.push(tmp3);
				var tmp4 = {"displayCategory":"构件属性","displayName":"累计完成百分比 ","displayValue":data.curstatuspercent+"%"};
				properties.push(tmp4);
				var tmp5 = {"displayCategory":"构件属性","displayName":"空间","displayValue":data.pbelevation};
				properties.push(tmp5);
				for(var ex in data.extern){
					tmp5 = {"displayCategory":"构件属性","displayName":data.extern[ex].key,"displayValue":data.extern[ex].value};
					properties.push(tmp5);
				}
				
				tmp5 = {"displayCategory":"项目属性","displayName":"建设单位","displayValue":data.constrator};
				properties.push(tmp5);
				tmp5 = {"displayCategory":"项目属性","displayName":"施工单位","displayValue":data.builder};
				properties.push(tmp5);
				tmp5 = {"displayCategory":"项目属性","displayName":"项目经理","displayValue":data.manager};
				properties.push(tmp5);
				
				_panel.setProperties(properties);
				if(!_panel.isVisible()) {
					_panel.setVisible(true);
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
				setpbproperty(data);
			} else {
				alert("无构件信息！");
			}

		}
	});
}


var _pbDbidList = [];
function getpbstatuslist(){
	$.ajax({
	  type:"get",
	  url:"/task/modelview/getpbstatuslist/",
	  cache:false,
	  dataType:"json",
	  data:{"_curUnitId": _curUnitId,"_curMajor": _curMajor,},
	  success: function(data){
		if(data.issuc="true")
		{
			_pbDbidList = [];
			for(var each in data.pbstatuslist){ 
			
				for(var eachpb in data.pbstatuslist[each].pblist){
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
			}
			//_viewer.isolate(_pbDbidList);
		}
	  }
	});
}


function LoadAllCustomTrees(){
	
}
