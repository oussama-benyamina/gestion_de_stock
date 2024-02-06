import mysql.connector
import tkinter as tk
from tkinter import messagebox
import csv

# Fonction pour charger et afficher les produits depuis la base de données
def load_products():
    product_listbox.delete(0, tk.END)
    mycursor.execute("SELECT * FROM product")
    products = mycursor.fetchall()
    for product in products:
        product_listbox.insert(tk.END, f"{product[0]} - {product[1]}")

# Fonction pour insérer un nouveau produit dans la base de données
def insert_product(name, description, price, quantity, category):
    sql = "INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)"
    val = (name, description, price, quantity, category)
    mycursor.execute(sql, val)
    mydb.commit()
    load_products()  # Recharger les produits

# Fonction pour supprimer un produit sélectionné de la base de données
def delete_product():
    try:
        index = product_listbox.curselection()[0]
        product_id = int(product_listbox.get(index).split(" - ")[0])
        sql = "DELETE FROM product WHERE id = %s"
        val = (product_id,)
        mycursor.execute(sql, val)
        mydb.commit()
        product_listbox.delete(index)
    except IndexError:
        messagebox.showerror("Erreur", "Veuillez sélectionner un produit à supprimer.")

# Fonction pour exporter les produits en stock au format CSV
def export_products():
    mycursor.execute("SELECT * FROM product")
    products = mycursor.fetchall()
    with open("stock.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Nom", "Description", "Prix", "Quantité", "ID Catégorie"])
        for product in products:
            writer.writerow(product)

# Créer une fenêtre Tkinter
root = tk.Tk()
root.title("Gestion de stock")

# Liste des produits
product_listbox = tk.Listbox(root, width=50)
product_listbox.pack(padx=10, pady=10)

# Boutons pour ajouter, supprimer, exporter des produits
add_product_button = tk.Button(root, text="Ajouter produit", command=lambda: insert_product("Nouveau produit", "", 0, 0, 1))
add_product_button.pack(padx=10, pady=5)

delete_product_button = tk.Button(root, text="Supprimer produit", command=delete_product)
delete_product_button.pack(padx=10, pady=5)

export_product_button = tk.Button(root, text="Exporter CSV", command=export_products)
export_product_button.pack(padx=10, pady=5)

# Connexion à la base de données
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1020",
    database="store"
)

# Création d'un curseur pour exécuter des requêtes SQL
mycursor = mydb.cursor()

# Insertion d'une catégorie et d'un produit d'exemple
sql = "INSERT INTO category (name) VALUES (%s)"
val = ("Électronique",)
mycursor.execute(sql, val)
mydb.commit()

insert_product("Téléphone", "Smartphone haut de gamme", 999, 10, 1)

# Charger et afficher les produits
load_products()

root.mainloop()

