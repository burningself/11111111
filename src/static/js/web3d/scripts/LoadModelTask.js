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
	
var _selectedId = null;

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
    _viewer.loadExtension('Autodesk.ADN.Viewing.Extension.SampleTask');   //显示属性页 !!!!!!
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
		
		if (_viewer.model) {
			customViewer();
		
		 	_viewer.getObjectTree(function(objTree) {
				getpbstatuslist();
			});

		 }
	
	  
	});
	
	_viewer.addEventListener(Autodesk.Viewing.SELECTION_CHANGED_EVENT, onSelectedCallback);
	_viewer.setGhosting(false); 
	//getDbid2ElementId();
}


function onSelectedCallback(event) {
	// display a message if an element is selected
	var msg = "";
	
	if (event.dbIdArray.length > 0) {
		_selectedId = event.dbIdArray[0];
		getpbproperty(_selectedId);
	} 
}

function getpbproperty(dbId){
	$.ajax({
	  type:"get",
	  url:"/task/modelview/getpbproperty/",
	  cache:false,
	  dataType:"json",
	  data:{"dbId": dbId,"_curUnitId": _curUnitId,"_curMajor": _curMajor,},
	  success: function(data){
		if(data.issuc=="true")
		{
			$("#pbnumber").text(data.pbnumber);
			$("#pbtask").text(data.task);
			$("#pbstatus").text(data.pbstatus);
			$("#statuspercent").text(data.curstatuspercent+"%");
			$("#plantime").text(data.plantime);
			$("#realtime").text(data.realtime);
			
			//var traceurl='/task/goujian/trace/?pbid='+data.pbid;
			
			var traceurl="javascript:TracePbStatus("+data.pbid+");";
			
			$("#pbtrace").attr('href',traceurl); 
		}
		else
		{
			$("#pbnumber").text("无构件信息");	
			$("#plantime").text("");
			$("#pbtask").text("")
			$("#pbstatus").text("");
			$("#realtime").text("");
			$("#pbqrcode").attr('href','#');
			$("#pbtrace").attr('href','#'); 
		}

	  }
	});
}




var mapStatus={
	"weikaishi":"#F9B1F5",
	"jinxingzhong":"#3A84C3",
	"wancheng":"#50C13A",
	"chaoshiweiwancheng":"#D4C327",
	"chaoshiweikaishi":"#C43A3A"
}

function getpbstatuslist(){
	
	var timerange=$("#timerange").val();
	$.ajax({
	  type:"get",
	  url:"/task/projecttask/getstatus/",
	  cache:false,
	  dataType:"json",
	  data:{"curUnitId": _curUnitId,"curMajor": _curMajor,"timerange": timerange},
	  success: function(data){
		if(data.issuc=="true")
		{
			_viewer.clearThemingColors();
			
			for(var each in data.pbstatuslist){ 
				for(var eachpb in data.pbstatuslist[each].pblist){
		
					var color = getColorByStr(mapStatus[data.pbstatuslist[each].name]);
					
					_viewer.setThemingColor(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid), color);
					//todo 特殊处理 pgb
					//if(_curMajor==2)
					{
						setChildThemingColor(parseInt(data.pbstatuslist[each].pblist[eachpb].lvmdbid), color);
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

function Drawpbstatuslist(data){
	var total = data.listcount;
	var rate_weikaishi = (parseFloat( data.weikaishi.value / total )*100).toFixed(2) ;
    var rate_jinxingzhong = (parseFloat( data.jinxingzhong.value / total )*100).toFixed(2) ;
    var rate_wancheng= (parseFloat( data.wancheng.value / total )*100).toFixed(2) ;
    var rate_chaoshiweiwancheng = (parseFloat( data.chaoshiweiwancheng.value / total )*100).toFixed(2) ;
    var rate_chaoshiweikaishi = (parseFloat( data.chaoshiweikaishi.value / total )*100).toFixed(2) ;

	var colors = [];
	for(var key in mapStatus){ 
		 colors.push(mapStatus[key]) ;
	} 

	
	
	var plotdata= [
				{label: '未开始', data: rate_weikaishi },
				{label: '进行中', data: rate_jinxingzhong },
				{label: '完成', data: rate_wancheng },
				{label: '超时未完成', data: rate_chaoshiweiwancheng },
				{label: '超时未开始', data: rate_chaoshiweikaishi },
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
	 progressdsc +="总计需要完成构件数量："+total+"<br>";
	 if(total>0)
	 {
	 	progressdsc +="<span style='color:"+mapStatus["weikaishi"]+";'><div style='width:150px;float:left'>未开始："+data.weikaishi.value+"</div>占比："+rate_weikaishi+"%</span><br>";
		progressdsc +="<span style='color:"+mapStatus["jinxingzhong"]+";'><div style='width:150px;float:left'>进行中："+data.jinxingzhong.value+"</div>占比："+rate_jinxingzhong+"%</span><br>";
		progressdsc +="<span style='color:"+mapStatus["wancheng"]+";'><div style='width:150px;float:left'>完成："+data.wancheng.value+"</div>占比："+rate_wancheng+"%</span><br>";
		progressdsc +="<span style='color:"+mapStatus["chaoshiweiwancheng"]+";'><div style='width:150px;float:left'>超时未完成："+data.chaoshiweiwancheng.value+"</div>占比："+rate_chaoshiweiwancheng+"%</span><br>";
		progressdsc +="<span style='color:"+mapStatus["chaoshiweikaishi"]+";'><div style='width:150px;float:left'>超时未开始："+data.chaoshiweikaishi.value+"</div>占比："+rate_chaoshiweikaishi+"%</span><br>";
	 }

	 $("#progressdsc").html(progressdsc);
}


