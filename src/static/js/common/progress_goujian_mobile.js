var _filterCode = "构件";
var _tapId = '#statusTabGoujian';
var _totalpage = 99999;
var _yanshouSelectFilterKey="yanshouSelectFilter";

 function getSelectFilter() {
  	var SelectFilter = localStorage.getItem(_yanshouSelectFilterKey);
  	if(SelectFilter) {
  		//_selElevations = valueSelElevations;
  		console.log(SelectFilter);
		var mapSelectFilter =  JSON.parse(SelectFilter);
		var unitPro = $(_tapId + " .unitProject").val(mapSelectFilter.unitPro);
		loadElevation();
		var pbmajor = $(_tapId + " .pbmajor").val(mapSelectFilter.pbmajor);
		getstatuslist();
		var pbelevation =mapSelectFilter.pbelevation;
		for(var each in pbelevation){
			//$(_tapId + " .pbelevation").val();
			 //$(_tapId + " .pbelevation").find("option[val='"+pbelevation[each]+"']").attr("selected",true);
			 $(_tapId + " .pbelevation").find("option").each(function(){
					if($(this).val()==pbelevation[each]){
						$(this).attr("selected",true);
						return;
					}
			  });
		}


		var pbstatus = mapSelectFilter.pbstatus;
		for(var each in pbstatus){
			//$(_tapId + " .pbstatus").val(pbstatus[each]);
			$(_tapId + " .pbstatus").find("option").each(function(){
					if($(this).val()==pbstatus[each]){
						$(this).attr("selected",true);
						return;
					}
			  });
		}
  	}

  }
  
 function saveSelectFilter() {
 	var SelectFilter = {};
  	var unitPro = $(_tapId + " .unitProject").children('option:selected').val();
  	SelectFilter.unitPro = unitPro;
	var pbmajor = $(_tapId + " .pbmajor").children('option:selected').val();
	SelectFilter.pbmajor = pbmajor;
	var pbelevation = [];
	 $(_tapId + " .pbelevation option:selected").each(function(){
			pbelevation.push($(this).val());
	});
	SelectFilter.pbelevation = pbelevation;
	var pbstatus = [];
	$(_tapId + " .pbstatus option:selected").each(function(){
			pbstatus.push($(this).val());
	});
	SelectFilter.pbstatus = pbstatus;
  	localStorage.setItem(_yanshouSelectFilterKey, JSON.stringify(SelectFilter));
 }


$().ready(function() {
	
	initSwiper();
	
	getSelectFilter();
	
	loadTableData('构件', 1, "00");
	initOption();
});

var topSwiper = new Object;

function initSwiper() {

	topSwiper = new Swiper('.swiper-container-topnav', {
		slidesPerView: 'auto',
		spaceBetween: 0,
		speed: 500,
		grabCursor: true,
		freeMode: true,
	});

}

function loadTableData(filterCode, page, querytype) {

	_filterCode = filterCode;
	if(1 == page) {
		_totalpage = 99999;
		$("#pageNo").val(1);
	}

	if(page > _totalpage) {
		return;
	}

 	$.showLoading();

	if(filterCode == '分区') {
		_tapId = '#statusTabFenqu';
	} else if(filterCode == '构件') {
		_tapId = '#statusTabGoujian';
	} else if(filterCode == '安全设施') {
		_tapId = '#statusTabSheshi';
	} else if(filterCode == '施工机械') {
		_tapId = '#statusTabJixie';
	} else if(filterCode == '任务') {
		_tapId = '#statusTabRenwu';
	} else {

	}

	var unitPro = $(_tapId + " .unitProject").children('option:selected').val();
	var pbmajor = $(_tapId + " .pbmajor").children('option:selected').val();
	var pbelevation = [];
	 $(_tapId + " .pbelevation option:selected").each(function(){
			pbelevation.push($(this).val());
	});
	var pbstatus = [];
	$(_tapId + " .pbstatus option:selected").each(function(){
			pbstatus.push($(this).val());
	});
	
	
		$.ajax({
		type: "POST",
		url: "/progress/goujian/loadCount/",
		cache: false,
		dataType: "json",
		data: {
			"filterCode": filterCode,
			"unitProject": unitPro,
			"pbelevation":JSON.stringify(pbelevation),
			"pbmajor": pbmajor,
			"pbstatus": JSON.stringify(pbstatus),
		},
		success: function(data) {
			if(data.status == 1) {
					var tmpStr = "";
					for(var each in data.countinfolist) {
						tmpStr += '<li class="list-group-item">'+data.countinfolist[each]+'</li>';
					}

	
					$(_tapId + " .countlist").html(tmpStr);

			} else {
				alert(data.error);
			}
		}
	})
	
	$.ajax({
		type: "POST",
		url: "/progress/goujian/loadTable/",
		cache: false,
		dataType: "json",
		data: {
			"filterCode": filterCode,
			"unitProject": unitPro,
			"pbelevation":JSON.stringify(pbelevation),
			"pbmajor": pbmajor,
			"pbstatus": JSON.stringify(pbstatus),
			"page": page
		},
		success: function(data) {
			if(data.status == 1) {
				for(mainIndex in data.titles) {
						var traceurl = "#";
						if(filterCode == '分区') {
							//traceurl='/task/goujian/trace/?pbid=' + data.list_items[mainIndex][eachBody].id;
						} else if(filterCode == '构件') {
							traceurl = '/task/goujian/trace/';
						} else if(filterCode == '安全设施') {
							//traceurl='/task/goujian/trace/?pbid=' + data.list_items[mainIndex][eachBody].id;
						} else if(filterCode == '施工机械') {
							//traceurl='/task/goujian/trace/?pbid=' + data.list_items[mainIndex][eachBody].id;
						} else if(filterCode == '任务') {
							//traceurl='/task/goujian/trace/?pbid=' + data.list_items[mainIndex][eachBody].id;
						} else {
					
						}
		
					$($(_tapId + " .title_row h3 i")[mainIndex]).html(data.titles[mainIndex]);
					var tmpStr = "";
					for(eachHead in data.list_items_head[mainIndex]) {
						tmpStr += "<th>" + data.list_items_head[mainIndex][eachHead] + "</th>";
					}

					$($(_tapId + " .goujian_table thead tr")[mainIndex]).html(tmpStr);

					tmpStr = "";
					for(eachBody in data.list_items[mainIndex]) {
						tmpStr += "<tr>";
						for(eachProp in data.list_items_head[mainIndex]) {
							if(eachProp == 0) {
								tmpStr += "<td><a href='" + traceurl + "?pbid=" + data.list_items[mainIndex][eachBody].id+"'>" + data.list_items[mainIndex][eachBody][data.list_items_head[mainIndex][eachProp]] + "<a></td>";
							} else {
								tmpStr += "<td>" + data.list_items[mainIndex][eachBody][data.list_items_head[mainIndex][eachProp]] + "</td>";
							}
						}
						tmpStr += "</tr>";

					}

					if(querytype == "00") {
						_totalpage = data.list_items_totalpage[mainIndex]
						$($(_tapId + " .goujian_table tbody")[mainIndex]).html(tmpStr);
					} else {
						$($(_tapId + " .goujian_table tbody")[mainIndex]).append(tmpStr);
					}

				}
			} else {
				alert(data.error);
			}
			loading = true;
			 $.hideLoading();
		}
	});
	

	
}

function initOption()
{
//	$(_tapId + " .unitProject").change(function() {
//		loadTableData(_filterCode, 1, "00");
//
//		var unitPro = $(_tapId + " .unitProject").children('option:selected').val();
//		$.ajax({
//			type: "POST",
//			url: "/progress/goujian/loadElevation/",
//			cache: false,
//			dataType: "json",
//			data: {
//				"unitProject": unitPro
//			},
//			success: function(data) {
//				tmpStr = '<option value="0" selected>全部</option>';
//				for(each in data.elevationList) {
//					tmpStr += '<option value="' + data.elevationList[each].id.toString() + '">' + data.elevationList[each].name + '</option>';
//				}
//				$(_tapId +" .pbelevation").html(tmpStr);
//			}
//		})
//	});
//
//	$(_tapId + " .pbelevation").change(function() {
//			loadTableData(_filterCode, 1, "00");
//	});
//	
//	$(_tapId + " .pbmajor").change(function() {
//			loadTableData(_filterCode, 1, "00");
//	});	
}

function loadElevation(){
	var unitPro = $(_tapId + " .unitProject").children('option:selected').val();
	$.ajax({
			type: "POST",
			url: "/progress/goujian/loadElevation/",
			cache: false,
			dataType: "json",
			data: {
				"unitProject": unitPro
			},
			success: function(data) {
				var tmpStr = '';
				for(each in data.elevationList) {
					tmpStr += '<option value="' + data.elevationList[each].id.toString() + '">' + data.elevationList[each].name + '</option>';
				}
				$(_tapId +" .pbelevation").html(tmpStr);
			}
	})
}

function unitPrjChange(){
	saveSelectFilter();
	loadTableData(_filterCode, 1, "00");

	loadElevation();
}

function pbelevationChange(){
	saveSelectFilter();
	loadTableData(_filterCode, 1, "00");
}

function getstatuslist(){
		
	var _curMajor = $(_tapId + " .pbmajor").children('option:selected').val();
	
	$.ajax({
  		type: "get",
  		url: "/task/modelview/getstatuslist",
  		cache: false,
  		dataType: "json",
  		data: {
  			"_curMajor": _curMajor,
  		},
  		success: function(data) {
  				var tmpStr = '';
				for(each in data.statuslist) {
					tmpStr += '<option value="' + data.statuslist[each].id + '">' + data.statuslist[each].name + '</option>';
				}
				$(_tapId +" .pbstatus").html(tmpStr);
  		}
  	});
}
function pbmajorChange(){
	saveSelectFilter();
	loadTableData(_filterCode, 1, "00");
	
	getstatuslist();
}

function pbstatusChange(){
	saveSelectFilter();
	loadTableData(_filterCode, 1, "00");
}

function loadTableDataMore() {}

var loading = false;
Zepto(function($) {
	$(window).scroll(function() {
		if(($(window).scrollTop() + $(window).height() > $(document).height() - 10) && loading) {

			loading = false;
			var page = parseInt($("#pageNo").val()) + 1;
			$("#pageNo").val(page);
			loadTableData(_filterCode, page, "01");
		}
	});
})