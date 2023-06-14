from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required

from django.template import loader

from datetime import datetime, timedelta
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
        print(member)
        data.append(member)
    response = HttpResponse(
        data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = "attachment; filename=export.xlsx"

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
    last_sat = today - timedelta(7 + idx - 6)

    template = loader.get_template('dashboard.html')

    last_sat = make_aware(last_sat)

    print(last_sat.day)
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
            )
            new_member.save()

    except Exception as e:
        print("Failed to add -->", e)

    return HttpResponseRedirect('/')


# @login_required(login_url='/')
# def details(request):
#     all_bets = Bet.objects.all()
#     template = loader.get_template('bet/viewbets.html')
#     context = {
#         'all_bets': all_bets,
#     }
#     return HttpResponse(template.render(context, request))

# @login_required(login_url='/')
# def accountView(request):
#     template = loader.get_template('bet/viewaccount.html')

#     context = {
#         # 'all_bets': all_bets,
#         'player': Player.objects.filter(name=request.user)[0],
#         'bets_answer': BetAnswer.objects.filter(player_name=request.user)
#     }
#     return HttpResponse(template.render(context, request))

# @login_required(login_url='/')
# def userbets(request):
#     template = loader.get_template('bet/mybet.html')
#     mybets = Bet.objects.filter(owner=request.user)

#     context = {
#         # 'all_bets': all_bets,
#         'bets': mybets
#     }
#     return HttpResponse(template.render(context, request))

# @login_required(login_url='/')
# def leaderboardView(request):
#     template = loader.get_template('bet/leaderboard.html')

#     context = {
#         # 'all_bets': all_bets,
#         'players': Player.objects.all().order_by('-wallet')
#     }
#     return HttpResponse(template.render(context, request))

# @login_required(login_url='/')
# def allbets(request):
#     template = loader.get_template('bet/viewall.html')
#     mybets = Bet.objects.all()

#     context = {
#         # 'all_bets': all_bets,
#         'bets': mybets
#     }
#     return HttpResponse(template.render(context, request))

# ~~~~~~~~~~~~~~~~~~~~
# APIs
# ~~~~~~~~~~~~~~~~~~~~

# @csrf_exempt
# @require_POST
# def post_new_bet(request):
#     # print("printing the request", request.body)
#     # print(request.POST['bet_text'])

#     # print(str(request.body.decode()).split('=')[1].replace("+"," "))
#     try:
#         if len(request.POST['bet_text']) <= 0:
#             raise Exception("Empty Bet")

#         newbet = Bet.objects.create(bet_text=request.POST['bet_text'],
#                                     owner=request.user,
#                                     pub_date=datetime.now(),
#                                     solution=None)

#         newbet.save()

#         messages.success(request, 'Your bet has been placed successfully !')

#     except Exception as e:
#         print("Failed to add new bet -->", e)

#     return HttpResponseRedirect('/bets')
#     # return HttpResponse(status=200)

# @csrf_exempt
# @require_POST
# def post_bet_choice(request):
#     # print("printing the request", request.body)
#     # print(request.POST['bet_choice'])
#     try:
#         thebet = Bet.objects.get(id=request.POST['bet_choice'].split('-')[1])

#         check_if_answered = BetAnswer.objects.filter(
#             player_name=request.user).filter(
#                 bet__id=int(request.POST['bet_choice'].split('-')[1]))

#         # print(check_if_answered[0].getdetails())

#         if int(request.POST['bet_value']) > 0:
#             print(request.POST['bet_value'])

#             if not check_if_answered:

#                 # Update player's wallet
#                 current_player = Player.objects.filter(name=request.user)
#                 p = current_player[0]
#                 # print("before",p.wallet)

#                 if p.wallet < int(request.POST['bet_value']):
#                     raise Exception("Not Enough funds in wallet")

#                 p.wallet = F('wallet') - int(request.POST['bet_value'])
#                 # print("after",p.wallet)
#                 p.save()

#                 newanswer = BetAnswer.objects.create(
#                     choice=request.POST['bet_choice'].split('-')[0],
#                     bet=thebet,
#                     player_name=request.user,
#                     value=request.POST['bet_value'])

#                 #Save submission
#                 newanswer.save()

#             else:
#                 raise Exception("Already submitted")

#                 messages.success(
#                     request,
#                     'Your bet choice has been changed placed successfully !')
#     except Exception as e:
#         print("placeing bet value failed -->", e)
#     return HttpResponseRedirect('/account')

# @csrf_exempt
# @require_POST
# def close_bet(request):
#     thebet = Bet.objects.get(id=request.POST['bet_solution'].split('-')[1])

#     solution = request.POST['bet_solution'].split('-')[0]

#     thebet.solution = solution
#     thebet.closed = True

#     thebet.save()

#     #~~~~~~~~~~~~~~ Calculate Winnings

#     # answers = Bet.objects.filter(id =int(request.POST['bet_solution'].split('-')[1]))
#     # answers = BetAnswer.objects.all()
#     answers = BetAnswer.objects.filter(
#         bet__id=int(request.POST['bet_solution'].split('-')[1]))

#     # ~~~~~~~~~ Winner or loser
#     for a in answers:
#         choice = a.getdetails()
#         if choice['player_choice'] == solution:
#             print("winner winner chicken dinner", choice['player_name'])
#             p = Player.objects.filter(name=choice['player_name'])[0]
#             if choice['bet_owner'] == choice['player_name']:
#                 p.wallet = p.wallet + (choice['bet_value'] * 2)
#             else:
#                 p.wallet = p.wallet + (choice['bet_value'] * 1.5)

#             p.save()

#     return HttpResponseRedirect('/account')

# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)
