#import flask
from flask import Flask, render_template, session, request ,redirect
from datetime import datetime
import pymongo

app= Flask("Review")
app.secret_key ="cookies"
mongo = pymongo.MongoClient("mongodb+srv://aya:J4im3l3sgl4c3@cluster0.bud6o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
bdd_utilisateurs = mongo.bdd.utilisateurs
mon_utilisateur = bdd_utilisateurs.find_one({"pseudo":"Aya"})
print(mon_utilisateur)


@app.route("/")
def accueil() :
    # On récupère toutes les annonces
    mes_annonces = mongo.bdd.annonces
    annonces = mes_annonces.find({})
    if "utilisateur" in session :
        # Si l'utilisateur est connecté, on affiche la page en précisant l'utilisateur
        mes_utilisateurs = mongo.bdd.utilisateurs
        utilisateur = mes_utilisateurs.find_one({"pseudo" : session["utilisateur"]})
        return render_template("index.html",utilisateur = utilisateur,annonces = annonces)
    else :
        # Si l'utilisateur n'est pas connecté, on affiche simplement la page
        return render_template("index.html",annonces = annonces)

@app.route("/login", methods = ["GET","post"])
def login():
    if request.method == "GET":
      return render_template("c.html")
    
    else:
      
      pseudo_enter = request.form["input_pseudo"]
      mdp_enter =request.form["input_mdp"]

      mes_utilisateurs = mongo.bdd.utilisateurs
      utilisateur = mes_utilisateurs.find_one({"pseudo" : pseudo_enter})
          
      if not utilisateur :
          return render_template("c.html", erreur =" l'utilisateur est inexistant")
           
      elif mdp_enter != utilisateur["mdp"] :
         return render_template("c.html", erreur = "le mot de passe est incorrect")
      else :
         session["utilisateur"] = pseudo_enter
         return redirect("/")


@app.route("/profil")
def profil():
    mes_utilisateurs = mongo.bdd.utilisateurs
    utilisateur = mes_utilisateurs.find_one({"pseudo":session["utilisateur"]})
    print(utilisateur)
    return render_template("profil.html" ,utilisateur = utilisateur)

# Route nouvelle annonce
@app.route("/nouvelle-annonce", methods = ["GET", "POST"])
def nouvelleannonce() :
    if request.method == "GET" :
        mes_utilisateurs = mongo.bdd.utilisateurs
        utilisateur = mes_utilisateurs.find_one({"pseudo":session["utilisateur"]})
        return render_template("newpost.html", utilisateur = utilisateur)
    else :
        # 1 : on récupère les informations entrées dans les boîtes (inputs)
        titre_entre = request.form["input_titre"]
        description_entre = request.form["input_description"]
        image_entre = request.form["input_image"]
        if image_entre == "" :
            image_entre = "data:image/png;base64,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"
        # 2 : on gère tous les cas d'erreur
        mes_utilisateurs = mongo.bdd.utilisateurs
        utilisateur = mes_utilisateurs.find_one({"pseudo" : session["utilisateur"]})
        # si aucun titre n'a été rentré    
        if titre_entre == "" :
            return render_template("newpost.html", erreur = "Veuillez rentrer un titre")
        # si la description ne fait pas assez de caractères
        elif len(description_entre) < 5 :
            return render_template("newpost.html", erreur = "La description doit être plus longue")
        else :
            # 3 : on crée l'annonce, A FAIRE LA SEMAINE PROCHAINE (18/01)
            mes_annonces = mongo.bdd.annonces
            mes_annonces.insert_one({


                                        "titre" : titre_entre,
                                         "description" : description_entre,
                                         "image" : image_entre,
                                         "auteur" : utilisateur["pseudo"],
                                         "date" : datetime.now()
                                         })
            

            # on redirige vers la page d'accueil
            return redirect("/")



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods = ["GET", "POST"])
def register() :
    if request.method == "GET" :
        return render_template("r.html")
    else :
        # 1 : on récupère les informations entrées dans les boîtes (inputs)
        pseudo_entre = request.form["input_pseudo"]
        mdp_entre = request.form["input_mdp"]
        avatar_entre = request.form["input_avatar"]
        if avatar_entre == "" :
            avatar_entre = "https://i.pinimg.com/736x/c6/df/ec/c6dfec4f1a0b8dbbfe69756f1a249a46.jpg"
        # 2 : on gère tous les cas d'erreur
        mes_utilisateurs = mongo.bdd.utilisateurs
        utilisateur = mes_utilisateurs.find_one({"pseudo" : pseudo_entre})
        # si le pseudo existe déjà
        if utilisateur :
            return render_template("r.html", erreur = "L'utilisateur existe déjà")
        # si aucun pseudo n'a été rentré    
        elif pseudo_entre == "" :
            return render_template("r.html", erreur = "Veuillez rentrer un pseudo")
        # si le mot de passe ne fait pas assez de caractères
        elif len(mdp_entre) < 4 :
            return render_template("r.html", erreur = "Le mot de passe doit faire au moins 4 caractères")
        else :
            # 3 : on crée le compte utilisateur
            mes_utilisateurs.insert_one({
                "pseudo" : pseudo_entre,
                "mdp" : mdp_entre,
                "avatar" : avatar_entre,
                "age" : 0,
                "nationalite" : "non précisée"
            })
            # on connecte l'utilisateur via le cookie
            session["utilisateur"] = pseudo_entre
            # on redirige vers la page d'accueil
            return redirect("/")


@app.route("/find")
def find() :
    bdd_utilisateur = mongo.bdd.utilisateurs
    resultat = bdd_utilisateur.find({"pseudo" : "toto"})
    return render_template("test.html", resultat = list(resultat))

@app.route("/insert")
def insert() :
    bdd_utilisateur = mongo.bdd.utilisateurs
    resultat = bdd_utilisateur.insert_one({
        "pseudo" : "toto",
        "mdp" : "5555",
        "age" : 14,
        "avatar" : ""})
    return render_template("test.html", resultat = resultat)



# Exemple de requête "update_one" --> mettre à jour UNE entrée
@app.route("/update")
def update():
    bdd_utilisateur = mongo.bdd.utilisateurs
    resultat = bdd_utilisateur.update_one(
        {"pseudo" : "toto"},
        {"$set" : {"mdp" : "6789", "age" : 23}})
    return render_template("test.html", resultat = resultat)


@app.route("/admin/livre")
def livre():
    bdd_annonces = mongo.bdd.annonces
    mes_an = bdd_annonces.find({})
    return render_template("admin/livre.html", mes_an = list(mes_an))

@app.route("/supprimeran/<titre>")
def suprimeran(titre):
    bdd_an = mongo.bdd.annonces
    bdd_an.delete_one({"titre" : titre })
    return redirect("/admin/livre")



app.run("0.0.0.0", "6452")