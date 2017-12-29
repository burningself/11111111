
var bdids = [];

var bdid;
var biaodantype;
var biaodan_btn;
function openuedit(ty,obj) {
	//		$('#biaodan').modal('show');
	flag = 1;
	biaodan_btn = obj;
	$("#biaodanback").css("display", "inline-block");
	addTableSuc();
	var exp = new Date();
	biaodantype = ty + exp.getTime();
//	if(ty == 'zlwt') {
////		window.open('/assist/issue/biaodan1?biaodantype=' + biaodantype, 'newwindow')
		window.open('/assist/biaodanedit/?mbId='+ty+'&biaodantype=' + biaodantype,
			Date.parse(new Date()))
//	} else {
//		window.open('/assist/biaodanedit/?mbId=42&biaodantype=' + biaodantype, 'newwindow')
//	}

};

function setBiaodanIds(bdid){
	$("#relatebdids").val(JSON.stringify(bdids));
}

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
				bdids.push(bdid)
				delCookie('bdid');
				delCookie(biaodantype);
				new TipBox({
					type: 'success',
					str: '操作成功',
					hasBtn: true
				});
				var fun = "chakanBbiaodan(" + bdid + ")"
				setBiaodanIds();
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

function chakanBbiaodan(bdid){
	window.open('/assist/biaodanedit/?bdid=' + bdid, Date.parse(new Date()))
}