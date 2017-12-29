/**
 * msg string 消息内容
 * title string 对话框标题
 * callback function 返回函数。在隐藏并且CSS动画结束后触发
 **/
window.alert = function (msg, title, callback) {
    if (!title) {
        title = '温馨提示';
    }
    var dialogHTML = '<div id="selfAlert" class="modal fade">';
    dialogHTML += '<div class="modal-dialog" style="margin-top: 10%;width: 20%;">';
    dialogHTML += '<div class="modal-content">';
    dialogHTML += '<div class="modal-header">';
    dialogHTML += '<button type="button" class="close" data-dismiss="modal" aria-label="Close">';
    dialogHTML += '<span aria-hidden="true">&times;</span>';
    dialogHTML += '</button>';
    dialogHTML += '<h4 class="modal-title"  style="text-align: center;font-weight: bold;">' + title + '</h4>';
    dialogHTML += '</div>';
    dialogHTML += '<div class="modal-body"  style="text-align: center;">';
    dialogHTML += msg;
    dialogHTML += '</div>';
    dialogHTML += '<div class="modal-footer"  style="text-align: center;">';
    // dialogHTML += '<button type="button" style="margin-right:10%;" class="btn btn-danger" data-dismiss="modal">取消</button>';
    dialogHTML += '<button type="button" class="btn btn-primary" data-dismiss="modal" >确定</button>';
    dialogHTML += '</div>';
    dialogHTML += '</div>';
    dialogHTML += '</div>';
    dialogHTML += '</div>';

    if ($('#selfAlert').length <= 0) {
        $('body').append(dialogHTML);
    }
    $('#selfAlert').on('hidden.bs.modal', function () {
        $('#selfAlert').remove();
        if (typeof callback == 'function'){
          callback();
        }
    }).modal('show');
}

window.alertConfirm = function (msg, title, callback) {
    if (!title) {
        title = '温馨提示';
    }
    var dialogHTML = '<div id="selfConfirmAlert" class="modal fade">';
    dialogHTML += '<div class="modal-dialog" style="margin-top: 10%;width: 20%;">';
    dialogHTML += '<div class="modal-content">';
    dialogHTML += '<div class="modal-header">';
    dialogHTML += '<button type="button" class="close" data-dismiss="modal" aria-label="Close">';
    dialogHTML += '<span aria-hidden="true">&times;</span>';
    dialogHTML += '</button>';
    dialogHTML += '<h4 class="modal-title"  style="text-align: center;font-weight: bold;">' + title + '</h4>';
    dialogHTML += '</div>';
    dialogHTML += '<div class="modal-body"  style="text-align: center;">';
    dialogHTML += msg;
    dialogHTML += '</div>';
    dialogHTML += '<div class="modal-footer"  style="text-align: center;">';
    dialogHTML += '<button type="button" style="margin-right:7.5%;" class="btn btn-danger" data-dismiss="modal">取消</button>';
    dialogHTML += '<button type="button" style="margin-left:7.5%;" class="btn btn-primary" data-dismiss="modal" id="confirm">确定</button>';
    dialogHTML += '</div>';
    dialogHTML += '</div>';
    dialogHTML += '</div>';
    dialogHTML += '</div>';

    if ($('#selfConfirmAlert').length <= 0) {
        $('body').append(dialogHTML);
    }
    $('#selfConfirmAlert').on('hidden.bs.modal', function () {
        $('#selfConfirmAlert').remove();
    }).modal('show');

    $('#confirm').on('click',function(){
      $('#selfConfirmAlert').modal('hide');
      console.log(typeof callback);
      if (typeof callback == 'function'){
          callback();
      }
    });
}

/**
 * format 需要转换的日期格式
 **/
Date.prototype.format = function(format) {
   var date = {
        "M+": this.getMonth() + 1,
        "d+": this.getDate(),
        "h+": this.getHours(),
        "m+": this.getMinutes(),
        "s+": this.getSeconds(),
        "q+": Math.floor((this.getMonth() + 3) / 3),
        "S+": this.getMilliseconds()
   };
   if (/(y+)/i.test(format)) {
        format = format.replace(RegExp.$1, (this.getFullYear() + '').substr(4 - RegExp.$1.length));
   }
   for (var k in date) {
        if (new RegExp("(" + k + ")").test(format)) {
            format = format.replace(RegExp.$1, RegExp.$1.length == 1
                ? date[k] : ("00" + date[k]).substr(("" + date[k]).length));
        }
   }
   return format;
}
$(window).load(function() {
	var barHeight = 80;
	$(window).scroll(function() {
		if($(window).scrollTop() < barHeight) {
			$(".navbar").stop().animate({
				marginTop: 0,
			}, 100);

		} else {
			$(".navbar").stop().animate({
				marginTop: '-90px',
			}, 100);
		}
	});

	//load Project info
	loadProject();

	//customize topnav
	loadNavmenu();

	//show qrcode
	showQrcode();
});

function loadProject() {
	var username = $("#username").attr("class");
	$.ajax({
		type: "get",
		url: "/user/project/",
		cache: false,
		dataType: "json",
		data: {
			"username": username
		},
		success: function(data) {
			if(data.status != "Failed") {
				var optContent = "";
				if(data.current) {
					for(each in data.proList) {
						optContent = optContent + "<option value='" + data.proList[each]["url"] + "'>" + data.proList[each]["name"] + "</option>"
					}
					if(!optContent) {
						optContent = "<option value>未关联项目</option>";
					}
					$(".proselector").html(optContent);
					$(".proselector").val(data.current);
					$('.proselector').change(function() {
						window.location.href = $(".proselector").val();
					})
				} else {
					alert("缺少该项目权限,请联系平台负责人！");
					window.location.href = "/login/";
				}
			}
			return true;
		},
		error: function(data) {
			return false;
		},
		complete: function(data) {}
	});
}

function showQrcode() {
	$('.brand').hover(function() {
			$(".qrcode").show();
		},
		function() {
			$(".qrcode").hide();
		});
}

function addHover() {
	$('.dropdown').hover(function() {
			$(this).addClass('open');
		},
		function() {
			$(this).removeClass('open');
		});

}

function scrollMainTop() {
	document.documentElement.scrollTop = document.body.scrollTop = 0;
}

$(window).resize(function() {
	loadNavmenu();
});

function loadNavmenu() {/*
	if($(".main-nav .nav").width() < 1063) {
		var len = $(".main-nav .nav > li").length - 1;
		console.log(len);
		for(; len > 0; len--) {
			$(".main-nav .nav > li")[len].style.display = "inline-block";
		}
		var num = parseInt((1063 - $(".main-nav .nav").width()) / 95) + 1;
		console.log(num);
		var len = $(".main-nav .nav > li").length;
		for(; num > 0; num--) {
			var idx = len - num;
			console.log(idx);
			$(".main-nav .nav > li")[idx].style.display = "none";
		}
	} else {
		var len = $(".main-nav .nav > li").length - 1;
		for(; len > 0; len--) {
			$(".main-nav .nav > li")[len].style.display = "inline-block";
		}
	}*/
}
