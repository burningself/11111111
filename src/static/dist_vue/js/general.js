$(document).ready(function(){
    //model
    loadInitialModel();

    $("#selUnitproject").change(function() {
        var defaultunitId = $("#selUnitproject option:selected").val();
        $.ajax({
            type: "get",
            url: "/task/modelview/setinitialmodel/",
            cache: false,
            //async: false,
            dataType: "json",
            data: { "defaultunitId": defaultunitId, },
            success: function(data) {
                if(data.issuc == "true") {
                    var r = confirm("设置成功！是否重新加载默认单位工程？");
                    if(r == true) {
                        getModelFile2();
                    }

                } else {
                    //alert(data.error);
                    return;
                }

            }
        });
    });

    var anquanChart = echarts.init( document.getElementById("echarts_anquan") );
    var zhiliangChart = echarts.init( document.getElementById("echarts_zhiliang") );

    $(window).resize(function (){
        anquanChart.resize();
        zhiliangChart.resize();
    })


    $.ajax({
        url:"/task/issue/issuecount/",
        dataType : "json",
        type:'post',
        data:{issuetype:"anquan"},
        cache: false,
        timeout:15000, //超时时间
        beforeSend:function( XMLHttpRequest ){
        },
        success:function(data){
            var anquan_sum = 0;
            if( data.issuc == 'true'){
                anquanOption.legend.data = data.majorlist;
                for(var i = 0;i < data.issuelistUnDo.length; i++){
                    anquanOption.series[0].data.push( {name:data.majorlist[i],value:data.issuelistUnDo[i]});
                    anquan_sum += parseInt( data.issuelistUnDo[i] );
                }
                $("#anquan_sum").html( anquan_sum );
                anquanChart.setOption( anquanOption );
            }
        },
        error:function(){
            console.log('读取失败');
        }
    });

    $.ajax({
        url:"/task/issue/issuecount/",
        dataType : "json",
        type:'post',
        data:{issuetype:"zhiliang"},
        cache: false,
        timeout:15000, //超时时间
        beforeSend:function( XMLHttpRequest ){
        },
        success:function(data){
            var sum = 0;
            if( data.issuc == 'true'){
                zhiliangOption.legend.data = data.majorlist;
                for(var j = 0;j < data.majorlist.length;j++){
                    zhiliangOption.series[0].data.push( {name : data.majorlist[j],value: data.issuelistUnDo[j]} );
                    sum += parseInt( data.issuelistUnDo[j] );
                }
                $("#zhiliang_sum").html( sum );
                zhiliangChart.setOption( zhiliangOption );
            }
        },
        error:function(){
            console.log('读取失败');
        }
    });
    var anquanOption = {
        title: {
            text: '安全问题',
            textStyle:{
                fontSize:22
            },
            padding:20,
            top:'left'
        },
        tooltip: {
            trigger: 'item',
            formatter: "{b}:{c}"
        },
        legend: {
            bottom:0,
            data:[],
            selectedMode:false
        },
        series: [
            {
                name:'当前问题',
                type:'pie',
                radius: ['50%', '70%'],
                avoidLabelOverlap: false,
                label: {
                    normal: {
                        show: false,
                        position: 'center',
                    },
                    emphasis: {
                        show: true,
                        textStyle: {
                            fontSize: '25',
                            fontWeight: 'bold',
                            backgroundColor:'#000',
                            padding:20
                        }
                    }
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                data:[]
            }
        ]
    };

    var zhiliangOption = {
        title: {
            text: '质量问题',
            textStyle:{
                fontSize:22
            },
            padding:20,
            top:'left'
        },
        tooltip: {
            trigger: 'item',
            formatter: "{b}: {c}"
        },
        legend: {
            bottom:0,
            data:[],
            selectedMode:false
        },
        series: [
            {
                name:'当前问题',
                type:'pie',
                radius: ['50%', '70%'],
                avoidLabelOverlap: false,
                label: {
                    normal: {
                        show: false,
                        position: 'center',
                    },
                    emphasis: {
                        show: true,
                        textStyle: {
                            fontSize: '25',
                            fontWeight: 'bold',
                            backgroundColor:'#fff',
                            padding:20
                        }
                    }
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                data:[]
            }
        ]
    };

    zhiliangChart.on('mouseover', function(){
        $(".right-model-bottom>p").hide();
             });
    zhiliangChart.on('mouseout', function(){
        $(".right-model-bottom>p").show();
    });
    anquanChart.on('mouseover', function(){
        $(".right-model-top>p").hide();
    });
    anquanChart.on('mouseout', function(){
        $(".right-model-top>p").show();
    });
});
function LoadAllCustomTrees(){
	   $.ajax({
        url:"/task/modelfiles/",
        dataType : "json",
        type:'get',
        data:'',
        timeout:15000, //超时时间
        beforeSend:function( XMLHttpRequest ){
        },
        success:function(data){
            var temp ='';
            if( data.results.length > 0){
                for(var n = 0;n < data.results.length;n++){
                	if(data.results[n].relatedunitprojectid==_curUnitId && data.results[n].relatedmajorid==_curMajor){
                		temp += "<option value="+ data.results[n].id +" selected>"+data.results[n].unitprojectname +"-"+data.results[n].majorname +"</option>";
                	}else{
                		temp += "<option value="+ data.results[n].id +">"+data.results[n].unitprojectname +"-"+data.results[n].majorname +"</option>";
                	}
                    
                }
                $("#selUnitproject").html( temp );
            }
        },
        error:function(){
            console.log('读取失败');
        }
    });

}


