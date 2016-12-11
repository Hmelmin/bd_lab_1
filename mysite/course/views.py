from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from lab3.models import type,region,farm, report

def main_table(request):
    if request.method == "GET":
         query = report.objects.all()
         print(query)
         return render(request,'lab3/main_table.html', {"query": query})
    elif request.method == "POST":
         query = report.objects.all()
         print request.POST
         if request.POST.get("Find") is not None:
             return HttpResponseRedirect("find")
         elif request.POST.get("Ins") is not None:
             return HttpResponseRedirect("add")
         elif request.POST.get("Delete") is not None:
             print(int(request.POST.get("Delete").split("_")[1]))
             report.objects.filter(id=request.POST.get("Delete").split("_")[1]).delete()
             return HttpResponseRedirect("main_table")
         elif request.POST.get("Edit") is not None:
             id = request.POST.get("Edit").split("_")[1]
             url = reverse('edit', kwargs={'id': id})
             return HttpResponseRedirect(url)


def find(request):
     if request.method =='GET':
          region_query = region.objects.all()
          type_query = type.objects.all()
          farm_query = farm.objects.all()
          return render(request, 'lab3/find.html', {"type": type_query, "region": region_query, "farm": farm_query})
     elif request.method =='POST':
         print request.POST
         if request.POST.get("Find") is not None:
             return HttpResponseRedirect("find")
         elif request.POST.get("Ins") is not None:
             return HttpResponseRedirect("add")
         elif request.POST.get("Delete") is not None:
             print(int(request.POST.get("Delete").split("_")[1]))
             farm.objects.filter(id=request.POST.get("Delete").split("_")[1]).delete()
             return HttpResponseRedirect("main_table")
         elif request.POST.get("Edit") is not None:
             id = request.POST.get("Edit").split("_")[1]
             url = reverse('edit', kwargs={'id': id})
             return HttpResponseRedirect(url)

         search_type = request.POST.get("type")
         profit = request.POST.get("profit")
         search_farm = request.POST.get("farm")
         search_region = request.POST.get("region")
         employees = request.POST.get("employees")

         result = report.objects.all()
         if len(search_farm)>0:
             farm_id = farm.objects.get(id=search_farm)
             result = result.filter(farm=farm_id)
         elif len(search_type)>0:
             type_id = type.objects.get(id=search_type)
             result = result.filter(type=type_id)
         elif len(search_region) > 0:
             region_id = region.objects.get(id = search_region)
             result = result.filter(region = region_id)
         elif len(profit) > 0:
             result = result.filter(profits__gte = profit)
         elif len(employees) > 0:
             result = result.filter(employees__lte = employees)

         return render(request, "lab3/main_table.html", {"query": result})

     return render(request, 'lab3/find.html', )


def add(request):
     region_query = region.objects.all()
     type_query = type.objects.all()
     farm_query= farm.objects.all()

     if request.method =='GET':
        return render(request, 'lab3/add.html', {"region": region_query, "type": type_query, "farm": farm_query })
     elif request.method == 'POST':
         print(request.POST)

         new_report = report.objects.create(   farm=farm_query.get(id=int(request.POST.get("farm"))),type=type_query.get(id=int(request.POST.get("type"))),region=region_query.get(id=int(request.POST.get("region"))),
                                                   employees=int(request.POST.get("employees")),
                                                   costs=int(request.POST.get("costs")),
                                                   profits=int(request.POST.get("profits")))

         new_report.save()
         return HttpResponseRedirect("main_table")
     return render(request, 'lab3/add.html', )

def edit(request, id):
     query = report.objects.get(id=int(id))
     region_query = region.objects.all()
     type_query = type.objects.all()
     farm_query= farm.objects.all()
     query = report.objects.get(id=int(id))
     if request.method =='GET':
         return render(request, 'lab3/edit.html', {"query": query,"region": region_query, "type": type_query, "farm": farm_query})
     elif request.method == 'POST':
         print(request.POST)

         query.region_id = region.objects.get(id=int(request.POST.get("region")))
         query.farm_id = farm.objects.get(id=int(request.POST.get("farm")))
         query.type_id = type.objects.get(id=int(request.POST.get("type")))
         query.employees = int(request.POST.get("employees"))
         query.profits = int(request.POST.get("profits"))
         query.costs = int(request.POST.get("costs"))
         query.save()
         return HttpResponseRedirect("../main_table")
     return render(request, 'lab3/edit.html', )

