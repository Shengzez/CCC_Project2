$(function() {
    var dom = document.getElementById("container2");
    var myChart = echarts.init(dom);
    var app = {};
    option = null;
    option = {
        legend: {
            x : 'center',
            y : 'bottom',
            itemWidth: 12,
            itemHeight: 12,
            textStyle:{//图例文字的样式
                color:'#fff',
                fontSize:16
            },
            data:['Neutral','Positive','Negative']
        },
        calculable : true,
        
        series : [
            {
                name:'面积模式',
                type:'pie',
                radius : [45, 90],
                center : ['50%', '45%'],
                data:[
                    {value:100, name:'Neutral',itemStyle:{normal:{color:'#f3e73af4'}}},
                    {value:200, name:'Positive',itemStyle:{normal:{color:'#98b9f3f4'}}},
                    {value:600, name:'Negative',itemStyle:{normal:{color:'#ed322ceb'}}}
                ]
            }
        ]
    };
    ;
    
    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }
});