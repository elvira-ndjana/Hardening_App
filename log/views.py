from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from log.models import Log

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

class HomeView(LoginRequiredMixin, View):

    """HomeView."""

def liste_log(request):
    logs = Log.objects.all()
    logs = logs.order_by('-id')
    context = {"logs": logs}
    return render(request, 'log/gestion_des_logs.html', context)

def recherche_logs(request):
    date = request.GET.get('date')
    user = request.GET.get('user')
    procedure = request.GET.get('procedure')
    ip = request.GET.get('equipement')
    if user == "":
        user = None
    if procedure == "":
        procedure = None
    if ip == "":
        ip = None
    if date == "":
        date = None
    logs = []
    if date != None and user != None and procedure != None and ip != None:
        logs = Log.objects.filter(date__contains=date, user__contains=user, procedure__contains=procedure,
                                  ip__contains=ip)
    elif date != None and user != None and procedure != None and ip == None:
        logs = Log.objects.filter(date__contains=date, user__contains=user, procedure__contains=procedure)
    elif date != None and user != None and procedure == None and ip != None:
        logs = Log.objects.filter(date__contains=date, user__contains=user, ip__contains=ip)
    elif date != None and user != None and procedure == None and ip == None:
        logs = Log.objects.filter(date__contains=date, user__contains=user)
    elif date != None and user == None and procedure != None and ip != None:
        logs = Log.objects.filter(date__contains=date, procedure__contains=procedure, ip__contains=ip)
    elif date != None and user == None and procedure != None and ip == None:
        logs = Log.objects.filter(date__contains=date, procedure__contains=procedure)
    elif date != None and user == None and procedure == None and ip != None:
        logs = Log.objects.filter(date__contains=date, ip__contains=ip)
    elif date != None and user == None and procedure == None and ip == None:
        logs = Log.objects.filter(date__contains=date)
    elif date == None and user != None and procedure != None and ip != None:
        logs = Log.objects.filter(user__contains=user, procedure__contains=procedure, ip__contains=ip)
    elif date == None and user != None and procedure != None and ip == None:
        logs = Log.objects.filter(user__contains=user, procedure__contains=procedure)
    elif date == None and user != None and procedure == None and ip != None:
        logs = Log.objects.filter(user__contains=user, ip__contains=ip)
    elif date == None and user != None and procedure == None and ip == None:
        logs = Log.objects.filter(user__contains=user)
    elif date == None and user == None and procedure != None and ip != None:
        logs = Log.objects.filter(procedure__contains=procedure, ip__contains=ip)
    elif date == None and user == None and procedure != None and ip == None:
        logs = Log.objects.filter(procedure__contains=procedure)
    elif date == None and user == None and procedure == None and ip != None:
        logs = Log.objects.filter(ip__contains=ip)
    elif date == None and user == None and procedure == None and ip == None:
        logs = Log.objects.all()
    logs = logs.order_by('-id')
    logss = []
    for x in logs:
        logss.append({'id': x.id, 'routine': x.routine, 'date': x.date.strftime("%d %B %Y %H:%M") ,
                      'type': x.type, 'ip': ip, 'user': x.user, 'procedure': x.procedure, 'rapport': x.rapport})

    #print(logss)
    return JsonResponse({"logs": list(logss)})







