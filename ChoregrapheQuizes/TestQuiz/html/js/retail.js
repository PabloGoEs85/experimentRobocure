var questionCount = 0;
var randomNumbers = [];
var correctAns = 0;
var COUPONnumber = 1;
var startTime = "";
// var HAPPYnumber = 1;
// var LOVEnumber = 1;
// var SUNnumber = 1;

var session = new QiSession();

// GO TO HOME FUNCTION -------------------------------------
function goHome(){
	questionCount = 0;
	randomNumbers = [];
	correctAns = 0;
	var d = new Date();
	var n = d.toString();
	document.getElementById("inputTextToSave").value = "NON FINISHED "+ startTime + " " + d;	
	saveTextAsFile();	
	document.getElementById("quiz-view").style.display="block";
	document.getElementById("question-view").style.display="none";
	document.getElementById("feedback-view").style.display="none";
	document.getElementById("info-view").style.display="none";	
	document.getElementById("code-view").style.display="none";
	
}

function noQuiz2(){
	questionCount = 0;
	randomNumbers = [];
	correctAns = 0;
	var d = new Date();
	var n = d.toString();
	document.getElementById("inputTextToSave").value = "NOT STARTED "+ startTime + " " + d;	
	saveTextAsFile();	
	document.getElementById("quiz-view").style.display="block";
	document.getElementById("question-view").style.display="none";
	document.getElementById("feedback-view").style.display="none";
	document.getElementById("info-view").style.display="none";	
	document.getElementById("code-view").style.display="none";
}

function goHomeFinished(){
	questionCount = 0;
	randomNumbers = [];
	correctAns = 0;
	document.getElementById("quiz-view").style.display="block";
	document.getElementById("question-view").style.display="none";
	document.getElementById("feedback-view").style.display="none";
	document.getElementById("info-view").style.display="none";	
	document.getElementById("code-view").style.display="none";
}

//	SAVE RESULTS FUNCTION -----------------------------------
function saveTextAsFile(){
    var textToWrite = document.getElementById("inputTextToSave").value;
	var textFileAsBlob = new Blob([textToWrite], {type:'text/plain'});
	var d = new Date();
	var n = d.toString();	
    var fileNameToSaveAs = n;
    var downloadLink = document.createElement("a");
    downloadLink.download = fileNameToSaveAs;
	downloadLink.innerHTML = "Download File";
	console.log(textToWrite);
    if (window.webkitURL != null)
    {
        // Chrome allows the link to be clicked
        // without actually adding it to the DOM.
        downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
    }
    else
    {
        // Firefox requires the link to be added to the DOM
        // before it can be clicked.
        downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
        downloadLink.onclick = destroyClickedElement;
        downloadLink.style.display = "none";
        document.body.appendChild(downloadLink);
    }

    downloadLink.click();
}

//  GET 10 DIFFERENT RANDOM NUMBERS -------------------------
function getRandomNumbers(){
	while(randomNumbers.length < 3){
    	var randomnumber = Math.ceil(Math.random()*20)
    	if(randomNumbers.indexOf(randomnumber) > -1) continue;
    	randomNumbers[randomNumbers.length] = randomnumber;
	}
	return randomNumbers;
}

// DISPLAYS THE YES/NO QUESTION ----------------------------

// QUIZ REJECTED ------------------------------------------
function noQuiz(){
	document.getElementById("quiz-view").style.display="none";
	document.getElementById("info").innerHTML=my_app.noquiz;	
	document.getElementById("info-view").style.display="block";
}

// STARTS THE QUIZ -----------------------------------------
function startFirstQuestion(){
	randomNumbers = getRandomNumbers();
	document.getElementById("quiz-view").style.display="none";
	document.getElementById("question-view").style.display="block";
	
	var my_question = my_app.questions["q".concat(randomNumbers[questionCount].toString())];
	
	document.getElementById("question").innerHTML=my_question.q;
	document.getElementById("1").innerHTML=my_question.answers.a1;
	document.getElementById("2").innerHTML=my_question.answers.a2;
	document.getElementById("3").innerHTML=my_question.answers.a3;
	document.getElementById("4").innerHTML=my_question.answers.a4;
	document.getElementById("question-pic").src=my_question.img;

	session.service("ALAnimatedSpeech").done(function (tts){
	    tts.say(my_question.q);
	});
}

// ADVANCES IN THE QUESTIONS -------------------------------
function correctQuestion(my_answer){
// CORRECT THE QUESTION
	var my_question = my_app.questions["q".concat(randomNumbers[questionCount].toString())];
	document.getElementById("question-view").style.display="none";
	document.getElementById("feedback-view").style.display="block";
	
	if(my_answer==my_question.correct){
		correctAns+=1;
		document.getElementById("feedback").innerHTML=my_question.good;
	} else {
		document.getElementById("feedback").innerHTML=my_question.bad;
		
	}
		// ADD HERE TO SHOW THE CORRECT/WRONG ASNWER DETAILS (THE PHRASE FROM THE WORD)

}

function nextQuestion(){
// UPDATE QUESTION COUNTER
	questionCount +=1
// IF IT IS LESS THAN 5 QUESTIONS, SHOW THE NEXT ONE, IF NOT SHOW  THE QR PART
	if(questionCount<=2){
		document.getElementById("feedback-view").style.display="none";			
		document.getElementById("question-view").style.display="block";
		
		var my_question = my_app.questions["q".concat(randomNumbers[questionCount].toString())];
		document.getElementById("question").innerHTML=my_question.q;
		document.getElementById("1").innerHTML=my_question.answers.a1;
		document.getElementById("2").innerHTML=my_question.answers.a2;
		document.getElementById("3").innerHTML=my_question.answers.a3;
		document.getElementById("4").innerHTML=my_question.answers.a4;
		document.getElementById("question-pic").src=my_question.img;

		session.service("ALAnimatedSpeech").done(function (tts){
			tts.say(my_question.q);
		});

	
	} else {
		showResults();
	}
}


function showResults(){
	
	document.getElementById("feedback-view").style.display="none";				
	document.getElementById("code-view").style.display="block";
	document.getElementById("correct-ans").innerHTML="You answered correcty " + correctAns.toString() + " out of 10 questions";
	var d = new Date();
	var n = d.toString();
	document.getElementById("inputTextToSave").value = correctAns.toString()+ " " + startTime+ " " + d;
	saveTextAsFile();
}





