import re


text = '''matn @inerpfnergpe 
werwrwerwerwerwer
werwerwerwerwe
@woe
'''



res = re.findall(r'^(.+)\s\@',string = text,flags=re.S)


print(res[0])