import os
import csv
import numpy as np

csv_dir = os.path.join(os.path.dirname(__file__), 'data')
in_csv = os.path.join(csv_dir, 'profile2.csv')
out_csv = in_csv.replace('.csv', '_new.csv')

lines = []
values = []
global_dep_index = []
dep_type = {'depression': "depression", 'ascending': "ascending", 'descending': "descending", 'unknown': 'unknown'}

with open(in_csv) as f:
    lines = f.readlines()
    for index, line in enumerate(lines):
        if index > 0:
            # print(index)
            line = line.strip()
            value = line.split(",")[-1]
            values.append(float(value))

size = len(values)
print("Total number of lines: {}".format(size))

def check_dep_type(value_list, index):
    if index == 0:
        if value_list[0] <= value_list[1]:
            return dep_type['ascending']
        else:
            return dep_type['descending']
    elif index == (len(value_list) - 1):
        if value_list[len(value_list) - 2] >= value_list[len(value_list) - 1]:
            return dep_type['descending']
        else:
            return dep_type['ascending']
    else:
        if (value_list[index] <= value_list[index - 1]) and (value_list[index]) <= value_list[index + 1]:
            return dep_type['depression']
        elif (value_list[index] > value_list[index - 1]) and (value_list[index] < value_list[index + 1]):
            return dep_type['ascending']
        elif (value_list[index] > value_list[index + 1]) and (value_list[index] < value_list[index - 1]):
            return dep_type['descending'] 
        else:
            return dep_type['unknown']

min_index = np.argmin(values)
print(check_dep_type(values, 50))

def find_acending(value_list, index):
    ascending_loc = []
    cursor = index
    while (cursor < (len(value_list) - 1 )) and (value_list[cursor] < value_list[cursor + 1]):
        ascending_loc.append(cursor)
        cursor = cursor + 1
    ascending_loc.append(cursor)
    return set(ascending_loc)
 

def find_descending(value_list, index):
    descending_loc = []
    cursor = index
    while (cursor < (len(value_list) - 1 )) and (value_list[cursor] > value_list[cursor + 1]):
        descending_loc.append(cursor)
        cursor = cursor + 1
    descending_loc.append(cursor)
    return set(descending_loc)

def find_descending_backward(value_list, index):
    descending_loc = []
    cursor = index
    while (cursor > 0) and (value_list[cursor] < value_list[cursor - 1]):
        descending_loc.append(cursor)
        cursor = cursor - 1
    descending_loc.append(cursor)
    return set(descending_loc[::-1])


def find_depression(value_list, index):
    dep_loc = []
    ascending_loc = list(find_acending(value_list, index))
    descending_loc = list(find_descending_backward(value_list, index))
    dep_loc = descending_loc + ascending_loc[1:]
    return set(dep_loc)


def fill_depression(value_list, dep_set):
    dep_loc = list(dep_set)
    pour_value = np.min([value_list[dep_loc[0]], value_list[dep_loc[-1]]])
    for item in dep_loc:
        if value_list[item] > pour_value:
            dep_set.remove(item)
    return dep_set


min_index = 1189
print(np.argmin(values))
dep_pts = find_depression(values, min_index)
print(dep_pts)
print(fill_depression(values, dep_pts))

global_set = set(range(size))
print(len(global_set))


def process_edges():
    left_edge = find_acending(values, 0)
    if len(left_edge) > 0:
        for item in left_edge:
            global_set.remove(item)

    right_edge = find_descending_backward(values, size - 1)
    if len(right_edge) > 0:
        for item in right_edge:
            global_set.remove(item)

process_edges()
num_arr = np.array(values)
# min_candidates = list(np.where(num_arr == 51.9285)[0])
# print(min_candidates)
# for item in min_candidates:
#     print(item)

dep_list = []

while len(global_set) > 0:
    tmp_arr = num_arr[list(global_set)]
    min_value = np.min(tmp_arr)
    min_candidates = list(np.where(num_arr == min_value)[0])
    
    min_index = min_candidates[0]

    if len(min_candidates) > 1:
        for item in min_candidates:
            if item in global_set: 
                min_index = item
                break

    dep_index = find_depression(values, min_index)
    # print(dep_index)
    dep_list.append(dep_index)

    for item in dep_index:
        if item in global_set: 
            global_set.remove(item)

print(dep_list)

level1_values = np.copy(num_arr)
for dep in dep_list:
    true_dep = fill_depression(values, dep)
    pour_value = np.max(num_arr[list(true_dep)])
    level1_values[list(dep)] = pour_value

print(len(level1_values.tolist()))

# print(fill_depression(values, find_depression(values, min_index))




# print(find_acending(values, 50))
# print(find_descending(values, 580))

left_index = 0
right_index = size -1

new_values = [0] * size

while left_index <= right_index:
    # print("left index: {}; right index: {}".format(left_index, right_index))
    left_value = values[left_index]
    right_value = values[right_index]
    if left_value < right_value:
        if left_index == 0: 
            new_values[left_index] = left_value
        elif left_value < new_values[left_index - 1]:
            new_values[left_index] = new_values[left_index - 1] 
        else:
            new_values[left_index] = left_value

        left_index = left_index + 1
    else:
        if right_index == size - 1:
            new_values[right_index] = right_value
        elif right_value < new_values[right_index + 1]:
            new_values[right_index] = new_values[right_index + 1]
        else:
            new_values[right_index] = right_value

        right_index = right_index - 1

# # print(len(new_values))


# def process_edges(value_list):
#     size = len(value_list)
#     left_loc = 0
#     right_loc = size - 1
#     for index, value in enumerate(value_list):
#         if value < value_list[index + 1]:
#             left_loc = index + 1
#         else:
#             left_loc = index
#             break
#     left_pour = value_list[left_loc]
#     for i in range(left_loc + 1):
#         value_list[i] = left_pour
#         global_dep_index.append(i)

#     print("left pour: {} - {}".format(left_loc, left_pour))

#     for index, value in enumerate(reversed(value_list)):
#         # print("index: {}; value: {}".format(index, value))
#         if value < value_list[size - (index + 2)]:
#             right_loc = size - 2 - index
#         else:
#             right_loc = size - 1 - index
#             break
#     right_pour = value_list[right_loc]


#     for i in range(right_loc, size):
#         value_list[i] = right_pour
#         global_dep_index.append(i)

#     print("right pour: {} - {}".format(right_loc, right_pour))

#     return value_list
            

# def find_depression(value_list, valley_index):
#     dep_index = []
#     dep_dict = {}
#     size = len(value_list)
#     if valley_index > 0 and valley_index < size - 1:
#         min_value = value_list[valley_index]
#         left_index = valley_index - 1
#         right_index = valley_index + 1


#         left_value = value_list[left_index]
#         right_value = value_list[right_index]

#         dep_index.append(valley_index)
#         dep_index.append(left_index)
#         dep_index.append(right_index)
#         # dep_dict[valley_index] = value_list[valley_index]
#         # dep_dict[left_index] = value_list[left_index]
#         # dep_dict[right_index] = value_list[right_index]

#         # print("valley index: {} - {}".format(valley_index, value_list[valley_index]))
#         # print("left index: {} - {}".format(left_index, value_list[left_index]))
#         # print("right index: {} - {}".format(right_index, value_list[right_index]))

#         while (left_value >= min_value and right_value >= min_value):
#             min_value = np.min([left_value, right_value])
#             # print('min value: {}'.format(min_value))
#             # if min_value == 49.74258:
#             #     print("stop")
#             if (left_index in global_dep_index) or (right_index in global_dep_index):
#                 break

#             if left_value > right_value and right_index < (size - 1):
#                 # min_value = right_value
#                 right_index = right_index + 1
#                 right_value = value_list[right_index]
#                 # dep_dict[right_index] = value_list[right_index]
#                 if right_value >= min_value:
#                     dep_index.append(right_index)
#                     # print("right index: {} - {}".format(right_index, value_list[right_index]))
#             elif right_index == size -1:
#                 break
#             else:
#                 # min_value = left_value
#                 left_index = left_index - 1
#                 left_value = value_list[left_index]
#                 # dep_dict[left_index] = value_list[left_index]
#                 if left_value >= min_value:
#                     dep_index.append(left_index)
#                     # print("left index: {} - {}".format(left_index, value_list[left_index]))

#         for item in sorted(dep_index):
#             dep_dict[item] = value_list[item]
#             # global_dep_index.append(item)

#         return dep_dict, min_value


# def fill_depression(value_list, dep_dict, pour_value):
#     for key in dep_dict:
#         if key not in global_dep_index:
#             value_list[key] = pour_value
#             global_dep_index.append(key)
#         else:
#             print("{} is in global index".format(key))
#     return value_list


# values = process_edges(values)
# min_index = np.argmin(values)
# print("min index: {}; min value: {}".format(min_index, values[min_index]))
 
# while True:
#     if min_index > 0 and min_index < len(values) - 1 :
#         if values[min_index - 1] >= values[min_index] and values[min_index + 1] >= values[min_index]:
#             dep_dict, pour_value = find_depression(values, min_index)
#             values = fill_depression(values, dep_dict, pour_value)
#             print(values[min_index])
#             print("min_index: {}; pour value: {}".format(min_index, pour_value))
#             print("min index: {}; min value: {}".format(min_index, values[min_index]))
#             min_index = np.argmin(values)

#     else:
#         break
#     # elif min_index == 0:
#     #     global_dep_index.append(min_index)
#     #     values[min_index] = values[min_index + 1]
#     #     min_index = np.argmin(values[1:])
#     # elif min_index == size - 1:
#     #     global_dep_index.append(min_index)
#     #     values[min_index] = values[min_index - 1]
#     #     min_index = np.argmin(values[(size - 1):])



            



# # print(min_index)
# # dep_dict, pour_value = find_depression(values, min_index)

# # fill_depression(values, dep_dict, pour_value)
# # dep_dict, pour_value = find_depression(values, np.argmin(values))
# # fill_depression(values, dep_dict, pour_value)

header = lines[0].strip() + ", FILLED, LEVEL-1\n"
lines.pop(0)
out_lines = []

for index,  line in enumerate(lines):
    line = line.strip()
    line = line + ',' + str(new_values[index]) + ',' + str(level1_values[index]) + '\n'
    out_lines.append(line)

# print(out_lines)

with open(out_csv, 'w') as f:
    f.write(header)
    f.writelines(out_lines)