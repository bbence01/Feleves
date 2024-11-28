import matplotlib.pyplot as plt

genders = ['férfi', 'nő', 'nő', 'férfi', 'férfi', 'nő', 'nő', 'nő', 'nő', 'férfi', 'férfi', 'férfi', 'nő', 'férfi', 'férfi']
gender_counts = {'férfi': genders.count('férfi'), 'nő': genders.count('nő')}

languages = {
    'magyar': 23.3,
    'német': 34.5,
    'holland': 2.1,
    'angol': 1.0,
    'egyéb': 39.1
}

plt.figure(figsize=(8, 5))
plt.bar(gender_counts.keys(), gender_counts.values())
plt.title("Nemek Megoszlása")
plt.xlabel("Nemek")
plt.ylabel("Darabszám")
plt.show()

plt.figure(figsize=(8, 8))
plt.pie(languages.values(), labels=languages.keys(), autopct='%1.1f%%', startangle=140)
plt.title("Nyelvi Megoszlás")
plt.show()
