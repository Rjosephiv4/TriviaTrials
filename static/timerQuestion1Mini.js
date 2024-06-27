document.addEventListener('DOMContentLoaded', function () {
    async function getScores() {
        try {
            const response = await fetch("/getUserScores");
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            const dataOfWhole = await response.json();

            console.log("Check 1", dataOfWhole["miniQuestionsToday"] );

            async function getQuestions(){
                try{
                    const quizTemp = await fetch("/getTodaysQuestions");
                    if (!response.ok) {
                        throw new Error('Network response was not ok: ' + response.statusText);
                    }
                    const quiz = await quizTemp.json();

                    let timerCheck = true;
                    let inGame = true;
                    let currentQuestion = dataOfWhole["miniQuestionsToday"] + 1;
                    let correctQuestions = dataOfWhole["miniScoreToday"];
                    let isQuestionCorrect = false;
                    let intervalId = null;   

                    console.log("Check 2", currentQuestion);

                    getCurrentStandingsMini(); 
                    pageLoad();

                    function pageLoad() {
                        console.log("PART 2 - Page Loaded");
                        console.log("Starting a new timer");
                        if(inGame)
                            {
                                startNewTimer();
                                setupAnswerClickHandlers();
                                setupFormSubmitHandler();
                            }
                            else
                            {
                                window.location.href = '/';    
                            }
                    }

                    function startNewTimer() {
                        timerCheck = true;
                        let duration = 0.25 * 60;
                        console.log("Starting a new timer with duration:", duration);
                        let display = document.getElementById('timer');
                        startTimer(duration, display);
                        console.log("Check 3", currentQuestion);
                    }

                    function startTimer(duration, display) {
                        let timer = duration, minutes, seconds;
                        console.log("Starting timer with duration:", duration);

                        intervalId = setInterval(function() {
                            if (timerCheck) {
                                minutes = parseInt(timer / 60, 10);
                                seconds = parseInt(timer % 60, 10);

                                minutes = minutes < 10 ? "0" + minutes : minutes;
                                seconds = seconds < 10 ? "0" + seconds : seconds;

                                console.log("Timer updated: ", minutes + ":" + seconds);
                                display.textContent = seconds;
                            } else {
                                clearInterval(intervalId);
                                console.log("Timer stopped");
                            }

                            if (--timer < 0) {
                                clearInterval(intervalId);
                                display.textContent = "TIME'S UP";
                                display.style.color = 'red';
                                display.style.fontSize = '1rem';
                                isQuestionCorrect = false;

                                console.log("Time's up, disabling answers");
                                disableAndStyleAnswers();
                                setTimeout(() => {
                                    console.log("Loading next question");
                                    loadNextQuestion();
                                }, 1000);
                            }
                        }, 1000);
                    }

                    function stopTimer() {
                        console.log("Stopping timer");
                        clearInterval(intervalId);
                        timerCheck = false;
                    }

                    function loadNextQuestion() {
                        const percentClassic = (correctQuestions/currentQuestion).toFixed(2);

                        console.log("Check 4", currentQuestion);

                        const sentQuestions  = {
                            "miniQuestionsToday": currentQuestion, 
                            "miniScoreToday": correctQuestions,
                            "miniPercentToday" : percentClassic, 
                            "isQuestionCorrect": isQuestionCorrect 
                            };
                        fetch('/questionSubmitMini',
                            {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify(sentQuestions)
                        })
                        .catch((error) => {
                            console.error('Error: ', error);
                        });

                        currentQuestion = parseInt(currentQuestion, 10) + 1;

                        console.log("Check 6", currentQuestion);

                        if (currentQuestion <=  5) {
                            console.log(currentQuestion)
                            console.log("Preparing to load next question");
                            resetAnswers();
                            updateDisplayForNextQuestion();
                        } else {
                            console.log("Loading Final Page");
                            stopTimer();
                            loadFinalPage(); 
                        } 
                    }

                    function loadFinalPage() {
                        inGame = false; 
                        currentQuestion = parseInt(currentQuestion, 10) + 1;
                        console.log("Check 7", currentQuestion);
                        window.location.href = '/leaderboardMiniSummary';
                    }

                    function disableAndStyleAnswers() {
                        const answers = document.getElementsByClassName("answers");
                        const submit = document.getElementById('questionSubmit');
                        submit.disabled = true; 
                        for (var i = 0; i < answers.length; i++) {
                            var answer = answers[i];
                            if (answer.getAttribute("value") == "CORRECT") {
                                answer.nextElementSibling.style.color = "green";
                                answer.disabled = true;
                            } else {
                                answer.nextElementSibling.style.color = "red";
                                answer.disabled = true;
                            }
                        }
                    }

                    function resetAnswers() {
                        var answers = document.getElementsByClassName("answers");
                        var submit = document.getElementById('questionSubmit');

                        submit.disabled = false;
                        submit.className = "button-64PostSubmission";
                        for (var i = 0; i < answers.length; i++) {
                            var answer = answers[i];
                            answer.nextElementSibling.style.color = "white";
                            answer.disabled = false;
                            answer.parentElement.className = "answerWrapper button-64";
                            answer.checked = false; 

                        }
                    }


                    function updateDisplayForNextQuestion() {
                        const display = document.getElementById('timer');
                        display.style.color = '#B45300';
                        display.textContent = "Q #" + currentQuestion;

                        const questionsAnsweredHTML = document.getElementById("questionsAnswered");
                        const score = document.getElementById("correctQuestions");
                        
                        score.textContent = correctQuestions; 
                        questionsAnsweredHTML.textContent = currentQuestion - 1;
                        const randomNum = getRandomInt(0, 3);

                        var answer1 = document.getElementsByClassName('answer1')[0];
                        if (randomNum !== 0) {
                            answer1.value = "INCORRECT";
                            answer1.nextElementSibling.textContent = quiz["questions"][currentQuestion - 1 + 15]["incorrect1"];
                        } else {
                            answer1.nextElementSibling.textContent = quiz["questions"][currentQuestion - 1 + 15]["correct"];
                            answer1.value = "CORRECT";
                        }

                        var answer2 = document.getElementsByClassName('answer2')[0];
                        if (randomNum !== 1) {
                            answer2.nextElementSibling.textContent = quiz["questions"][currentQuestion - 1 + 15]["incorrect2"];
                            answer2.value = "INCORRECT";
                        } else {
                            answer2.value = "CORRECT";
                            answer2.nextElementSibling.textContent = quiz["questions"][currentQuestion - 1 + 15]["correct"];
                        }

                        var answer3 = document.getElementsByClassName('answer3')[0];
                        if (randomNum !== 2) {
                            answer3.nextElementSibling.textContent = quiz["questions"][currentQuestion - 1 + 15]["incorrect3"];
                            answer3.value = "INCORRECT";
                        } else {
                            answer3.nextElementSibling.textContent = quiz["questions"][currentQuestion - 1 + 15]["correct"];
                            answer3.value = "CORRECT";
                        }

                        var answer4 = document.getElementsByClassName('answer4')[0];
                        // Determine the correct or incorrect answer for the fourth option
                        if (randomNum !== 3) {
                            let incorrectOption = `incorrect${randomNum + 1}`;
                            answer4.nextElementSibling.textContent = quiz["questions"][currentQuestion - 1 + 15][incorrectOption];
                            answer4.value = "INCORRECT";
                        } else {
                            answer4.nextElementSibling.textContent = quiz["questions"][currentQuestion - 1 + 15]["correct"];
                            answer4.value = "CORRECT";
                        }

                        console.log(randomNum);
                        document.getElementsByClassName('gameQuestion')[0].textContent = quiz["questions"][currentQuestion - 1 + 15]["question"];
                        
                        console.log("Check 7", currentQuestion);
                        if(currentQuestion <= 5)
                            {
                                startNewTimer();
                            }

                        display.style.fontSize = '2rem';
                    }


                    function setupAnswerClickHandlers() {
                        console.log("Setting up answer click handlers");
                        var answerContainers = document.querySelectorAll('[id^=answer]');
                        answerContainers.forEach((container, index) => {
                            container.addEventListener('click', function() {
                                var elements = document.getElementsByClassName('answer' + (index + 1));
                                for (var i = 0; i < elements.length; i++) {
                                    elements[i].click();
                                }
                                console.log("Answer " + (index + 1) + " clicked");
                            });
                        });
                    }

                    function setupFormSubmitHandler() {
                        console.log("Setting up form submit handler");
                        document.querySelector('.questionAnswersForm').addEventListener('submit', function(event) {
                            event.preventDefault();
                            console.log("Form submitted, stopping timer");
                            clearInterval(intervalId);
                            stopTimer();

                            const selectedAnswer = document.querySelector('input[name="question1"]:checked');
                            var display = document.getElementById('timer');
                            var submit = document.getElementById('questionSubmit');

                            if (selectedAnswer) {
                                console.log("Selected answer:", selectedAnswer.value);
                                var answers = document.getElementsByClassName("answers");
                                for (var i = 0; i < answers.length; i++) {
                                    var answer = answers[i];
                                    submit.disabled = true;
                                    submit.className = "button-64PostSubmission";
                                    if (answer.getAttribute("value") == "CORRECT") {
                                        answer.nextElementSibling.style.color = "green";
                                        answer.disabled = true;
                                        answer.parentElement.className = "answerWrapper button-64PostSubmission";
                                        submit.text = correctQuestions;
                                    } else {
                                        answer.nextElementSibling.style.color = "red";
                                        answer.disabled = true;
                                        answer.parentElement.className = "answerWrapper button-64PostSubmission";
                                    }
                                }
                                if (selectedAnswer.value == 'CORRECT') {
                                    correctQuestions++;
                                    isQuestionCorrect = true; 
                                    display.textContent = "CORRECT!";
                                    display.style.color = 'green';
                                    display.style.fontSize = '1rem';
                                } else {
                                    isQuestionCorrect = false; 
                                    display.textContent = "INCORRECT";
                                    display.style.color = 'red';
                                    display.style.fontSize = '1rem';
                                }
                            }
                            else
                            {
                                display.textContent = "Skipped";
                                isQuestionCorrect = false;
                                display.style.color = 'red';
                                display.style.fontSize = '1rem';
                                var answers = document.getElementsByClassName("answers");
                                for (var i = 0; i < answers.length; i++) {
                                    var answer = answers[i];
                                    submit.disabled = true;
                                    submit.className = "button-64PostSubmission";
                                    if (answer.getAttribute("value") == "CORRECT") {
                                        answer.nextElementSibling.style.color = "green";
                                        answer.disabled = true;
                                        answer.parentElement.className = "answerWrapper button-64PostSubmission";
                                        submit.text = correctQuestions;
                                    } else {
                                        answer.nextElementSibling.style.color = "red";
                                        answer.disabled = true;
                                        answer.parentElement.className = "answerWrapper button-64PostSubmission";
                                    }
                                }
                            }

                            setTimeout(() => loadNextQuestion(), 1200);
                        });
                    }

                    function getRandomInt(min, max) {
                        min = Math.ceil(min); 
                        max = Math.floor(max); 
                        return Math.floor(Math.random() * (max - min + 1)) + min; 
                    }

                    function getCurrentStandingsMini() {
                        console.log("Fetching current standings...");
                        fetch("/getUserScores")
                            .then(response => {
                                if (!response.ok) {
                                    console.error('Network response was not ok: ' + response.statusText);
                                    throw new Error('Network response was not ok');
                                }
                                return response.json();
                            })
                            .then(data => {
                                console.log("User scores received:", data);
                                // Process the data here
                            })
                            .catch(error => {
                                console.error('Error fetching user scores:', error);
                            });
                    }
                } catch (error) {
                    console.error('Error:', error);
                }
            }
            getQuestions();
        } catch (error) {
            console.error('Error:', error);
        }
    }
    getScores();
});
