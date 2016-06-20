while True:
	print('Who are you?')
	name = input()
	if name != 'Kan':
		continue
	print('Hello, Kanyon. What is the password (It is a fish.)')
	password = input()
	if password == 'swordfish':
		break
print('Access granted.')