var businessManager,jstreeitem;

var mouse_key = 0;

businessManager = {
  init : function(){
    var that = this;
    that.bindListener();
    that.jstreeInit();
    that.filterInit();
    that.formValidator();
  },

  bindListener:function(){
    var that = this;
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
  },

  jstreeInit : function(){
    jstreeitem = $('#jstree_demo_div').jstree({
      'core': {
          'data':{
            'url' : '/business/get_business_otheritem_tree/',
            'data' : function (node) {
                  return { 'id' : node.id };
                }
              }
      },
      'multiple': false,
      "plugins": [
          "wholerow","themes", "json_data","contextmenu"
      ],
      "contextmenu": {
          "items": function (node) {
            var nodeidstr = node.id;
              var temp = {
                  "lookbq": {
                      "label": "查看",
                      "icon":"fa fa-file",
                      "separator_after": true,
                      "action": function (data) {
                        $.ajax({
                          type:'get',
                          dataType:'json',
                          url:'/business/getBqitemBycode/',
                          data:{bqcode:node.id},
                          success:function(data){
                            if(data.issuc){
                              $("#bqitem_xuhao").val(data.bqitem.no);
                              $("#bqitem_code").val(data.bqitem.BQItem_Code);
                              $("#bqitem_name").val((data.bqitem.BQItemName).trim());
                              $("#bqitem_unit").val(data.bqitem.BQItemUnit);
                              $("#bqitem_designs").val(data.bqitem.designBqs);
                              $("#bqitem_builds").val(data.bqitem.buildBqs);
                              $("#bqitem_unitprice").val(data.bqitem.allunitrate);
                              $("#bqitem_money").val(data.bqitem.allrate);

                              $("#showBqitemDialog").modal("show");
                            }else{
                              alert(data.msg);
                            }
                          },
                          error:function(data){
                            alert("系统异常");
                          }
                        });
                      }
                  },
                  "lockbq": {
                      "label": "锁定",
                      "icon":"fa fa-file",
                      "separator_after": true,
                      "action": function (data) {
                          alert("锁定清单");
                      }
                  }
              };
              var pactmenu = {
                "pact_detail": {
                    "label": "详情",
                    "icon":"fa fa-file",
                    "separator_after": true,
                    "action": function (data) {
                        _app.detailbpact(nodeidstr.split("-")[2]);
                    }
                },
                "pact_edit": {
                    "label": "修改",
                    "icon":"fa fa-file",
                    "separator_after": true,
                    "action": function (data) {
                        _app.editZbaoFormData.pact_id = nodeidstr.split("-")[2];
                        _app.editZbaoFormData.zbao_pactname = node.text;
                        $("#updateZbaoDialog").modal('show');
                    }
                },
                "pact_del": {
                      "label": "删除",
                      "icon":"fa fa-file",
                      "separator_after": true,
                      "action": function (data) {
                           alertConfirm("是否删除","",function(){
                              _app.delzbpact(nodeidstr.split("-")[2]);
                           });
                      }
                  },
              };
              var spacemenu = {
                "upspace": {
                    "label": "上移",
                    "icon":"fa fa-file",
                    "separator_after": true,
                    "action": function (data) {
                        _app.movespace(node.id,1);
                    }
                },
                "downspace": {
                    "label": "下移",
                    "icon":"fa fa-file",
                    "separator_after": true,
                    "action": function (data) {
                        _app.movespace(node.id,-1);
                    }
                },
                "addpact": {
                      "label": "添加",
                      "icon":"fa fa-file",
                      "separator_after": true,
                      "action": function (data) {
                            _app.addzbpactDate.space_id = node.id;
                           $("#addZbaoDialog").modal('show');
                      }
                  },
                "updatespace": {
                    "label": "修改",
                    "icon":"fa fa-file",
                    "separator_after": true,
                    "action": function (data) {
                        $("#updatespaceDialog").modal('show');
                        _app.editspaceFormData.spacename = node.text;
                        _app.editspaceFormData.id = node.id;
                    }
                },
                "delspace": {
                    "label": "删除",
                    "icon":"fa fa-file",
                    "separator_after": true,
                    "action": function (data) {
                        _app.delspacebyid(node.id);
                    }
                },
              };
              /**
               * 如果选择不是所想节点，则不出右键菜单项
               */
               console.log(node);
              var menu = {};

              if(node.parent=="#"){
                return spacemenu;
              }else if(nodeidstr.indexOf("zixingyg")>=0||nodeidstr.indexOf("fenbaoyg")>=0){
                return pactmenu;
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
        }
    });

    $('#uploadfile_qingdan').filer({
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
    $('#addspaceForm').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            spacename: {
                validators: {
                    notEmpty: {
                        message: '空间名称不能为空'
                    }
                }
            },
        }
    });
    $('#addFeilvForm').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            feilvname: {
                validators: {
                    notEmpty: {
                        message: '费率名称不能为空'
                    }
                }
            },
        }
    });

    $('#updatespaceForm').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            editspacename: {
                validators: {
                    notEmpty: {
                        message: '空间名称不能为空'
                    }
                }
            },
        }
    });

    $('#addpactForm').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
          valid: 'glyphicon glyphicon-ok',
          invalid: 'glyphicon glyphicon-remove',
          validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
          zbao_isself: {
            validators: {
                notEmpty: {
                    message: '类型不能为空'
                }
            }
          },
          zbao_contenttype: {
            validators: {
                notEmpty: {
                    message: '内容不能为空'
                }
            }
          },
          zbao_pactname: {
            validators: {
                notEmpty: {
                    message: '名称不能为空'
                },
                stringLength: {
                    min: 5,
                    max: 20,
                    message: '名称5-20个字'
                }
            }
          },
          zbao_pactcode:{
            validators:{
              notEmpty:{
                message:'预算编号不能为空'
              },
            }
          },
          zbao_company: {
            validators: {
                notEmpty: {
                    message: '预算单位不能为空'
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

// console.log(Editable);
var _app = new Vue({
  delimiters:['[[',']]'],
  el:"#app",
  data:{
    can_export:0,
    show_type:0,//0：展示清单表格，1：展示费率表，2：展示工料机表；3：展示2000定额工料机表
    indexData:{
      rqitemlist:[],
      rtlist:[],
      bqitemlist:[],
      dingarr:[],
      rtitem:{},
    },
    addFeilvFormData:{
      feilvname:'',
      id:0,
      pact_id:0
    },
    pactspace_rateData:{
      list:[]
    },
    pactspace_resourceData:{
      list:[],

    },
    pactspace_thoundResData:{
      list:[]
    },
    addDingeData:{
      dinge_show:0,
      RTItemID:0,
      RTContentAmount:'',
      dinge_rencaji:1,
    },
    editZbaoFormData:{
      zbao_pactname:'',
      pact_id:0,
    },
    detailzbpactDate:{
      addbutton_disabled:false,
      zbao_pactname: '',
      zbao_pactcode: '',
      zbao_pacttype: 1,
      zbao_professional: 1,
      zbao_company: 1,
      // zbao_pacttax: '',
      zbao_pactdesc: '',
      zbao_isself:1,
      zbao_contenttype:1,
      space_id:0,
    },
    addzbpactDate:{
      addbutton_disabled:false,
      zbao_pactname: '',
      zbao_pactcode: '',
      zbao_pacttype: 1,
      zbao_professional: 1,
      zbao_company: 1,
      // zbao_pacttax: '',
      zbao_pactdesc: '',
      zbao_isself:1,
      zbao_contenttype:1,
      space_id:0,
      uploadfile_qingdanStr: uploadfile_qingdanStr,
      uploadfile_fujianStr: uploadfile_fujianStr,
    },
    space_dialog_show:1,
    addspaceFormData:{
      spacename:'',
    },
    editspaceFormData:{
      spacename:'',
      id:0
    },
  },
  mounted:function(){
    var that = this;
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
    that.initData(0,0,0,'notrclick');
    $("#addZbaoDialog").on("hidden.bs.modal",function(){
      $("#addpactForm").data('bootstrapValidator').destroy();
      $('#addpactForm').data('bootstrapValidator', null);
      document.getElementById("addpactForm").reset();//清空表单
      businessManager.formValidator();
    });
    $("#addFeilvDialog").on("hidden.bs.modal",function(){
      $("#addFeilvForm").data('bootstrapValidator').destroy();
      $('#addFeilvForm').data('bootstrapValidator', null);
      document.getElementById("addFeilvForm").reset();//清空表单
      businessManager.formValidator();
    });
    $("#addspaceDialog").on("hidden.bs.modal",function(){
      $("#addspaceForm").data('bootstrapValidator').destroy();
      $('#addspaceForm').data('bootstrapValidator', null);
      document.getElementById("addspaceForm").reset();//清空表单
      businessManager.formValidator();
      jstreeitem.jstree().refresh();
    });
    $("#updatespaceDialog").on("hidden.bs.modal",function(){
      $("#updatespaceForm").data('bootstrapValidator').destroy();
      $('#updatespaceForm').data('bootstrapValidator', null);
      document.getElementById("updatespaceForm").reset();//清空表单
      businessManager.formValidator();
      jstreeitem.jstree().refresh();
    });

    $("#jstree_demo_div").bind("activate_node.jstree", function(obj, e){
      var selectedid = e.node.id;
      that.can_export = 0;
      if(selectedid.indexOf('fenbaoyg')>=0||selectedid.indexOf('zixingyg')>=0||selectedid.indexOf('fenbaobqitem')>=0||selectedid.indexOf('zixingbqitem')>=0){
        that.show_type = 0;
        that.initData(selectedid.split('-')[2],0,0,'notrclick');
      }else if(selectedid.indexOf('fenbaopact')>=0||selectedid.indexOf('zixingpact')>=0){
        that.show_type = 0;
        that.initData(selectedid.split('-')[2],selectedid.split('-')[3],0,'notrclick');
      }else if(selectedid.indexOf('feilv')>=0){
        that.show_type = 1;
        console.log("获取"+selectedid.split('-')[2]+'的费率');
        that.addFeilvFormData.pact_id = parseInt(selectedid.split('-')[2])
        that.getpsrate_or_resource(selectedid.split('-')[2],1);
      }else if(selectedid.indexOf('copy')>=0){
        console.log("获取"+selectedid.split('-')[2]+'的工料机');
        that.show_type = 3;
        that.getpsrate_or_resource(selectedid.split('-')[2],3);
      }else if(selectedid.indexOf('resource')>=0){
        console.log("获取"+selectedid.split('-')[2]+'的工料机');
        that.show_type = 2;
        that.getpsrate_or_resource(selectedid.split('-')[2],2);
        that.can_export = 1;
        export_tableid = 'right-main-div';
        export_name = '工料机表';
      }
    });
  },
  methods:{
    datatoFixed:function(data,num){
      var patrn = /^(-)?\d+(\.\d+)?$/;
      if (patrn.exec(data) == null || data == "") {
          data = 0;
      }

      return parseFloat(data).toFixed(num);
    },
    getpsrate_or_resource:function(id,type){
      var that = this;
      console.log(id,type);
      $.ajax({
          type: "get",
          url: "/business/getpsrate_or_resource/",
          dataType: "json",
          data: {pact_id:id,operate:type},
          success: function(data) {
            $(".edit-table-rate").editable("destroy");
            if(type==1){
              that.pactspace_rateData.list = [];
              that.$nextTick(function(){
                that.pactspace_rateData.list = data.ratelist
                that.$nextTick(function(){
                  that.editableinit();
                });
              });
            }else if(type==2){
              that.pactspace_resourceData.list = [];
              that.$nextTick(function(){
                that.pactspace_resourceData.list = data.resourcelist
                that.$nextTick(function(){
                  if(that.show_type!=3){
                    that.editableinit();
                  }
                });
              });
            }else{

              that.pactspace_thoundResData.list = [];
              that.pactspace_thoundResData.list = data.resourcelist

            }
          },
          error: function() {}
        });
    },
    editableinit:function(){
      console.log("重新初始化");
      var that = this;
      $(".edit-table").editable({
        title:"含量",
        url :function(params) {
          console.log(params);
          $.ajax({
            type: "post",
            url: "/business/updateDinge/",
            dataType: "json",
            data: {pk:params.name,name:4,value:params.value},
            success: function(data) {
              // console.log($(".for-color-"+data.id).html()+'--------'+data.comparison);
              if($(".for-color-"+data.id).html()==data.comparison){
                $(".for-color-"+data.id).attr("style","color:black;");
              }else{
                $(".for-color-"+data.id).attr("style","color:red;");
              }
              console.log(that.indexData.dingarr);
              for (var i = that.indexData.dingarr.length-1; i>=0; i--)
                if (that.indexData.dingarr[i].id==params.name)
                    that.indexData.dingarr[i].RTActualAmount = params.value;
            },
            error: function(data) {}
          });
        },
        success:function(a){
        },
        validate: function (value) { //字段验证
            if (!$.trim(value)) {
                return '不能为空';
            }else{}
        },
      });

      $(".edit-table-buildnums").editable({
        validate: function (value) { //字段验证
            if (!$.trim(value)) {
                return '不能为空';
            }else{}
        },
        success: function(a,b,c){
          console.log(a);
          if(a.issucc=='true'){
            alert("修改成功",null,function(){
              window.location.reload();
            });
          }else{
            alert("修改错误");
          }
        }
      });
      $(".edit-table-rate").editable({
        validate: function (value,params) { //字段验证
            if (!$.trim(value)) {
                return '不能为空';
            }
        },
        url :function(params) {
          console.log(params);
          if((params.name).indexOf('feilv-')>=0){
            params.name = 2;
          }else{
            params.name = 1;
          }
          $.ajax({
            type: "post",
            url: "/business/updateSpaceRate/",
            dataType: "json",
            data: {pk:params.pk,name:params.name,value:params.value},
            success: function(data) {
              if(data.issuc){
                for (var i = that.pactspace_rateData.list.length-1; i>=0; i--){
                  if (that.pactspace_rateData.list[i].id==data.id){
                    if(data.type==1){
                      that.pactspace_rateData.list[i].name = data.value;
                    }else if(data.type==2){
                      that.pactspace_rateData.list[i].rate = parseFloat(data.value);
                      that.getpsrate_or_resource(data.pact_id,1);
                    }else{
                      that.pactspace_rateData.list[i].money = parseFloat(data.value).toFixed(2);
                    }
                  }
                }
              }else{
                alert("修改异常，请检测是否输入正确费率");
              }
            },
            error: function(data) {
              alert("修改异常，请检测是否输入正确费率");
            }
          });
        },
        success: function(a,b){

        }
      });
    },
    /**
    * 获取清单、定额、关联人材机列表
    * pact_id:分包ID
    * bqid:清单ID,
    * deid:定额ID
    * istr:类型（根据字符串区分）
    **/
    initData:function(pact_id,bqid,deid,istr){
      var that = this;
      // console.log("销毁edittable");
      $(".edit-table").editable("destroy");
      $(".edit-table-buildnums").editable("destroy");
      if(istr=='rtitemtrclick'){
        $(".rtitem-click").removeClass("rtitem-click");
        event.currentTarget.parentElement.classList.add('rtitem-click')
      }else if(istr=='bqitemtrclick'){
        $(".bqitem-click").removeClass("bqitem-click");
        $(".rtitem-click").removeClass("rtitem-click");
        event.currentTarget.parentElement.classList.add('bqitem-click')
      }else{
        $(".bqitem-click").removeClass("bqitem-click");
        $(".rtitem-click").removeClass("rtitem-click");
      }
      $.ajax({
          type: "get",
          url: "/business/initmanagerData/",
          dataType: "json",
          data: {pact_id:pact_id,bqid:bqid,deid:deid},
          success: function(data) {
            if((bqid==0&&deid==0)||(bqid!=0&&pact_id!=0)){
              that.indexData.bqitemlist = data.bqitemlist;
            }
            if(deid==0){
              that.indexData.rtlist = data.rtlist;
            }
            that.indexData.dingarr = data.dingarr;
            that.indexData.rtitem = data.rtitem;
            that.$nextTick(function(){
              console.log(1111);
              that.editableinit();

            });
          },
          error: function(data) {}
        });
    },
    delSpaceRate:function(id){
      var that = this;
      alertConfirm('确定删除吗',null,function(){
        $.ajax({
          type:'get',
          dateType:'json',
          url:'/business/delSpaceRate/',
          data:{feilvid:id},
          success:function(data){
            alert("删除成功",null,function(){
              that.getpsrate_or_resource(data.pact_id,1);
            });
          },
          error:function(data){}
        });
      });
    },
    delSpaceResource:function(id){
      var that = this;
      alertConfirm('确定删除吗',null,function(){
        $.ajax({
          type:'get',
          dateType:'json',
          url:'/business/rencaijirelatedel/',
          data:{id:id},
          success:function(data){
            alert("删除成功",null,function(){
              var arrt;
              for (var i = that.pactspace_resourceData.list.length-1; i>=0; i--){
                console.log(that.pactspace_resourceData.list[i].id);
                if (that.pactspace_resourceData.list[i].id==id){
                    that.pactspace_resourceData.list.splice(i,1);
                    arrt = that.pactspace_resourceData.list;
                }
              }

              that.pactspace_resourceData.list = [];
              that.$nextTick(function(){
                that.pactspace_resourceData.list = arrt;
                that.$nextTick(function(){
                  that.editableinit();
                });
              });
            });
          },
          error:function(data){}
        });
      });
    },
    formatnumdata:function(data,num){
      return parseFloat(data).toFixed(num);
    },


    detailbpact:function(pactid){
      var that = this;
      $.ajax({
          type: "get",
          url: "/business/getpactbyid/",
          dataType: "json",
          data: {pact_id:pactid},
          success: function(data) {
            that.detailzbpactDate.zbao_pactname = data.pactitem.name;
            that.detailzbpactDate.zbao_pactcode = data.pactitem.pactcode;
            that.detailzbpactDate.zbao_pacttype = data.pactitem.type;
            that.detailzbpactDate.zbao_professional = data.pactitem.major_id;
            that.detailzbpactDate.zbao_company = data.pactitem.cooperation_id;
            // that.detailzbpactDate.zbao_pacttax = data.pactitem.cess;
            that.detailzbpactDate.zbao_pactdesc = data.pactitem.description;
            that.detailzbpactDate.zbao_isself = data.pactitem.is_self;
            that.detailzbpactDate.zbao_contenttype = data.pactitem.budgetcont_type;
            $("#editZbaoDialog").modal('show');
          },
          error: function(data) {}
        });
    },
    updateZbaoform:function(){
      var that = this;
      $.ajax({
          type: "get",
          url: "/business/updatepact/",
          dataType: "json",
          data: {pact_id:that.editZbaoFormData.pact_id,pact_name:that.editZbaoFormData.zbao_pactname},
          success: function(data) {
            jstreeitem.jstree().refresh();
            $("#updateZbaoDialog").modal("hide");
          },
          error: function(data) {}
        });
    },
    delzbpact:function(pactid){
      $(".pro-loading").fadeIn();
      $.ajax({
          type: "get",
          url: "/business/delpact/",
          dataType: "json",
          data: {pact_id:pactid},
          success: function(data) {
            $(".pro-loading").fadeOut();
            if(data.issuc){
              alert("删除成功",null,function(){
                window.location.reload();
              });
            }else{
              alert(data.msg);
            }
          },
          error: function(data) {}
        });
    },
    addZbaoPact:function(){
      var that = this;
      $('#addpactForm').bootstrapValidator('validate');
      if(!($('#addpactForm').data('bootstrapValidator').isValid())){
        return ;
      }
      if(uploadfile_qingdanStr==''){
        alert("请上传清单");
        return ;
      }
      $(".pro-loading").fadeIn();
      document.getElementById("btnAddZbaopact").disabled = true;
      $.ajax({
        type: "get",
        url: "/business/addpact/",
        dataType: "json",
        data: {
          "space_id":that.addzbpactDate.space_id,
          "zbao_isself":that.addzbpactDate.zbao_isself,
          "zbao_contenttype":that.addzbpactDate.zbao_contenttype,
          "zbao_pactname": that.addzbpactDate.zbao_pactname,
          "zbao_pactcode": that.addzbpactDate.zbao_pactcode,
          "zbao_pacttype": that.addzbpactDate.zbao_pacttype,
          "zbao_professional": that.addzbpactDate.zbao_professional,
          "zbao_company": that.addzbpactDate.zbao_company,
          // "zbao_pacttax": that.addzbpactDate.zbao_pacttax,
          "zbao_pactdesc": that.addzbpactDate.zbao_pactdesc,
          "uploadfile_qingdanStr": uploadfile_qingdanStr,
          "uploadfile_fujianStr": uploadfile_fujianStr,
        },
        success: function(data) {
          $(".pro-loading").fadeOut();
          if (data.issuc = "true") {
            alert("添加预算成功",null,function(){
              $("#addZbaoDialog").modal("hide");
              window.location.reload();
            });

          } else {
            alert("添加失败");
          }
        },
        error: function(data) {
          $(".pro-loading").fadeOut();
        }
      });
    },

    addspace:function(){
      var that = this;
      $("#addspaceDialog").modal("show");
    },
    addfeilv:function(id){
      var that = this;
      that.addFeilvFormData.id = id;
      $("#addFeilvDialog").modal("show");
    },
    movespace:function(pid,dir){
      $.ajax({
        type:'get',
        dateType:'json',
        url:'/business/movespace/',
        data:{
          id:pid,
          dir:dir,
        },
        success:function(data){
          jstreeitem.jstree().refresh();
        },
        error:function(e){
          alert("删除失败");
        }
      });
    },
    delspacebyid:function(pid){
      alertConfirm("确定删除空间吗","",function(){
          $.ajax({
          type:'get',
          dateType:'json',
          url:'/business/delspace/',
          data:{
            id:pid
          },
          success:function(data){
            if(data.issuc){
              alert("删除成功","",function(){
                // jstreeitem.jstree().refresh();
                window.location.reload();
              });
            }else{
              alert("删除失败");
            }
          },
          error:function(e){
            alert("删除失败");
          }
        });
      });
    },
    updatespaceform:function(){
      var that = this;
      // console.log(that.editspaceFormData.spacename);
      $('#updatespaceForm').bootstrapValidator('validate');
      if(!($('#updatespaceForm').data('bootstrapValidator').isValid())){
        return ;
      }
      $.ajax({
        type:'get',
        dateType:'json',
        url:'/business/updatespace/',
        data:{
          id:that.editspaceFormData.id,
          spacename:that.editspaceFormData.spacename,
        },
        success:function(data){
          if(data.issuc){
            alert("修改成功",'',function(){
              $("#updatespaceDialog").modal("hide");
            });
          }else{
            alert("修改失败",'',function(){
              $("#updatespaceDialog").modal("hide");
            });
          }
        },
        error:function(e){
          alert("修改失败",'',function(){
              $("#updatespaceDialog").modal("hide");
            });
        }
      });
    },
    addfeilvform:function(){
      var that = this;
      $('#addFeilvForm').bootstrapValidator('validate');
      if(!($('#addFeilvForm').data('bootstrapValidator').isValid())){
        return ;
      }
      $.ajax({
        type:'get',
        dateType:'json',
        url:'/business/addpactspacefeilv/',
        data:{
          name : that.addFeilvFormData.feilvname,
          pact_id:that.addFeilvFormData.pact_id,
          parent_id:that.addFeilvFormData.id,
        },
        success:function(data){
          if(data.issuc){
            alert("添加成功",'',function(){
              $("#addFeilvDialog").modal("hide");
              that.getpsrate_or_resource(that.addFeilvFormData.pact_id,1);
            });
          }else{
            alert("添加失败",'',function(){
              $("#addFeilvDialog").modal("hide");
            });
          }
        },
        error:function(e){
          alert("添加失败",'',function(){
              $("#addFeilvDialog").modal("hide");
            });
        }
      });
    },
    addspaceform:function(){
      var that = this;
      $('#addspaceForm').bootstrapValidator('validate');
      if(!($('#addspaceForm').data('bootstrapValidator').isValid())){
        return ;
      }
      console.log(that.addspaceFormData.spacename);
      $.ajax({
        type:'get',
        dateType:'json',
        url:'/business/addpactspace/',
        data:{
          spacename : that.addspaceFormData.spacename
        },
        success:function(data){
          if(data.issuc){
            alert("添加成功",'',function(){
              $("#addspaceDialog").modal("hide");
            });
          }else{
            alert("添加失败",'',function(){
              $("#addspaceDialog").modal("hide");
            });
          }
        },
        error:function(e){
          alert("添加失败",'',function(){
              $("#addspaceDialog").modal("hide");
            });
        }
      });
    }
  }
});
