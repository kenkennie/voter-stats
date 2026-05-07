import pandas as pd
import random

random.seed(42)

# Kenyan counties with constituencies and wards
kenya_data = {
    "Nairobi": {
        "Westlands": ["Kangemi", "Mountain View", "Westlands", "Parklands", "Kitisuru"],
        "Embakasi East": ["Utawala", "Mihango", "Upper Savanna", "Lower Savanna", "Embakasi"],
        "Dagoretti North": ["Riruta", "Uthiru", "Ruthimitu", "Gitaru", "Kabiro"],
    },
    "Mombasa": {
        "Mvita": ["Mji wa Kale", "Tudor", "Tononoka", "Shimanzi", "Ganjoni"],
        "Likoni": ["Mtongwe", "Shika Adabu", "Bofu", "Likoni", "Timbwani"],
    },
    "Kisumu": {
        "Kisumu Central": ["Shaurimoyo", "Market Milimani", "Railways", "Migosi", "Kondele"],
        "Kisumu East": ["Kajulu", "Kolwa East", "Manyatta B", "Nyalenda A", "Nyalenda B"],
    },
    "Nakuru": {
        "Nakuru Town East": ["Biashara", "Kivumbini", "Flamingo", "Menengai", "Nakuru East"],
        "Rongai": ["Soin", "Visoi", "Menengai West", "Mosop", "Solai"],
    },
    "Kiambu": {
        "Thika Town": ["Township", "Kamenu", "Hospital", "Gatuanyaga", "Ngoliba"],
        "Ruiru": ["Gitothua", "Biashara", "Gatongora", "Kahawa Sukari", "Kahawa Wendani"],
    },
    "Meru": {
        "Imenti North": ["Municipality", "Ntima East", "Ntima West", "Nyaki West", "Nyaki East"],
        "Igembe South": ["Maua", "Nyambene Hills", "Athiru Gaiti", "Igembe East", "Athiru Rujiine"],
    },
    "Machakos": {
        "Machakos Town": ["Mutituni", "Machakos Central", "Mua", "Milimani", "Kalama"],
        "Mavoko": ["Syokimau", "Mlolongo", "Athi River", "Kinanie", "Muthwani"],
    },
    "Eldoret": {
        "Turbo": ["Turbo", "Eldoret East", "Lemook", "Ng'Arua", "Ngenyilel"],
        "Kapseret": ["Simat", "Megun", "Kipkenyo", "Ngeria", "Langas"],
    },
}

# First names pool (Kenyan)
first_names_male = [
    "Kamau", "Kipchoge", "Otieno", "Mwangi", "Njoroge", "Omondi", "Kariuki",
    "Waweru", "Mutua", "Ochieng", "Kimani", "Kiptoo", "Auma", "Odhiambo",
    "Ngugi", "Njenga", "Koech", "Cheruiyot", "Kipkoech", "Barasa",
    "Hassan", "Ahmed", "Omar", "Salim", "Rashid", "Hamisi", "Mwenda",
    "Maina", "Gitahi", "Thuo", "Muriithi", "Kinyanjui", "Gacheru",
]
first_names_female = [
    "Wanjiku", "Akinyi", "Fatuma", "Zawadi", "Atieno", "Adhiambo", "Nyambura",
    "Wambui", "Njeri", "Wairimu", "Kemunto", "Moraa", "Bosibori", "Kwamboka",
    "Mumbi", "Gathoni", "Waceera", "Nyaguthii", "Wangari", "Muthoni",
    "Halima", "Amina", "Zuhura", "Khadija", "Safia", "Rehema", "Mwanaidi",
    "Chebet", "Jepchirchir", "Rotich", "Jelimo", "Chepkoech",
]
last_names = [
    "Otieno", "Mwangi", "Odhiambo", "Kariuki", "Mutua", "Njoroge", "Kimani",
    "Omondi", "Waweru", "Ngugi", "Auma", "Ochieng", "Koech", "Cheruiyot",
    "Hassan", "Omar", "Salim", "Barasa", "Njenga", "Mwenda", "Gitahi",
    "Thuo", "Muriithi", "Kinyanjui", "Gacheru", "Ruto", "Kiptoo",
    "Moraa", "Bosibori", "Adhiambo", "Atieno", "Akinyi", "Jelimo",
]

occupations = [
    "Farmer", "Teacher", "Trader", "Nurse", "Driver", "Engineer",
    "Student", "Accountant", "Self-employed", "Casual Worker",
    "Police Officer", "Clerk", "Mechanic", "Tailor", "Shopkeeper",
]
statuses = ["Active", "Active", "Active", "Active", "Inactive", "Under Review"]
years = [2013, 2017, 2022, 2027]

records = []
id_pool = random.sample(range(10000000, 49999999), 600)

for i in range(600):
    gender = random.choice(["Male", "Female"])
    first = random.choice(first_names_male if gender == "Male" else first_names_female)
    last = random.choice(last_names)
    full_name = f"{first} {last}"

    county = random.choice(list(kenya_data.keys()))
    constituency = random.choice(list(kenya_data[county].keys()))
    ward = random.choice(kenya_data[county][constituency])

    age = random.randint(18, 85)
    year = random.choices(years, weights=[15, 25, 40, 20])[0]
    national_id = id_pool[i]
    polling_station = f"{ward} Primary School"
    occupation = random.choice(occupations)
    status = random.choices(statuses, weights=[70, 70, 70, 70, 10, 10])[0]
    sub_county = constituency  # simplified

    records.append({
        "full_name": full_name,
        "gender": gender,
        "age": age,
        "national_id": national_id,
        "county": county,
        "sub_county": sub_county,
        "constituency": constituency,
        "ward": ward,
        "polling_station": polling_station,
        "registration_year": year,
        "occupation": occupation,
        "voter_status": status,
    })

df = pd.DataFrame(records)
df.to_csv("voters.csv", index=False)
print(f"Done! Generated {len(df)} voter records -> voters.csv")
print(df.head(3).to_string())