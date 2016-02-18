/**
 * Created by vincentfung13 on 18/02/2016.
 */
var margin = {top: 20, right: 30, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

function draw_line_charts(time_list, reputation_scores, title) {
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

    lineChartSVG.append("text")
              .attr("class", "title")
              .attr("x", width/2)
              .attr("y", 1)
              .attr("text-anchor", "middle")
              .style("font-size","25px")
              .text(title);

    lineChartSVG.append("g")
                .attr("class", "y axis")
                .call(yAxis)
                .append("text")
                    .attr("transform", "rotate(-90)")
                    .attr("y", 6)
                    .attr("dy", ".71em")
                    .style("text-anchor", "end")
                    .text("Reputation Score");

    lineChartSVG.append("path")
                .datum(arrData)
                .attr("class", "score_line")
                .attr("d", score_line)
                .attr("stroke", "red");

    lineChartSVG.append("path")
                .datum(arrData)
                .attr("class", "base_line")
                .attr("d", base_line)
                .attr("stroke", "red")

    lineChartSVG.append("text")
                .attr("transform", "translate(" + width * 0.75 + "," + yScale(arrData[arrData.length - 1][1]) + ")")
                .attr("dy", ".35em")
                .attr("text-anchor", "start")
                .style("fill", "steelblue")
                .text("Reputation Score");

	lineChartSVG.append("text")
                .attr("transform", "translate(" + width * 0.75 + "," + yScale(0) + ")")
                .attr("dy", ".35em")
                .attr("text-anchor", "start")
                .style("fill", "red")
                .text("Neutral");
}

function draw_bar_charts(time_list, tweet_count_list, negative_percentage_list, title) {
    // Construct data for the axis and charts
    var arrData = [];
    for (var i = 0; i < time_list.length; i++) {
        var time_score_pair = [time_list[i], tweet_count_list[i]];
        arrData.push(time_score_pair);
    }

    // Draw the axis
    var xScale = d3.time.scale()
        .domain([new Date(arrData[0][0]), d3.time.day.offset(new Date(arrData[arrData.length - 1][0]), 1)])
        .rangeRound([0, width - margin.left - margin.right]);

    var yScale = d3.scale.linear()
        .domain([
            0, d3.max(arrData, function (d) {
                return d[1] * 1.1;
            })
        ])
        .range([height - margin.top - margin.bottom, 0]);

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
        .tickPadding(8);

    var barChartSVG = d3.select("#bar-chart")
                        .append("svg")
                        .attr("class", "chart")
                        .attr("width", width + margin.left + margin.right)
                        .attr("height", height + margin.top + margin.bottom)
                        .append("g")
                        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    barChartSVG.append("text")
              .attr("class", "title")
              .attr("x", width/2)
              .attr("y", 1)
              .attr("text-anchor", "middle")
              .style("font-size","25px")
              .text(title);

    barChartSVG.append("g")
                .attr("class", "x axis")
                .attr('transform', 'translate(0, ' + (height - margin.top - margin.bottom) + ')')
                .call(xAxis)
                .selectAll("text")
                    .attr("y", 0)
                    .attr("x", 0)
                    .attr("transform", "rotate(25)")
                    .style("text-anchor", "start")

    barChartSVG.append("g")
                .attr("class", "y axis")
                .call(yAxis)
                .append("text")
                    .attr("transform", "rotate(-90)")
                    .attr("y", 6)
                    .attr("dy", ".71em")
                    .style("text-anchor", "end")
                    .text("Count");

    barChartSVG.selectAll('.chart')
                .data(arrData)
                .enter().append('rect')
                    .attr('class', 'bar')
                    .attr('x', function(d) {
                        return xScale(new Date(d[0]));
                    })
                    .attr('y', function(d) {
                        return height - margin.top - margin.bottom - (height - margin.top - margin.bottom - yScale(d[1]))
                    })
                    .attr('width', 50)
                    .attr('height', function(d) {
                        return height - margin.top - margin.bottom - yScale(d[1])
                    });

}