from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .models import Trips, User
from .decorators import login_required


def logout(request):
    if 'user' in request.session:
        del request.session['user']
    
    return redirect("/login")
    

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):

                user = {
                    "id" : log_user.id,
                    "name": f"{log_user}",
                    "email": log_user.email,
                    "role": log_user.role
                }

                request.session['user'] = user
                messages.success(request, "Logueado correctamente.")
                return redirect("/travels")
            else:
                messages.error(request, "Password o Email  incorrectos.")
        else:
            messages.error(request, "Email o password incorrectos.")



        return redirect("/login")
    else:
        return render(request, 'login.html')


def registro(request):
    if request.method == "POST":

        errors = User.objects.validador_basico(request.POST)
        # print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            
            request.session['register_name'] =  request.POST['name']
            request.session['register_email'] =  request.POST['email']

        else:
            request.session['register_name'] = ""
            request.session['register_email'] = ""

            password_encryp = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 

            usuario_nuevo = User.objects.create(
                name = request.POST['name'],
                email=request.POST['email'],
                password=password_encryp,
                role=request.POST['role']
            )

            messages.success(request, "El usuario fue agregado con exito.")
            

            request.session['user'] = {
                "id" : usuario_nuevo.id,
                "name": f"{usuario_nuevo.name}",
                "email": usuario_nuevo.email
            }
            return redirect("/travels")

        return redirect("/registro")
    else:
        return render(request, 'registro.html')

def index(request):
    creador = User.objects.get(id=request.session['user']['id'])
    viajes = Trips.objects.filter(created_by=creador)
    total = Trips.objects.all()
    otros = list(filter(lambda x: x.created_by != creador, total))

    context = {
        'listTrip': viajes,
        'others_trips': otros,
    }

    print(otros)
    messages.success(request, request.session['user']['id'])

    return render(request, 'index.html', context)


def add(request):
    return render(request, 'add.html')

def add_trip(request):
    creador= User.objects.get(id=request.session['user']['id'] )
    
    contex = Trips.objects.create(
        place = request.POST['place'],
        date_start = request.POST['date_start'],
        date_end = request.POST['date_end'],
        plan = request.POST['plan'],
        created_by = creador,
    )

    messages.success(request, "El destino fue agregado con exito.")
    return redirect('/travels')

def join(request, id):
    user = User.objects.get(id=request.session['user']['id'])
    trip = Trips.objects.get(id=id)
    trip.travellers.add(user)
    trip.save()
    return redirect('/travels')


def view(request, id):
    context = {
        'trip': Trips.objects.get(id=id)
    }

    return render(request, 'destination.html', context)

def delete(request):
    this_trip.trips.remove(this_trip)