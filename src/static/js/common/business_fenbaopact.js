var storage = null;
var uploadfile_qingdanStr = '';//合同清单id字符串
var uploadfile_fujianStr = '';//合同附件id字符串
var mouse_key = 0;//鼠标点击，1：左键，2：右键
var fenbaotable;
var laowutable;
var keeplist = new Object();
var tbpact_id,jstree_demo;
var datatable_options = {
   "dom": 'tip',
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
      "url":'/../../business/getpactqingdanlist/',
      "type":'POST',
    },

    "columns": [{
      "data": "code"
    }, {
      "data": "name"
    }, {
      "data": "unit"
    },
    {
      "data": null
    }, {
      "data": null
    }, ],
    columnDefs:[//添加自定义按钮
    {
        targets: 3,
        render: function (a, b, c, d) {
          if(a.designBqs==''||a.designBqs=="0"||a.designBqs=='null'){
            return '';
          }else{
            return a.designBqs;
          }
        }
    },
    {
        targets: 4,
        render: function (a, b, c, d) {
          if(a.price==''||a.price=="0"||a.price=='null'){
            return '';
          }else{
            return a.price;
          }
        }
    },
    ],
    //向服务器传额外的参数
    "fnServerParams": function(aoData) {
      aoData.param = keeplist;
    },
};
var datatable_labour_options = {
   "dom": 'tip',
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
      "url":'/../../business/getpactqingdanlist/',
      "type":'POST',
    },

    "columns": [{
      "data": "name"
    }, {
      "data": "unit"
    },{
      "data": "taxprice"
    } ],
    //向服务器传额外的参数
    "fnServerParams": function(aoData) {
      aoData.param = keeplist;
    },
};
$(function(){
  businessManager.init();
  document.onmousedown=function(e){
      e = e || window.event;
      var btn = e.button + 1 || e.which;
      if(btn == 1){
          mouse_key = 1;
      }else if(btn==2){
          mouse_key = 1;
      }else if(btn==3){
          mouse_key = 2;
      }
  }
  fenbaotable = $("#fenbaopact").DataTable(datatable_options);
  $('#zbao_yusuan').multiselect({
        nonSelectedText: "请选择",
        allSelectedText:'已全选'
    });
  // laowutable = $("#laowupact").DataTable(datatable_labour_options);
});

var businessManager = {
  init : function(){
    var that = this;
    that.bindListener();
    jstree_demo = that.jstreeInit();
    that.filterInit();
    that.formValidator();
  },

  bindListener:function(){
    var that = this;

    $("#clearstorage").bind("click",function(){
      that.removeLocalstorage();
    });
    $("#hysrq").bind("click",function(){
      $('#hysrq').datetimepicker({
        language: 'zh-CN',//显示中文
        autoclose: true,//选中自动关闭
      }).on('hide',function(e) {});
    });
    $("#hysrq").click();

    $("#zbao_pacttime").bind("click",function(){
      $('#zbao_pacttime').datetimepicker({
        language: 'zh-CN',//显示中文
        autoclose: true,//选中自动关闭
      }).on('hide',function(e) {});
    });
    $("#zbao_pacttime").click();

    $("#jstree_demo_div").bind("activate_node.jstree", function(obj, e){
      var selectedid = e.node.id;
      if(mouse_key!=1)
        return ;
      if(selectedid.indexOf("@@")>=0){
        var idarr = selectedid.split("@@");
        var currtype = parseInt(idarr[0]);
        var currselectedid= idarr[1];
        keeplist.pact_id = currselectedid;
        keeplist.pact_type = currtype;
        tbpact_id = currselectedid;
        if(currtype==5){
          fenbaotable.draw();
          $(".laowupact").addClass("table-unactive").removeClass("table-active");
          $(".fenbaopact").addClass("table-active").removeClass("table-unactive");
        }else if(currtype==2){
          if(laowutable==null){
            laowutable = $("#laowupact").DataTable(datatable_labour_options);
          }else{
            laowutable.draw();
          }

          $(".fenbaopact").addClass("table-unactive").removeClass("table-active");
          $(".laowupact").addClass("table-active").removeClass("table-unactive");
        }

      }else{
        console.log("父类节点");
      }
    });

    $("#btnAddZbaopact").bind("click",function(){
      $('#addpactForm').bootstrapValidator('validate');
      if(!($('#addpactForm').data('bootstrapValidator').isValid())){
        return ;
      }
      that.addZbaopact();
    });

    $("#addZbaoDialog").on("hidden.bs.modal",function(){
      $("#addpactForm").data('bootstrapValidator').destroy();
      $('#addpactForm').data('bootstrapValidator', null);
      document.getElementById("addpactForm").reset();//清空表单
      // $(".jFiler-items").remove();
      // $(".jFiler-input-caption span").html('');
      that.formValidator();
    });


  },

  addZbaopact:function(){
      var zbao_pactname = $("#zbao_pactname").val();
      var zbao_pactcode = $("#zbao_pactcode").val();
      var zbao_pacttype = $("#zbao_pacttype option:selected").val();
      var zbao_professional = $("#zbao_professional option:selected").val();
      var zbao_company = $("#zbao_company option:selected").val();
      var zbao_pacttax = $("#zbao_pacttax").val();
      var zbao_pactdesc = $("#zbao_pactdesc").val();
      // console.log(zbao_pacttype);
      if(uploadfile_qingdanStr==''){
        alert("请上传清单");
        return ;
      }
      var selected = [];
      $("#zbao_yusuan option:selected").each(function () {
        selected.push($(this).val());
      });

      $(".pro-loading").fadeIn();
      $.ajax({
        type: "get",
        url: "/business/addfenpact/",
        dataType: "json",
        data: {
          "zbao_pactname": zbao_pactname,
          "zbao_pactcode": zbao_pactcode,
          "zbao_pacttype": zbao_pacttype,
          "zbao_professional": zbao_professional,
          "zbao_company": zbao_company,
          "zbao_yusuan": selected.join(','),
          "zbao_pacttax": zbao_pacttax,
          "zbao_pactdesc": zbao_pactdesc,
          "uploadfile_qingdanStr": uploadfile_qingdanStr,
          "uploadfile_fujianStr": uploadfile_fujianStr,
        },
        success: function(data) {
          $(".pro-loading").fadeOut();
          if (data.issuc) {
            alert("添加分包成功",null,function(){
              $("#addZbaoDialog").modal("hide");
              window.location.reload();
            });
          } else {
            alert("添加分包异常",null,function(){$("#addZbaoDialog").modal("hide");});
          }
        },
        error: function(data) {
          $(".pro-loading").fadeOut();
        }
      });
  },

  uploadQingdan:function(){
    var pid = $("#currpactid").val();
    var typeid = $("#currtype_id").val();
    if(uploadfile_qingdanStr==''){
      alert("请上传清单");
      return ;
    }
    $(".pro-loading").fadeIn();
    $.ajax({
        type: "get",
        url: "/business/uploadQingdan/",
        dataType: "json",
        data: {
          "pact_id": pid,
          "type_id": typeid,
          "docid": uploadfile_qingdanStr,
        },
        success: function(data) {
          $(".pro-loading").fadeOut();
          if (data.issuc = "true") {
            $("#uploadQingdanDialog").modal("hide");
            uploadfile_qingdanStr = '';
            window.location.reload();
          } else {
            alert("添加失败");
          }
        },
        error: function(data) {
          $(".pro-loading").fadeOut();
        }
      });
  },
  jstreeInit : function(){
    return $('#jstree_demo_div').jstree({
      'core': {
          'data':{
            'url' : '/business/get_fenbaopact_tree/',
            'data' : function (node) {
                  return { 'id' : node.id };
              }
            }
      },

      "plugins": [
          "wholerow","themes", "json_data","contextmenu"
      ],
      "contextmenu":{
        "items": function (node) {
              var nodeidstr = node.id;
              var pactmenu = {}
              pactmenu = {
                "pact_del": {
                      "label": "删除",
                      "icon":"fa fa-file",
                      "separator_after": true,
                      "action": function (data) {
                          var inst = jQuery.jstree.reference(data.reference),
                          obj = inst.get_node(data.reference);
                          var selectedid = obj.id;
                          if(selectedid.indexOf("@@")<0){
                            return ;
                          }
                          var idarr = selectedid.split("@@");
                          var currtype = parseInt(idarr[0]);
                          var currselectedid= idarr[1];
                          alertConfirm("确定删除该分包吗？",null,function(){
                            $.ajax({
                              type:'get',
                              dataType:'json',
                              data:{pactid:currselectedid},
                              url:'/business/delFenbaoitem/',
                              success:function(data){
                                alert('删除成功',null,function(){window.location.reload();});
                              },
                              error:function(data){
                                alert('删除失败');
                              }
                            });
                          });
                      }
                  },
              }

              /**
               * 如果选择不是所想节点，则不出右键菜单项
               */
              console.log(node);
              if(node.parent!="#"){
                return pactmenu;
              }
          },
        // "items":{
        //     "删除清单":{
        //         "label":"删除",
        //         "action":function(data){
        //             var inst = jQuery.jstree.reference(data.reference),
        //             obj = inst.get_node(data.reference);
        //             var selectedid = obj.id;
        //             if(selectedid.indexOf("@@")<0){
        //               return ;
        //             }
        //             var idarr = selectedid.split("@@");
        //             var currtype = parseInt(idarr[0]);
        //             var currselectedid= idarr[1];
        //             alertConfirm("确定删除该分包吗？",null,function(){
        //               $.ajax({
        //                 type:'get',
        //                 dataType:'json',
        //                 data:{pactid:currselectedid},
        //                 url:'/business/delFenbaoitem/',
        //                 success:function(data){
        //                   alert('删除成功',null,function(){window.location.reload();});
        //                 },
        //                 error:function(data){
        //                   alert('删除失败');
        //                 }
        //               });
        //             });
        //         }
        //     },
        //   }
        },
    });
  },
  filterInit : function(){
    var that = this;
    $('#uploadfile_fujian').filer({
        showThumbs: true,
        addMore: true,
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
            url: "/uploadfile_conc2/",
            data: null,
            type: 'POST',
            enctype: 'multipart/form-data',
            beforeSend: function(){},
            success: function(data, el){
                if (data.issuc=="true"){
                    el.attr("value",data.docId);
                    // console.log(data.docId);
                    if(uploadfile_fujianStr==""){
                        uploadfile_fujianStr+=data.docId;
                    }else{
                        uploadfile_fujianStr+='#'+data.docId;
                    }
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
            uploadfile_fujianStr = "";//清空清单附件
        }
    });

    $('#uploadfile_qingdan').filer({
        showThumbs: true,
        addMore: true,
        limit :1,
        allowDuplicates: false,
        captions:{
            button: "添加文件",
            feedback: "",
            feedback2: "个文件已选择",
            drop: "拖到文件到这里",
            removeConfirmation: "确定删除该文件吗？",
            errors: {
                filesLimit: "只能上传一份清单",
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
                    if(uploadfile_qingdanStr==""){
                        uploadfile_qingdanStr+=data.docId;
                    }else{
                        uploadfile_qingdanStr+='#'+data.docId;
                    }
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
    $('#addpactForm').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
          valid: 'glyphicon glyphicon-ok',
          invalid: 'glyphicon glyphicon-remove',
          validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
          zbao_pactname: {
            validators: {
                notEmpty: {
                    message: '合同名称不能为空'
                },
                stringLength: {
                    min: 5,
                    max: 20,
                    message: '合同名称5-20个字'
                }
            }
          },
          zbao_pactcode:{
            validators:{
              notEmpty:{
                message:'合同编号不能为空'
              },
            }
          },
          zbao_pacttax: {
            validators: {
                notEmpty: {
                    message: '合同税率不能为空'
                },
                regexp:{
                  message:'格式不对，请输入合同税率',//
                  regexp:/^[0-9]+([.]{1}[0-9]+){0,1}$/
                }
            }
          },
          zbao_yusuan: {
            validators: {
                notEmpty: {
                    message: '关联预算不能为空'
                }
            }
          },
          zbao_pacttype: {
            validators: {
                notEmpty: {
                    message: '合同类型不能为空'
                }
            }
          },
          zbao_company: {
            validators: {
                notEmpty: {
                    message: '合作单位不能为空'
                }
            }
          },
          zbao_professional: {
            validators: {
                notEmpty: {
                    message: '所属专业不能为空'
                }
            }
          },
          zbao_pactdesc: {
            validators: {
                notEmpty: {
                    message: '描述不能为空'
                },
                stringLength: {
                    min: 5,
                    max: 120,
                    message: '描述在5-120个字'
                }
            }
          },
        }
    });
  }
}
