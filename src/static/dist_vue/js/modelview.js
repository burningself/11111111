$(document).ready(function() {
    //wgetFit();
    loadInitialModel();

    $('#timerange').daterangepicker({
        ranges: {
            '今天': [moment(), moment()],
            '昨天': [moment().subtract('days', 1), moment().subtract('days', 1)],
            '最近7天': [moment().subtract('days', 6), moment()],
            '最近30天': [moment().subtract('days', 29), moment()],
            '本月': [moment().startOf('month'), moment().endOf('month')],
            '上个月': [moment().subtract('month', 1).startOf('month'), moment().subtract('month', 1).endOf('month')]
        },
        locale: {
            applyLabel: '确定',
            cancelLabel: '取消',
            fromLabel: '起始时间',
            toLabel: '结束时间',
            customRangeLabel: '自定义',
            daysOfWeek: ['日', '一', '二', '三', '四', '五', '六'],
            monthNames: ['一月', '二月', '三月', '四月', '五月', '六月',
                '七月', '八月', '九月', '十月', '十一月', '十二月'
            ],
            firstDay: 1
        },
    });

    $(".accordion-toggle").click(function () {
        if( $(this).find("i").hasClass("pro-font-xiangyou") ){
            $(".accordion-toggle").find("i").removeClass("pro-font-arrow_down").addClass("pro-font-xiangyou");
            $(this).find("i").removeClass("pro-font-xiangyou").addClass("pro-font-arrow_down");
        }else{
            $(".accordion-toggle").find("i").removeClass("pro-font-arrow_down").addClass("pro-font-xiangyou");
        }
    });


  $("#btnPbsearch").click(function() {
  	console.log("你妈嗨！");
  	var pbstatus = $("#pbstatussel").val();
  	var timerange = $("#timerange").val();

  	$.ajax({
  		type: "get",
  		url: "/task/modelview/getpblisttimerange",
  		cache: false,
  		dataType: "json",
  		data: {
  			"pbstatus": pbstatus,
  			"timerange": timerange,
  			"_selElevations": _selElevations,
  			"_selPbtypes": _selPbtypes,
  			"_curUnitId": _curUnitId,
  			"_selZones": _selZones,
  			"_curMajor": _curMajor,
  		},
  		success: function(data) {
  			_viewer.clearThemingColors();


				var dbids=[];

  			for(var each in data.pblist) {
  				var color = getColorByStr(data.pblist[each].color);
  				_viewer.setThemingColor(parseInt(data.pblist[each].lvmdbid), color);
  				setChildThemingColor(parseInt(data.pblist[each].lvmdbid), color);
  				dbids.push(parseInt(data.pblist[each].lvmdbid));
  			}
  			
  			_viewer.isolateById(dbids);

  		}
  	});

  	changepage2PageStatus(1);
  });

  $("#btnRestore").click(function() {
  	console.log("你妈嗨！");
  	_viewer.showAll();
  	getpbstatuslist();
  });

});

$(function() {
    bindResize(document.getElementById('Bottombar1'),"jstree_div");
    bindResize(document.getElementById('Bottombar2'),"jstree_div_pbtype");
    bindResize(document.getElementById('Bottombar3'),"div_status_filter");
    bindResize(document.getElementById('Bottombar4'),"div_pbpro");
    bindResize(document.getElementById('Bottombar5'),"div_pbrelatefile");
    bindResize(document.getElementById('Bottombar6'),"div_pblist");
});


function PrintPbQrcode()
{
    var dwidth=window.screen.width;
    var dheight=window.screen.height;
    if(arguments[0])
    {
        var pbid = arguments[0];
        if(window.ActiveXObject)
        { //IE
            var dlgResult = window.showModalDialog("/task/goujian/qrcode/?pbid="+pbid, window, "dialogWidth:"+dwidth+"px;dialogHeight:"+dheight+"px; status:0");
        }
        else
        {  //非IE
            window.open("/task/goujian/qrcode/?pbid="+pbid, 'newwindow',"width="+dwidth+",height="+dheight+",toolbar=no,menubar=no,scrollbars=no, resizable=no,location=no, status=no");
        }
    }
    else{
        alert("没有选择构件");
    }
}

function PrintGrpQrcode()
{
    var dwidth=window.screen.width;
    var dheight=window.screen.height;
    if(arguments[0])
    {
        var pbid = arguments[0];
        if(window.ActiveXObject)
        { //IE
            var dlgResult = window.showModalDialog("/task/goujian/grpqrcode/?grpnumber="+pbid, window, "dialogWidth:"+dwidth+"px;dialogHeight:"+dheight+"px; status:0");
        }
        else
        {  //非IE
            window.open("/task/goujian/grpqrcode/?grpnumber="+pbid, 'newwindow',"width="+dwidth+",height="+dheight+",toolbar=no,menubar=no,scrollbars=no, resizable=no,location=no, status=no");
        }
    }
    else{
        alert("没有选择构件");
    }
}



function TracePbStatus()
{
    var dwidth=window.screen.width;
    var dheight=window.screen.height;
    if(arguments[0])
    {
        var pbid = arguments[0];
        window.open("/task/goujian/trace/?pbid="+pbid);
    }
    else{
        alert("没有选择构件");
    }
}


function PrintPbQrcode2()
{
    var dwidth=window.screen.width;
    var dheight=window.screen.height;
    if(_selPbtypes.length>0 || _selElevations.length>0)
    {
        if(window.ActiveXObject)
        { //IE
            var dlgResult = window.showModalDialog("/task/goujian/qrcode/?selPbtypes="+_selPbtypes+"&selElevations="+_selElevations, window, "dialogWidth:"+dwidth+"px;dialogHeight:"+dheight+"px; status:0");
        }
        else
        {  //非IE
            window.open("/task/goujian/qrcode/?selPbtypes="+_selPbtypes+"&selElevations="+_selElevations, 'newwindow',"width="+dwidth+",height="+dheight+",toolbar=no,menubar=no,scrollbars=no, resizable=no,location=no, status=no");
        }
    }
    else{
        alert("没有选择构件列表");
    }
}

function changepage2Page(page){
    $("#pbtable tbody").html("");
    $("#pagebar").html("");
    $.ajax({
        type:"get",
        url:"/task/modelview/getpblist",
        cache:false,
        dataType:"json",
        data:{"page": page,"_selPbtypes":_selPbtypes,"_selElevations":_selElevations,"_curUnitId": _curUnitId,"_selZones":_selZones,"_curMajor": _curMajor},
        success: function(data){
            $("#pbtable tbody").html(data.pblist);
            $("#pagebar").html(data.pageinfo);
        }
    });
}


function changepage2PageStatus(page){
    var pbstatus=$("#pbstatussel").val();
    var timerange=$("#timerange").val();

    $.ajax({
        type:"get",
        url:"/task/modelview/getpblist2",
        cache:false,
        dataType:"json",
        data:{"page": page,"selPbtypes":_selPbtypes,"selElevations":_selElevations,"curUnitId": _curUnitId,"pbstatus": pbstatus,"timerange":timerange,"_selZones":_selZones},
        success: function(data){
            if(data.issuc=="true")
            {
                $("#pbtable tbody").html(data.pblist);
                $("#pagebar").html(data.pageinfo);
            }
            else
            {
                alert(data.error);
            }
        }
    });
}


function changefunction(){
    var str="";
    $("input[type='radio'][name='pbcheck']:checked").each(function(){
        str = $(this).val();
        //_viewer.select(parseInt(str));
        if (_viewer.impl.selector) {
            _viewer.impl.selector.setSelection([parseInt(str)]);
            _viewer.utilities.fitToView();
        }
    })
}

function wgetFit(){
    $(".content-row").height($(window).height() -150);
    $(".content-row > div").height($(window).height() -160);
    $(".sideMenuDiv").height($(window).height() -165);
}