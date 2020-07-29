# Constant Fraction Discriminator

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import shift
from scipy.signal import find_peaks


def pileup_adjust(edges, width=4, delta_width=2):
    # an idea to %mod wide peaks by 4 and count possible stacks
    # may not be needed if I can get parameters right
    widths = edges[1::2] - edges[:-1:2]
    print(widths)
    stacked_bool = widths > width + delta_width
    #np.append(rising_edge, new_edges)
    print(stacked_bool)
    rising_edge = edges[::2]
    return rising_edge


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
    
    cfd_signal = signal - delayed
    plt.xlim(0, len(spectrum))
    plt.ylim(0, max(spectrum)+20)
    plt.plot(signal, '--', alpha=.5, color='blue', label='original signal')
    plt.plot(scaled, ':', alpha=.5, color='red', label='scaled signal')
    plt.plot(delayed,'-.', alpha=.5, color='green', label='delayed signal')
    plt.plot(cfd_signal,'-', color='black',label='cfd_signal')
    plt.axhline(threshold, linestyle='-', color='black', alpha=.3, label='threshold')
    plt.title("CFD processing (Ar 2+ Data)")
    plt.xlabel("tof (.5ns)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.show()
    # Edge detection
    # edges_bool is true when signal is above threshold
    edges_bool = cfd_signal > threshold

    # edges bool 2
    # XOR comparison of edges_bool[1:], edges_bool[:-1]
    # Returns true if odd number of trues
    # compares each element of edges_bool with neighbor
    # if one is false and one is true
    # returns true
    # meaning that one index is below threshold
    # one is above
    # this is an edge of the peak
    edges_bool_2 = np.logical_xor(edges_bool[1:],edges_bool[:-1])
    
    # Edge indicies are where edges_bool_2 is true
    # np.squeeze() just makes it 1d
    edge_index = np.squeeze(np.where(edges_bool_2 == True))
    print(edge_index)
    
    return edge_index
        

if __name__ == "__main__":

    #Ar2+ Data
    #spectrum = np.array([-2.1741943, -2.1741943, -0.17419434, 1.8258057, -1.1741943, -4.1741943, 1.8258057, 4.8258057, 40.825806, 125.825806, 208.8258, 207.8258, 130.8258, 35.825806, -17.174194, -46.174194, -48.174194, -32.174194, -17.174194, -2.1741943, -4.1741943, -8.174194, -1.1741943, -6.1741943, -5.1741943, -5.1741943, -6.1741943, 4.8258057, 31.825806, 120.825806, 248.8258, 298.8258, 233.8258, 149.8258, 159.8258, 254.8258, 310.8258, 262.8258, 148.8258, 92.825806, 131.8258, 192.8258, 233.8258, 290.8258, 414.8258, 556.8258, 565.8258, 411.8258, 187.8258, 10.825806, -84.174194, -90.174194, -79.174194, -32.174194, 63.825806, 238.8258, 413.8258, 449.8258, 326.8258, 153.8258, 15.825806, -52.174194, -60.174194, -33.174194, 25.825806, 126.825806, 206.8258, 220.8258, 244.8258, 392.8258, 586.8258, 695.8258, 654.8258, 476.8258, 235.8258, 55.825806, -36.174194, -60.174194, -41.174194, -17.174194])
    #Ar3+ Data
    #spectrum = np.array([-2.1741943, 3.8258057, 9.825806, 67.825806, 206.8258, 438.8258, 678.8258, 790.8258, 690.8258, 435.8258, 163.8258, -30.174194, -90.174194, -90.174194, -64.174194, 105.825806, 488.8258, 997.8258, 1300.8258, 1304.8258, 1093.8258, 756.8258, 358.8258, 93.825806, 89.825806, 357.8258, 695.8258, 896.8258, 863.8258, 663.8258, 503.8258, 540.8258, 674.8258, 674.8258, 489.8258, 238.8258, 38.825806, 8.825806, 132.8258, 277.8258, 310.8258, 225.8258, 108.825806, 13.825806, -22.174194, -11.174194, 4.8258057, 27.825806, 41.825806, 47.825806, 59.825806, 151.8258, 336.8258, 575.8258, 756.8258, 765.8258, 568.8258, 281.8258, 45.825806, -76.174194, -90.174194, -60.174194, -14.174194, 21.825806, 40.825806, 31.825806, 12.825806, 7.8258057, -1.1741943, 4.8258057, 29.825806, 129.8258, 282.8258, 367.8258, 307.8258, 176.8258, 52.825806, -26.174194, -52.174194, -32.174194])
    #Ar4+ Data
    #spectrum = np.array([-0.17419434, 6.8258057, 46.825806, 140.8258, 232.8258, 225.8258, 153.8258, 117.825806, 225.8258, 396.8258, 493.8258, 487.8258, 440.8258, 349.8258, 205.8258, 51.825806, -19.174194, 36.825806, 183.8258, 273.8258, 253.8258, 148.8258, 40.825806, -31.174194, -53.174194, -47.174194, -19.174194, 3.8258057, 7.8258057, 12.825806, 9.825806, 10.825806, 7.8258057, 8.825806, 13.825806, 10.825806, 12.825806, 13.825806, 16.825806, 18.825806])
    #Ar5+ Data
    #spectrum = np.array([0.82580566, -3.1741943, 0.82580566, -1.1741943, -2.1741943, -2.1741943, 2.8258057, -2.1741943, 24.825806, 109.825806, 234.8258, 270.8258, 207.8258, 107.825806, 108.825806, 211.8258, 309.8258, 316.8258, 335.8258, 436.8258, 531.8258, 476.8258, 301.8258, 105.825806, -20.174194, -29.174194, 123.825806, 348.8258, 471.8258, 448.8258, 409.8258, 418.8258, 401.8258, 343.8258, 351.8258, 449.8258, 520.8258, 455.8258, 290.8258, 171.8258, 272.8258, 612.8258, 1021.8258, 1220.8258, 1101.8258, 741.8258, 332.8258, 42.825806, -74.174194, -80.174194, -33.174194, 27.825806, 54.825806, 57.825806, 49.825806, 45.825806, 42.825806, 41.825806, 37.825806, 32.825806])
    #Ar6+ Data
    #spectrum = np.array([-10.174194, -7.1741943, -6.1741943, -5.1741943, -5.1741943, -0.17419434, -3.1741943, 0.82580566, 1.8258057, 7.8258057, 1.8258057, 8.825806, 6.8258057, 7.8258057, 5.8258057, 6.8258057, 2.8258057, 2.8258057, 2.8258057, 6.8258057, 2.8258057, 3.8258057, 1.8258057, 2.8258057, 1.8258057, -0.17419434, 0.82580566, 1.8258057, -0.17419434, 2.8258057, 24.825806, 120.825806, 310.8258, 481.8258, 477.8258, 323.8258, 128.8258, -8.174194, -64.174194, -59.174194, -36.174194, -14.174194, -5.1741943, -3.1741943, -9.174194, -4.1741943, -5.1741943, 1.8258057, -2.1741943, 2.8258057, 1.8258057, 1.8258057, 7.8258057, 8.825806, 3.8258057, 12.825806, 6.8258057, 11.825806, 11.825806, 13.825806])
    #Ar7+ Data
    #spectrum = np.array([-0.17419434, 0.82580566, -1.1741943, -2.1741943, -3.1741943, -3.1741943, -4.1741943, -1.1741943, -6.1741943, 1.8258057, 3.8258057, 3.8258057, 5.8258057, 6.8258057, 5.8258057, 4.8258057, -0.17419434, 3.8258057, 17.825806, 86.825806, 276.8258, 554.8258, 843.8258, 977.8258, 882.8258, 600.8258, 319.8258, 258.8258, 436.8258, 632.8258, 772.8258, 973.8258, 1245.8258, 1341.8258, 1234.8258, 1091.8258, 940.8258, 720.8258, 433.8258, 161.8258, -18.174194, -65.174194, -62.174194, -43.174194, -3.1741943, 36.825806, 54.825806, 57.825806, 50.825806, 32.825806, 18.825806, 18.825806, 32.825806, 51.825806, 62.825806, 60.825806, 53.825806, 44.825806, 38.825806, 32.825806])
    #Ar8+ Data
    #spectrum = np.array([-0.17419434, -2.1741943, 1.8258057, -3.1741943, 20.825806, 104.825806, 269.8258, 400.8258, 401.8258, 282.8258, 128.8258, 3.8258057, -61.174194, -65.174194, -45.174194, -23.174194, 0.82580566, -0.17419434, 0.82580566, -2.1741943, 3.8258057, 3.8258057, 16.825806, 98.825806, 318.8258, 604.8258, 764.8258, 675.8258, 469.8258, 354.8258, 442.8258, 614.8258, 741.8258, 824.8258, 827.8258, 702.8258, 478.8258, 242.8258, 70.825806, 82.825806, 288.8258, 553.8258, 691.8258, 625.8258, 405.8258, 160.8258, 6.8258057, -56.174194, -49.174194, -7.1741943, 28.825806, 43.825806, 38.825806, 37.825806, 37.825806, 25.825806, 24.825806, 21.825806, 15.825806, 21.825806])
    #Ar9+ Data
    #spectrum = np.array([0.82580566, -1.1741943, -4.1741943, 2.8258057, -0.17419434, 3.8258057, -3.1741943, -2.1741943, -2.1741943, 0.82580566, -5.1741943, 1.8258057, -2.1741943, 1.8258057, 0.82580566, -4.1741943, -0.17419434, -0.17419434, -1.1741943, 0.82580566, 0.82580566, 2.8258057, 3.8258057, -0.17419434, -0.17419434, 1.8258057, 0.82580566, -1.1741943, 3.8258057, 1.8258057, 1.8258057, 3.8258057, 1.8258057, -2.1741943, 0.82580566, 1.8258057, 1.8258057, -1.1741943, 0.82580566, 1.8258057, 1.8258057, -1.1741943, -2.1741943, 1.8258057, -2.1741943, 3.8258057, -3.1741943, -1.1741943, 0.82580566, -3.1741943, -1.1741943, -1.1741943, -2.1741943, 0.82580566, -4.1741943, -2.1741943, -2.1741943, 0.82580566, -0.17419434, -1.1741943])
    #Ar10+ Data
    #spectrum = np.array([-26.174194, -21.174194, -3.1741943, 12.825806, 18.825806, 14.825806, 0.82580566, -2.1741943, -4.1741943, -8.174194, -4.1741943, -2.1741943, -2.1741943, -2.1741943, -2.1741943, -1.1741943, 4.8258057, -3.1741943, 0.82580566, -2.1741943, -6.1741943, -3.1741943, -3.1741943, -2.1741943, -2.1741943, -6.1741943, -4.1741943, -2.1741943, -2.1741943, -2.1741943, -0.17419434, -0.17419434, 4.8258057, -4.1741943, -1.1741943, 5.8258057, -4.1741943, 2.8258057, 3.8258057, -0.17419434, 5.8258057, -0.17419434, 0.82580566, 0.82580566, -2.1741943, -0.17419434, 4.8258057, 1.8258057, 2.8258057, 1.8258057, -3.1741943, 1.8258057, 0.82580566, 3.8258057, 0.82580566, -0.17419434, -0.17419434, -6.1741943, -1.1741943, -3.1741943])
    #Ar11+ Data
    #spectrum = np.array([-2.1741943, -1.1741943, -1.1741943, -0.17419434, -0.17419434, -1.1741943, -4.1741943, 1.8258057, -4.1741943, 0.82580566, -1.1741943, -2.1741943, -2.1741943, -0.17419434, -2.1741943, 4.8258057, -5.1741943, -0.17419434, 0.82580566, -4.1741943, -0.17419434, 22.825806, 143.8258, 451.8258, 798.8258, 947.8258, 816.8258, 501.8258, 170.8258, -39.174194, -72.174194, 95.825806, 402.8258, 618.8258, 572.8258, 357.8258, 119.825806, -35.174194, -90.174194, -86.174194, -55.174194, -16.174194, 3.8258057, 8.825806, 6.8258057, 16.825806, 16.825806, 15.825806, 17.825806, 20.825806, 17.825806, 16.825806, 18.825806, 20.825806, 12.825806, 19.825806, 21.825806, 17.825806, 24.825806, 20.825806])
    #Ar12+ Data
    #spectrum = np.array([-3.1741943, -0.17419434, -3.1741943, -2.1741943, 3.8258057, 39.825806, 200.8258, 530.8258, 822.8258, 893.8258, 706.8258, 380.8258, 92.825806, -72.174194, -90.174194, -90.174194, -47.174194, -1.1741943, 7.8258057, 4.8258057, 4.8258057, 2.8258057, -4.1741943, -2.1741943, -1.1741943, -1.1741943, 0.82580566, 3.8258057, 4.8258057, 4.8258057, 5.8258057, 3.8258057, 3.8258057, 7.8258057, 6.8258057, 8.825806, 9.825806, 7.8258057, 4.8258057, 9.825806, 7.8258057, 1.8258057, 7.8258057, 3.8258057, 5.8258057, 8.825806, 7.8258057, 10.825806, 9.825806, 8.825806, 8.825806, 8.825806, 10.825806, 15.825806, 14.825806, 11.825806, 6.8258057, -2.1741943, -7.1741943, -13.174194, -12.174194, -18.174194, -13.174194, -4.1741943, -3.1741943, 5.8258057, 8.825806, 11.825806, 12.825806, 12.825806, 6.8258057, 8.825806, 10.825806, 7.8258057, 11.825806, 10.825806, 11.825806, 19.825806, 19.825806, 23.825806])
    #Ar13+ Data
    #spectrum = np.array([-0.17419434, -0.17419434, 0.82580566, -3.1741943, 2.8258057, 2.8258057, 0.82580566, 1.8258057, -1.1741943, 2.8258057, -0.17419434, 1.8258057, 3.8258057, -4.1741943, 1.8258057, -1.1741943, -2.1741943, -0.17419434, 0.82580566, -0.17419434, 1.8258057, -0.17419434, -1.1741943, 30.825806, 183.8258, 519.8258, 896.8258, 1064.8258, 923.8258, 584.8258, 227.8258, -20.174194, -90.174194, -50.174194, 185.8258, 522.8258, 762.8258, 756.8258, 558.8258, 275.8258, 58.825806, -54.174194, -70.174194, -45.174194, -4.1741943, 24.825806, 26.825806, 22.825806, 18.825806, 14.825806, 11.825806, 10.825806, 12.825806, 11.825806, 20.825806, 39.825806, 107.825806, 182.8258, 188.8258, 137.8258])
    spectrum = np.array([0.82580566, 3.8258057, 2.8258057, -0.17419434, 0.82580566, 1.8258057, -0.17419434, 15.825806, 81.825806, 253.8258, 413.8258, 435.8258, 308.8258, 137.8258, 6.8258057, -19.174194, 75.825806, 188.8258, 202.8258, 136.8258, 39.825806, -26.174194, -57.174194, -49.174194, -29.174194, 35.825806, 199.8258, 475.8258, 693.8258, 724.8258, 614.8258, 496.8258, 382.8258, 260.8258, 126.825806, 11.825806, -44.174194, -55.174194, -34.174194, 96.825806, 365.8258, 638.8258, 739.8258, 705.8258, 615.8258, 555.8258, 491.8258, 403.8258, 264.8258, 122.825806, 24.825806, 64.825806, 231.8258, 401.8258, 502.8258, 517.8258, 417.8258, 250.8258, 84.825806, -9.174194])
    

    #Ar16+ Data
    #spectrum = np.array([-0.17419434, 5.8258057, 0.82580566, -0.17419434, -1.1741943, 0.82580566, -2.1741943, -0.17419434, 0.82580566, -2.1741943, -4.1741943, 0.82580566, -0.17419434, 1.8258057, -0.17419434, 1.8258057, -0.17419434, 1.8258057, -0.17419434, -1.1741943, -1.1741943, 0.82580566, -1.1741943, -1.1741943, 8.825806, 85.825806, 286.8258, 575.8258, 774.8258, 872.8258, 852.8258, 666.8258, 375.8258, 117.825806, -40.174194, -90.174194, -74.174194, -40.174194, -9.174194, 12.825806, 13.825806, 18.825806, 10.825806, 10.825806, 14.825806, 12.825806, 7.8258057, 16.825806, 14.825806, 20.825806, 19.825806, 15.825806, 17.825806, 15.825806, 12.825806, 15.825806, 13.825806, 16.825806, 11.825806, 16.825806])
    
    f=.51
    d=1.75
    t= 30 #210 for ar3+
    edges = cfd(signal=spectrum, fraction=f, delay=d, threshold=t)


    plt.clf()
    plt.xlim(0, len(spectrum))
    plt.ylim(0, max(spectrum)+20)
    plt.title("CFD Results (Ar 2+ Data)")
    plt.xlabel("tof (.5ns)")
    plt.ylabel("Amplitude")
    plt.plot(spectrum, '-', color='black', label='original signal')

    peaks, _ = find_peaks(spectrum, prominence=82, wlen=20)
    plt.plot(peaks, spectrum[peaks], "x", color='darkorange', label='peak finder', markersize=12)
    
    for edge in edges[::2]:
        if edge == edges[-2]:
            plt.axvline(edge, color="r", linestyle="--", alpha=.6, label='CFD')
        else:
            plt.axvline(edge, color="r", linestyle="--", alpha=.6)#, label='Ion detected')

            


    plt.legend()
    plt.draw()
    plt.show()
    #print(widths)
    #print(np.mean(widths), np.std(widths))

    

    
