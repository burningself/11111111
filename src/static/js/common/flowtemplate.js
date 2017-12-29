$().ready(function(){
	$("span.assign-btn").click(function(){
			$("div.observer-member-select").css('display','none'); 
			$("div.assign-member-select").css('display','block'); 
			
	 	});
	 
	$("#btnActorConfim").click(function(){
		var configData=new Array();
		$('input[name="actor-checkbox"]:checked').each(function(){    
			 configData.push($(this).val());
		});  
		
		var tmpStr="<br>";
		var tmp="";
		for(each in configData){
			if($(".observer-member-panel").html().indexOf(configData[each]) == -1){
				tmpStr=tmpStr+"&nbsp&nbsp<a>" + configData[each] + "</a>&nbsp&nbsp";	
			}
			else{
				alert("所选用户存在观察者！");
				return ;
			}
		}
		
		$(".assign-member-panel").html(tmpStr);
		
		$("div.assign-member-select").css('display','none'); 
	});
	 
	$("#btnActorCancle").click(function(){
		$("div.assign-member-select").css('display','none'); 
	});
	 
	$("span.observer-btn").click(function(){
		$("div.assign-member-select").css('display','none'); 
		$("div.observer-member-select").css('display','block'); 
	});
	 
	$("#btnObserverConfim").click(function(){
		var configData=new Array();
		$('input[name="observer-checkbox"]:checked').each(function(){    
			 configData.push($(this).val());
		});  
		
		var tmpStr="<br>";
		var tmp="";
		for(each in configData){
			if($(".assign-member-panel").html().indexOf(configData[each]) == -1){
				tmpStr=tmpStr+"&nbsp&nbsp<a>" + configData[each] + "</a>&nbsp&nbsp";	
			}
			else{
				alert("所选用户存在执行者！");
				return ;
			}
		}
		
		$(".observer-member-panel").html(tmpStr);
		
		$("div.observer-member-select").css('display','none'); 
	});
	 
	$("#btnObserverCancle").click(function(){
		$("div.observer-member-select").css('display','none'); 
	});
	
	$("#stepConfigCancel").click(function(){
		$('#TemplateStepConfig').modal('hide');
	})
	
	$("#btnAddTemplateStep").click(function(){
		$('.newStepForm #id_template').removeAttr("disabled");
		var options ={   
	        url:'/task/flowtemplatestep/create/',   
	        type:'post',                    
	        data:null,
	        success:function(data){
	        	console.log(data);
	            if(data.status)
				{
					window.location.reload()
				}
				else
				{
					$(".newStepMsg").html(data.msg);
						$('.newStepForm #id_template').attr("disabled","true");
				}
	        }   
	    };
	        
	    $(".newStepForm").ajaxSubmit(options); 
	});
	
	$("#stepConfigConfirm").click(updateStepConfig);
	
})

function updateStepConfig(){
	var actorStr='';
	var observerStr='';
	
	$(".assign-member-panel a").each(function(){
		actorStr= actorStr+$(this).html()+":";
	})
	
	$(".observer-member-panel a").each(function(){
		observerStr= observerStr+$(this).html()+":";
	})
	
//	console.log(actorStr); console.log(observerStr);
	var ruleStr='';
	var srcStepId=$("#templateStepId").html();
	
	var Error = null;
	$(".action-edit-panel").each(function(){
		ruleStr=ruleStr + $(this).children(".actortype").val() + "_" + $(this).children(".sourceStep").val() + "_" + $(this).children(".targetStep").val()+ ":"; 
		if(!$(this).children(".sourceStep").val()||$(this).children(".sourceStep").val()==""){
			Error="步骤操作不能名称为空！";
		}
	})
	
	if(Error){
		alert(Error);
		return;
	}
//	console.log(ruleStr);

	$.ajax({
		type:"post",
		url:"/task/flowtemplatestep/edit/"+srcStepId+"/",
		cache:false,
		dataType:"json",
		data:{"actorStr":actorStr,"observerStr":observerStr,"ruleStr":ruleStr},
		success: function(data){
			if(data.status==1)
			{
				window.location.reload();
			}
			else
			{
				alert(data.error);
			}
		}
	});
	
}

function infoControl(tpid){
	if($('.basicTab').hasClass('active')){
//		var options ={   
//          url:window.location.pathname,   
//          type:'post',                    
//          data:null,
//          success:function(data){
//              if(data.issuc==true)
//				{
//					alert("保存成功！");
//					$(".infoBtn").html('<i class="fa fa-cog"></i> 编辑基本信息'); 
//					$('.basicTab').removeClass('active');
//					$('.basicTab input').attr('readonly',"true");
//					$('.basicTab select').attr('readonly',"true");	
//					$('.basicTab').css("color","darkgray");
//				}
//				else
//				{
//					alert(data.error);
//				}
//          }   
//      };
//      
//      $(".infoForm").ajaxSubmit(options); 
        
        
        	var templateName = $('#templateName').val();
			var templateMajor = $('#templateMajor').val();
			var templateType = $('#templateType').val();
			var templateDesc = $('#templateDesc').val();
			
			var selBrowsers = [];
			$("#templateuser option:selected").each(function(){
					selBrowsers.push($(this).val());
			});

		
			$.ajax({
				type: "post",
//				url: "/task/flowtemplate/create/",
				cache: false,
				dataType: "json",
				data: {
					"templateName": templateName,
					"templateMajor": templateMajor,
					"templateType": templateType,
					"templateDesc": templateDesc,
					"selBrowsers":JSON.stringify(selBrowsers),
				},
				success: function(data) {
					if (data.issuc == "true") {
						alert("保存成功！");
						$(".infoBtn").html('<i class="fa fa-cog"></i> 编辑基本信息'); 
						$('.basicTab').removeClass('active');
						$('.basicTab input').attr('readonly',"true");
						$('.basicTab select').attr('readonly',"true");	
						$('.basicTab').css("color","darkgray");
					} else {
						alert(data.error);
					}
				}
			});
	}
	else{
		$('.basicTab').addClass("active");
		$(".infoBtn").html('<i class="fa fa-save"></i> 保存基本信息'); 
		$('.basicTab input').removeAttr('readonly');
		$('.basicTab select').removeAttr('readonly');
		$('.basicTab').css("color","black");
	}
}
	
function lockControl(obj){
	if($(".lockBtn .fa-lock").length>0){
		$(obj).html('<i class="fa fa-unlock"></i> 解锁排序');
		$('.sortable').sortable( 'disable' ) ;
		$(".box").css("border","");
	}else{
		$(obj).html('<i class="fa fa-lock"></i> 锁定阶段排序');
		$('.sortable').sortable( 'enable' );
		$(".box").css("border","groove 6px");
	}
}

function FunTemplateStepConfig(StepId){
	$.ajax({
		type:"post",
		url:"/task/flowtemplatestep/get/"+StepId.toString()+"/",
		cache:false,
		dataType:"json",
		data:{},
		success: function(data){
			if(data.status==1)
			{	
				var operaTempStr="";
//				for(each in data.stpOperList){
//					operaTempStr += "<option value=" + data.stpOperList[each].id.toString()
//					+ ">" + data.stpOperList[each].name + "</option>";
//				}
//				
//				$(".srcStepList").html(operaTempStr);	

				$('#templateStepId').html(StepId);

				$(".assign-member-panel").html($("#"+ StepId.toString()+' .assign-panel-body').html());
				$(".observer-member-panel").html($("#"+ StepId.toString()+' .observer-panel-body').html());
				
				$(" .actor-select input").prop("checked", false);
				$(".assign-member-panel a").each(function(){
					var chooseUser=$(this).html();
					$(" .actor-select input[value='" + chooseUser +"']").prop("checked", true);
				});
				
				$(" .observer-select input").prop("checked", false);
				$(".observer-member-panel a").each(function(){
					var chooseUser=$(this).html();
					$(".observer-select input[value='" + chooseUser +"']").prop("checked", true);
				});
				
				$(".action-list").html('');
				$("#"+ StepId.toString()+' .ruleContent').each(function(index,obj){
					AddAction();
				});
				$("#"+ StepId.toString()+' .ruleContent').each(function(index,obj){
					actorStr = $($(obj).children(".keyword")[0]).html();
					stepStr = $($(obj).children(".keyword")[1]).html();
					nextStepStr = $($(obj).children(".keyword")[2]).html();
			
					$($(".action-edit-panel")[index]).children(".actortype").children("option").each(function(){
						if($(this).html()==actorStr){$(this).attr("selected", "selected"); 
							console.log($(this).prop("outerHTML"));}
						
					})
					
					$($(".action-edit-panel")[index]).children(".sourceStep").val(stepStr);
					
					$($(".action-edit-panel")[index]).children(".targetStep").children("option").each(function(){
						if($(this).html()==nextStepStr){$(this).attr("selected", "selected");}
					})
				});
				$('#TemplateStepConfig').modal('show');
				
			}
			else
			{
				alert(data.error);
			}
		}
	});
}

function FunChangeTemplateStepInfo(StepId){
	$.ajax({
	type:"get",
	url:"/task/flowtemplatestep/update/"+StepId.toString()+"/",
	cache:false,
	dataType:"json",
	data:{"stpId":StepId,},
	success: function(data){
		if(data.status==1)
		{	
			$(".updateStepForm").html(data.form);
			$(".updateStepForm #id_template").attr("disabled","true");
			$(".updateStepForm #id_sequence").attr("disabled","true");
		}
		else
		{
			alert(data.error);
		}
	}
	});
	
	$("#btnChangeTemplateStepInfo").removeAttr("onclick");
	$("#btnChangeTemplateStepInfo").attr("onclick","updateInfo("+StepId.toString()+")");
	$('#ChangeTemplateStepInfo').modal('show');
}

function updateInfo(stepId){	
	$(".updateStepForm #id_template").removeAttr("disabled");
	$(".updateStepForm #id_sequence").removeAttr("disabled");
	var options ={   
        url: "/task/flowtemplatestep/update/"+stepId.toString()+"/",
        type:'post',                    
        data:null,
        success:function(data){
            if(data.status==1)
			{
				alert("修改成功！"); 
				$('#ChangeTemplateStepInfo').modal('hide');
				window.location.reload();
			}
			else
			{
				alert(data.msg);
			}
        }   
    };
	        
	$(".updateStepForm").ajaxSubmit(options); 
}

function removeStep(stpid){
	if(confirm("确认要删除阶段吗？")){
		$.ajax({
			type:"post",
			url:"/task/flowtemplatestep/delete/",
			cache:false,
			dataType:"json",
			data:{"stpid":stpid,},
			success: function(data){
				if(data.status==1)
				{
					alert("删除成功！");
					window.location.reload();
				}
				else
				{
					alert(data.error);
				}
			}
		});	
	}
}

function AddAction(){ 
$("#action-list").append(' <div class="action-edit-panel"  style="overflow-x:auto;margin-bottom:2px">  \
	<select class="actortype" name="actortype" class="mod-input"> \
	</select> \
		<label class="control-label" class="mod-input">执行者</label> \
		<input name="sourceStep" class="stepControl sourceStep mod-input"></input>  \
		<label class="control-label">该步骤自动移至</label> \
	<select class="stepControl targetStep" name="targetStep" class="mod-input"> \
	</select>  \
	    <a type="button" id="btnObserverConfim" class="btn btn-primary btn-sm pull-right"><i class="fa fa-check"></i></a>  \
		<a type="button" name="rmlink" id="btnObserverCancle" class="btn btn-danger btn-sm pull-right"><i class="fa fa-trash-o"></i></a>  \
	</div>'); 
	
	// 为新元素节点添加事件侦听器
	bindListener();
//	$(".sourceStep").html($(".srcStepList").html());
	$(".targetStep").html($(".tgtStepList").html());
	$(".actortype").html($(".actorMode").html());
	$(".targetStep option[value=" + $("#templateStepId").html() + "]").remove();
}

 // 用来绑定事件(使用unbind避免重复绑定)
function bindListener(){
  $("a[name=rmlink]").unbind().click(function(){
    $(this).parent().remove(); 
  });
}

 //监听键盘，只允许输入数字和小数点 
$(".checkNum").keypress(function(event) { 
    var keyCode = event.which; 
    if ((keyCode >= 48 && keyCode <=57)) 
        return true; 
    else 
        return false; 
}).focus(function() { 
    this.style.imeMode='disabled'; 
}); 

$(".checkNum").keyup(function(){     
	var tmptxt=$(this).val();     
	$(this).val(tmptxt.replace(/\D|^0/g,''));     
}).bind("paste",function(){     
	var tmptxt=$(this).val();     
	$(this).val(tmptxt.replace(/\D|^0/g,''));     
}).css("ime-mode", "disabled"); 
 