$(function() {
	var dom = document.getElementById("container");
	var myChart = echarts.init(dom);
	var app = {};
	option = null;
	app.title = '';
	
	option = {
	    //tooltip: {
	        //trigger: 'item',
	        //formatter: "{a} <br/>{b}: {c} ({d}%)"
	   // },
	    legend: {
	        orient: 'horizontal',
	        x: 'left',
	        data:['Twitter','Aurin'],
	        itemWidth: 8,
	        itemHeight: 8,
	        textStyle:{//图例文字的样式
	            color:'#fff',
	            fontSize:12
	        }
	    },
	    color:['#37a2da','#ffd85c'],
	    series: [
	        {
	            name:'Twitter',
	            type:'pie',
	            radius: ['50%', '70%'],
	            avoidLabelOverlap: false,
	            label: {
	                normal: {
	                    show: false,
	                    position: 'center'
	                },
	                emphasis: {
	                    show: true,
	                    textStyle: {
	                        fontSize: '24',
	                        color:'#fffff',
	                        fontWeight: 'bold'
	                    }
	                }
	            },
	            labelLine: {
	                normal: {
	                    show: false,
	                }
	            },
	            data:[
	                {value:vm.dtu.on, name:'Twitter'},
                  {name:'Aurin'}
	            ]
	        }
	    ]
	};

	if (option && typeof option === "object") {
	    myChart.setOption(option, false);
	}
});