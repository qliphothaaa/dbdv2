import sys

dic = {'a':234}
json = sys.argv[1]
a,b  = json.split(':')
dic[a] = b

#print(l_json)
#a,b = l_json
print(a)
print(b)
print(dic)
