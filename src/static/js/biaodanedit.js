
//ueditor start
var ue;
var _curStep=null;
var _histdval = "";
var readonly = "false";
function initUE(){

    
    ue = UE.getEditor('editor',{
        initialFrameHeight:600,
        autoHeightEnabled: true,
        autoFloatEnabled: true,
                //关闭字数统计  
        wordCount:false,  
        //关闭elementPath  
        elementPathEnabled:false,  
    });
    
    
    ue.addListener("afterSetContent",function(obj){
    	if(readonly!="true"){
    		loadBiaoDanAuth();
    	}
		
	 });
	
	ue.addListener("contentChange",function(obj){
		if(_curStep&&readonly!="true"){
			var focusNode = ue.selection.getStart();	
			if(UE.dom.domUtils.hasClass( focusNode, "setauthclass" ))
			{
					var  classArr = focusNode.className.split(" ");
					if(classArr.length>0){
						var flowstep = classArr[1];
						var step = flowstep.split("_")[1];
						if(_curStep!=step){
							focusNode.innerHTML=_histdval;		
						}
					}
				
			}
			else
			{
			
			}
		}

  });
	
    
}


	function loadBiaoDanAuth(){
		if(_curStep){
			var viewdoc = document.getElementById('ueditor_0').contentWindow.document;
			var tdarr = UE.dom.domUtils.getElementsByTagName(viewdoc,"td");
	
			 for (var i = 0, td; td = tdarr[i++];) {
				if(UE.dom.domUtils.hasClass( td, "setauthclass" ))
				{
					var  classArr = td.className.split(" ");
					if(classArr.length>0){
						var flowstep = classArr[1];
						var step = flowstep.split("_")[1];
						if(_curStep==step){
							UE.dom.domUtils.removeStyle(td, "background-color");
						}else{
							UE.dom.domUtils.setStyle( td, 'background-color', '#F3F0D2' );
							UE.dom.domUtils.on(td,"click",function(evt){
								 //evt为事件对象，this为被点击元素对象
								 _histdval = this.innerHTML;
								 alert("没有权限编辑！");
								 return false;
							 });	
						}

					}
				}
	        }
		}
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
function setContent(isAppendTo,step) {
	step=step||null; 
	_curStep = step;
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
       }
     });
     fanhui();
        
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
        $(tr).remove()
       }
     });
}

function editMb(obj){
    var tr = obj.parentNode.parentNode;
    var tdlist = $(tr).children('td');
    var mbID =$(tdlist[0]).html();
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
	var viewdoc = document.getElementById('ueditor_0').contentWindow.document;
	var tdarr = UE.dom.domUtils.getElementsByTagName(viewdoc,"td");
	for (var i = 0, td; td = tdarr[i++];) {	
		UE.dom.domUtils.removeStyle(td, "background-color");
	}
	
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