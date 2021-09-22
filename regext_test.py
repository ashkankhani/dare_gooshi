import re


text = '''matn
fnpwefwefwep powmpowef
'''

#main (.+)\s\@(.*)

res = re.findall(r'^(.+)\s\@(.*)',string = text,flags=re.S)


print(len(res))
