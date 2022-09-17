import base64
from io import BytesIO
import pathlib
import pandas as pd

from flask import Flask
from matplotlib.figure import Figure

import numpy as np
from matplotlib.collections import LineCollection

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

app = Flask(__name__)


def generate_competition_preview(path):
    fig = Figure(figsize=(2, 2))
    ax = fig.subplots()
    ax.axis('off')
    for run in path.glob('*.csv'):
        data = pd.read_csv(run)
        if 'xPos[m]' in data:
            ax.plot(data['xPos[m]'], data['yPos[m]'])
        elif 'Latitude[deg]' in data:
            ax.plot(data['Latitude[deg]'], data['Longitude[deg]'])
        else:
            print('no columns xpos/ypos', run)

    ax.relim()
    ax.autoscale_view()
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"


@app.route("/")
def hello():
    root_path = pathlib.Path('data/skiing')
    competitions = set()
    for child in root_path.rglob('*.csv'):
        competitions.add(child.parent)
        # break
    competitions = sorted(competitions)
    return ''.join([
        '<div>' + generate_competition_preview(c) + '<br>' + str(c) + '<div>'
        for c in competitions])


@app.route("/sample")
def hello1():
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


@app.route("/multicolor")
def hello3():
    x = np.linspace(0, 3 * np.pi, 500)
    y = np.sin(x)
    dydx = np.cos(0.5 * (x[:-1] + x[1:]))  # first derivative

    # Create a set of line segments so that we can color them individually
    # This creates the points as a N x 1 x 2 array so that we can stack points
    # together easily to get the segments. The segments array for line collection
    # needs to be (numlines) x (points per line) x 2 (for x and y)
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    fig = Figure()
    axs = fig.subplots(2, 1, sharex=True, sharey=True)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(dydx.min(), dydx.max())
    lc = LineCollection(segments, cmap='viridis', norm=norm)
    # Set the values used for colormapping
    lc.set_array(dydx)
    lc.set_linewidth(2)
    line = axs[0].add_collection(lc)
    fig.colorbar(line, ax=axs[0])

    # Use a boundary norm instead
    cmap = ListedColormap(['r', 'g', 'b'])
    norm = BoundaryNorm([-1, -0.5, 0.5, 1], cmap.N)
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(dydx)
    lc.set_linewidth(2)
    line = axs[1].add_collection(lc)
    fig.colorbar(line, ax=axs[1])

    axs[0].set_xlim(x.min(), x.max())
    axs[0].set_ylim(-1.1, 1.1)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"


@app.route("/both")
def hello4():
    x = np.linspace(0, 3 * np.pi, 500)
    y = np.sin(x)
    dydx = np.cos(0.5 * (x[:-1] + x[1:]))  # first derivative

    # Create a set of line segments so that we can color them individually
    # This creates the points as a N x 1 x 2 array so that we can stack points
    # together easily to get the segments. The segments array for line collection
    # needs to be (numlines) x (points per line) x 2 (for x and y)
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    fig = Figure()
    axs = fig.subplots(2, 1, sharex=True, sharey=True)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(dydx.min(), dydx.max())
    lwidths = 1 + (2 * x[:-1])
    lc = LineCollection(segments, cmap='viridis', norm=norm, linewidths=lwidths)
    # Set the values used for colormapping
    lc.set_array(dydx)
    # lc.set_linewidth(2)
    line = axs[0].add_collection(lc)
    fig.colorbar(line, ax=axs[0])

    # Use a boundary norm instead
    cmap = ListedColormap(['r', 'g', 'b'])
    norm = BoundaryNorm([-1, -0.5, 0.5, 1], cmap.N)
    lc = LineCollection(segments, cmap=cmap, norm=norm, linewidths=lwidths)
    lc.set_array(dydx)
    # lc.set_linewidth(2)
    line = axs[1].add_collection(lc)
    fig.colorbar(line, ax=axs[1])

    axs[0].set_xlim(x.min(), x.max())
    axs[0].set_ylim(-1.1, 1.1)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
