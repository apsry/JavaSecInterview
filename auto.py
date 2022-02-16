# 自动更新数量统计
index = open("README.md", "r+", encoding="utf-8");
lines = index.readlines()

all = 0
all_index = 0
for i in range (0,len(lines)):
    if lines[i].startswith("["):
        line = lines[i]
        suffix = line.split("tree/master/")[1]
        suffix = suffix.split(")")[0]
        temp = open(suffix + "/" + "README.md", "r", encoding="utf-8")
        temp_lines = temp.readlines()
        total = 0
        for q in temp_lines:
            if q.startswith("###"):
                total = total + 1
        p = line.split("-")[0]
        s = line.split("个]")[1]
        all += total
        lines[i] = p + "- " + str(total) + "个]" + s
        print(suffix + ":" + str(total))
    if lines[i].startswith("当前问题总数"):
        all_index = i

print("total:" + str(all))
lines[all_index] = "当前问题总数："+ str(all) + "\n"
index.seek(0)
index.truncate()
index.writelines(lines)
