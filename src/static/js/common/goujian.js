function intVue() {
	_app = new Vue({
		el: "#app",
		delimiters: ["[[", "]]"],
		data: {
			loading: true,
			columnsPb: [{
				title: '构件编号',
				key: 'number',
				sortkey: 'number',
				sortable: 'custom'
			}, 
			{
				title: '显示编号',
				key: 'drawnumber',
			}, {
				title: '单位工程',
				key: 'unitprojectname',
				sortkey: 'elevation__unitproject',
				sortable: 'custom'
			}, {
				title: '标高',
				key: 'elevationname',
				sortkey: 'elevation',
				sortable: 'custom'
			}, {
				title: '专业',
				key: 'majorname',
				sortkey: 'pbtype__major',
				sortable: 'custom'
			}, {
				title: '构件类型',
				key: 'pbtypename',
				sortkey: 'pbtype',
				sortable: 'custom'
			}, {
				title: '当前状态',
				key: 'curstatusname',
				sortkey: 'curstatus',
				sortable: 'custom'
			}, {
				title: '操作',
				key: 'action',
				width: 190,
				align: 'center',
				render: (h, params) => {
					return h('div', [
						h('Button', {
							props: {
								type: 'info',
								size: 'small'
							},
							style: {
								marginRight: '5px'
							},
							on: {
								click: () => {
									_app.PbTrace(_app.dataPb[params.index].id)
								}
							}
						}, '追踪'),
						h('Button', {
							props: {
								type: 'error',
								size: 'small'
							},
							on: {
								click: () => {
									_app.PrintPbQrcode(_app.dataPb[params.index].id);
								}
							}
						}, '二维码')
					]);
				}
			}],
			dataPb: [],

			//分页参数
			total: 0,
			page: 1,
			perPage: 15, //每页数量

			search: null,
			pbtype: null,
			pbtype__major: null,
			elevation: null,
			elevation__unitproject: null,
			curstatus: null,
			ordering:null,

			spaceData: [],
			spacevalue: [],
			typeData: [],
			typevalue: [],
			tableheight: 500,
			
			exportloading:true
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

				$.ajax({
					url: "/task/precastbeam/",
					type: "get",
					data: {
						"page": page,
						"perPage": that.perPage,
						"pbtype__major": that.pbtype__major,
						"pbtype": that.pbtype,
						"elevation": that.elevation,
						"elevation__unitproject": that.elevation__unitproject,
						"curstatus": that.curstatus,
						"search":that.search,
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
			PrintPbQrcode() {
				var dwidth = window.screen.width;
				var dheight = window.screen.height;
				if(arguments[0]) {
					var pbid = arguments[0];
					var fullLink = arguments[1];
					if(window.ActiveXObject) { //IE  
						var dlgResult = window.showModalDialog("/task/goujian/qrcode/?pbid=" + pbid + "&full=" + fullLink, window, "dialogWidth:" + dwidth + "px;dialogHeight:" + dheight + "px; status:0");
					} else { //非IE  
						window.open("/task/goujian/qrcode/?pbid=" + pbid + "&full=" + fullLink, 'newwindow', "width=" + dwidth + ",height=" + dheight + ",toolbar=no,menubar=no,scrollbars=no, resizable=no,location=no, status=no");
					}
				} else {

					var pburl = "/task/goujian/qrcode/?number=" + (this.search==null?'':this.search) + "&unitproject=" + (this.elevation__unitproject==null?'':this.elevation__unitproject) + "&pbelevation=" + (this.elevation==null?'':this.elevation )+ "&pbstatus=" + (this.curstatus==null?'':this.curstatus) + "&major=" + (this.pbtype__major==null?'':this.pbtype__major) + "&pbtype=" + (this.pbtype==null?'':this.pbtype);
					if(window.ActiveXObject) { //IE  
						var dlgResult = window.showModalDialog(pburl, window, "dialogWidth:" + dwidth + "px;dialogHeight:" + dheight + "px; status:0");
					} else { //非IE  
						window.open(pburl, 'newwindow', "width=" + dwidth + ",height=" + dheight + ",toolbar=no,menubar=no,scrollbars=no, resizable=no,location=no, status=no");
					}
				}
			},
			PbTrace(pbid){
				window.open("/task/goujian/trace/?pbid="+pbid); 
			},
			exportData(){
				var that=this;
				
				const msg = that.$Message.loading({
                    content: '正在导出构件，请耐心等待...',
                    duration: 0
                });
				
					$.ajax({
					url: "/task/precastbeam/",
					type: "get",
					data: {
						"page": 1,
						"perPage":999999,
						"pbtype__major": that.pbtype__major,
						"pbtype": that.pbtype,
						"elevation": that.elevation,
						"elevation__unitproject": that.elevation__unitproject,
						"curstatus": that.curstatus,
						"search":that.search,
						"ordering":that.ordering,
					},
					dataType: "json",
					error: function() {
						alert('请求列表失败');
						that.$Message.destroy();
					},
					success: function(res) {
						var columnsPb=[{
							title: '构件编号',
							key: 'number',
						}, 
						{
							title: '显示编号',
							key: 'drawnumber',
						}, {
							title: '单位工程',
							key: 'unitprojectname',
						}, {
							title: '标高',
							key: 'elevationname',
						}, {
							title: '专业',
							key: 'majorname',
						}, {
							title: '构件类型',
							key: 'pbtypename',
						}, {
							title: '当前状态',
							key: 'curstatusname',
						}];
						
						 that.$refs.pbtable.exportCsv({
		                    filename: '构件导出',
		                    columns: columnsPb,
		                    data: res.results
		                  });
		                  
		                  that.$Message.destroy();
					}
					
				});
				

			}

		},
	})
}

! function() {
	intVue();
	_app.init();
}();

