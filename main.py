import base64
from io import BytesIO

from flask import Flask
from matplotlib.figure import Figure

import numpy as np
from matplotlib.collections import LineCollection

app = Flask(__name__)


@app.route("/")
def hello():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

@app.route("/var-width-line")
def hello2():
    x = np.linspace(0, 4 * np.pi, 10000)
    y = np.cos(x)
    lwidths = 1 + x[:-1]
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, linewidths=lwidths, color='blue')
    fig = Figure()
    a = fig.subplots()
    a.add_collection(lc)
    a.set_xlim(0, 4 * np.pi)
    a.set_ylim(-1.1, 1.1)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

