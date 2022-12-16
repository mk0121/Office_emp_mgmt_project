from django.shortcuts import render, HttpResponse
from .models import Department, Role, Employee
from datetime import datetime
from django.db.models import Q


# Create your views here.

def index(request):
    return render(request, 'emp_app/index.html')


def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'emp_app/all_emp.html', context)


def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dept = int(request.POST['dept'])
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        role = int(request.POST['role'])
        phone = int(request.POST['phone'])

        new_emp = Employee(first_name=first_name, last_name=last_name, dept_id=dept, salary=salary, bonus=bonus,
                           role_id=role, phone=phone, hire_date=datetime.now())
        new_emp.save()
        return HttpResponse('emp added!')

    elif request.method == 'GET':
        return render(request, 'emp_app/add_emp.html')

    else:
        return HttpResponse("An Exception Occurred! Employee Has Not Been Added")


def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_id_to_delete = Employee.objects.get(id=emp_id)
            emp_id_to_delete.delete()
            return HttpResponse('removed Successfully')

        except:
            return HttpResponse('pls enter valid emp ID')

    emps = Employee.objects.all()

    context = {
        'emps': emps
    }
    return render(request, 'emp_app/remove_emp.html', context)


def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        role = request.POST['role']
        dept = request.POST['dept']

        emps = Employee.objects.all()

        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))

        if role:
            emps = emps.filter(role__name__icontains=role)

        if dept:
            emps = emps.filter(dept__name__icontains=dept)

        context = {
            'emps': emps
        }

        return render(request, 'emp_app/all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'emp_app/filter_emp.html')

    else:
        return HttpResponse('Exception occurred !')