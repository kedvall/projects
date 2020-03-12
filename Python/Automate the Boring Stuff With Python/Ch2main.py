name = 'Kan'
print('Enter password')
password = input()
if name == 'Kan':
	print('Hello, Kan')
	if password == 'abc123':
		print('Access granted')
	elif password == '12345':
		print('An idiot uses that on their luggage')
	else:
		print('Wrong password')