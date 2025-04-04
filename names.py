#!/usr/bin/env python3
from enum import Enum
from typing import Set, Dict


def clamp(i: int, min_val: int, max_val: int) -> int:
	return max(min_val, min(i, max_val))


# Data provided
data = """Jon	0.908301
Lea	0.904785
Gary	0.903516
Jenna	0.901807
Mike	0.885742
Laura	0.882666
Lauren	0.878320
Eileen	0.875635
Alisa	0.874219
Karen	0.872363
Barbara	0.871509
Carol	0.863623
Emily	0.854932
Rose	0.852246
Will	0.851074
Patrick	0.850977
Eric	0.845459
Rick	0.845020
Anna	0.844922
Tina	0.839160"""

allNames: Set[str] = {
	'Laura',
	'Gary',
	'Jon',
	'Lea',
	'Karen',
	'Rick',
	'Brenda',
	'David',
	'Eileen',
	'Jordan',
	'Mike',
	'Yann',
	'Joy',
	'James',
	'Eric',
	'Lauren',
	'Rose',
	'Will',
	'Jason',
	'Aaron',
	'Naomie',
	'Alisa',
	'Patrick',
	'Jerry',
	'Tina',
	'Jenna',
	'Bill',
	'Tom',
	'Carol',
	'Barbara',
	'Rebecca',
	'Anna',
	'Bruce',
	'Emily',
	'A female',
	'A male',
	'A person',
}

# Since sex information is not provided, I'll make an assumption based on common names
# This is just for demonstration - in a real scenario, you'd want actual sex data
maleNames: Set[str] = {
	'Jon',
	'Gary',
	'Mike',
	'Will',
	'Patrick',
	'Eric',
	'Rick',
	'David',
	'Jordan',
	'Yann',
	'James',
	'Jason',
	'Aaron',
	'Jerry',
	'Bill',
	'Tom',
	'Bruce',
	'A male',
}
femaleNames: Set[str] = {
	'Lea',
	'Jenna',
	'Laura',
	'Lauren',
	'Eileen',
	'Alisa',
	'Karen',
	'Barbara',
	'Carol',
	'Emily',
	'Rose',
	'Anna',
	'Tina',
	'Brenda',
	'Joy',
	'Naomie',
	'Rebecca',
	'A female',
}


defaultFemaleVoice: str = 'A female'
defaultMaleVoice: str = 'A male'
defaultEitherVoice: str = 'A person'


class Sex(Enum):
	Male = 'male'
	Female = 'female'
	Either = 'either'


class Person:
	def __init__(
		self,
		name: str,
		score: float | None,
		sex: Sex | None = None,
	):
		self.name = name
		self.score = score
		self.sex = (
			sex
			if sex is not None
			else Sex.Male
			if name in maleNames
			else Sex.Female
			if name in femaleNames
			else Sex.Either
		)


class People:
	def __init__(self):
		def createPeople() -> list[Person]:
			people: list[Person] = []
			peopleSet: Set[str] = set()
			for line in data.strip().split('\n'):
				parts = line.split('\t')
				if len(parts) == 2:
					name, score = parts
					people.append(
						Person(
							name,
							float(score),
						)
					)
					peopleSet.add(name)
			for name in allNames:
				if name not in peopleSet:
					people.append(Person(name, None))
			return people

		def createMales() -> list[Person]:
			males: list[Person] = [
				person for person in self.people if person.sex == Sex.Male
			]
			males.sort(
				key=lambda x: x.score or 0,
				reverse=True,
			)
			return males

		def createFemales() -> list[Person]:
			females: list[Person] = [
				person for person in self.people if person.sex == Sex.Female
			]
			females.sort(
				key=lambda x: x.score or 0,
				reverse=True,
			)
			return females

		def createPeopleDict() -> Dict[str, Person]:
			people_dict: Dict[str, Person] = {}
			for person in self.people:
				people_dict[person.name] = person
			return people_dict

		def createMaleDict() -> Dict[str, Person]:
			male_dict: Dict[str, Person] = {}
			for person in self.males:
				male_dict[person.name] = person
			return male_dict

		def createFemaleDict() -> Dict[str, Person]:
			female_dict: Dict[str, Person] = {}
			for person in self.females:
				female_dict[person.name] = person
			return female_dict

		self.people: list[Person] = createPeople()
		self.males: list[Person] = createMales()
		self.females: list[Person] = createFemales()
		self.people_dict: Dict[str, Person] = createPeopleDict()
		self.male_dict: Dict[str, Person] = createMaleDict()
		self.female_dict: Dict[str, Person] = createFemaleDict()

	def coercePerson(self, name: str, sex: Sex) -> Person:
		match sex:
			case Sex.Male:
				if name in self.male_dict:
					return self.male_dict[name]
				return self.male_dict[defaultMaleVoice]
			case Sex.Female:
				if name in self.female_dict:
					return self.female_dict[name]
				return self.female_dict[defaultFemaleVoice]
			case Sex.Either:
				if name in self.people_dict:
					return self.people_dict[name]
				return self.people_dict[defaultEitherVoice]

	def getPersonByIndex(self, i: int, sex: Sex) -> Person:
		match sex:
			case Sex.Female:
				if i < 0:
					return self.female_dict[defaultFemaleVoice]
				i = clamp(
					i,
					0,
					len(self.females) - 1,
				)
				return self.females[i]
			case Sex.Male:
				if i < 0:
					return self.male_dict[defaultMaleVoice]
				i = clamp(
					i,
					0,
					len(self.males) - 1,
				)
				return self.males[i]
			case Sex.Either:
				if i < 0:
					return self.people_dict[defaultEitherVoice]
				i = clamp(
					i,
					0,
					len(self.people) - 1,
				)
				return self.people[i]

	def getNamesBySex(self, sex: Sex) -> list[str]:
		match sex:
			case Sex.Female:
				return [person.name for person in self.females]
			case Sex.Male:
				return [person.name for person in self.males]
			case Sex.Either:
				return [person.name for person in self.people]

	def printNames(self) -> None:
		print('Male array:')
		for i, person in enumerate(self.males):
			print(f'[{i}] {person.name}: {person.score}')

		print('\nFemale array:')
		for i, person in enumerate(self.females):
			print(f'[{i}] {person.name}: {person.score}')


people = People()
