var businessManager,jstreeitem;
// console.log(Editable);
var _app = new Vue({
  delimiters:['[[',']]'],
  el:"#app",
  data:{
    can_export:0,
    show_type:0,//0：展示清单表格，1：展示费率表，2：展示工料机表；3：展示2000定额工料机表
    indexData:{
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

    other_projectData:[], //其他项目合计数据

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
  filters: {
    percent:function(value){
      return value*100+'%';
    }
  },
  mounted:function(){
    var that = this;

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

    $("#btnAddDinge").bind("click",function(){
      $('#addDingeForm').bootstrapValidator('validate');
      if(!($('#addDingeForm').data('bootstrapValidator').isValid())){
        return ;
      }
      $.ajax({
        type:'get',
        dateType:'json',
        url:'/business/rencaijiadd/',
        data:{
          RTItemID:that.addDingeData.RTItemID,
          RTContentAmount:that.addDingeData.RTContentAmount,
          rencaiji:that.addDingeData.dinge_rencaji,
          show:that.addDingeData.show
        },
        success:function(data){
          if(data.issuc){
            alert("添加成功",'',function(){
              that.indexData.dingarr.push(data.resourcerelate);
              if($(".for-color-"+data.resourcerelate.RTItemID).html()==data.comparison){
                $(".for-color-"+data.resourcerelate.RTItemID).attr("style","color:black;");
              }else{
                $(".for-color-"+data.resourcerelate.RTItemID).attr("style","color:red;");
              }
              $("#addDingeDialog").modal("hide");
              that.$nextTick(function(){
                that.editableinit();
              });
            });
          }else{
            alert(data.msg,null,function(){$("#addDingeDialog").modal("hide");});
          }
        },
        error:function(data){}
      });
    });

    $("#addDingeDialog").on("hidden.bs.modal",function(){
      $("#addDingeForm").data('bootstrapValidator').destroy();
      $('#addDingeForm').data('bootstrapValidator', null);
      document.getElementById("addDingeForm").reset();//清空表单
      businessManager.formValidator();
    });

    $("#jstree_demo_div").bind("activate_node.jstree", function(obj, e){  //0：展示清单表格，1：展示费率表，2：展示工料机表；3：展示2000定额工料机表
      var selectedid = e.node.id;
      console.log(selectedid)
      that.can_export = 0;
      if(selectedid.split('-')[0]=='fenbaoyg'||selectedid.split('-')[0]=='zixingyg'){
        that.show_type = 0;
        that.initData(selectedid.split('-')[2],0,0,'notrclick');
      }else if(selectedid.split('-')[0]=='fenbufenxiang'){
        that.show_type = 0;
        that.initData(selectedid.split('-')[1],0,0,'notrclick');
      }else if(selectedid.split('-')[0]=='feilvbiao'){
        that.show_type = 1;
        console.log("获取"+selectedid.split('-')[2]+'的费率');
        that.addFeilvFormData.pact_id = parseInt(selectedid.split('-')[1])
        that.getpsrate_or_resource(selectedid.split('-')[1],1);
      }else if(selectedid.split('-')[0]=='cpresource'){
        console.log("获取"+selectedid.split('-')[1]+'的工料机');
        that.show_type = 3;
        that.getpsrate_or_resource(selectedid.split('-')[1],3);
      }else if(selectedid.split('-')[0]=='cresource'){
        console.log("获取"+selectedid.split('-')[2]+'的工料机');
        that.show_type = 2;
        that.getpsrate_or_resource(selectedid.split('-')[1],2);
        that.can_export = 1;       //如果是1就有导出execl表的功能
        export_tableid = 'right-main-div';  //?
        export_name = '工料机表';           //?
      }else if((selectedid.split('-')[0]=='qitaxiangm')){
        that.show_type = 'qitaxiangm';
        that.initData(selectedid.split('-')[1],0,0,'notrclick','qitaxiangm');
      }
    });
    that.jisuanwidth();
  },
  methods:{
    jisuanwidth:function(t){


    },
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
            if(type==1){    //展示费率表
              that.pactspace_rateData.list = [];
              that.$nextTick(function(){
                that.pactspace_rateData.list = data.ratelist
                that.$nextTick(function(){
                  that.editableinit();
                });
              });
            }else if(type==''){ //工料机表
              that.pactspace_resourceData.list = [];
              that.$nextTick(function(){
                that.pactspace_resourceData.list = data.resourcelist
                that.$nextTick(function(){
                  if(that.show_type!=3){
                    that.editableinit();
                  }
                });
              });
            }else{   //2000定额工料机表
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
      $(".edit-table").editable({    //地下连续墙-定额条目-实际含量验证
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
      $(".edit-table-select").editable({   //?未知验证
        source: sourceoptions,
        title:"人材机选项",
        url :function(params) {
          $.ajax({
            type: "post",
            url: "/business/updateDinge/",
            dataType: "json",
            data: {pk:params.name,name:2,value:params.value},
            success: function(data) {
              console.log($(".for-color-"+data.id).html()+'--------'+data.comparison);
              if($(".for-color-"+data.id).html()==data.comparison){
                $(".for-color-"+data.id).attr("style","color:black;");
              }else{
                $(".for-color-"+data.id).attr("style","color:red;");
              }
              for (var i = that.indexData.dingarr.length-1; i>=0; i--){
                if (that.indexData.dingarr[i].id==params.name){
                    that.indexData.dingarr[i].resourcetype = data.type;
                    that.indexData.dingarr[i].resourcename = data.resourcename;
                    that.indexData.dingarr[i].resourceunit = data.unit;
                    that.indexData.dingarr[i].resourcecode = data.resourcecode;
                    that.indexData.dingarr[i].resourceprice = parseFloat(data.price).toFixed(2);
                }
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
      $(".edit-table-resource").editable({
        validate: function (value) { //字段验证
            if (!$.trim(value)) {
                return '不能为空';
            }else{}
        },
        success: function(a,b,c){

          for (var i = that.pactspace_resourceData.list.length-1; i>=0; i--){
                if (that.pactspace_resourceData.list[i].id==a.relateid){
                    that.pactspace_resourceData.list[i].amount = b;
                }
              }
        }
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
          // for (var i = that.pactspace_resourceData.list.length-1; i>=0; i--){
          //   if (that.pactspace_resourceData.list[i].id==a.relateid){
          //       that.pactspace_resourceData.list[i].amount = b;
          //       console.log(2222222);
          //   }
          // }
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
            url: "/business/spacefeilv/",
            dataType: "json",
            data: {pk:params.pk,name:params.name,value:params.value,type:'update'},
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
       $('.edit-table-select2').editable({
          source: sourceoptions2,
          select2: {
              width: 200,
              placeholder: '选择工料机',
              allowClear: true,
          },
          url :function(params) {
            console.log(JSON.stringify(params));
            $.ajax({
              type: "post",
              url: "/business/updateDinge/",
              dataType: "json",
              data: {pk:params.name,name:2,value:params.value},
              success: function(data) {
                console.log($(".for-color-"+data.id).html()+'--------'+data.comparison);
                if($(".for-color-"+data.id).html()==data.comparison){
                  $(".for-color-"+data.id).attr("style","color:black;");
                }else{
                  $(".for-color-"+data.id).attr("style","color:red;");
                }
                for (var i = that.indexData.dingarr.length-1; i>=0; i--){
                  if (that.indexData.dingarr[i].id==params.name){
                      that.indexData.dingarr[i].resourcetype = data.type;
                      that.indexData.dingarr[i].resourcename = data.resourcename;
                      that.indexData.dingarr[i].resourceunit = data.unit;
                      that.indexData.dingarr[i].resourcecode = data.resourcecode;
                      that.indexData.dingarr[i].resourceprice = parseFloat(data.price).toFixed(2);
                  }
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
    /**
    * 获取清单、定额、关联人材机列表
    * pact_id:分包ID
    * bqid:清单ID,
    * deid:定额ID
    * istr:类型（根据字符串区分）
    **/
    initData:function(pact_id,bqid,deid,istr,type){
      var that = this;
      $(".edit-table").editable("destroy");
      $(".edit-table-buildnums").editable("destroy");
      $(".edit-table-select").editable("destroy");
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
      $.ajax({                  //清单接口传id
          type: "get",
          url: "/business/initmanagerData/",
          dataType: "json",
          data: {pact_id:pact_id,bqid:bqid,deid:deid},
          success: function(data) {
            console.log(data);
            if(!type){  //如果不传type参数就是第二道支撑预算里面的数据请求处理
              if((bqid==0&&deid==0)||(bqid!=0&&pact_id!=0)){
                that.indexData.bqitemlist = data.bqitemlist;
              }
              if(deid==0){
                that.indexData.rtlist = data.rtlist;
              }
              that.indexData.dingarr = data.dingarr;
              that.indexData.rtitem = data.rtitem; 
              
            }else{
              that.other_projectData=data.bqitemlist;
            }


            
            that.$nextTick(function(){
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
          url:'/business/spacefeilv/',
          data:{feilvid:id,type:'delete'},
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
          url:'/business/resourcehandle/',
          data:{id:id,type:'delete'},
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
    rencaijiAdd:function(id,n){
      var that = this;
      if(n!=1){
        n=0;
      }
      that.addDingeData.RTItemID = id;
      that.addDingeData.show = n;
      $("#addDingeDialog").modal("show");
    },
    rencaijiDel:function(id){
      var that = this;
      alertConfirm('确定删除吗',null,function(){
        $.ajax({
          type:'get',
          dateType:'json',
          url:'/business/resourcehandle/',
          data:{id:id,type:'delete'},
          success:function(data){
            alert("删除成功",null,function(){
              if($(".for-color-"+data.RTItemID).html()==data.comparison){
                $(".for-color-"+data.RTItemID).attr("style","color:black;");
              }else{
                $(".for-color-"+data.RTItemID).attr("style","color:red;");
              }
              var arrt;
              for (var i = that.indexData.dingarr.length-1; i>=0; i--){
                if (that.indexData.dingarr[i].id==id){
                    that.indexData.dingarr.splice(i,1);
                    arrt = that.indexData.dingarr;
                }
              }

              that.indexData.dingarr = [];
              that.$nextTick(function(){
                that.indexData.dingarr = arrt;
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
    detailbpact:function(pactid){
      var that = this;
      $.ajax({
          type: "get",
          url: "/business/pacthandle/",
          dataType: "json",
          data: {pact_id:pactid,type:'info'},
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
          url: "/business/pacthandle/",
          dataType: "json",
          data: {pact_id:that.editZbaoFormData.pact_id,pact_name:that.editZbaoFormData.zbao_pactname,type:'update'},
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
          url: "/business/pacthandle/",
          dataType: "json",
          data: {pact_id:pactid,type:'delete'},
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
          if (data.issuc) {
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
        url:'/business/spacemanager/',
        data:{
          id:pid,
          dir:dir,
          type:'move'
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
          url:'/business/spacemanager/',
          data:{
            id:pid,
            type:'delete'
          },
          success:function(data){
            if(data.issuc){
              alert("删除成功","",function(){
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
        url:'/business/spacemanager/',
        data:{
          id:that.editspaceFormData.id,
          spacename:that.editspaceFormData.spacename,
          type:'update'
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
        url:'/business/spacefeilv/',
        data:{
          name : that.addFeilvFormData.feilvname,
          pact_id:that.addFeilvFormData.pact_id,
          parent_id:that.addFeilvFormData.id,
          type:'add'
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
        url:'/business/spacemanager/',
        data:{
          spacename : that.addspaceFormData.spacename,
          type:'add'
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
var mouse_key = 0;
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
});

businessManager = {
  init : function(){
    var that = this;
    that.bindListener();
    that.jstreeInit();
    that.filterInit();
    that.formValidator();
    // $('.selectpicker').selectpicker({
    //     'selectedText': '请选择工料机',
    //     'noneSelectedText':'没有符合的选项'
    // });
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

    $("#btnAddRencaijiResource").bind("click",function(){
      $('#addrencaijiResourceForm').bootstrapValidator('validate');
      if(!($('#addrencaijiResourceForm').data('bootstrapValidator').isValid())){
        return ;
      }
      that.addrencaijiResource();
    });

    $("#addRencaijiResourceDialog").on("hidden.bs.modal",function(){
      $("#addrencaijiResourceForm").data('bootstrapValidator').destroy();
      $('#addrencaijiResourceForm').data('bootstrapValidator', null);
      document.getElementById("addrencaijiResourceForm").reset();//清空表单
      that.formValidator();
    });

    $("#btnAddRencaiji").bind("click",function(){
      if(uploadfile_rcjexecl==''){
        alert("未选择文件");
        return ;
      }
      that.anslysis_rencaijifile(uploadfile_rcjexecl,"btnAddRencaiji");
    });

  },

  addrencaijiResource : function(){
    var name = $("#add_rencaijiresource_name").val();
    var unit = $("#add_rencaijiresource_unit").val();
    var price = $("#add_rencaijiresource_price").val();
    var code = $("#add_rencaijiresource_code").val();
    var resourcetype = $("#add_rencaijiresource_type option:selected").val();
    $.ajax({
      type:'get',
      dataType:'json',
      url:'/business/resourcehandle/',
      data:{'name':name,'unit':unit,'price':price,'code':code,'resourcetype':resourcetype,type:'add'},
      success:function(data){
        alert(data.msg,null,function(){
          if(data.issuc){
            sourceoptions2.push({id:data.resource_id,text:code});
            sourceoptions.push({value:data.resource_id,text:code});
            var selectedobj = document.getElementById("add_dinge_rencaji");
            selectedobj.options[selectedobj.options.length]=new Option(code+name,data.resource_id);
            $("#addRencaijiResourceDialog").modal("hide");
          }
        });
      }
    });
  },

  anslysis_rencaijifile:function(docid,attrid){
    var that = this;

    var buttonel = document.getElementById(attrid);
    buttonel.disabled = true;
    $(".pro-loading").fadeIn();
    $.ajax({
      type:"get",
      url:"/business/analysis_rencaiji_execl",
      dateType:"json",
      data:{'docid':docid},
      success:function(data){
        $(".pro-loading").fadeOut();
        alert("添加人材机成功",null,function(){
            $("#addRencaijiDialog").modal("hide");
            window.location.reload();
          });
      },
      error:function(data){
        $(".pro-loading").fadeOut();
        alert("添加人材机成功",null,function(){
            $("#addRencaijiDialog").modal("hide");
            window.location.reload();
          });
      }
    });
  },

  jstreeInit : function(){
    jstreeitem = $('#jstree_demo_div').jstree({
      'core': {
          'data':{
            'url' : '/business/get_business_tree/',
            'data' : function (node) {
                  console.log(node.id);
                  return { 'id' : node.id };
                }
              }
      },
      "plugins": [
          "wholerow","themes", "json_data","contextmenu"
      ],
      "contextmenu": {
          "items": function (node) {
              var nodeidstr = node.id;
              console.log(nodeidstr);

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
                      console.log(node.id);
                        _app.movespace(node.id.split("-")[1],1);
                    }
                },
                "downspace": {
                    "label": "下移",
                    "icon":"fa fa-file",
                    "separator_after": true,
                    "action": function (data) {
                        _app.movespace(node.id.split("-")[1],-1);
                    }
                },
                "addpact": {
                      "label": "添加",
                      "icon":"fa fa-file",
                      "separator_after": true,
                      "action": function (data) {
                            _app.addzbpactDate.space_id = node.id.split("-")[1];
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
                        _app.editspaceFormData.id = node.id.split("-")[1];
                    }
                },
                "delspace": {
                    "label": "删除",
                    "icon":"fa fa-file",
                    "separator_after": true,
                    "action": function (data) {
                        _app.delspacebyid(node.id.split("-")[1]);
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
    $('#uploadfile_rencaiji').filer({
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
                    // data.docId
                    uploadfile_rcjexecl = data.docId;
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
    $('#addDingeForm').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
          valid: 'glyphicon glyphicon-ok',
          invalid: 'glyphicon glyphicon-remove',
          validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
          add_dinge_rencaji: {
            validators: {
                notEmpty: {
                    message: '人材机不能为空'
                }
            }
          },
          add_dinge_RTContentAmount:{
            validators:{
              notEmpty:{
                message:'含量不能为空'
              },
              regexp:{
                regexp:/^[0-9]+([.]{1}[0-9]+){0,1}$/,
                message:'格式不对',//
              }
            }
          }
        }
    });
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
    $("#addrencaijiResourceForm").bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
          valid: 'glyphicon glyphicon-ok',
          invalid: 'glyphicon glyphicon-remove',
          validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
          add_rencaijiresource_name: {
            validators: {
                notEmpty: {
                    message: '资源名称不能为空'
                },

            }
          },
          add_rencaijiresource_code:{
            validators:{
              notEmpty:{
                message:'资源编号不能为空'
              },
            }
          },
          add_rencaijiresource_type:{
            validators:{
              notEmpty:{
                message:'资源类型不能为空'
              },
            }
          },
          add_rencaijiresource_price: {
            validators: {
                notEmpty: {
                    message: '资源价格不能为空'
                },
                regexp:{
                  message:'格式不对，请输入价格',//
                  regexp:/^[0-9]+([.]{1}[0-9]+){0,1}$/
                }
            }
          },
          add_rencaijiresource_unit: {
            validators: {
                notEmpty: {
                    message: '资源单位不能为空'
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
          // zbao_pacttax: {
          //   validators: {
          //       notEmpty: {
          //           message: '合同税率不能为空'
          //       },
          //       regexp:{
          //         message:'格式不对，请输入合同税率',//
          //         regexp:/^[0-9]+([.]{1}[0-9]+){0,1}$/
          //       }
          //   }
          // },
          // zbao_pacttype: {
          //   validators: {
          //       notEmpty: {
          //           message: '合同类型不能为空'
          //       }
          //   }
          // },
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
