$().ready(function(){
	initSwiper();
	loadTableData(1);
});

function initSwiper(){
	var mySwiper = new Swiper ('.swiper-container-problem' , {
	//	speed:1000,
	    initialSlide: 0,
	    effect : 'coverflow',
	    coverflow: {
	        rotate: 30,
	        stretch: 10,
	        depth: 60,
	        modifier: 2,
	        slideShadows : true
	    },
		onSlideChangeEnd: function(swiper){
	   }
	}) 
	
	var mySwiper = new Swiper ('.swiper-container-topnav', {
		initialSlide: 0,
	    slidesPerView: 'auto',
	    spaceBetween: 0,
	    speed:500,
	    grabCursor: true,
	    freeMode: true,
	}); 
	
}

function loadTableData(filterCode){
	$.ajax({
	  type:"POST",
	  url:"/task/progress/problem/loadTable/",
	  cache:false,
	  dataType:"json",
	  data:{"filterCode":filterCode},
	  success: function(data){
	  	if(data.status==1){
	  		for(mainIndex in data.titles){
	  			$($(".swiper-container-problem .title_row i")[mainIndex]).html(data.titles[mainIndex]);
	  			var tmpStr="";
	  			for(eachHead in data.list_items_head[mainIndex]){
	  				tmpStr+="<th>" + data.list_items_head[mainIndex][eachHead] + "</th>";
	  			}
	  			$($(".swiper-container-problem thead tr")[mainIndex]).html(tmpStr);
	  			
	  			tmpStr="";
	  			for(eachBody in data.list_items[mainIndex] ){
	  				tmpStr+="<tr>";
	  				for(eachProp in data.list_items_head[mainIndex]){
	  					if(eachProp==0){ 
	  						if(filterCode==1){
	  							tmpStr+="<td><a href='/task/progress/problem/" + data.list_items[mainIndex][eachBody].id + "/'>" + data.list_items[mainIndex][eachBody][data.list_items_head[mainIndex][eachProp]] + "<a></td>";
	  						}
	  						else if(filterCode==2){
	  							tmpStr+="<td><a href='/task/progress/issue/edit/?eventId=" + data.list_items[mainIndex][eachBody].id + "'>" + data.list_items[mainIndex][eachBody][data.list_items_head[mainIndex][eachProp]] + "<a></td>";
	  						}
	  						else{
	  							tmpStr+="<td><a href='/task/progress/problem/watch/" + data.list_items[mainIndex][eachBody].id + "/'>" + data.list_items[mainIndex][eachBody][data.list_items_head[mainIndex][eachProp]] + "<a></td>";
	  						}
	  					}
	  					else{
	  						tmpStr+="<td>" + data.list_items[mainIndex][eachBody][data.list_items_head[mainIndex][eachProp]] + "</td>";
	  					}
	  				}
	  				tmpStr+="</tr>";
	  				
	  			}
	  			$($(".swiper-container-problem tbody")[mainIndex]).html(tmpStr);
	  		}
	  	}
	  	else{
	  		alert(data.error);
	  	}
	  }
	})
}

function loadTableDataMore(){}
