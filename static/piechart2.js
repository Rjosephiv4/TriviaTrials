document.addEventListener('DOMContentLoaded', function() {
    createPieChart("classic", "Today", 1);
    createPieChart("classic", "AllTime", 3);
});

function createPieChart(game, day, chart) {

    async function fetchAndLogUserScores() {
        try {
            var correctOfGame = game + "Score" + day;
            var questionsOfGame = game + "Questions" + day;
            const chartClass = chart === 1 ? ".pie-chart" : `.pie-chart${chart}`;
            
            console.log(correctOfGame);
            console.log(questionsOfGame);

            const response = await fetch("/getUserScores");
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            var dataOfWhole = await response.json();

            function getRadius() {
                if (window.matchMedia("(max-width: 400px)").matches) {
                    return Math.min(window.innerWidth, window.innerHeight) / 5;
                } else if (window.matchMedia("(max-width: 572px)").matches) {
                    return Math.min(window.innerWidth, window.innerHeight) / 5.5;
                } else if (window.matchMedia("(max-width: 800px)").matches) {
                    return Math.min(window.innerWidth, window.innerHeight) / 6.5;
                } else if (window.matchMedia("(max-width: 930px)").matches) {
                    return Math.min(window.innerWidth, window.innerHeight) / 6.5;
                } else {
                    return Math.min(window.innerWidth, window.innerHeight) / 6;
                }
            }

            if (dataOfWhole[questionsOfGame] == 0) {
                var notDone = [
                    {"percentage": 1},
                    {"percentage": 0}
                ];

                var svgWidth = window.innerWidth * 0.45, svgHeight = window.innerHeight * 0.35, radius = getRadius();
                var svg = d3.select(chartClass)
                    .attr("width", svgWidth)
                    .attr("height", svgHeight);

                var g = svg.append("g")
                    .attr("transform", "translate(" + (svgWidth / 2) + "," + (svgHeight / 2) + ")");

                var pie = d3.pie().value(function(d) {
                    return d.percentage;
                }).padAngle(0.00);

                var path = d3.arc()
                    .outerRadius(radius)
                    .innerRadius(radius / 1.2);

                var arc = g.selectAll("arc")
                    .data(pie(notDone))
                    .enter()
                    .append("g")
                    .attr("class", "arc");

                arc.append("path")
                    .attr("d", path)
                    .attr("fill", "gray");

                g.append("text")
                    .attr("text-anchor", "middle")
                    .attr("dy", "0.35em")
                    .style("font-size", "1rem")
                    .style("font-weight", "bold")
                    .style("fill", "white")
                    .text("0/0");
            } else {
                var data = [
                    {"performance": "Correct", "correct": true, "percentage": parseInt(dataOfWhole[correctOfGame], 10)},
                    {"performance": "Incorrect", "correct": false, "percentage": parseInt(dataOfWhole[questionsOfGame], 10) - parseInt(dataOfWhole[correctOfGame], 10)}
                ];

                console.log(`Data for pie chart:${correctOfGame}`, data);

                var svgWidth = window.innerWidth * 0.45, svgHeight = window.innerHeight * 0.35, radius = getRadius();
                var svg = d3.select(chartClass)
                    .attr("width", svgWidth)
                    .attr("height", svgHeight);

                var g = svg.append("g")
                    .attr("transform", "translate(" + (svgWidth / 2) + "," + (svgHeight / 2) + ")");

                var pie = d3.pie().value(function(d) {
                    return d.percentage;
                }).padAngle(dataOfWhole[correctOfGame] == 15 || dataOfWhole[correctOfGame] == 0 ? 0.00 : 0.05);

                var path = d3.arc()
                    .outerRadius(radius)
                    .innerRadius(radius / 1.2);

                var arc = g.selectAll("arc")
                    .data(pie(data))
                    .enter()
                    .append("g")
                    .attr("class", "arc");

                arc.append("path")
                    .attr("d", path)
                    .attr("fill", function(d) {
                        return d.data.correct ? "#0B6623" : "#A91B0D";
                    });

                var innerText = dataOfWhole[correctOfGame] + "/" + dataOfWhole[questionsOfGame];
               
                g.append("text")
                    .attr("text-anchor", "middle")
                    .attr("dy", "0.35em")
                    .style("font-size", "1rem")
                    .style("font-weight", "bold")
                    .style("fill", "white")
                    .text(innerText);

                console.log("Pie chart rendered successfully");
            }
        } catch (error) {
            console.error("There has been a problem with fetch operation:", error);
        }
    }

    fetchAndLogUserScores();
}
