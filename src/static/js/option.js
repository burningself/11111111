function slidebar_change(select){
  if(typeof(Storage)!=="undefined")
  {
	if (sessionStorage.getItem(select))
    {
		if(sessionStorage.getItem(select)=="selected")
			sessionStorage.setItem(select, "dselected"); 
		else
			sessionStorage.setItem(select, "selected"); 
    }
	else
    {
		sessionStorage.setItem(select, "selected"); 
    }
  }
}
$(document).ready(function(){
	var storage = window.sessionStorage; 
	for (var i=0, len = storage.length; i  <  len; i++)
	{     
		var key = storage.key(i);  
		var value = storage.getItem(key);  
		if(value=="selected")
		{
			var id="#"+key;
			$(id).collapse("toggle");
		}	
   }
});

function setCookie(name, value) {  
                var Days = 1; 
                var exp = new Date(); 
                exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000); //换成毫秒  
                document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();  
            }  

function getCookie(name) {
	var strCookie = document.cookie;
	var arrCookie = strCookie.split("; ");
	for ( var i = 0; i < arrCookie.length; i++) {
		var arr = arrCookie[i].split("=");
		if (arr[0] == name) {
			return arr[1];
		}
	}
	return "";
}
function delCookie(name) {
	var exp = new Date(); 
	exp.setTime(exp.getTime() - 1); 
	var cval = getCookie(name);
	if (cval != null)
		document.cookie = name + "=" + cval + ";expires="+ exp.toGMTString();
}