#!/usr/bin/env python3
from names import Sex, Person, people, clamp


def test_clamp():
	"""Test the clamp function."""
	# Rename the parameters to avoid conflict with built-in min/max
	assert clamp(5, 0, 10) == 5
	assert clamp(-5, 0, 10) == 0
	assert clamp(15, 0, 10) == 10


def test_person_creation():
	"""Test Person class initialization."""
	# Test with explicit sex
	person1 = Person('TestName', 0.5, Sex.Male)
	assert person1.name == 'TestName'
	assert person1.score == 0.5
	assert person1.sex == Sex.Male

	# Test with implicit sex determination
	person2 = Person('Jon', 0.9, None)
	assert person2.sex == Sex.Male

	person3 = Person('Laura', 0.8, None)
	assert person3.sex == Sex.Female

	# Test with unknown name
	person4 = Person('Unknown', 0.7, None)
	assert person4.sex == Sex.Either


def test_people_initialization():
	"""Test People class initialization."""

	# Check if people lists are created
	assert isinstance(people.people, list)
	assert isinstance(people.males, list)
	assert isinstance(people.females, list)

	# Check if dictionaries are created
	assert isinstance(people.people_dict, dict)
	assert isinstance(people.male_dict, dict)
	assert isinstance(people.female_dict, dict)


def test_get_names_by_sex():
	"""Test getNamesBySex method."""
	male_names = people.getNamesBySex(Sex.Male)
	female_names = people.getNamesBySex(Sex.Female)
	all_names = people.getNamesBySex(Sex.Either)

	# Check if the lists contain names
	assert len(male_names) > 0
	assert len(female_names) > 0
	assert len(all_names) > 0

	# Check if male and female names are subsets of all names
	assert set(male_names).issubset(set(all_names))
	assert set(female_names).issubset(set(all_names))


def test_get_person_by_index():
	"""Test getPersonByIndex method."""
	# Test valid indices
	male = people.getPersonByIndex(0, Sex.Male)
	assert male.sex == Sex.Male

	female = people.getPersonByIndex(0, Sex.Female)
	assert female.sex == Sex.Female

	# Test out of bounds indices
	male_oob = people.getPersonByIndex(999, Sex.Male)
	assert male_oob.sex == Sex.Male

	# Test negative indices
	default_male = people.getPersonByIndex(-1, Sex.Male)
	assert default_male.name == 'A male'


def test_coerce_person():
	"""Test coercePerson method."""
	# Test existing names with score
	jon = people.coercePerson('Jon', Sex.Male)
	assert jon.name == 'Jon'
	assert jon.sex == Sex.Male

	lea = people.coercePerson('Lea', Sex.Female)
	assert lea.name == 'Lea'
	assert lea.sex == Sex.Female

	# Test existing names without score
	scorelessFemalePerson = [p for p in people.females if p.score is None][0]
	scorelessFemale = people.coercePerson(
		scorelessFemalePerson.name, Sex.Female
	)
	assert scorelessFemale.name == scorelessFemalePerson.name
	assert scorelessFemale.sex == Sex.Female

	scorelessMalePerson = [p for p in people.males if p.score is None][0]
	scorelessMale = people.coercePerson(scorelessMalePerson.name, Sex.Male)
	assert scorelessMale.name == scorelessMalePerson.name
	assert scorelessMale.sex == Sex.Male

	# Test non-existing names
	default_female = people.coercePerson('NonExistentName', Sex.Female)
	assert default_female.name == 'A female'
	assert default_female.sex == Sex.Female

	default_male = people.coercePerson('NonExistentName', Sex.Male)
	assert default_male.name == 'A male'
	assert default_male.sex == Sex.Male

	default_either = people.coercePerson('NonExistentName', Sex.Either)
	assert default_either.name == 'A person'
	assert default_either.sex == Sex.Either
