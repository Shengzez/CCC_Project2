$(function() {
    var dom = document.getElementById("container3");
    var myChart = echarts.init(dom);
    var app = {};
    option = null;

    option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'none'
            },
            formatter: function (params) {
                return params[0].name + ': ' + params[0].value;
            }
        },
        xAxis: {
            data: ['Positive', 'Nagative', 'Neutral'],
            axisTick: {show: false},
            axisLine: {show: false},
            axisLabel: {
                textStyle: {
                    color: '#ffffffff',    
                }
            }
        },
        yAxis: {
            splitLine: {show: false},
            axisTick: {show: false},
            axisLine: {show: false},
            axisLabel: {show: false}
        },
        color: ['#f8ec07', 'ffffffff'],
        series: [{
            name: 'hill',
            type: 'pictorialBar',
            barCategoryGap: '-130%',
            // symbol: 'path://M0,10 L10,10 L5,0 L0,10 z',
            symbol: 'path://M0,10 L10,10 C5.5,10 5.5,5 5,0 C4.5,5 4.5,10 0,10 z',
            itemStyle: {
                normal: {
                    opacity: 0.5
                },
                emphasis: {
                    opacity: 1
                }
            },
            //"这里规定下data"
            data: [100,200,300]
        }]
    };;
    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }
});