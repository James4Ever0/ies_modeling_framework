with open(BASHRC:= "/root/.bashrc",'r') as f:
    lines = f.read().split("\n")

uncomment = lambda l: l.split("#")[-1]
flag = False

new_lines = []
for line in lines:
    if not flag:
        if "mamba initialize" in line:
        # if "conda initialize" in line:
            flag = True
        
    if flag:
        line = uncomment(line)
    new_lines.append(line)

with open(BASHRC, 'w+') as f:
    f.write("\n".join(new_lines))