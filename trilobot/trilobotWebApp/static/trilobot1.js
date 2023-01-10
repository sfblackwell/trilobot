function optionsProccess() {
 
    let data = new FormData();
	data.append("paramType" , "options");
	data.append("collectData" , document.getElementById("options").elements.namedItem("collectData").checked);
	data.append("showData", document.getElementById("options").elements.namedItem("showData").checked);
 	data.append("collectGPS" , document.getElementById("options").elements.namedItem("collectGPS").checked);
	data.append("showGPS", document.getElementById("options").elements.namedItem("showGPS").checked);
 	data.append("collectTOF" , document.getElementById("options").elements.namedItem("collectTOF").checked);
	data.append("showTOF", document.getElementById("options").elements.namedItem("showTOF").checked);
 	data.append("collectULT" , document.getElementById("options").elements.namedItem("collectULT").checked);
	data.append("showULT", document.getElementById("options").elements.namedItem("showULT").checked);
 	data.append("collectENV" , document.getElementById("options").elements.namedItem("collectENV").checked);
	data.append("showENV", document.getElementById("options").elements.namedItem("showENV").checked);
 	data.append("collectGRD" , document.getElementById("options").elements.namedItem("collectGRD").checked);
	data.append("showGRD", document.getElementById("options").elements.namedItem("showGRD").checked);
 	
	data.append("collectFrequency" , document.getElementById("options").elements.namedItem("collectFrequency").value);
	data.append("showFrequency", document.getElementById("options").elements.namedItem("showFrequency").value);

    fetch("http://192.168.1.221:5000/trilobotparams", {
        "method": "POST",
        "body": data,
        }).then((message) => { 
            //dummy   
            })       
    }
//	parameters update javascript

function messProccess() {
 
    let data = new FormData();
	data.append("paramType" , "messages");
	data.append("startupMess" , document.getElementById("messages").elements.namedItem("startupMess").value);
	data.append("scrollMess", document.getElementById("messages").elements.namedItem("scrollMess").value);
 	data.append("shutdownMess", document.getElementById("messages").elements.namedItem("shutdownMess").value);

    fetch("http://192.168.1.221:5000/trilobotparams", {
        "method": "POST",
        "body": data,
        }).then((message) => { 
            //dummy   
            })       
    }
	
function miscProccess() {

    let data = new FormData();
	data.append("paramType" , "miscItems");
	data.append("gameController"   , document.getElementById("miscItems").elements.namedItem("gameController").value);
	data.append("stopEnvCollection", document.getElementById("miscItems").elements.namedItem("stopEnvCollection").checked);
	data.append("motorStatic", document.getElementById("miscItems").elements.namedItem("motorStatic").checked);
	data.append("motorButtonBig", document.getElementById("miscItems").elements.namedItem("motorButtonBig").checked);
 
    fetch("http://192.168.1.221:5000/trilobotparams", {
        "method": "POST",
        "body": data,
        }).then((message) => { 

            })       
    }



//	restart javascript

function piRestart(type) {

    let data = new FormData();
    data.append("type" , type);

    if (type == "piShutdownConfirm" || type == "piRebootConfirm") {
        if (type == "piShutdownConfirm") {
            let piShutingdownMess = `Trilobot is shuting down`;
            document.getElementById("piDoingIt").style = "text-align: center; border: 5px double #FF0000; border: 7px double #000000; font-size: 20px; background-color: #FF0000; margin-top: 10px; margin-left: 20px; margin-right: 10px; text-transform: capitalize;";
            document.getElementById("piDoingIt").innerHTML = piShutingdownMess;
            }
        else if (type == "piRebootConfirm") {
            let piRestartingMess = `Trilobot is restarting`;
            document.getElementById("piDoingIt").style = "text-align: center; border: 5px double #FF0000; border: 7px double #000000; font-size: 20px; background-color: #FF0000; margin-top: 10px; margin-left: 20px; margin-right: 10px; text-transform: capitalize;";
            document.getElementById("piDoingIt").innerHTML = piRestartingMess;
            }
    
         fetch("http://192.168.1.221:5000/trilobotrestart", {
            "method": "POST",
            "body": data,
        }).then((message) => { 
            //dummy   
            })       
        }

    else if (type == "shutdown") {
        let piShutdownConfirm = `<button id="piShutdownBtn" class="tblButton" onclick="piRestart('piShutdownConfirm')">Confirm Shutdown</button>`;
        document.getElementById("piDoIt").innerHTML = piShutdownConfirm;

        let piShutdownCancel = `<button id="piShutdownCancelBtn" class="tblButton" onclick="piRestart('picancel')">Cancel Shutdown</button>`;
        document.getElementById("piCancel").innerHTML = piShutdownCancel;
        
        document.getElementById("Shutdown").disabled = true;
        document.getElementById("Shutdown").style.color = "white";
        document.getElementById("Restart").disabled = true;
        document.getElementById("Restart").style.color = "white";
        }    
    
    else if (type == "reboot") {
        let piRebootConfirm = `<button id="piRebootBtn" class="tblButton" onclick="piRestart('piRebootConfirm')">Confirm Reboot</button>`;
        document.getElementById("piDoIt").innerHTML = piRebootConfirm;
        
        let piRebootCancel = `<button id="piRebootCancelBtn" class="tblButton" onclick="piRestart('picancel')">Cancel Reboot</button>`;
        document.getElementById("piCancel").innerHTML = piRebootCancel;
        
        document.getElementById("Shutdown").disabled = true;
        document.getElementById("Shutdown").style.color = "white";
        document.getElementById("Restart").disabled = true;
        document.getElementById("Restart").style.color = "white";
        }
       
    else if (type == "picancel") {

        document.getElementById("piCancel").innerHTML = "";
        document.getElementById("piDoIt").innerHTML = "";
      
        document.getElementById("piDoingIt").innerHTML = "";
        document.getElementById("piDoingIt").style = "";
/* 		
        document.getElementById("piResting").innerHTML = "";
        document.getElementById("piResting").style = ""; */
       
        document.getElementById("Shutdown").disabled = false;
        document.getElementById("Shutdown").style.color = "black";
		
        document.getElementById("Restart").disabled = false;
        document.getElementById("Restart").style.color = "black";
	}

}
