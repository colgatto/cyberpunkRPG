# -*- encoding: utf-8 -*-
from pathlib import Path
from prettytable import PrettyTable
from .items import Item

class Bag:
	def __init__(self, content = []):
		self.content = []
		for item in content:
			self.content.append(Item(item['name'], item['qnt'], item['value'], item['weight'], item['type']))

	def getWeight(self):
		size = 0
		for item in self.content:
			size += item.fullWeight()
		return size

	def insert(self, item):
		if isinstance(item, Item):
			it = self.contain(item)
			if it == False:
				self.content.append(item)
				return True
			else:
				it.add(item.qnt)
				return True
		return False

	def contain(self, searched):
		if isinstance(searched, Item):
			for bagItem in self.content:
				if bagItem == searched:
					return bagItem
		elif isinstance(searched, str):
			for bagItem in self.content:
				if bagItem.name == searched:
					return bagItem
		return False

	def getItemsByName(self, name):
		founds = []
		for item in self.content:
			if item.name == name:
				founds.append(item)
		return founds

	def remove(self,name,qnt):
		for item in self.content:
			if item.name == name:
				if qnt <= item.qnt:
					item.qnt -= qnt
					return 1
				return -1
		return 0

	_headerListedLabel = ['Nome', 'Tipo', 'Quantità', 'Peso', 'Valore']

	def generateListedRow(self, item):
		return [item.name, item.type, item.qnt, str(item.weight) + '[' + str(item.fullWeight()) + ']', str(item.value) + '[' + str(item.fullValue()) + ']']

	def listed(self, sortby="Nome", desc=False):
		t = PrettyTable(self._headerListedLabel)
		for item in self.content:
			t.add_row(self.generateListedRow(item))
		return t.get_string(sortby=sortby, reversesort=desc)

	def __str__(self):
		return self.listed()

	def getDict(self):
		ret = []
		for item in self.content:
			ret.append(item.getDict())
		return ret

class CyberParts(Bag):

	_headerListedLabel = ['Nome', 'Valore', 'HU']
	
	def __init__(self, content = []):
		Bag.__init__(self, content)

	def generateListedRow(self, item):
		return [item.name, item.value, item.hu]

	def humanityLost(self):
		tot = 0
		for item in self.content:
			tot += item.hu
		return tot