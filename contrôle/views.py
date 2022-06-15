from datetime import datetime
import paramiko
import re
import base64
import requests
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from equipement.models import Equipement
from log.models import Log
from procedure.models import Procedure
from .models import Controle
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


class HomeView(LoginRequiredMixin, View):

    """HomeView."""

pas = 0 # pour modifier la barre de chargement. il s'agit de pas d'incrementation
nbre_exceution = 0 # pour le nombre de commande effectué
total_command = 0 # pour le total des commandes a effectuer
nbre_conformite = 0 # pour le total des conformites


# Create your views here.
def liste_controles(request):
    procedures = Procedure.objects.all()  # recuperation de toutes les lignes dans la table procedures
    controles = Controle.objects.all().order_by('-id')  # recuperation de toutes les lignes dans la table procedures
    if request.method == 'POST':
        if 'rechercher' in request.POST:
            controles = Controle.objects.filter(id=request.POST.get('id'), default=request.POST.get('default')).values()
        elif 'voir_tout' in request.POST:
            controles = Controle.objects.all()
    context = {'controles': controles, 'procedures': procedures}
    return render(request, 'contrôles/liste_contrôles.html', context)


def recherche_controle(request):
    id = request.GET.get('id')
    code = request.GET.get('code')
    defaut = request.GET.get('default')
    procedure = request.GET.get('procedure')
    Equipement = request.GET.get('equipement')
    if code == "":
        code = None
    if defaut == "":
        defaut = None
    if procedure == "":
        procedure = None
    if Equipement == "":
        Equipement = None
    controle = []
    if id != None and code != None and defaut != None and procedure != None and Equipement != None:
        proced = Procedure.objects.get(nom__contains=procedure, type_equipement__contains=Equipement)
        controle = Controle.objects.filter(id=id, code__contains=code, default=defaut, procedure=proced)
    elif id != None and code != None and defaut != None and procedure != None and Equipement == None:
        proced = Procedure.objects.get(nom__contains=procedure)
        controle = Controle.objects.filter(id=id, code__contains=code, default=defaut, procedure=proced)
    elif id != None and code != None and defaut != None and procedure == None and Equipement == None:
        controle = Controle.objects.filter(id=id, code__contains=code, default=defaut)
    elif id != None and code != None and defaut == None and procedure == None and Equipement == None:
        controle = Controle.objects.filter(id=id, code__contains=code)
    elif id != None and code == None and defaut == None and procedure == None and Equipement == None:
        controle = Controle.objects.filter(id=id)
    elif id == None and code != None and defaut != None and procedure != None and Equipement != None:
        proced = Procedure.objects.get(nom__contains=procedure, type_equipement__contains=Equipement)
        controle = Controle.objects.filter(code__contains=code, default=defaut, procedure=proced)
    elif id == None and code == None and defaut != None and procedure != None and Equipement != None:
        proced = Procedure.objects.get(nom__contains=procedure, type_equipement__contains=Equipement)
        controle = Controle.objects.filter(default=defaut, procedure=proced)
    elif id == None and code == None and defaut == None and procedure != None and Equipement != None:
        proced = Procedure.objects.get(nom__contains=procedure, type_equipement__contains=Equipement)
        controle = Controle.objects.filter(procedure=proced)
    elif id == None and code == None and defaut == None and procedure == None and Equipement != None:
        proced = Procedure.objects.get(type_equipement__contains=Equipement)
        controle = Controle.objects.filter(procedure=proced)
    elif id != None and code != None and defaut == None and procedure != None and Equipement != None:
        proced = Procedure.objects.get(nom__contains=procedure, type_equipement__contains=Equipement)
        controle = Controle.objects.filter(id=id, code__contains=code, procedure=proced)
    elif id != None and code != None and defaut == None and procedure == None and Equipement != None:
        proced = Procedure.objects.get(type_equipement__contains=Equipement)
        controle = Controle.objects.filter(id=id, code__contains=code, procedure=proced)
    elif id == None and code != None and defaut == None and procedure == None and Equipement != None:
        proced = Procedure.objects.get(type_equipement__contains=Equipement)
        controle = Controle.objects.filter(code__contains=code, procedure=proced)
    elif id == None and code != None and defaut == None and procedure == None and Equipement == None:
        controle = Controle.objects.filter(code__contains=code)
    elif id != None and code != None and defaut != None and procedure == None and Equipement != None:
        controle = Controle.objects.filter(id=id, code__contains=code, default=defaut)
    elif id != None and code == None and defaut != None and procedure == None and Equipement == None:
        controle = Controle.objects.filter(id=id, default=defaut)
    elif id == None and code == None and defaut != None and procedure == None and Equipement == None:
        controle = Controle.objects.filter(default=defaut)
    elif id == None and code != None and defaut != None and procedure != None and Equipement == None:
        proced = Procedure.objects.get(nom__contains=procedure)
        controle = Controle.objects.filter(code__contains=code, default=defaut, procedure=proced)
    elif id == None and code == None and defaut != None and procedure != None and Equipement == None:
        proced = Procedure.objects.get(nom__contains=procedure)
        controle = Controle.objects.filter(default=defaut, procedure=proced)
    elif id == None and code == None and defaut == None and procedure != None and Equipement == None:
        proced = Procedure.objects.get(nom__contains=procedure)
        controle = Controle.objects.filter(procedure=proced)
    elif id == None and code == None and defaut == None and procedure == None and Equipement == None:
        controle = Controle.objects.all()
    controle = controle.order_by('-id')
    controles = []
    for x in controle:
        controles.append({'id': x.id, 'code': x.code, 'type': x.procedure.type_equipement, 'default': x.default,
                          'libelle': x.libelle, 'nom': x.procedure.nom, 'commande': x.commande,
                          'verification': x.verification,
                          'champVerification': x.champVerification})

    return JsonResponse({"controle": list(controles)})


def ajouter_controle(request):
    if request.method == 'POST':
        controle = Controle()
        controle.code = request.POST.get('code')
        controle.libelle = request.POST.get('libelle')
        controle.default = request.POST.get('default')
        controle.commande = request.POST.get('commande')
        controle.verification = request.POST.get('verification')
        controle.champVerification = request.POST.get('champVerification')
        procedure = Procedure.objects.get(id=request.POST.get('procedure'))
        controle.procedure = procedure
        controle.save()
        ecrireLog("Ajout de controle", procedure.type_equipement, "", "user@gmail.com", procedure.nom, "")
        controle = Controle.objects.order_by('-id')
        controles = []
        for x in controle:
            controles.append({'id': x.id, 'code': x.code, 'type': x.procedure.type_equipement, 'default': x.default,
                              'libelle': x.libelle, 'nom': x.procedure.nom, 'commande': x.commande})
            break
        return JsonResponse(controles[0])


def supprimer_controle(request):
    controle = Controle.objects.get(id=int(request.GET.get('id')))
    ecrireLog("Suppresion de controle", controle.procedure.type_equipement, "", "user@gmail.com", controle.procedure.nom, "")
    controle.delete()
    return JsonResponse({"status": 0})

def verification_controle(request):
    equipements = Equipement.objects.all()
    context = {"equipements": equipements}
    return render(request, 'contrôles/vérification.html', context)


def recherche_procedure(request):
    Equipement = request.GET.get('equipement')
    if Equipement != None:
        procedure = Procedure.objects.filter(type_equipement=Equipement)
    procedure = procedure.order_by('-id')
    procedures = []
    for x in procedure:
        procedures.append({'id': x.id, 'type': x.type_equipement, 'nom': x.nom, 'systeme': x.systeme})
    return JsonResponse({"procedure": list(procedures)})


def executer_verification(request):
    global pas, nbre_exceution, total_command, nbre_conformite
    pas = 0
    nbre_conformite = 0
    total_command = 0
    nbre_exceution = 0
    adresse_ip = request.GET.get('ip')
    type = request.GET.get('type')
    procedures = request.GET.get('procedure')
    email = request.GET.get('email')
    if adresse_ip == "":
        adresse_ip = None
    if type == "":
        type = None
    if procedures == "":
        procedures = None
    if email == "":
        email = None

    if adresse_ip != None and type != None and procedures != None and email != None:
        procedures = procedures.split(",")
        conformite = []
        commandes = []
        champVerification = []
        if "Tout" in procedures:
            procedure = Procedure.objects.filter(type_equipement=type)
            for x in procedure:
                controles = Controle.objects.filter(procedure=x)
                for controle in controles:
                    conformite.append(controle.commande)
                    commandes.append(controle.verification)
                    champVerification.append(controle.champVerification)
        else:
            for i in range(len(procedures) - 1):
                procedure = Procedure.objects.get(id=procedures[i])
                controles = Controle.objects.filter(procedure=procedure)
                for controle in controles:
                    conformite.append(controle.commande)
                    commandes.append({'code': controle.code, 'procedure': controle.procedure.nom, 'libelle': controle.libelle, 'controle': controle.verification})
                    champVerification.append(controle.champVerification)
        reponse = durcissemnt(type, adresse_ip, "root", "root", commandes, champVerification, conformite, email)
        return JsonResponse(reponse)
    else:
        message = "Veuillez remplir tous les champs svp !!"
        return JsonResponse({"status": 400, "message": message})


def durcissemnt(serveur, adresse_ip, user, mdp, commandes, verifications, conformite, email):
    global pas, total_command
    listeCommandes = []
    listeConformites = []
    listeVerifications = []
    #structuration de la liste des commandes
    for i in range(len(commandes)):
        commande = commandes[i]['controle'].split(",")
        for x in commande:
            listeCommandes.append({'code': commandes[i]['code'], 'procedure': commandes[i]['procedure'], 'libelle': commandes[i]['libelle'], 'commande': x})
    #structuration des champs de la verification
    for champ in verifications:
        champ = champ.split(",")
        for x in champ:
            listeVerifications.append(x)

    # structuration des commandes de non conformite
    for champ in conformite:
        champ = champ.split(",")
        for x in champ:
            listeConformites.append(x)

    total_command = len(listeCommandes) + 2
    pas = 100 / total_command # calcule du pas
    if serveur == "Serveur Linux":
        return connexion(serveur, adresse_ip, user, mdp, listeCommandes, listeVerifications, listeConformites, email)


def avancement(request):
    global pas, nbre_exceution, total_command, nbre_conformite
    return JsonResponse({"pourcentage": pas * nbre_exceution, "total": total_command,
                         "effectue": nbre_exceution, "conformite": nbre_conformite})


def connexion(type, ip_address, username, password, commandes, verifications, conformites, email):
    global nbre_exceution, nbre_conformite
    try:
        rapport = []
        listeConformites = ""
        rapport.append({'code': 'Code', 'procedure': 'Procédure', 'libelle': 'Libellé', 'resultat': 'Statuts',
                         'commentaire': 'Commentaires'})
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip_address, username=username, password=password)
        print("Successfully connected to", ip_address)
        allProcedure = ""
        for i in range (len(commandes)):
            stdin, stdout, stderr = ssh_client.exec_command(commandes[i]['commande'])
            stdout.channel.set_combine_stderr(True)
            sortie = stdout.readlines()
            #keywords = str(verifications[i].split('=')[0]+'=\w+')
            resultat = "KO"
            for output in sortie:
                if verifications[i] in output:
                    resultat = "OK"
                    break

            if resultat == "KO":
                print(conformites)
                listeConformites += conformites[i] + ','
                nbre_conformite += 1
            if commandes[i]['procedure'] not in allProcedure:
                allProcedure += commandes[i]['procedure'] + ","
            rapport.append(
                {'code': commandes[i]['code'], 'procedure': commandes[i]['procedure'], 'libelle': commandes[i]['libelle'],
                 'resultat': resultat, 'commentaire': ''})
            nbre_exceution += 1
        nomRapport, rapport = creationCSV(rapport)
        allProcedure = allProcedure.strip(',')
        ecrireLog("Vérification", type, ip_address, email, allProcedure, nomRapport)
        today = datetime.now()
        today = today.strftime("%d-%m-%Y à %Hh%Mm%Ss")
        html = contenuMail(ip_address, type, today)
        EnvoyerMail(email, html, rapport, nomRapport)
        return {"status": 200, "message": "", "conformites": listeConformites}
        ssh_client.close
    except TimeoutError as e:
        message = "Erreur : Impossible de joindre l'adresse IP " + str(ip_address)
        return {"status": 400, "message": message}
    except paramiko.ssh_exception.AuthenticationException as e:
        message = "Erreur: nom d'utilisateur ou mot de passe incorrect"
        return {"status": 400, "message": message}
    except paramiko.ssh_exception.NoValidConnectionsError as e:
        message = "Erreur: port 22 non ouvert sur le serveur"
        return {"status": 400, "message": message}
    except Exception as e:
        return {"status": 400, "message": e}
        pass

def creationCSV(rapport):
    global nbre_exceution
    entetes = [
        rapport[0]['code'],
        rapport[0]['procedure'],
        rapport[0]['libelle'],
        rapport[0]['resultat'],
        rapport[0]['commentaire']
    ]

    valeurs = []
    for i in range(1,len(rapport)):
        valeurs.append([rapport[i]['code'], rapport[i]['procedure'], rapport[i]['libelle'], rapport[i]['resultat'],
        rapport[i]['commentaire']])

    today = datetime.now()
    today = today.strftime("%d-%m-%Y à %Hh%Mm%Ss")
    nomFichier = str(today)+".csv"
    f = open("static/rapport/"+nomFichier, 'w')
    ligneEntete = ";".join(entetes) + "\n"
    f.write(ligneEntete)
    for valeur in valeurs:
        ligne = ";".join(valeur) + "\n"
        f.write(ligne)
    f.close()
    nbre_exceution += 1
    return nomFichier, encodage(nomFichier)

def encodage(fichier):
    file = open("static/rapport/"+fichier, "r")
    data = file.read()
    file.close()
    encoded = base64.b64encode(data.encode())
    return encoded

def contenuMail(ip, type, date):
    html = "<html><head><style>.header{ display: flex; flex-direction: row; justify-content: space-between; background-color: black; font-size: medium; color: white; font-weight: bold; font-family: Arial, Helvetica, sans-serif; width: auto; height: 80px; padding-top: 30px; padding-left: 2%; padding-right:2%; margin-top: 20px; } .footer{ position: fixed; bottom: 0; display: flex; flex-direction: row; background-color: white; font-size: x-small; color: black; font-weight: bold; font-family: Arial, Helvetica, sans-serif; width: 100%; height: 100px; padding-left: 3%; padding-right:3%; margin-left: auto; margin-right: auto; margin-top: 300px;  } span {padding: 15px; } p{  color: black;  font-family: Arial, Helvetica, sans-serif;  font-size: x-small; }.bodi{margin: 30px; } .hardening{ display: flex; flex-direction: row;  } .fiche{    background-color: rgba(211, 84, 0,.8) !important;    margin: 30px;    height:160px;    width:600px;    align-items: center;    text-align: center;    margin-top: 5px;} form{    text-align: left;    margin-left: 30px;    margin-top: 10px;    padding-top: 10px;    font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;    font-weight: bold;   }</style>     </head>     <body> <div class='header'>  <div class='hardening'>  <img src='https://zupimages.net/up/22/21/rpvt.jpg' alt='' height='60' width='60' >  <span>HardeningApp</span> </div>  <img src='https://zupimages.net/up/22/21/h7dr.jpg' alt='' height='60' width='60' > </div > <div class='bodi'> <p>Bonjour!</p> <p>Veuillez retrouver en PJ le rapport de vérification des configurations de durcissement que vous venez d'éffectuer.</p> <p>Cordialement,</p> <p>HardeningApp.</p></div>        <div class='fiche'> <form action=''>  <p>"
    html += '<label for="">Adresse IP : '+ip+'</label> </p> <p><label for="">Type : '+type+'</label> </p>'
    html += '<p> <label for="">Le : '+date+'</label> </p> &nbsp; </form>'
    html += '</div>&nbsp;<div class="footer"> <img src="https://zupimages.net/up/22/21/0xbz.jpg" alt="" height="60" width="60" > <span > ©Orange Cameroun, 2022 <br> Interne Orange </span> </div> </body> </html>'
    return html

def EnvoyerMail(mail, body, encoded, namefile):
    global nbre_exceution
    url = "https://tools-svc.orange.cm/api/Email/sendmail"
    payload = json.dumps({
        "recipient": str(mail),
        "cc": str(mail),
        "subject": "Rapport de vérification des configuration de durcissement",
        "body": str(body),
        "filecontent": str(encoded),
        "filename": str(namefile)
    })
    headers = {
        'accept': 'application/json',
        'sendFromEmail': 'noreply@orange.cm',
        'sendFromName': 'HardeningApp',
        'Content-Type': 'application/json-patch+json'
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    nbre_exceution += 1

def ecrireLog(routine, type, ip, user, procedure, rapport):
    log = Log()
    log.routine = routine
    log.type = type
    log.ip = ip
    log.user = user
    log.procedure = procedure
    log.rapport = rapport
    log.save()
