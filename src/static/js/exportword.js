
var myExportTimer;
function ExportWordReport()
{
	$("#exportpgbar").attr("style","width: 0%;");
	$("#exportpgbar").text("");
	var btn=document.getElementById("btnExportWord");
	 btn.disabled=true;
	
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
		{
			alert(result);
			var btn=document.getElementById("btnExportWord");
			btn.disabled=false;
		}
		else
		{
			$("#reporturl").attr("href",result);
			myExportTimer=setInterval(function(){TimerFun()},1000);
			//$('#exportworddlg').modal('show');
		}
	  }
	}
	//var reportdate = $('#reportdate').val();
	//xmlhttp.open("GET","/task/exportwordreport/?reportdate="+reportdate,true);
	//xmlhttp.send();
	
	xmlhttp.open("POST","/task/exportwordreport/",false);
	xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	var reportdate = $('#reportdate').val();
	var param="reportdate="+reportdate;
	xmlhttp.send(param);
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
				var btn=document.getElementById("btnExportWord");
				btn.disabled=false;
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
			var btn=document.getElementById("btnExportWord");
			btn.disabled=false;
		 }
	  }
	  else
	  {
		
	  }
	}
	xmlhttp.open("GET","/task/getwordexportpro/",true);
	xmlhttp.send();
}
	
function StopTimerFun()
{
	window.clearInterval(myExportTimer);
}

function downloadreport(){
	 var lnk = document.getElementById("reporturl");
	 lnk.click();
	 var btn=document.getElementById("btnDownload");
	 btn.disabled=true;
}
