

bmi = 27

def classify_bmi(bmi):
    if bmi >= 30:
        return "Obese"
    elif bmi >= 25:
        return "Overweight"
    elif bmi >= 18.5:
        return "Normal"
    else:
        return "Underweight"

print(classify_bmi(bmi))

best_value = 18
result = classify_bmi(best_value)
print(f"Your category is: {result}")

# 4 calculating bmi


bmi = 27

# Step 3: Classify BMI
def classify_bmi(bmi):
    if bmi >= 30:
        return "Obese"
    elif bmi >= 25:
        return "Overweight"
    elif bmi >= 18.5:
        return "Normal"
    else:
        return "Underweight"

print(classify_bmi(bmi))

# Step 4: Calculate BMI


def compute_bmi(height, weight):
    bmi = weight / (height * height)
    return bmi

height = 1.85
weight = 90

bmi = compute_bmi(height, weight)

print(bmi)
print(classify_bmi(bmi))


# Step 5: Create main function

def main():
    height = float(input("Enter your height in meters: "))
    weight = float(input("Enter your weight in kilograms: "))

    bmi = compute_bmi(height, weight)
    category = classify_bmi(bmi)

    print(f"Your BMI is: {bmi:.2f}")
    print(f"Your category is: {category}")

main()


