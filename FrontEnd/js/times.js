function showLocale(objD){
	var str,colorhead,colorfoot;
	var yy = objD.getYear();
	if(yy<1900) yy = yy+1900;
	var MM = objD.getMonth()+1;
	if(MM<10) MM = '0' + MM;
	var dd = objD.getDate();
	if(dd<10) dd = '0' + dd;
	var hh = objD.getHours();
	if(hh<10) hh = '0' + hh;
	var mm = objD.getMinutes();
	if(mm<10) mm = '0' + mm;
	var ss = objD.getSeconds();
	if(ss<10) ss = '0' + ss;
	var ww = objD.getDay();
	if  ( ww==0 )  colorhead="<font color=\"#ffffff\">";
	if  ( ww > 0 && ww < 6 )  colorhead="<font color=\"#ffffff\">";
	if  ( ww==6 )  colorhead="<font color=\"#ffffff\">";
	if  (ww==0)  ww="Sunday";
	if  (ww==1)  ww="Monday";
	if  (ww==2)  ww="Tuesday";
	if  (ww==3)  ww="Wednesday";
	if  (ww==4)  ww="Thursday";
	if  (ww==5)  ww="Friday";
	if  (ww==6)  ww="Saturday";
	colorfoot="</font>"
	str = colorhead + +  hh + ":" + mm + ":" + ss + ' &nbsp&nbsp&nbsp'+ ww + "&nbsp&nbsp&nbsp&nbsp" + dd + "/" + MM + "/"  + yy + " "  +  colorfoot;
	return(str);
}

function tick(){
var today;
today = new Date();
document.getElementById("localtime").innerHTML = showLocale(today);
window.setTimeout("tick()", 1000);
}

tick();