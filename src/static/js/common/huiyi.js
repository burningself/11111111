	var documentsStr = '';
	var removeDocumentsStr = '';
	var selectedValues = [];
	$(document).ready(function() {
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
		    if(data.node.id != "#" && data.node.id!="rootprjusertree"&& data.node.id.indexOf("_")==-1) {
				var sdate = {"value":data.node.id,"text":data.node.text};
				moveOption(sdate, document.getElementById('right'),'right','addhuiyiForm')
		    }		
		});	
		
		$("#left2").jstree({
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
		$('#left2').bind("select_node.jstree", function (evt, data) {
			
		    // 处理代码
		    if(data.node.id != "#" && data.node.id!="rootprjusertree"&& data.node.id.indexOf("_")==-1) {
				var sdate = {"value":data.node.id,"text":data.node.text};
				moveOption(sdate, document.getElementById('right2'),'right2','editHuiyiForm')
		    }
			
		});	
		
		formValidator();

		$("#right2").on("mouseenter",".noattend",function(){
			$(".shownoattend").html("缺席原因："+$(this).attr("data")).show();
		});
		$("#right2").on("mouseleave",".noattend",function(){
			$(".shownoattend").hide();
		});
		$("#clickaddhuiyi").bind("click",function(){
			var selDate = moment(new Date()).format('YYYY-MM-DD'); //格式化日期
			var selTime = moment(new Date()).format('HH:mm'); //格式化日期
			$("#hysrq").val(selDate+" 09:00");
			$("#hyerq").val(selDate+" 18:00");
			FunAddMeetting(selDate)
		});
	    //Modal验证销毁重构
	    $('#addmeet').on('hidden.bs.modal', function() {
	        $("#addhuiyiForm").data('bootstrapValidator').destroy();
	        $('#editHuiyiForm').data('bootstrapValidator', null);
	        formValidator();
	    });
	    $('#editmeet').on('hidden.bs.modal', function() {
	        $("#addhuiyiForm").data('bootstrapValidator').destroy();
	        $('#editHuiyiForm').data('bootstrapValidator', null);
	        $("#btnEditHuiyi").show();
	        $("#btnDeleteHuiyi").show();
			$("#addFileRoot").show();
	        
	        document.getElementById("edit_meetname").disabled = false;
			document.getElementById("ehysrq").disabled = false;
			document.getElementById("ehyerq").disabled = false;
			document.getElementById("edit_qdescribe").disabled = false;
			document.getElementById("edit_issuePriority").disabled = false;
			document.getElementById("edit_meetroon").disabled = false;
			document.getElementById("left2").disabled = false;
			document.getElementById("right2").disabled = false;
	        formValidator();
	    });
	    $("#hysrq").bind("click",function(){
			$('#hysrq').datetimepicker({
				language: 'zh-CN',//显示中文
				autoclose: true,//选中自动关闭
			}).on('hide',function(e) {
	            $('#addhuiyiForm').data('bootstrapValidator')
	               .updateStatus('hysrq', 'NOT_VALIDATED',null)
	               .validateField('hysrq');
	            });
		});
		$("#hysrq").click();

	    $("#ehysrq").bind("click",function(){
			$('#ehysrq').datetimepicker({
				language: 'zh-CN',//显示中文
				autoclose: true,//选中自动关闭
			}).on('hide',function(e) {
	            $('#editHuiyiForm').data('bootstrapValidator')
	               .updateStatus('ehysrq', 'NOT_VALIDATED',null)
	               .validateField('ehysrq');
	            });
		})
		$("#ehysrq").click();

	    $("#ehyerq").bind("click",function(){
			$('#ehyerq').datetimepicker({
				language: 'zh-CN',//显示中文
				autoclose: true,//选中自动关闭
			}).on('hide',function(e) {
	            $('#editHuiyiForm').data('bootstrapValidator')
	               .updateStatus('ehyerq', 'NOT_VALIDATED',null)
	               .validateField('ehyerq');
	            });
		});
		$("#ehyerq").click();
	    $("#hyerq").bind("click",function(){
			$('#hyerq').datetimepicker({
				language: 'zh-CN',//显示中文
				autoclose: true,//选中自动关闭
			}).on('hide',function(e) {
	            $('#addhuiyiForm').data('bootstrapValidator')
	               .updateStatus('hyerq', 'NOT_VALIDATED',null)
	               .validateField('hyerq');
	            });
		});
		$("#hyerq").click();

		$('#btnFaqiWenTi').click(function() {
			//判断是否可以提交表单
			$('#addhuiyiForm').bootstrapValidator('validate');
			if(!($('#addhuiyiForm').data('bootstrapValidator').isValid())){
				return ;
			}
			addHuiyiInfo();
		});

		$("#btnEditHuiyi").bind("click",function(){
			$('#editHuiyiForm').bootstrapValidator('validate');
			console.log(!$('#editHuiyiForm').data('bootstrapValidator').isValid());
			if(!($('#editHuiyiForm').data('bootstrapValidator').isValid())){
				return ;
			}
			editHuiyiInfo();
		});

		$("#btnDeleteHuiyi").bind("click", function() {
		    $.ajax({
		        type: "get",
		        url: "/assist/deleteMeeting/",
		        dataType: "json",
		        data: { meetid: $("#edit_meetid").val() },
		        success: function(data) {
					$("#editmeet").modal("hide");
					window.location.reload();
		        },		
				error: function(e){
					if(e.status==403){
						alert("您没有权限删除会议，请联系管理员！");
					}else{
						alert("服务器错误！")
					}
				}
		    });
		});

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
                    filesLimit: "只能同时上传 {{fi-limit}}个文件 。",
                    filesType: "只能上传MicrosoftProject文件",
                    filesSize: "{{fi-name}} 太大! 最大允许上传 {{fi-fileMaxSize}} MB。",
                    filesSizeAll: "Files you've choosed are too large! Please upload files up to {{fi-maxSize}} MB。",
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

        $('#agian_add').filer({
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
                    filesLimit: "只能同时上传 {{fi-limit}}个文件 。",
                    filesType: "只能上传MicrosoftProject文件",
                    filesSize: "{{fi-name}} 太大! 最大允许上传 {{fi-fileMaxSize}} MB。",
                    filesSizeAll: "Files you've choosed are too large! Please upload files up to {{fi-maxSize}} MB。",
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

		//日历操作
		$('#calendar').fullCalendar({
			header: {
				left: 'prev,next today',
				center: 'title',
				right: 'month,agendaWeek,agendaDay,listMonth'
			},
			defaultDate: getNowFormatDate(),
			locale: 'zh-cn',
			navLinks: true, // can click day/week names to navigate views
			businessHours: true, // display business hours
			editable: true,

			events: function(start,end,timezone, callback){
				var date = this.getDate().format('YYYY-MM');
				var year = date.substring(0,4);
				var month = date.substring(5,7);
				$.ajax({
					type: "get",
					url: "/assist/loadMeetingDatas/",
					dataType: "json",
					data: {
						year:year,
						month:month
					},
					success: function(data) {
						var events = [];
						var meetingslist = data.meetings;
						if(meetingslist!=null&&meetingslist.length>0){
							for(var i=0;i<meetingslist.length;i++){
								var meetingmodel = meetingslist[i];
								events.push({
									title: meetingmodel.title,
									mid: meetingmodel.mid,
									room_id: meetingmodel.room_id,
									roomname:meetingmodel.roomname,
									meetingtype:meetingmodel.meetingtype,
									start: meetingmodel.start,
									end: meetingmodel.end,
									constraint: meetingmodel.constraint,
									color: meetingmodel.color,
									canupdate:meetingmodel.canupdate,
									contant:meetingmodel.contant,
									huiyitype:meetingmodel.huiyitype,
								});
							}
						}
						callback(events);
					},
					error:function(data){
						if(data.status==403){
							alert("您要访问的数据没有权限，请联系管理员！");
						}
					}
				});
			},
			dayClick: function(date, allDay, jsEvent, view) {
				var selDate = moment(date).format('YYYY-MM-DD'); //格式化日期
				var selTime = moment(date).format('HH:mm'); //格式化日期
				$("#hysrq").val(selDate+" 09:00");
				$("#hyerq").val(selDate+" 18:00");
				$(".timevalid").hide();
				FunAddMeetting(selDate)
			},
			eventClick: function(calEvent, jsEvent, view) {
				$("#hyinfo_files").html("");
				$("#edit_qdescribe").val(calEvent.contant);
				$("#edit_meetname").val(calEvent.title)
				$("#edit_meetid").val(calEvent.mid);
				$("#edit_issuePriority").val(calEvent.meetingtype);
				$("#edit_meetroon").val(calEvent.roomname);
				var selDate = moment(calEvent.start).format('YYYY-MM-DD HH:mm'); //格式化日期
				$("#ehysrq").val(selDate);
				selDate = moment(calEvent.end).format('YYYY-MM-DD HH:mm'); //格式化日期
				$("#ehyerq").val(selDate);
				$(".timevalid").hide();
				if(calEvent.canupdate!=1){
					$("#btnEditHuiyi").hide();
					$("#btnDeleteHuiyi").hide();
					$("#addFileRoot").hide();
					document.getElementById("edit_meetname").disabled = true;
					document.getElementById("ehysrq").disabled = true;
					document.getElementById("ehyerq").disabled = true;
					document.getElementById("edit_qdescribe").disabled = true;
					document.getElementById("edit_issuePriority").disabled = true;
					document.getElementById("edit_meetroon").disabled = true;
					document.getElementById("left2").disabled = true;
					document.getElementById("right2").disabled = true;
				}
				//获取参会人员
				$.ajax({
					type:"get",
					url:"/assist/getMeetingMember/",
					dataType:"json",
					data:{meetid:calEvent.mid,huiyitype:calEvent.huiyitype},
					success:function(data){
						var str = '';
						if(data.issuc=='true'&&data.meetingusers.length>0){
							var meetusers = data.meetingusers;
							for(var i=0;i<meetusers.length;i++){
								var usermodel = meetusers[i];
								// str+='<option value="'+usermodel.user_id+'" >'+usermodel.truename+'</option>';
								if(usermodel.isattend==1){
									str+='<option class="attend" value="'+usermodel.user_id+'" >'+usermodel.truename+'(参加)</option>';
								}else if(usermodel.isattend==2){
									str+='<option class="noattend" data="'+usermodel.reason+'" value="'+usermodel.user_id+'" >'+usermodel.truename+'(不参加)</option>';
									//onmouseover="showinfo(this)"
								}else{
									str+='<option class="attendunkown" value="'+usermodel.user_id+'" >'+usermodel.truename+'(未确认)</option>';
								}
							}
							$("#right2").html(str);
						}
					},
					error:function(data){
						console.log("获取参会人员异常");
					}
				});

				$.ajax({
					type:"get",
					url:"/assist/getMeetingFile/",
					dataType:"json",
					data:{meetid:calEvent.mid,huiyitype:calEvent.huiyitype},
					success:function(data){
						var files = data.meetingfiles;
		                    if(files.length>0){
		                        var filestr = '<tbody>';
		                        for(var i=0;i<files.length;i++){
		                            var fileitem = files[i];
		                            filestr+='<tr>';
		                            if(fileitem.isrecord=="1"){
		                                filestr+='<td style="text-align: left;"><a href="/'+fileitem.filepath+'" style="cursor: pointer; target="_blank"">'+fileitem.filename+'(纪要)</a></td>';
		                            }else{
		                                filestr+='<td style="text-align: left;"><a href="/'+fileitem.filepath+'" style="cursor: pointer;" target="_blank">'+fileitem.filename+'</a></td>';
		                            }
		                            filestr+='<td style="width:100px;"><a href="/'+fileitem.filepath+'" title="删除文件" style="cursor: pointer;" target="_blank">[查看]</a>';
		                            if(calEvent.canupdate==1){
		                            	filestr+='<a  href="javascript:void(0);" style="cursor: pointer;" onclick="removeFile(this,'+fileitem.fileid+')" value="'+fileitem.fileid+'">[删除]</a>';
		                            }
		                            filestr+='</td>';
		                            filestr+='</tr>';
		                        }
		                        filestr += '</tbody>';
		                        $("#hyinfo_files").html(filestr);
		                    }
					},
					error:function(data){
						console.log("获取数据异常");
					}
				});
				$('#editmeet').modal('show');
			},
			eventMouseover: function (calEvent, jsEvent, view) {
				$(this).attr('title', calEvent.title);
				$(this).css('font-size', 'larger');
//				$(this).attr('title', calEvent);
//				$(this).css('font-weight', 'normal');
//				$(this).tooltip({
//					effect: 'toggle',
//					cancelDefault: true
//				});
			},
			eventMouseout: function (calEvent, jsEvent, view) {
				$(this).attr('title', calEvent.title);
				$(this).css('font-size', 'small');
//				$(this).attr('title', calEvent);
//				$(this).css('font-weight', 'normal');
//				$(this).tooltip({
//					effect: 'toggle',
//					cancelDefault: true
//				});
			},

		});

	});


	function removeFile(sefl,fileid){
			$(sefl).parent().parent().hide();
			if( removeDocumentsStr == ''){
				removeDocumentsStr += fileid;
			}else{
				removeDocumentsStr +='#'+fileid;
			}
	}
	function addHuiyiInfo() {
		//表单验证码成功，执行你的操作
		var meetname = $("#meetname").val();
		var issuePriority = $("#issuePriority option:selected").val();
		var meetroom = $("#meetroon").val();
		var hyzt = $("#hyzt").val();
		var hysrq = $("#hysrq").val();
		hysrq = hysrq + ":00";
		var hyerq = $("#hyerq").val();
		hyerq = hyerq + ":00";
		selectedValues = [];
		$("#right option").each(function(){
			selectedValues.push($(this).val());
		});
		$.ajax({
			type: "get",
			url: "/assist/createhuiyi/",
			dataType: "json",
			data: {
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
				if (data.issuc == "true") {
					$("#addmeet").modal("hide");
					window.location.reload();
				} else {}
			},		
			error: function(e){
				if(e.status==403){
					alert("您没有权限编辑会议，请联系管理员！");
				}else{
					alert("服务器错误！")
				}
			}
		});
	}


	//修改会议信息
	function editHuiyiInfo() {
		var meetid = $("#edit_meetid").val();
		var meetname = $("#edit_meetname").val();
		var issuePriority = $("#edit_issuePriority option:selected").val();
		var meetroom = $("#edit_meetroon").val();
		var hyzt = $("#edit_qdescribe").val();
		var hysrq = $("#ehysrq").val();
		hysrq = hysrq +":00";
		var hyerq = $("#ehyerq").val();
		hyerq = hyerq +":00";
		selectedValues = [];
		$("#right2 option").each(function(){
			selectedValues.push($(this).val());
		});
		$.ajax({
			type: "get",
			url: "/assist/edithuiyi/",
			dataType: "json",
			data: {
				"meetname": meetname,
				"issuePriority": issuePriority,
				"meetroom": meetroom,
				"hyzt": hyzt,
				"selectedValues": selectedValues.join("#"),
				"hysrq": hysrq,
				"hyerq": hyerq,
				"documents": documentsStr,
				"meetid":meetid,
				"removedocuments":removeDocumentsStr
			},
			success: function(data) {
				if(data.issuc = "true"){
					$("#editmeet").modal("hide");
					window.location.reload();
				}else {}
			},		
			error: function(e){
				if(e.status==403){
					alert("您没有权限编辑会议，请联系管理员！");
				}else{
					alert("服务器错误！")
				}
			}
		});
	}

	//时间比较（yyyy-MM-dd HH:mm:ss）
	function compareTime(startTime,endTime) {
	  var startTimes = startTime.substring(0, 10).split('-');
	  var endTimes = endTime.substring(0, 10).split('-');
	  startTime = startTimes[1] + '-' + startTimes[2] + '-' + startTimes[0] + ' ' + startTime.substring(10, 19);
	  endTime = endTimes[1] + '-' + endTimes[2] + '-' + endTimes[0] + ' ' + endTime.substring(10, 19);
	  var thisResult = (Date.parse(endTime) - Date.parse(startTime)) / 3600 / 1000;
	  if (thisResult < 0) {
	    return -1;
	  } else if (thisResult > 0) {
	    return 1;
	  } else if (thisResult == 0) {
	    return 0;
	  } else {
	    return '异常';
	  }
	}


	function getNowFormatDate() {
		var date = new Date();
		var seperator1 = "-";
		var seperator2 = ":";
		var month = date.getMonth() + 1;
		var strDate = date.getDate();
		if(month >= 1 && month <= 9) {
			month = "0" + month;
		}
		if(strDate >= 0 && strDate <= 9) {
			strDate = "0" + strDate;
		}
		var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate;
		return currentdate;
	}

	function FunAddMeetting() {
		$('#addmeet').modal('show');
	}

	//获取日历中的会议信息
	function loadCalendarMeetingDatas() {

	}

	function moveOption(obj1, obj2,field,fromid) {

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
	}


	function deleteOption(obj,field,fromid) {
		
		for(var i = obj.options.length - 1; i >= 0; i--) {
			if(obj.options[i].selected) {
				obj.remove(i);
			}
		}
		$('#'+fromid).data('bootstrapValidator')
	               .updateStatus(field, 'NOT_VALIDATED',null)
	               .validateField(field);
	}
	
	
	function moveOption2(obj1, obj2,field,fromid) {
		// $("#selectmember2").hide();
		for(var i = obj1.options.length - 1; i >= 0; i--) {
			// console.log(obj1.options[i].text);
			if(obj1.options[i].selected) {
				var opt = new Option(obj1.options[i].text, obj1.options[i].value);
				opt.selected = true;
				obj2.options.add(opt);
				obj1.remove(i);
			}
		}
		$('#'+fromid).data('bootstrapValidator')
	               .updateStatus(field, 'NOT_VALIDATED',null)
	               .validateField(field);
	}
	
	

	function formValidator(){
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
	                            max: 120,
	                            message: '会议名称3-120个字'
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
	                        	max: 500,
	                        	message: '会议主题5-500个字'
	                        }
	                    }
	                },
	                hysrq:{
	                	validators: {
	                        notEmpty: {
	                            message: '开始时间不能为空'
	                        },
	                        callback: {
		                        message: '开始日期不能大于结束日期',
		                        callback:function(value, validator,$field,options){
		                            var end = $('#hyerq').val();
		                            validator.updateStatus('hyerq', 'VALID');
		                            return new Date(value)<=new Date(end);
		                        }
		                    }
	                    }
	                },
	                hyerq:{
	                	validators: {
	                        notEmpty: {
	                            message: '结束时间不能为空'
	                        },
	                        callback: {
		                        message: '结束日期不能小于开始日期',
		                        callback:function(value, validator,$field){
		                            var begin = $('#hysrq').val();
		                            console.log(value);
		                            $('#hysrq').keypress();
		                            validator.updateStatus('hysrq', 'VALID');
		                            return new Date(value)>=new Date(begin);
		                        }
		                    }
	                    }
	                }
	            }
	        });
	    $('#editHuiyiForm')
	        .bootstrapValidator({
	            message: 'This value is not valid',
	            feedbackIcons: {
	                valid: 'glyphicon glyphicon-ok',
	                invalid: 'glyphicon glyphicon-remove',
	                validating: 'glyphicon glyphicon-refresh'
	            },
	            fields: {
	                edit_meetname: {
	                    message: 'The username is not valid',
	                    validators: {
	                        notEmpty: {
	                            message: '会议名称不能为空'
	                        },
	                        stringLength: {
	                            min: 3,
	                            max: 120,
	                            message: '会议名称3-120个字'
	                        }
	                    }
	                },
	                edit_issuePriority: {
		                validators: {
		                    notEmpty: {
		                        message: '会议类型为必选'
		                    }
		                }
		            },

		            edit_meetroon: {
		                validators: {
		                    notEmpty: {
		                        message: '会议室为必选'
		                    }
		                }
		            },
	                edit_qdescribe: {
	                    validators: {
	                        notEmpty: {
	                            message: '主题不能为空'
	                        },
	                        stringLength: {
	                        	min: 5,
	                        	max: 500,
	                        	message: '会议主题5-500个字'
	                        }
	                    }
	                },
	                right2:{
		            	validators:{
		                    callback:{
		                    	message:'参会人员不能为空',
		                    	callback:function(value, validator,$field,options){
		                            var v = $("#right2 option").length;
		                            return v==0?false:true;
		                        }
		                    }
		            	}
		            },
	                ehysrq:{
	                	validators: {
	                        notEmpty: {
	                            message: '开始时间不能为空'
	                        },
	                        callback: {
		                        message: '开始日期不能大于结束日期',
		                        callback:function(value, validator,$field,options){
		                            var end = $('#ehyerq').val();
		                            validator.updateStatus('ehyerq', 'VALID');
		                            return new Date(value)<=new Date(end);
		                        }
		                    }
	                    }
	                },
	                ehyerq:{
	                	validators: {
	                        notEmpty: {
	                            message: '结束时间不能为空'
	                        },
	                        callback: {
		                        message: '结束日期不能小于开始日期',
		                        callback:function(value, validator,$field){
		                            var begin = $('#ehysrq').val();
		                            console.log(value);
		                            $('#ehysrq').keypress();
		                            validator.updateStatus('ehysrq', 'VALID');
		                            return new Date(value)>=new Date(begin);
		                        }
		                    }
	                    }
	                }
	            }
	        });
	}


