import pandas

def fix_csv_and_return_dataframe(csv_path):

    lines = []
    line_sep_count_list = []
    with open(csv_path, "r") as f:
        for line in f.readlines():
            line_sep_count = line.count(",")
            if line_sep_count == 0:
                continue
            lines.append(line)
            line_sep_count_list.append(line_sep_count)

    line_sep_count_max = max(line_sep_count_list)
    for index, line_sep_count in enumerate(line_sep_count_list):
        lines[index] = lines[index].strip() + "," * (line_sep_count_max - line_sep_count)

    with open(csv_path, "w+") as f:
        for line in lines:
            f.write(line + "\n")

    df = pandas.read_csv(csv_path, header=None, on_bad_lines="warn")
    return df