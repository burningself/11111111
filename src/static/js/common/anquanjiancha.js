
var datatable_options = {
	  "iDisplayLength": 15,
      "searching": true,
      "ordering":  false,
      "bLengthChange":false,
      "bInfo":true,
      //"bStateSave": true, //保存状态到cookie *************** 很重要 ， 当搜索的时候页面一刷新会导致搜索的消失。使用这个属性就可避免了
      "pagingType": "input",
      "oLanguage": {
      	 	"sEmptyTable": "没有相关记录",
            "sLengthMenu": "每页显示 _MENU_ 条记录",
            "sZeroRecords": "对不起，查询不到相关数据",
            "sInfo": "当前显示 _START_ 到 _END_ 条，共 _TOTAL_ 条记录",
            "sInfoEmpty": "第 0 到 0 条记录，共 0 条",
            "sInfoFiltered": "数据表中共为 _MAX_ 条记录",
            "sProcessing": "正在加载中...",
            "sSearch": "搜索",
            "sUrl": "", //多语言配置文件，可将oLanguage的设置放在一个txt文件中，例：Javascript/datatable/dtCH.txt
            "oPaginate": {
                "sFirst":    "首页",
                "sPrevious": " 上一页 ",
                "sNext":     " 下一页 ",
                "sLast":     " 尾页 "
            }
        }, //多语言配置
        dom: 'Bftirp',
        "buttons": [{
				text: '新增安全检查',
//				className: "createbtn",
				action: function(e, dt, node, config) {
					addjiancha();
				}
			}

		],
        "aLengthMenu": [[15, 25, 50, -1, 0], ["每页5条", "每页25条", "每页50条", "显示所有数据", "不显示数据"]]
};
$(function(){
  $(':input').labelauty();
  anquanjianchaManager.init();
  $('.datatable').dataTable(datatable_options);

});

function addjiancha(){
	$("#addjiancha").modal("show");
}

var anquanjianchaManager = {
  init : function(){
    var that = this;
    that.bindListener();

    that.formValidator();
  },

  bindListener:function(){
    var that = this;

	    $("#zhouqitype").bind("change",function(){
            // console.log("内容改变"+$("#zhouqitype").val());
            $("#createtime").val('');
            var zhouqitype = $("#zhouqitype").val();
            if(zhouqitype=="每天"){
                $(".time-day").removeClass("active").addClass("unactive");
                $(".time-week").removeClass("active").addClass("unactive");
                $(".zhoutimeselect").removeClass("active").addClass("unactive");
                $(".createtimediv").removeClass("active").addClass("unactive");
            }else if(zhouqitype=="每周"){
                $(".createtimediv").removeClass("unactive").addClass("active");
                $(".zhoutimeselect").removeClass("unactive").addClass("active");
                $(".time-day").removeClass("active").addClass("unactive");
                $(".time-week").removeClass("unactive").addClass("active");
            }else if(zhouqitype=="每月"){
                $(".createtimediv").removeClass("unactive").addClass("active");
                $(".zhoutimeselect").removeClass("unactive").addClass("active");
                $(".time-week").removeClass("active").addClass("unactive");
                $(".time-day").removeClass("unactive").addClass("active");
            }
        });

        $("#createtime").bind("focus",function(){
            var zhouqitype = $("#zhouqitype").val();
            if(zhouqitype=="每天"){
                $(".time-day").removeClass("active").addClass("unactive");
                $(".time-week").removeClass("active").addClass("unactive");
                $(".zhoutimeselect").removeClass("active").addClass("unactive");
                $(".createtimediv").removeClass("active").addClass("unactive");
            }else if(zhouqitype=="每周"){
                $(".createtimediv").removeClass("unactive").addClass("active");
                $(".zhoutimeselect").removeClass("unactive").addClass("active");
                $(".time-day").removeClass("active").addClass("unactive");
                $(".time-week").removeClass("unactive").addClass("active");
            }else if(zhouqitype=="每月"){
                $(".createtimediv").removeClass("unactive").addClass("active");
                $(".zhoutimeselect").removeClass("unactive").addClass("active");
                $(".time-week").removeClass("active").addClass("unactive");
                $(".time-day").removeClass("unactive").addClass("active");
            }
        });

        $(".labelauty").bind("click",function(){
            var createtimeval = $("#createtime").val();
            var value = $("#"+this.id).attr("data");
            if(createtimeval.indexOf(value)>=0){
                createtimeval = createtimeval.replace(','+value,'').replace(value+',','').replace(value,'');;
                $("#createtime").val(createtimeval);
            }else{
                if(createtimeval==null||createtimeval==""){
                    $("#createtime").val(value);
                }else{
                    createtimeval+=','+value
                    $("#createtime").val(createtimeval);
                }
            }
            if($("#createtime").val()!=null&&$("#createtime").val()!=""){
                $("#createtime-small").hide();
            }
        });

        $(".time-week-btn").bind("click",function(){
            if($("#createtime").val()==null||$("#createtime").val()==""){
                $("#createtime-small").show();
            }else{
                $(".time-day").removeClass("active").addClass("unactive");
                $(".time-week").removeClass("active").addClass("unactive");
                $(".zhoutimeselect").removeClass("active").addClass("unactive");
            }
        });
        $(".time-day-btn").bind("click",function(){
            if($("#createtime").val()==null||$("#createtime").val()==""){
                $("#createtime-small").show();
            }else{
                $(".time-day").removeClass("active").addClass("unactive");
                $(".time-week").removeClass("active").addClass("unactive");
                $(".zhoutimeselect").removeClass("active").addClass("unactive");
            }
        });


    $("#btnAddJiancha").bind("click",function(){
      $('#addJianchaForm').bootstrapValidator('validate');
      if(!($('#addJianchaForm').data('bootstrapValidator').isValid())){
        return ;
      }
      that.addJiancha();
    });


    $("#btnEditJiancha").bind("click",function(){
      $('#editJianchaForm').bootstrapValidator('validate');
      if(!($('#editJianchaForm').data('bootstrapValidator').isValid())){
        return ;
      }
      that.editAction();
    });

  },

  editJiancha:function(id){
  	
  
  },
  editAction:function(){

  },
  detailJiancha:function(id){
	window.open("/task/anquan/jianchadetail/?jianchaId="+id); 
  },
  batchJiancha:function(id){
	window.open("/task/anquan/jianchajiancha/?jianchaId="+id); 
  },
  delJiancha:function(id){
  	if(!confirm("确认删除？")){
  		return;
  	}
    $.ajax({
        type:'post',
        dataType:'json',
        //url:'/business/delTaskorderByid/',
        data:{"opt":"delete","id":id},
        success:function(data){
            if(data.issuc == "true"){
                alert("删除成功");
                window.location.reload();
            }
            else{
            	alert(data.error);
            }
        },
        error:function(data){}
    });
  },

  addJiancha:function(){
     
   	var jsonobj = $('#addJianchaForm').serializeJSON();
	jsonobj.opt='create';

	$.ajax({
		type: "post",
		cache: false,
		dataType: "json",
		data: jsonobj,
		success: function(data) {
			if(data.issuc == "true") {
				alert("添加成功");
				window.location.reload(true);
			} else {
				alert(data.error);
			}

		}
	});
	$('#addjiancha').modal('hide');
	
  },


  formValidator :function(){
    $('#addJianchaForm').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
          valid: 'glyphicon glyphicon-ok',
          invalid: 'glyphicon glyphicon-remove',
          validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
          new_name: {
            validators: {
                notEmpty: {
                    message: '名称不能为空'
                },
				stringLength: {
					min: 3,
					max: 64,
					message: '名称3-64个字'
				}
              }
          },
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
          edit_taskorder_money: {
            validators: {
                notEmpty: {
                    message: ''
                }
              }
          },
          edit_taskorder_position:{
            validators: {
                notEmpty: {
                    message: '名称不能为空'
                }
              }
          }
        }
    });
  }
}