import plotly.plotly as py
import plotly.graph_objs as go

USER_NAME = 'stas2104'
API_KEY = '1fh8baq323'

FILE_NAME = "./sample_data.csv"


def read_data(filename):
    import csv
    hop_avg = []
    hop_stdev = []
    trace_time = []
    hop_wrst = []
    hop_loss = []
    hop_best = []
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            hop_avg.append(row[0])
            hop_stdev.append(row[2])
            trace_time.append(row[3].replace("+13", ""))
            hop_wrst.append(row[4])
            hop_loss.append(row[5])
            hop_best.append(row[6])

    return (hop_avg[1:], hop_stdev[1:], trace_time[1:], hop_wrst[1:], hop_loss[1:], hop_best[1:])


def make_trace_avg(trace_time, hop_avg, legend_data):
    res = go.Scatter(
        x=trace_time,
        y=hop_avg,
        mode='lines',
        name=legend_data,
        hoverinfo='name',
        opacity=1,
        line=dict(
            shape='hvh',
            width=1
        )
    )
    return res


def make_trace_stdev(trace_time, hop_stdev, legend_data):
    res = go.Scatter(
        x=trace_time,
        y=hop_stdev,
        mode='lines',
        name=legend_data,
        hoverinfo='name',
        opacity=0.3,
        line=dict(
            shape='hvh',
            width=5
        ),
        marker=dict(
            color="rgb(0, 255, 255)"
        )
    )
    return res


def make_trace_wrst(trace_time, hop_wrst, legend_data):
    res = go.Scatter(
        x=trace_time,
        y=hop_wrst,
        mode='lines',
        name=legend_data,
        hoverinfo='name',
        opacity=0.3,
        line=dict(
            shape='hvh',
            width=5,
        ),
        marker=dict(
            color="rgb(44, 160, 44)"
        )
    )
    return res


def make_trace_best(trace_time, hop_best, legend_data):
    res = go.Scatter(
        x=trace_time,
        y=hop_best,
        mode='lines',
        name=legend_data,
        hoverinfo='name',
        line=dict(
            shape='hvh',
            width=1
        ),
        marker=dict(
            color="rgb(214, 39, 40)"
        )
    )
    return res


def make_trase_loss(hop_loss, trace_time):
    shapes = []
    for idx, val in enumerate(hop_loss):
        if float(val) != 0:
            shapes.append(
                {
                    'type': 'line',
                    'yref': 'paper',
                    'x0': trace_time[idx],
                    'y0': 0,
                    'x1': trace_time[idx],
                    'y1': 1,
                    'opacity': 0.5,
                    'line': {
                        'color': 'rgb(255, 0, 0)',
                        'width': 1,
                        'dash': 'dot',
                    },
                }
            )
    return shapes


def make_layout(shapes):
    layout = dict(
        titlefont=dict(
            size=20,
        ),
        font=dict(
            family='Consolas',
        ),
        legend=dict(
            y=-1.2,
            x=0,
            traceorder='normal',
            font=dict(
                size=14
            )
        ),
        shapes=shapes,
        title="Title",
        yaxis=dict(
            title='Seconds',
            zeroline=False,
            showline=True,
        ),
        xaxis=dict(
            zeroline=False,
            showline=True,
        ),
        height=300,
        paper_bgcolor='rgba(242,244,243,1)',
        margin=dict(
            t=50,
        ),
    )
    return layout


def main():
    (hop_avg, hop_stdev, trace_time, hop_wrst, hop_loss, hop_best) = read_data(FILE_NAME)

    trace_avg = make_trace_avg(trace_time, hop_avg, "Avg.")
    trace_stdev = make_trace_stdev(trace_time, hop_stdev, "St. Dev")
    trace_wrst = make_trace_wrst(trace_time, hop_wrst, "Wrst.")
    trace_best = make_trace_best(trace_time, hop_best, "Best")

    data = [trace_avg, trace_stdev, trace_wrst, trace_best]

    shapes = make_trase_loss(hop_loss, trace_time)
    layout = make_layout(shapes)

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='line-shapes')

if __name__ == "__main__":
    py.sign_in(USER_NAME, API_KEY)

    main()