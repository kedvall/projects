# InventoryAdd.py
def addToInventory(inventory, addedItems):
	for index in addedItems:
		if index in inventory.keys():
			inventory[index] += 1
		else:
			inventory[index] = 1
	return inventory

def displayInventory(inventory):
	total = 0
	print('Inventory:')
	for k, v in inventory.items():
		print(str(v) + ' ' + k)
		total += v
	print('Total number of items: ' + str(total))

inv = {'gold coin': 42, 'rope': 1}
dragonLoot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']
inv = addToInventory(inv, dragonLoot)

displayInventory(inv)