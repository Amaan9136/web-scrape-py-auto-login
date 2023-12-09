import itertools

keywords = ["i88888", "dananjay", "kumar", "88888", "rite", "app","7", "appu", "kumar", "88888", "rite", "app"]

# Function to generate all combinations of keywords with and without spaces
def generate_combinations(keywords):
    all_combinations = []
    for r in range(1, len(keywords) + 1):
        combinations = itertools.combinations(keywords, r)
        for combo in combinations:
            with_spaces = " ".join(combo)
            without_spaces = "".join(combo)
            all_combinations.extend([with_spaces, without_spaces])
    return all_combinations

# Generate and print all possible combinations
all_possible_combinations = generate_combinations(keywords)

# Create a set of credentials using the mobile number and keyword combinations
mobile = "7562879235"
credentials = [(mobile, combo) for combo in all_possible_combinations]

# Read existing keyword combinations from the file
existing_combinations = set()
with open("common-codes\password_combinations.txt", "r") as file:
    lines = file.read().splitlines()
    existing_combinations = set(lines)

# Filter out repeated keyword combinations
filtered_credentials = [(mobile, password) for password in all_possible_combinations if password not in existing_combinations]

# Write the filtered keyword combinations to a text file
with open("common-codes\password_combinations.txt", "a") as file:
    # Write a marker to separate old and new combinations
    for mobile, password in filtered_credentials:
        file.write(password + "\n")

print("Filtered Keyword combinations with and without spaces written to 'common-codes\password_combinations.txt'")

count=0
for i in range(len(filtered_credentials)):
    print("credentials =", filtered_credentials[i],"\n")
    count+=1
print(count,"Credentials Added!")
