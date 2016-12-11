from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from bson.objectid import ObjectId
import datetime
from db import DatabaseManager
import cache
db_manager = DatabaseManager()


# Create your views here.
def flights(request):
    if request.method == "GET":
        query_set = db_manager.SelectAllFlights()
        query = []
        for item in query_set:
            my_dict = {}
            for key in item:
                if key == "_id":
                    my_dict["id"] = str(item.get(key))
                else:
                    my_dict[key] = item.get(key)
            query.append(my_dict.copy())
        return render(request, 'lab3/flights.html', {"query": query})
    elif request.method == "POST":
        query = db_manager.SelectAllFlights()
        print request.POST
        if request.POST.get("Find") is not None:
            return HttpResponseRedirect("find")
        elif request.POST.get("Ins") is not None:
            return HttpResponseRedirect("add")
        elif request.POST.get("Delete") is not None:
            print(request.POST.get("Delete"))
            id=request.POST.get("Delete")
            flight = db_manager.SelectFlightById(id)
            date = flight.get("date")
            if cache.is_key_present(date):
                updated=[]
                list_flights=cache.get_from(date)
                for item in list_flights:
                    if not(str(item.get("_id"))==(str(id))):

                        print item.get("_id")
                        print ObjectId(id)
                        updated.append(item)
                for item in updated:

                    print item
                cache.set_from(date,updated)
            db_manager.DeleteFlight(request.POST.get("Delete"))
            return HttpResponseRedirect("flights")
        elif request.POST.get("Edit") is not None:
            id = request.POST.get("Edit")
            url = reverse('edit', kwargs={'id': id})
            return HttpResponseRedirect(url)




def find(request):

    if request.method =='GET':

        return render(request, 'lab3/find.html',)
    elif request.method =='POST':
        print request.POST
        if request.POST.get("Find") is not None:
            return HttpResponseRedirect("find")
        elif request.POST.get("Ins") is not None:
            return HttpResponseRedirect("add")
        elif request.POST.get("Delete") is not None:
            print(request.POST.get("Delete"))
            id=request.POST.get("Delete")
            flight = db_manager.SelectFlightById(id)
            date = flight.get("date")
            if cache.is_key_present(date):
                updated=[]
                list_flights=cache.get_from(date)
                for item in list_flights:
                    if not(str(item.get("_id"))==(str(id))):

                        print item.get("_id")
                        print ObjectId(id)
                        updated.append(item)
                for item in updated:

                    print item
                cache.set_from(date,updated)
            db_manager.DeleteFlight(request.POST.get("Delete"))
            return HttpResponseRedirect("flights")
        elif request.POST.get("Edit") is not None:
            id = request.POST.get("Edit")
            url = reverse('edit', kwargs={'id': id})
            return HttpResponseRedirect(url)



        date = request.POST.get("date")

        query_set = db_manager.SearchSelect(date)
        query = []
        for item in query_set:
            my_dict = {}
            for key in item:
                if key == "_id":
                    my_dict["id"] = str(item.get(key))
                else:
                    my_dict[key] = item.get(key)
                    print (item.get(key))
            query.append(my_dict.copy())
        return render(request, "lab3/flights.html", {"query": query,})

    # return render(request, 'lab3/find.html', )


def add(request):
    if request.method =='GET':

        return render(request, 'lab3/add.html')
    elif request.method == 'POST':
        print(request.POST)
        time = datetime.datetime.now()
        date=request.POST.get("date")
        db_manager.InsertFlightTemp(request.POST.get("avia"),request.POST.get("city_out"),request.POST.get("city_in"),request.POST.get("plane"),date,request.POST.get("passengers"),time)
        flight=db_manager.SelectFlightByTime(time)
        if cache.is_key_present(date):
                updated=[]
                list_flights=cache.get_from(date)
                for item in list_flights:
                        updated.append(item)
                updated.append(flight)
                for item in updated:

                    print item
                cache.set_from(date,updated)
        return HttpResponseRedirect("flights")
    #return render(request, 'lab3/add.html', )

def edit(request, id):
    if request.method =='GET':
        query = db_manager.SelectFlightById(id)

        return render(request, 'lab3/edit.html', {"query": query})
    elif request.method == 'POST':
        print(request.POST)
        db_manager.EditFlight(id,request.POST.get("city_out"),request.POST.get("city_in"),request.POST.get("plane"),request.POST.get("avia"),request.POST.get("passengers"))
        flight = db_manager.SelectFlightById(id)
        date = flight.get("date")
        if cache.is_key_present(date):
                updated=[]
                list_flights=cache.get_from(date)
                for item in list_flights:
                    if not(str(item.get("_id"))==(str(id))):

                        print item.get("_id")
                        print ObjectId(id)
                        updated.append(item)
                    else:
                        updated.append(flight)
                for item in updated:

                    print item
                cache.set_from(date,updated)

        return HttpResponseRedirect("../flights")
    return render(request, 'lab3/edit.html', )

