def collatz(number):
	if number % 2 == 0:
		print(number // 2)
		return number // 2
	else:
		print(3 * number + 1)
		return 3 * number + 1

# Use collatz sequence to eventually reach 1
print('Enter a number:')
try:
	num = int(input())
except ValueError:
	print('Enter a integer:')
	num = int(input())

while num != 1:
	try:
		num = collatz(num)
	except ValueError:
		print('Please enter a number')