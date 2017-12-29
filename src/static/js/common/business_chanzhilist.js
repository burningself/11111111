var mouse_key = 0; //鼠标点击，1：左键，2：右键
var itemtype = 1; //添加行 选项1:清单，2：工料机汇总表，3：费用表， 4：分建成本， 5：劳务成本
var curr_tableid = 'table-bqs'; //当前表格id
var curr_slectnode = null;
var curr_jstree, account_jstree;
var keeplist = new Object();
var tablebqs, tableres,tablerate, tablethound2, tablecos, tablefenjian, tablelaowu;


var datatable_thound2_options = {
    "dom": 'tip',
    "iDisplayLength": 15,
    "lengthChange": false, //是否允许用户自定义显示数量
    "bPaginate": true, //翻页功能
    "bFilter": false, //列筛序功能
    "searching": false, //本地搜索
    "ordering": false, //排序功能
    "Info": true, //页脚信息
    "autoWidth": true, //自动宽度
    "oLanguage": { //国际语言转化
        "oAria": {
            "sSortAscending": " - click/return to sort ascending",
            "sSortDescending": " - click/return to sort descending"
        },
        "sLengthMenu": "显示 _MENU_ 记录",
        "sZeroRecords": "对不起，查询不到任何相关数据",
        "sEmptyTable": "未有相关数据",
        "sLoadingRecords": "正在加载数据-请等待...",
        "sInfo": "当前显示 _START_ 到 _END_ 条，共 _TOTAL_ 条记录。",
        "sInfoEmpty": "当前显示0到0条，共0条记录",
        "sInfoFiltered": "（数据库中共为 _MAX_ 条记录）",
        "sProcessing": "<img src='../resources/user_share/row_details/select2-spinner.gif'/> 正在加载数据...",
        "sSearch": "模糊查询：",
        "sUrl": "",
        //多语言配置文件，可将oLanguage的设置放在一个txt文件中，例：Javascript/datatable/dtCH.txt
        "oPaginate": {
            "sFirst": "首页",
            "sPrevious": " 上一页 ",
            "sNext": " 下一页 ",
            "sLast": " 尾页 "
        }
    },
    "processing": true,
    "serverSide": true,
    //数据来源（包括处理分页，排序，过滤） ，即url，action，接口，等等
    "ajax": {
        "url": '/../../business/getbqtablelist/',
        "type": 'POST',
    },

    "columns": [{
        "data": null
    }, {
        "data": "code"
    }, {
        "data": "name"
    }, {
        "data": "unit"
    }, {
        "data": null
    }, {
        "data": null
    },
    {
        "data": null
    }
    ],
    columnDefs: [ //添加自定义按钮
        {
            targets: 4,
            render: function(a, b, c, d) {
                return (a.amount).toFixed(4);
                // if (a.locked == 1) {
                //     return (a.amount).toFixed(4);
                // } else {
                //     return '<a href="#" class="selfedit-table"  data-url="/business/updateReportResitem/" id="nums" data-type="text" data-pk="' + a.id + '" data-title="数量">' + (a.amount).toFixed(4) + '</a>';
                // }
            }
        },
        {
            targets: 5,
            render: function(a, b, c, d) {
                return (a.unitprice).toFixed(2);
                // if (a.locked == 1) {
                //     return (a.unitprice).toFixed(2);
                // } else {
                //     return '<a href="#" class="selfedit-table"  data-url="/business/updateReportResitem/" id="price" data-type="text" data-pk="' + a.id + '" data-title="单价">' + (a.unitprice).toFixed(2) + '</a>';;
                // }
            }
        },
        {
            targets: 6,
            render: function(a, b, c, d) {
                return (a.amount * a.unitprice).toFixed(2);
            }
        },
    ],
    //向服务器传额外的参数
    "fnServerParams": function(aoData) {
        aoData.param = keeplist;
    },
    "fnDrawCallback": function() {　　
        this.api().column(0).nodes().each(function(cell, i) {　　　　 cell.innerHTML = i + 1;　　 });
        $(".selfedit-table").editable({
            validate: function(value) { //字段验证
                if (!$.trim(value)) {
                    return '不能为空';
                } else {

                }
            },
            success: function() {
                tablethound2.draw();
            }
        });

    },
};
var datatable_rate_options = {
    "dom": 'tip',
    "iDisplayLength": 15,
    "lengthChange": false, //是否允许用户自定义显示数量
    "bPaginate": true, //翻页功能
    "bFilter": false, //列筛序功能
    "searching": false, //本地搜索
    "ordering": false, //排序功能
    "Info": true, //页脚信息
    "autoWidth": true, //自动宽度
    "oLanguage": { //国际语言转化
        "oAria": {
            "sSortAscending": " - click/return to sort ascending",
            "sSortDescending": " - click/return to sort descending"
        },
        "sLengthMenu": "显示 _MENU_ 记录",
        "sZeroRecords": "对不起，查询不到任何相关数据",
        "sEmptyTable": "未有相关数据",
        "sLoadingRecords": "正在加载数据-请等待...",
        "sInfo": "当前显示 _START_ 到 _END_ 条，共 _TOTAL_ 条记录。",
        "sInfoEmpty": "当前显示0到0条，共0条记录",
        "sInfoFiltered": "（数据库中共为 _MAX_ 条记录）",
        "sProcessing": "<img src='../resources/user_share/row_details/select2-spinner.gif'/> 正在加载数据...",
        "sSearch": "模糊查询：",
        "sUrl": "",
        //多语言配置文件，可将oLanguage的设置放在一个txt文件中，例：Javascript/datatable/dtCH.txt
        "oPaginate": {
            "sFirst": "首页",
            "sPrevious": " 上一页 ",
            "sNext": " 下一页 ",
            "sLast": " 尾页 "
        }
    },
    "processing": true,
    "serverSide": true,
    //数据来源（包括处理分页，排序，过滤） ，即url，action，接口，等等
    "ajax": {
        "url": '/../../business/getbqtablelist/',
        "type": 'POST',
    },

    "columns": [{
        "data": "num"
    }, {
        "data": "name"
    }, {
        "data": "rate"
    }, {
        "data": "money"
    }],
    columnDefs: [ //添加自定义按钮

    ],
    //向服务器传额外的参数
    "fnServerParams": function(aoData) {
        aoData.param = keeplist;
    },
    "fnDrawCallback": function() {　

    },
};
var datatable_res_options = {
    "dom": 'tip',
    "iDisplayLength": 15,
    "lengthChange": false, //是否允许用户自定义显示数量
    "bPaginate": true, //翻页功能
    "bFilter": false, //列筛序功能
    "searching": false, //本地搜索
    "ordering": false, //排序功能
    "Info": true, //页脚信息
    "autoWidth": true, //自动宽度
    "oLanguage": { //国际语言转化
        "oAria": {
            "sSortAscending": " - click/return to sort ascending",
            "sSortDescending": " - click/return to sort descending"
        },
        "sLengthMenu": "显示 _MENU_ 记录",
        "sZeroRecords": "对不起，查询不到任何相关数据",
        "sEmptyTable": "未有相关数据",
        "sLoadingRecords": "正在加载数据-请等待...",
        "sInfo": "当前显示 _START_ 到 _END_ 条，共 _TOTAL_ 条记录。",
        "sInfoEmpty": "当前显示0到0条，共0条记录",
        "sInfoFiltered": "（数据库中共为 _MAX_ 条记录）",
        "sProcessing": "<img src='../resources/user_share/row_details/select2-spinner.gif'/> 正在加载数据...",
        "sSearch": "模糊查询：",
        "sUrl": "",
        //多语言配置文件，可将oLanguage的设置放在一个txt文件中，例：Javascript/datatable/dtCH.txt
        "oPaginate": {
            "sFirst": "首页",
            "sPrevious": " 上一页 ",
            "sNext": " 下一页 ",
            "sLast": " 尾页 "
        }
    },
    "processing": true,
    "serverSide": true,
    //数据来源（包括处理分页，排序，过滤） ，即url，action，接口，等等
    "ajax": {
        "url": '/../../business/getbqtablelist/',
        "type": 'POST',
    },

    "columns": [{
        "data": null
    }, {
        "data": "code"
    }, {
        "data": "name"
    }, {
        "data": "unit"
    }, {
        "data": null
    }, {
        "data": null
    }, {
        "data": null
    },
    // {
    //     "data": null
    // },
    ],
    columnDefs: [ //添加自定义按钮
        {
            targets: 4,
            render: function(a, b, c, d) {
                return (a.amount).toFixed(6);
                // if (a.locked == 1) {
                //     return (a.amount).toFixed(4);
                // } else {
                //     return '<a href="#" class="selfedit-table"  data-url="/business/updateReportResitem/" id="nums" data-type="text" data-pk="' + a.id + '" data-title="数量">' + (a.amount).toFixed(4) + '</a>';
                // }
            }
        },
        {
            targets: 5,
            render: function(a, b, c, d) {
                return (a.unitprice).toFixed(2);
                // if (a.locked == 1) {
                //     return (a.unitprice).toFixed(2);
                // } else {
                //     return '<a href="#" class="selfedit-table"  data-url="/business/updateReportResitem/" id="price" data-type="text" data-pk="' + a.id + '" data-title="单价">' + (a.unitprice).toFixed(2) + '</a>';;
                // }
            }
        },
        {
            targets: 6,
            render: function(a, b, c, d) {
                return (a.amount * a.unitprice).toFixed(2);
            }
        },
        // {
        //     targets: 7,
        //     render: function(a, b, c, d) {
        //         var html = '';
        //         if (a.locked == 1) {
        //             html = '<button style="margin-left:2px;margin-right:2px;" type="button" data="' + a.id + '" class="btn btn-danger btn-xs disabled" >删除行</button>';;
        //         } else {
        //             html = '<button style="margin-left:2px;margin-right:2px;" type="button" data="' + a.id + '" class="btn btn-danger btn-xs delurl" >删除行</button>';
        //         }
        //         return html;
        //     }
        // }
    ],
    //向服务器传额外的参数
    "fnServerParams": function(aoData) {
        aoData.param = keeplist;
    },
    "fnDrawCallback": function() {　　
        this.api().column(0).nodes().each(function(cell, i) {　　　　 cell.innerHTML = i + 1;　　 });
        $(".selfedit-table").editable({
            validate: function(value) { //字段验证
                if (!$.trim(value)) {
                    return '不能为空';
                } else {

                }
            },
            success: function() {
                tableres.draw();
            }
        });

    },
};
var datatable_bqs_options = {
    "dom": 'tip',
    "iDisplayLength": 15,
    "lengthChange": false, //是否允许用户自定义显示数量
    "bPaginate": true, //翻页功能
    "bFilter": false, //列筛序功能
    "searching": false, //本地搜索
    "ordering": false, //排序功能
    "Info": true, //页脚信息
    "autoWidth": true, //自动宽度
    "oLanguage": { //国际语言转化
        "oAria": {
            "sSortAscending": " - click/return to sort ascending",
            "sSortDescending": " - click/return to sort descending"
        },
        "sLengthMenu": "显示 _MENU_ 记录",
        "sZeroRecords": "对不起，查询不到任何相关数据",
        "sEmptyTable": "未有相关数据",
        "sLoadingRecords": "正在加载数据-请等待...",
        "sInfo": "当前显示 _START_ 到 _END_ 条，共 _TOTAL_ 条记录。",
        "sInfoEmpty": "当前显示0到0条，共0条记录",
        "sInfoFiltered": "（数据库中共为 _MAX_ 条记录）",
        "sProcessing": "<img src='../resources/user_share/row_details/select2-spinner.gif'/> 正在加载数据...",
        "sSearch": "模糊查询：",
        "sUrl": "",
        //多语言配置文件，可将oLanguage的设置放在一个txt文件中，例：Javascript/datatable/dtCH.txt
        "oPaginate": {
            "sFirst": "首页",
            "sPrevious": " 上一页 ",
            "sNext": " 下一页 ",
            "sLast": " 尾页 "
        }
    },
    "processing": true,
    "serverSide": true,
    //数据来源（包括处理分页，排序，过滤） ，即url，action，接口，等等
    "ajax": {
        "url": '/../../business/getbqtablelist/',
        "type": 'POST',
    },

    "columns": [{
        "data": "xuhao"
    }, {
        "data": "code"
    }, {
        "data": "name"
    }, {
        "data": "unit"
    }, {
        "data": null
    }, {
        "data": null
    }, {
        "data": null
    },
    {
        "data": null
    },
    ],
    columnDefs: [ //添加自定义按钮
        {
            targets: 4,
            render: function(a) {
                if (a.locked == 1) {
                    return (a.quantity).toFixed(4)
                }
                if (a.datatype == 1) {
                    return '<a href="#" class="selfedit-table"  data-url="/business/updateReportBqitem/" id="nums-1" data-type="text" data-pk="' + a.id + '" data-title="工程量">' + (a.quantity).toFixed(4) + '</a>';
                } else {
                    return (a.quantity).toFixed(4);
                    // return '<a href="#" class="selfedit-table"  data-url="/business/updateReportBqitem/" id="nums-2" data-type="text" data-pk="' + a.id + '" data-title="工程量">' + (a.quantity).toFixed(4) + '</a>';
                }
            }
        },
        {
            targets: 5,
            render: function(a) {
                if (a.locked == 1) {
                    return (a.unitprice).toFixed(2)
                }
                if (a.datatype == 1) {
                    return '<a href="#" class="selfedit-table"  data-url="/business/updateReportBqitem/" id="price-1" data-type="text" data-pk="' + a.id + '" data-title="综合单价">' + (a.unitprice).toFixed(2) + '</a>';
                } else {
                    return (a.unitprice).toFixed(2);
                    // return '<a href="#" class="selfedit-table"  data-url="/business/updateReportBqitem/" id="price-2" data-type="text" data-pk="' + a.id + '" data-title="综合单价">' + (a.unitprice).toFixed(2) + '</a>';
                }
            }
        },
        {
            targets: 6,
            render: function(a) {
                return (a.unitprice * a.quantity).toFixed(2);
            }
        },
        {
            targets: 7,
            render: function(a, b, c, d) {
                var key = a.datatype + '-' + a.id
                var html = '';
                // console.log(a)
                if (a.locked == 1) {
                    if(a.datatype == 1){
                        html = '<button style="margin-left:2px;margin-right:2px;" type="button" data="' + key + '" class="btn btn-danger btn-xs disabled" >删除行</button>';
                    }
                } else {
                    if(a.datatype == 1){
                        html = '<button style="margin-left:2px;margin-right:2px;" type="button" data="' + key + '" class="btn btn-danger btn-xs delurl" >删除行</button>';
                    }

                }

                return html;
            }
        }
    ],
    //向服务器传额外的参数
    "fnServerParams": function(aoData) {
        aoData.param = keeplist;
    },
    "fnDrawCallback": function(data) {
        $(".selfedit-table").editable({
            validate: function(value) { //字段验证
                if (!$.trim(value)) {
                    return '不能为空';
                } else {

                }
            },
            success: function() {
                tablebqs.draw();
            }
        });
    },
};
var datatable_cos_options = {
    "dom": 'tip',
    "iDisplayLength": 15,
    "lengthChange": false, //是否允许用户自定义显示数量
    "bPaginate": true, //翻页功能
    "bFilter": false, //列筛序功能
    "searching": false, //本地搜索
    "ordering": false, //排序功能
    "Info": true, //页脚信息
    "autoWidth": true, //自动宽度
    "oLanguage": { //国际语言转化
        "oAria": {
            "sSortAscending": " - click/return to sort ascending",
            "sSortDescending": " - click/return to sort descending"
        },
        "sLengthMenu": "显示 _MENU_ 记录",
        "sZeroRecords": "对不起，查询不到任何相关数据",
        "sEmptyTable": "未有相关数据",
        "sLoadingRecords": "正在加载数据-请等待...",
        "sInfo": "当前显示 _START_ 到 _END_ 条，共 _TOTAL_ 条记录。",
        "sInfoEmpty": "当前显示0到0条，共0条记录",
        "sInfoFiltered": "（数据库中共为 _MAX_ 条记录）",
        "sProcessing": "<img src='../resources/user_share/row_details/select2-spinner.gif'/> 正在加载数据...",
        "sSearch": "模糊查询：",
        "sUrl": "",
        //多语言配置文件，可将oLanguage的设置放在一个txt文件中，例：Javascript/datatable/dtCH.txt
        "oPaginate": {
            "sFirst": "首页",
            "sPrevious": " 上一页 ",
            "sNext": " 下一页 ",
            "sLast": " 尾页 "
        }
    },
    "processing": true,
    "serverSide": true,
    //数据来源（包括处理分页，排序，过滤） ，即url，action，接口，等等
    "ajax": {
        "url": '/../../business/getbqtablelist/',
        "type": 'POST',
    },

    "columns": [{
        "data": null
    }, {
        "data": "name"
    }, {
        "data": "ratedescription"
    }, {
        "data": "rate"
    }, {
        "data": "money"
    }, {
        "data": null
    }, ],
    columnDefs: [ //添加自定义按钮
        {
            targets: 5,
            render: function(a, b, c, d) {
                var html = '';
                // return html;
                if (a.locked == 1) {
                    html = '<button style="margin-left:2px;margin-right:2px;" type="button" data="' + a.id + '" class="btn btn-danger btn-xs disabled" >删除行</button>';;
                } else {
                    html = '<button style="margin-left:2px;margin-right:2px;" type="button" data="' + a.id + '" class="btn btn-danger btn-xs delurl" >删除行</button>';
                }
                return html;
            }
        }
    ],
    //向服务器传额外的参数
    "fnServerParams": function(aoData) {
        aoData.param = keeplist;
    },
    "fnDrawCallback": function() { //序号
        　　
        this.api().column(0).nodes().each(function(cell, i) {　　　　 cell.innerHTML = i + 1;　　 });
    },
};
var datatable_fenjian_options = {
    "dom": 'tip',
    "iDisplayLength": 15,
    "lengthChange": false, //是否允许用户自定义显示数量
    "bPaginate": true, //翻页功能
    "bFilter": false, //列筛序功能
    "searching": false, //本地搜索
    "ordering": false, //排序功能
    "Info": true, //页脚信息
    "autoWidth": true, //自动宽度
    "oLanguage": { //国际语言转化
        "oAria": {
            "sSortAscending": " - click/return to sort ascending",
            "sSortDescending": " - click/return to sort descending"
        },
        "sLengthMenu": "显示 _MENU_ 记录",
        "sZeroRecords": "对不起，查询不到任何相关数据",
        "sEmptyTable": "未有相关数据",
        "sLoadingRecords": "正在加载数据-请等待...",
        "sInfo": "当前显示 _START_ 到 _END_ 条，共 _TOTAL_ 条记录。",
        "sInfoEmpty": "当前显示0到0条，共0条记录",
        "sInfoFiltered": "（数据库中共为 _MAX_ 条记录）",
        "sProcessing": "<img src='../resources/user_share/row_details/select2-spinner.gif'/> 正在加载数据...",
        "sSearch": "模糊查询：",
        "sUrl": "",
        //多语言配置文件，可将oLanguage的设置放在一个txt文件中，例：Javascript/datatable/dtCH.txt
        "oPaginate": {
            "sFirst": "首页",
            "sPrevious": " 上一页 ",
            "sNext": " 下一页 ",
            "sLast": " 尾页 "
        }
    },
    "processing": true,
    "serverSide": true,
    //数据来源（包括处理分页，排序，过滤） ，即url，action，接口，等等
    "ajax": {
        "url": '/../../business/getbqtablelist/',
        "type": 'POST',
    },

    "columns": [{
        "data": "xuhao"
    }, {
        "data": "code"
    }, {
        "data": "name"
    }, {
        "data": "unit"
    }, {
        "data": "quanlity"
    }, {
        "data": "unitprice"
    }, {
        "data": null,
    }, {
        "data": null
    }, ],
    columnDefs: [ //添加自定义按钮
        {
            targets: 6,
            render: function(a, b, c, d) {
                return (a.quanlity * a.unitprice).toFixed(2);
            }
        },
        {
            targets: 7,
            render: function(a, b, c, d) {
                var html = '';
                if (a.locked == 1) {
                    html = '<button style="margin-left:2px;margin-right:2px;" type="button" data="' + a.id + '" class="btn btn-danger btn-xs disabled" >删除行</button>';;
                } else {
                    html = '<button style="margin-left:2px;margin-right:2px;" type="button" data="' + a.id + '" class="btn btn-danger btn-xs delurl" >删除行</button>';
                }
                return html;
            }
        }
    ],
    //向服务器传额外的参数
    "fnServerParams": function(aoData) {
        aoData.param = keeplist;
    },
};
var datatable_laowu_options = {
    "dom": 'tip',
    "iDisplayLength": 15,
    "lengthChange": false, //是否允许用户自定义显示数量
    "bPaginate": true, //翻页功能
    "bFilter": false, //列筛序功能
    "searching": false, //本地搜索
    "ordering": false, //排序功能
    "Info": true, //页脚信息
    "autoWidth": true, //自动宽度
    "oLanguage": { //国际语言转化
        "oAria": {
            "sSortAscending": " - click/return to sort ascending",
            "sSortDescending": " - click/return to sort descending"
        },
        "sLengthMenu": "显示 _MENU_ 记录",
        "sZeroRecords": "对不起，查询不到任何相关数据",
        "sEmptyTable": "未有相关数据",
        "sLoadingRecords": "正在加载数据-请等待...",
        "sInfo": "当前显示 _START_ 到 _END_ 条，共 _TOTAL_ 条记录。",
        "sInfoEmpty": "当前显示0到0条，共0条记录",
        "sInfoFiltered": "（数据库中共为 _MAX_ 条记录）",
        "sProcessing": "<img src='../resources/user_share/row_details/select2-spinner.gif'/> 正在加载数据...",
        "sSearch": "模糊查询：",
        "sUrl": "",
        //多语言配置文件，可将oLanguage的设置放在一个txt文件中，例：Javascript/datatable/dtCH.txt
        "oPaginate": {
            "sFirst": "首页",
            "sPrevious": " 上一页 ",
            "sNext": " 下一页 ",
            "sLast": " 尾页 "
        }
    },
    "processing": true,
    "serverSide": true,
    //数据来源（包括处理分页，排序，过滤） ，即url，action，接口，等等
    "ajax": {
        "url": '/../../business/getbqtablelist/',
        "type": 'POST',
    },

    "columns": [
        // {
        //   "data": "xuhao"
        // }, {
        //   "data": "code"
        // },
        {
            "data": "name"
        }, {
            "data": "unit"
        }, {
            "data": "quanlity"
        }, {
            "data": "unitprice"
        }, {
            "data": null,
        }, {
            "data": null
        },
    ],
    columnDefs: [ //添加自定义按钮
        {
            targets: 4,
            render: function(a, b, c, d) {
                return (a.quanlity * a.unitprice).toFixed(2);
            }
        },
        {
            targets: 5,
            render: function(a, b, c, d) {
                var html = '';
                if (a.locked == 1) {
                    html = '<button style="margin-left:2px;margin-right:2px;" type="button" data="' + a.id + '-' + a.tasktype + '" class="btn btn-danger btn-xs disabled" >删除行</button>';;
                } else {
                    html = '<button style="margin-left:2px;margin-right:2px;" type="button" data="' + a.id + '-' + a.tasktype + '" class="btn btn-danger btn-xs delurl" >删除行</button>';
                }
                return html;
            }
        }
    ],
    //向服务器传额外的参数
    "fnServerParams": function(aoData) {
        aoData.param = keeplist;
    },
};
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



// $(function() {
//     businessManager.init();
//     tablebqs = $('#table-bqs').DataTable(datatable_bqs_options);
// });

var businessManager = {
    init: function() {
        var that = this;

        that.formValidator();
        that.bindListener();
        curr_jstree = that.jstreeInit();
        // account_jstree = that.jstreeAccountInit();
        that.formValidator();
    },

    bindListener: function() {
        var that = this;
        $("#qingdan_code").change(function() {
            $.ajax({
                type: 'get',
                dataType: 'json',
                url: '/business/getqingdancodeinfo/',
                data: {
                    id: $(this).val()
                },
                success: function(data) {
                    if (data.issuc) {
                        var name = data.bqitem.BQItemName;
                        $("#qingdan_name").val(name.trim());
                        $("#qingdan_unit").val(data.bqitem.BQItemUnit);
                        $("#qingdan_amount").val(data.bqitem.designBqs);
                        $("#qingdan_price").val(data.bqitem.allunitrate);
                    } else {
                        alert(data.msg);
                    }
                },
                error: function(data) {},
            });
        });
        $("#fenjian_name").change(function() {
            $.ajax({
                type: 'get',
                dataType: 'json',
                url: '/business/getSciteminfo/',
                data: {
                    id: $(this).val()
                },
                success: function(data) {
                    if (data.issuc) {
                        $("#fenjian_unit").val(data.scitem.unit);
                        $("#fenjian_quantities").val(data.scitem.designBqs);
                        $("#fenjian_price").val(data.scitem.price);

                    } else {
                        alert(data.msg);
                    }
                },
                error: function(data) {},
            });
        });
        $("#start_time").bind("click", function() {
            $('#start_time').datetimepicker({
                language: 'zh-CN', //显示中文
                autoclose: true, //选中自动关闭
                format: "yyyy-mm-dd", //日期格式
                minView: "month", //设置只显示到月份
            }).on('hide', function(e) {
                $('#addclucreportForm').data('bootstrapValidator')
                    .updateStatus('start_time', 'NOT_VALIDATED', null)
                    .validateField('start_time');
            });
        });
        $("#start_time").click();

        $("#end_time").bind("click", function() {
            $('#end_time').datetimepicker({
                language: 'zh-CN', //显示中文
                autoclose: true, //选中自动关闭
                format: "yyyy-mm-dd", //日期格式
                minView: "month", //设置只显示到月份
            }).on('hide', function(e) {
                $('#addclucreportForm').data('bootstrapValidator')
                    .updateStatus('end_time', 'NOT_VALIDATED', null)
                    .validateField('end_time');
            });
        });
        $("#end_time").click();
        $("#jstree_demo_div").bind("activate_node.jstree", function(obj, e) {
            if (mouse_key != 1)
                return;

            var selectedid = e.node.id;
            curr_slectnode = selectedid;
            console.log(curr_slectnode);
            _app.can_export = 0;
            if (selectedid.indexOf("-") >= 0 && selectedid.split('-')[0]!='space' && selectedid.split('-')[0]!='fenbao' && selectedid.split('-')[0]!='zixing' && selectedid.split('-')[0]!='zixingyg'&& selectedid.split('-')[0]!='fenbaoyg'&& selectedid.split('-')[0]!='chanzhi'&& selectedid.split('-')[0]!='chengben') {
                curr_tableid = 'table-' + selectedid.split('-')[0];
                keeplist.report_id = selectedid.split('-')[1]
                if (selectedid.split('-')[0] == 'bqs') {
                    keeplist.report_type = 1;
                    tablebqs.draw();
                    itemtype = 1;
                    export_tableid = 'table-bqs';
                    export_name = '清单项目表';
                    $("#shangbaoReport").show();
                    // $(".header-div").show();
                    _app.show_menu_button = 1;
                } else if (selectedid.split('-')[0] == 'res') {
                    keeplist.report_type = 2;
                    itemtype = 2;
                    _app.getresdatalist(keeplist.report_id,keeplist.report_type);
                    _app.can_export = 1;
                    export_tableid = 'table-res';
                    export_name = '工料机表';
                    $("#shangbaoReport").show();
                    // $(".header-div").show();
                    _app.show_menu_button = 1;
                } else if (selectedid.split('-')[0] == 'cos') {
                    keeplist.report_type = 3;
                    if (tablecos == null) {
                        tablecos = $('#table-cos').DataTable(datatable_cos_options);
                    } else {
                        tablecos.draw();
                    }
                    itemtype = 3;

                    $("#shangbaoReport").show();
                    // $(".header-div").show();
                    _app.show_menu_button = 1;
                } else if (selectedid.split('-')[0] == 'fenjian' || selectedid.split('-')[0] == 'company') {
                    keeplist.report_type = 4;
                    curr_tableid = 'table-fenjian';
                    keeplist.report = selectedid.split('-')[1]
                    keeplist.company = selectedid.split('-')[2]
                    if (tablefenjian == null) {
                        tablefenjian = $('#table-fenjian').DataTable(datatable_fenjian_options);
                    } else {
                        tablefenjian.draw();
                    }
                    $("#shangbaoReport").hide();
                    // $(".header-div").show();
                    _app.show_menu_button = 1;
                    itemtype = 4;
                } else if (selectedid.split('-')[0] == 'laowu') {
                    keeplist.report_type = 5;
                    keeplist.report = selectedid.split('-')[1]
                    keeplist.company = selectedid.split('-')[2]
                    curr_tableid = 'table-laowu';
                    if (tablelaowu == null) {
                        tablelaowu = $('#table-laowu').DataTable(datatable_laowu_options);
                    } else {
                        tablelaowu.draw();
                    }
                    // $(".header-div").hide();
                    _app.show_menu_button = 0;
                    itemtype = 5;
                } else if (selectedid.split('-')[0] == 'thound2') {
                    keeplist.report_type = 6;
                    keeplist.report = selectedid.split('-')[1]
                    export_tableid = 'table-thound2';
                    export_name = '2000定额工料机';
                    _app.getresdatalist(keeplist.report_id,keeplist.report_type);
                    // $(".header-div").hide();
                    _app.show_menu_button = 0;
                    itemtype = 6;
                } else if (selectedid.split('-')[0] == 'rate') {
                    keeplist.report_type = 7;
                    keeplist.report = selectedid.split('-')[1]
                    console.log(111111);
                    // keeplist.company=selectedid.split('-')[2]
                    export_tableid = 'table-rate';
                    export_name = '费率表';
                    curr_tableid = 'table-rate';
                    if (tablerate == null) {
                        tablerate = $('#table-rate').DataTable(datatable_rate_options);
                    } else {
                        tablerate.draw();
                    }
                    // $(".header-div").hide();
                    _app.show_menu_button = 0;
                    itemtype = 7;
                }
                curr_report_id = keeplist.report_id;
                $(".table-active").removeClass("table-active").addClass("table-unactive");
                $("." + curr_tableid).removeClass("table-unactive").addClass("table-active");
            } else if (selectedid.indexOf("report") >= 0) {
                curr_tableid = 'table-bqs';
                keeplist.report_id = selectedid.replace('report', '');
                keeplist.report_type = 1;
                tablebqs.draw();
                itemtype = 1;
                export_tableid = 'table-bqs';
                export_name = '清单项目表';
                curr_report_id = keeplist.report_id;
                $(".table-active").removeClass("table-active").addClass("table-unactive");
                $("." + curr_tableid).removeClass("table-unactive").addClass("table-active");
                $("#shangbaoReport").show();
                // $(".header-div").show();
                _app.show_menu_button = 1;
            }
        });

        $('#addRow').on('click', function() {
            if (itemtype == 1) {
                $("#addQingdanRowDialog").modal('show');
            } else if (itemtype == 2) {
                $("#addGongliaojiRowDialog").modal('show');
            } else if (itemtype == 3) {
                $("#addFeiyongRowDialog").modal('show');
            } else if (itemtype == 4) {
                $("#addFengjianRowDialog").modal('show');
            }
        });

        $('#shangbaoReport').on('click', function() {

            if (curr_slectnode == null || curr_slectnode == 'root') {
                alert("请选择要上报的报告");
                return;
            }
            var text = '';
            var reportid = '';
            var node = $('#jstree_demo_div').jstree("get_node", curr_slectnode);
            console.log(node);
            if(curr_slectnode.indexOf('chanzhi')>=0||curr_slectnode.indexOf('chengben')>=0){
                reportid = curr_slectnode.split('-')[3];
            }else{
                alert("请选择要上报的报告");
                return;
            }
            alertConfirm('确定要上报 ' + node.text + "，一经上报不可再修改哦", null, function() {
                $.ajax({
                    type: 'get',
                    dataType: 'json',
                    data: { "report_id": reportid },
                    url: '/business/lockReport/',
                    success: function(data) {
                        if (data.issuc) {
                            alert("上报成功", null, function() {
                                window.location.reload();
                            });
                        } else {
                            alert(data.msg);
                        }
                    },
                    error: function(data) {
                        alert(data.msg)
                    }
                });
            });
        });
        $('#calcuteReport').on('click', function() {
            var currdate = new Date()
            var name = currdate.getFullYear() + "年" + (currdate.getMonth() + 1) + "月份产值报告"
            var start = currdate.getFullYear() + "-" + (currdate.getMonth() + 1) + "-1";
            var end = currdate.getFullYear() + "-" + (currdate.getMonth() + 1) + "-" + new Date(currdate.getFullYear(), currdate.getMonth() + 1, 0).getDate();
            $("#report_name").val(name);
            $("#start_time").val(start);
            $("#end_time").val(end);
            $("#addClucReportDialog").modal('show');
        });

        $("#btnAddReport").on("click", function() {
            $('#addclucreportForm').bootstrapValidator('validate');
            if (!($('#addclucreportForm').data('bootstrapValidator').isValid())) {
                return;
            }
            $(".pro-loading").show();
            $.ajax({
                type: 'get',
                dataType: 'json',
                url: '/business/calculateReport/',
                data: {
                    start_time: $("#start_time").val(),
                    end_time: $("#end_time").val(),
                    report_name: $("#report_name").val(),
                    budget_id: $("#budget_id").val()
                },
                success: function(data) {
                    $(".pro-loading").hide();
                    if (data.issuc) {
                        alert("计算产值成功", null, function() {
                            $("#addClucReportDialog").modal('hide');
                            window.location.reload(); //重新加载
                        });
                    } else {
                        alert("计算产值异常")
                    }
                },
                error: function(data) {
                    alert("系统异常");
                }
            });
        });
        $("#btnAddRowqingdan").bind("click", function() {
            $('#addQingdanRowForm').bootstrapValidator('validate');
            if (!($('#addQingdanRowForm').data('bootstrapValidator').isValid())) {
                return;
            }
            $.ajax({
                type: 'get',
                dataType: 'json',
                url: '/business/addReportBqitem/',
                data: {
                    bqid: $("#qingdan_code option:selected").val(),
                    name: $("#qingdan_name").val(),
                    unit: $("#qingdan_unit").val(),
                    amount: $("#qingdan_amount").val(),
                    price: $("#qingdan_price").val(),
                    report_id: curr_report_id,
                },
                success: function(data) {
                    if (data.issuc) {
                        alert("添加成功", null, function() {
                            tablebqs.draw();
                            $("#addQingdanRowDialog").modal('hide');
                            document.getElementById("addQingdanRowForm").reset(); //清空表单
                        });
                    } else {
                        alert(data.msg, null, function() {
                            $("#addQingdanRowDialog").modal('hide');
                            document.getElementById("addQingdanRowForm").reset(); //清空表单
                        });
                    }
                },
                error: function(data) {
                    alert(data.msg)
                }
            });
        });

        $("#btnAddRowGongliaoji").bind("click", function() {
            $('#addGongliaojiRowForm').bootstrapValidator('validate');
            if (!($('#addGongliaojiRowForm').data('bootstrapValidator').isValid())) {
                return;
            }
            $.ajax({
                type: 'get',
                dataType: 'json',
                url: '/business/addReportRes/',
                data: {
                    resourceid: $("#gongliaoji_code option:selected").val(),
                    name: $("#gongliaoji_name").val(),
                    amount: $("#gongliaoji_amount").val(),
                    price: $("#gongliaoji_price").val(),
                    report_id: curr_report_id,
                },
                success: function(data) {
                    if (data.issuc) {
                        alert("添加成功", null, function() {
                            tableres.draw()
                            $("#addGongliaojiRowDialog").modal('hide');
                            document.getElementById("addGongliaojiRowForm").reset(); //清空表单
                        });
                    } else {
                        alert(data.msg, null, function() {
                            $("#addGongliaojiRowDialog").modal('hide');
                            document.getElementById("addGongliaojiRowForm").reset(); //清空表单
                        });
                    }
                },
                error: function(data) {
                    alert(data.msg)
                }
            });
        });

        $("#btnAddRowFeiyong").bind("click", function() {
            $('#addFeiyongRowForm').bootstrapValidator('validate');
            if (!($('#addFeiyongRowForm').data('bootstrapValidator').isValid())) {
                return;
            }
            $.ajax({
                type: 'get',
                dataType: 'json',
                url: '/business/addReportCost/',
                data: {
                    name: $("#feiyong_name").val(),
                    rate: $("#feiyong_rate").val(),
                    ratedescription: $("#feiyong_jishu").val(),
                    money: $("#feiyong_money").val(),
                    scid: $("#feiyong_sc option:selected").val(),
                    report_id: curr_report_id,
                },
                success: function(data) {
                    if (data.issuc) {
                        alert("添加成功", null, function() {
                            tablecos.draw()
                            $("#addFeiyongRowDialog").modal('hide');
                            document.getElementById("addFeiyongRowForm").reset(); //清空表单
                        });
                    } else {
                        alert(data.msg, null, function() {
                            $("#addFeiyongRowDialog").modal('hide');
                            document.getElementById("addFeiyongRowForm").reset(); //清空表单
                        })
                    }
                },
                error: function(data) {
                    alert(data.msg);
                }
            });
        });

        $("#btnAddRowFenjian").bind("click", function() {
            $('#addFenjianRowForm').bootstrapValidator('validate');
            if (!($('#addFenjianRowForm').data('bootstrapValidator').isValid())) {
                return;
            }
            $.ajax({
                type: 'get',
                dataType: 'json',
                url: '/business/addSeparateCost/',
                data: {
                    scid: $("#fenjian_name option:selected").val(),
                    price: $("#fenjian_price").val(),
                    unit: $("#fenjian_unit").val(),
                    quantities: $("#fenjian_quantities").val(),
                    money: $("#fenjian_money").val(),
                    report_id: curr_report_id,
                    companyid: keeplist.company
                },
                success: function(data) {
                    if (data.issuc) {
                        alert("添加成功", null, function() {
                            tablefenjian.draw()
                            $("#addFengjianRowDialog").modal('hide');
                            document.getElementById("addFenjianRowForm").reset(); //清空表单
                        });
                    } else {
                        alert(data.msg, null, function() {
                            $("#addFengjianRowDialog").modal('hide');
                            document.getElementById("addFenjianRowForm").reset(); //清空表单
                        })
                    }
                },
                error: function(data) {
                    alert(data.msg);
                }
            });
        });

        $("#addClucReportDialog").on("hidden.bs.modal", function() {
            $("#addclucreportForm").data('bootstrapValidator').destroy();
            $('#addclucreportForm').data('bootstrapValidator', null);
            document.getElementById("addclucreportForm").reset(); //清空表单
            that.formValidator();
        });
        $("#addQingdanRowDialog").on("hidden.bs.modal", function() {
            $("#addQingdanRowForm").data('bootstrapValidator').destroy();
            $('#addQingdanRowForm').data('bootstrapValidator', null);
            document.getElementById("addQingdanRowForm").reset(); //清空表单
            that.formValidator();
        });
        $("#addGongliaojiRowDialog").on("hidden.bs.modal", function() {
            $("#addGongliaojiRowForm").data('bootstrapValidator').destroy();
            $('#addGongliaojiRowForm').data('bootstrapValidator', null);
            document.getElementById("addGongliaojiRowForm").reset(); //清空表单
            that.formValidator();
        });
        $("#addFeiyongRowDialog").on("hidden.bs.modal", function() {
            $("#addFeiyongRowForm").data('bootstrapValidator').destroy();
            $('#addFeiyongRowForm').data('bootstrapValidator', null);
            document.getElementById("addFeiyongRowForm").reset(); //清空表单
            that.formValidator();
        });
        $("#addFengjianRowDialog").on("hidden.bs.modal", function() {
            $("#addFenjianRowForm").data('bootstrapValidator').destroy();
            $('#addFenjianRowForm').data('bootstrapValidator', null);
            document.getElementById("addFenjianRowForm").reset(); //清空表单
            that.formValidator();
        });
        $(".table-bqs").on("click", '.datatable .delurl', function() {
            var key = $(this).attr('data');
            var report_bqid = 0;
            var report_rtid = 0;
            if (key.split('-')[0] == 1) {
                report_bqid = key.split('-')[1]
            } else if (key.split('-')[0] == 2) {
                report_rtid = key.split('-')[1]
            }
            console.log(report_rtid,report_bqid);
            alertConfirm("确定删除吗", null, function() {
                $.ajax({
                    type: 'get',
                    dataType: 'json',
                    url: '/business/delReportBqitem/',
                    data: {
                        report_bqid: report_bqid,
                        report_rtid: report_rtid,
                        deltype: key.split('-')[0]
                    },
                    success: function(data) {
                        if (data.issuc) {
                            alert("删除成功", null, function() {
                                tablebqs.draw();
                            });
                        }
                    },
                    error: function(data) {
                        alert('系统异常');
                    }
                });
            })
        });
        $(".table-res").on("click", '.datatable .delurl', function() {
            var key = $(this).attr('data');
            alertConfirm("确定删除吗", null, function() {
                $.ajax({
                    type: 'get',
                    dataType: 'json',
                    url: '/business/delReportRes/',
                    data: {
                        report_sourceid: key,
                    },
                    success: function(data) {
                        if (data.issuc) {
                            alert("删除成功", null, function() {
                                tableres.draw();
                            });
                        }
                    },
                    error: function(data) {
                        alert('系统异常');
                    }
                });
            })
        });
        $(".table-cos").on("click", '.datatable .delurl', function() {
            var key = $(this).attr('data');
            alertConfirm("确定删除吗", null, function() {
                $.ajax({
                    type: 'get',
                    dataType: 'json',
                    url: '/business/delReportCost/',
                    data: {
                        report_costid: key,
                    },
                    success: function(data) {
                        if (data.issuc) {
                            alert("删除成功", null, function() {
                                tablecos.draw();
                            });
                        }
                    },
                    error: function(data) {
                        alert('系统异常');
                    }
                });
            })
        });
        $(".table-fenjian").on("click", '.datatable .delurl', function() {
            var key = $(this).attr('data');
            console.log(key);
            alertConfirm("确定删除吗", null, function() {
                $.ajax({
                    type: 'get',
                    dataType: 'json',
                    url: '/business/delSeparateCost/',
                    data: {
                        id: key,
                    },
                    success: function(data) {
                        if (data.issuc) {
                            alert("删除成功", null, function() {
                                tablefenjian.draw();
                            });
                        }
                    },
                    error: function(data) {
                        alert('系统异常');
                    }
                });
            })
        });
        $(".table-laowu").on("click", '.datatable .delurl', function() {
            var key = $(this).attr('data');
            alertConfirm("确定删除吗", null, function() {
                $.ajax({
                    type: 'get',
                    dataType: 'json',
                    url: '/business/delTaskorderByid/',
                    data: {
                        id: key.split('-')[0],
                        tasktype: key.split('-')[1]
                    },
                    success: function(data) {
                        if (data.issuc) {
                            alert("删除成功", null, function() {
                                tablelaowu.draw();
                            });
                        }
                    },
                    error: function(data) {
                        alert('系统异常');
                    }
                });
            })
        });
    },

    jstreeInit: function() {
        $("#jstree_demo_div").jstree({
            "core": {
                'data': {
                    'url': '/business/get_hazard_tree/',
                    'data': function(node) {
                        return {
                            'id': node.id
                        };
                    }
                }
            },
            'multiple': false,
            "plugins": ["themes", "json_data","contextmenu" ],
            "contextmenu": {
              "items": function (node) {
                  var temp = {
                      "deletereport": {
                          "label": "删除",
                          "icon":"fa fa-times",
                          // "separator_after": true,
                          "action": function (data) {
                            alertConfirm("确定删除 "+node.text+" 吗?",null,function(){
                              var report_id = (node.id).split('-')[3];
                              $.ajax({
                                type:'get',
                                dataType:'json',
                                url:'/business/delReport/',
                                data:{report_id:report_id},
                                success:function(data){
                                  if(data.issuc){
                                    alert("删除成功",null,function(){
                                      window.location.reload();
                                    });
                                  }else{
                                    alert(data.msg);
                                  }
                                },
                                error:function(data){
                                  alert("系统异常");
                                }
                              });
                            });
                          }
                      },
                      "shagnbaoreport": {
                          "label": "上报",
                          "icon":"fa fa-times",
                          // "separator_after": true,
                          "action": function (data) {
                            alertConfirm("确定上报 "+node.text+" 吗?",null,function(){
                              var report_id = (node.id).split('-')[3];
                              $.ajax({
                                    type: 'get',
                                    dataType: 'json',
                                    data: { "report_id": report_id },
                                    url: '/business/lockReport/',
                                    success: function(data) {
                                        if (data.issuc) {
                                            alert("上报成功", null, function() {
                                                window.location.reload();
                                            });
                                        } else {
                                            alert(data.msg);
                                        }
                                    },
                                    error: function(data) {
                                        alert(data.msg)
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
                  console.log('生成菜单'+node.id)
                  if((node.id).indexOf("chanzhi")>=0||(node.id).indexOf("chengben")>=0){
                     console.log('生成菜单222')
                    return temp;
                  }else{
                    return menu;
                  }
              },
              "select_node": false
          },
        });
    },
    jstreeAccountInit: function() {
        return $('#jstree_demo_div2').jstree({
            'core': {
                'data': {
                    'url': '/business/get_report_account_tree/',
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
                            "label": "删除报告",
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

    formValidator: function() {
        $('#addQingdanRowForm').bootstrapValidator({
            message: 'This value is not valid',
            feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {
                qingdan_code: {
                    validators: {
                        notEmpty: {
                            message: '编号不能为空'
                        },
                    }
                },
                qingdan_name: {
                    validators: {
                        notEmpty: {
                            message: '名称不能为空'
                        }
                    }
                },
                qingdan_unit: {
                    validators: {
                        notEmpty: {
                            message: '单位不能为空'
                        }
                    }
                },
                qingdan_amount: {
                    validators: {
                        notEmpty: {
                            message: '工程量不能为空'
                        },
                        regexp: {
                            regexp: /^[0-9]+([.]{1}[0-9]+){0,1}$/,
                            message: '格式不对，只能输入数字', //
                        }
                    }
                },
                qingdan_price: {
                    validators: {
                        notEmpty: {
                            message: '价格不能为空'
                        },
                        regexp: {
                            message: '格式不对，请输入价格', //
                            regexp: /^[0-9]+([.]{1}[0-9]+){0,1}$/
                        }
                    }
                },

            }
        });

        $('#addGongliaojiRowForm').bootstrapValidator({
            message: 'This value is not valid',
            feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {

                gongliaoji_code: {
                    validators: {
                        notEmpty: {
                            message: '编号不能为空'
                        },
                    }
                },
                gongliaoji_name: {
                    validators: {
                        notEmpty: {
                            message: '名称不能为空'
                        }
                    }
                },

                gongliaoji_amount: {
                    validators: {
                        notEmpty: {
                            message: '数量不能为空'
                        },
                        regexp: {
                            regexp: /^[0-9]+([.]{1}[0-9]+){0,1}$/,
                            message: '格式不对，只能输入数字', //
                        }
                    }
                },
                gongliaoji_price: {
                    validators: {
                        notEmpty: {
                            message: '价格不能为空'
                        },
                        regexp: {
                            message: '格式不对，请输入价格', //
                            regexp: /^[0-9]+([.]{1}[0-9]+){0,1}$/
                        }
                    }
                },

            }
        });
        $('#addFeiyongRowForm').bootstrapValidator({
            message: 'This value is not valid',
            feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {

                feiyong_name: {
                    validators: {
                        notEmpty: {
                            message: '名称不能为空'
                        }
                    }
                },
                feiyong_name: {
                    validators: {
                        notEmpty: {
                            message: '名称不能为空'
                        }
                    }
                },
                feiyong_jishu: {
                    validators: {
                        notEmpty: {
                            message: '基数说明不能为空'
                        },
                        stringLength: {
                            min: 5,
                            max: 20,
                            message: '描述在5-20个字'
                        }

                    }
                },
                feiyong_rate: {
                    validators: {
                        notEmpty: {
                            message: '费率不能为空'
                        },
                        regexp: {
                            message: '格式不对，请输入费率', //
                            regexp: /^[0-9]+([.]{1}[0-9]+){0,1}$/
                        }
                    }
                },
                feiyong_money: {
                    validators: {
                        notEmpty: {
                            message: '金额不能为空'
                        },
                        regexp: {
                            message: '格式不对，请输入金额', //
                            regexp: /^[0-9]+([.]{1}[0-9]+){0,1}$/
                        }
                    }
                },
            }
        });

        $("#addFenjianRowForm").bootstrapValidator({
            message: 'This value is not valid',
            feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {
                fenjian_name: {
                    validators: {
                        notEmpty: {
                            message: '名称不能为空'
                        }
                    }
                },
                fenjian_unit: {
                    validators: {
                        notEmpty: {
                            message: '单位不能为空'
                        }
                    }
                },
                fenjian_quantities: {
                    validators: {
                        notEmpty: {
                            message: '工程量不能为空'
                        },
                        regexp: {
                            regexp: /^[0-9]+([.]{1}[0-9]+){0,1}$/,
                            message: '格式不对，只能输入数字', //

                        }
                    }
                },
                fenjian_price: {
                    validators: {
                        notEmpty: {
                            message: '单价不能为空'
                        },
                        regexp: {
                            message: '格式不对，请输入单价', //
                            regexp: /^[0-9]+([.]{1}[0-9]+){0,1}$/
                        }
                    }
                },
                fenjian_money: {
                    validators: {
                        notEmpty: {
                            message: '合价不能为空'
                        },
                        regexp: {
                            message: '格式不对，请输入合价', //
                            regexp: /^[0-9]+([.]{1}[0-9]+){0,1}$/
                        }
                    }
                },
            }
        });

        $('#addclucreportForm').bootstrapValidator({
            message: 'This value is not valid',
            feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {
                report_name: {
                    message: 'The username is not valid',
                    validators: {
                        notEmpty: {
                            message: '报告名称不能为空'
                        },

                    }
                },
                start_time: {
                    validators: {
                        callback: {
                            message: '开始日期不能为空且需小于结束日期',
                            callback: function(value, validator, $field, options) {
                                var endtime = $('#end_time').val()

                                if (endtime == null || endtime == '' || value == null || value == '') {
                                    return false;
                                }
                                var sta = Date.parse(new Date(value));
                                var end = Date.parse(new Date(endtime));

                                validator.updateStatus('end_time', 'VALID');
                                $('#end_time').keypress();
                                return sta < end ? true : false;
                            }
                        }
                    }
                },
                end_time: {
                    validators: {
                        callback: {
                            message: '结束日期不能为空且需大于开始日期',
                            callback: function(value, validator, $field) {
                                var begin = $('#start_time').val();
                                if (begin == null || begin == '' || value == null || value == '') {
                                    return false;
                                }

                                var sta = Date.parse(new Date(begin));
                                var end = Date.parse(new Date(value));

                                $('#start_time').keypress();
                                validator.updateStatus('start_time', 'VALID');
                                return sta < end ? true : false;
                            }
                        }
                    }
                }
            }
        });
    }
}


var _app = new Vue({
    delimiters: ['[[', ']]'],
    el: "#app",
    mounted:function(){
        businessManager.init();
        tablebqs = $('#table-bqs').DataTable(datatable_bqs_options);
        export_tableid = 'table-bqs';
        export_name = '清单项目表';
    },
    data: {
        show_export_button:1,
        show_menu_button:1,
        can_export:0,
        resDatalist:[],
        taizhangData: {
            list: [],
            reportlist: []
        }
    },
    methods: {
        getresdatalist:function(id,type){
            var that = this;
            $.ajax({
                type: 'post',
                dataType: 'json',
                url: '/business/getbqtablelist/',
                data: {
                    'param[report_id]': id,
                    'param[report_type]':type
                },
                success: function(data) {
                    that.resDatalist = data.data;
                },
                error: function(data) {
                    alert('系统异常');
                }
            });
        },
        getaccountData: function(type, pact_id) {
            var that = this;
            console.log(pact_id);
            $.ajax({
                type: 'get',
                dataType: 'json',
                data: { type: type, pact_id: pact_id },
                url: '/business/loadAccountList/',
                success: function(data) {
                    if (data.issuc) {
                        that.taizhangData.list = data.datalist;
                        that.taizhangData.reportlist = data.reportlist;
                    }
                },
                error: function(data) {

                }
            });
        }
    }
});
