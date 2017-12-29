
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

//iput组件
var inputText = {
    template: `
    <Tooltip content="单击编辑" v-if="!edit && usercan" @click.native="focusit()" placement="top-start" class="tooltopbox">
        <span class="m-span m-spancursor" ><slot>{{currentValue}}</slot></span>
    </Tooltip>
    <span class="m-span" v-else-if="!usercan">{{currentValue}}</span>
    <div v-else-if="edit && usercan">
        <i-input  v-model="currentValue" class="inputText_input" ref="focusinput"/>
        <div class="perserveData">
            <div @click="perserve">
                <Button type="text" icon="checkmark-round"></Button>
            </div>
            <div @click="cancel">
                <Button type="text" icon="close-round"></Button>
            </div> 
        </div> 
    </div>
    `,
    data() {
        return {
            edit: false,
            currentValue: null,
            contentlist:{},
        }
    },
    props: ['dataalls', 'type', 'usercan'],
    methods: {
        perserve() {
            var that = this;
            var newurl = this.dataalls.url;
            var test =  newurl.split("user");
            newurl = "/user"+test[1];

            //this.contentlist = JSON.parse(this.dataalls.content);
            if(this.dataalls.content != '') {
                this.contentlist = JSON.parse(this.dataalls.content);
                
            }else {
                this.contentlist = {};
            }
            this.contentlist[that.type] = this.currentValue;
            console.log(this.contentlist);
            this.dataalls.content = JSON.stringify(this.contentlist);
            $.ajax({
                url:newurl,
                type:"PUT",
                data: that.dataalls,
                success:function(response){
                    that.edit = false;
                    console.log(response);
                    that.$emit("newresponselist",that.contentlist,that.type);
                },
                error:function(){

                }
            })
            
        },
        cancel() {

            this.edit = false;
            this.currentValue = this.contentlist[this.type];
        },
        focusit(){
            this.edit=true;
            if(this.dataalls.content != '') {
                this.contentlist = JSON.parse(this.dataalls.content);
                
            }else {
                this.contentlist = {};
            }
            this.$nextTick(function(){
                 this.$refs.focusinput.focus();
            })
           
        }
    },
    watch:{
        dataalls(){
            if(this.dataalls.content != '') {
                this.contentlist = JSON.parse(this.dataalls.content);
                
            }else {
                this.contentlist = {};
            }
            this.currentValue = this.contentlist[this.type];
        },
        usercan(val,old){
            if(val == false) {
                this.cancel();
            }
        }
        
    },
    mounted(){

    }

}

//日期选择组件

var  dataPickers= {
    template: `
    <Tooltip content="单击编辑" v-if="!edit && usercan" @click.native="focusit()" placement="top-start" class="tooltopbox">
        <span class="m-span m-spancursor"><slot>{{currentValue}}</slot></span>
    </Tooltip>
    <span class="m-span" v-else-if="!usercan">{{currentValue}}</span>
    <div v-else-if="edit && usercan">
        <DatePicker v-model="currentValue" type="date" class="inputText_input"></DatePicker>
        <div class="perserveData">
            <div @click="perserve">
                <Button type="text" icon="checkmark-round"></Button>
            </div>
            <div @click="cancel">
                <Button type="text" icon="close-round"></Button>
            </div> 
        </div> 
    </div>
    `,
    data() {
        return {
            edit: false,
            currentValue: null,
            contentlist:{},
        }
    },
    props: ['usercan', 'dataalls', 'type'],
    methods: {
        perserve() {
            var that = this;
            var newurl = this.dataalls.url;
            var test =  newurl.split("user");
            newurl = "/user"+test[1];
            if(this.dataalls.content != '') {
                this.contentlist = JSON.parse(this.dataalls.content);
                
            }else {
                this.contentlist = {};
            }
            // this.contentlist = JSON.parse(this.dataalls.content);
            this.contentlist[this.type] = this.currentValue.format("yyyy-MM-dd");
            this.dataalls.content = JSON.stringify(this.contentlist);
            $.ajax({
                url:newurl,
                type:"PUT",
                data: that.dataalls,
                success:function(response){
                    that.edit = false;
                    that.currentValue = that.contentlist[that.type];
                    that.$emit("newresponselist",that.contentlist,that.type);
                },
                error:function(){

                }
            })
            
        },
        cancel() {
            this.edit = false;
            this.currentValue = this.contentlist[this.type];

        },
        focusit(){
            this.edit=true;
            if(this.dataalls.content != '') {
                this.contentlist = JSON.parse(this.dataalls.content);
                
            }else {
                this.contentlist = {};
            }
        }
    },
    watch:{
        dataalls(){
            if(this.dataalls.content != '') {
                this.contentlist = JSON.parse(this.dataalls.content);
                
            }else {
                this.contentlist = {};
            }
            this.currentValue = this.contentlist[this.type];  
        },
         usercan(val,old){
            if(val == false) {
                this.cancel();
            }
        }
        
    }

}

!function () {
    initVue();

}();



function initVue() {
    
    // Vue.component('inputText',inputText);
    introtable = new Vue({
        el: '#introducetables',
        data(){
            return {
                responselist:null,
                INTRO:{
                },
                PrjName:"PrjName",
                address:"address",
                GCGS:"GCGS",
                XMJL:"XMJL",
                PrjId:"PrjId",
                KGRQ:"KGRQ",
                JGRQ:"JGRQ",
                jsdw:"jsdw",
                jgsjdw:"jgsjdw",
                whsjdw:"whsjdw",
                area:"area",
                dxarea:"dxarea",
                height:"height",
                dscs:"dscs",
                dxcs:"dxcs",
                gczdmj: "gczdmj",
                tctz:"tctz",
                whjglx:"whjglx",
                whzc:"whzc",
                zcxs:"zcxs",
                jkmj:"jkmj",
                zswtsd:"zswtsd",
                pjwtsd:"pjwtsd",
                zjlb:"zjlb",
                zjcd_js:"zjcd_js",
                zsjcz:"zsjcz",
                jglx:"jglx",
                jgzdkd:"jgzdkd",
                zlmb:"zlmb",
                aqmb: "aqmb",
                usercanedit:true
            }
        },
        components: {
            inputText,
            dataPickers
        },
        created() {
            var that = this;
            $.ajax({
                url: "/user/project/?curProject=True",
                type:"GET",
                success:function(response) {
                    that.responselist = response.results[0];
                    if(that.responselist.content == '') {
                        that.INTRO = {};
                    }else {
                        that.INTRO = JSON.parse(that.responselist.content);
                    }
                    console.log(that.responselist);
                   
                }
            })
        },
        methods:{
            newprint(){
                var that = this;
                this.usercanedit = false;

                
                setTimeout(function(){
                    print_excel();
                    that.usercanedit = true;
                },10);
            },
            newexport() {
                var that = this;
                this.usercanedit = false;
                
                setTimeout(function(){
                    export_execl();
                    that.usercanedit = true;
                },10);
            },
            newresponse(a,b){
                this.INTRO = a;
            },
            tback() {

                var that = this;
                that.responselist.content = 1;
                var newurl = that.responselist.url;
                var test =  newurl.split("user");
                newurl = "/user"+test[1];
                $.ajax({
                    url:newurl,
                    type:"PUT",
                    data: that.responselist,
                    success:function(response){
                        console.log(response);
                    },
                    error:function(){

                    }
                })
                }
        }

    })
}

var idTmr;
var export_name = "项目概述";
var export_tableid = "introtable";
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
        tableToExcel(tableid,export_name);
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
                'text-align: left;'+
                'border-top: thin solid #999;'+
                'background-color: #E6E6E6;'+
                '}'+
                '.line_t {'+
                'width:30%;'+
                '}'+
                '.excelTable  td{'+
                'border:thin solid #999;'+
                'padding:2px 5px;'+
                'text-align: left;'+
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

function print_excel() {
            var tableToPrint = document.getElementById('introtable');//将要被打印的表格
            var newWin= window.open("");//新打开一个空窗口
            newWin.document.write(tableToPrint.outerHTML);//将表格添加进新的窗口
            newWin.document.close();//在IE浏览器中使用必须添加这一句
            newWin.focus();//在IE浏览器中使用必须添加这一句
            newWin.print();//打印
            newWin.close();//关闭窗口
}
