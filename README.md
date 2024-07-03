
# Trivia Trials
#### Video Demo:  <URL "https://www.youtube.com/watch?v=KUnDT_yv-N0">
#### Description:
Trivia Trials is a project born out of my family's shared love for trivia games. It's a completely automated trivia game that uses OpenAI's API, Beautiful Soups web-scrapper, Flask's framework, and a variety of different programming languages. The ultimate goal of this application was to create a game for us to train for bar trivia with. 

This project is made up of five primary pages.

- The Starting Page
- The Game
    - The Classic
    - The Mini 
- The Summary
- The Leaderboard

Additionally, significant backend components allow the app to function correctly.

- The Web-Scrapper
- The Trivia Generator 
- The Database
- The Timing Operators 

### The Starting Page

From the starting page, the user can either sign in, register, start the classic, or start the Mini (the classic is a 15-question trivia game, and the Mini is a 5-question trivia game).

The header (built using HTML and CSS) implements features from Bootstrap 5 and logical statements using Jinja. If the user is signed in, it will allow them to see the games, leaderboard, or logout. If the user is not signed in, the user will see the options to log in or register. 

The Classic start button redirects the user to the classic game.
The Mini start button redirects users to the mini-game. 

Files: The starting page consists of the templates found in the templates folder labeled layout and index, as well as the styling found inside static labeled styles.css, the photos labeled TriviaTrials.png, logFor15.png, and logoFor5.png

### The Game

The game file is the primary driving force behind the operations of this website. 

#### The Classic

The classic is a 15-question game that pulls information from Britannica's this day in history website. The 15 questions are generated using The Trivia Generator.

Every night at midnight, the classic relies on the trivia generator. The trivia generator uses the beautiful soup API to web scrape. The trivia generator will query for today's date and create a formatted string that effectively becomes the URL for today's page of this day in history on Britannica's website. It then uses the request API to get that page and give the HTML information to Beautiful Soup. Beautiful Soup then extracts all that information and develops a text file with all the valuable information that the program needs. Then, the trivia generator uses the open API to query for 20 trivia questions to be returned in a JSON object. Once this JSON file is returned, the classic game can be created.

The classic game will take these first 15 trivia questions in the JSON object and ask them. There is a 15-second timer on each question, which is implemented using JS. If the user answers the question correctly, the scoreboard in the top right corner of the page will be updated, the word correct will appear, the correct answer will flash momentarily in the color green, and the next question will be rendered. If the question is skipped, the question will not increase the scoreboard, the word skipped will flash in red, and the next question will load. If the incorrect answer is given, the word incorrect will flash momentarily in the color red, the next question will load, and the scoreboard will not increase. 

Files: The classic page consists of the templates found in the templates folder labeled classicLoadingPage, classic, question1Classic, as well as the styling found inside static labeled styles.css, and the js files including firstPageClassic, question1Classic, and timerQuestion1Classic.



#### The Mini

The Mini is a 5 question game that pulls information from Britannica's this day in history website. The five questions are generated using The Trivia Generator. 

The mini-game will take the five remaining questions found in the JSON file and develop a much shorter game to play. It operates in the same way as the classic but intends to be a much shorter game and operates with the same timer. 

Files: The mini page consists of the templates found in the templates folder labeled miniLoadingPage, Mini, question1Mini, as well as the styling found inside static labeled styles.css, and the js files including firstPageMini, question1Mini, and timerQuestion1Mini.


#### The Summary 
The summary page is immediately after the Mini and the classic finish. They contain SVG elements that show the user their score as a pie chart and intend to display a quick representation of the user's performance in the game. 

Files: The summary consists of the templates found in the templates folder labeled miniSummary and classicSummary as well as the styling found inside static labeled styles.css, and the js file pichart2 and pichart3 depending on if you are in mini or classic. 



### The Leaderboard 
The leaderboard takes all the player information from the database and sorts it based on the percentage of the questions they got correct. This leaderboard is a table with the top 5 highest-scoring players. There is additionally a pie chart that contains all the individual players' personal information on their performance today. 

Files: The leaderboard consists of the template found in the templates folder labeled leaderboard as well as the styling found inside static labeled styles.css and the js file labeled piechart.
