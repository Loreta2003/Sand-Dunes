import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def interpolate(x_original, y_original, x_new):
    interpolation_function = interp1d(x_original, y_original, kind="linear")
    y_new = interpolation_function(x_new)
    return y_new

file_path = 'all_profiles/experiment53.csv'
data = pd.read_csv(file_path)
rot_num_data = np.array(data.iloc[:, 0])
pos_data = np.array(data.iloc[:, 1])
height_data = np.array(data.iloc[:, 2])
time_data = np.array(data.iloc[:, 3])

rotation = []
index = 0
while rot_num_data[index] == 0:
    index+=1
for current_rot in range(1, rot_num_data[-1]):
    single_rotation_pos = []
    single_rotation_height = []
    single_rotation_time = []
    while rot_num_data[index] == current_rot:
        single_rotation_pos.append(pos_data[index])
        single_rotation_height.append(height_data[index])
        single_rotation_time.append(time_data[index])
        if index < len(rot_num_data) - 1:
            index += 1
        else:
            break
    single_rotation_data = {
        "rotation_number": current_rot,
        "position": np.array(single_rotation_pos),
        "height": np.array(single_rotation_height),
        "time": np.array(single_rotation_time),
        "averaged_timepoint": (single_rotation_time[-1]+single_rotation_time[0])/2
    }
    rotation.append(single_rotation_data)

def Waterfall_Plot():
    x_max = min(rot["position"][-1] for rot in rotation)
    x_min = max(rot["position"][0] for rot in rotation)

    x_coord = np.linspace(x_min, x_max, 10000)
    for rot in rotation:
        interpolated_height=interpolate(rot["position"], rot["height"], x_coord)
        final_height = interpolated_height + (rot["averaged_timepoint"]-rotation[0]["averaged_timepoint"])
        plt.plot(x_coord, final_height, color="orange")
        plt.legend()
        plt.xlabel("x/mm")
        plt.ylabel("Time/s")
    plt.show()

def HeatMap():
    x_max = min(rot["position"][-1] for rot in rotation)
    x_min = max(rot["position"][0] for rot in rotation)

    x_coord = np.linspace(x_min, x_max, 500)
    grid_data = []
    for rot in rotation:
        interpolated_height=interpolate(rot["position"], rot["height"], x_coord)
        grid_data.append(interpolated_height)
    grid_data = np.array(grid_data)
    plt.imshow(grid_data, cmap='viridis', interpolation='nearest')
    plt.colorbar(label="Height")
    #plt.xlabel("x/mm")
    plt.ylabel("Time/s")
    plt.show()

def ContourPlot():
    x_max = min(rot["position"][-1] for rot in rotation)
    x_min = max(rot["position"][0] for rot in rotation)

    x_coord = np.linspace(x_min, x_max, 500)
    times = []
    grid_data = []
    for rot in rotation:
        interpolated_height=interpolate(rot["position"], rot["height"], x_coord)
        times.append(rot["averaged_timepoint"]-rotation[0]["averaged_timepoint"])
        grid_data.append(interpolated_height)
    grid_data = np.array(grid_data)
    times = np.array(times)

    plt.contour(x_coord, times, grid_data, levels=3, cmap='viridis')
    plt.colorbar(label="Height")
    plt.title("Contour Plot")
    plt.xlabel("x/mm")
    plt.ylabel("Time/s")
    plt.show()

ContourPlot()