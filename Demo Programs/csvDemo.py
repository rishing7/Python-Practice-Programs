with open("file.csv", 'r') as f: # file.csv is input file
    with open("temp.csv", '') as t: # temp1.csv is output file
        for lines in f:
            new_line = lines.replace(",", " ")
            t.write(new_line)