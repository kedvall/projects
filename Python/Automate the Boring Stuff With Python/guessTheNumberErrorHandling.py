# This is a guess the number game.
import random
secretNumber = random.randint(1, 20)
print('I am thinking of a number between 1 and 20.')

# Ask the player to guess 6 times.
for guessesTaken in range(1, 7):
	print('Take a guess.')
	try:
		guess = int(input())
	except ValueError:
		print('Please enter a number.')
		guess = int(input())

	if guess < secretNumber:
		print('Your guess is too low')
	elif guess > secretNumber:
		print('Your guess is too high')
	else:
		break #This condition is the correct guess!

if guess == secretNumber:
	print('Good job! You guessed the number in ' + str(guessesTaken) + ' guesses!')
else:
	print('Nope. The number I was thinking of was ' + str(secretNumber))