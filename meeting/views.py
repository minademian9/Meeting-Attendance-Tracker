from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required

from django.template import loader

from datetime import datetime, timedelta, date
from django.utils.timezone import make_aware

from .models import Attendee, AttendanceRecord

from django.contrib import messages

# from django.db.models import F

from django.conf import settings

# import pandas as pd
import tablib

# Create your views here.


def index(request):

    members = Attendee.objects.all()
    template = loader.get_template('index.html')
    context = {
        'all_members': members,
    }

    return HttpResponse(template.render(context, request))


def thankyou(request):

    template = loader.get_template('thankyou.html')
    context = {
        # 'all_members': members,
    }

    return HttpResponse(template.render(context, request))


def newmember(request):

    template = loader.get_template('new_member.html')
    context = {
        # 'all_members': members,
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='/admin')
def export(request):
    members = Attendee.objects.all().values_list('name', 'email', 'mobile')

    headers = ('Full Name', 'Email', 'Mobile Number')
    data = []
    data = tablib.Dataset(*data, headers=headers)
    # print(members)
    for member in list(members):
        # print(member)
        data.append(member)
    response = HttpResponse(
        data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = "attachment; filename=export.xlsx"

    return response


@login_required(login_url='/admin')
def export_attendance(request):
    attendance = AttendanceRecord.objects.all(
    )  #.values_list('member', 'record_date')

    headers = ('Full Name', 'Attendance Count')
    data = []
    data = tablib.Dataset(*data, headers=headers)

    counter = {}
    results = attendance.values()
    # print(results)
    for record in list(results):
        member = Attendee.objects.get(id=record['member_id'])
        # print(member.name)
        if member.name in counter.keys():
            counter[member.name] = counter[member.name] + 1
        else:
            counter[member.name] = 1

    print(counter)
    for c in counter:
        data.append([c, counter[c]])

    response = HttpResponse(
        data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
    response[
        'Content-Disposition'] = "attachment; filename=export_attendance.xlsx"

    return response
    # return HttpResponse("Done")


@login_required(login_url='/admin')
def export_records(request):
    records = AttendanceRecord.objects.all().values_list(
        'member', 'record_date')

    headers = ('Full Name', 'Attendance Date')
    data = []
    data = tablib.Dataset(*data, headers=headers)
    # print(members)
    for rec in list(records):
        # print()
        datetime_element = rec[1].date()  # Extracting the date
        date = datetime_element.strftime('%m/%d/%Y')
        row = (Attendee.objects.get(id=rec[0]).name, date)
        print(row)
        data.append(row)
    response = HttpResponse(
        data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
    response[
        'Content-Disposition'] = "attachment; filename=export-records.xlsx"

    return response


@login_required(login_url='/admin')
def data_import(request):
    template = loader.get_template('import.html')
    context = {
        # 'all_members': members,
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='/admin')
def download_database(request):
    db_path = settings.DATABASES['default']['NAME']
    # dbfile = File(open(db_path, "rb"))
    dbfile = open(db_path, "rb")
    response = HttpResponse(dbfile, content_type='application/x-sqlite3')
    response['Content-Disposition'] = 'attachment; filename=%s' % 'db.sqlite3'
    # response['Content-Length'] = dbfile.size
    return response


@login_required(login_url='/admin')
def dashboard(request):
    #Get Last Saturday
    today = datetime.today()
    idx = (today.weekday() + 1) % 7  # MON = 0, SUN = 6 -> SUN = 0 .. SAT = 6
    print(f"the idx= {idx}")
    if idx == 6:
        last_sat = today
    else:
        last_sat = today - timedelta(7 + idx - 6)
    print(f"last saturday = {last_sat}")
    template = loader.get_template('dashboard.html')

    last_sat = make_aware(last_sat)

    # print(last_sat.day)
    # all_records = AttendanceRecord.objects.all()
    all_records = AttendanceRecord.objects.filter(
        record_date__year=last_sat.year,
        record_date__month=last_sat.month,
        record_date__day=last_sat.day)
    # all_records = AttendanceRecord.objects.filter(record_date=last_sat)
    formatted_records = []

    for rec in all_records:
        formatted_records.append({"name": rec.member, "date": rec.record_date})

    context = {
        'all_attendance': formatted_records,
        'saturday_date': last_sat.now().strftime("%Y-%m-%d"),
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='/admin')
def export_date_range_page(request):
    template = loader.get_template('export_date_range.html')
    context = {
        # 'all_members': members,
    }

    return HttpResponse(template.render(context, request))


######################
# Post Methods
#####################


@csrf_exempt
@require_POST
def add_attendance(request):
    # print("printing the request", dir(request))
    print("Submitter ", list(request.POST.keys())[1])
    member_id = list(request.POST.keys())[1].split(',')[1]
    print("id", member_id)

    last_sat = datetime.now()
    last_sat = make_aware(last_sat)

    try:

        member = Attendee.objects.get(id=member_id)
        print("member ----- ", member)
        already_added = AttendanceRecord.objects.filter(
            member__id=member.id,
            record_date__year=last_sat.year,
            record_date__month=last_sat.month,
            record_date__day=last_sat.day)

        # print("already added ????", already_added)

        if len(already_added) <= 0:
            new_attend = AttendanceRecord.objects.create(
                member=member, record_date=make_aware(datetime.now()))

            new_attend.save()

            messages.success(request, 'Attendance Recorded !')
        return HttpResponseRedirect('/thankyou')
    except Exception as e:
        print("Failed to add new attendance -->", e)

    return HttpResponseRedirect('/')


@csrf_exempt
@require_POST
def add_new_member(request):
    print("New Member ", request.POST)

    try:
        if len(request.POST['full_name']) <= 0:
            raise Exception("Missing Name")

        new_member = Attendee.objects.create(
            name=request.POST['full_name'],
            email=request.POST['email_address'],
            mobile=request.POST['mobile_number'],
            date_created=datetime.now(),
        )

        new_member.save()

        new_attend = AttendanceRecord.objects.create(
            member=new_member, record_date=datetime.now())

        new_attend.save()

        messages.success(request, 'You have been added successfully !')

        return HttpResponseRedirect('/thankyou')

    except Exception as e:
        print("Failed to add new member -->", e)

    return HttpResponseRedirect('/newmember')


@csrf_exempt
@require_POST
def importdata(request):
    print("Data to import ", request.POST)
    # filename = request.POST['datafile']
    print("File ", request.FILES['datafile'])

    try:
        dataset = tablib.Dataset()
        new_members = request.FILES['datafile']
        # imported_data = dataset.load(new_members.read().decode('utf-8'),format='xlsx')
        imported_data = dataset.load(new_members.read(), format='xlsx')
        # print(imported_data)

    except Exception as e:
        print("Failed to parse -->", e)

    try:
        print("Importing members")
        for row in imported_data:
            new_member = Attendee.objects.create(
                name=row[0],
                email=row[1],
                mobile=row[2],
                date_created=datetime.now(),
            )
            new_member.save()

    except Exception as e:
        print("Failed to add -->", e)

    return HttpResponseRedirect('/')


#--------- Helper Date Functions ---------#
def get_saturdays(start_date, end_date):
    saturdays = []
    for single_date in daterange(start_date, end_date):
        if single_date.weekday() == 5:  # Saturday is represented by 5
            saturdays.append(single_date)
    return saturdays


def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)


@csrf_exempt
@require_POST
def get_export_range(request):
    print("New Range ", request.POST)

    try:
        if len(request.POST['start_date']) <= 0:
            raise Exception("Missing start date")
        elif len(request.POST['end_date']) <= 0:
            raise Exception("Missing end date")

        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        start_date = date(int(start_date.split('-')[0]),
                          int(start_date.split('-')[1]),
                          int(start_date.split('-')[2]))
        end_date = date(int(end_date.split('-')[0]),
                        int(end_date.split('-')[1]),
                        int(end_date.split('-')[2]))

        if start_date > end_date:
            raise Exception("Start date is before End Date")

        # Excel Prep -------

        headers = get_saturdays(start_date, end_date)
        headers = [i.strftime('%Y-%m-%d') for i in headers]
        headers.insert(0, "Attendees")
        row = ["" for i in range(len(headers))]

        data = []
        data = tablib.Dataset(*data, headers=headers)

      

        records = AttendanceRecord.objects.all().values_list('member', 'record_date')

        # ----- Aggregate Date
        aggregator = {}
        for record in records:
          member = Attendee.objects.get(id=record[0])
          # print(member.name)
          if member.name in aggregator.keys():
            aggregator[member.name].append(record[1].date().strftime('%Y-%m-%d'))
          else:
            aggregator[member.name] = [record[1].date().strftime('%Y-%m-%d')]
          
        # print(aggregator)

        for key,val in aggregator.items():
          row[0] = key
          for one_date in val:
            if one_date in headers:
              index = headers.index(one_date)
              row[index] = "YES"
              
          data.append(row)
          row = ["" for i in range(len(headers))]
          
    
        # for rec in list(records):
        #   datetime_element = rec[1].date()  # Extracting the date
        #   the_date = datetime_element.strftime('%Y-%m-%d')
            
        #   row[0] = Attendee.objects.get(id=rec[0]).name
        #   print(data["Attendees"])
        #   row[1] = the_date
        #   # print(row)
        #   data.append(row)

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=saturday-export.xlsx"

        return response

    except Exception as e:
        print("Failed to export full range error: -->", e)

    return HttpResponseRedirect('/export-range')
