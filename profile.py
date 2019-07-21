import os
import numpy as np


# class for depression
class Depression:
    def __init__(self, id, width, depth, area, pour_elev, min_elev, points, internal_pts):
        self.id = id
        self.width = width
        self.depth = depth
        self.area = area
        self.pour_elev = pour_elev
        self.min_elev = min_elev
        self.points = points
        self.internal_pts = internal_pts 


# read profile values from CSV
def read_csv(in_csv, header = True, col_index = 1):
    with open(in_csv) as f:
        lines = f.readlines()
        if header:
            lines = lines[1:]

        values = []
        for line in lines:
            line = line.strip()
            value = line.split(",")[col_index - 1]
            values.append(float(value))
    
    return values


def write_csv(in_csv, out_csv, col_name, in_values):
    with open(in_csv) as f:
        lines = f.readlines()
        header = lines[0].strip() + "," + col_name + '\n'
        lines.pop(0)
        out_lines = []

        for index,  line in enumerate(lines):
            line = line.strip()
            line = line + ',' + str(in_values[index]) +'\n'
            out_lines.append(line)

        with open(out_csv, 'w') as ff:
            ff.write(header)
            ff.writelines(out_lines)


# check the depression type of a point based on its neighbors
def check_dep_type(value_list, index):
    if index == 0:
        if value_list[0] <= value_list[1]:
            return 'ascending'
        else:
            return 'descending'
    elif index == (len(value_list) - 1):
        if value_list[len(value_list) - 2] >= value_list[len(value_list) - 1]:
            return 'descending'
        else:
            return 'ascending'
    else:
        if (value_list[index] == value_list[index - 1]) and (value_list[index]) == value_list[index + 1]:
            return 'flat'
        elif (value_list[index] <= value_list[index - 1]) and (value_list[index]) <= value_list[index + 1]:
            return 'depression'
        elif (value_list[index] > value_list[index - 1]) and (value_list[index] < value_list[index + 1]):
            return 'ascending'
        elif (value_list[index] > value_list[index + 1]) and (value_list[index] < value_list[index - 1]):
            return 'descending' 
        else:
            return 'unknown'

# find forward ascending neighbors
def find_ascending(value_list, index):
    ascending_loc = []
    cursor = index
    while (cursor < (len(value_list) - 1 )) and (value_list[cursor] < value_list[cursor + 1]):
        ascending_loc.append(cursor)
        cursor = cursor + 1
    ascending_loc.append(cursor)
    # print(ascending_loc)
    return set(ascending_loc)
 

# find forward descending neighbors
def find_descending(value_list, index):
    descending_loc = []
    cursor = index
    while (cursor < (len(value_list) - 1 )) and (value_list[cursor] > value_list[cursor + 1]):
        descending_loc.append(cursor)
        cursor = cursor + 1
    descending_loc.append(cursor)
    return set(descending_loc)


# find backward descending neighbors
def find_descending_backward(value_list, index):
    descending_loc = []
    cursor = index
    while (cursor > 0) and (value_list[cursor] < value_list[cursor - 1]):
        descending_loc.append(cursor)
        cursor = cursor - 1
    descending_loc.append(cursor)
    return set(descending_loc[::-1])

# find all points associated with a depression based on one point
def find_single_depression(value_list, index):
    dep_loc = []
    ascending_loc = list(find_ascending(value_list, index))
    # ascending_loc = ascending_loc.sort()
    # print(ascending_loc.sort())
    descending_loc = list(find_descending_backward(value_list, index))
    dep_loc = descending_loc + ascending_loc
    return set(dep_loc)

# remove acending edge and descending edge
def process_edges(value_list):
    size = len(value_list)
    pts_list = set(range(size))
    left_edge = find_ascending(value_list, 0)
    if len(left_edge) > 0:
        for item in left_edge:
            pts_list.remove(item)

    right_edge = find_descending_backward(value_list, size - 1)
    if len(right_edge) > 0:
        for item in right_edge:
            pts_list.remove(item)
    return pts_list


# get depression width, height, and area
def get_width_depth_area(value_list, pts_set):
    min_index = min(pts_set)
    max_index = max(pts_set)

    left_elev = value_list[min_index]
    right_elev = value_list[max_index]

    pts_list = list(pts_set)
    pts_arr = np.array(value_list)[pts_list]
    min_value = np.min(pts_arr)
    pour_value = min([left_elev, right_elev])
    depth = pour_value - min_value

    new_pts_arr = pts_arr[pts_arr <= pour_value]
    width = new_pts_arr.size
    area = pour_value * new_pts_arr.size - np.sum(new_pts_arr)

    new_pts_set = pts_set.copy()

    for item in pts_set:
        if value_list[item] > pour_value:
            new_pts_set.remove(item)

    return width, depth, area, pour_value, new_pts_set


# find all depressions recursively
def find_depressions(in_values, in_width = 0, in_depth = 0, in_area = 0, dep_list = []):
    size = len(in_values)
    global_set = process_edges(in_values)
    num_arr = np.array(in_values)
    # dep_list = []

    while len(global_set) > 0:
        # print("Remaining: {}".format(len(global_set)))
        # if len(global_set) == 2:
        #     print(global_set)
        tmp_arr = num_arr[list(global_set)]
        min_value = np.min(tmp_arr)
        min_candidates = list(np.where(num_arr == min_value)[0])
        min_index = min_candidates[0]

        if len(min_candidates) > 1:
            for item in min_candidates:
                items = [item - 1, item, item + 1]
                con = all(elem in items for elem in global_set)
                if con : 
                    min_index = item
                    break
                else:

                    ascending_loc_tmp = find_ascending(in_values, item)
                    descending_loc_tmp = find_descending_backward(in_values, item)
                    dep_loc_tmp = list(ascending_loc_tmp) + list(descending_loc_tmp)
                    max_value = np.max(num_arr[dep_loc_tmp])
                    num_arr[dep_loc_tmp] = max_value
                    for item in dep_loc_tmp:
                        if item in global_set:
                            global_set.remove(item)
                            min_index = -1

        elif len(global_set) < 3:
            global_set_tmp = global_set.copy()
            for item in global_set_tmp:
                global_set.remove(item)
            min_index = -1

        if min_index != -1:

            dep_index = find_single_depression(list(num_arr), min_index)
            # print(dep_index)

            width, depth, area, pour_elev, dep_tmp_set = get_width_depth_area(in_values, dep_index)

            # print(dep_tmp_set)
            # if len(dep_tmp_set) == 1:
            #     print('stop')
            #     print(pour_elev)

            if (width >= in_width) and (depth >= in_depth) and (area > in_area):
                print("************************************")
                print("depression loc: {}".format(dep_index))
                print("min candidates: {}".format(min_candidates))
                # print("Pour elevation: {}".format(pour_elev))
                print("width = {}; depth = {}; area = {}; pour = {}".format(width, round(depth, 2), round(area, 2), pour_elev))
                # dep_list.append(dep_index)
                id = len(dep_list) + 1
                dep_list.append(Depression(id, width, round(depth, 4), round(area, 4), pour_elev, min_value, dep_index, dep_tmp_set))
                for item in dep_index:
                    if item in global_set: 
                        global_set.remove(item)
            # elif len(dep_tmp_set) == 1:
            #     continue
            else:
                # print(dep_tmp_set)
                for item in dep_tmp_set:
                    num_arr[item] = pour_elev
                    global_set.add(item)
        
    # for dep in dep_list:
    #     print(dep)

    print("Number of depressions: {}".format(len(dep_list)))
    return dep_list


def fill_depressions(in_values, dep_list):
    for dep in dep_list:
        points = dep.points
        internal_pts = dep.internal_pts
        pour_elev = dep.pour_elev
        for point in internal_pts:
            in_values[point] = pour_elev
    return in_values


def get_hierarchy(in_csv, out_dir, width = 0, height = 0, area = 0):
    pass



if __name__ == '__main__':
    # ************************ change the following parameters if needed ******************************** #
    width = 0
    height = 0
    area = 0

    work_dir = os.path.dirname(__file__)
    in_csv = os.path.join(work_dir, 'data/profile1.csv')
    out_csv = in_csv.replace('.csv', '_level1.csv')


    values = read_csv(in_csv, header=True, col_index=4)
    size = len(values)
    print("Total number of rows: {}".format(size))

    dep_type = check_dep_type(values, 557)
    # print(dep_type)

    dep_pts = find_single_depression(values, index = 1087)
    # print(dep_pts)

    dep_list = find_depressions(values, in_width = 3, in_depth = 0)

    out_values = fill_depressions(values, dep_list)
    # print(out_values)

    write_csv(in_csv, out_csv, "LEVEL-1", out_values)

    # print(get_width_depth_area(values, dep_pts))

    # ************************************************************************************************** #