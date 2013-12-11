

f = open('NomsDesRoms.txt')
lines = f.readlines()
str = ""
l = []
for i in range(1,len(lines)):
    str =  str + lines[i].split(' ')[3] + " \r"
print str
