/**
 * Created by vincentfung13 on 18/02/2016.
 */
var margin = {top: 20, right: 30, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var colour = {
    "Apple": "steelblue",
    "Amazon": "purple",
    "Tesco": "grey",
    "BMW": "black",
    "HSBC": "darkorange",
    "Heineken": "darkgreen"
};

function init_graph() {
    // Get values for the three selectors
    var entity = document.getElementById('entity-picker').value;
    var dimension = document.getElementById('dimension-picker').value;
    var graph_type = document.getElementById('graph-picker').value;

    if (dimension == 'All') {
        $.ajax({
				url : '/twitter_services/stats/' + graph_type + '/' + entity,
				success : function(data) {
					$("#graph-container").html(data);
				}
        });
    }
    else {
        $.ajax({
				url : '/twitter_services/stats_both/' + graph_type + '/' + entity + '/' + dimension,
				success : function(data) {
					$("#graph-container").html(data);
				}
        });
    }
}

/**
 * Draw a line chart regarding the reputation score of an entity
 * @param time_list
 * @param reputation_scores
 */
function draw_line_charts(entity, dimension, time_list, reputation_scores) {
    // Construct data for the axis and lines
    var arrData = [];
    for (var i = 0; i < time_list.length; i++) {
        var time_score_pair = [time_list[i], reputation_scores[i]];
        arrData.push(time_score_pair);
    }

    // Draw the axis
    var xScale = d3.time.scale()
        .domain([new Date(arrData[0][0]), d3.time.day.offset(new Date(arrData[arrData.length - 1][0]), 1)])
        .rangeRound([0, width - margin.left - margin.right]);

    var yScale = d3.scale.linear()
        .domain([
            d3.min(arrData, function (d) {
                return d[1] - 1;
            }),

            d3.max(arrData, function (d) {
                return d[1] + 1;
            })
        ])
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(xScale)
        .orient('bottom')
        .ticks(d3.time.days, 1)
        .tickFormat(d3.time.format('%y-%m-%d'))
        .tickSize(0)
        .tickPadding(8);

    var yAxis = d3.svg.axis()
        .scale(yScale)
        .orient('left')
        .ticks(5)
        .tickSize(5)
        .tickPadding(8);

    // Create the lines
    var score_line = d3.svg.line()
        .x(function(d) {
            return xScale(new Date(d[0]));
        })
        .y(function(d) {
            return yScale(d[1]);
        });

    var base_line = d3.svg.line()
        .x(function(d) {
            return xScale(new Date(d[0]));
        })
        .y(function(d) {
            return yScale(0);
        });

    // Append all the element to the svg
    var lineChartSVG = d3.select("#line-chart")
                        .append("svg")
                        .attr("width", width + margin.left + margin.right)
                        .attr("height", height + margin.top + margin.bottom)
                        .append("g")
                        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    lineChartSVG.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis)
                .selectAll("text")
                    .attr("y", 0)
                    .attr("x", 0)
                    .attr("dy", ".5em")
                    .attr("transform", "rotate(25)")
                    .style("text-anchor", "start")

    lineChartSVG.append("g")
                .attr("class", "y axis")
                .call(yAxis)
                .append("text")
                    .attr("transform", "rotate(-90)")
                    .attr("y", 6)
                    .attr("dy", ".71em")
                    .style("text-anchor", "end")
                    .text("Reputation Score");

    // Append dot to points
    var node = lineChartSVG.selectAll(".g")
                .data(arrData)
                .enter()
                .append("g");

    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (d) {
                return "<span style='color:black'>Click to see tweets in " + d[0] + "</span>";
            }
        );
    lineChartSVG.call(tip);

    node.append("circle")
        .attr("class", "dot")
        .attr("cx", function(d) { return xScale(new Date(d[0])); })
        .attr("cy", function(d) { return yScale(d[1]); })
        .attr("r", 5)
        .attr("fill", colour[entity])
        .on("mouseover", tip.show)
        .on("mouseout", tip.hide)
        .on("click", function(d) {
            if (dimension == 'None') {
                post('/twitter_services/entity/' + entity + '/',
                    {entity: entity, date: d[0]});
            }
            else {
                post('/twitter_services/entity_dimension/' + entity + '/' + dimension + '/',
                    {entity: entity, dimension: dimension, date: d[0]});
            }
            console.log(d);
        });

    node.append("text")
        .attr("transform", function(d) {
            var cx = xScale(new Date(d[0])) + 10;
            var cy = yScale(d[1]);
            return "translate(" + cx + "," + cy + ")"
        })
        .style("fill", colour[entity])
        .style("font-size", "13px")
        .text(function(d) {
            return d[1];
        });

    // Append charts
    lineChartSVG.append("path")
                .datum(arrData)
                .attr("class", "score_line")
                .attr("d", score_line)
                .attr("stroke", colour[entity])

    lineChartSVG.append("path")
                .datum(arrData)
                .attr("class", "base_line")
                .attr("d", base_line)
                .attr("stroke", "red")

    lineChartSVG.append("text")
                .attr("transform", "translate(" + width * 0.77 + "," + yScale(arrData[arrData.length - 1][1]) + ")")
                .attr("dy", ".35em")
                .attr("text-anchor", "start")
                .style("fill", colour[entity])
                .style("font-size", "13px")
                .text(entity);

	lineChartSVG.append("text")
                .attr("transform", "translate(" + width * 0.75 + "," + yScale(0) + ")")
                .attr("dy", ".35em")
                .attr("text-anchor", "start")
                .style("fill", "red")
                .style("font-size", "13px")
                .text("Neutral");
}

/**
 * Draw a stack bar chart representing the tweet count and negative count
 * @param time_list
 * @param tweet_count_list
 * @param negative_count_list
 */
function draw_bar_charts(time_list, tweet_count_list, negative_count_list) {
    // Construct data for the axis and charts
    var arrData = [];
    for (var i = 0; i < time_list.length; i++) {
        var time_score_pair = [time_list[i], negative_count_list[i], tweet_count_list[i] - negative_count_list[i]];
        arrData.push(time_score_pair);
    }

    var barChartSVG = d3.select("#bar-chart")
                        .append("svg")
                        .attr("class", "chart")
                        .attr("width", width + margin.left + margin.right)
                        .attr("height", height + margin.top + margin.bottom)
                        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

   var xScale = d3.time.scale()
        .domain([new Date(arrData[0][0]), d3.time.day.offset(new Date(arrData[arrData.length - 1][0]), 1)])
        .rangeRound([0, width - margin.left - margin.right]);

    var yScale = d3.scale.linear()
        .range([height, 0])
        .domain([
            0,
            d3.max(arrData, function (d) {
                return (d[1] + d[2]) * 1.1;
            })
        ]);

    // Append bottom
    barChartSVG.selectAll("g")
        .data(arrData).enter()
            .append("g")
                .attr("class", "date group")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
            .append("rect")
                .attr("class", "data negative")
                .attr("y", function(d) {
                    return yScale(+d[1]);
                })
                .attr("height", function(d) {
                    return Math.abs(yScale(+d[1]) - yScale(0));
                });

    // Append top
    barChartSVG.selectAll("g")
        .data(arrData)
        .append("rect")
        .attr("class", "data positive")
        .attr("y", function(d) {
            return yScale(+d[1] + +d[2])
        })
        .attr("height", function(d){
            return Math.abs(yScale(+d[2]) - yScale(0));
        });

    barChartSVG.selectAll("g")
        .data(arrData)
        .selectAll("rect.data")
        .attr("x", function(d){
            return xScale(new Date(d[0]));
        })
        .attr("width", 100);

    var xAxis = d3.svg.axis()
        .scale(xScale)
        .orient('bottom')
        .ticks(d3.time.days, 1)
        .tickFormat(d3.time.format('%y-%m-%d'))
        .tickSize(0)
        .tickPadding(8);

    var yAxis = d3.svg.axis()
        .scale(yScale)
        .orient('left')
        .ticks(5)
        .tickSize(5)
        .tickPadding(8);

    barChartSVG.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(" + 2 * margin.right + "," + (height + margin.top) + ")")
                .call(xAxis)
                .selectAll("text")
                    .attr("y", 0)
                    .attr("x", 0)
                    .attr("dy", ".5em")
                    .attr("transform", "rotate(30)")
                    .style("text-anchor", "start")

    barChartSVG.append("g")
                .attr("class", "y axis")
                .attr("transform", "translate(" + margin.right * 1.35 + "," + margin.top + ")")
                .call(yAxis)
                .append("text")
                    .attr("transform", "rotate(-90)")
                    .attr("y", 5)
                    .attr("dy", ".71em")
                    .style("text-anchor", "end")
                    .text("Count");
}