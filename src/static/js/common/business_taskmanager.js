var storage = null;
var mouse_key = 0; //鼠标点击，1：左键，2：右键
var uploadfile_qingdanStr = ''; //合同清单id字符串
var uploadfile_fujianStr = ''; //合同附件id字符串
var keeplist = new Object();
var currselectreport_id = '';
var tasktable,tablefenjian;
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
var datatable_options = {
    "dom": 'ltip',
    "iDisplayLength": 15,
    "lengthChange": false, //是否允许用户自定义显示数量
    "bPaginate": true, //翻页功能
    "bFilter": false, //列筛序功能
    "searching": false, //本地搜索
    "ordering": false, //排序功能
    "Info": false, //页脚信息
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
        "url": '/../../business/gettabletasks/',
        "type": 'POST',
    },

    "columns": [
    {
        "data": "name"
    },
    {
        "data": function(a) {
            return new Date(a.issuing_time * 1000).format('yyyy-MM-dd');
        }
    }, {
        "data": "professional"
    }, {
        "data": "quantities"
    }, {
        "data": function(a) {
            return (a.price).toFixed(2);
        }
    }, {
        "data": function(a) {
            return (a.price * a.quantities).toFixed(2);
        }
    }, {
        "data": "reportname"
    }, {
        "data": null
    }],

    columnDefs: [ //添加自定义按钮
        {
            targets: 7,
            render: function(a, b, c, d) {
                var html = '';
                if (a.reportlocked == 1) {
                    html = '<button type="button" class="btn btn-default btn-xs" onclick="_app.detailTaskorder(' + a.id + ',' + a.tasktype + ')">查看</button> <button type="button" class="btn btn-success btn-xs" onclick="_app.editTaskorder(' + a.id + ',' + a.tasktype + ',' + a.reportlocked + ')">编辑</button> <button type="button" class="btn btn-danger btn-xs" onclick="_app.delTaskorder(' + a.id + ',' + a.tasktype + ',' + a.reportlocked + ')">删除</button>';
                } else {
                    html = '<button type="button" class="btn btn-default btn-xs" onclick="_app.detailTaskorder(' + a.id + ',' + a.tasktype + ')">查看</button> <button type="button" class="btn btn-success btn-xs" onclick="_app.editTaskorder(' + a.id + ',' + a.tasktype + ',' + a.reportlocked + ')">编辑</button> <button type="button" class="btn btn-danger btn-xs" onclick="_app.delTaskorder(' + a.id + ',' + a.tasktype + ',' + a.reportlocked + ')">删除</button>';
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

//vue使用
var _app = new Vue({
    delimiters: ['[[', ']]'],
    el: "#app",
    data:{
        show_table_type:1,//1：显示实物量或者非实物量表格，2：显示分建表格
        taskshow_style:'display:show',
        fenjianshow_style:'display:none',
    },
    mounted:function(){
        var that = this;
        that.init();
    },
    methods:{
        init: function() {
            var that = this;
            tasktable = $('.datatable').DataTable(datatable_options);
            //使用col插件实现表格头宽度拖拽
            $(".datatable").colResizable();
            that.bindListener();
            that.filterInit();
            that.formValidator();
            that.jstreeInit();
        },

        bindListener: function() {
            var that = this;
            $("#tasksearch").bind("click", function() {
                keeplist.search_company = $("#search_company option:selected").val();
                tasktable.draw();
            });

            $(".table-fenjian").on("click", '.datatable .delurl', function() {
                var key = $(this).attr('data');

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

            $("#jstree_demo_div").bind("activate_node.jstree", function(obj, e) {
                if (mouse_key != 1)
                    return;
                var selectedid = e.node.id;
                curr_slectnode = selectedid;
                keeplist.search_physical = undefined;
                keeplist.search_report = undefined;
                keeplist.search_company = undefined;
                keeplist.search_task = undefined;
                console.log("当前选择：" + selectedid);
                currselectreport_id = selectedid.split('-')[1];
                keeplist = new Object();
                if(selectedid.split('-')[0]=='shiwuliang'){
                    that.fenjianshow_style = 'display:none';
                    that.taskshow_style = 'display:block';
                    keeplist.search_physical = 1;
                    keeplist.search_report = selectedid.split('-')[3]
                    that.$nextTick(function(){
                        if (tasktable == null) {
                            tasktable = $('.datatable').DataTable(datatable_options);
                        } else {
                            tasktable.draw();
                        }
                    });
                }else if(selectedid.split('-')[0]=='noshiwuliang'){
                    that.fenjianshow_style = 'display:none';
                    that.taskshow_style = 'display:block';
                    keeplist.search_physical = 0;
                    keeplist.search_report = selectedid.split('-')[3]

                    that.$nextTick(function(){
                        if (tasktable == null) {
                            tasktable = $('.datatable').DataTable(datatable_options);
                        } else {
                            tasktable.draw();
                        }
                    });
                }else if(selectedid.split('-')[0]=='fenjiancb'){
                    that.taskshow_style= 'display:none';
                    that.fenjianshow_style = 'display:block';
                    keeplist.report_type = 4;
                    keeplist.report_id = selectedid.split('-')[3]
                    that.$nextTick(function(){
                        if (tablefenjian == null) {
                            tablefenjian = $('.table-fenjian').DataTable(datatable_fenjian_options);
                        } else {
                            tablefenjian.draw();
                        }
                    });
                }

            });

            $("#taskorder_company").change(function() {
                $.ajax({
                    type: 'get',
                    dataType: 'json',
                    data: { company_id: $("#taskorder_company option:selected").val() },
                    url: '/business/getLaborpactsBycompany/',
                    success: function(data) {
                        if (data.labors.length == 0) {
                            $("#taskorder_pact").html('<option></option>');
                            var taskorder_pactprice = document.getElementById("taskorder_pactprice");
                            taskorder_pactprice.disabled = false;
                            taskorder_pactprice.value = '';
                        } else {
                            document.getElementById("taskorder_pact").options.length = 0;
                            var html = '';
                            $("#taskorder_pact").empty();

                            for (var i = 0; i < data.labors.length; i++) {
                                var item = data.labors[i];
                                if (i == 0) {
                                    var taskorder_pactprice = document.getElementById("taskorder_pactprice");
                                    taskorder_pactprice.disabled = true;
                                    taskorder_pactprice.value = item.taxprice;
                                }
                                html += '<option value="' + item.id + '" data="' + item.taxprice + '">' + item.name + '</option>';
                            }
                            $("#taskorder_pact").html(html);
                        }
                        $('#addTaskorderForm').data('bootstrapValidator').updateStatus('taskorder_pact', 'NOT_VALIDATED').validateField('taskorder_pact');
                    },
                    error: function(data) {}
                });
            });
            $(".selectpact").change(function() {
                var taskorder_pactprice = document.getElementById("taskorder_pactprice");
                taskorder_pactprice.disabled = true;
                taskorder_pactprice.value = $("#taskorder_pact option:selected").attr('data');
            });
            $("#addtask").bind("click", function() {
                $("#taskorder_issuetime").val(new Date().format("yyyy-MM-dd"));
                $("#addTaskorderDialog").modal("show");
            });
            $("#addtaskNophysical").bind("click", function() {
                $("#taskorderNophysical_issuetime").val(new Date().format("yyyy-MM-dd"));
                $("#addTaskorderNophysicalDialog").modal("show");
            });
            $("#taskorder_issuetime").bind("click", function() {
                $('#taskorder_issuetime').datetimepicker({
                    language: 'zh-CN', //显示中文
                    minView: 'month',
                    autoclose: true, //选中自动关闭
                    format: 'yyyy-mm-dd',
                }).on('hide', function(e) {
                    $('#addTaskorderForm').data('bootstrapValidator')
                        .updateStatus('taskorder_issuetime', 'NOT_VALIDATED', null)
                        .validateField('taskorder_issuetime');
                });
            });
            $("#taskorder_issuetime").click();
            $("#taskorderNophysical_issuetime").bind("click", function() {
                $('#taskorderNophysical_issuetime').datetimepicker({
                    language: 'zh-CN', //显示中文
                    minView: 'month',
                    autoclose: true, //选中自动关闭
                    format: 'yyyy-mm-dd',
                }).on('hide', function(e) {
                    $('#addTaskorderNophysicalForm').data('bootstrapValidator')
                        .updateStatus('taskorderNophysical_issuetime', 'NOT_VALIDATED', null)
                        .validateField('taskorderNophysical_issuetime');
                });
            });
            $("#taskorderNophysical_issuetime").click();

            $("#edit_taskorder_issuetime").bind("click", function() {
                $('#edit_taskorder_issuetime').datetimepicker({
                    language: 'zh-CN', //显示中文
                    minView: 'month',
                    autoclose: true, //选中自动关闭
                    format: 'yyyy-mm-dd',
                }).on('hide', function(e) { that.formValidator(); });
            });
            $("#edit_taskorder_issuetime").click();

            $("#edit_taskorderNophysical_issuetime").bind("click", function() {
                $('#edit_taskorderNophysical_issuetime').datetimepicker({
                    language: 'zh-CN', //显示中文
                    minView: 'month',
                    autoclose: true, //选中自动关闭
                    format: 'yyyy-mm-dd',
                }).on('hide', function(e) { that.formValidator(); });
            });
            $("#edit_taskorderNophysical_issuetime").click();

            $("#btnAddTaskNophysical").bind("click", function() {
                $('#addTaskorderNophysicalForm').bootstrapValidator('validate');
                if (!($('#addTaskorderNophysicalForm').data('bootstrapValidator').isValid())) {
                    return;
                }
                that.addTaskorderNophysical();
            });
            $("#btnAddTask").bind("click", function() {
                $('#addTaskorderForm').bootstrapValidator('validate');
                if (!($('#addTaskorderForm').data('bootstrapValidator').isValid())) {
                    return;
                }
                that.addTaskorder();
            });

            $("#addTaskorderDialog").on("hidden.bs.modal", function() {
                $("#addTaskorderForm").data('bootstrapValidator').destroy();
                $('#addTaskorderForm').data('bootstrapValidator', null);
                document.getElementById("addTaskorderForm").reset(); //清空表单
                that.formValidator();
            });
            $("#addTaskorderDialog").on("hidden.bs.modal", function() {
                $("#addTaskorderForm").data('bootstrapValidator').destroy();
                $('#addTaskorderForm').data('bootstrapValidator', null);
                document.getElementById("addTaskorderForm").reset(); //清空表单
                that.formValidator();
            });
            $("#addTaskorderNophysicalDialog").on("hidden.bs.modal", function() {
                $("#addTaskorderNophysicalForm").data('bootstrapValidator').destroy();
                $('#addTaskorderNophysicalForm').data('bootstrapValidator', null);
                document.getElementById("addTaskorderNophysicalForm").reset(); //清空表单
                that.formValidator();
            });

            $("#btnEditTask").bind("click", function() {
                $('#editTaskorderForm').bootstrapValidator('validate');
                if (!($('#editTaskorderForm').data('bootstrapValidator').isValid())) {
                    return;
                }
                that.editAction();
            });

            $("#editTaskorderDialog").on("hidden.bs.modal", function() {
                $("#editTaskorderForm").data('bootstrapValidator').destroy();
                $('#editTaskorderForm').data('bootstrapValidator', null);
                that.formValidator();
            });
            $("#btnEditTaskNophysical").bind("click", function() {
                $('#editTaskorderNophysicalForm').bootstrapValidator('validate');
                if (!($('#editTaskorderNophysicalForm').data('bootstrapValidator').isValid())) {
                    return;
                }
                that.editActionNophysical();
            });

            $("#editTaskorderNophysicalDialog").on("hidden.bs.modal", function() {
                $("#editTaskorderNophysicalForm").data('bootstrapValidator').destroy();
                $('#editTaskorderNophysicalForm').data('bootstrapValidator', null);
                that.formValidator();
            });
        },

        editTaskorder: function(id, tasktype, locked) {
            if (locked == 1) {
                alert("关联产值报告已经上报，无法删除或修改");
                return;
            }
            $.ajax({
                type: 'get',
                dataType: 'json',
                url: '/business/getTaskorderByid/',
                data: { id: id, tasktype: tasktype },
                success: function(data) {
                    if (data.issuc) {
                        var taskorderinfo = data.taskorder;
                        if (tasktype == 1) {
                            $("#edit_taskorder_company").val(taskorderinfo.company_id);
                            $("#edit_taskorder_pact").val(taskorderinfo.pact_id);
                            $("#edit_taskorder_report").val(taskorderinfo.report_id);
                            $("#edit_taskorder_id").val(id);
                            $("#edit_taskorder_tasktype").val(tasktype);
                            $("#edit_taskorder_quantities").val(taskorderinfo.quantities);
                            $("#edit_taskorder_unit").val(taskorderinfo.unit);
                            $("#edit_taskorder_professional").val(taskorderinfo.professional_id);
                            $("#edit_taskorder_issuetime").val(taskorderinfo.issuing_time);
                            $("#edit_taskorder_pactprice").val(taskorderinfo.price);
                            $("#edit_taskorder_description").val(taskorderinfo.description);
                            $("#editTaskorderDialog").modal("show");
                        } else {
                            $("#edit_taskorderNophysical_worktype").val(taskorderinfo.worktype);
                            $("#edit_taskorderNophysical_company").val(taskorderinfo.company_id);
                            // $("#edit_taskorderNophysical_pact").val(taskorderinfo.pact_id);
                            $("#edit_taskorderNophysical_report").val(taskorderinfo.report_id);
                            $("#edit_taskorderNophysical_id").val(id);
                            $("#edit_taskorder_tasktype").val(tasktype);
                            $("#edit_taskorderNophysical_quantities").val(taskorderinfo.quantities);
                            $("#edit_taskorderNophysical_unit").val(taskorderinfo.unit);
                            $("#edit_taskorderNophysical_professional").val(taskorderinfo.professional_id);
                            $("#edit_taskorderNophysical_issuetime").val(taskorderinfo.issuing_time);
                            $("#edit_taskorderNophysical_pactprice").val(taskorderinfo.price);
                            $("#edit_taskorderNophysical_description").val(taskorderinfo.description);
                            $("#editTaskorderNophysicalDialog").modal("show");
                        }
                    }
                },
                error: function(data) {}
            });
        },
        editActionNophysical: function() {
            var taskorder_description = $("#edit_taskorderNophysical_description").val();
            var taskorder_pactprice = $("#edit_taskorderNophysical_pactprice").val();
            var taskorder_quantities = $("#edit_taskorderNophysical_quantities").val();
            var taskorder_id = $("#edit_taskorderNophysical_id").val();
            var taskorder_issuetime = $("#edit_taskorderNophysical_issuetime").val();
            var taskorder_professional = $("#edit_taskorderNophysical_professional option:selected").val();
            var taskorder_company = $("#edit_taskorderNophysical_company option:selected").val();
            var taskorder_pact = $("#edit_taskorderNophysical_pact option:selected").val();
            var taskorder_report = $("#edit_taskorderNophysical_report option:selected").val();
            var taskorder_unit = $("#edit_taskorderNophysical_unit").val();
            var taskorder_worktype = $("#edit_taskorderNophysical_worktype").val();
            alertConfirm("确定修改该记录吗？", null, function() {
                $.ajax({
                    type: "get",
                    url: "/business/updateTaskorder/",
                    dataType: "json",
                    data: {
                        "taskorder_type": 2,
                        "taskorder_unit": taskorder_unit,
                        "taskorder_report": taskorder_report,
                        "taskorder_pact": taskorder_pact,
                        "taskorder_quantities": taskorder_quantities,
                        "taskorder_id": taskorder_id,
                        "taskorder_price": taskorder_pactprice,
                        "taskorder_issuetime": taskorder_issuetime,
                        "taskorder_professional": taskorder_professional,
                        "taskorder_company": taskorder_company,
                        "taskorder_description": taskorder_description,
                        "taskorder_worktype": taskorder_worktype,
                    },
                    success: function(data) {
                        if (data.issuc = "true") {
                            alert("数据已经更新", null, function() {
                                $("#editTaskorderNophysicalDialog").modal("hide");
                                tasktable.draw();
                            });

                        } else {}
                    },
                    error: function(data) {}
                });
            });
        },
        editAction: function() {
            var taskorder_description = $("#edit_taskorder_description").val();
            var taskorder_pactprice = $("#edit_taskorder_pactprice").val();
            var taskorder_quantities = $("#edit_taskorder_quantities").val();
            var taskorder_id = $("#edit_taskorder_id").val();
            var taskorder_issuetime = $("#edit_taskorder_issuetime").val();
            var taskorder_professional = $("#edit_taskorder_professional option:selected").val();
            var taskorder_company = $("#edit_taskorder_company option:selected").val();
            var taskorder_pact = $("#edit_taskorder_pact option:selected").val();
            var taskorder_report = $("#edit_taskorder_report option:selected").val();
            var taskorder_unit = $("#edit_taskorder_unit").val();
            alertConfirm("确定修改该记录吗？", null, function() {
                $.ajax({
                    type: "get",
                    url: "/business/updateTaskorder/",
                    dataType: "json",
                    data: {
                        "taskorder_type": 1,
                        "taskorder_unit": taskorder_unit,
                        "taskorder_report": taskorder_report,
                        "taskorder_pact": taskorder_pact,
                        "taskorder_quantities": taskorder_quantities,
                        "taskorder_id": taskorder_id,
                        "taskorder_price": taskorder_pactprice,
                        "taskorder_issuetime": taskorder_issuetime,
                        "taskorder_professional": taskorder_professional,
                        "taskorder_company": taskorder_company,
                        "taskorder_description": taskorder_description,
                    },
                    success: function(data) {
                        if (data.issuc = "true") {
                            alert("数据已经更新", null, function() {
                                console.log('数据更新隐藏模态框');
                                $("#editTaskorderDialog").modal("hide");
                                tasktable.draw();
                            });

                        } else {}
                    },
                    error: function(data) {}
                });
            });
        },
        detailTaskorder: function(id, tasktype) {
            $.ajax({
                type: 'get',
                dataType: 'json',
                url: '/business/getTaskorderByid/',
                data: { id: id, tasktype: tasktype },
                success: function(data) {
                    if (data.issuc) {
                        var taskorderinfo = data.taskorder;
                        if (tasktype == 1) {
                            $("#detail_taskorder_company").val(taskorderinfo.company_id);
                            $("#detail_taskorder_pact").val(taskorderinfo.pact_id);
                            $("#detail_taskorder_report").val(taskorderinfo.report_name);
                            $("#detail_taskorder_id").val(id);
                            $("#detail_taskorder_quantities").val(taskorderinfo.quantities);
                            $("#detail_taskorder_unit").val(taskorderinfo.unit);
                            $("#detail_taskorder_professional").val(taskorderinfo.professional_id);
                            $("#detail_taskorder_issuetime").val(taskorderinfo.issuing_time);
                            $("#detail_taskorder_price").val(taskorderinfo.price);
                            $("#detail_taskorder_description").val(taskorderinfo.description);
                            $("#detailTaskorderDialog").modal("show");
                        } else {
                            $("#detail_taskorderNophysical_worktype").val(taskorderinfo.worktype);
                            $("#detail_taskorderNophysical_company").val(taskorderinfo.company_id);
                            $("#detail_taskorderNophysical_pact").val(taskorderinfo.pact_id);
                            $("#detail_taskorderNophysical_report").val(taskorderinfo.report_name);
                            $("#detail_taskorderNophysical_id").val(id);
                            $("#detail_taskorderNophysical_quantities").val(taskorderinfo.quantities);
                            $("#detail_taskorderNophysical_unit").val(taskorderinfo.unit);
                            $("#detail_taskorderNophysical_professional").val(taskorderinfo.professional_id);
                            $("#detail_taskorderNophysical_issuetime").val(taskorderinfo.issuing_time);
                            $("#detail_taskorderNophysical_price").val(taskorderinfo.price);
                            $("#detail_taskorderNophysical_description").val(taskorderinfo.description);
                            $("#detailTaskorderNophysicalDialog").modal("show");
                        }
                    }
                },
                error: function(data) {}
            });
        },
        delTaskorder: function(id, tasktype, locked) {
            if (locked == 1) {
                alert("关联产值报告已经上报，无法删除");
                return;
            }

            alertConfirm("确定删除该记录？", null, function() {
                $.ajax({
                    type: 'get',
                    dataType: 'json',
                    url: '/business/delTaskorderByid/',
                    data: { id: id, tasktype: tasktype },
                    success: function(data) {
                        if (data.issuc) {
                            alert("删除成功", null, function() {
                                tasktable.draw();
                                $('#jstree_demo_div').jstree().refresh();
                            });
                        } else {
                            alert(data.msg);
                        }
                    },
                    error: function(data) {}
                });
            });
        },
        addTaskorderNophysical: function() {
            var taskorder_pactprice = $("#taskorderNophysical_pactprice").val();
            var taskorder_issuetime = $("#taskorderNophysical_issuetime").val();
            var taskorder_professional = $("#taskorderNophysical_professional option:selected").val();
            var taskorder_company = $("#taskorderNophysical_company option:selected").val();
            var taskorder_quantities = $("#taskorderNophysical_quantities").val();
            var taskorder_description = $("#taskorderNophysical_description").val();
            // var taskorder_pact = $("#taskorderNophysical_pact option:selected").val();
            var taskorder_report = $("#taskorderNophysical_report option:selected").val();
            var taskorder_unit = $("#taskorderNophysical_unit").val();
            var taskorderNophysical_worktype = $("#taskorderNophysical_worktype").val();
            $.ajax({
                type: "get",
                url: "/business/addTaskorder/",
                dataType: "json",
                data: {
                    "operatetype": 2,
                    "taskorder_pactprice": taskorder_pactprice,
                    "taskorder_issuetime": taskorder_issuetime,
                    "taskorder_professional": taskorder_professional,
                    "taskorder_company": taskorder_company,
                    "taskorder_quantities": taskorder_quantities,
                    "taskorder_description": taskorder_description,
                    "taskorder_report": taskorder_report,
                    // "taskorder_pact":taskorder_pact,
                    "taskorder_unit": taskorder_unit,
                    "taskorderNophysical_worktype": taskorderNophysical_worktype
                },
                success: function(data) {
                    if (data.issuc) {
                        alert("添加成功", null, function() {
                            $("#addTaskorderNophysicalDialog").modal("hide");
                            tasktable.draw();
                            $('#jstree_demo_div').jstree().refresh();
                        });
                    } else {
                        alert(data.msg);
                    }
                },
                error: function(data) {}
            });
        },
        addTaskorder: function() {
            var taskorder_pactprice = $("#taskorder_pactprice").val();
            var taskorder_issuetime = $("#taskorder_issuetime").val();
            var taskorder_professional = $("#taskorder_professional option:selected").val();
            var taskorder_company = $("#taskorder_company option:selected").val();
            var taskorder_quantities = $("#taskorder_quantities").val();
            var taskorder_description = $("#taskorder_description").val();
            var taskorder_pact = $("#taskorder_pact option:selected").val();
            var taskorder_report = $("#taskorder_report option:selected").val();
            var taskorder_unit = $("#taskorder_unit").val();
            $.ajax({
                type: "get",
                url: "/business/addTaskorder/",
                dataType: "json",
                data: {
                    "operatetype": 1,
                    "taskorder_pactprice": taskorder_pactprice,
                    "taskorder_issuetime": taskorder_issuetime,
                    "taskorder_professional": taskorder_professional,
                    "taskorder_company": taskorder_company,
                    "taskorder_quantities": taskorder_quantities,
                    "taskorder_description": taskorder_description,
                    // "uploadfile_fujianStr": uploadfile_fujianStr,
                    "taskorder_report": taskorder_report,
                    "taskorder_pact": taskorder_pact,
                    "taskorder_unit": taskorder_unit
                },
                success: function(data) {
                    if (data.issuc) {
                        alert("添加成功", null, function() {
                            $("#addTaskorderDialog").modal("hide");
                            tasktable.draw();
                            $('#jstree_demo_div').jstree().refresh();
                        });
                    } else {
                        alert(data.msg);
                    }
                },
                error: function(data) {}
            });
        },


        filterInit: function() {
            var that = this;
            $('#uploadfile_fujian').filer({
                showThumbs: true,
                addMore: true,
                allowDuplicates: false,
                captions: {
                    button: "添加文件",
                    feedback: "",
                    feedback2: "个文件已选择",
                    drop: "拖到文件到这里",
                    removeConfirmation: "确定删除该文件吗？",
                    errors: {
                        filesLimit: "只能同时上传 1个文件 。",
                        filesType: "只能上传MicrosoftProject文件",
                        filesSize: "1太大! 最大允许上传 1 MB。",
                        filesSizeAll: "Files you've choosed are too large! Please upload files up to 1MB。",
                        folderUpload: "不允许上传文件夹。"
                    }
                },
                uploadFile: {
                    url: "/uploadfile_conc2/",
                    data: null,
                    type: 'POST',
                    enctype: 'multipart/form-data',
                    beforeSend: function() {},
                    success: function(data, el) {
                        if (data.issuc == "true") {
                            el.attr("value", data.docId);
                            // console.log(data.docId);
                            if (uploadfile_fujianStr == "") {
                                uploadfile_fujianStr += data.docId;
                            } else {
                                uploadfile_fujianStr += '#' + data.docId;
                            }
                        }
                    },
                    error: function(el) {},
                    statusCode: null,
                    onProgress: null,
                    onComplete: null
                },
                onRemove: function(itemEl, file) {
                    var fileid = itemEl.attr("value")
                    $.post('/del_uploadfile/', { fileid: fileid });
                }
            });

            $('#uploadfile_qingdan').filer({
                showThumbs: true,
                addMore: true,
                allowDuplicates: false,
                captions: {
                    button: "添加文件",
                    feedback: "",
                    feedback2: "个文件已选择",
                    drop: "拖到文件到这里",
                    removeConfirmation: "确定删除该文件吗？",
                    errors: {
                        filesLimit: "只能同时上传 1个文件 。",
                        filesType: "只能上传MicrosoftProject文件",
                        filesSize: "1太大! 最大允许上传 1 MB。",
                        filesSizeAll: "Files you've choosed are too large! Please upload files up to 1MB。",
                        folderUpload: "不允许上传文件夹。"
                    }
                },
                uploadFile: {
                    url: "/uploadfile_conc2/",
                    data: null,
                    type: 'POST',
                    enctype: 'multipart/form-data',
                    beforeSend: function() {},
                    success: function(data, el) {
                        console.log(data);
                        if (data.issuc == "true") {
                            el.attr("value", data.docId);
                            if (uploadfile_qingdanStr == "") {
                                uploadfile_qingdanStr += data.docId;
                            } else {
                                uploadfile_qingdanStr += '#' + data.docId;
                            }
                        }
                    },
                    error: function(el) {},
                    statusCode: null,
                    onProgress: null,
                    onComplete: null
                },
                onRemove: function(itemEl, file) {
                    var fileid = itemEl.attr("value")
                    $.post('/del_uploadfile/', { fileid: fileid });
                }
            });
        },

        jstreeInit: function() {
            var curr_jstree = $('#jstree_demo_div').jstree({
                'core': {
                    'data': {
                        'url': '/business/get_task_tree/',
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

        formValidator: function() {
            $('#addTaskorderForm').bootstrapValidator({
                message: 'This value is not valid',
                feedbackIcons: {
                    valid: 'glyphicon glyphicon-ok',
                    invalid: 'glyphicon glyphicon-remove',
                    validating: 'glyphicon glyphicon-refresh'
                },
                fields: {
                    taskorder_company: {
                        validators: {
                            notEmpty: {
                                message: '分包商不能为空'
                            },

                        }
                    },
                    taskorder_quantities: {
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
                    taskorder_pactprice: {
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
                    taskorder_issuetime: {
                        validators: {
                            notEmpty: {
                                message: '时间不能为空'
                            },
                        }
                    },
                    taskorder_professional: {
                        validators: {
                            notEmpty: {
                                message: '专业不能为空'
                            },
                        }
                    },
                    taskorder_unit: {
                        validators: {
                            notEmpty: {
                                message: '单位不能为空'
                            },
                        }
                    },
                    taskorder_report: {
                        validators: {
                            notEmpty: {
                                message: '报表不能为空'
                            },
                        }
                    },
                    taskorder_pact: {
                        validators: {
                            notEmpty: {
                                message: '分包不能为空'
                            },
                            // callback:{
                            //   message:'xuxxx',
                            //   callback:function(value, validator,$field,options){
                            //     console.log(value);
                            //     return false;
                            //   }
                            // }
                        }
                    },
                    taskorder_description: {
                        validators: {
                            stringLength: {
                                max: 100,
                                message: '描述在0-100字之间'
                            },
                        }
                    }
                }
            });

            $('#addTaskorderNophysicalForm').bootstrapValidator({
                message: 'This value is not valid',
                feedbackIcons: {
                    valid: 'glyphicon glyphicon-ok',
                    invalid: 'glyphicon glyphicon-remove',
                    validating: 'glyphicon glyphicon-refresh'
                },
                fields: {
                    taskorderNophysical_company: {
                        validators: {
                            notEmpty: {
                                message: '分包商不能为空'
                            }
                        }
                    },
                    taskorderNophysical_quantities: {
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
                    taskorderNophysical_pactprice: {
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
                    taskorderNophysical_issuetime: {
                        validators: {
                            notEmpty: {
                                message: '时间不能为空'
                            },
                        }
                    },
                    taskorderNophysical_professional: {
                        validators: {
                            notEmpty: {
                                message: '专业不能为空'
                            },
                        }
                    },
                    taskorderNophysical_unit: {
                        validators: {
                            notEmpty: {
                                message: '单位不能为空'
                            },
                        }
                    },
                    taskorderNophysical_worktype: {
                        validators: {
                            notEmpty: {
                                message: '工种不能为空'
                            },
                        }
                    },
                    taskorderNophysical_report: {
                        validators: {
                            notEmpty: {
                                message: '报表不能为空'
                            },
                        }
                    },
                    // taskorderNophysical_pact:{
                    //   validators:{
                    //     notEmpty:{
                    //       message:'分包不能为空'
                    //     },
                    //   }
                    // },
                    taskorderNophysical_description: {
                        validators: {
                            stringLength: {
                                max: 100,
                                message: '描述在0-100字之间'
                            },
                        }
                    }
                }
            });

            $('#editTaskorderForm').bootstrapValidator({
                message: 'This value is not valid',
                feedbackIcons: {
                    valid: 'glyphicon glyphicon-ok',
                    invalid: 'glyphicon glyphicon-remove',
                    validating: 'glyphicon glyphicon-refresh'
                },
                fields: {
                    edit_taskorder_company: {
                        validators: {
                            notEmpty: {
                                message: '分包商不能为空'
                            }
                        }
                    },
                    edit_taskorder_quantities: {
                        validators: {
                            notEmpty: {
                                message: '工程量不能为空'
                            },
                            regexp: {
                                regexp: /^[0-9]+([.]{1}[0-9]+){0,1}$/,
                                message: '格式不对，请输入正确的工程量', //

                            }
                        }
                    },
                    edit_taskorder_pactprice: {
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
                    edit_taskorder_issuetime: {
                        validators: {
                            notEmpty: {
                                message: '时间不能为空'
                            },
                        }
                    },
                    edit_taskorder_professional: {
                        validators: {
                            notEmpty: {
                                message: '专业不能为空'
                            },
                        }
                    },
                    edit_taskorder_unit: {
                        validators: {
                            notEmpty: {
                                message: '单位不能为空'
                            },
                        }
                    },
                    edit_taskorder_report: {
                        validators: {
                            notEmpty: {
                                message: '报表不能为空'
                            },
                        }
                    },
                    edit_taskorder_pact: {
                        validators: {
                            notEmpty: {
                                message: '分包不能为空'
                            },
                        }
                    },
                    edit_taskorder_description: {
                        validators: {
                            stringLength: {
                                max: 100,
                                message: '描述在0-100字之间'
                            },
                        }
                    }
                }
            });

            $('#editTaskorderNophysicalForm').bootstrapValidator({
                message: 'This value is not valid',
                feedbackIcons: {
                    valid: 'glyphicon glyphicon-ok',
                    invalid: 'glyphicon glyphicon-remove',
                    validating: 'glyphicon glyphicon-refresh'
                },
                fields: {
                    edit_taskorderNophysical_company: {
                        validators: {
                            notEmpty: {
                                message: '分包商不能为空'
                            }
                        }
                    },
                    edit_taskorderNophysical_quantities: {
                        validators: {
                            notEmpty: {
                                message: '人工日不能为空'
                            },
                            regexp: {
                                regexp: /^[0-9]+([.]{1}[0-9]+){0,1}$/,
                                message: '格式不对，请输入正确的人工日', //

                            }
                        }
                    },
                    edit_taskorderNophysical_pactprice: {
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
                    edit_taskorderNophysical_issuetime: {
                        validators: {
                            notEmpty: {
                                message: '时间不能为空'
                            },
                        }
                    },
                    edit_taskorderNophysical_professional: {
                        validators: {
                            notEmpty: {
                                message: '专业不能为空'
                            },
                        }
                    },
                    edit_taskorderNophysical_unit: {
                        validators: {
                            notEmpty: {
                                message: '单位不能为空'
                            },
                        }
                    },
                    edit_taskorderNophysical_worktype: {
                        validators: {
                            notEmpty: {
                                message: '工种不能为空'
                            },
                        }
                    },
                    edit_taskorderNophysical_report: {
                        validators: {
                            notEmpty: {
                                message: '报表不能为空'
                            },
                        }
                    },
                    edit_taskorderNophysical_description: {
                        validators: {
                            stringLength: {
                                max: 100,
                                message: '描述在0-100字之间'
                            },
                        }
                    }
                }
            });
        }
    }
});
