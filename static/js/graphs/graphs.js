/**
 * Created by vincentfung13 on 12/02/2016.
 */
function draw_line_charts(time_list, reputation_scores) {
    var arrData = [];
    for (var i = 0; i < time_list.length; i++) {
        var time_score_pair = [time_list[i], reputation_scores[i]];
        arrData.push(time_score_pair);
        console.log("yo");
    }

    console.log(arrData);

    var margin = {top: 20, right: 20, bottom: 30, left: 50},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var parseDate = d3.time.format("%Y-%m-%d").parse;


    var x = d3.time.scale()
        .range([0, width])

    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var line = d3.svg.line()
        .x(function (d) {
            return x(d.date);
        })
        .y(function (d) {
            return y(d.close);
        });

    var svg = d3.select("#line-chart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var data = arrData.map(function (d) {
        return {
            date: parseDate(d[0]),
            close: d[1]
        };
    });

    console.log(data);

    x.domain(d3.extent(data, function (d) {
        return d.date;
    }));
    y.domain(d3.extent(data, function (d) {
        return d.close;
    }));

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Reputation Score");

    svg.append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", line);
}

function draw_bar_charts(time_list, tweet_count_list) {
    var margin = {top: 20, right: 30, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

    var parseDate = d3.time.format("%Y-%m-%d").parse;

    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var chart = d3.select("#bar-chart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var data = [];
    for (var i = 0; i < time_list.length; i++) {
        var pair = {
            time: time_list[i],
            count: tweet_count_list[i],
        }
        data.push(pair);
    }

    console.log(data);

    x.domain(data.map(function(d) { return d.time; }));
    y.domain([0, d3.max(data, function(d) { return d.count; })]);

    chart.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    chart.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Number of Tweets");

    chart.selectAll(".bar")
        .data(data)
        .enter().append("rect")
          .attr("class", "bar")
          .attr("x", function(d) { return x(d.time); })
          .attr("y", function(d) { return y(d.count); })
          .attr("height", function(d) { return height - y(d.count); })
          .attr("width", x.rangeBand())
          .attr("fill", "green");

    function type(d) {
        d.time = +d.count; // coerce to number
        return d;
    }
}