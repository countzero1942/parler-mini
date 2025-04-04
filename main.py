#!/usr/bin/env python3
import names
from generate_voices import generateAllVoices, generateVoice
from names import Sex


def main():
	prompt = "Hey! Are you feeling freaky today? I'm feeling freakin' freaky! Oh yeah!!"
	# generateAllVoices(prompt, sex=Sex.Female)
	generateVoice(prompt, names.people.getPersonByIndex(2, Sex.Female))

	names.people.printNames()


if __name__ == '__main__':
	main()
