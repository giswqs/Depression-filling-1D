import os
import csv

csv_dir = os.path.join(os.path.dirname(__file__), 'data')

in_csv = os.path.join(csv_dir, 'profile1.csv')
out_csv = in_csv.replace('.csv', '_new.csv')
print(out_csv)

lines = []
values = []

with open(in_csv) as f:
    lines = f.readlines()
    for index, line in enumerate(lines):
        if index > 0:
            # print(index)
            line = line.strip()
            value = line.split(",")[-1]
            values.append(float(value))
            # print(value)

size = len(values)
print("Total number of lines: {}".format(size))

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

# print(len(new_values))

header = lines[0].strip() + ", FILLED\n"
lines.pop(0)
out_lines = []

for index,  line in enumerate(lines):
    line = line.strip()
    line = line + ',' + str(new_values[index]) + '\n'
    out_lines.append(line)

# print(out_lines)

with open(out_csv, 'w') as f:
    f.write(header)
    f.writelines(out_lines)
