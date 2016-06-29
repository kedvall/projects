Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> spam = 'Hello world!'
>>> spam[0]
'H'
>>> spam[1]
'e'
>>> spam[0:5]
'Hello'
>>> spam[:5]
'Hello'
>>> spam[3:]
'lo world!'
>>> spam = '              Hello         '
>>> spam.strip
<built-in method strip of str object at 0x004BD598>
>>> spam.strip()
'Hello'
>>> spam.strip('')
'              Hello         '
>>> spam.strip()
'Hello'
>>> tableData = [['apples', 'oranges', 'cherries', 'banana'],
             ['Alice', 'Bob', 'Carol', 'David'],
             ['dogs', 'cats', 'moose', 'goose']]
... ... >>> 
>>> 
>>> for outerIndex in range(len(tableData)):
	print(outerIndex)
... ... 
0
1
2
>>> for outerIndex in range(len(tableData)):
	print('Outer: ' + outerIndex)
	for innerIndex in tableData[outerIndex]:
		print('Inner: ' + innerIndex)
... ... ... ... 
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
TypeError: Can't convert 'int' object to str implicitly
>>> for outerIndex in range(len(tableData)):
	print('Outer: ' + outerIndex)
	for innerIndex in tableData[outerIndex]:
		print('Inner: ' + str(innerIndex))
... ... ... ... 
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
TypeError: Can't convert 'int' object to str implicitly
>>> for outerIndex in range(len(tableData)):
	print('Outer: ' + str(outerIndex))
	for innerIndex in tableData[outerIndex]:
		print('Inner: ' + str(innerIndex))
... ... ... ... 
Outer: 0
Inner: apples
Inner: oranges
Inner: cherries
Inner: banana
Outer: 1
Inner: Alice
Inner: Bob
Inner: Carol
Inner: David
Outer: 2
Inner: dogs
Inner: cats
Inner: moose
Inner: goose
>>> for outerIndex in range(len(tableData)):
	print('Outer: ' + str(outerIndex))
	for innerIndex in len(tableData[outerIndex]):
		print('Inner: ' + str(innerIndex))
... ... ... ... 
Outer: 0
Traceback (most recent call last):
  File "<stdin>", line 3, in <module>
TypeError: 'int' object is not iterable
>>> for outerIndex in range(len(tableData)):
	print('Outer: ' + str(outerIndex))
	for innerIndex in range(len(tableData[outerIndex])):
		print('Inner: ' + str(innerIndex))
... ... ... ... 
Outer: 0
Inner: 0
Inner: 1
Inner: 2
Inner: 3
Outer: 1
Inner: 0
Inner: 1
Inner: 2
Inner: 3
Outer: 2
Inner: 0
Inner: 1
Inner: 2
Inner: 3
>>> 