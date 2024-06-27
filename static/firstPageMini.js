document.addEventListener('DOMContentLoaded', function() {
    var startButton = document.getElementById("questionSubmit");
    
    startButton.addEventListener('click', function(event){
        event.preventDefault();
        loadSpecificQuestion();
    });
    
    var globalData = {};

    async function fetchUserScores() {
        try {
            const response = await fetch("/getUserScores");
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            const dataOfWhole = await response.json();
            globalData = {
                currentScore: parseInt(dataOfWhole["miniScoreToday"], 10),
                currentQuestion: parseInt(dataOfWhole["miniQuestionsToday"], 10)
            };
            console.log('User Scores:', globalData);
        } catch (error) {
            console.error("There has been a problem with fetch operation:", error);
        }
    }

    async function loadSpecificQuestion() {
        await fetchUserScores();
        if (globalData["currentQuestion"]>= 5)
        {
            window.location.href = '/leaderboardMiniSummary';
        }
        else
        {
            window.location.href = '/miniStart';

        }
    }
});