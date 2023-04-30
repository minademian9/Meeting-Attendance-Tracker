from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required

from django.template import loader

from datetime import datetime

from .models import Attendee, AttendanceRecord

from django.contrib import messages

from django.db.models import F

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

    try:

        member = Attendee.objects.get(id=member_id)
        print("member ----- ", member)
        new_attend = AttendanceRecord.objects.create(
            member=member, record_date=datetime.now())

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
