import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from scipy.stats import norm

XX = "XX"
YY = "YY"

DTA_FILE = "./example.dta"

def draw_1(plt, data):
    plt.subplot(221)
    plt.hist(x=data["rank_"], bins=60, weights=data["gra_"])
    plt.title("Heading")
    plt.xlabel("x-heading")
    plt.text(1, 25000, "Top " + XX + "%", fontdict={"fontsize":12}, ha='center', va='center')

def draw_2(plt):
    plt.subplot(222)
    x_axis = np.arange(-1.2, 1.2, 0.01)
    plt.plot(x_axis, norm.pdf(x_axis, 0, 1))
    plt.title("Heading")
    plt.xlabel("x-heading")
    plt.text(0.75, 0.35, "Top " + XX + "%", fontdict={"fontsize":12})

def draw_3(plt, data):
    plt.subplot(223)
    dta = data[np.isfinite(data["note_"])]
    plt.hist(dta["note_"], normed=True, weights=dta["gra_"], width=0.9, range=(0, 5)) #range=[1, 4.1])
    plt.gca().invert_xaxis()
    plt.title("Heading")
    plt.xlabel("x-heading")
    plt.text(1.1, 0.65, "Top " + YY + "%", fontdict={"fontsize":12})

def draw_4(plt):
    plt.subplot(224)
    x_axis = np.arange(0, 4, 0.01)
    plt.plot(x_axis, norm.pdf(x_axis, 2, 3))
    plt.title("Heading")
    plt.xlabel("x-heading")
    plt.text(1, 0.13, "Top " + YY + "%", fontdict={"fontsize":12})
    plt.gca().invert_xaxis()

def main():
    style.use("ggplot")
    data = pd.io.stata.read_stata(DTA_FILE)
    plt.figure(1)

    draw_1(plt, data)
    draw_2(plt)
    draw_3(plt, data)
    draw_4(plt)

    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    main()
