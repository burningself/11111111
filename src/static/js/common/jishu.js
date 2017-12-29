var IssueRelateFileDocIds = [];
var relatetype;

$(function() {

	$('#createtTimerange').daterangepicker({
		ranges: {
			'今天': [moment(), moment()],
			'昨天': [moment().subtract('days', 1), moment().subtract('days', 1)],
			'最近7天': [moment().subtract('days', 6), moment()],
			'最近30天': [moment().subtract('days', 29), moment()],
			'本月': [moment().startOf('month'), moment().endOf('month')],
			'上个月': [moment().subtract('month', 1).startOf('month'), moment().subtract('month', 1).endOf('month')]
		},
		locale: {
			applyLabel: '确定',
			cancelLabel: '取消',
			fromLabel: '起始时间',
			toLabel: '结束时间',
			customRangeLabel: '自定义',
			daysOfWeek: ['日', '一', '二', '三', '四', '五', '六'],
			monthNames: ['一月', '二月', '三月', '四月', '五月', '六月',
				'七月', '八月', '九月', '十月', '十一月', '十二月'
			],
			firstDay: 1
		},
	});

});

var flag = 1;


function FunAddBiaoDan() {

	$('#addbiaodan').modal('show');
};


function FunFaqizhiliangDlg() {
	g_CurOprType = "发起问题";
	$("#addbiaodan").html("点击增加表单");
	$('#faqizhiliangdlg').modal('show');
	flag = 1;
	$.ajax({
		type: "get",
		url: "/task/issue/createconfig/",
		cache: false,
		dataType: "json",
		data: {
			"issuetype": "{{issuetype}}",
		},
		success: function(data) {
			if(data.issuc = "true") {} else {

			}

		}
	});

};



function CreatHuiYi() {

}
var biaodantype;
var biaodan_btn;
function zhenggaiDlg(ty,obj) {
	//		$('#biaodan').modal('show');
	var deadline = $("#deadline").val();
	if(!deadline){
		alert("请先选择截止时间！");
		return;
	}
	
	var stepParam = "";
	if(_stepid&&_stepid!="undefined"){
		stepParam = "&step="+_stepid;
	}
	
	flag = 1;
	biaodan_btn = obj;
	$("#biaodanback").css("display", "inline-block");
	addTableSuc();
	var exp = new Date();
	biaodantype = ty + exp.getTime();
//	if(ty == 'zlwt') {
////		window.open('/assist/issue/biaodan1?biaodantype=' + biaodantype, 'newwindow')
		window.open('/assist/biaodanedit/?mbId='+ty+'&biaodantype=' + biaodantype+'&glys='+encodeURI(encodeURI(JSON.stringify(selectedGJs)))+"&kj="+selectedKJ+stepParam
							+'&rijidate='+deadline,Date.parse(new Date()))
//	} else {
//		window.open('/assist/biaodanedit/?mbId=42&biaodantype=' + biaodantype, 'newwindow')
//	}

};


function shigongrijiDlg(ty,obj) {
	var builddiary_date = $("#builddiary_date").val();
	if(!builddiary_date){
		alert("请先选择日记日期！");
		return;
	}
	
	flag = 1;
	biaodan_btn = obj;
	$("#biaodanback").css("display", "inline-block");
	addTableSuc();
	var exp = new Date();
	biaodantype = ty + exp.getTime();

	window.open('/assist/biaodanedit/?mbId='+ty+'&biaodantype=' + biaodantype+'&rijidate='+builddiary_date,Date.parse(new Date()))

};

function chakanBbiaodan(bdid){
	var stepParam = "";
	if(typeof _stepid!="undefined"&&_stepid){
		stepParam = "&step="+_stepid;
	}
	window.open('/assist/biaodanedit/?bdid=' + bdid+stepParam, Date.parse(new Date()))
}


function yanshoudanDlg(obj) {
	//		$('#biaodan').modal('show');
	biaodan_btn = obj;
	flag = 1;
	$("#biaodanback").css("display", "inline-block");
	addTableSuc();
	var exp = new Date();
	biaodantype = "zlysd" + exp.getTime();
	window.open('/task/issue/biaodan4?biaodantype=' + biaodantype, Date.parse(new Date()))
};



var bdid=null;
function addTableSuc() {
	var obj = new TipBox({
		type: 'load',
		str: "正在操作表格..",
		hasBtn: true,
		setTime: 500,
		callBack: function() {
			var cval = getCookie(biaodantype);
			if(cval) {
				bdid = getCookie('bdid');
				delCookie('bdid');
				delCookie(biaodantype);
				new TipBox({
					type: 'success',
					str: '操作成功',
					hasBtn: true
				});
				var fun = "chakanBbiaodan(" + bdid + ")"
				$(biaodan_btn).attr('onclick',fun);
				$(biaodan_btn).html("查看表单");
				$("#biaodanback").css("display", "none");

			} else {
				if(flag == 0) {
					$("#addbiaodan").html("点击增加表单");
					$("#biaodanback").css("display", "none");
					obj.destroy();
				} else {
					addTableSuc();
				}

			}
		}
	});
}

function getCookie(name) {

	var arr, reg = new RegExp("(^| )" + name+"=([^;]*)(;|$)");
	if(arr = document.cookie.match(reg))
		return unescape(arr[2]);
	else
		return null;
}

function delCookie(name) {
	var exp = new Date();
	exp.setTime(exp.getTime() - 1000);
	document.cookie = name + "=succ" + "';path=/;expires=" + exp.toGMTString();

}

function RelateTypeChange() {
	$("#RelateElement").val(null).trigger("change");;
	$("#RelateElement:selected").remove();
	$("#RelateElement").empty();
	//var relatetype = $("input[name=optionsRadiosRelateType]:checked").val();
	//
	//$.ajax({
	//  type:"get",
	//  url:"/task/issue/getrelatetype/",
	//  cache:false,
	//  dataType:"json",
	//  data:{"relatetype":relatetype,},
	//  success: function(data){
	//	if(data.issuc="true")
	//	{
	//		for(var each in data.RelateElementList){
	//			$("#RelateElement").append("<option value=" + data.RelateElementList[each].biaodantype + ">" + data.RelateElementList[each].name+ "</option>");
	//		}
	//	}
	//	else
	//	{
	//		
	//	}
	//
	//  }
	//});
};




$(function() {
	function initTableCheckbox() {
		var $thr = $('table-checkbox thead tr');
		var $checkAllTh = $('<th><input type="checkbox" id="checkAll" name="checkAll" /></th>');
		/*将全选/反选复选框添加到表头最前，即增加一列*/
		$thr.prepend($checkAllTh);
		/*“全选/反选”复选框*/
		var $checkAll = $thr.find('input');
		$checkAll.click(function(event) {
			/*将所有行的选中状态设成全选框的选中状态*/
			$tbr.find('input').prop('checked', $(this).prop('checked'));
			/*并调整所有选中行的CSS样式*/
			if($(this).prop('checked')) {
				$tbr.find('input').parent().parent().addClass('warning');
			} else {
				$tbr.find('input').parent().parent().removeClass('warning');
			}
			/*阻止向上冒泡，以防再次触发点击操作*/
			event.stopPropagation();
		});
		/*点击全选框所在单元格时也触发全选框的点击操作*/
		$checkAllTh.click(function() {
			$(this).find('input').click();
		});
		var $tbr = $('.table-checkbox tbody tr');
		var $checkItemTd = $('<td><input type="checkbox" name="checkItem" /></td>');
		/*每一行都在最前面插入一个选中复选框的单元格*/
		$tbr.prepend($checkItemTd);
		/*点击每一行的选中复选框时*/
		$tbr.find('input').click(function(event) {
			/*调整选中行的CSS样式*/
			$(this).parent().parent().toggleClass('warning');
			/*如果已经被选中行的行数等于表格的数据行数，将全选框设为选中状态，否则设为未选中状态*/
			$checkAll.prop('checked', $tbr.find('input:checked').length == $tbr.length ? true : false);
			/*阻止向上冒泡，以防再次触发点击操作*/
			event.stopPropagation();
		});
		/*点击每一行时也触发该行的选中操作*/
		$tbr.click(function() {
			$(this).find('input').click();
		});
	}
	initTableCheckbox();
});



