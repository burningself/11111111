var gxyanshoudoc=[]
$(function() {


});

function funGxyanshou(objId){
	//		$("#qdescribe").val('');
	//		$(".icon-jfi-trash").click();//清空附件
	//		$("#qid").val(objId);
	//		$("#gxyanshoudlg").modal('show');
	window.open("/task/projecttask/lurujindu/?gxid="+objId);
}

function delete_confirm(id){
		var res = confirm("删除是不可恢复的，您确认要删除吗？");
		if(res){
			$.ajax({
			type: "delete",
			url: "/task/acceptance/opt/"+id,
			cache: false,
			dataType: "json",
			data: JSON.stringify({'delid':id}),
			success: function(data) {
				if(data.res == "succ") {
//						var r = confirm("删除成功！");
					window.location.reload(true);
				} else {
//						var r = confirm(data.error);
					window.location.reload(true);
				}
			}
		});
		}
	}
	function guanbi_confirm(id){
		var res = confirm("确认要关闭吗？");
		if(res){
			$.ajax({
			type: "post",
			url: "/task/acceptance/opt/"+id,
			cache: false,
			dataType: "json",
			data: JSON.stringify({'id':id}),
			success: function(data) {
				if(data.res == "succ") {
//						var r = confirm("删除成功！");
					window.location.reload(true);
				} else {
					var r = confirm(data.error);

				}
			}
		});
		}
	}

$('#deadlineTimerange').daterangepicker({
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


function gxshou(){

	var jsonobj = $('#gxyanshouForm').serializeJSON();
	jsonobj.docs= JSON.stringify(gxyanshoudoc)
	$.ajax({
		type: "post",
		url: "/task/zhiliangyanshou/gongxu/",
		cache: false,
		dataType: "json",
		data: jsonobj,
		success: function(data) {
			if(data.issuc == "true") {

				window.location.reload(true);
			} else {
				alert(data.value);
				$("#gxyanshoudlg").modal('hide');
			}

		}
	});
}