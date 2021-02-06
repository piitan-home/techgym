from typing import Iterable
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def plot3D(X: Iterable, label: Iterable):
    fig = plt.figure()
    ax_3d = Axes3D(fig)
    ax_3d.set_xlabel(label[0])
    ax_3d.set_ylabel(label[1])
    ax_3d.set_zlabel(label[2])
    ax_3d.view_init(elev=10., azim=-15)
    ax_3d.plot(X[0], X[1], X[2], marker='o', linestyle='None', color='blue')
