# A class groups similar functions and variables together
class Enemy:
	life = 3

	def attack(self):
		print('ouch!')
		self.life -= 1

	def checkLife(self):
		if self.life <= 0:
			print('I am dead')
		else:
			print(str(self.life) + " life left")

# An object is a way to access things inside a class
enemy1 = Enemy()
enemy2 = Enemy()

# Got to class enemy and use the function attack
enemy1.attack()
enemy1.attack()
enemy1.checkLife()

enemy2.checkLife()