function intVue() {
	_app = new Vue({
		el: "#app",
		delimiters: ["[[", "]]"],
		data: {
			loading: true,
			columnsPb: [{
				title: '构件编号',
				key: 'pbnumber',
				sortkey: 'precastbeam__number',
				sortable: 'custom'
			}, 
			{
				title: '构件状态',
				key: 'statusname',
				sortkey: 'status',
				sortable: 'custom'
			}
			, {
				title: '验收人员',
				key: 'actorname',
				sortkey: 'actor',
				sortable: 'custom'
			}
			, {
				title: '验收时间',
				key: 'time',
				sortkey: 'time',
				sortable: 'custom'
			}, {
				title: '单位工程',
				key: 'unitprojectname',
				sortkey: 'precastbeam__elevation__unitproject',
				sortable: 'custom'
			}, {
				title: '标高',
				key: 'elevationname',
				sortkey: 'precastbeam__elevation',
				sortable: 'custom'
			}, {
				title: '专业',
				key: 'majorname',
				sortkey: 'precastbeam__pbtype__major',
				sortable: 'custom'
			}, {
				title: '构件类型',
				key: 'pbtypename',
				sortkey: 'precastbeam__pbtype',
				sortable: 'custom'
			}, {
				title: '操作',
				key: 'action',
				width: 90,
				align: 'center',
				render: (h, params) => {
					return h('div', [
						h('Button', {
							props: {
								type: 'error',
								size: 'small'
							},
							on: {
								click: () => {
									_app.PbTrace(_app.dataPb[params.index].precastbeam_id)
								}
							}
						}, '追踪')
					]);
				}
			}],
			dataPb: [],

			//分页参数
			total: 0,
			page: 1,
			perPage: 15, //每页数量

			daterange:null,
			search: null,
			pbtype: null,
			pbtype__major: null,
			elevation: null,
			elevation__unitproject: null,
			curstatus: null,
			ordering:'-time',

			spaceData: [],
			spacevalue: [],
			typeData: [],
			typevalue: [],
			tableheight: 500
		},
		methods: {
			init: function() {

				var that = this;

				that.tableheight = document.body.clientHeight - 265;

				that.loadUnitProject();

				that.loadMajor();

				that.loadList(1);

			},
			loadList: function(page) {
				var that = this;
				that.page = page;
				that.loading = true;
				
				var time__gte="";
				var time__lte="";
				if(that.daterange && that.daterange[0]!=null && that.daterange[0]!=""){
					time__gte=that.daterange[0].format("yyyy-MM-dd 00:00:00")
					time__lte=that.daterange[1].format("yyyy-MM-dd 23:59:59")
				}

				$.ajax({
					url: "/task/pbstatusrecords/",
					type: "get",
					data: {
						"page": page,
						"perPage": that.perPage,
						"precastbeam__pbtype__major": that.pbtype__major,
						"precastbeam__pbtype": that.pbtype,
						"precastbeam__elevation": that.elevation,
						"precastbeam__elevation__unitproject": that.elevation__unitproject,
						"status": that.curstatus,
						"search":that.search,
						"time__gte":time__gte,
						"time__lte":time__lte,
						"ordering":that.ordering,
					},
					dataType: "json",
					error: function() {
						alert('请求列表失败')
					},
					success: function(res) {
						that.dataPb = res.results;
						that.pageAll = Math.ceil(res.count / that.perPage); //计算总页数
						that.total = res.count;

						that.loading = false;
					}
					
				});
			},
			sortPb(orderobj){
				console.log(orderobj);
				if(orderobj.order=="desc"){
					this.ordering = "-"+orderobj.column.sortkey;
				}else{
					this.ordering = orderobj.column.sortkey;
				}
				this.loadList(1);
			},
			handleSubmit() {
				this.elevation__unitproject = null;
				this.elevation = null;
				this.pbtype__major = null;
				this.pbtype = null;
				this.curstatus = null;

				if(this.spacevalue.length > 0) {
					this.elevation__unitproject = this.spacevalue[0];
				}
				if(this.spacevalue.length > 1) {
					this.elevation = this.spacevalue[1];
				}

				if(this.typevalue.length > 0) {
					this.pbtype__major = this.typevalue[0];
				}
				if(this.typevalue.length > 1) {
					this.pbtype = this.typevalue[1];
				}
				if(this.typevalue.length > 2) {
					this.curstatus = this.typevalue[2];
				}

				this.loadList(1);
			},
			loadUnitProject() {
				var that = this;
				$.ajax({
					url: "/task/unitprojects/",
					type: "get",
					data: {
						"page": 1,
						"perPage": 9999
					},
					dataType: "json",
					error: function() {
						alert('请求列表失败')
					},
					success: function(res) {

						var unitfilters = [];
						for(var each in res.results) {
							var tmp = {};
							tmp.label = res.results[each].name;
							tmp.value = res.results[each].id;
							tmp.children = [];
							tmp.loading = false;
							unitfilters.push(tmp);
						}

						that.spaceData = unitfilters;
					}
				});
			},
			loadElevation(item, callback) {
				var that = this;
				console.log(item);
				item.loading = true;
				$.ajax({
					url: "/task/elevations/",
					type: "get",
					data: {
						"page": 1,
						"perPage": 9999,
						"unitproject": item.value
					},
					dataType: "json",
					error: function() {
						alert('请求列表失败');
						item.loading = false;
					},
					success: function(res) {

						var filters = [];
						for(var each in res.results) {
							var tmp = {};
							tmp.label = res.results[each].name;
							tmp.value = res.results[each].id;
							filters.push(tmp);
						}

						item.children = filters;
						item.loading = false;
						callback();
					}
				});
			},
			loadMajor() {
				var that = this;
				$.ajax({
					url: "/user/majors/",
					type: "get",
					data: {
						"page": 1,
						"perPage": 9999
					},
					dataType: "json",
					error: function() {
						alert('请求列表失败');
					},
					success: function(res) {

						var filters = [];
						for(var each in res.results) {
							var tmp = {};
							tmp.label = res.results[each].name;
							tmp.value = res.results[each].id;
							tmp.type = "major";
							tmp.children = [];
							tmp.loading = false;
							filters.push(tmp);
						}

						that.typeData = filters;
					}
				});
			},
			loadSubType(item, callback) {
				var that = this;
				item.loading = true;

				if(item.type == "major") {
					$.ajax({
						url: "/task/pbtypes/",
						type: "get",
						data: {
							"page": 1,
							"perPage": 9999,
							"major": item.value
						},
						dataType: "json",
						error: function() {
							alert('请求列表失败');
							item.loading = false;
						},
						success: function(res) {

							var filters = [];
							for(var each in res.results) {
								var tmp = {};
								tmp.label = res.results[each].name;
								tmp.value = res.results[each].id;
								tmp.type = "pbtype";
								tmp.children = [];
								tmp.loading = false;
								filters.push(tmp);
							}

							item.children = filters;
							item.loading = false;
							callback();
						}
					});
				} else {
					$.ajax({
						url: "/task/pbstatuss/",
						type: "get",
						data: {
							"page": 1,
							"perPage": 9999,
							"pbtype": item.value
						},
						dataType: "json",
						error: function() {
							alert('请求列表失败');
							item.loading = false;
						},
						success: function(res) {

							var filters = [];
							for(var each in res.results) {
								var tmp = {};
								tmp.label = res.results[each].statusname;
								tmp.value = res.results[each].id;
								filters.push(tmp);
							}

							item.children = filters;
							item.loading = false;
							callback();
						}
					});
				}

				
			},
			PbTrace(pbid){
				window.open("/task/goujian/trace/?pbid="+pbid); 
			}

		},
	})
}

! function() {
	intVue();
	_app.init();
}();

var myTimer;

function ExportReport() {
	$("#exportpgbar").attr("style", "width: 0%;");
	$("#exportpgbar").text("");

	var xmlhttp;
	if(window.XMLHttpRequest) { // code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp = new XMLHttpRequest();
	} else { // code for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function() {
		if(xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			var result = xmlhttp.responseText;
			if(result == "error")
				alert(result);
			else {
				$("#reporturl").attr("href", result);
				myTimer = setInterval(function() {
					TimerFun()
				}, 1000);
				$('#exportdlg').modal('show');
			}
		}
	}
	xmlhttp.open("GET", "/task/exportreport/", true);
	xmlhttp.send();
}

function TimerFun() {
	var xmlhttp;
	if(window.XMLHttpRequest) { // code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp = new XMLHttpRequest();
	} else { // code for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function() {
		if(xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			var result = xmlhttp.responseText;
			var results = result.split(",");
			if(results[0] == "suc") {
				$("#exportpgbar").attr("style", "width: " + results[1] + "%;");
				$("#exportpgbar").text("完成" + results[1] + "%");
				if(results[1] == "100") {
					var btn = document.getElementById("btnDownload");
					btn.disabled = false;
					StopTimerFun();
				}
			} else {
				$("#exportpgbar").attr("style", "width: 100%;");
				$("#exportpgbar").text("生成报表失败！");
				StopTimerFun();
			}
		} else {

		}
	}
	xmlhttp.open("GET", "/task/getexportpro/", true);
	xmlhttp.send();
}

function StopTimerFun() {
	window.clearInterval(myTimer);
}

function downloadreport() {
	var lnk = document.getElementById("reporturl");
	lnk.click();
	var btn = document.getElementById("btnDownload");
	btn.disabled = true;
}

function DialogUploadFile() {
	//var dlgResult = window.showModalDialog("/task/precastbeam/import/", window, "dialogWidth:480px; dialogHeight:240px; status:0");
	if(window.ActiveXObject) { //IE  
		var dlgResult = window.showModalDialog("/task/precastbeam/import/" + id, window, "dialogWidth:480px; dialogHeight:240px; status:0");
	} else { //非IE  
		window.open("/task/precastbeam/import/" + id, 'newwindow', 'width=480,height=240,toolbar=no,menubar=no,scrollbars=no, resizable=no,location=no, status=no');
	}
}