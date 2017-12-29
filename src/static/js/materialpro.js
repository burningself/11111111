				

	
	 function findObj(theObj, theDoc)
    { 
        var p, i, foundObj; 
        if(!theDoc) theDoc = document; 
        if( (p = theObj.indexOf("?")) > 0 && parent.frames.length) 
        {
            theDoc = parent.frames[theObj.substring(p+1)].document;
            theObj = theObj.substring(0,p);
         } 
        if(!(foundObj = theDoc[theObj]) && theDoc.all) 
            foundObj = theDoc.all[theObj];
        for (i=0; !foundObj && i < theDoc.forms.length; i++)     
            foundObj = theDoc.forms[i][theObj]; 
        for(i=0; !foundObj && theDoc.layers && i < theDoc.layers.length; i++)     
            foundObj = findObj(theObj,theDoc.layers[i].document); 
        if(!foundObj && document.getElementById) 
            foundObj = document.getElementById(theObj);   
        return foundObj;
     }
     
        function SmAddSignRow(sm)
		{ 
            var signFrame = findObj("SpecialMaterialItem",document);
			
			 //添加行
			var newTR = signFrame.insertRow(signFrame.rows.length-1);
			newTR.id = sm.sminfo.pk;

			//添加列
			var newNameTD=newTR.insertCell(0);
				
			//添加列内容
			newNameTD.innerHTML = sm.sminfo.fields.number;
			
			//添加列
			var newNameTD1=newTR.insertCell(1);
			
			newNameTD1.innerHTML = "<input type='text' class='form-control' name='"+sm.sminfo.fields.number+"' id='"+sm.sminfo.fields.number+"' value=''>";
			
			//添加列
			var newNameTD2=newTR.insertCell(2);
			newNameTD2.innerHTML = sm.sminfo.fields.unit;

			var newDeleteTD=newTR.insertCell(3);
			newDeleteTD.innerHTML = "<div align='center'><a type='button'  value='del' onclick=\"SmDeleteRow('" + sm.sminfo.pk + "')\"  class='inputStyle' role='button'>取消</i></a></div>";
        }
		
        //删除指定行
        function SmDeleteRow(rowid){
			
			var signFrame = findObj("SpecialMaterialItem",document);
            var signItem = findObj(rowid,document);

            //获取将要删除的行的Index
            var rowIndex = signItem.rowIndex;
			
            //删除指定Index的行
            signFrame.deleteRow(rowIndex);
			
			//删除数据库
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
	
				}
			}
			xmlhttp.open("POST","/task/specialmaterial/del/",true);
			xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
			var param="smid="+rowid;
			xmlhttp.send(param);
			
       }
	   
	   
		function rmAddSignRow(rm)
		{ 
            var signFrame = findObj("reforceMaterialItem",document);
			
			 //添加行
			var newTR = signFrame.insertRow(signFrame.rows.length-1);
			newTR.id = rm.sminfo.pk;

			//添加列
			var newNameTD=newTR.insertCell(0);
				
			//添加列内容
			newNameTD.innerHTML = rm.sminfo.fields.number;
			
			//添加列
			var newNameTD1=newTR.insertCell(1);
			newNameTD1.innerHTML = "<input type='text' class='form-control' name='"+rm.sminfo.fields.number+"' id='"+rm.sminfo.fields.number+"' value=''>";	
			
			//添加列
			var newNameTD2=newTR.insertCell(2);
			newNameTD2.innerHTML = rm.sminfo.fields.unit;

			var newDeleteTD=newTR.insertCell(3);
			newDeleteTD.innerHTML = "<div align='center'><a type='button'  value='del' onclick=\"rmDeleteRow('" + rm.sminfo.pk + "')\"  class='inputStyle' role='button'>取消</i></a></div>";
        }
		
        //删除指定行
        function rmDeleteRow(rowid){
			
			var signFrame = findObj("reforceMaterialItem",document);
            var signItem = findObj(rowid,document);

            //获取将要删除的行的Index
            var rowIndex = signItem.rowIndex;
			
            //删除指定Index的行
            signFrame.deleteRow(rowIndex);
			
			//删除数据库
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
	
				}
			}
			xmlhttp.open("POST","/task/reforcematerial/del/",true);
			xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
			var param="smid="+rowid;
			xmlhttp.send(param);
			
       }
	