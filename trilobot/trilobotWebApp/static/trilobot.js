
fetchUpdate();
setInterval(fetchUpdate, 30000);

function fetchUpdate() {

    fetch("http://192.168.1.221:5000/trilobotdata")

	// Converting received data to JSON
	.then(response => response.json())
	.then(json => {
	
        var li0 = ``;
        var li1 = ``;
        var li2 = ``;
        var li3 = ``;
	
	    json.forEach(user => {
			
			// setup buttons
			
			if (user.motorButtonBig == "checked") {
				document.getElementById("motorAndServo").innerHTML = motorAndServoBig();
				document.getElementById("buttonOrDataGrid").innerHTML = setupButtonBig();
				document.getElementById("buttonOrDataGridRight").innerHTML = gridGridBig();
				}
			else {
				document.getElementById("motorAndServo").innerHTML = motorAndServoSmall();
				document.getElementById("dataGridOrButton").innerHTML = gridGridSmall();
				document.getElementById("buttonOrDataGrid").innerHTML = setupButton();
				}
	    
		
            if (user.collectENV == "checked") {
                style=` style="background-color:#00FF00" `; }
            else  {
                style=` style="background-color:#FF0000" `; } 
      
            li0 += `<tr><th>ENV Data</th><th>`;
            li0 += `<button id="envData" class="tblButton" ` + style + ` value="${user.collectENV}" onclick="collectData(1)">Collect</button>`;
 
            if (user.showENV == "checked") {
               style=` style="background-color:#00FF00" `; }
            else  {
               style=` style="background-color:#FF0000" `; } 
 
            li0 += `<button id="envDataShow" class="tblButton" ` + style + ` value="${user.showENV}" onclick="collectData(5)">Show</button>`;
            li0 += `</th></tr>`;
            
            if (user.collectGPS == "checked") {
                style=` style="background-color:#00FF00" `; }
            else  {
                style=` style="background-color:#FF0000" `; } 

            li1 += `<tr><th>GPS Data</th><th>`;
            li1 += `<button id="gpsData" class="tblButton" ` + style + ` value="${user.collectGPS}" onclick="collectData(2)">Collect</button>`;
 
            if (user.showGPS == "checked") {
               style=` style="background-color:#00FF00" `; }
            else  {
               style=` style="background-color:#FF0000" `; } 
 
            li1 += `<button id="gpsDataShow" class="tblButton" ` + style + ` value="${user.ShowGPS}" onclick="collectData(6)">Show</button>`;
            li1 += `</th></tr>`;
            
            if (user.collectTOF == "checked") {
                style=` style="background-color:#00FF00" `; }
            else  {
                style=` style="background-color:#FF0000" `; }
                
            li2 += `<tr><th>TOF Data</th><th colspan="4">`;
            li2 += `<button id="tofGrid" class="tblButton" ` + style + `  value="${user.collectGRD}" onclick="collectData(3)">Collect</button>`;

            if (user.showTOF == "checked") {
                style=` style="background-color:#00FF00" `; }
            else  {
                style=` style="background-color:#FF0000" `; }

            li2 += `<button id="tofGridShow" class="tblButton" ` + style + ` value="${user.ShowGRD}" onclick="collectData(7)">Show</button>`;
            li2 += `</th></tr>`;
            
            if (user.collectULT == "checked") {
                style=` style="background-color:#00FF00" `; }
            else  {
                style=` style="background-color:#FF0000" `; }
  
            li3 += `<tr><th>ULT Data</th><th>`;
            li3 += `<button id="ultData" class="tblButton" ` + style + ` value="${user.collectULT}" onclick="collectData(4)">Collect</button>`;

            if (user.showULT == "checked") {
                style=` style="background-color:#00FF00" `; }
            else  {
                style=` style="background-color:#FF0000" `; }

            li3 += `<button id="ultDataShow" class="tblButton" ` + style + ` value="${user.ShowULT}" onclick="collectData(8)">Show</button>`;
            li3 += `</th></tr>`;

            // 	create table data grids

			if (user.showENV == "checked") {
                li0 += `<tr><td>Time</td><td>${user.ENVts}</td></tr>
                <tr><td>Temperature</td><td>${user.temperature}</td></tr>
                <tr><td>Pressure</td><td>${user.pressure}</td></tr>
                <tr><td>Humidity</td><td>${user.humidity}</td></tr>`;
                }
            
            if (user.showGPS == "checked") {
                li1 += `<tr><td>Time</td><td>${user.gpsTS}</td></tr>
                <tr><td>Latitude</td><td>${user.latitude}</td></tr>
                <tr><td>Longitude</td><td>${user.longitude}</td></tr>
                <tr><td>Altitude</td><td>${user.altitude}</td></tr>
                <tr><td>Num Sats</td><td>${user.num_sats}</td></tr>
                <tr><td>GPS Quality</td><td>${user.gps_qual}</td></tr>`;
                }	
     
			if (user.showTOF == "checked") {
                li2 += `<tr id="tofTS"><td >Time</td><td colspan="3">${user.tofTS}</td></tr>`;
                li2 += `<tr id="tofTS"><td  colspan="4" align="center">TOF Grid Distances in mm</td></tr>`;
                
                const TOFgrid = [user.p0, user.p1, user.p2, user.p3, user.p4, user.p5, user.p6, user.p7, user.p8, user.p9, user.p10, user.p11, user.p12, user.p13, user.p14, user.p15];
                TOFgrid.sort(function(a, b){return b - a});
     
                var GRDmin = TOFgrid[0];
                var GRDmax = TOFgrid[TOFgrid.length-1];
                
                var txt = ``;
                TOFgrid.forEach(( eleVal, eleIndex) => {
                     if (eleIndex == 0 || eleIndex == 4 || eleIndex == 8 || eleIndex == 12) {
                          txt += `<tr>`;}
                      
                      style = ``
                      if (eleVal == GRDmin) {
                          style=` style="background-color:#00FF00"`; }
                      if (eleVal == GRDmax) {
                          style=` style="background-color:#FF0000"`; }  
                          
                      txt += `<td` + style +`> ` + eleVal.toString() + `</td>`;
                          
                      if (eleIndex == 3 || eleIndex == 7 || eleIndex == 11 || eleIndex == 15) {
                          txt += `</tr>`;}    
                    
                });

                li2 += txt;
                }
            
            if (user.showULT == "checked") {
                li3 += `<tr><td>Time Stamp</td><td>${user.ULTts}</td></tr>
                    <tr><td>Distance</td><td>${user.ULTdistance}</td></tr>`
                }

		});
			
		
		
	// Display result
	document.getElementById("ENVdata").innerHTML = li0;
	document.getElementById("GPSdata").innerHTML = li1;
	document.getElementById("TOFgrid").innerHTML = li2;
	document.getElementById("ULTdata").innerHTML = li3;
});
};


function collectData(grid) {

    if (grid == 1) {        
        var btnName = "envData";
        var btnValue = document.getElementById("envData").value;
        var sGrid = "collectENV";
        }
    else if (grid == 2) {
        var btnName = "gpsData";
        var btnValue = document.getElementById("gpsData").value;
        var sGrid = "collectGPS";
        }
    else if (grid == 3) {
        var btnName = "tofGrid";
        var btnValue = document.getElementById("tofGrid").value;
        var sGrid = "collectTOF";
        }
    else if (grid == 4) {
        var btnName = "ultData";
        var btnValue = document.getElementById("ultData").value;
        var sGrid = "collectULT";
        }       
    else if (grid == 5) {        
        var btnName = "envDataShow";
        var btnValue = document.getElementById("envDataShow").value;
        var sGrid = "showENV";
        }
    else if (grid == 6) {
        var btnName = "gpsDataShow";
        var btnValue = document.getElementById("gpsDataShow").value;
        var sGrid = "showGPS";
        }
    else if (grid == 7) {
        var btnName = "tofGridShow";
        var btnValue = document.getElementById("tofGridShow").value;
        var sGrid = "showTOF";
        }
    else if (grid == 8) {
        var btnName = "ultDataShow";
        var btnValue = document.getElementById("ultDataShow").value;
        var sGrid = "showULT";
        }   
    else {
        var btnName = "Not found";
        var btnValue = "Not found";
        var sGrid = "Not found";
        } 




if (btnValue == "Enabled") { 
    var newBtnValue = ""; 
    var newBtnStyle= "#FF0000";
    }   
else { 
    var newBtnValue = "checked";
    var newBtnStyle= "#00FF00";
    }

let data = new FormData();

data.append("dataCollect" , sGrid);
data.append("dataCollectStatus" , newBtnValue);

//for(let [name, value] of data) {
//  alert(`${name} = ${value}`); // key1 = value1, then key2 = value2
//}

fetch("http://192.168.1.221:5000/trilobotupdatedata", {
    "method": "POST",
    "body": data,
}).then((message) => {

//    alert(newBtnStyle +" - "+ newBtnValue +" - "+ btnName); 

//    if (grid == 1) {
//        document.getElementById("envData").innerHTML = newBtnValue;
        document.getElementById(btnName).value = newBtnValue;
        document.getElementById(btnName).style.background = newBtnStyle;
//    }
//    else if (grid == 2) {
//        document.getElementById("gpsData").innerHTML = newBtnValue;
//        document.getElementById("gpsData").value = newBtnValue;
//        document.getElementById("gpsData").style.background = newBtnStyle;  
//    }
//    else if (grid == 3) {
//        document.getElementById("tofGrid").innerHTML = newBtnValue;
//        document.getElementById("tofGrid").value = newBtnValue;
//        document.getElementById("tofGrid").style = newBtnStyle;
//    }
//    else if (grid == 4) {
//        document.getElementById("ultData").innerHTML = newBtnValue;
//        document.getElementById("ultData").value = newBtnValue;
//        document.getElementById("ultData").style = newBtnStyle;
//    } 
        
      })
}

// motor drive 

function letsDance(btnAction, btnReaction) { 

	//alert(btnAction + " - " + btnReaction);

	motorSpeed = document.getElementById("speedSlider").value;
	
	
	let data = new FormData();
	data.append("btnAction" , btnAction);
	data.append("btnReaction" , btnReaction);
	data.append("motorSpeed" , motorSpeed);
	
	fetch("http://192.168.1.221:5000/trilobotmotor", {
		"method": "POST",
		"body": data,
		})// Converting received data to JSON
	.then(response => response.json())
	.then(json => {
			json.forEach(data => {
				var motorSpeed = data.motorSpeed;
				
				document.getElementById("speedSlider").value = motorSpeed;
				
				if (btnReaction == "ACT_PRESSED" && btnAction != "BTN_STOP") {
					document.getElementById(btnAction).style = "background-color:#FF0000" ;
					}
				else if (btnReaction == "ACT_PRESSED"  && btnAction == "BTN_STOP") {
					document.getElementById(btnAction).style = "background-color:#FF0000" ;
					}
				else {
					document.getElementById(btnAction).style = "background-color:#00FF00" ;
					}
			});

});
};


function motorAndServoSmall() { 

let smallOption = `<!-- Combined motor and servo controls table -->
		
<table class="motTables" >
<thead><tr><th>Speed Control</th><th>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th><th>Motor Control</th></tr></thead>
<tbody><tr><td>

<!-- Speed and Servo table -->

<table>
<tbody>
	<tr>
		<td colspan="3" style="text-align: center;"><input id="speedSlider" class="speedSlider" type="range" min="0" max="100" value="30"></td>
	</tr>
	<tr>
		<td colspan="3">Servo</td>
	</tr>
	<tr>
		<td><button id="BTN_Y" class="motButton" style="background-color:#00FF00" onmouseout="letsDance('BTN_Y', 'ACT_RELEASED')" onclick="letsDance('BTN_Y', 'ACT_PRESSED')" onmouseover="letsDance('BTN_Y', 'ACT_PRESSED')">&#8634</button></td>
		<td><button id="BTN_X" class="motButton" style="background-color:#00FF00" onmouseout="letsDance('BTN_X', 'ACT_RELEASED')" onclick="letsDance('BTN_X', 'ACT_PRESSED')" onmouseover="letsDance('BTN_X', 'ACT_PRESSED')">&#8630</button></td>
		<!-- <td><button id="BTN_B" class="motButton" style="background-color:#00FF00" onmouseout="letsDance('BTN_B', 'ACT_RELEASED')" onclick="letsDance('BTN_B', 'ACT_PRESSED')" onmouseover="letsDance('BTN_B', 'ACT_PRESSED')">&#8654</button></td> -->
		<td><button id="BTN_A" class="motButton" style="background-color:#00FF00" onmouseout="letsDance('BTN_A', 'ACT_RELEASED')" onclick="letsDance('BTN_A', 'ACT_PRESSED')" onmouseover="letsDance('BTN_A', 'ACT_PRESSED')">&#8635</button></td>
	</tr>
</tbody>
</table>
</td>

<td>
</td>

<!-- Motor controls table -->

<td>
<table>
<tbody>
	<tr>
		<td><button id="BTN_TLEFT" class="motButton" style="background-color:#00FF00" onmouseout="letsDance('BTN_TLEFT', 'ACT_RELEASED')" onclick="letsDance('BTN_TLEFT', 'ACT_PRESSED')" onmouseover="letsDance('BTN_TLEFT', 'ACT_PRESSED')">&#8662</button></td>
		<td><button id="BTN_UP" class="motButton" style="background-color:#00FF00" onmouseout="letsDance('BTN_UP', 'ACT_RELEASED')" onclick="letsDance('BTN_UP', 'ACT_PRESSED')" onmouseover="letsDance('BTN_UP', 'ACT_PRESSED')">&#8679</button></td>
		<td><button id="BTN_TRIGHT" class="motButton" style="background-color:#00FF00" onmouseout="letsDance('BTN_TRIGHT', 'ACT_RELEASED')" onclick="letsDance('BTN_TRIGHT', 'ACT_PRESSED')" onmouseover="letsDance('BTN_TRIGHT', 'ACT_PRESSED')">&#8663</button></td>
	</tr>
	<tr>
		<td><button id="BTN_LEFT" class="motButton" style="background-color:#00FF00" onmouseout="letsDance('BTN_LEFT', 'ACT_RELEASED')" onclick="letsDance('BTN_LEFT', 'ACT_PRESSED')" onmouseover="letsDance('BTN_LEFT', 'ACT_PRESSED')">&#8678</button></td>
		<td><button id="BTN_STOP" class="motButtonS" style="background-color:#00FF00" onmouseout="letsDance('BTN_STOP', 'ACT_RELEASED')" onclick="letsDance('BTN_STOP', 'ACT_PRESSED')" onmouseover="letsDance('BTN_STOP', 'ACT_PRESSED')">Stop</button></td>
		<td><button id="BTN_RIGHT" class="motButton" style="background-color:#00FF00" onmouseout="letsDance('BTN_RIGHT', 'ACT_RELEASED')" onclick="letsDance('BTN_RIGHT', 'ACT_PRESSED')" onmouseover="letsDance('BTN_RIGHT', 'ACT_PRESSED')">&#8680</button></td>
	</tr>
	<tr>
		<td><button id="BTN_RLEFT" class="motButton" style="background-color:#00FF00" onmouseout="letsDance('BTN_RLEFT', 'ACT_RELEASED')" onclick="letsDance('BTN_RLEFT', 'ACT_PRESSED')" onmouseover="letsDance('BTN_RLEFT', 'ACT_PRESSED')">&#8665</button></td>
		<td><button id="BTN_DOWN" class="motButton" style="background-color:#00FF00" onmouseout="letsDance('BTN_DOWN', 'ACT_RELEASED')" onclick="letsDance('BTN_DOWN', 'ACT_PRESSED')" onmouseover="letsDance('BTN_DOWN', 'ACT_PRESSED')">&#8659</button></td>
		<td><button id="BTN_RRIGHT" class="motButton" style="background-color:#00FF00" onmouseout="letsDance('BTN_RRIGHT', 'ACT_RELEASED')" onclick="letsDance('BTN_RRIGHT', 'ACT_PRESSED')" onmouseover="letsDance('BTN_RRIGHT', 'ACT_PRESSED')">&#8664</button></td>
	</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>

<!-- End of combined motor and servo controls table -->`

return smallOption;

};

function motorAndServoBig() { 

let bigOption = `<!-- Combined motor and servo controls table -->
		
<table class="motTablesBig" >
<tbody>

<!-- Speed table -->
<tr><td>Speed Control</td></tr>
<tr><td>
<table>
<tbody>
	<tr>
		<td colspan="3" style="text-align: center;"><input id="speedSlider" class="speedSlider" type="range" min="0" max="100" value="30"></td>
	</tr>
</tbody>
</table>
</td></tr>

<!-- Motor controls table -->
<tr><td>Motor Control</td></tr>
<tr><td>
<table>
<tbody>
	<tr>
		<td><button id="BTN_TLEFT" class="motButtonBig" style="background-color:#00FF00" onmouseout="letsDance('BTN_TLEFT', 'ACT_RELEASED')" onclick="letsDance('BTN_TLEFT', 'ACT_PRESSED')" onmouseover="letsDance('BTN_TLEFT', 'ACT_PRESSED')">&#8662</button></td>
		<td><button id="BTN_UP" class="motButtonBig" style="background-color:#00FF00" onmouseout="letsDance('BTN_UP', 'ACT_RELEASED')" onclick="letsDance('BTN_UP', 'ACT_PRESSED')" onmouseover="letsDance('BTN_UP', 'ACT_PRESSED')">&#8679</button></td>
		<td><button id="BTN_TRIGHT" class="motButtonBig" style="background-color:#00FF00" onmouseout="letsDance('BTN_TRIGHT', 'ACT_RELEASED')" onclick="letsDance('BTN_TRIGHT', 'ACT_PRESSED')" onmouseover="letsDance('BTN_TRIGHT', 'ACT_PRESSED')">&#8663</button></td>
	</tr>
	<tr>
		<td><button id="BTN_LEFT" class="motButtonBig" style="background-color:#00FF00" onmouseout="letsDance('BTN_LEFT', 'ACT_RELEASED')" onclick="letsDance('BTN_LEFT', 'ACT_PRESSED')" onmouseover="letsDance('BTN_LEFT', 'ACT_PRESSED')">&#8678</button></td>
		<td><button id="BTN_STOP" class="motButtonSBig" style="background-color:#00FF00" onmouseout="letsDance('BTN_STOP', 'ACT_RELEASED')" onclick="letsDance('BTN_STOP', 'ACT_PRESSED')" onmouseover="letsDance('BTN_STOP', 'ACT_PRESSED')">Stop</button></td>
		<td><button id="BTN_RIGHT" class="motButtonBig" style="background-color:#00FF00" onmouseout="letsDance('BTN_RIGHT', 'ACT_RELEASED')" onclick="letsDance('BTN_RIGHT', 'ACT_PRESSED')" onmouseover="letsDance('BTN_RIGHT', 'ACT_PRESSED')">&#8680</button></td>
	</tr>
	<tr>
		<td><button id="BTN_RLEFT" class="motButtonBig" style="background-color:#00FF00" onmouseout="letsDance('BTN_RLEFT', 'ACT_RELEASED')" onclick="letsDance('BTN_RLEFT', 'ACT_PRESSED')" onmouseover="letsDance('BTN_RLEFT', 'ACT_PRESSED')">&#8665</button></td>
		<td><button id="BTN_DOWN" class="motButtonBig" style="background-color:#00FF00" onmouseout="letsDance('BTN_DOWN', 'ACT_RELEASED')" onclick="letsDance('BTN_DOWN', 'ACT_PRESSED')" onmouseover="letsDance('BTN_DOWN', 'ACT_PRESSED')">&#8659</button></td>
		<td><button id="BTN_RRIGHT" class="motButtonBig" style="background-color:#00FF00" onmouseout="letsDance('BTN_RRIGHT', 'ACT_RELEASED')" onclick="letsDance('BTN_RRIGHT', 'ACT_PRESSED')" onmouseover="letsDance('BTN_RRIGHT', 'ACT_PRESSED')">&#8664</button></td>
	</tr>
</tbody>
</table>
</td></tr>

<!-- Servo table -->
<tr><td>Servo Control</td></tr>
<tr><td>
<table>
<tbody>
	<tr>
		<td><button id="BTN_Y" class="motButtonBig" style="background-color:#00FF00" onmouseout="letsDance('BTN_Y', 'ACT_RELEASED')" onclick="letsDance('BTN_Y', 'ACT_PRESSED')" onmouseover="letsDance('BTN_Y', 'ACT_PRESSED')">&#8634</button></td>
		<td><button id="BTN_X" class="motButtonBig" style="background-color:#00FF00" onmouseout="letsDance('BTN_X', 'ACT_RELEASED')" onclick="letsDance('BTN_X', 'ACT_PRESSED')" onmouseover="letsDance('BTN_X', 'ACT_PRESSED')">&#8630</button></td>
		<!-- <td><button id="BTN_B" class="motButtonBig" style="background-color:#00FF00" onmouseout="letsDance('BTN_B', 'ACT_RELEASED')" onclick="letsDance('BTN_B', 'ACT_PRESSED')" onmouseover="letsDance('BTN_B', 'ACT_PRESSED')">&#8654</button></td> -->
		<td><button id="BTN_A" class="motButtonBig" style="background-color:#00FF00" onmouseout="letsDance('BTN_A', 'ACT_RELEASED')" onclick="letsDance('BTN_A', 'ACT_PRESSED')" onmouseover="letsDance('BTN_A', 'ACT_PRESSED')">&#8635</button></td>
	</tr>
</tbody>
</table>
</td></tr>


</tbody>
</table>

<!-- End of combined motor and servo controls table -->`

return bigOption;

}

function gridGridSmall() { 

	let gridGrid = `<table>
		<tr>
		<td style="vertical-align: top;"><table id="TOFgrid" class="blueTable"></table></td>
		<td style="vertical-align: top;"><table id="GPSdata" class="blueTable"></table></td>
		</tr>
		<tr>
		<td style="vertical-align: top;"><table id="ENVdata" class="blueTable"></table></td>
		<td style="vertical-align: top;"><table id="ULTdata" class="blueTable"></table></td>
		
		</tr>
		<tr>
		<td  colspan="2"><br></td>		
		</tr>
		</table>`;		

return gridGrid;

};

function gridGridBig() { 

	let gridGrid = `<table border="2">
		<tr>
		<td style="vertical-align: top;"><table id="TOFgrid" class="blueTable"></table></td>
		<td style="vertical-align: top;"><table id="GPSdata" class="blueTable"></table></td>
		<td style="vertical-align: top;"><table id="ENVdata" class="blueTable"></table></td>
		<td style="vertical-align: top;"><table id="ULTdata" class="blueTable"></table></td>
		</tr>
		</table>`;		

return gridGrid;

};



function setupButton() { 

let setupButton = `<a class="setupBtn" href="http://192.168.1.221:5000/trilobotsetup" target="_self">Setup Page</a> `;		

return setupButton;

};

function setupButtonBig() { 

let setupButton = `<a class="setupBtnBig" href="http://192.168.1.221:5000/trilobotsetup" target="_self">Setup Page</a> `;		

return setupButton;

};
