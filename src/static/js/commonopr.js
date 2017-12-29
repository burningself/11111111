function DialogPbTrace(id) { 
	if(window.ActiveXObject)
	{ //IE  
         var dlgResult = window.showModalDialog("/task/precastbeam/trace/"+id, window, "dialogWidth:480px; dialogHeight:540px; status:0"); 
	}
	else
	{  //非IE  
        window.open("/task/precastbeam/trace/"+id, 'newwindow','width=480,height=540,toolbar=no,menubar=no,scrollbars=no, resizable=no,location=no, status=no');  
	}  
} 

function DialogConcretTrace(id) { 
	if(window.ActiveXObject)
	{ //IE  
         var dlgResult = window.showModalDialog("/task/concretematerial/trace/"+id, window, "dialogWidth:480px; dialogHeight:540px; status:0"); 
	}
	else
	{  //非IE  
        window.open("/task/concretematerial/trace/"+id, 'newwindow','width=480,height=540,toolbar=no,menubar=no,scrollbars=no, resizable=no,location=no, status=no');  
	} 
} 

function DialogReforceTrace(id) { 
	if(window.ActiveXObject)
	{ //IE  
         var dlgResult = window.showModalDialog("/task/reforcematerial/trace/"+id, window, "dialogWidth:480px; dialogHeight:540px; status:0"); 
	}
	else
	{  //非IE  
        window.open("/task/reforcematerial/trace/"+id, 'newwindow','width=480,height=540,toolbar=no,menubar=no,scrollbars=no, resizable=no,location=no, status=no');  
	} 
} 