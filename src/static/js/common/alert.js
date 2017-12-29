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
        $('#selfAlert').modal('hide');
        $(".modal-backdrop").remove();
        $("body").removeClass('modal-open');
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
    dialogHTML += '<button type="button" style="margin-right:10%;" class="btn btn-danger" data-dismiss="modal">取消</button>';
    dialogHTML += '<button type="button" style="margin-left:10%;" class="btn btn-primary" data-dismiss="modal" id="confirm">确定</button>';
    dialogHTML += '</div>';
    dialogHTML += '</div>';
    dialogHTML += '</div>';
    dialogHTML += '</div>';

    if ($('#selfConfirmAlert').length <= 0) {
        $('body').append(dialogHTML);
    }
    $('#selfConfirmAlert').on('hidden.bs.modal', function () {
        $('#selfConfirmAlert').remove();
        // $(".modal-backdrop").remove();
        $("body").removeClass('modal-open');
    }).modal('show');

    $('#confirm').on('click',function(){
      $('#selfConfirmAlert').modal('hide');
      // $(".modal-backdrop").remove();
        $("body").removeClass('modal-open');
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


var idTmr,export_tableid,export_name;
function  getExplorer() {
    var explorer = window.navigator.userAgent ;
    if (explorer.indexOf("MSIE") >= 0) {
        return 'ie';
    }else if (explorer.indexOf("Firefox") >= 0) {
        return 'Firefox';
    }else if(explorer.indexOf("Chrome") >= 0){
        return 'Chrome';
    }else if(explorer.indexOf("Opera") >= 0){
        return 'Opera';
    }else if(explorer.indexOf("Safari") >= 0){
        return 'Safari';
    }
}
function export_execl() {
    var tableid = export_tableid;

    if(getExplorer()=='ie')
    {
        var curTbl = document.getElementById(tableid);
        var oXL = new ActiveXObject("Excel.Application");
        var oWB = oXL.Workbooks.Add();
        var xlsheet = oWB.Worksheets(1);
        var sel = document.body.createTextRange();
        sel.moveToElementText(curTbl);
        sel.select();
        sel.execCommand("Copy");
        xlsheet.Paste();
        oXL.Visible = true;
        try {
            var fname = oXL.Application.GetSaveAsFilename("Excel.xlsx", "Excel Spreadsheets (*.xlsx), *.xlsx");
        } catch (e) {
            print("Nested catch caught " + e);
        } finally {
            oWB.SaveAs(fname);
            oWB.Close(savechanges = false);
            oXL.Quit();
            oXL = null;
            idTmr = window.setInterval("Cleanup();", 1);
        }

    }
    else
    {
        tableToExcel(tableid,export_name)
    }
}
function Cleanup() {
    window.clearInterval(idTmr);
    CollectGarbage();
}
var tableToExcel = (function() {
    var uri = 'data:application/vnd.ms-excel;base64,',
            //template = '<html><head><meta charset="UTF-8"><style>td,th{border: 1px solid #ddd;}</style></head><body><table>{table}</table></body></html>',
            template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel"'+
                'xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet>'
                +'<x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets>'
                +'</x:ExcelWorkbook></xml><![endif]-->'+
                ' <style type="text/css">'+
                '.excelTable  {'+
                'border-collapse:collapse;'+
                 ' border:thin solid #999; '+
                '}'+
                '.excelTable  th {'+
                'border: thin solid #999;'+
                'padding:20px;'+
                'text-align: center;'+
                'border-top: thin solid #999;'+
                'background-color: #E6E6E6;'+
                '}'+
                '.excelTable  td{'+
                'border:thin solid #999;'+
                'padding:2px 5px;'+
                'text-align: center;'+
                '}</style>'+
                '</head><body ><table class="excelTable">{table}</table></body></html>',
            base64 = function(s) { return window.btoa(unescape(encodeURIComponent(s))) },
            format = function(s, c) {
                return s.replace(/{(\w+)}/g,
                        function(m, p) { return c[p]; }) }
    return function(table, name) {
        //if (!table.nodeType)
        console.log(table);
        table = document.getElementById(table);
        var ctx = {worksheet:name || 'Worksheet', table: table.innerHTML};
        // window.location.href = uri + base64(format(template, ctx))
        document.getElementById("exportExcel").href = uri + base64(format(template, ctx));
        document.getElementById("exportExcel").download = export_name;
        document.getElementById("exportExcel").click();
    }
})()
