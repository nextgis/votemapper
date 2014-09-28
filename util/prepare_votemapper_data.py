# -*- encoding: utf-8 -*-
# Prepare vote-data from CIK for VoteMapper
# Data will be put here: ./level1.csv, level2.csv etc...
# example: python prepare_votemapper_data.py

import csv


def load_codes(maxlevel):
    codes = []

    for i in range(0,maxlevel+1):
        coder_name = "level" + str(i) + "_codes.csv"
        coder_data = [row for row in csv.reader(open(coder_name))]
        codes.append(coder_data)

    return codes

def load_uiks(csv_path):
    uiks = []

    f_uiks = csv.reader(open(csv_path))
    for uik in f_uiks:
        uiks.append([uik[3],uik[1],uik[2]])

    return uiks

def generate_ids(level,atds):

    parent_id = ''
    cur_id = ''
    for i in range(0,level):
        parent_id = parent_id + find_code(i,atds[i])
        
    for i in range(0,level+1):
        cur_id = cur_id + find_code(i,atds[i])

    return cur_id,parent_id

def get_uik_coords(uik,atd):
    code = find_code(maxlevel,atd)
    res = filter(lambda item: item[0] == code, uiks)
    y = res[0][1]
    x = res[0][2]

    return x,y

def find_code(level,atd):
    res = filter(lambda item: item[0] == atd, codes[level])
    code = res[0][1]

    return code

def find_name(level,atd):
    res = filter(lambda item: item[0] == atd, codes[level])
    name = res[0][0]

    return name

if __name__ == '__main__':

    f = open("data.csv")
    data_csv = csv.reader(f)
    maxlevel = 3
    codes = load_codes(maxlevel)
    uiks = load_uiks('../uikgeo/77.csv')

    fn_arr = []
    for i in range(1,maxlevel+1):
        fname = "level" + str(i) + ".csv"
        fn_arr.append(csv.writer(open(fname,'wb')))

    for row in data_csv:
        #new_row = filter(None,row)
        vals = row[maxlevel+2:]
        level = int(row[maxlevel+1])
        atds = row[0:maxlevel+1]

        cur_id,parent_id = generate_ids(level,atds)
        name = find_name(level,atds[level])
        if level == maxlevel:
            x,y = get_uik_coords(uiks, atds[level])

        new_row = []
        new_row.append(cur_id)
        new_row.append(parent_id)
        new_row.append(name)

        if level == maxlevel:
            new_row.append(x)
            new_row.append(y)   
        new_row.extend(vals)

        fn_arr[int(row[maxlevel+1])-1].writerow(new_row)

