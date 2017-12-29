function diff() {
    var chartData = [{
               "time": "2016-1-1",
                   "jihua": 650,
                   "shiji": 121
           }, {
               "time": "2016-2-3",
                   "jihua": 683,
                   "shiji": 146
           }, {
               "time": "2016-3-1",
                   "jihua": 691,
                   "shiji": 138
           }, {
               "time": "2016-4-1",
                   "jihua": 642,
                   "shiji": 127
           }, {
               "time": "2016-5-1",
                   "jihua": 699,
                   "shiji": 105
           }, {
               "time": "2016-6-1",
                   "jihua": 721,
                   "shiji": 109
           }, {
               "time": "2016-7-1",
                   "jihua": 737,
                   "shiji": 112
           }, {
               "time": "2016-8-1",
                   "jihua": 680,
                   "shiji": 101
           }, {
               "time": "2016-9-1",
                   "jihua": 664,
                   "shiji": 97
           }, {
               "time": "2016-10-1",
                   "jihua": 648,
                   "shiji": 93
           }];

           AmCharts.makeChart("chartdiv", {
               type: "serial",
               dataProvider: chartData,
               marginTop: 10,
               categoryField: "time",
               dataDateFormat:"YYYY-MM-DD",
               credits: { enabled: false},
               zoomOutText : "显示全部",
               categoryAxis: {
                   gridAlpha: 0.07,
                   axisColor: "#DADADA",
                   startOnAxis: true,
               },
               valueAxes: [{
                   stackType: "regular",
                   gridAlpha: 0.07,
                   title: "数量"
               }],

               graphs: [{
                   type: "line",
                   title: "实际",
                   valueField: "shiji",
                   fillColors: "rgb(13, 82, 209)",
                   lineAlpha: 0,
                   fillAlphas: 0.6,
                   balloonText: "<span style='font-size:14px; color:#000000;'><b>[[value]]</b></span>"
               }, {
                   type: "line",
                   title: "计划",
                   valueField: "jihua",
                   fillColors: "rgb(13, 142, 207)",
                   lineAlpha: 0,
                   fillAlphas: 0.6,
                   balloonText: "<span style='font-size:14px; color:#000000;'><b>[[value]]</b></span>"
               }],
               legend: {
                   position: "bottom",
                   valueText: "[[value]]",
                   valueWidth: 100,
                   valueAlign: "left",
                   equalWidths: false,
                   periodValueText: "总共: [[value.sum]]"
               },
               chartCursor: {
                   cursorAlpha: 0
               },
               chartScrollbar: {
                   color: "FFFFFF"
               }

           });
};

function addrow(t){
     //得到table对象
     var mytable;
     if(t==0){
         mytable = document.getElementById("cailiaojihua");
     }else{
         mytable = document.getElementById("cailiaoshiji");
     }
   
     //向table中插入一行
     var mytr=mytable.insertRow();
   
     //创建一个新的td对象
     var mytd=document.createElement("td");   
   
     //创建一个新的<input >对象
     var inputtext=document.createElement("input");
   
     //设置input对象的type属性
     inputtext.setAttribute("type","date");
   
     //向td中加入input对象
     mytd.appendChild(inputtext);

     //向tr中加入td对象
     mytr.appendChild(mytd);

     mytd=document.createElement("td");   
   
     //创建一个新的<input >对象
     inputtext=document.createElement("input");
   
     //设置input对象的type属性
     inputtext.setAttribute("type","date");
   
     //向td中加入input对象
     mytd.appendChild(inputtext);

     //向tr中加入td对象
     mytr.appendChild(mytd);

     mytd=document.createElement("td");   
   
     //创建一个新的<input >对象
     inputtext=document.createElement("input");
   
     //设置input对象的type属性
     inputtext.setAttribute("type","number");
   
     //向td中加入input对象
     mytd.appendChild(inputtext);

     //向tr中加入td对象
     mytr.appendChild(mytd);


	 mytd=document.createElement("td");  
	 mytd.setAttribute("style","vertical-align: middle;");
     var tda = document.createElement("a");
     tda.setAttribute("style","cursor: pointer;")
     tda.setAttribute("onclick","deleteRow(this)")
     var tdai = document.createElement("i");
     tdai.setAttribute("class","glyphicon glyphicon-remove");
     tdai.setAttribute("style","top:3px;")
     
     // <a href='#' style='cursor: pointer;'>[<i class='glyphicon glyphicon-remove' style='top:3px;'></i>删除]</a>
     tda.appendChild(tdai)
     mytd.appendChild(tda)
     mytr.appendChild(mytd);
}
  
  
    //删除行
function deleteRow(obj){  
    var tr=obj.parentNode.parentNode;  
    var tb=tr.parentNode;  
    tb.removeChild(tr);  
} 

function xiugaiRow(obj){  
   var tr=obj.parentNode.parentNode;  
   var tds = tr.find("td");
   $("#xgbh").val(tds[0].val());
   $("#xgmc").val(tds[0].val());
   $("#xgcj").val(tds[0].val());
}  