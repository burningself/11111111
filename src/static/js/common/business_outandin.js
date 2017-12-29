
var chart = AmCharts.makeChart("chartdiv", {
    "type": "serial",
     "theme": "light",
    "categoryField": "year",

    "startDuration": 1,
    "categoryAxis": {
        "gridPosition": "start",

    },
    "trendLines": [],
    "graphs": [
        {
            "balloonText": "产值:[[value]]元",
            "fillAlphas": 0.8,
            "id": "AmGraph-1",
            "lineAlpha": 0.2,
            "title": "Income",
            "type": "column",
            "valueField": "income"
        },
        {
            "balloonText": "成本:[[value]]元",
            "fillAlphas": 0.8,
            "id": "AmGraph-2",
            "lineAlpha": 0.2,
            "title": "Expenses",
            "type": "column",
            "valueField": "expenses"
        }
    ],
    "yAxis":{
        "min":0,
         "max":0,
    },
    "guides": [],
    "valueAxes": [
        {
            "id": "ValueAxis-1",
            // "position": "top",
            "axisAlpha": 0
        }
    ],
    "allLabels": [],
    "balloon": {},
    "titles": [],
    "dataProvider": [

        {
            "year": "一月份",
            "income": 23.5,
            "expenses": 18.1
        },
        {
            "year": "二月份",
            "income": 26.2,
            "expenses": 22.8
        },
        {
            "year": "三月份",
            "income": 30.1,
            "expenses": 23.9
        },
        {
            "year": "四月份",
            "income": 29.5,
            "expenses": 25.1
        },
        {
            "year": "五月份",
            "income": 24.6,
            "expenses": 25
        },
        {
            "year": "六月份",
            "income": 24.6,
            "expenses": 25
        },
        {
            "year": "七月份",
            "income": 24.6,
            "expenses": 25
        },
        {
            "year": "八月份",
            "income": 29.6,
            "expenses": 20
        },
        {
            "year": "九月份",
            "income": 24.6,
            "expenses": 25
        },
        {
            "year": "十月份",
            "income": 24.6,
            "expenses": 25
        },
        {
            "year": "十一月份",
            "income": 24.6,
            "expenses": 25
        },
        {
            "year": "十二月份",
            "income": 24.6,
            "expenses": 25
        }

    ],
    "export": {
        "enabled": true
     }

});
jQuery('.chart-input').off().on('input change',function() {
  var property  = jQuery(this).data('property');
  var target    = chart;
  chart.startDuration = 0;

  if ( property == 'topRadius') {
    target = chart.graphs[0];
        if ( this.value == 0 ) {
          this.value = undefined;
        }
  }

  target[property] = this.value;
  chart.validateNow();
});
