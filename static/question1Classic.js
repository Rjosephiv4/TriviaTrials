document.addEventListener('DOMContentLoaded', function () {
    async function getScores() {
        try {
            const response = await fetch("/getUserScores");
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            const dataOfWhole = await response.json();

            let timerCheck = true;
            let inGame = true;
            let currentQuestion = dataOfWhole["classicQuestionsToday"] || 1;
            let correctQuestions = dataOfWhole["classicScoreToday"];
            let isQuestionCorrect = false;
            let intervalId = null;

            getCurrentStandingsClassic();
            pageLoad();

            function pageLoad() {
                console.log("PART 2 - Page Loaded");
                console.log("Starting a new timer");
                if (inGame) {
                    startNewTimer();
                    setupAnswerClickHandlers();
                    setupFormSubmitHandler();
                } else {
                    console.log("SummaryPage");
                }
            }

            function startNewTimer() {
                timerCheck = true;
                const duration = 0.25 * 60;
                console.log("Starting a new timer with duration:", duration);
                const display = document.getElementById('timer');
                startTimer(duration, display);
            }

            function startTimer(duration, display) {
                let timer = duration;
                intervalId = setInterval(() => {
                    if (timerCheck) {
                        const minutes = String(Math.floor(timer / 60)).padStart(2, '0');
                        const seconds = String(timer % 60).padStart(2, '0');
                        display.textContent = seconds;
                        console.log("Timer updated:", `${minutes}:${seconds}`);
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
                        setTimeout(loadNextQuestion, 1000);
                    }
                }, 1000);
            }

            function stopTimer() {
                console.log("Stopping timer");
                clearInterval(intervalId);
                timerCheck = false;
            }

            function loadNextQuestion() {
                const percentClassic = (correctQuestions / currentQuestion).toFixed(2);
                const sentQuestions = {
                    "classicQuestionsToday": currentQuestion,
                    "classicScoreToday": correctQuestions,
                    "classicPercentToday": percentClassic,
                    "isQuestionCorrect": isQuestionCorrect
                };
                fetch('/questionSubmitClassic', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(sentQuestions)
                }).catch(error => console.error('Error:', error));

                currentQuestion += 1;

                if (currentQuestion <= 15) {
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
                window.location.href = '/leaderboardClassicSummary';
            }

            function disableAndStyleAnswers() {
                const answers = document.getElementsByClassName("answers");
                const submit = document.getElementById('questionSubmit');
                submit.disabled = true;
                Array.from(answers).forEach(answer => {
                    answer.disabled = true;
                    answer.nextElementSibling.style.color = answer.value === "CORRECT" ? "green" : "red";
                });
            }

            function resetAnswers() {
                const answers = document.getElementsByClassName("answers");
                const submit = document.getElementById('questionSubmit');
                submit.disabled = false;
                submit.className = "button-64PostSubmission";
                Array.from(answers).forEach(answer => {
                    answer.nextElementSibling.style.color = "white";
                    answer.disabled = false;
                    answer.parentElement.className = "answerWrapper button-64";
                    answer.checked = false;
                });
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
                const questionData = quiz[currentQuestion - 1];

                const answerElements = ['answer1', 'answer2', 'answer3', 'answer4'];
                answerElements.forEach((answerClass, index) => {
                    const answer = document.getElementsByClassName(answerClass)[0];
                    if (randomNum !== index) {
                        const incorrectKey = `incorrect${index + 1}`;
                        answer.value = "INCORRECT";
                        answer.nextElementSibling.textContent = questionData[incorrectKey];
                    } else {
                        answer.value = "CORRECT";
                        answer.nextElementSibling.textContent = questionData.correct;
                    }
                });

                console.log(randomNum);
                document.getElementsByClassName('gameQuestion')[0].textContent = questionData.question;

                if (currentQuestion < 16) {
                    startNewTimer();
                }

                display.style.fontSize = '2rem';
            }

            function setupAnswerClickHandlers() {
                console.log("Setting up answer click handlers");
                const answerContainers = document.querySelectorAll('[id^=answer]');
                answerContainers.forEach((container, index) => {
                    container.addEventListener('click', () => {
                        const elements = document.getElementsByClassName('answer' + (index + 1));
                        Array.from(elements).forEach(element => element.click());
                        console.log(`Answer ${index + 1} clicked`);
                    });
                });
            }

            function setupFormSubmitHandler() {
                console.log("Setting up form submit handler");
                document.querySelector('.questionAnswersForm').addEventListener('submit', function (event) {
                    event.preventDefault();
                    console.log("Form submitted, stopping timer");
                    stopTimer();

                    const selectedAnswer = document.querySelector('input[name="question1"]:checked');
                    const display = document.getElementById('timer');
                    const submit = document.getElementById('questionSubmit');

                    if (selectedAnswer) {
                        console.log("Selected answer:", selectedAnswer.value);
                        const answers = document.getElementsByClassName("answers");
                        Array.from(answers).forEach(answer => {
                            answer.disabled = true;
                            answer.nextElementSibling.style.color = answer.value === "CORRECT" ? "green" : "red";
                            answer.parentElement.className = "answerWrapper button-64PostSubmission";
                        });
                        submit.disabled = true;
                        submit.className = "button-64PostSubmission";

                        if (selectedAnswer.value === 'CORRECT') {
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
                    } else {
                        display.textContent = "Skipped";
                        isQuestionCorrect = false;
                        display.style.color = 'red';
                        display.style.fontSize = '1rem';
                        disableAndStyleAnswers();
                    }

                    setTimeout(loadNextQuestion, 1200);
                });
            }

            function getRandomInt(min, max) {
                return Math.floor(Math.random() * (max - min + 1)) + min;
            }

            function getCurrentStandingsClassic() {
                console.log("Fetching current standings...");
                fetch("/getUserScores")
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok: ' + response.statusText);
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log("User scores received:", data);
                    })
                    .catch(error => console.error('Error fetching user scores:', error));
            }

            const quiz = [
                {
                    question: "In what year was Michelangelo's statue of David installed in Florence?",
                    correct: "1504",
                    incorrect1: "1501",
                    incorrect2: "1512",
                    incorrect3: "1498"
                },
                {
                    question: "Which artist created the statue of David?",
                    correct: "Michelangelo",
                    incorrect1: "Leonardo da Vinci",
                    incorrect2: "Raphael",
                    incorrect3: "Donatello"
                },
                {
                    question: "What Renaissance ideal does Michelangelo's David embody?",
                    correct: "Perfect humanity",
                    incorrect1: "Divine beauty",
                    incorrect2: "Military strength",
                    incorrect3: "Artistic innovation"
                },
                {
                    question: "Where was Frank Lloyd Wright born?",
                    correct: "Richland Center, Wisconsin",
                    incorrect1: "Chicago, Illinois",
                    incorrect2: "New York, New York",
                    incorrect3: "Phoenix, Arizona"
                },
                {
                    question: "When did Frank Lloyd Wright die?",
                    correct: "April 9, 1959",
                    incorrect1: "June 8, 1967",
                    incorrect2: "December 5, 1955",
                    incorrect3: "July 4, 1965"
                },
                {
                    question: "How old was Anthony Bourdain when he died?",
                    correct: "61",
                    incorrect1: "55",
                    incorrect2: "59",
                    incorrect3: "63"
                },
                {
                    question: "What was the aim of the first World Oceans Day hosted by the United Nations?",
                    correct: "To raise awareness of the threats to oceans and marine ecosystems",
                    incorrect1: "To promote marine tourism",
                    incorrect2: "To celebrate ocean sports",
                    incorrect3: "To encourage ocean fishing"
                },
                {
                    question: "Who did Serena Williams defeat to win her first French Open title?",
                    correct: "Venus Williams",
                    incorrect1: "Maria Sharapova",
                    incorrect2: "Victoria Azarenka",
                    incorrect3: "Simona Halep"
                },
                {
                    question: "When was Kanye West born?",
                    correct: "June 8",
                    incorrect1: "July 4",
                    incorrect2: "May 20",
                    incorrect3: "August 14"
                },
                {
                    question: "When did the NFL and AFL merger become effective?",
                    correct: "1970",
                    incorrect1: "1965",
                    incorrect2: "1968",
                    incorrect3: "1972"
                },
                {
                    question: "Who is credited as the inventor of the World Wide Web?",
                    correct: "Tim Berners-Lee",
                    incorrect1: "Bill Gates",
                    incorrect2: "Steve Jobs",
                    incorrect3: "Larry Page"
                },
                {
                    question: "Which British author wrote the dystopian classic 'Nineteen Eighty-four'?",
                    correct: "George Orwell",
                    incorrect1: "Aldous Huxley",
                    incorrect2: "Ray Bradbury",
                    incorrect3: "Philip K. Dick"
                },
                {
                    question: "Who received the 1962 Nobel Prize for the determination of the molecular structure of DNA?",
                    correct: "Francis Crick, James Watson, and Maurice Wilkins",
                    incorrect1: "Linus Pauling",
                    incorrect2: "Rosalind Franklin",
                    incorrect3: "Max Perutz"
                },
                {
                    question: "Who was crowned king of Hungary during the Third Crusade?",
                    correct: "Franz Joseph",
                    incorrect1: "Richard I",
                    incorrect2: "Louis VII",
                    incorrect3: "Frederick I"
                },
                {
                    question: "Where did Muhammad, the founder of Islam, die?",
                    correct: "Medina",
                    incorrect1: "Mecca",
                    incorrect2: "Jerusalem",
                    incorrect3: "Baghdad"
                }
            ];
            
        } catch (error) {
            console.error('Error:', error);
        }
    }
    getScores();
});
