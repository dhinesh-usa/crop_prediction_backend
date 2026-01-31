"""
Indian Location Data - States, Districts, and Cities
"""

INDIAN_LOCATIONS = {
    "Maharashtra": {
        "Mumbai": ["Mumbai City", "Mumbai Suburban", "Thane", "Kalyan", "Navi Mumbai"],
        "Pune": ["Pune City", "Pimpri-Chinchwad", "Baramati", "Maval", "Haveli"],
        "Nashik": ["Nashik City", "Malegaon", "Sinnar", "Igatpuri", "Trimbakeshwar"],
        "Nagpur": ["Nagpur City", "Kamptee", "Katol", "Parseoni", "Narkhed"],
        "Aurangabad": ["Aurangabad City", "Jalna", "Beed", "Osmanabad", "Latur"]
    },
    "Karnataka": {
        "Bangalore Urban": ["Bangalore City", "Bangalore Rural", "Devanahalli", "Doddaballapur", "Hoskote"],
        "Mysore": ["Mysore City", "Mandya", "Chamarajanagar", "Hassan", "Kodagu"],
        "Hubli-Dharwad": ["Hubli", "Dharwad", "Gadag", "Haveri", "Ranebennur"],
        "Mangalore": ["Mangalore City", "Udupi", "Puttur", "Sullia", "Bantwal"],
        "Belgaum": ["Belgaum City", "Bagalkot", "Bijapur", "Gulbarga", "Raichur"]
    },
    "Tamil Nadu": {
        "Chennai": ["Chennai City", "Kanchipuram", "Tiruvallur", "Chengalpattu", "Tambaram"],
        "Coimbatore": ["Coimbatore City", "Tirupur", "Erode", "Salem", "Namakkal"],
        "Madurai": ["Madurai City", "Dindigul", "Theni", "Virudhunagar", "Sivaganga"],
        "Tiruchirappalli": ["Trichy City", "Thanjavur", "Tiruvarur", "Nagapattinam", "Mayiladuthurai"],
        "Tirunelveli": ["Tirunelveli City", "Thoothukudi", "Kanyakumari", "Ramanathapuram", "Tenkasi"]
    },
    "Gujarat": {
        "Ahmedabad": ["Ahmedabad City", "Gandhinagar", "Mehsana", "Patan", "Sabarkantha"],
        "Surat": ["Surat City", "Bharuch", "Narmada", "Tapi", "Navsari"],
        "Vadodara": ["Vadodara City", "Anand", "Kheda", "Panchmahal", "Dahod"],
        "Rajkot": ["Rajkot City", "Jamnagar", "Porbandar", "Junagadh", "Amreli"],
        "Bhavnagar": ["Bhavnagar City", "Botad", "Gir Somnath", "Surendranagar", "Morbi"]
    },
    "Uttar Pradesh": {
        "Lucknow": ["Lucknow City", "Unnao", "Rae Bareli", "Sitapur", "Hardoi"],
        "Kanpur": ["Kanpur City", "Kanpur Dehat", "Farrukhabad", "Etawah", "Auraiya"],
        "Agra": ["Agra City", "Mathura", "Firozabad", "Mainpuri", "Etah"],
        "Varanasi": ["Varanasi City", "Chandauli", "Ghazipur", "Jaunpur", "Azamgarh"],
        "Allahabad": ["Prayagraj City", "Kaushambi", "Pratapgarh", "Fatehpur", "Banda"]
    },
    "West Bengal": {
        "Kolkata": ["Kolkata City", "Howrah", "Hooghly", "North 24 Parganas", "South 24 Parganas"],
        "Siliguri": ["Darjeeling", "Jalpaiguri", "Cooch Behar", "Alipurduar", "Kalimpong"],
        "Durgapur": ["Paschim Bardhaman", "Purba Bardhaman", "Birbhum", "Murshidabad", "Nadia"],
        "Asansol": ["Paschim Bardhaman", "Purulia", "Bankura", "Jhargram", "Paschim Medinipur"],
        "Malda": ["Malda", "Uttar Dinajpur", "Dakshin Dinajpur", "South Dinajpur", "North Dinajpur"]
    },
    "Rajasthan": {
        "Jaipur": ["Jaipur City", "Sikar", "Jhunjhunu", "Alwar", "Dausa"],
        "Jodhpur": ["Jodhpur City", "Pali", "Jalore", "Sirohi", "Barmer"],
        "Udaipur": ["Udaipur City", "Rajsamand", "Dungarpur", "Banswara", "Pratapgarh"],
        "Kota": ["Kota City", "Bundi", "Jhalawar", "Baran", "Sawai Madhopur"],
        "Bikaner": ["Bikaner City", "Churu", "Sri Ganganagar", "Hanumangarh", "Nagaur"]
    },
    "Punjab": {
        "Ludhiana": ["Ludhiana City", "Khanna", "Samrala", "Payal", "Raikot"],
        "Amritsar": ["Amritsar City", "Tarn Taran", "Gurdaspur", "Pathankot", "Batala"],
        "Jalandhar": ["Jalandhar City", "Kapurthala", "Hoshiarpur", "Nawanshahr", "Phagwara"],
        "Patiala": ["Patiala City", "Rajpura", "Samana", "Nabha", "Sangrur"],
        "Bathinda": ["Bathinda City", "Mansa", "Sardulgarh", "Rampura Phul", "Talwandi Sabo"]
    },
    "Haryana": {
        "Gurgaon": ["Gurugram City", "Sohna", "Pataudi", "Farukh Nagar", "Manesar"],
        "Faridabad": ["Faridabad City", "Ballabgarh", "Palwal", "Hodal", "Hathin"],
        "Panipat": ["Panipat City", "Samalkha", "Israna", "Bapoli", "Madlauda"],
        "Ambala": ["Ambala City", "Ambala Cantt", "Naraingarh", "Barara", "Shahzadpur"],
        "Hisar": ["Hisar City", "Hansi", "Barwala", "Uklana", "Adampur"]
    },
    "Kerala": {
        "Thiruvananthapuram": ["Trivandrum City", "Neyyattinkara", "Varkala", "Attingal", "Nedumangad"],
        "Kochi": ["Kochi City", "Aluva", "Perumbavoor", "Angamaly", "Kothamangalam"],
        "Kozhikode": ["Calicut City", "Vatakara", "Koyilandy", "Ramanattukara", "Feroke"],
        "Thrissur": ["Thrissur City", "Chalakudy", "Kodungallur", "Irinjalakuda", "Guruvayur"],
        "Kollam": ["Kollam City", "Karunagappally", "Punalur", "Paravur", "Kottarakkara"]
    }
}

def get_states():
    """Get list of all states"""
    return list(INDIAN_LOCATIONS.keys())

def get_districts(state):
    """Get districts for a given state"""
    return list(INDIAN_LOCATIONS.get(state, {}).keys())

def get_cities(state, district):
    """Get cities for a given state and district"""
    return INDIAN_LOCATIONS.get(state, {}).get(district, [])

def get_all_locations():
    """Get all locations in hierarchical format"""
    return INDIAN_LOCATIONS