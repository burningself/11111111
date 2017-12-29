var mouse_key = 0; //鼠标点击，1：左键，2：右键
document.onmousedown = function(e) {
    e = e || window.event;
    var btn = e.button + 1 || e.which;
    if (btn == 1) {
        mouse_key = 1;
    } else if (btn == 2) {
        mouse_key = 1;
    } else if (btn == 3) {
        mouse_key = 2;
    }
}

var _app = new Vue({
    delimiters: ['[[', ']]'],
    el: "#app",
    data: {
        taizhangData: {
            list: [],
            reportlist: []
        },
        show_taizhang: 1,
        curr_jstree: null,
        curr_slectnode: null,
        curr_type: 'maint',
        curr_space_id: '', //工程ID
        list: ['111'],
        totalData: {
            list:[],
            namelist: [],
            tds: []
        },
        export_json: '',
        sourceoptions: [{
                id: 1,
                text: '自行'
            },
            {
                id: 2,
                text: '分包'
            }
        ],
        search_form: {
            start_time: '',
            end_time: '',
            space: '',
            major: '',
            company: '',
            zxorfb: ''
        },
        ratelist: [{
                num: '1',
                name: 'xxxx',
                sum_money: 222
            },
            {
                num: '1',
                name: 'xxxx',
                sum_money: 222
            }
        ]

    },
    mounted: function() {
        
        var that = this;

        that.list.push('222');
        console.log(that.list);
        that.curr_jstree = that.jstreeInit();
        $("#jstree_demo_div").bind("activate_node.jstree", function(obj, e) {
            if (mouse_key != 1)
                return;
            var selectedid = e.node.id;
            that.curr_slectnode = selectedid;
            var tt = that.curr_slectnode.split('-');
            if (tt[0] == 'space') {
                that.show_taizhang = 1;
                that.curr_type = tt[0];
                that.curr_space_id = tt[1];
                that.manageraccount('total');
            } else if (tt[0] == 'zixingyg' || tt[0] == 'fenbaoyg') {
                console.log('获取报表');
                that.show_taizhang = 0;
                that.getaccountData(tt[2]);
            } else if (tt[0] == 'maint') {
                that.show_taizhang = 1;
                that.curr_space_id = '';
                that.curr_type = 'maint';
                console.log("执行模拟点击");
                $("#chome").click();
                that.manageraccount('total');
            }
        });


        that.listenerinit();

        that.manageraccount('total');
    },
    methods: {
        showblurrate: function(data) {
            // alert('触摸了我');

            console.log(data)
            var that = this;
            if (data) {
                that.ratelist = [];
                that.ratelist = data;
            }

            $("#rateDialog").modal("show");
        },

        listenerinit: function() {
            $("#start_time").bind("click", function() {
                $('#start_time').datetimepicker({
                    language: 'zh-CN', //显示中文
                    autoclose: true, //选中自动关闭
                    format: "yyyy-mm", //日期格式
                    startView: 3,
                    minView: "year", //设置只显示到月份
                }).on('changeDate', function(ev) {
                    var time = $("#start_time").val();
                    if (time != that.search_form.start_time) {
                        that.search_form.start_time = time;
                        that.manageraccount('zidingyitz');
                    }
                });
            });
            $("#start_time").click();

            $("#end_time").bind("click", function() {
                $('#end_time').datetimepicker({
                    language: 'zh-CN', //显示中文
                    autoclose: true, //选中自动关闭
                    format: "yyyy-mm", //日期格式
                    startView: 3,
                    minView: "year", //设置只显示到月份
                });
            }).on('changeDate', function(ev) {
                var time = $("#end_time").val();
                if (time != that.search_form.end_time) {
                    that.search_form.end_time = time;
                    that.manageraccount('zidingyitz');
                }
            });
            $("#end_time").click();

            $("#fenbao-select").selectpicker({ title: '分包筛选' });
            
            $("#major-select").selectpicker({ title: '专业筛选' });
            $("#company-select").selectpicker({ title: '单位筛选' });
            $("#space-select").selectpicker({ title: '空间筛选' });
        },
        timeformat: function(time) {
            var st = new Date(time * 1000);
            var y = st.getFullYear();
            var m = st.getMonth() + 1;
            return y + '年' + m + '月'
        },
        searchf_change: function(type) {
            var that = this;
            that.manageraccount('zidingyitz');
            console.log(that.search_form);
        },
        manageraccount: function(type) {
            var that = this;
            console.log(that.totalData.list);
            that.totalData.list.length = 0;
            that.totalData.tds.length = 0;
            var options = {}
            if (type == 'zidingyitz') {
                that.listenerinit();
                options = {
                    space: that.search_form.space == '' ? that.search_form.space : that.search_form.space.join(','),
                    company: that.search_form.company == '' ? that.search_form.company : that.search_form.company.join(','),
                    major: that.search_form.major == '' ? that.search_form.major : that.search_form.major.join(','),
                    zxorfb: that.search_form.zxorfb == '' ? that.search_form.zxorfb : that.search_form.zxorfb.join(','),
                    start_time: that.search_form.start_time,
                    end_time: that.search_form.end_time,
                }
            }
            options.type = type;
            options.space_id = that.curr_space_id;

            $.ajax({
                type: 'get',
                dataType: 'json',
                data: options,
                url: '/business/manageraccount/',
                success: function(data) {
                    if (data.issuc) {
                        console.log(data.rnames);
                        that.totalData.list = data.rnames;
                        that.totalData.tds = data.tds;
                        that.$nextTick(function() {
                            that.exportJsonData(2, type);
                        });

                    }
                },
                error: function(data) {

                }
            });
        },
        exportJsonData: function(type, tabletype) {
            //type 值为2,3，表示2号或者3号台账
            var that = this;
            var list = [];
            if (type == 2) {
                var tbrows = [];
                if (tabletype == 'total') {
                    export_tableid = 'table-taizhang';
                    export_name = '总产值台账';
                } else if (tabletype == 'zixing') {
                    export_tableid = 'profile-taizhang';
                    export_name = '自行产值台账';
                } else if (tabletype == 'fenbao') {
                    export_tableid = 'messages-taizhang';
                    export_name = '分包产值台账';
                } else if (tabletype == 'company') {
                    export_tableid = 'settings-taizhang';
                    export_name = '单位工程汇总台账';
                } else if (tabletype == 'fenbaocompany') {
                    export_tableid = 'fenbaodanwei-taizhang';
                    export_name = '分包单位台账';
                } else if (tabletype == 'zhuanye') {
                    export_tableid = 'fenzhuanye-taizhang';
                    export_name = '分专业台账';
                } else if (tabletype == 'zidingyitz') {
                    export_tableid = 'zidingyitz-taizhang';
                    export_name = '自定义台账';
                }
            } else if (type == 3) {
                export_tableid = 'threeetaizhang';
                console.log(that.curr_slectnode);
                var node = $('#jstree_demo_div').jstree("get_node", that.curr_slectnode);
                export_name = node.text;
            }
            // console.log(list);
        },
        getaccountData: function(pact_id) {
            var that = this;
            $.ajax({
                type: 'get',
                dataType: 'json',
                data: { pact_id: pact_id },
                url: '/business/loadAccountList/',
                success: function(data) {
                    if (data.issuc) {
                        that.taizhangData.list = data.datalist;
                        that.taizhangData.reportlist = data.reportlist;
                        that.$nextTick(function() {
                            that.exportJsonData(3);
                        });
                    }
                },
                error: function(data) {

                }
            });
        },

        jstreeInit: function() {
            return $('#jstree_demo_div').jstree({
                'core': {
                    'data': {
                        'url': '/business/get_account_tree/',
                        'data': function(node) {
                            return { 'id': node.id };
                        }
                    }
                },
                "plugins": [
                    "wholerow", "themes", "json_data", "contextmenu"
                ],
                "contextmenu": {
                    "items": function(node) {
                        var temp = {
                            "deletereport": {
                                "label": "删除",
                                "icon": "fa fa-times",
                                // "separator_after": true,
                                "action": function(data) {
                                    alertConfirm("确定删除 " + node.text + " 吗?", null, function() {
                                        var report_id = (node.id).replace('report', '');
                                        $.ajax({
                                            type: 'get',
                                            dataType: 'json',
                                            url: '/business/delReport/',
                                            data: { report_id: report_id },
                                            success: function(data) {
                                                if (data.issuc) {
                                                    alert("删除成功", null, function() {
                                                        window.location.reload();
                                                    });
                                                } else {
                                                    alert(data.msg);
                                                }
                                            },
                                            error: function(data) {
                                                alert("系统异常");
                                            }
                                        });
                                    });
                                }
                            },
                        };
                        /**
                         * 如果选择不是所想节点，则不出右键菜单项
                         */
                        var menu = {};
                        if ((node.id).indexOf("report") >= 0) {
                            return temp;
                        } else {
                            return menu;
                        }
                    },
                    "select_node": false
                },
            });
        },
    }
});