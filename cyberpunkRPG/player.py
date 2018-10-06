# -*- encoding: utf-8 -*-
import json, math
from pathlib import Path
from .bag import Bag

statNames = ['INT','RIF','TEC','FRE','FAS','FOR','MOV','COS','EMP']

class Player:	
	_statusList = [
		'Lieve',
		'Grave',
		'Critico',
		'Mortale 0',
		'Mortale 1',
		'Mortale 2',
		'Mortale 3',
		'Mortale 4',
		'Mortale 5',
		'Mortale 6',
		'Deceduto'
	]
	_statBase = {
		'INT' : 0,
		'RIF' : 0,
		'TEC' : 0,
		'FRE' : 0,
		'FAS' : 0,
		'FOR' : 0,
		'MOV' : 0,
		'COS' : 0,
		'EMP' : 0
	}
	_initDebuff = {
		'INT' : 0,
		'RIF' : 0,
		'TEC' : 0,
		'FRE' : 0,
		'FAS' : 0,
		'FOR' : 0,
		'MOV' : 0,
		'COS' : 0,
		'EMP' : 0
	}

	def __init__(self, name):
		self.name = name
		if Path('players/' + self.name + '.json').is_file():
			self.loadFromJson()
		else:
			self.malus = 0
			self.stat = self._statBase
			self.debuff = self._initDebuff
			self.bag = Bag()
			self.saveToJson()

	def hurt(self, point):
		if point > 0:
			newMalus = self.malus + point
			if newMalus <= 41:
				self.malus = newMalus
			else:
				self.malus = 41
		self.saveToJson()

	def heal(self, point):
		if point > 0:
			newMalus = self.malus - point
			self.malus = 0 if newMalus < 0 else newMalus
			self.saveToJson()

	def getStatus(self):
		if self.malus > 0:
			return self._statusList[math.floor((self.malus -1) / 4)] + '[' + str(self.malus) + ']'
		else:
			return 'in salute[0]'

	def getStat(self, statName):
		return self.stat[statName] - self.debuff[statName]

	def resetDebuff(self, stat = 'ALL'):
		if stat == 'ALL':
			self.debuff = self._initDebuff
			#? CONTROLLARE SE PYTHON PASSA GLI OGGETTI PER VALORE O PER RIFERIMENTO
			#? NON SI POSSONO MODIFICARE GLI ATTRIBUTI CHE INIZIANO PER '_' (SONO COSTANTI PRIVATE)

	def humanity(self):
		base = self.stat['EMP'] * 10
		lost = 0
		for item in self.bag.content:
			if item['cyber']:
				lost += item['hu']
		newhu = base - lost
		return 0 if newhu < 0 else newhu

	def run(self):
		return self.stat['MOV'] * 3

	def loadFromJson(self):
		with open('players/' + self.name + '.json', 'r') as f:
			data = json.load(f)
			self.malus = data['malus']
			self.stat = data['stat']
			self.debuff = data['debuff']
			self.bag = Bag(data['bag'])

	def saveToJson(self):
		with open('players/' + self.name + '.json', 'w') as f:
			f.write(json.dumps({
				"malus": self.malus,
				"stat": self.stat,
				"debuff": self.debuff,
				"bag": self.bag.content
			}, indent=4, sort_keys=False))

	def info(self):
		text = []

		t = PrettyTable(['INFO','PERSONAGGIO'])
		t.add_row(['Nome', self.name])
		t.add_row(['Stato', self.getStatus()])
		t.add_row(['umanità', self.humanity()])
		text.append(t.get_string())

		t = PrettyTable(['Stat', 'Valore'])
		for name in statNames:
			t.add_row([name, str(self.stat[name]) + '' if self.debuff[name] == 0 else ' [-' + str(self.debuff[name]) + ']' ])
		t.add_row(['Corsa', self.run()])
		text.append(t.get_string())

		return '\n'.join(str(x) for x in text)