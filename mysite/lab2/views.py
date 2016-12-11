from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from db import DatabaseManager

db_manager = DatabaseManager()


# Create your views here.
def flights(request):
    if request.method == "GET":



        query_set = db_manager.SelectAllFlights()
        mapreduce1 = db_manager.mapreduce1().find()
        mr1 = []
        for item in mapreduce1:
            my_dict = {}
            for key in item:
                if key == "_id":
                    my_dict["id"] = str(item.get(key))
                else:
                    my_dict[key] = item.get(key)
            mr1.append(my_dict.copy())
        mapreduce2 = db_manager.mapreduce2().find()
        mr2 = []
        for item in mapreduce2:
            my_dict = {}
            for key in item:
                if key == "_id":
                    my_dict["id"] = str(item.get(key))
                else:
                    my_dict[key] = item.get(key)
            mr2.append(my_dict.copy())

        aggregation = db_manager.aggregate()
        aggr = []
        print "================================="
        for item in aggregation:
            print item
            my_dict = {}
            for key in item:
                if key == "_id":
                    my_dict["id"] = str(item.get(key))
                else:
                    my_dict[key] = item.get(key)
            aggr.append(my_dict.copy())

        print "================================="

        query = []
        for item in query_set:
            my_dict = {}
            for key in item:
                if key == "_id":
                    my_dict["id"] = str(item.get(key))
                else:
                    my_dict[key] = item.get(key)
            query.append(my_dict.copy())




        return render(request, 'lab2/flights.html', {"query": query,"mreduce1": mr1,"mreduce2": mr2,"aggr": aggr})
    elif request.method == "POST":
        query = db_manager.SelectAllFlights()
        print request.POST
        if request.POST.get("Find") is not None:
            return HttpResponseRedirect("find")
        elif request.POST.get("Ins") is not None:
            return HttpResponseRedirect("add")
        elif request.POST.get("Delete") is not None:
            print(request.POST.get("Delete"))
            db_manager.DeleteFlight(request.POST.get("Delete"))
            return HttpResponseRedirect("flights")
        elif request.POST.get("Edit") is not None:
            id = request.POST.get("Edit")
            url = reverse('edit', kwargs={'id': id})
            return HttpResponseRedirect(url)




def find(request):

    if request.method =='GET':

        return render(request, 'lab2/find.html',)
    elif request.method =='POST':
        print request.POST
        if request.POST.get("Find") is not None:
            return HttpResponseRedirect("find")
        elif request.POST.get("Ins") is not None:
            return HttpResponseRedirect("add")
        elif request.POST.get("Delete") is not None:
            print(int(request.POST.get("Delete")))
            db_manager.DeleteFlight(request.POST.get("Delete"))
            return HttpResponseRedirect("flights")
        elif request.POST.get("Edit") is not None:
            id = request.POST.get("Edit")
            url = reverse('edit', kwargs={'id': id})
            return HttpResponseRedirect(url)


        out_list = request.POST.get("city_out")
        in_list = request.POST.get("city_in")
        plane = request.POST.get("plane")
        date = request.POST.get("date")
        airline = request.POST.get("airline")
        query_set = db_manager.SearchSelect(out_list, in_list, date, plane, airline )
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

        mapreduce1 = db_manager.mapreduce1().find()
        mr1 = []
        for item in mapreduce1:
            my_dict = {}
            for key in item:
                if key == "_id":
                    my_dict["id"] = str(item.get(key))
                else:
                    my_dict[key] = item.get(key)
            mr1.append(my_dict.copy())
        mapreduce2 = db_manager.mapreduce2().find()
        mr2 = []
        for item in mapreduce2:
            my_dict = {}
            for key in item:
                if key == "_id":
                    my_dict["id"] = str(item.get(key))
                else:
                    my_dict[key] = item.get(key)
            mr2.append(my_dict.copy())

        aggregation = db_manager.aggregate()
        aggr = []
        print "================================="
        for item in aggregation:
            print item
            my_dict = {}
            for key in item:
                if key == "_id":
                    my_dict["id"] = str(item.get(key))
                else:
                    my_dict[key] = item.get(key)
            aggr.append(my_dict.copy())

        print "================================="




        return render(request, "lab2/flights.html", {"query": query,"mreduce1": mr1,"mreduce2": mr2,"aggr": aggr})

    # return render(request, 'lab3/find.html', )


def add(request):
    if request.method =='GET':

        return render(request, 'lab2/add.html')
    elif request.method == 'POST':
        print(request.POST)

        db_manager.InsertFlight(request.POST.get("avia"),request.POST.get("city_out"),request.POST.get("city_in"),request.POST.get("plane"),request.POST.get("date"),request.POST.get("passengers"))
        # insert
        return HttpResponseRedirect("flights")
    return render(request, 'lab2/add.html', )

def edit(request, id):
    if request.method =='GET':
        query = db_manager.SelectFlightById(id)

        return render(request, 'lab2/edit.html', {"query": query})
    elif request.method == 'POST':
        print(request.POST)
        db_manager.EditFlight(id,request.POST.get("city_out"),request.POST.get("city_in"),request.POST.get("plane"),request.POST.get("avia"),request.POST.get("date_out"),request.POST.get("passengers"))
        return HttpResponseRedirect("../flights")
    return render(request, 'lab2/edit.html', )

