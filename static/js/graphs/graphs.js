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
        width = 500 - margin.left - margin.right,
        height = 200 - margin.top - margin.bottom;

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

    var svg = d3.select("body").append("svg")
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