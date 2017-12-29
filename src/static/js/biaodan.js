
//ueditor start
var ue;
var _curMbId="";

function initUE(){
    UE.registerUI('添加数据源', function(editor, uiName) {
        //注册按钮执行时的command命令，使用命令默认就会带有回退操作
        editor.registerCommand(uiName, {
            execCommand: function() {
                FunXuanShuJuYuan();
                
            }
        });
        //创建一个button
        var btn = new UE.ui.Button({
            //按钮的名字
            name: uiName,
            //提示
            title: uiName,
            //添加额外样式，指定icon图标，这里默认使用一个重复的icon
            cssRules: 'background-position: -500px 0;',
            //点击时执行的命令
            onclick: function() {
                //这里可以不用执行命令,做你自己的操作也可
                editor.execCommand(uiName);
            }
        });
        //当点到编辑内容上时，按钮要做的状态反射
        editor.addListener('selectionchange', function() {
            var state = editor.queryCommandState(uiName);
            if (state == -1) {
                btn.setDisabled(true);
                btn.setChecked(false);
            } else {
                btn.setDisabled(false);
                btn.setChecked(state);
            }
        });
        //因为你是添加button,所以需要返回这个button
        return btn;
    });
    
    UE.registerUI('设置权限', function(editor, uiName) {
        //注册按钮执行时的command命令，使用命令默认就会带有回退操作
        editor.registerCommand(uiName, {
            execCommand: function() {
                
                FunSheZhiQuanXian();
            }
        });
        //创建一个button
        var btn = new UE.ui.Button({
            //按钮的名字
            name: uiName,
            //提示
            title: uiName,
            //添加额外样式，指定icon图标，这里默认使用一个重复的icon
            cssRules: 'background-position: -620px -40px;',
            //点击时执行的命令
            onclick: function() {
                //这里可以不用执行命令,做你自己的操作也可
                editor.execCommand(uiName);
            }
        });
        //当点到编辑内容上时，按钮要做的状态反射
        editor.addListener('selectionchange', function() {
            var state = editor.queryCommandState(uiName);
//          if (state == -1) {
//              btn.setDisabled(true);
//              btn.setChecked(false);
//          } else {
//              btn.setDisabled(false);
//              btn.setChecked(state);
//          }
            
            var viewdoc = document.getElementById('ueditor_0').contentWindow.document;
			var tdarr = UE.dom.domUtils.getElementsByTagName(viewdoc,"td");
			for (var i = 0, td; td = tdarr[i++];) {
				if(UE.dom.domUtils.hasClass( td, "selectTdClass" ))
				{
					btn.setDisabled(false);
					btn.setChecked(state);
                	return;
				}
		      }
			
		 	 btn.setDisabled(true);
             btn.setChecked(false);
		 
        });
        //因为你是添加button,所以需要返回这个button
        return btn;
    });
    
    UE.registerUI('取消权限设置', function(editor, uiName) {
        //注册按钮执行时的command命令，使用命令默认就会带有回退操作
        editor.registerCommand(uiName, {
            execCommand: function() {
                
                funRemoveAuth();
            }
        });
        //创建一个button
        var btn = new UE.ui.Button({
            //按钮的名字
            name: uiName,
            //提示
            title: uiName,
            //添加额外样式，指定icon图标，这里默认使用一个重复的icon
            cssRules: 'background-position: -640px 0px;',
            //点击时执行的命令
            onclick: function() {
                //这里可以不用执行命令,做你自己的操作也可
                editor.execCommand(uiName);
            }
        });
        //当点到编辑内容上时，按钮要做的状态反射
        editor.addListener('selectionchange', function() {
            var state = editor.queryCommandState(uiName);
//          if (state == -1) {
//              btn.setDisabled(true);
//              btn.setChecked(false);
//          } else {
//              btn.setDisabled(false);
//              btn.setChecked(state);
//          }
            
            var viewdoc = document.getElementById('ueditor_0').contentWindow.document;
			var tdarr = UE.dom.domUtils.getElementsByTagName(viewdoc,"td");
			for (var i = 0, td; td = tdarr[i++];) {
				if(UE.dom.domUtils.hasClass( td, "selectTdClass" )&&UE.dom.domUtils.hasClass( td, "setauthclass" ))
				{
					btn.setDisabled(false);
					btn.setChecked(state);
                	return;
				}
		      }
			
		 	 btn.setDisabled(true);
             btn.setChecked(false);
		 
        });
        //因为你是添加button,所以需要返回这个button
        return btn;
    });
    
    ue = UE.getEditor('editor',{
        initialFrameHeight:600,
        autoHeightEnabled: true,
        autoFloatEnabled: true,
        //关闭字数统计  
        wordCount:false,  
        //关闭elementPath  
        elementPathEnabled:false,  
    });
}
var shujuyuanid

function FunXuanShuJuYuan() {
    $('#shujuyuan').modal('show');
};
var select_shujuyuan=[];//统计选中的数据源
function FunXuanShuJuYuanOK(){
    // ue.execCommand("inserthtml","{{"+shujuyuanid.text+"}}");
    select_shujuyuan.push($('input:radio:checked').val())
    var tag = "{{"+$('input:radio:checked').attr('content') +"}}"
    ue.execCommand("inserthtml",tag);
}


function FunSheZhiQuanXian() {
	$("#sel_relatedflowstep").empty();  
	$.ajax({
		type:"get",
		url:"/assist/biaodanmuban/getrelatestep/",
		dataType:"json",
		async:true,
		data:{"mbId":_curMbId},
		success: function(data){
			for(var i=0;i<data.relatestep.length;i++)
			{
				var option = "<option  value='"+ data.relatestep[i].id  +"'>"+data.relatestep[i].name+"</option>";
				$("#sel_relatedflowstep").append(option);
			}
			$('#quanxianshezhidlg').modal('show');
		}
	});
	
	
    
};

function SheZhiQuanXianOK(){
	var relateStep = $("#sel_relatedflowstep").val();
	funRemoveAuth();
	var viewdoc = document.getElementById('ueditor_0').contentWindow.document;
	var tdarr = UE.dom.domUtils.getElementsByTagName(viewdoc,"td");
	for (var i = 0, td; td = tdarr[i++];) {
		if(UE.dom.domUtils.hasClass( td, "selectTdClass" ))
		{
			UE.dom.domUtils.addClass( td, "setauthclass" );
			UE.dom.domUtils.addClass( td, "flowstep_"+relateStep);
			UE.dom.domUtils.setStyle( td, 'background-color', '#F3F0D2' );
		}
    }
	
}

	function funRemoveAuth(){
		var viewdoc = document.getElementById('ueditor_0').contentWindow.document;
		var tdarr = UE.dom.domUtils.getElementsByTagName(viewdoc,"td");
		for (var i = 0, td; td = tdarr[i++];) {
			if(UE.dom.domUtils.hasClass( td, "selectTdClass" )&&UE.dom.domUtils.hasClass( td, "setauthclass" ))
			{
				UE.dom.domUtils.removeStyle(td, "background-color");
				var  classArr = td.className.split(" ");
				for(var j=0;j<classArr.length;j++){
					if(classArr[j]!="selectTdClass"){
						UE.dom.domUtils.removeClasses( td, classArr[j] );
					}
				}

			}
        }
	}
	

function isFocus(e){
    alert(UE.getEditor('editor').isFocus());
    UE.dom.domUtils.preventDefault(e)
}
function setblur(e){
    UE.getEditor('editor').blur();
    UE.dom.domUtils.preventDefault(e)
}
function insertHtml() {
    var value = prompt('插入html代码', '');
    UE.getEditor('editor').execCommand('insertHtml', value)
}
function createEditor() {
    enableBtn();
    UE.getEditor('editor');
}
function getAllHtml() {
    alert(UE.getEditor('editor').getAllHtml())
}
function getContent() {
//  var arr = [];
//  arr.push("使用editor.getContent()方法可以获得编辑器的内容");
//  arr.push("内容为：");
//  arr.push(UE.getEditor('editor').getContent());
//  alert(arr.join("\n"));
    return UE.getEditor('editor').getContent()
}
function getPlainTxt() {
    var arr = [];
    arr.push("使用editor.getPlainTxt()方法可以获得编辑器的带格式的纯文本内容");
    arr.push("内容为：");
    arr.push(UE.getEditor('editor').getPlainTxt());
    alert(arr.join('\n'))
}
function setContent(isAppendTo) {
//  var arr = [];
//  arr.push("使用editor.setContent('欢迎使用ueditor')方法可以设置编辑器的内容");
    UE.getEditor('editor').setContent(isAppendTo);
//  alert(arr.join("\n"));
}
function setDisabled() {
    UE.getEditor('editor').setDisabled('fullscreen');
    disableBtn("enable");
}

function setEnabled() {
    UE.getEditor('editor').setEnabled();
    enableBtn();
}

function getText() {
    //当你点击按钮时编辑区域已经失去了焦点，如果直接用getText将不会得到内容，所以要在选回来，然后取得内容
    var range = UE.getEditor('editor').selection.getRange();
    range.select();
    var txt = UE.getEditor('editor').selection.getText();
    alert(txt)
}

function getContentTxt() {
    var arr = [];
    arr.push("使用editor.getContentTxt()方法可以获得编辑器的纯文本内容");
    arr.push("编辑器的纯文本内容为：");
    arr.push(UE.getEditor('editor').getContentTxt());
    alert(arr.join("\n"));
}
function hasContent() {
    var arr = [];
    arr.push("使用editor.hasContents()方法判断编辑器里是否有内容");
    arr.push("判断结果为：");
    arr.push(UE.getEditor('editor').hasContents());
    alert(arr.join("\n"));
}
function setFocus() {
    UE.getEditor('editor').focus();
}
function deleteEditor() {
    disableBtn();
    UE.getEditor('editor').destroy();
}
function disableBtn(str) {
    var div = document.getElementById('btns');
    var btns = UE.dom.domUtils.getElementsByTagName(div, "button");
    for (var i = 0, btn; btn = btns[i++];) {
        if (btn.id == str) {
            UE.dom.domUtils.removeAttributes(btn, ["disabled"]);
        } else {
            btn.setAttribute("disabled", "true");
        }
    }
}
function enableBtn() {
    var div = document.getElementById('btns');
    var btns = UE.dom.domUtils.getElementsByTagName(div, "button");
    for (var i = 0, btn; btn = btns[i++];) {
        UE.dom.domUtils.removeAttributes(btn, ["disabled"]);
    }
}

function getLocalData () {
    alert(UE.getEditor('editor').execCommand( "getlocaldata" ));
}

function clearLocalData () {
    UE.getEditor('editor').execCommand( "clearlocaldata" );
//  alert("已清空草稿箱")
}
//ueditor end

var id=-1;
function saveMuban()
{
	if($("#mname").val().length==0){
		alert("模板名称不能为空！");
		return;
	}
	
	if(getContent().length==0){
		alert("模板内容不能为空！");
		return;
	}
	
    var dat = {
        "id":id,
        "name":$("#mname").val(),
        "major":$('.major-s option:selected').val(),
        "formtype":$('.formtype-s option:selected').val(),
        "content":getContent(),
        "select_shujuyuan":JSON.stringify(select_shujuyuan),
    }
     $.ajax({
       type:"post",
       url:"/assist/biaodanmuban/",
//       cache:false,
       async: false,
//       dataType:"json",
       data:JSON.stringify(dat),
       success: function(data){
			select_shujuyuan=[];
			alert("模板保存成功！");
			window.location.reload();
       }
     });
    
        
};

function deleteMb(obj){
    var res = confirm("确认要删除吗？");
    if(!res){
        return
    }
    var tr = obj.parentNode.parentNode;
    var tdlist = $(tr).children('td');
    var mbID =$(tdlist[0]).html();
    var dat = {
        "id":mbID,
    }
     $.ajax({
       type:"delete",
       url:"/assist/biaodanmuban/",
       cache:false,
       async: false,
//       dataType:"json",
       data:JSON.stringify(dat),
       success: function(data){
       		if(data.res=="succ"){
       			$(tr).remove();
       		}
       		else
       		{
       			alert("模板已经被使用！");
       		}
        
       }
     });
}

function editMb(obj){
    var tr = obj.parentNode.parentNode;
    var tdlist = $(tr).children('td');
    var mbID =$(tdlist[0]).html();
    _curMbId=mbID;
    var dat = {
        "id":mbID,
        'from':'editMb',
    }
    id = mbID;
    
    $.ajax({
      url:"/assist/biaodanmuban/",
      data: dat,
      async: false,
      success: function(data){
          var jdata = JSON.parse(data);
        setContent(jdata.content);
        $("#mname").val(jdata.name);
        $(".major-s").val(jdata.major);
        $(".formtype-s").val(jdata.formtype);
       }
//      dataType: dataType
    });
    $(".bb1").css("display","none");
    $(".bb2").css("display","block");
}


function addMb() {
    id = -1;
    $("#mname").val('');
    setContent('');
    $(".bb1").css("display","none");
    $(".bb2").css("display","block");
}

function fanhui() {
    $(".bb1").css("display","block");
    $(".bb2").css("display","none");
    select_shujuyuan=[];
}

var biaodantype

function saveTable()
{
     
    var dat = {
        "id":id,
        "mbId":GetQueryString('mbId'),
        "name":$("#mname").val(),
        "major":$('.major-s option:selected').val(),
        "formtype":$('.formtype-s option:selected').val(),
        "content":getContent()
    }
     $.ajax({
       type:"post",
       url:"/assist/biaodan/",
//       cache:false,
       async: false,
//       dataType:"json",
       data:JSON.stringify(dat),
       success: function(data){
           var jdata = JSON.parse(data);
           
//        alert("保存成功");
        document.cookie=biaodantype+"=succ;"+";path=/";
        document.cookie="bdid="+jdata.id+";path=/";
        window.close();
       }
       
       
     });
};

function GetQueryString(name)
{
     var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i"); 
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)return  unescape(r[2]); return null;
}