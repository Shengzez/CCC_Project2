$(function() {
	var dom = document.getElementById("container1");
	var myChart = echarts.init(dom);
	var app = {};
	option = null;
	app.title = '环形图';

	option = {
	    //tooltip: {
	        //trigger: 'item',
	        //formatter: "{a} <br/>{b}: {c} ({d}%)"
	   // },
	    color:['#ffd85c'],
	    series: [
	        {
	            name:'Aurin',
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
	                    show: false
	                }
	            },
	            data:[
	                {value:vm.plc.on, name:'Aurin'},
	            ]
	        }
	    ]
	};

	;
	if (option && typeof option === "object") {
	    myChart.setOption(option, true);
	}
});