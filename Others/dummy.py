from werkzeug.security import generate_password_hash
import random

# Some common Indian first names
names = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Krishna", "Ishaan", "Shaurya",
    "Ananya", "Diya", "Aadhya", "Pari", "Avni", "Anika", "Navya", "Myra", "Ira", "Kiara",
    "Lakshmi", "Priya", "Rani", "Kavya", "Pooja", "Sneha", "Nisha", "Radha", "Divya", "Meera",
    "Rahul", "Amit", "Suresh", "Ramesh", "Vijay", "Karthik", "Sanjay", "Deepak", "Manoj", "Arvind",
    "Sunita", "Geeta", "Seema", "Lata", "Rekha", "Neha", "Shreya", "Aarti", "Payal", "Jyoti"
    "Ram","Admin","Murugan","Chandran","Devika","Lakshmi"
]

# Sample addresses in Indian cities
addresses = [
    "156, 5th Cross Road, Goregaon West, Mumbai",
    "22, MG Road, Indiranagar, Bangalore",
    "47, Park Street, Kolkata",
    "89, Anna Salai, Teynampet, Chennai",
    "12, Connaught Place, New Delhi",
    "78, Sector 18, Noida",
    "34, Baner Road, Pune",
    "56, Banjara Hills, Hyderabad",
    "9, Civil Lines, Jaipur",
    "44, Lalbagh Road, Lucknow"
]

users = []
for i in range(50):
    name = random.choice(names)
    email = f"{name.lower()}{i}@example.com"
    password = generate_password_hash(f"{name.lower()}123")
    mobile = "".join([str(random.randint(6, 9))] + [str(random.randint(0, 9)) for _ in range(9)])
    address = random.choice(addresses)
    users.append({
        "name": name,
        "email": email,
        "password": password,
        "is_admin": False,
        "mobile": mobile,
        "role": "user",
        "address": address
    })

# Print the list (you can also insert into DB or export as JSON)
for u in users:
    print(u)
