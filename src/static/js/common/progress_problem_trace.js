	var mySwiper;
	$(document).ready(function() {
		mySwiper = new Swiper('.swiper-container', {
			//	    loop: true,
			initialSlide: 0,
			onSlideChangeEnd: function(swiper) {
				$(".topBtn .active").removeClass("active");

				$($(".topBtn button")[swiper.activeIndex]).addClass("active");
			}
		})

		initDatepicer();

		$("#id_relateid").parent().css("display", "none");
		$("#id_curflowstep").parent().css("display", "none");
		$("#id_relateNum").after("<a id='qrCode'><i class='fa fa-barcode' ></i></a>");
	});



	function initDatepicer() {
		$('#id_deadline').datetimepicker({
			format: 'yyyy-mm-dd',
			language: 'zh-CN',
			todayBtn: 0,
			autoclose: 1,
			todayHighlight: 1,
			startView: 2,
			minView: 2,
			forceParse: 1,
			initialDate: new Date(),
			endDate: new Date(),
		}).on("changeDate", function(dateStr) {
			var ins = new Date();
			var chooseMonth = dateStr.date.getMonth();
			var chooseYear = dateStr.date.getFullYear();
			var curMonth = ins.getMonth();
			var curYear = ins.getFullYear();
		})

	}

	function loadTab(obj, id) {
		$(".topBtn .active").removeClass("active");
		$(obj).addClass("active");
		mySwiper.slideTo(id, 1000, false);
	}