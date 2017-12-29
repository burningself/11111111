
var _yanshouSelectFilterKey="yanshouSelectFilter";
var _filterCode='';

$().ready(function() {
	
	initSwiper();
	
	loadTableData('', 1, "00");

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


 	$.showLoading();
	_filterCode = filterCode;

	var unitPro = $(".unitProject").children('option:selected').val();
	var pbelevation = $(" .pbelevation").children('option:selected').val();;
	
					
	$.ajax({
		type: "POST",
		url: "/progress/goujian/count_mobile/",
		cache: false,
		dataType: "json",
		data: {
			"filterCode": filterCode,
			"unitProject": unitPro,
			"pbelevation":pbelevation,
		},
		success: function(data) {
			if(data.status == 1) {
					var tmpStr = "";
					for(var each in data.countinfolist) {
						tmpStr += "<tr>"
							for(var row in data.countinfolist[each]) {
								if("单位工程"==data.countinfolist[each][row]){
									tmpStr += `<td>
												 <select class="unitProject"  onchange="unitPrjChange()">`
												$.ajax({
													type: "get",
													url: "/task/unitprojects/?format=json",
													cache: false,
													dataType: "json",
													async: false,
													success: function(unitPros) {
														for(var unitPro in unitPros.results){
															if(unitPros.results[unitPro].id==data.unitProject){
																tmpStr += "<option value="+unitPros.results[unitPro].id+" selected>"+unitPros.results[unitPro].name+"</option>";
															}else{
																tmpStr += "<option value="+unitPros.results[unitPro].id+">"+unitPros.results[unitPro].name+"</option>";
															}
															
														}
													}
												});		
									tmpStr += `</select></td>`;
								}else if("楼层"==data.countinfolist[each][row]){
									tmpStr += `<td>
												 <select class="pbelevation"  onchange="pbelevationChange()">`
													$.ajax({
														type: "POST",
														url: "/progress/goujian/loadElevation/",
														cache: false,
														dataType: "json",
														async: false,
														data: {
															"unitProject": data.unitProject
														},
														success: function(data2) {
															console.log("11111");
															tmpStr += '<option value="0">全部楼层</option>';
															for(var each in data2.elevationList) {
																if(data2.elevationList[each].id==data.pbelevation){
																	tmpStr += '<option value="' + data2.elevationList[each].id.toString() + '" selected>' + data2.elevationList[each].name + '</option>';
																}else{
																	tmpStr += '<option value="' + data2.elevationList[each].id.toString() + '">' + data2.elevationList[each].name + '</option>';
																}
																
															}
														}
												});
												
									tmpStr += `</select></td>`;
								}else{
									tmpStr += "<td>"+data.countinfolist[each][row]+"</td>";
								}
								
							}		
						tmpStr += "</tr>";
					}
					console.log(tmpStr);
					$(".count_table").html(tmpStr);

			} else {
				alert(data.error);
			}
			 $.hideLoading();
		}
	});
	
}

function unitPrjChange(){
	console.log("11111");
	loadTableData(_filterCode, 1, "00");
}

function pbelevationChange(){
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