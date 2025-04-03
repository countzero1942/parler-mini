#!/usr/bin/env python3

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

# Parse the data
people = []
for line in data.strip().split('\n'):
    parts = line.split('\t')
    if len(parts) == 2:
        name, score = parts
        people.append({'name': name, 'score': float(score)})

# Since sex information is not provided, I'll make an assumption based on common names
# This is just for demonstration - in a real scenario, you'd want actual sex data
male_names = ['Jon', 'Gary', 'Mike', 'Will', 'Patrick', 'Eric', 'Rick']
female_names = ['Lea', 'Jenna', 'Laura', 'Lauren', 'Eileen', 'Alisa', 'Karen', 
                'Barbara', 'Carol', 'Emily', 'Rose', 'Anna', 'Tina']

# Create separate arrays for males and females
males = [person for person in people if person['name'] in male_names]
females = [person for person in people if person['name'] in female_names]

# Sort each array by score (highest to lowest)
males.sort(key=lambda x: x['score'], reverse=True)
females.sort(key=lambda x: x['score'], reverse=True)

def clamp(i, min, max):
    return max(min, min(i, max))

def get_female(i):
    i = clamp(i, 0, len(females) - 1)
    return females[i]['name']

def get_male(i):
    i = clamp(i, 0, len(males) - 1)
    return males[i]['name']


def print_names():
    print("Male array:")
    for i, person in enumerate(males):
        print(f"[{i}] {person['name']}: {person['score']}")

    print("\nFemale array:")
    for i, person in enumerate(females):
        print(f"[{i}] {person['name']}: {person['score']}")
