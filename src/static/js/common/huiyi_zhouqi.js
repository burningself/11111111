var documentsStr = '';
var selectedValues = [];
$(function(){

	
    $(':input').labelauty();
    huiyizhouqi.init();
    
    $("#left").jstree({
		   		"core": {
		   			'data': {
		   				'url': '/user/prjusertree/',
		   				'data': function(node) {
		   					return {
		   						'id': node.id
		   					};
		   				}
		   			}
		   		},
		   		"plugins": ["themes", "json_data"],
		});
		$('#left').bind("select_node.jstree", function (evt, data) {
			
		    // 处理代码
		    if(data.node.id != "#" && data.node.id!="rootprjusertree"&& data.node.id.indexOf("cmp_")==-1) {
				var sdate = {"value":data.node.id,"text":data.node.text};
				huiyizhouqi.moveOption(sdate, document.getElementById('right'),'right','addhuiyiForm')
		    }
			
		});	
})
var huiyizhouqi = {
    time_week_data : {
        "星期一":"labelauty-Monday",
        "星期二":"labelauty-Tuesday",
        "星期三":"labelauty-Wednesday",
        "星期四":"labelauty-Thursday",
        "星期五":"labelauty-Friday",
        "星期六":"labelauty-Saturday",
        "星期日":"labelauty-Sunday",
    },
    time_day_data : {
        "01":"labelauty-0d1",
        "02":"labelauty-0d2",
        "03":"labelauty-0d3",
        "04":"labelauty-0d4",
        "05":"labelauty-0d5",
        "06":"labelauty-0d6",
        "07":"labelauty-0d7",
        "08":"labelauty-0d8",
        "09":"labelauty-0d9",
        "10":"labelauty-1d10",
        "11":"labelauty-1d11",
        "12":"labelauty-1d12",
        "13":"labelauty-1d13",
        "14":"labelauty-1d14",
        "15":"labelauty-1d15",
        "16":"labelauty-1d16",
        "17":"labelauty-1d17",
        "18":"labelauty-1d18",
        "19":"labelauty-1d19",
        "20":"labelauty-2d20",
        "21":"labelauty-2d21",
        "22":"labelauty-2d22",
        "23":"labelauty-2d23",
        "24":"labelauty-2d24",
        "25":"labelauty-2d25",
        "26":"labelauty-2d26",
        "27":"labelauty-2d27",
        "28":"labelauty-2d28",
        "29":"labelauty-2d29",
        "30":"labelauty-3d30",
        "31":"labelauty-3d31",

    },
    init : function(){
        var that = this;
        that.formValidator();
        that.bindlistener();
        that.filterinit();
        that.daterangepickerinit();
    },
    bindlistener:function(){
        var that = this;

        $("#hysrq").bind("click",function(){
            $('#hysrq').clockpicker({
                placement: 'top',
                // donetext:'',
                afterDone: function() {
                    $('#addhuiyiForm').data('bootstrapValidator')
                   .updateStatus('hysrq', 'NOT_VALIDATED',null)
                   .validateField('hysrq');
                }
            })
        });
        $("#hysrq").click();

        $("#hyerq").bind("click",function(){
            $('#hyerq').clockpicker({
                placement: 'top',
                afterDone: function() {
                    $('#addhuiyiForm').data('bootstrapValidator')
                   .updateStatus('hyerq', 'NOT_VALIDATED',null)
                   .validateField('hyerq');
                }
            })
        });
        $("#hyerq").click();


        $("#btn_addzhouqihuiyi").bind("click",function(){
            $("#hysrq").val("09:00");
            $("#hyerq").val("16:00");
            $("#hhuititle").html("添加会议模板");
            $("#addzhouqihuiyi").modal("show");
        });

        $("#btnAddhuiyi").bind("click",function(){
            var ccurid = $("#edithuiyicid").val();
            //判断是否可以提交表单
            $('#addhuiyiForm').bootstrapValidator('validate');
            if(!($('#addhuiyiForm').data('bootstrapValidator').isValid())){
                return ;
            }
            if(ccurid==null||ccurid==""){
                that.addHuiyiInfo();
            }else{
                that.editHuiyiInfo(ccurid);
            }

        });

        $('#addzhouqihuiyi').on('hidden.bs.modal', function() {
            console.log("表单验证清除");
            document.getElementById("zhouqitype").disabled = false;
            document.getElementById("meetname").disabled = false;
            document.getElementById("issuePriority").disabled = false;
            document.getElementById("hyzt").disabled = false;
            document.getElementById("meetroon").disabled = false;
            document.getElementById("left").disabled = false;
            document.getElementById("right").disabled = false;
            document.getElementById("hysrq").disabled = false;
            document.getElementById("hyerq").disabled = false;
            document.getElementById("uploadfile_fujian").disabled=false;
            $("#btnAddhuiyi").show();
            $("#addhuiyiForm").data('bootstrapValidator').destroy();
            $('#addhuiyiForm').data('bootstrapValidator', null);
            $(".zhoutimeselect").removeClass("active").addClass("unactive");
            $(".huiyifiles").removeClass("active").addClass("unactive");
            // $(".createtimediv").hide();
            document.getElementById("addhuiyiForm").reset();//重置表单
            that.formValidator();
        });

        $("#createtime").bind("focus",function(){
            var zhouqitype = $("#zhouqitype").val();
            if(zhouqitype==1){
                $(".time-day").removeClass("active").addClass("unactive");
                $(".time-week").removeClass("active").addClass("unactive");
                $(".zhoutimeselect").removeClass("active").addClass("unactive");
                $(".createtimediv").removeClass("active").addClass("unactive");
            }else if(zhouqitype==2){
                $(".createtimediv").removeClass("unactive").addClass("active");
                $(".zhoutimeselect").removeClass("unactive").addClass("active");
                $(".time-day").removeClass("active").addClass("unactive");
                $(".time-week").removeClass("unactive").addClass("active");
            }else if(zhouqitype==3){
                $(".createtimediv").removeClass("unactive").addClass("active");
                $(".zhoutimeselect").removeClass("unactive").addClass("active");
                $(".time-week").removeClass("active").addClass("unactive");
                $(".time-day").removeClass("unactive").addClass("active");
            }
        });
        // $("#createtime").bind("blur",function(){
        //      console.log("失去焦点");
        //     // $(".zhoutimeselect").removeClass("active").addClass("unactive");
        // });

        $("#zhouqitype").bind("change",function(){
            // console.log("内容改变"+$("#zhouqitype").val());
            $("#createtime").val('');
            var zhouqitype = $("#zhouqitype").val();
            if(zhouqitype==1){
                $(".time-day").removeClass("active").addClass("unactive");
                $(".time-week").removeClass("active").addClass("unactive");
                $(".zhoutimeselect").removeClass("active").addClass("unactive");
                $(".createtimediv").removeClass("active").addClass("unactive");
            }else if(zhouqitype==2){
                $(".createtimediv").removeClass("unactive").addClass("active");
                $(".zhoutimeselect").removeClass("unactive").addClass("active");
                $(".time-day").removeClass("active").addClass("unactive");
                $(".time-week").removeClass("unactive").addClass("active");
            }else if(zhouqitype==3){
                $(".createtimediv").removeClass("unactive").addClass("active");
                $(".zhoutimeselect").removeClass("unactive").addClass("active");
                $(".time-week").removeClass("active").addClass("unactive");
                $(".time-day").removeClass("unactive").addClass("active");
            }

            var ccurid = $("#edithuiyicid").val();
            $(".labelauty").attr("checked",false);//隐藏时重置checkbox的选中状态
        });

        $(".labelauty").bind("click",function(){
            console.log(111);
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

        $("#truedelhuiyi").bind("click",function(){
            that.delhuiyifunc();
        });
    },

    edithuiyi:function(id,t){
        var that = this;
        $("#edithuiyicid").val(id);
        $.ajax({
            type: "get",
            url: "/assist/loadHuiyiZhouqiInfo/",
            dataType: "json",
            data: { meetid:id},
            success: function(data) {
                if(data.issuc=='true'){
                    $("#meetname").val(data.meetinginfo.name);
                    var hyinfo_type = data.meetinginfo.meetingtype;
                    var zhouqi_type = data.meetinginfo.zhouqitype;
                    var select = document.getElementById("zhouqitype");
                    var select2 = document.getElementById("issuePriority");
                    select.options[zhouqi_type-1].selected = true;
                    select2.options[hyinfo_type-1].selected = true;

                    var create_time = data.meetinginfo.create_time;
                    if(zhouqi_type==1){
                        $(".time-day").removeClass("active").addClass("unactive");
                        $(".time-week").removeClass("active").addClass("unactive");
                        $(".zhoutimeselect").removeClass("active").addClass("unactive");
                        $(".createtimediv").removeClass("active").addClass("unactive");
                    }else if(zhouqi_type==2){
                        $(".createtimediv").removeClass("unactive").addClass("active");
                        var create_timearr = create_time.split(",")
                        for(var i=0;i<create_timearr.length;i++){
                            var timeitem = create_timearr[i];
                            var weekid = that.time_week_data[timeitem];
                            $("#"+weekid).click();
                        }
                    }else if(zhouqi_type==3){
                        $(".createtimediv").removeClass("unactive").addClass("active");
                        var create_timearr = create_time.split(",")
                        for(var i=0;i<create_timearr.length;i++){
                            var timeitem = create_timearr[i];
                            var dayid = that.time_day_data[timeitem];
                            $("#"+dayid).click();
                        }
                    }

                    $("#hyzt").val(data.meetinginfo.description);
                    $("#meetroon").val(data.meetinginfo.roomname);
                    $("#hysrq").val(data.meetinginfo.start);
                    $("#hyerq").val(data.meetinginfo.end);

                    //获取参会人员
                    $.ajax({
                        type:"get",
                        url:"/assist/getMeetingZhouqiMember/",
                        dataType:"json",
                        data:{meetid:id},
                        success:function(data){
                            var str = '';
                            if(data.issuc=='true'&&data.meetingusers.length>0){
                                var meetusers = data.meetingusers;
                                for(var i=0;i<meetusers.length;i++){
                                    var usermodel = meetusers[i];
                                    str+='<option value="'+usermodel.user_id+'" >'+usermodel.truename+'</option>';
                                }
                                $("#right").html(str);
                            }
                        },
                        error:function(data){
                            console.log("获取参会人员异常");
                        }
                    });
                    var files = data.meetinginfo.files;
                    if(files.length>0){
                        var filestr = '<tbody>';
                        for(var i=0;i<files.length;i++){
                            var fileitem = files[i];
                            filestr+='<tr>';
                            var filenamestr = fileitem.filename;
                            if(filenamestr.length>15){
                                filenamestr = filenamestr.substring(0,15)+"..."
                            }
                            if(fileitem.isrecord=="1"){
                                filestr+='<td style="width: 75%;text-align: left;"><a href="/'+fileitem.filepath+'" style="cursor: pointer; target="_blank"">'+filenamestr+'(纪要)</a></td>';
                            }else{
                                filestr+='<td style="width: 75%;text-align: left;"><a href="/'+fileitem.filepath+'" style="cursor: pointer;" target="_blank">'+filenamestr+'</a></td>';
                            }
                            filestr+='<td><a href="/'+fileitem.filepath+'" title="查看文件" style="cursor: pointer;" target="_blank">[查看]</a></td>';
                            filestr+='</tr>';
                        }
                        filestr += '</tbody>';
                        $("#hyinfo_files").html(filestr);
                        $(".huiyifiles").removeClass("unactive").addClass("active");
                    }
                    // $("#huiyidetail").modal("show");
                }else{
                    // $("#common_show").modal("show");
                }
            },
            error: function(data) {}
        });
        if(t!=1){
            document.getElementById("zhouqitype").disabled = true;
            document.getElementById("meetname").disabled = true;
            document.getElementById("issuePriority").disabled = true;
            document.getElementById("hyzt").disabled = true;
            document.getElementById("meetroon").disabled = true;
            document.getElementById("left").disabled = true;
            document.getElementById("right").disabled = true;
            document.getElementById("hysrq").disabled = true;
            document.getElementById("hyerq").disabled = true;
            document.getElementById("uploadfile_fujian").disabled=true;
            $("#btnAddhuiyi").hide();
        }
        $("#zhouqitype").attr("disabled",true);
        $("#createtime").attr("disabled",true);
        $("#hhuititle").html("编辑会议模板");
        $("#addzhouqihuiyi").modal("show");
    },

    delhuiyifunc : function(){
        $.ajax({
            type: "get",
            url: "/assist/deleteMeetingZhouqi/",
            dataType: "json",
            data: { meetid:$("#currhyid").val()},
            success: function(data) {
                $("#deletehuiyiModal").modal("hide");
                window.location.reload();
            },		
			error: function(e){
				if(e.status==403){
					alert("您没有权限删除周期会议，请联系管理员！");
				}else{
					alert("服务器错误！")
				}
			}
        });
    },

    editHuiyiInfo:function(id) {
        //表单验证码成功，执行你的操作
        var zhouqitype = $("#zhouqitype").val();
        var createtime = '';
        if(zhouqitype==1){

        }else if(zhouqitype==2){
            createtime = $("#createtime").val();
        }else if(zhouqitype==3){
            createtime = $("#createtime").val();
        }
        var meetname = $("#meetname").val();
        var issuePriority = $("#issuePriority option:selected").val();
        var meetroom = $("#meetroon").val();
        var hyzt = $("#hyzt").val();
        var hysrq = $("#hysrq").val();
        var hyerq = $("#hyerq").val();
        selectedValues = [];
        $("#right option").each(function(){
            selectedValues.push($(this).val());
        });
        $.ajax({
            type: "get",
            url: "/assist/editzhouqihuiyi/",
            dataType: "json",
            data: {
                "zhouqitype":zhouqitype,
                "createtime":createtime,
                "meetname": meetname,
                "issuePriority": issuePriority,
                "meetroom": meetroom,
                "hyzt": hyzt,
                "selectedValues": selectedValues.join("#"),
                "documents": documentsStr,
                "meetid": id,
                "hysrq": hysrq,
                "hyerq": hyerq
            },
            success: function(data) {
                if (data.issuc = "true") {
                    $("#addhuiyiForm").modal("hide");
                    window.location.reload();
                } else {}
            },		
			error: function(e){
				if(e.status==403){
					alert("您没有权限编辑周期会议，请联系管理员！");
				}else{
					alert("服务器错误！")
				}
			}
        });
    },

    addHuiyiInfo:function() {
        //表单验证码成功，执行你的操作
        var zhouqitype = $("#zhouqitype").val();
        var createtime = '';
        if(zhouqitype==1){

        }else if(zhouqitype==2){
            createtime = $("#createtime").val();
        }else if(zhouqitype==3){
            createtime = $("#createtime").val();
        }
        var meetname = $("#meetname").val();
        var issuePriority = $("#issuePriority option:selected").val();
        var meetroom = $("#meetroon").val();
        var hyzt = $("#hyzt").val();
        var hysrq = $("#hysrq").val();
        var hyerq = $("#hyerq").val();
        selectedValues = [];
        $("#right option").each(function(){
            selectedValues.push($(this).val());
        });
        $.ajax({
            type: "get",
            url: "/assist/createzhouqihuiyi/",
            dataType: "json",
            data: {
                "zhouqitype":zhouqitype,
                "createtime":createtime,
                "meetname": meetname,
                "issuePriority": issuePriority,
                "meetroom": meetroom,
                "hyzt": hyzt,
                "selectedValues": selectedValues.join("#"),
                "documents": documentsStr,
                "hysrq": hysrq,
                "hyerq": hyerq
            },
            success: function(data) {
                if (data.issuc = "true") {
                    $("#addhuiyiForm").modal("hide");
                    window.location.reload();
                } else {}
            },		
			error: function(e){
				if(e.status==403){
					alert("您没有权限编辑周期会议，请联系管理员！");
				}else{
					alert("服务器错误！")
				}
			}
        });
    },

    daterangepickerinit:function(){

        // $("#hysrq").bind("click",function(){
        //     $('#hysrq').datetimepicker({
        //         startView:'day',
        //         format:'hh:ii',
        //         language: 'zh-CN',//显示中文
        //         autoclose: true,//选中自动关闭
        //     }).on('hide',function(e) {
        //         $('#addhuiyiForm').data('bootstrapValidator')
        //            .updateStatus('hysrq', 'NOT_VALIDATED',null)
        //            .validateField('hysrq');
        //         });
        // });
        // $("#hysrq").click();

        // $("#hyerq").bind("click",function(){
        //     $('#hyerq').datetimepicker({
        //         format:'hh:ii',
        //         language: 'zh-CN',//显示中文
        //         autoclose: true,//选中自动关闭
        //     }).on('hide',function(e) {
        //         $('#addhuiyiForm').data('bootstrapValidator')
        //            .updateStatus('hyerq', 'NOT_VALIDATED',null)
        //            .validateField('hyerq');
        //         });
        // })
        // $("#hyerq").click();
    },

    filterinit:function(){
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
                    filesLimit: "只能同时上传个文件 。",
                    filesType: "只能上传MicrosoftProject文件",
                    filesSize: "太大! 最大允许上传 MB。",
                    filesSizeAll: "Files you've choosed are too large! Please upload files up to MB。",
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
                        if(documentsStr==""){
                            documentsStr+=data.docId;
                        }else{
                            documentsStr+='#'+data.docId;
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

    deletehuiyi : function(obj){
        var that = this;
        $("#currhyid").val(obj)
        $("#deletehuiyiModal").modal("show");
    },

    moveOption:function(obj1, obj2,field,fromid){
		var isSelected = false;
		for(var i = obj2.options.length - 1; i >= 0; i--) {
			if(obj2.options[i].value==obj1.value) {
				isSelected = true;
				return;
			}
		}
		
		if(!isSelected){
			var opt = new Option(obj1.text, obj1.value);
			opt.selected = true;
			obj2.options.add(opt);
		}
		
		$('#'+fromid).data('bootstrapValidator')
	               .updateStatus(field, 'NOT_VALIDATED',null)
	               .validateField(field);
    },

    deleteOption:function(obj,field,fromid) {
		for(var i = obj.options.length - 1; i >= 0; i--) {
			if(obj.options[i].selected) {
				obj.remove(i);
			}
		}
		$('#'+fromid).data('bootstrapValidator')
	               .updateStatus(field, 'NOT_VALIDATED',null)
	               .validateField(field);
    },

    formValidator:function(){
        $('#addhuiyiForm').bootstrapValidator({
                message: 'This value is not valid',
                feedbackIcons: {
                    valid: 'glyphicon glyphicon-ok',
                    invalid: 'glyphicon glyphicon-remove',
                    validating: 'glyphicon glyphicon-refresh'
                },
                fields: {
                    meetname: {
                        message: 'The username is not valid',
                        validators: {
                            notEmpty: {
                                message: '会议名称不能为空'
                            },
                            stringLength: {
                                min: 3,
                                max: 15,
                                message: '会议名称3-15个字'
                            }
                        }
                    },
                    issuePriority: {
                        validators: {
                            notEmpty: {
                                message: '会议类型为必选'
                            }
                        }
                    },

                    meetroon: {
                        validators: {
                            notEmpty: {
                                message: '会议室为必选'
                            }
                        }
                    },
                    right:{
                        validators:{
                            callback:{
                                message:'参会人员不能为空',
                                callback:function(value, validator,$field,options){
                                    var v = $("#right option").length;
                                    return v==0?false:true;
                                }
                            }
                        }
                    },
                    hyzt: {
                        validators: {
                            notEmpty: {
                                message: '主题不能为空'
                            },
                            stringLength: {
                                min: 5,
                                max: 30,
                                message: '会议主题5-30个字'
                            }
                        }
                    },
                    hysrq:{
                        validators: {
                            // notEmpty: {
                            //     message: '开始时间不能为空'
                            // },
                            callback: {
                                message: '开始日期不能为空且需小于结束日期',
                                callback:function(value, validator,$field,options){
                                    var end = $('#hyerq').val();
                                    var beginpre = value.substring(0,2);
                                    var beginend = value.substring(3,5);
                                    var endpre = end.substring(0,2);
                                    var endend = end.substring(3,5);
                                    validator.updateStatus('hyerq', 'VALID');
                                    $('#hyerq').keypress();
                                    if(parseInt(beginpre)<parseInt(endpre)){
                                        return true;
                                    }else if(parseInt(beginpre)==parseInt(endpre)){
                                        if(parseInt(beginend)<parseInt(endend)){
                                            return true;
                                        }else{
                                            return false;
                                        }
                                    }else{
                                        return false;
                                    }
                                    // return new Date(value)<=new Date(end);
                                }
                            }
                        }
                    },
                    hyerq:{
                        validators: {
                            // notEmpty: {
                            //     message: '结束时间不能为空'
                            // },
                            callback: {
                                message: '结束日期不能为空且需大于开始日期',
                                callback:function(value, validator,$field){
                                    var begin = $('#hysrq').val();
                                    var beginpre = begin.substring(0,2);
                                    var beginend = begin.substring(3,5);
                                    var endpre = value.substring(0,2);
                                    var endend = value.substring(3,5);
                                    $('#hysrq').keypress();
                                    validator.updateStatus('hysrq', 'VALID');

                                    if(parseInt(beginpre)<parseInt(endpre)){
                                        return true;
                                    }else if(parseInt(beginpre)==parseInt(endpre)){
                                        if(parseInt(beginend)<parseInt(endend)){
                                            return true;
                                        }else{
                                            return false;
                                        }
                                    }else{
                                        return false;
                                    }
                                    // return new Date(value)>=new Date(begin);
                                }
                            }
                        }
                    }
                }
            });
    }
}
