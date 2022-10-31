from hashlib import md5

url = 'D:/MyQQ/MyQQ/MyQQ/bin/MyQQApi.dll'

file = open(url, 'rb')
fileContent = file.read()

m = md5()
m.update(fileContent)

hashStr = m.hexdigest()

print(hashStr)