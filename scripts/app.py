
# Step 1: Create a list of 8 people

people = [
    {"name": "John", "height": 1.80, "weight": 85},
    {"name": "Maria", "height": 1.65, "weight": 60},
    {"name": "Carlos", "height": 1.75, "weight": 95},
    {"name": "Anna", "height": 1.70, "weight": 55},
    {"name": "David", "height": 1.90, "weight": 110},
    {"name": "Sofia", "height": 1.60, "weight": 70},
    {"name": "James", "height": 1.85, "weight": 65},
    {"name": "Emma", "height": 1.68, "weight": 90}
]


# BMI Functions

def compute_bmi(height, weight):
    bmi = weight / (height * height)
    return bmi


def classify_bmi(bmi):
    if bmi >= 30:
        return "Obese"
    elif bmi >= 25:
        return "Overweight"
    elif bmi >= 18.5:
        return "Normal"
    else:
        return "Underweight"


# Step 2: Print each person

for person in people:
    print(person)

# person is one dictionary from the list
# person["height"] works
# people["height"] does not work because people is a list


# Step 3: Print name and BMI category

for person in people:
    bmi = compute_bmi(person["height"], person["weight"])
    category = classify_bmi(bmi)

    print(person["name"], category)


# Step 4: Count categories and find highest BMI

counts = {
    "Underweight": 0,
    "Normal": 0,
    "Overweight": 0,
    "Obese": 0
}

highest_bmi = 0
highest_person = ""

for person in people:
    bmi = compute_bmi(person["height"], person["weight"])
    category = classify_bmi(bmi)

    counts[category] = counts[category] + 1

    if bmi > highest_bmi:
        highest_bmi = bmi
        highest_person = person["name"]

print("BMI Category Counts:")
print(counts)

print("Total people:", len(people))
print("Total counted:", sum(counts.values()))

print("Person with highest BMI:", highest_person)
print("Highest BMI:", round(highest_bmi, 2))
