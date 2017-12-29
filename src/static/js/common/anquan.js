
var myTimer;
function ExportReport()
{
	$("#exportpgbar").attr("style","width: 0%;");
	$("#exportpgbar").text("");
	
	var xmlhttp;
	if (window.XMLHttpRequest)
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}
	else
	{// code for IE6, IE5
	  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange=function()
	{
	  if (xmlhttp.readyState==4 && xmlhttp.status==200)
	  {
		var result=xmlhttp.responseText;
		if(result=="error")
			alert(result);
		else
		{
			$("#reporturl").attr("href",result);
			myTimer=setInterval(function(){TimerFun()},1000);
			$('#exportdlg').modal('show');
		}
	  }
	}
	xmlhttp.open("GET","/task/exportreport/",true);
	xmlhttp.send();
}

function TimerFun()
{
	var xmlhttp;
	if (window.XMLHttpRequest)
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}
	else
	{// code for IE6, IE5
	  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange=function()
	{
	  if (xmlhttp.readyState==4 && xmlhttp.status==200)
	  {
		 var result=xmlhttp.responseText;
		 var results=result.split(",");
		 if(results[0]=="suc")
		 {
			$("#exportpgbar").attr("style","width: "+results[1]+"%;");
			$("#exportpgbar").text("完成"+results[1]+"%");
			if(results[1]=="100")
			{
				var btn=document.getElementById("btnDownload");
				btn.disabled=false;
				StopTimerFun();
			}	
		 }	
		 else
		 {
			$("#exportpgbar").attr("style","width: 100%;");
			$("#exportpgbar").text("生成报表失败！");
			StopTimerFun();
		 }
	  }
	  else
	  {
		
	  }
	}
	xmlhttp.open("GET","/task/getexportpro/",true);
	xmlhttp.send();
}
	
function StopTimerFun()
{
	window.clearInterval(myTimer);
}

function downloadreport(){
	 var lnk = document.getElementById("reporturl");
	 lnk.click();
	 var btn=document.getElementById("btnDownload");
	 btn.disabled=true;
}



function DialogUploadFile() { 
	//var dlgResult = window.showModalDialog("/task/precastbeam/import/", window, "dialogWidth:480px; dialogHeight:240px; status:0");
	if(window.ActiveXObject)
	{ //IE  
         var dlgResult = window.showModalDialog("/task/precastbeam/import/"+id, window, "dialogWidth:480px; dialogHeight:240px; status:0"); 
	}
	else
	{  //非IE  
        window.open("/task/precastbeam/import/"+id, 'newwindow','width=480,height=240,toolbar=no,menubar=no,scrollbars=no, resizable=no,location=no, status=no');  
	} 
}
