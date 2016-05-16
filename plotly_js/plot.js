var reader = new XMLHttpRequest() || new ActiveXObject('MSXML2.XMLHTTP');

function read_left_data(){
    reader.open('get', "./left_data.csv", true);
    reader.onreadystatechange = readLeftData;
    reader.send(null);
}
function readLeftData(){
    if(reader.readyState==4) {
        var allText = reader.responseText;
        var allTextLines = allText.split(/\r\n|\n/);
        var headers = allTextLines[0].split(',');
        var lines = [];

        for (var i=1; i<allTextLines.length; i++) {
            var data = allTextLines[i].split(',');
            if (data.length == headers.length) {
                lines.push(data);
            }
        }

        hop_avg = [];
        hop_stdev = [];
        trace_time = [];
        hop_wrst = [];
        hop_loss = [];
        hop_best = [];

        for (var j = 0; j<lines.length; j++){
            hop_avg.push(lines[j][0]);
            hop_stdev.push(lines[j][2]);
            trace_time.push(lines[j][3].split("+")[0]);
            hop_wrst.push(lines[j][4]);
            hop_loss.push(lines[j][5]);
            hop_best.push(lines[j][6]);
        }

        build_left(hop_avg,hop_stdev,trace_time,hop_wrst,hop_loss,hop_best);

    }
}
function build_left(hop_avg,hop_stdev,trace_time,hop_wrst,hop_loss,hop_best){
    var trace_avg = {
        x: trace_time,
        y: hop_avg,
        mode: 'lines',
        name: 'Avg.',
        opacity: 1,
        line: {shape: 'hvh', width: 1},
        marker: {
            color: "rgb(44, 160, 44)"
        }
    };
    var trace_stdev = {
        x: trace_time,
        y: hop_stdev,
        mode: 'lines',
        name: 'St. Dev',
        opacity: 0.3,
        line: {shape: 'hvh', width: 5},
        marker: {
            color: "rgb(0, 255, 255)"
        }
    };

    var trace_wrst = {
        x: trace_time,
        y: hop_wrst,
        mode: 'lines',
        name: 'Wrst.',
        opacity: 0.3,
        line: {shape: 'hvh', width: 5},
        marker: {
            color: "rgb(44, 160, 44)"
        }
    };
    var trace_best = {
        x: trace_time,
        y: hop_best,
        mode: 'lines',
        name: 'Best',
        opacity: 1,
        line: {shape: 'hvh', width: 1},
        marker: {
            color: "rgb(214, 39, 40)"
        }
    };

    myShapes = []
    for (var i = 0; i < hop_loss.length; i++){
        if (Number(hop_loss[i]) > 0){
            if (Number(hop_loss[i]) <= 40) {
                color = 'rgb(173,216,230)';
            } else if ((Number(hop_loss[i]) > 40) && (Number(hop_loss[i]) <= 75)) {
                color = 'rgb(128,0,128)';
            } else {
                color = 'rgb(255, 0, 0)';
            }

            shape = {
                'type': 'line',
                'yref': 'paper',
                'x0': trace_time[i],
                'y0': 0,
                'x1': trace_time[i],
                'y1': 1,
                'opacity': 1,
                'line': {
                    'color': color,
                    'width': 1,
                    'dash': 'dot',
                },
            }
            myShapes.push(shape)
        }
    }

    var layout = {
        titlefont : {
            size: 20,
        },
        font: {
            family: 'Consolas',
        },
        showlegend:false,
        shapes: myShapes,
        title: "Title",
        yaxis: {
            title: 'Seconds',
            zeroline: false,
            showline: false,
        },
        xaxis: {
            zeroline: false,
            showline: true,
        },
        height: 300,
        paper_bgcolor: 'rgba(242,244,243,1)',
        margin: {
            t: 50,
        },
    };

    var data = [trace_avg, trace_stdev, trace_wrst, trace_best];

    Plotly.newPlot('left', data, layout);
    read_right_data();

}


function read_right_data(){
    reader.open('get', "./right_data.csv", true);
    reader.onreadystatechange = readRightData;
    reader.send(null);
}
function readRightData(){
    if(reader.readyState==4) {
        var allText = reader.responseText;
        var allTextLines = allText.split(/\r\n|\n/);
        var headers = allTextLines[0].split(',');
        var lines = [];

        for (var i=1; i<allTextLines.length; i++) {
            var data = allTextLines[i].split(',');
            if (data.length == headers.length) {
                lines.push(data);
            }
        }

        var hop_loss = [];
        var hop_avg = [];
        var hop_wrst = [];
        var hop_host = [];

        for (var j = 0; j<lines.length; j++){
            hop_loss.push(lines[j][0]);
            hop_avg.push(lines[j][3]);
            hop_wrst.push(lines[j][5]);
            hop_host.push(lines[j][8]);
        }

        build_right(hop_loss,hop_avg,hop_wrst,hop_host);

    }
}
function build_right(hop_loss,hop_avg,hop_wrst,hop_host){
    var trace1 = {
        x: hop_avg,
        y: hop_host,
        mode: 'lines+markers',
        name: 'Avg.',
        opacity: 0.7,
        marker: {
            color: "rgb(0,0,128)",
            size: 9
        }
    };

    var trace2 = {
        x: hop_wrst,
        y: hop_host,
        mode: 'lines+markers',
        name: 'Wrst.',
        opacity: 0.7,
        marker: {
            color: "rgb	(0,128,0)",
            size: 9
        }
    };


    myShapes = []
    for (var i = 0; i < hop_loss.length; i++){
        if (Number(hop_loss[i]) > 0){
            if (Number(hop_loss[i]) <= 40) {
                color = 'rgb(173,216,230)';
            } else if ((Number(hop_loss[i]) > 40) && (Number(hop_loss[i]) <= 75)) {
                color = 'rgb(128,0,128)';
            } else {
                color = 'rgb(255, 0, 0)';
            }

            shape = {
                'type': 'line',
                'xref': 'paper',
                'x0': 0,
                'y0': i,
                'x1': 1,
                'y1': i,
                'opacity': 0.7,
                'line': {
                    'color': color,
                    'width': 2,
                    'dash': 'dot',
                },
            }
            myShapes.push(shape)
        }
    };


    var layout = {
        showlegend:false,
        shapes: myShapes,
        title: "Hoops",
        height: hop_host.length*30 + 200,
        yaxis: {
            range: [-1,hop_host.length],
            showticklabels: false,
            autorange: 'reversed'
        },
        margin: {
            l: 15,
            r: 50,
            b: 30,
            t: 50,
            pad: 4
        },
        paper_bgcolor: 'rgba(242,244,243,1)',
        titlefont : {
            size: 20,
        },
        font: {
            family: 'Consolas',
        },
        hovermode:'closest',
    };

    var data = [trace1, trace2];

    Plotly.newPlot('right', data, layout);
}


function main(){
    read_left_data();
}