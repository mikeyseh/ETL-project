from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient("mongodb://mongoadmin:mongoadmin@localhost:27017/")
db = client["to_minio"]  # Sélectionner la base de données 'dwh'
collection = db["source"]  # Sélectionner la collection 'destination'

# Documents à insérer
data = [
    {"id": 1, "nom": "Dupont", "prenom": "Jean"},
    {"id": 2, "nom": "Durand", "prenom": "Marie"},
    {"id": 3, "nom": "Martin", "prenom": "Luc"},
    {"id": 4, "nom": "Bernard", "prenom": "Claire"},
    {"id": 5, "nom": "Petit", "prenom": "Anne"}
]

# Insertion des documents
collection.insert_many(data)
print("Données insérées avec succès dans la collection 'source'.")

# Vérification de l'insertion
for document in collection.find():
    print(document)




