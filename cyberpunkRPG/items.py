# -*- encoding: utf-8 -*-
class Item:
	def __init__(self, name, qnt=1, value=0, weight=0, type='general'):
		self.name = name
		self.value = value
		self.weight = weight
		self.qnt = qnt
		self.type = type

	def fullWeight(self):
		return self.weight * self.qnt

	def fullValue(self):
		return self.value * self.qnt

	def add(self, qnt):
		self.qnt += qnt

	def __eq__(self, other):
		if isinstance(other, Item):
			return self.name == other.name and self.value == other.value and self.weight == other.weight
		else:
			return False

	def __str__(self):
		return str(self.qnt) + ' ' + self.name

class CyberItem(Item):
	def __init__(self, name, value, hu=0):
		Item.__init__(self, name, 1, value, 0, 'cyber')
		self.hu = hu
