
	function IsPbfolder(pb)
	{	
		if(pb.indexOf("_") > -1){
			return true;
		}
		else{
			return false;
		}
	}
	
	var pbselect=new UserList();
	
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
     
	function IsPbSelect(pb)
		{
			for (var i=0;i<pbselect.size();i++)
			{ 
				if(pbselect.get(i)=== pb){
					 return true;
				}
			}
		   return false;
		}
		
	function IsInPbTree(pbs,pb)
		{
			for (var i=0;i<pbs.length;i++)
			{ 
				if(pbs[i]=== pb){
					PbDeleteRow(pbselect.get(i));
					 return true;
				}
			}
			return false;
		}
		
    function PbAddSignRow(pbs)
		{ 
			var done=true;
			if(pbselect.size()>0)
			{
				while(done)
				{
					var isdel=true;
					for (var i=0;i<pbselect.size();i++)
					{ 
						isdel=true;
						for (var j=0;j<pbs.length;j++)
						{ 
							if(pbs[j]=== pbselect.get(i)){
								isdel=false;
								break;
							}
						}
						
						if(isdel)
						{
							break;
						}
					}
					
					if(isdel)
					{
						PbDeleteRow(pbselect.get(i));
					}
					else
					{
						break;
					}
				}
			}

			
			//for (var i=0;i<pbselect.size();i++)
			//{ 
				//$('#jstree').jstree(true).select_node(pbselect.get(i));
				//$('#jstree').jstree(true).disable_node(pbselect.get(i));
			//}
		
			//读取最后一行的行号，存放在PbTRLastIndex文本框中 
            var PbTRLastIndex = findObj("PbTRLastIndex",document);
            var rowID = parseInt(PbTRLastIndex.value);

            var signFrame = findObj("RelatePbItem",document);
			
			for (var i=0;i<pbs.length;i++)
			{ 
				if(IsPbSelect(pbs[i]) || IsPbfolder(pbs[i]))
				{
					continue;
				}
				pbselect.add(pbs[i]);
				//$('#jstree').jstree(true).disable_node(pbselect.get(i));
				
				 //添加行
				var newTR = signFrame.insertRow(signFrame.rows.length);
				newTR.id = pbs[i];

				//添加列
				var newNameTD=newTR.insertCell(0);
				
				//添加列内容
				newNameTD.innerHTML = pbs[i];

				var newDeleteTD=newTR.insertCell(1);
				newDeleteTD.innerHTML = "<div><a id='txtDel" + rowID + "' type='button'  value='del' onclick=\"PbDeleteRow('" + pbs[i] + "')\"  class='inputStyle' role='button'>取消</i></a></div>";
				newDeleteTD.setAttribute("colspan","1")
				rowID = rowID + 1;

				//将行号推进下一行
				PbTRLastIndex.value = (rowID + 1).toString() ;
			}
			
            $('#PbSelected').val(pbselect.toString());
        }
		
        //删除指定行
    function PbDeleteRow(rowid){
			var signFrame = findObj("RelatePbItem",document);
            var signItem = findObj(rowid,document);

            //获取将要删除的行的Index
            var rowIndex = signItem.rowIndex;

			var pbid=signItem.cells[0].innerHTML;
			$('#jstree').jstree(true).deselect_node(pbid);
			$('#jstree').jstree(true).enable_node(pbid);
			
            //删除指定Index的行
            signFrame.deleteRow(rowIndex);
			
			//从列表删除
			pbselect.remove(pbid);
			
			$('#PbSelected').val(pbselect.toString());
			console.log($('#PbSelected').val());
       }
	   
	    //删除指定行
    function PbDeleteUnSelect(pbs){
			for (var i=0;i<pbs.length;i++)
			{ 
				if(IsPbSelect(pbs[i]) || IsPbfolder(pbs[i]))
				{
					continue;
				}
				$('#jstree').jstree(true).deselect_node(pbs[i]);
            }
			
			for (var i=0;i<pbselect.size();i++)
			{ 
				$('#jstree').jstree(true).select_node(pbselect.get(i));
			}
       }
	   
	function SelectPb(obj){
		$('#update').modal('show');
	}
	
	
	var to = false;
	function searchFunction()
	{
		if(to)
		{ 
		   clearTimeout(to); 
		}
		to = setTimeout(function () 
		{
			var v = $('#search_pb').val();
			$('#jstree').jstree(true).search(v);
		}, 250);
	}