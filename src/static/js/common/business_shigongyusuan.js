var datatable_options = {
   "dom": 'ltip',
   "iDisplayLength": 15,
   "lengthChange": false,//是否允许用户自定义显示数量
   "bPaginate": true, //翻页功能
   "bFilter": false, //列筛序功能
   "searching": false,//本地搜索
   "ordering": false, //排序功能
   "Info": true,//页脚信息
   "autoWidth": true,//自动宽度
   "oLanguage": {//国际语言转化
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
      "url":'/../../business/getbudgetComponentQuantities/',
      "type":'POST',
    },

    "columns": [{
      "data": "code"
    }, {
      "data": "name"
    }, {
      "data": "description"
    } , {
      "data": "valueQuantity"
    }, {
      "data": "costQuantity"
    }],
    //向服务器传额外的参数
    "fnServerParams": function(aoData) {
      aoData.param = keeplist;
    },
};
var budgettable,jstree_demo;
var keeplist = new Object();



var businessManager = {
  init : function(){
    var that = this;
    that.bindListener();
    jstree_demo = that.jstreeInit();
    that.filterInit();
    that.formValidator();
    that.edittableinit();
  },
  addrule:function(bqitemid,unit){
      var that = this;
      alertConfirm("确定要添加吗?",null,function(){
        console.log(bqitemid);
        $.ajax({
          type: "post",
          url: "/business/updateYusuanRule/",
          dataType: "json",
          data: {bqitem_id:bqitemid,unit:unit,name:'addrule'},
          success: function(data) {
            if(data.issucc){
              alert("添加成功",null,function(){
                window.location.reload();
              });
            }else{
              alert(data.msg,null,function(){
              });
            }
          },
          error: function(data) {}
        });
      });
    },
  edittableinit:function(){
    $(".edit-table-liex").editable({
        validate: function (value) { //字段验证
            if (!$.trim(value)) {
                return '不能为空';
            }else{}
        },
        success: function(a,b,c){
          console.log(JSON.stringify(a));
          window.location.reload();
        }
      });
    $(".edit-table-type").editable({
        validate: function (value) { //字段验证
            if (!$.trim(value)) {
                return '不能为空';
            }else{}
        },
        success: function(a,b,c){
          console.log(JSON.stringify(a));
          window.location.reload();
        }
      });
    $(".edit-table-shuxing").editable({
        validate: function (value) { //字段验证
            if (!$.trim(value)) {
                return '不能为空';
            }else{}
        },
        success: function(a,b,c){
          console.log(JSON.stringify(a));
          window.location.reload();
        }
      });


    $('.edit-table-select2').editable({
          source: sourceoptions2,
          select2: {
              width: 200,
              placeholder: '选择分建或者任务',
              allowClear: true,
          },
          url :function(params) {
            console.log(JSON.stringify(params));
            $.ajax({
              type: "post",
              url: "/business/updateYusuanRule/",
              dataType: "json",
              data: {pk:params.name,name:params.value.split('-')[0],value:params.value.split('-')[1],bqitem_id:params.pk},
              success: function(data) {
                if(data.issucc){
                  alert("修改成功",null,function(){
                    window.location.reload();
                  });
                }else{
                  alert(data.msg,null,function(){
                    // window.location.reload();
                  });
                }
              },
              error: function(data) {}
            });
          },
          validate: function (value) { //字段验证
              if (!$.trim(value)) {
                  return '不能为空';
              }else{}
          },
      });
  },
  bindListener:function(){
    var that = this;
    $("#jstree_demo_div").bind("activate_node.jstree", function(obj, e){
      var selectedid = e.node.id;
      if(common_data.menubox_key==1){
        if(selectedid!='root'&&selectedid!='budgethuizong'&&selectedid!='chengben'&&selectedid!='rule'){
          keeplist.budget_id = selectedid;
          console.log(selectedid);
          if(budgettable==null){
            budgettable = $("#budgettbs").DataTable(datatable_options);
            $(".budgetxuqiu").addClass("table-unactive").removeClass("table-active");
            $(".budgethuizong").addClass("table-unactive").removeClass("table-active");
            $(".budgettbs").addClass("table-active").removeClass("table-unactive");

          }else{
            budgettable.draw();

            $(".budgetxuqiu").addClass("table-unactive").removeClass("table-active");
            $(".budgethuizong").addClass("table-unactive").removeClass("table-active");
            $(".budgettbs").addClass("table-active").removeClass("table-unactive");
          }
          $("#addrequirerow").hide();
          $("#uploadyusuanrule").hide();
          $("#yusuanrule").show();
          $("#adddaochu").show();
          $("#adddaochu_b").hide();
          history.pushState({},'','/business/shigongyusuan/')
        }else if(selectedid=='budgethuizong'){
          window.location.href = '/business/shigongyusuan/?status=2'
        }else if(selectedid=='rule'){
          window.location.href = '/business/shigongyusuan/?status=1'
        }
      }
    });

    $(".calc-tr").on("click",".rowdel",function(){
      var calc_id = $(this).attr("data");
      alertConfirm("确定删除吗",null,function(){
        $.ajax({
          type:'get',
          dataType:'json',
          url:'/business/delcalcrelation/',
          data:{calc_id:calc_id},
          success:function(data){
            if(data.issuc){
              alert("删除成功",null,function(){
                window.location.reload();
              });
            }else{
              alert(data.msg);
            }
          },
          error:function(data){alert("删除失败");}
        });
      });
    });

    $("#btnAddRequirementRow").bind("click",function(){
      $('#addRequirementsRowForm').bootstrapValidator('validate');
      if(!($('#addRequirementsRowForm').data('bootstrapValidator').isValid())){
        return ;
      }
      that.addAddRequirementsRow();
    });

    $("#btnAddBudget").bind("click",function(){
      $('#addBudgetForm').bootstrapValidator('validate');
      if(!($('#addBudgetForm').data('bootstrapValidator').isValid())){
        return ;
      }
      that.addAddBudget("btnAddBudget");
    });

    $("#addBudgetDialog").on("hidden.bs.modal",function(){
      $("#addBudgetForm").data('bootstrapValidator').destroy();
      $('#addBudgetForm').data('bootstrapValidator', null);
      document.getElementById("addBudgetForm").reset();//清空表单
      that.formValidator();
    });
    $("#btnAddRequirement").bind("click",function(){
      $('#addRequirementsForm').bootstrapValidator('validate');
      if(!($('#addRequirementsForm').data('bootstrapValidator').isValid())){
        return ;
      }
      that.addAddRequirement("btnAddRequirement");
    });

    $("#addRequirementsDialog").on("hidden.bs.modal",function(){
      $("#addRequirementsForm").data('bootstrapValidator').destroy();
      $('#addRequirementsForm').data('bootstrapValidator', null);
      document.getElementById("addRequirementsForm").reset();//清空表单
      that.formValidator();
    });

    $("#addRequirementsRowDialog").on("hidden.bs.modal",function(){
      $("#addRequirementsRowForm").data('bootstrapValidator').destroy();
      $('#addRequirementsRowForm').data('bootstrapValidator', null);
      document.getElementById("addRequirementsRowForm").reset();//清空表单
      that.formValidator();
    });
  },

  addAddRequirementsRow:function(){
    var require_row_name = $("#require_row_name").val();
    var require_row_category = $("#require_row_category").val();
    var require_row_bqitem = $("#require_row_bqitem option:selected").val();
    var require_row_scitem = $("#require_row_scitem option:selected").val();
    var require_row_valueunit = $("#require_row_valueunit").val();
    var require_row_costunit = $("#require_row_costunit").val();
    var require_row_desc = $("#require_row_desc").val();
    $.ajax({
      type:'get',
      dataType:'json',
      data:{
        require_row_name:require_row_name.trim(),
        require_row_category:require_row_category.trim(),
        require_row_bqitem:require_row_bqitem,
        require_row_scitem:require_row_scitem,
        require_row_valueunit:require_row_valueunit,
        require_row_costunit:require_row_costunit,
        require_row_desc:require_row_desc,
      },
      url:'/business/addbudget_requirerow/',
      success:function(data){
        if(data.issuc){
          alert("添加成功",null,function(){window.location.reload()});
        }else{
          alert(data.msg,null,function(){
            $("#addRequirementsRowDialog").modal("hide");
          });
        }
      },
      error:function(data){}
    });
  },
  addAddBudget:function(butid){
    if(common_data.uploadfile_budget==""){
      alert("请上传施工预算execl");
      return ;
    }
    $(".pro-loading").fadeIn();
    var name = $("#budget_name").val();
    var description = $("#budget_yusuan option:selected").val();
    var scrmodel_id = $("#budget_filename option:selected").val();
    var buttonel = document.getElementById(butid);
    console.log('---------'+description);
    buttonel.disabled = true;
    $.ajax({
      type:'get',
      dataType:'json',
      data:{
        name:name,
        description:description,
        docid:common_data.uploadfile_budget,
        scrmodel_id:scrmodel_id
      },
      url:'/business/addbudget_construct',
      success:function(data){
        $(".pro-loading").fadeOut();
        if(data.issuc){
          alert("上传成功",null,function(){
            window.location.reload();
          });
        }else{
          alert("上传失败");
        }
      },
      error:function(data){
        buttonel.disabled = false;
        $(".pro-loading").fadeOut();
      }
    });
  },

  addAddRequirement:function(butid){
    if(common_data.uploadfile_requirement==""){
      alert("请上传计算要求execl");
      return ;
    }
    $(".pro-loading").fadeIn();
    var buttonel = document.getElementById(butid);
    buttonel.disabled = true;
    $.ajax({
      type:'get',
      dataType:'json',
      data:{
        docid:common_data.uploadfile_requirement
      },
      url:'/business/addbudget_requirement',
      success:function(data){
        $(".pro-loading").fadeOut();
        if(data.issuc){
          alert("添加成功",null,function(){window.location.reload();});
        }else{
          alert(data.msg,null,function(){window.location.href = '/business/fenbaopact/';});
        }
      },
      error:function(data){
        $(".pro-loading").fadeOut();
      }
    });
  },

  jstreeInit : function(){
    return $('#jstree_demo_div').jstree({
      'core': {
          'data':{
            'url' : '/business/get_budget_tree/',
            'data' : function (node) {
                  return { 'id' : node.id };
              }
            }
      },
      "plugins": [
          "wholerow","themes", "json_data","contextmenu"
      ],
      "contextmenu": {
          "items": function (node) {
              var temp = {
                  "deletebudget": {
                      "label": "删除",
                      "icon":"fa fa-times",
                      // "separator_after": true,
                      "action": function (data) {
                        alertConfirm("确定删除 "+node.text+" 吗?",null,function(){
                          $.ajax({
                            type:'get',
                            dataType:'json',
                            url:'/business/deleteBudget/',
                            data:{budget_id:node.id},
                            success:function(data){
                              if(data.issuc){
                                alert("删除成功",null,function(){
                                  $('#jstree_demo_div').jstree(true).delete_node(node);
                                  $('#jstree_demo_div').jstree(true).refresh()
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
              };
              /**
               * 如果选择不是所想节点，则不出右键菜单项
               */
              var menu = {};
              if(node.parent=="chengben"){
                return temp;
              }else{
                return menu;
              }
          },
          "select_node": false
      },
    });
  },

  filterInit : function(){
    var that = this;
    $('#uploadfile_budget').filer({
        showThumbs: true,
        addMore: true,
        limit:1,
        allowDuplicates: false,
        captions:{
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
            url: "/uploadfile_conc/",
            data: null,
            type: 'POST',
            enctype: 'multipart/form-data',
            beforeSend: function(){},
            success: function(data, el){
                if (data.issuc=="true"){
                    el.attr("value",data.docId);
                    common_data.uploadfile_budget=data.docId;
                }
            },
            error: function(el){},
            statusCode: null,
            onProgress: null,
            onComplete: null
        },
        onRemove: function(itemEl, file){
            var fileid = itemEl.attr("value")
            $.post('/del_uploadfile/', {fileid: fileid});
        }
    });

    $('#uploadfile_requirement').filer({
        showThumbs: true,
        addMore: true,
        limit:1,
        allowDuplicates: false,
        captions:{
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
            url: "/uploadfile_conc/",
            data: null,
            type: 'POST',
            enctype: 'multipart/form-data',
            beforeSend: function(){},
            success: function(data, el){
                if (data.issuc=="true"){
                    el.attr("value",data.docId);
                    common_data.uploadfile_requirement=data.docId;
                }
            },
            error: function(el){},
            statusCode: null,
            onProgress: null,
            onComplete: null
        },
        onRemove: function(itemEl, file){
            var fileid = itemEl.attr("value")
            $.post('/del_uploadfile/', {fileid: fileid});
        }
    });
  },

  formValidator :function(){
    $('#addBudgetForm').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
          valid: 'glyphicon glyphicon-ok',
          invalid: 'glyphicon glyphicon-remove',
          validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
          budget_name: {
            validators: {
                notEmpty: {
                    message: '预算名称不能为空'
                }
            }
          },
          budget_filename: {
            validators: {
                notEmpty: {
                    message: '源文件名不能为空'
                }
            }
          },
          budget_yusuan: {
            validators: {
                notEmpty: {
                    message: '关联预算不能为空'
                }
            }
          },
        }
    });

    $('#addRequirementsRowForm').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
          valid: 'glyphicon glyphicon-ok',
          invalid: 'glyphicon glyphicon-remove',
          validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
          require_row_name: {
            validators: {
                notEmpty: {
                    message: '不能为空'
                }
            }
          },
          require_row_name:{
            validators:{
              notEmpty:{
                message:'不能为空'
              },
            }
          },
          require_row_valueunit:{
            validators:{
              notEmpty:{
                message:'不能为空'
              },
            }
          },
          require_row_costunit:{
            validators:{
              notEmpty:{
                message:'不能为空'
              },
            }
          }
        }
    });
    $('#addRequirementsForm').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
          valid: 'glyphicon glyphicon-ok',
          invalid: 'glyphicon glyphicon-remove',
          validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
          requirement_name: {
            validators: {
                notEmpty: {
                    message: '名称不能为空'
                }
            }
          },
          requirement_desc:{
            validators:{
              notEmpty:{
                message:'描述不能为空'
              },
            }
          }
        }
    });
  }
}

var _app = new Vue({
  delimiters:['[[',']]'],
  el:"#app",
  data:{},
  mounted:function(){
    console.log(33444);
    businessManager.init();
    document.onmousedown=function(e){
        e = e || window.event;
        var btn = e.button + 1 || e.which;
        if(btn == 1){
            // console.log("左键");
            common_data.menubox_key = 1;
        }else if(btn==2){
            // console.log("中键");
            common_data.menubox_key = 1;
        }else if(btn==3){
            // console.log("右键");
            common_data.menubox_key = 2;
        }
    }
    if(common_data.showstatus!=1&&common_data.showstatus!=2){
      budgettable = $("#budgettbs").DataTable(datatable_options);
      $(".budgetxuqiu").addClass("table-unactive").removeClass("table-active");
      $(".budgethuizong").addClass("table-unactive").removeClass("table-active");
      $(".budgettbs").addClass("table-active").removeClass("table-unactive");
    }
  },
  methods:{}
});
