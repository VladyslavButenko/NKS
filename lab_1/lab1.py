import numpy as np
data = np.array([3544, 20, 207, 1796, 327, 285, 732,
                551, 956, 642, 169, 5, 137, 616, 1352,
                302, 271,9, 13, 408, 45, 738, 854, 640,
                131, 1921, 472,1092, 166, 703, 155, 406, 223, 1070, 286,
                431, 375, 208, 449, 151, 39, 129, 487,
                17, 185, 302, 494, 695, 7, 204, 195, 121,
                1438, 311, 121, 455, 4, 361, 647, 540, 125,
                704, 7, 99, 628, 387, 193, 106, 1022, 1434,
                684, 76, 144, 761, 45, 672, 852, 872, 1215,
                1970, 42, 18, 529, 244, 1104, 1130, 2751,
                2134, 657, 867, 692, 61, 222, 122, 296, 789,
                408, 1138, 150, 1049])

gamma = 0.53
working_time = 3295
malfunction_intensity = 2556
N = len(data)

sorted_data = sorted(data)

mean_value = data.mean()

max_value = sorted_data[len(sorted_data) - 1]

k = 10
h = max_value / k

intervals = [round(interval * h, 2) for interval in range(k + 1)]

def data_sort_through_intervals(arr, intervals):
    data_intervals = [[] for _ in range(k)]
    for element in arr:
        for i in range(k):
            if intervals[i] <= element <= intervals[i + 1]:
                data_intervals[i].append(element)
    return data_intervals

def f_calculator(data_intervals, k):
    F = [0 for _ in range(k)]
    for i in range(k):
        F[i] = len(data_intervals[i]) / (N * h)
    return F


def find_the_interval(number, intervals):
    for i in range(k):
        if intervals[i] <= number <= intervals[i + 1]:
            return i


def probabilities(frequency):
    P = [0 for _ in range(k)]
    for i in range(k):
        square = 0
        for j in range(i + 1):
            square += (frequency[j] * h)
        P[i] = round(1 - square, 5)
    return P


def T(percentage, probability_arr, intervals):
    new_p_arr = probability_arr.copy()
    new_p_arr.insert(0, 1)
    for i in range(len(new_p_arr)):
        if new_p_arr[i] > percentage:
            new_p_arr.insert(i + 1, percentage)
    index = new_p_arr.index(percentage)
    d = round((new_p_arr[index + 1] - percentage) / (new_p_arr[index + 1] - new_p_arr[index - 1]), 2)
    T_value = round(intervals[index] - h * d, 2)
    return T_value


def probability_for_time(time, frequency_arr, intervals):
    number_of_interval = find_the_interval(time, intervals)
    square = 0
    for i in range(number_of_interval + 1):
        if i != number_of_interval:
            square += (frequency_arr[i] * h)
        else:
            square += (frequency_arr[i] * (time - intervals[i]))
    p = round(1 - square, 4)
    return p


def intensity_for_time(time, frequency_arr, intervals):
    number_of_interval = find_the_interval(time, intervals)
    p = probability_for_time(time, frequency_arr, intervals)
    return round(frequency_arr[number_of_interval] / p, 4)


data_intervals = data_sort_through_intervals(sorted_data, intervals)
print("Intervals: \n", intervals)

f_array = f_calculator(data_intervals, k)

p_array = probabilities(f_array)

t_value = T(gamma, p_array, intervals)
print("Average time to failure: ", t_value)

p = probability_for_time(working_time, f_array, intervals)
print("Probable time to failure: " + str(working_time) + " year" + "\n", p)

intensity = intensity_for_time(malfunction_intensity, f_array, intervals)
print("Intensity for  " + str(malfunction_intensity) + " year" + "\n", intensity)
