// LoadModel.js
var _viewer = null;     // the viewer
var _savedGlobalCamera = null;
var _loadedDocument = null;

var _curUnitId="";
var _isWholeModel = false;
var _curUnitId = "";
var _curMajor = "";
var	_selElevations="";
var	_selZones="";
var	_selPbtypes="";

// initialize the viewer into the HTML placeholder
function initializeViewer() {
    
    if (_viewer !== null) {
        //_viewer.uninitialize();
        _viewer.finish();
        _viewer = null;
        _savedGlobalCamera = null;
        _savedViewerStates = [];
    }

    var viewerElement = document.getElementById("viewer");  // placeholder in HTML to stick the viewer
    _viewer = new Autodesk.Viewing.Private.GuiViewer3D(viewerElement, {});
   //_viewer =new Autodesk.Viewing.Private.GuiViewer3D ($("#viewer") [0], {}) ; // With toolbar
   
    var retCode = _viewer.initialize();
    if (retCode !== 0) {
        alert("ERROR: Couldn't initialize viewer!");
        console.log("ERROR Code: " + retCode);      // TBD: do real error handling here
    }
    _viewer.loadExtension('Autodesk.ADN.Viewing.Extension.SampleTaskGoal');   //显示属性页 !!!!!!
}


// load a specific document into the intialized viewer
function loadDocument(urnStr) {
    
    _loadedDocument = null; // reset to null if reloading
	
	 selElevations="";
	 selPbtypes="";
	
    if (!urnStr || (0 === urnStr.length)) {
        alert("没有对应模型文件!");
        return;
    }
	
	initializeViewer();
	
	
    var fullUrnStr =  urnStr;
    
    _viewer.load(fullUrnStr);

	_viewer.addEventListener(Autodesk.Viewing.GEOMETRY_LOADED_EVENT, function(e) {
		

			customViewer();

	
	   	  _viewer.getObjectTree(function(objTree) {
				getpbstatuslist();
			});
			
	});
	
	_viewer.addEventListener(Autodesk.Viewing.SELECTION_CHANGED_EVENT, onSelectedCallback);
	_viewer.setGhosting(false); 
	//getDbid2ElementId();
}

function onSelectedCallback(event) {
	// display a message if an element is selected
	var msg = "";
	
	if (event.dbIdArray.length > 0) {
		//getpbproperty(event.dbIdArray[0]);
		
	} 
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
	  			"_selZones": _selZones,
	  			"_curMajor": _curMajor,
	  		},
	  		success: function(data) {
	
	  			_viewer.clearThemingColors();
	
	  			//HideAllModelsObject();
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


var mapStatus={
	"weiwancheng":"#3A84C3",
	"wancheng":"#50C13A",
}

function getpbstatuslist(){
	
	var goal = $("#build-goal").val();
	
	if(!goal){
		return;
	}
	
	$.ajax({
	  type:"get",
	  url:"/task/projecttask/getgoalstatus/",
	  cache:false,
	  dataType:"json",
	  data:{"curUnitId": _curUnitId,"curMajor": _curMajor,"goal": goal},
	  success: function(data){
		if(data.issuc=="true")
		{
			_viewer.clearThemingColors();
			
			for(var each in data.pbstatuslist){ 
				for(var eachpb in data.pbstatuslist[each].pblist){
		
					var color = getColorByStr(mapStatus[data.pbstatuslist[each].name]);
					
					_viewer.setThemingColor(parseInt(data.pbstatuslist[each].pblist[eachpb]), color);
					
					//todo 特殊处理 pgb
					//if(_curMajor==2)
					{
						setChildThemingColor(parseInt(data.pbstatuslist[each].pblist[eachpb]), color);
					}
						
				}
			}
			
			Drawpbstatuslist(data);
		}
		else
		{
			alert(data.error);
		}
	  }
	});
}


function Drawpbstatuslist(data){
	var total = data.listcount;
	var rate_wancheng = (parseFloat( data.wancheng.value / total )*100).toFixed(2);
    var rate_weiwancheng = (parseFloat( data.weiwancheng.value / total )*100).toFixed(2);
	
	var colors = [];
	for(var key in mapStatus){ 
		 colors.push(mapStatus[key]) ;
	} 

	
	var plotdata= [	{label: '目标未完成比例', data: rate_weiwancheng }, 
				{label: '完成比例', data: rate_wancheng }
			  ] ;

          
    $.plot($("#item-donut"), plotdata, {  
         series: {  
                pie: {   
                      show: true //显示饼图  
                 }  
            },  
            legend: {  
                   show: false //不显示图例  
            } ,
				colors: colors,
     });  

	 
	 var progressdsc = "";
	 progressdsc +="目标总计需要完成构件数量："+total+"<br>";
	 if(total>0)
	 {
	 	progressdsc +="<span style='color:"+mapStatus["wancheng"]+";'><div style='width:150px;float:left'>完成数量："+data.wancheng.value+"</div>占比："+rate_wancheng+"%</span><br>";
	 	progressdsc +="<span style='color:"+mapStatus["weiwancheng"]+";'><div style='width:150px;float:left'>未完成数量："+data.weiwancheng.value+"</div>占比："+rate_weiwancheng+"%</span><br>";
	 }

	 $("#progressdsc").html(progressdsc);
}


