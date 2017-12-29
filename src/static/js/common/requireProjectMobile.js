require.config({
	waitSeconds: 30,
    paths: {
        'raphael':'/js/morris.js-0.5.1/raphael-min',
        'morris':'/js/morris.js-0.5.1/morris.min',
        'swiper':'/js/swiperjs/swiper.min',
    },
    
    shim : {
    	'morris': '/css/project/morris.css',
        'swiper': '/css/swipercss/swiper.min.css',
        
    }
});
 
require(['raphael','morris'], function() {
    //draw_chart
    loadDraw('week');
			
	$(".proChoose").bind("change", function() { 
		var proid=$(".proChoose").val();
		reload(proid);
	});
	var proid=$(".proChoose").val();
	  reload(proid);
});

require(['swiper',], function() {
    //draw_chart
    initSlide();
});

