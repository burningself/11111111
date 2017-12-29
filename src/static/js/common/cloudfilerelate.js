$(document).ready(function() {
	$(".select2-selection--single").css("margin","0px 2px 0px 2px");
	
	$("#btnLoadFileSelectDlg").click(function()
	{
		$("#relatefiledlg").modal("show");
	});

});

$("#btnSaveFileRelate").click(function()
{
	alert("todo：保存关联关系 by yLost");
});


$("#RelateElement-WBS").select2({
		placeholder: "添加关联WBS",
		language: "zh-CN",
		ajax: {
			url: "/task/issue/getrelatetype/",
			dataType: 'json',
			delay: 400,
			data: function(params) {
				relatetype = '任务';
				return {
					q: params.term, // search term  
					relatetype: relatetype,
					page: params.page
				};
			},
			processResults: function(data, page) {
				// parse the results into the format expected by Select2.  
				// since we are using custom formatting functions we do not need to  
				// alter the remote JSON data  
				//console.debug("ajax返回的对象是:")  
				//console.debug(data.items)  
				return {
					results: data.items
				};
			},
			cache: true
		},
		escapeMarkup: function(markup) {
			//console.debug(markup)  
			return markup;
		}, // let our custom formatter work  
		minimumInputLength: 2, //至少输入多少个字符后才会去调用ajax  
		maximumInputLength: 30, //最多能输入多少个字符后才会去调用ajax  
		minimumResultsForSearch: 1,
	});
	
$("#RelateElement-Kongjian").select2({
		placeholder: "添加关联空间",
		language: "zh-CN",
		ajax: {
			url: "/task/issue/getrelatetype/",
			dataType: 'json',
			delay: 400,
			data: function(params) {
				relatetype = '构件';
				return {
					q: params.term, // search term  
					relatetype: relatetype,
					page: params.page
				};
			},
			processResults: function(data, page) {
				// parse the results into the format expected by Select2.  
				// since we are using custom formatting functions we do not need to  
				// alter the remote JSON data  
				//console.debug("ajax返回的对象是:")  
				//console.debug(data.items)  
				return {
					results: data.items
				};
			},
			cache: true
		},
		escapeMarkup: function(markup) {
			//console.debug(markup)  
			return markup;
		}, // let our custom formatter work  
		minimumInputLength: 2, //至少输入多少个字符后才会去调用ajax  
		maximumInputLength: 30, //最多能输入多少个字符后才会去调用ajax  
		minimumResultsForSearch: 1,
	});
	
$("#RelateElement-FenleiXinxi").select2({
		placeholder: "添加关联分类信息",
		language: "zh-CN",
		ajax: {
			url: "/task/issue/getrelatetype/",
			dataType: 'json',
			delay: 400,
			data: function(params) {
				relatetype = '构件';
				return {
					q: params.term, // search term  
					relatetype: relatetype,
					page: params.page
				};
			},
			processResults: function(data, page) {
				// parse the results into the format expected by Select2.  
				// since we are using custom formatting functions we do not need to  
				// alter the remote JSON data  
				//console.debug("ajax返回的对象是:")  
				//console.debug(data.items)  
				return {
					results: data.items
				};
			},
			cache: true
		},
		escapeMarkup: function(markup) {
			//console.debug(markup)  
			return markup;
		}, // let our custom formatter work  
		minimumInputLength: 2, //至少输入多少个字符后才会去调用ajax  
		maximumInputLength: 30, //最多能输入多少个字符后才会去调用ajax  
		minimumResultsForSearch: 1,
	});
	
$("#RelateElement-prebeam").select2({
		placeholder: "添加关联构件",
		language: "zh-CN",
		ajax: {
			url: "/task/issue/getrelatetype/",
			dataType: 'json',
			delay: 400,
			data: function(params) {
				relatetype = '构件';
				return {
					q: params.term, // search term  
					relatetype: relatetype,
					page: params.page
				};
			},
			processResults: function(data, page) {
				// parse the results into the format expected by Select2.  
				// since we are using custom formatting functions we do not need to  
				// alter the remote JSON data  
				//console.debug("ajax返回的对象是:")  
				//console.debug(data.items)  
				return {
					results: data.items
				};
			},
			cache: true
		},
		escapeMarkup: function(markup) {
			//console.debug(markup)  
			return markup;
		}, // let our custom formatter work  
		minimumInputLength: 2, //至少输入多少个字符后才会去调用ajax  
		maximumInputLength: 30, //最多能输入多少个字符后才会去调用ajax  
		minimumResultsForSearch: 1,
	});
	

$("#RelateElement-WBS").change(function(e)
{
	var text = $(this).children('option:selected').html();
	var RelateId = $(this).children('option:selected').val();
	
	var newRow = "<tr> \
					<td style='width: 75%;' value='"+RelateId+"'>"+text+"</td> \
					<td> <a href='#'  onclick='funDelFileRelate(this)' style='cursor: pointer;'>[删除]</a></td> \
				</tr>";
	$("#table-filerelate-wbs tr:last").after(newRow);
});

$("#RelateElement-prebeam").change(function(e)
{
	var text = $(this).children('option:selected').html();
	var RelateId = $(this).children('option:selected').val();
	
	var newRow = "<tr> \
					<td style='width: 75%;' value='"+RelateId+"'>"+text+"</td> \
					<td> <a href='#'  onclick='funDelFileRelate(this)' style='cursor: pointer;'>[删除]</a></td> \
				</tr>";
	$("#table-filerelate-prebeam tr:last").after(newRow);
});


function funDelFileRelate(obj)
{
	$(obj).parents("tr").remove();
}