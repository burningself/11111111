$(document).ready(function() {
	guanjiandiandiv();
});

function guanjiandiandiv(){
	$.ajax({
		type: "post",
//		url: "/task/issue/getmajortemplate/",
		cache: false,
		dataType: "json",
		data: {
			"type": 'guanjiandian',
			"opt": 'cha',
		},
		success: function(data) {
			if (data.issuc == "true") {
				for(var i in data.data){
					tmp = '<tr class="info">';
					tmp += 	'<td>';
					tmp +=	data.data[i].id;
					tmp +=	'</td>';
					tmp +=	'<td>';
					tmp +=		data.data[i].typename;
					tmp +=	'</td>';
					tmp +=	'<td>';
					tmp +=		data.data[i].formname;
					tmp +=	'</td>';
					tmp +=	'<td>';
					tmp +=		data.data[i].major;
					tmp +=	'</td>';
					tmp +=	'<td>';
					tmp +=	'<a href="#" onclick="delone(this)">[删除]</a>';
					tmp +=	'</td>';
					tmp +='</tr>';
					$('#guanjiandiantbody').append(tmp);
				}
				
			} else {
				alert(data.error);
			}

		}
	});
}

function addnew(){
	tmp = '<tr class="info">';
	tmp += 	'<td>';
	tmp +=	'</td>';
	tmp +=	'<td>'
	tmp +=		'<input type="text" required="required" maxlength="64" class="form-control" id="name" placeholder="请输入名称">'
	tmp +=	'</td>';
	tmp +=	'<td>';
	tmp +=		$("#allbdmb").html();
	tmp +=	'</td>';
	tmp +=	'<td>';
	tmp +=		$("#allmajor").html();
	tmp +=	'</td>';
	tmp +=	'<td>';
	tmp +=	'<a href="#" onclick="saveone(this)">[保存]</a>';
	tmp +=	'<a href="#" onclick="cancle(this)">[取消]</a>';
	tmp +=	'</td>';
	tmp +='</tr>';
	$('#guanjiandiantbody').append(tmp);
}

function saveone(obj){
	var typename = obj.parentNode.parentNode.children[1].children[0].value;
	var bdmb = obj.parentNode.parentNode.children[2].children[0].value;
	var major = obj.parentNode.parentNode.children[3].children[0].value;
	if(typename=="" || typename==null)
	{
	    alert("类型名称不能为空");
	    return;
	}
	$.ajax({
		type: "post",
//		url: "/task/issue/getmajortemplate/",
		cache: false,
		dataType: "json",
		data: {
			"typename": typename,
			"bdmb":bdmb,
			"opt": 'add',
			'type':'guanjiandian',
			'major':major,
		},
		success: function(data) {
			if (data.issuc == "true") {
				window.location.reload();
			} else {
				alert(data.error);
			}

		}
	})
}

function delone(obj){
	var id = obj.parentNode.parentNode.children[0].textContent;

	$.ajax({
		type: "post",
//		url: "/task/issue/getmajortemplate/",
		cache: false,
		dataType: "json",
		data: {
			"opt": 'del',
			'type':'guanjiandian',
			'id':id,
		},
		success: function(data) {
			if (data.issuc == "true") {
				window.location.reload();
			} else {
				alert(data.error);
			}

		}
	})
}

function cancle(obj){
	obj.parentNode.parentNode.remove();
}
