# Constant Fraction Discriminator

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import shift


def cfd(signal, fraction, delay=1, threshold=20):
    """Constant Fraction Discriminator
    :param np.array signal: the input from the digitizer
    :param float fraction: the fraction, from 0 to 1
    :param float delay: the delay of the CFD
    :param float threshold: the threshold
    :return np.array edge_indices: the start and stop indices for each peak
    """

    # Scaled and delayed signal
    scaled = signal * fraction
    delayed = shift(scaled, -delay, mode="nearest")

    #plt.plot(signal, color='green')
    plt.plot(delayed, color='red')
    
    cfd_signal = signal - delayed
    plt.plot(cfd_signal, color='green')
    plt.axhline(t, alpha=.2, color='green')

    # Edge detection
    # edges_bool is true when signal is above threshold
    edges_bool = cfd_signal > threshold
    
    edges_bool_2 = edges_bool[1:] != edges_bool[:-1]
    # Edge indicies are where edges_bool_2 is true
    edge_indices = np.squeeze(np.where(edges_bool_2 == True))

    print(edge_indices)
    for edge in edge_indices:
        plt.axvline(edge, color="r", linestyle="solid", alpha=.3)

    plt.show()


    return edge_indices
        

if __name__ == "__main__" :

    spectrum = np.array([-2.1741943, -2.1741943, -0.17419434, 1.8258057, -1.1741943, -4.1741943, 1.8258057, 4.8258057, 40.825806, 125.825806, 208.8258, 207.8258, 130.8258, 35.825806, -17.174194, -46.174194, -48.174194, -32.174194, -17.174194, -2.1741943, -4.1741943, -8.174194, -1.1741943, -6.1741943, -5.1741943, -5.1741943, -6.1741943, 4.8258057, 31.825806, 120.825806, 248.8258, 298.8258, 233.8258, 149.8258, 159.8258, 254.8258, 310.8258, 262.8258, 148.8258, 92.825806, 131.8258, 192.8258, 233.8258, 290.8258, 414.8258, 556.8258, 565.8258, 411.8258, 187.8258, 10.825806, -84.174194, -90.174194, -79.174194, -32.174194, 63.825806, 238.8258, 413.8258, 449.8258, 326.8258, 153.8258, 15.825806, -52.174194, -60.174194, -33.174194, 25.825806, 126.825806, 206.8258, 220.8258, 244.8258, 392.8258, 586.8258, 695.8258, 654.8258, 476.8258, 235.8258, 55.825806, -36.174194, -60.174194, -41.174194, -17.174194])
    f=.3
    d=5
    t=130
    edges = cfd(signal=spectrum, fraction=f, delay=d, threshold=t)

    plt.clf()
    plt.plot(spectrum)

    for edge in edges :
        plt.axvline(edge, color="r", linestyle="solid", alpha=.3)

    plt.xlim(0, len(spectrum))
    plt.ylim(0, max(spectrum)+20)
    plt.draw()
    plt.show()
    
    widths = edges[1::2] - edges[:-1:2]
    
    print(widths)
    print(np.mean(widths), np.std(widths))
