from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
import paramiko
import json
import requests
# Create your view
from contrôle.models import Controle
from equipement.models import Equipement
from log.models import Log
from procedure.models import Procedure

from django.contrib.auth.mixins import LoginRequiredMixin


#class HomeView(LoginRequiredMixin, View):

"""HomeView."""

pas = 0 # pour modifier la barre de chargement. il s'agit de pas d'incrementation
nbre_exceution = 0 # pour le nombre de commande effectué
total_command = 0 # pour le total des commandes a effectuer
allProcedure = ""

def liste_procedures(request):
    equipements = Equipement.objects.all()
    context = {"equipements": equipements}
    return render(request, 'durcissement/Durcissement.html', context)

params_conformite = {}
def correction_conformite(request):
    global params_conformite
    #context = {"equipements": equipements}
    if request.method == 'POST':
        ip = request.POST.get('ip')
        type = request.POST.get('type')
        procedures = request.POST.get('procedure')
        procedures = procedures
        email = request.POST.get('email')
        params_conformite = {'ip': ip, 'type': type, 'procedure': procedures, 'email': email}
    return render(request, 'durcissement/non_conformite.html', params_conformite)

def recherche_procedure(request):
    Equipement = request.GET.get('equipement')
    if Equipement != None:
        procedure = Procedure.objects.filter(type_equipement=Equipement)
    procedure = procedure.order_by('-id')
    procedures = []
    for x in procedure:
        procedures.append({'id': x.id, 'type': x.type_equipement, 'nom': x.nom, 'systeme': x.systeme})
    return JsonResponse({"procedure": list(procedures)})

def executer_procedure(request):
    global pas, nbre_exceution, total_command, allProcedure
    pas = 0
    allProcedure = ""
    total_command = 0
    nbre_exceution=0
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
        commandes = []
        if "Tout" in procedures:
            procedure = Procedure.objects.filter(type_equipement=type)
            for x in procedure:
                allProcedure += x.nom + ","
                controles = Controle.objects.filter(procedure=x)
                for controle in controles:
                    commandes.append(controle.commande)
        else:
            for i in range (len(procedures)-1):
                procedure = Procedure.objects.get(id=procedures[i])
                allProcedure += procedure.nom + ","
                controles = Controle.objects.filter(procedure=procedure)
                for controle in controles:
                    commandes.append(controle.commande)
        reponse = durcissemnt(type, adresse_ip, "root", "root", commandes, email)
        return JsonResponse(reponse)
    else:
        message = "Veuillez remplir tous les champs svp !!"
        return JsonResponse({"status": 400, "message" : message})

def executer_conformite(request):
    global pas, nbre_exceution, total_command, allProcedure, params_conformite
    pas = 0
    allProcedure = ""
    total_command = 0
    nbre_exceution=0
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
        listeCommandes = []
        for x in procedures:
            listeCommandes.append(x)
        listeCommandes.pop() # on supprime la virgule de la fin
        total_command = len(listeCommandes)
        pas = 100 / (total_command+1)
        reponse = {"status": 400, "message": "Erreur inconnue"}
        if type == "Serveur Linux":
            reponse = connexion_linux(type, adresse_ip, "root", "root", listeCommandes, email, "non conformité")
            params_conformite = {}
        return JsonResponse(reponse)
    else:
        message = "Veuillez remplir tous les champs svp !!"
        return JsonResponse({"status": 400, "message" : message})

def durcissemnt(serveur, adresse_ip, user, mdp, commandes, email):
    global pas, total_command
    listeCommandes = []
    for commande in commandes:
        commande = commande.split(",")
        for x in commande:
            listeCommandes.append(x)
    total_command = len(listeCommandes) + 1
    pas = 100 / total_command # calcule du pas
    if serveur == "Serveur Linux":
       return connexion_linux(serveur, adresse_ip, user, mdp, listeCommandes, email, "Durcissement")

def avancement(request):
    global pas, nbre_exceution, total_command
    return JsonResponse({"pourcentage": pas*nbre_exceution, "total": total_command, "effectue": nbre_exceution})

def connexion_linux(type, ip_address, username, password, commandes, email, nature):
    global nbre_exceution, allProcedure
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip_address, username=username, password=password)
        print("Successfully connected to", ip_address)

        for commande in commandes:
            stdin, stdout, stderr = ssh_client.exec_command(commande)
            stdout.channel.set_combine_stderr(True)
            sortie = stdout.readlines()
            for output in sortie:
                print(output)
            nbre_exceution += 1
        today = datetime.now()
        today = today.strftime("%d-%m-%Y à %Hh%Mm%Ss")
        html = contenuMail(ip_address, type, today)
        allProcedure = allProcedure.strip(',')
        ecrireLog(nature, type, ip_address, email, allProcedure, "")
        EnvoyerMail(email, html)
        return {"status": 200, "message": ""}
        ssh_client.close
    except TimeoutError as e:
        message = "Erreur : Impossible de joindre l'adresse IP "+str(ip_address)
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

def contenuMail(ip, type, date):
    html = "<html><head><style>.header{ display: flex; flex-direction: row; justify-content: space-between; background-color: black; font-size: medium; color: white; font-weight: bold; font-family: Arial, Helvetica, sans-serif; width: auto; height: 80px; padding-top: 30px; padding-left: 2%; padding-right:2%; margin-top: 20px; } .footer{ position: fixed; bottom: 0; display: flex; flex-direction: row; background-color: white; font-size: x-small; color: black; font-weight: bold; font-family: Arial, Helvetica, sans-serif; width: 100%; height: 100px; padding-left: 3%; padding-right:3%; margin-left: auto; margin-right: auto; margin-top: 300px;  } span {padding: 15px; } p{  color: black;  font-family: Arial, Helvetica, sans-serif;  font-size: x-small; }.bodi{margin: 30px; } .hardening{ display: flex; flex-direction: row;  } .fiche{    background-color: rgba(211, 84, 0,.8) !important;    margin: 30px;    height:160px;    width:600px;    align-items: center;    text-align: center;    margin-top: 5px;} form{    text-align: left;    margin-left: 30px;    margin-top: 10px;    padding-top: 10px;    font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;    font-weight: bold;   }</style>     </head>     <body> <div class='header'>  <div class='hardening'>  <img src='https://zupimages.net/up/22/21/rpvt.jpg' alt='' height='60' width='60' >  <span>HardeningApp</span> </div>  <img src='https://zupimages.net/up/22/21/h7dr.jpg' alt='' height='60' width='60' > </div > <div class='bodi'> <p>Bonjour!</p> <p>Veuillez retrouver en PJ le rapport de vérification des configurations de durcissement que vous venez d'éffectuer.</p> <p>Cordialement,</p> <p>HardeningApp.</p></div>        <div class='fiche'> <form action=''>  <p>"
    html += '<label for="">Adresse IP : '+ip+'</label> </p> <p><label for="">Type : '+type+'</label> </p>'
    html += '<p> <label for="">Le : '+date+'</label> </p> &nbsp; </form>'
    html += '</div>&nbsp;<div class="footer"> <img src="https://zupimages.net/up/22/21/0xbz.jpg" alt="" height="60" width="60" > <span > ©Orange Cameroun, 2022 <br> Interne Orange </span> </div> </body> </html>'
    return html

def EnvoyerMail(mail, body):
    global nbre_exceution
    url = "https://tools-svc.orange.cm/api/Email/sendmail"
    payload = json.dumps({
        "recipient": str(mail),
        "cc": str(mail),
        "subject": "Rapport de vérification des configuration de durcissement",
        "body": str(body)
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
