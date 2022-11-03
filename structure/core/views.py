from flask import render_template,request,Blueprint,session,current_app,redirect,url_for
from structure.models import User, Message, Contact, Phonebook, Package ,Payment,SenderId,SMSReport , Rate
from structure.core.forms import MessageForm,ContactForm,PhonebookForm,SenderIDForm,RatesForm
from structure.users.forms import RegistrationForm

# from structure.team.views import team
from sqlalchemy.orm import load_only
from flask_login import login_required
from structure import db
import json
import requests
import csv
import os
import random
import datetime
import urllib.request
core = Blueprint('core',__name__)

@core.route('/')
@login_required
def index():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    phonebooks = Phonebook.query.filter_by(user_id =user_id).all()
    contacts = Contact.query.filter_by(user_id = user_id).all()
    messages = Message.query.filter_by(user_id=user_id).all()
  
    return render_template('index.html',phonebooks=phonebooks,contacts=contacts,messages=messages,user=user)

@core.route('/base')
def base():
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    return render_template('base.html')



@core.route('/tests')
@login_required
def test():

    # single message
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    campaigns_id = user.email[0:8]+ str(random.randint(1,1000))

    print(user)
    # rslr.connectbind.com:8080/bulksms/bulksms?username=dlp-test123&password=D3l3ph@!&type=0&dlr=1&destination=233551660436&source=test&message=atest
    # http://rslr.connectbind.com:8080/bulksms/bulksms?username=dlp-testacc&password=tE$t1234&type=0&dlr=1&destination=233551660436&source=test&message=atest
    username = "dlp-testacc"
    password = "tE$t1234"
    type = 0
    dlr = 1
    destination = ['0551660436','0244614107']
    destination_json = json.dumps(destination)
    source = "flask"
    message = "Flask test from Raymondzxwwx"
    # res = requests.post('http://rslr.connectbind.com:8080/bulksms?username=username&password=password&type=type&dlr=dlr&destination=destination&source=source&message=message')
    # print ('response from server:',res)
    # return "test"
    # return (res.json())
    # dictFromServer = res.json()
    # print (dictFromServer)
    # return (rslr.connectbind.com:8080/bulksms?username=username&password=password&type=type&dlr=dlr&destination=destination&source=source&message=message)
    endPoint = 'https://api.mnotify.com/api/sms/quick'
    apiKey = 'DGh55p4QDIFgIzskqW8unzHRhjHjnOJ1u07Apbq2T6iBG'
    data = {
    'recipient[]':['0551660436','23324522000222'],
    'sender': 'ChampLabs',
    'message': 'test message. get it?ignore',
    'is_schedule': False,
    'schedule_date': ''
    }
    url = endPoint + '?key=' + apiKey
    response = requests.post(url, data)
    data = response.json()
    response_status = data['status']
    response_message = data['message']
    response_code = data['code']
    response_successful = data['summary']['numbers_sent']
    print (response_successful)
    response_successful_json = json.dumps(response_successful)
    total_sent = data['summary']['total_sent']
    total_rejected = data['summary']['total_rejected']
    api_id = data['summary']['_id']
    sms_num = data['summary']['credit_used']
    print(len(destination))
    # for i in  range(0, len(destination)):
    message_id = user.email[0:8]+ str(random.randint(1,1000000))
    message_save = Message(message=message,
                            source="source",
                            type="0",response_status=response_status,destination_json = destination_json
                            ,response_message=response_message,response_code=response_code,user_id=user_id,time= datetime.datetime.now(),date=datetime.datetime.now(),total_rejected=total_rejected,total_sent=total_sent,response_successful= response_successful,api_id=api_id,message_id=message_id)

    db.session.add(message_save)
    db.session.commit()
    print(data['status'])
    # # return data  this  works no delivery status
    # for number in response_successful:
    #     message_id = user.email[0:8]+ str(random.randint(1,1000000))
    #     campaign_id = api_id
    #     date  = datetime.datetime.now()
    #     print(date)
    #     t  = datetime.datetime.now
    #     # time = t.strftime("%H:%M:%S")
    #     message = message
    #     recipient = number
    #     sender = "source"
    #     sms_save = SMSReport(message_id = message_id, campaign_id = campaign_id, date = date, recepient = recipient, sender = sender, status = response_status,retries = 0,message=message,user_id=user_id)
  
    #     db.session.add(sms_save)
        # db.session.commit()

    # undeliveredendPoint = 'https://api.mnotify.com/api/campaign/39EEEF67-A6FC-4E9C-9512-3F7C5B9AA0A5/undelivered'   + campaign_id +'undelivered'
    # api_id = "678D78CE-6049-40B0-A83F-46A905816560"
    undeliveredendPoint = 'https://api.mnotify.com/api/campaign/'   + api_id +'/undelivered'


    apiKey = 'DGh55p4QDIFgIzskqW8unzHRhjHjnOJ1u07Apbq2T6iBG' 
    url = undeliveredendPoint + '?key=' + apiKey
    response = urllib.request.urlopen(url)
    undelivereddata = response.read()
    udictdata = json.loads(undelivereddata)
    print(len(udictdata))
    print("ddataa")
    print(udictdata)

    for i in range(0, 1):


            # item_q = udictdata['report'][i]['_id']
            message_id = udictdata['report'][i]['_id']
            campaign_id = udictdata['report'][i]['campaign_id']
            date = udictdata['report'][i]['date_sent']
            message = udictdata['report'][i]['message']
            print(message)
            recipient = udictdata['report'][i]['recipient']
            retries = udictdata['report'][i]['retries']
            sender = udictdata['report'][i]['sender']
            status = udictdata['report'][i]['status']
            sms_save = SMSReport(message_id = message_id, campaign_id = campaign_id, date = date, recepient = recipient, sender = sender, status = status,retries = 0,message=message,user_id=user_id)
    
            db.session.add(sms_save)
            db.session.commit()


    deliveredendPoint = 'https://api.mnotify.com/api/campaign/'   + api_id +'/delivered'

    apiKey = 'DGh55p4QDIFgIzskqW8unzHRhjHjnOJ1u07Apbq2T6iBG' 
    url = deliveredendPoint + '?key=' + apiKey
    response = urllib.request.urlopen(url)
    deliveredendPoint = response.read()
    dictdata = json.loads(deliveredendPoint)
    print(len(udictdata))

    for i in range(0, 1):
        


            # item_q = udictdata['report'][i]['_id']
            message_id = dictdata['report'][i]['_id']
            campaign_id = dictdata['report'][i]['campaign_id']
            date = dictdata['report'][i]['date_sent']
            message = dictdata['report'][i]['message']
            print(message)
            recipient = dictdata['report'][i]['recipient']
            retries = dictdata['report'][i]['retries']
            sender = dictdata['report'][i]['sender']
            status = dictdata['report'][i]['status']
            sms_save = SMSReport(message_id = message_id, campaign_id = campaign_id, date = date, recepient = recipient, sender = sender, status = status,retries = 0,message=message,user_id=user_id)
    
            db.session.add(sms_save)
            db.session.commit()
    return data
        


    # # print(response_summary)
    # endPoint2 = 'https://api.mnotify.com/api/campaign/'+ api_id
    # apiKey2 = 'DGh55p4QDIFgIzskqW8unzHRhjHjnOJ1u07Apbq2T6iBG'
    # url = endPoint2 + '?key=' + apiKey2
    # response2 = urllib.request.urlopen(url)
    # mdata = response2.read()
    # dictdata = json.loads(mdata)

    # # print("report")
    # # print(dictdata)
    # # print("report")
    # # print(mdata['report'])
    # mdata_len = len(dictdata)
    # print("length")
    # print(mdata_len)
    # print(api_id)
    # saved_sms = []
    # some_list = []

    # smsreports = SMSReport.query.filter_by(user_id=user_id,campaign_id=api_id).all()
    # for sms in smsreports:
    #     print(sms.message_id)

    #     if sms in saved_sms:
    #         some_list.append(sms.message_id)
    #     else:
    #         saved_sms.append(sms.message_id)
    # print(saved_sms)
    # print(some_list)

    # for i in range(0, len(dictdata)):


    #     item_q = dictdata['report'][i]['_id']
    #     message_id = dictdata['report'][i]['_id']
    #     campaign_id = dictdata['report'][i]['campaign_id']
    #     date = dictdata['report'][i]['date_sent']
    #     message = dictdata['report'][i]['message']
    #     print(message)
    #     recipient = dictdata['report'][i]['recipient']
    #     retries = dictdata['report'][i]['retries']
    #     sender = dictdata['report'][i]['sender']
    #     status = dictdata['report'][i]['status']
    #     if item_q:

    #         sms_save = SMSReport(message_id = message_id, campaign_id = campaign_id, date = date, recepient = recipient, sender = sender, status = status,retries = retries,message=message,user_id=user_id
    #                                     )
    #         # message_save = Message(message=message,
    #         #                 source="source",
    #         #                 type=type,response_status=response_status,destination_json = destination_json
    #         #                 ,response_message=response_message,response_code=response_code,user_id=user_id,time= td,date=date,total_rejected=total_rejected,total_sent=total_sent,response_successful= response_successful,api_id=api_id)

    #         db.session.add(sms_save)
    #         db.session.commit()
    #         print(data['status'])
    #     return data


# endPoint = 'https://api.mnotify.com/api/sms/quick'
# apiKey = 'YOUR_API_KEY'
# data = {
#    'recipient[]': ['0249706365', '0203698970'],
#    'sender': 'mNotify',
#    'message': 'API messaging is fun!',
#    'is_schedule': False,
#    'schedule_date': ''
# }
# url = endPoint + '?key=' + apiKey
# response = requests.post(url, data)
# data = response.json()

@core.route('/reports')
@login_required
def reports():
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    messages = Message.query.filter_by(user_id=user_id).all()



    return render_template('oldmessages.html',messages=messages,user=user)

@core.route('/campaignreports/<campaign_id>')
@login_required
def campaignreports(campaign_id):
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    messages = SMSReport.query.filter_by(user_id=user_id,message_id=campaign_id).all()
    return render_template('campaignreports.html',messages=messages,user=user)



@core.route('/smsreports')
@login_required
def smsreports():
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    smsreports = SMSReport.query.filter_by(user_id=user_id).all()

    messages = Message.query.filter_by(user_id=user_id).all()
    endPoint = 'https://api.mnotify.com/api/campaign/apiv2-2022-08-16-233551660436'
    apiKey = 'DGh55p4QDIFgIzskqW8unzHRhjHjnOJ1u07Apbq2T6iBG'
    url = endPoint + '?key=' + apiKey
    response = urllib.request.urlopen(url)
    mdata = response.read()

    # theids = data['report']['_id']
    # print (theids)
    # for id in theids:
    #     theitem_ids.append(id)

    # theitem_ids.append(data['report']['_id'])
    print("i taya sef")
    # print(theitem_ids)
    dictdata = json.loads(mdata)
    print(dictdata)

    data_len = len(dictdata)
    id_dict = []
    if dictdata:
        for i in range(0, data_len):

    # for item in data['report']:
            item_q = dictdata['report'][i]['_id']
            sms = SMSReport.query.filter_by(message_id=item_q).first()
            print(item_q)
            if sms is not None:
                sms_id = sms.message_id
                id_dict.append(sms_id)
            else:
                sms_id = ""
                # if sms.message_id == item_q:
                #     print(sms.message_id)
                #     print("equal")
                # else:
                #     print("different")
            print("ids dict")
            print(id_dict)
            if item_q not in id_dict:
                # if sms_id != item_q:
                message_id = dictdata['report'][i]['_id']
                campaign_id = dictdata['report'][i]['campaign_id']
                date = dictdata['report'][i]['date_sent']
                message = dictdata['report'][i]['message']
                recipient = dictdata['report'][i]['recipient']
                retries = dictdata['report'][i]['retries']
                sender = dictdata['report'][i]['sender']
                status = dictdata['report'][i]['status']
                print("item")
                print(message_id)
                sms_save = SMSReport(message_id = message_id, campaign_id = campaign_id, date = date, recepient = recipient, sender = sender, status = status,retries = retries,message=message,user_id=user_id
                                    )

                db.session.add(sms_save)
                db.session.commit()
            else:

                print("already exists")
        print("ids")
        print(id_dict)
        return mdata




@core.route('/sreports')
@login_required
def sreports():
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    smsreports = SMSReport.query.filter_by(user_id=user_id).all()

    messages = Message.query.filter_by(user_id=user_id).all()
    # endPoint = 'https://api.mnotify.com/api/status/315376121'
# The above code is creating a variable called endPoint and assigning it the value of the url of the
# API endpoint.
    endPoint = 'https://api.mnotify.com/api/campaign/25C85999-5903-4CC2-95EF-1FBCAD3FCF0F/delivered'

    apiKey = 'DGh55p4QDIFgIzskqW8unzHRhjHjnOJ1u07Apbq2T6iBG' 
    url = endPoint + '?key=' + apiKey
    response = urllib.request.urlopen(url)
    mdata = response.read()

    # theids = data['report']['_id']
    # print (theids)
    # for id in theids:
    #     theitem_ids.append(id)

    # theitem_ids.append(data['report']['_id'])
    print("i taya sef")
    # # print(theitem_ids)
    # dictdata = json.loads(mdata)
    # print(dictdata)

    # data_len = len(dictdata)
    # id_dict = []
    # if dictdata:
    #     for i in range(0, data_len):

    # # for item in data['report']:
    #         item_q = dictdata['report'][i]['_id']
    #         sms = SMSReport.query.filter_by(message_id=item_q).first()
    #         print(item_q)
    #         if sms is not None:
    #             sms_id = sms.message_id
    #             id_dict.append(sms_id)
    #         else:
    #             sms_id = ""
    #             # if sms.message_id == item_q:
    #             #     print(sms.message_id)
    #             #     print("equal")
    #             # else:
    #             #     print("different")
    #         print("ids dict")
    #         print(id_dict)
    #         if item_q not in id_dict:
    #             # if sms_id != item_q:
    #             message_id = dictdata['report'][i]['_id']
    #             campaign_id = dictdata['report'][i]['campaign_id']
    #             date = dictdata['report'][i]['date_sent']
    #             message = dictdata['report'][i]['message']
    #             recipient = dictdata['report'][i]['recipient']
    #             retries = dictdata['report'][i]['retries']
    #             sender = dictdata['report'][i]['sender']
    #             status = dictdata['report'][i]['status']
    #             print("item")
    #             print(message_id)
    #             sms_save = SMSReport(message_id = message_id, campaign_id = campaign_id, date = date, recepient = recipient, sender = sender, status = status,retries = retries,message=message,user_id=user_id
    #                                 )

    #             db.session.add(sms_save)
    #             db.session.commit()
    #         else:

    #             print("already exists")
    #     print("ids")
    return mdata




@core.route('/senderids',methods=['GET', 'POST'])
@login_required
def senderids():
    form = SenderIDForm()
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    messages = Message.query.filter_by(user_id=user_id).all()
    senderids = SenderId.query.filter_by(user_id = user_id).all()
    if request.method == 'POST':
        sendername = form.name.data
        description = form.description.data
        endPoint = 'https://api.mnotify.com/api/senderid/register'
        apiKey = 'DGh55p4QDIFgIzskqW8unzHRhjHjnOJ1u07Apbq2T6iBG'
        data = {
        'sender_name': sendername,
        'purpose': description,

        }
        url = endPoint + '?key=' + apiKey
        response = requests.post(url, data)
        response_data = response.json()
        print(response_data)
        response_status = response_data['summary']['status']
        status = response_data['status']
        senderid_save = SenderId(name=sendername,
                                description=description,
                                status=status,api_status=response_status,user_id=user_id)

        db.session.add(senderid_save)
        db.session.commit()

    return render_template('senderids.html',messages=messages,user=user,form=form,senderids=senderids)



# @core.route('/message',methods=['GET', 'POST'])
# @login_required
# def message():
#     form = MessageForm()
#     user = User.query.filter_by(email=session['email']).first()
#     user_id = user.id
#     credit_balance = user.credit
#     messages = Message.query.filter_by(user_id=user_id).all()
#     phonebook_all= Phonebook.query.filter_by(user_id=user_id).all()
#     data= []
#     campaign_id = user.email[0:8]+ str(random.randint(1,1000))

#     if request.method == 'POST':
#         message = form.message.data
#         date = form.date.data
#         datee = form.date.data.strftime('%Y-%m-%d')
#         if form.time.data:
#             time = form.time.data
#             # mytime = datetime.datetime.strptime(time,'%H%M').time()
#             mytime = str(time)
#             mydate = str(date)
#             is_sch = True
#             thedatetime = mydate + " " + mytime
#             print("mytime")  
#             print(thedatetime) 
#         else:
#             is_sch = False
#             thedatetime = " "
#             print("no time")
#         print("date")  
#         print(date) 
#         # phonebook_id = form
#         if form.phonebook.data:
#             # print("Phonebook id")
#             # print(form.phonebook.data)
#             phonebooky = Contact.query.filter_by(phonebook_id=form.phonebook.data).all()
#             # print("Phonebooky")
#             # print(phonebooky)
#             for number in phonebooky:
#                 data.append(number.number)
#             print(data)
#         # destination_dict = []
#         destinations = form.destination.data
#         if "," in destinations:
#             data = destinations.split(",")
#         else:
#             dat = form.destination.data
#             data.append(dat)
#         if form.contacts.data:
#             uploaded_file = request.files['contacts'] 
#             print("file")
#             print(uploaded_file.filename)
#             filepath = os.path.join(current_app.root_path, uploaded_file.filename)
#             uploaded_file.save(filepath)
#             with open(filepath, encoding='utf-8-sig') as file:
#                 csv_file = csv.reader(file)
#                 for row in csv_file:
#                     data.append(row[0])
#         print("contacts")
#         print(data)
#         number_messages = len(data)
#         # print(number_messages)
#         destination_json = json.dumps(data)
#         endPoint = 'https://api.mnotify.com/api/sms/quick'
#         apiKey = 'DGh55p4QDIFgIzskqW8unzHRhjHjnOJ1u07Apbq2T6iBG'
#         data = {
#         'recipient[]':data,
#         'sender': 'ChampLabs',
#         'message': message,
#         'is_schedule': False,
#         'schedule_date': " "
#         }
#         url = endPoint + '?key=' + apiKey
#         if credit_balance > number_messages:
#             response = requests.post(url, data)
#             response_data = response.json()
#             print(response_data)
#             response_status = response_data['status']
#             response_message = response_data['message']
#             response_code = response_data['code']
#             response_successful = response_data['summary']['numbers_sent']
#             response_successful_json = json.dumps(response_successful)
#             total_sent = response_data['summary']['total_sent']
#             total_rejected = response_data['summary']['total_rejected']
#             type = response_data['summary']['type']
#             api_id = response_data['summary']['_id']

#             # times=int(time)
#             # print(times)
#             # timed= datetime.datetime(time)
#             print("new time")
#             print(time)
#             tr = str(time)
#             td=tr[11:]
#             ts = datetime.datetime.now().timestamp()
#             print("ts")
#             print(ts)
#             print(td)
#             message_save = Message(message=message,
#                             source="source",
#                             type=type,response_status=response_status,destination_json = destination_json
#                             ,response_message=response_message,response_code=response_code,user_id=user_id,time= td,date=date,total_rejected=total_rejected,total_sent=total_sent,response_successful= response_successful,api_id=api_id)

#             db.session.add(message_save)
#             db.session.commit()
#             credit_rem = user.credit - number_messages
#             print("rem_credit")
#             print (credit_rem)
#             userrr = User.query.get_or_404(user_id)
#             userrr.credit = credit_rem
#             print(response_data['status'])
#             return response_data
#         else:
#             print("insufficient balance to send messages")
#             return redirect(url_for('core.packages'))
 


#     return render_template('message.html',messages=messages,form=form,phonebook_all=phonebook_all,user=user)

@core.route('/uploadrates',methods=['GET', 'POST'])
def uploadrates():
    form = RatesForm()
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    credit_balance = user.credit
    messages = Message.query.filter_by(user_id=user_id).all()
    phonebook_all= Phonebook.query.filter_by(user_id=user_id).all()
    data= []
    campaign_id = user.email[0:8]+ str(random.randint(1,1000))

    if request.method == 'POST':
        if form.uploadfile.data:

            uploaded_file = request.files['uploadfile'] 
            print("file")
            print(uploaded_file.filename)
            filepath = os.path.join(current_app.root_path, uploaded_file.filename)
            uploaded_file.save(filepath)
            with open(filepath, encoding='utf-8-sig') as file:
                csv_file = csv.reader(file)
                for row in csv_file:
                    data.append(row[0])
                    rates_save = Rate(code=row[0],cost=row[1],country=row[2],route=row[3])
                    db.session.add(rates_save)
                    db.session.commit()
        else:
            rates_save = Rate(code=form.code.data,cost=form.cost.data,country=form.country.data,route=form.route.data)
            db.session.add(rates_save)
            db.session.commit()
    return render_template('uploadrates.html',form=form,user=user)


@core.route('/addrates',methods=['GET', 'POST'])
def addrates():
    form = RatesForm()
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    credit_balance = user.credit
    messages = Message.query.filter_by(user_id=user_id).all()
    phonebook_all= Phonebook.query.filter_by(user_id=user_id).all()
    data= []
    campaign_id = user.email[0:8]+ str(random.randint(1,1000))
    rates = Rate.query.all()
    if request.method == 'POST':
        rates_save = Rate(code=form.code.data,cost=form.cost.data,country=form.country.data,route=form.route.data)
        db.session.add(rates_save)
        db.session.commit()

    return render_template('uploadrates.html',form=form,user=user,rates=rates)


@core.route('/rates',methods=['GET', 'POST'])
def rates():
    form = RatesForm()
    user = User.query.filter_by(email=session['email']).first()
    rates = Rate.query.all()

    return render_template('rates.html',user=user,rates=rates)



@core.route('/editrate/<int:rate_id>', methods=['GET', 'POST'])
@login_required
def editrate(rate_id):
    rate = Contact.query.get_or_404(rate_id)
    phonebooks = Phonebook.query.all()
    user = User.query.filter_by(email=session['email']).first()


    form = PhonebookForm()
    if request.method == 'POST':     
        rate.code = form.code.data
        rate.cost = form.cost.data
        rate.country = form.country.data
        rate.route = form.route.data
        db.session.commit() 
        print('updated')
        return redirect(url_for('core.addcontact'))

    elif request.method == 'GET':
        form.cost.data = rate.cost
        form.code.data = rate.code
        form.country.data = rate.country
        form.route.data = rate.route

    return render_template('editrate.html', form=form,rate=rate,phonebooks=phonebooks,user=user)

@core.route('/routemessage',methods=['GET', 'POST'])
def routemessage():
    form = MessageForm()
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    credit_balance = user.credit
    messages = Message.query.filter_by(user_id=user_id).all()
    phonebook_all= Phonebook.query.filter_by(user_id=user_id).all()
    data= []
    campaign_id = user.email[0:8]+ str(random.randint(1,1000))

    if request.method == 'POST':
        message = form.message.data
        date = form.date.data
        datee = form.date.data.strftime('%Y-%m-%d')
        len_message = len(message)
        if form.time.data:
            time = form.time.data
            # mytime = datetime.datetime.strptime(time,'%H%M').time()
            mytime = str(time)
            mydate = str(date)
            is_sch = True
            thedatetime = mydate + " " + mytime
         
        else:
            is_sch = False
            thedatetime = " "
     
        # phonebook_id = form
        if form.phonebook.data:
            # print("Phonebook id")
            # print(form.phonebook.data)
            phonebooky = Contact.query.filter_by(phonebook_id=form.phonebook.data).all()
            # print("Phonebooky")
            # print(phonebooky)
            for number in phonebooky:
                data.append(number.number)
        # destination_dict = []
        destinations = form.destination.data
        if "," in destinations:
            data = destinations.split(",")
        else:
            dat = form.destination.data
            data.append(dat)
        if form.contacts.data:
            uploaded_file = request.files['contacts'] 
            print("file")
            print(uploaded_file.filename)
            filepath = os.path.join(current_app.root_path, uploaded_file.filename)
            uploaded_file.save(filepath)
            with open(filepath, encoding='utf-8-sig') as file:
                csv_file = csv.reader(file)
                for row in csv_file:
                    data.append(row[0])
  
        number_messages = len(data)
        destination = data 
        message = form.message.data
        # http://rslr.connectbind.com:8080/bulksms/bulksms?username=dlp-testacc&password=tE$t1234&type=0&dlr=1&destination=233551660436&source=test&message=atest
        # print(number_messages)
        destination_json = json.dumps(data)
        url = 'http://rslr.connectbind.com:8080/bulksms/bulksms'
        apiKey = 'DGh55p4QDIFgIzskqW8unzHRhjHjnOJ1u07Apbq2T6iBG'
        data = {
            'username': 'dlp-testacc',
            'password': 'tE$t1234',
            'type':'0',
            'dlr':'1',
            'destination':destination,
            'source':'test',
            'message':message
        }
        response = requests.post(url, data)
        message_id = user.email[0:8]+ str(random.randint(1,1000))
        api_id = "q4rafshhhs"
        # response_data = response.json()
        # print("response_data")
        res = response.text.split("|")
        print(res[0])
        if len(res)>2:
            api_id = res[2]
        else:
            api_id = "null"
        # print(response_data)
        # if len(data)<2:
        message_save = Message(message=message,
                            source="routesms",type="schedule",response_status="response_status",destination_json = destination_json
                            ,response_message="ttest",response_code=res[0],user_id=user_id,total_sent="",response_successful="",date=mydate,time= mytime, total_rejected="",platform='fsfss',message_id=message_id,api_id=api_id)

        db.session.add(message_save)
        db.session.commit()
        if len(data)>1:
            for da in destination:
                # message_save = Message(message=message,
                #                 source="routesms",type="schedule",response_status="response_status",destination_json = da
                #                 ,response_message="ttest",response_code=res[0],user_id=user_id,total_sent="",response_successful="",date=mydate,time= mytime, total_rejected="",platform='fsfss',message_id=message_id,api_id=api_id)
                
                # db.session.add(message_save)
                # db.session.commit()
                sms_save = SMSReport(message_id = message_id, campaign_id = campaign_id, date = date, recepient = da, sender = "source", status = res[0],retries = 0,message=message,user_id=user_id)
            
                db.session.add(sms_save)
                db.session.commit()
        unfound_rates = []
        price = []
        p=0
        if len_message <151:
            multiplier = 1
            print('multipli')
            print(multiplier)
        elif len_message > 150 and len_message < 300 :
            
            multiplier = 2
            print('multipli')
            print(multiplier)
            
                    
        elif len_message > 300 and len_message <450:
            multiplier = 3
            print('multipli')
            print(multiplier)
        elif len_message > 450 and len_message < 600:
            multiplier = 4
            print('multipli')
            print(multiplier)
        
        print ('multiplier') 
        print (multiplier) 
        for dest in destination:
            dest_code = str(dest)
            dest_code = dest_code[:5]
            print("code")
            print(dest_code)
            rate_found = Rate.query.filter_by(code=dest_code).first()
            if rate_found:
                price.append(rate_found.cost)
                p += rate_found.cost
                p = p * multiplier
                # print(p)
                
            else:
                unfound_rates.append(dest)
        print(unfound_rates)
        print(p)
   

        user.balance = user.balance - p
        db.session.commit()
        print(user.balance) 




    return render_template('message.html',messages=messages,form=form,phonebook_all=phonebook_all,user=user)







@core.route('/message',methods=['GET', 'POST'])
@login_required
def message():
    form = MessageForm()
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    credit_balance = user.credit
    messages = Message.query.filter_by(user_id=user_id).all()
    phonebook_all= Phonebook.query.filter_by(user_id=user_id).all()
    data= []
    campaign_id = user.email[0:8]+ str(random.randint(1,1000))

    if request.method == 'POST':
        message = form.message.data
        date = form.date.data
        datee = form.date.data.strftime('%Y-%m-%d')
        if form.time.data:
            time = form.time.data
            # mytime = datetime.datetime.strptime(time,'%H%M').time()
            mytime = str(time)
            mydate = str(date)
            is_sch = True
            thedatetime = mydate + " " + mytime
            print("mytime")  
            print(thedatetime) 
        else:
            is_sch = False
            thedatetime = " "
            print("no time")
        print("date")  
        print(date) 
        # phonebook_id = form
        if form.phonebook.data:
            # print("Phonebook id")
            # print(form.phonebook.data)
            phonebooky = Contact.query.filter_by(phonebook_id=form.phonebook.data).all()
            # print("Phonebooky")
            # print(phonebooky)
            for number in phonebooky:
                data.append(number.number)
            print(data)
        # destination_dict = []
        destinations = form.destination.data
        if "," in destinations:
            data = destinations.split(",")
        else:
            dat = form.destination.data
            data.append(dat)
        if form.contacts.data:
            uploaded_file = request.files['contacts'] 
            print("file")
            print(uploaded_file.filename)
            filepath = os.path.join(current_app.root_path, uploaded_file.filename)
            uploaded_file.save(filepath)
            with open(filepath, encoding='utf-8-sig') as file:
                csv_file = csv.reader(file)
                for row in csv_file:
                    data.append(row[0])
        print("contacts")
        print(data)
        number_messages = len(data)
        # print(number_messages)
        destination_json = json.dumps(data)
        endPoint = 'https://api.mnotify.com/api/sms/quick'
        apiKey = 'DGh55p4QDIFgIzskqW8unzHRhjHjnOJ1u07Apbq2T6iBG'
        data = {
        'recipient[]':data,
        'sender': 'ChampLabs',
        'message': message,
        'is_schedule': False,
        'schedule_date': " "
        }
        url = endPoint + '?key=' + apiKey
        if credit_balance > number_messages:
            response = requests.post(url, data)
            response_data = response.json()
            print("response_data")
            print(response_data)
            response_status = response_data['status']
            response_message = response_data['message']
            response_code = response_data['code']
            response_successful = response_data['summary']['numbers_sent']
            response_successful_json = json.dumps(response_successful)
            total_sent = response_data['summary']['total_sent']
            total_rejected = response_data['summary']['total_rejected']
            type = response_data['summary']['type']
            api_id = response_data['summary']['_id']

            # times=int(time)
            # print(times)
            # timed= datetime.datetime(time)
            print("new time")
            print(time)
            tr = str(time)
            td=tr[11:]
            ts = datetime.datetime.now().timestamp()
            print("ts")
            print(ts)
            print(td)
            message_id = user.email[0:8]+ str(random.randint(1,1000000))

            message_save = Message(message=message,message_id=message_id,
                            source="source",
                            type=type,response_status=response_status,destination_json = destination_json
                            ,response_message=response_message,response_code=response_code,user_id=user_id,time= td,date=date,total_rejected=total_rejected,total_sent=total_sent,response_successful= response_successful,api_id=api_id,platform='mnotify')

            db.session.add(message_save)
            db.session.commit()
            credit_rem = user.credit - number_messages
            # print("rem_credit")
            # print (credit_rem)
            userrr = User.query.get_or_404(user_id)
            userrr.credit = credit_rem
            # print(response_data['status'])
            print("id")
            print(api_id)


            deliveredendPoint = 'https://api.mnotify.com/api/campaign/'   + api_id +'/delivered'

            apiKey = 'DGh55p4QDIFgIzskqW8unzHRhjHjnOJ1u07Apbq2T6iBG' 
            url = deliveredendPoint + '?key=' + apiKey
            response = urllib.request.urlopen(url)
            deliveredendPoint = response.read()
            dictdata = json.loads(deliveredendPoint)
            print(len(dictdata))
            print('del')
            print(dictdata)
            print(len(data['recipient[]']))
            # print(dictdata['report']['_id'])
            if dictdata['message'] == 'id supplied is incorrect':
                dict_rep = "No records found"
            if len(dictdata) > 2:  
                dict_rep = dictdata['report']
            if dict_rep  != "No records found":
                
                for i in range(0, len(data['recipient[]'])-1):
                    # item_q = udictdata['report'][i]['_id']
                    message_id = dictdata['report'][i]['_id']
                    campaign_id = dictdata['report'][i]['campaign_id']
                    date = dictdata['report'][i]['date_sent']
                    message = dictdata['report'][i]['message']
                    print(message)
                    recipient = dictdata['report'][i]['recipient']
                    retries = dictdata['report'][i]['retries']
                    sender = dictdata['report'][i]['sender']
                    status = dictdata['report'][i]['status']
                    sms_save = SMSReport(message_id = message_id, campaign_id = campaign_id, date = date, recepient = recipient, sender = sender, status = status,retries = 0,message=message,user_id=user_id)
            
                    db.session.add(sms_save)
                    db.session.commit()
                    print ("successful save")
            else:
                print ("no delivered found ")


            undeliveredendPoint = 'https://api.mnotify.com/api/campaign/'+ api_id +'/undelivered'
            apiKey = 'DGh55p4QDIFgIzskqW8unzHRhjHjnOJ1u07Apbq2T6iBG' 
            url = undeliveredendPoint + '?key=' + apiKey
            print(url)
            response = urllib.request.urlopen(url)
            undelivereddata = response.read()
            udictdata = json.loads(undelivereddata)

            print(len(udictdata))
            print("udata")
            print(udictdata)
            print(data)
            if dictdata['message'] == 'id supplied is incorrect':
                dict_rep = "No records found"
            if len(dictdata) > 2:  
                dict_rep = dictdata['report']
            if dict_rep  != "No records found":
            # if dictdata['report']  != "No records found":
                for i in range(0, 2):
                    # item_q = udictdata['report'][i]['_id']
                    message_id = udictdata['report'][i]['_id']
                    campaign_id = udictdata['report'][i]['campaign_id']
                    date = udictdata['report'][i]['date_sent']
                    message = udictdata['report'][i]['message']
                    print(message)
                    recipient = udictdata['report'][i]['recipient']
                    retries = udictdata['report'][i]['retries']
                    sender = udictdata['report'][i]['sender']
                    status = udictdata['report'][i]['status']
                    sms_save = SMSReport(message_id = message_id, campaign_id = campaign_id, date = date, recepient = recipient, sender = sender, status = status,retries = retries,message=message,user_id=user_id)
            
                    db.session.add(sms_save)
                    db.session.commit()
            else:
                print ("no undelivered found ")



        else:
            print("insufficient balance to send messages")
            return redirect(url_for('core.packages'))
 


    return render_template('message.html',messages=messages,form=form,phonebook_all=phonebook_all,user=user)





@core.route('/schedule_routesms',methods=['GET', 'POST'])
@login_required
def schedule_routesms():
    form = MessageForm()
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    credit_balance = user.credit
    messages = Message.query.filter_by(user_id=user_id).all()
    phonebook_all= Phonebook.query.filter_by(user_id=user_id).all()
    dataa= []
    if request.method == 'POST':
        message = form.message.data
        date = form.date.data
        datee = form.date.data.strftime('%Y-%m-%d')
        len_message = len(message)
        if form.time.data:
            time = form.time.data
            # mytime = datetime.datetime.strptime(time,'%H%M').time()
            mytime = str(time)
            mydate = str(date)
            is_sch = True
            thedatetime = mydate + " " + mytime
           
        else:
            is_sch = False
            thedatetime = " "
            print("no time")
     
        # phonebook_id = form
        if form.phonebook.data:
            # print("Phonebook id")
            # print(form.phonebook.data)
            phonebooky = Contact.query.filter_by(phonebook_id=form.phonebook.data).all()
            # print("Phonebooky")
            # print(phonebooky)
            for number in phonebooky:
                dataa.append(number.number)
            print(dataa)
        # destination_dict = []
        destinations = form.destination.data
        if "," in destinations:
            dataa = destinations.split(",")
        else:
            dat = form.destination.data
            dataa.append(dat)
        if form.contacts.data:
            uploaded_file = request.files['contacts'] 
            print("file")
            print(uploaded_file.filename)
            filepath = os.path.join(current_app.root_path, uploaded_file.filename)
            uploaded_file.save(filepath)
            with open(filepath, encoding='utf-8-sig') as file:
                csv_file = csv.reader(file)
                for row in csv_file:
                    dataa.append(row[0])
        print("contacts")
        print(dataa)
        number_messages = len(dataa)
        #  http://rslr.connectbind.com:8080/bulksms/bulksms?username=dlp-testacc&password=tE$t1234&type=0&dlr=1&destination=233551660436&source=test&message=atest
# http://rslr.connectbind.com:8080/bulksms/schedulesms?username=dlp-testacc&password=tE$t1234&message=TestingScheduleMsgAPI&type=0&dlr=1&source=TESTSM&destination=233551660436&date=10/10/2022&time=04:45%20pm&gmt=GMT
        destination_json = json.dumps(dataa)
        url = 'http://rslr.connectbind.com:8080/bulksms/schedulesms'
        apiKey = 'DGh55p4QDIFgIzskqW8unzHRhjHjnOJ1u07Apbq2T6iBG'
        data = {
            'username': 'dlp-testacc',
            'password': 'tE$t1234',
            'type':'0',
            'dlr':'1',
            'destination':dataa,
            'source':'test',
            'message':message,
            'date':'10/10/2022',
            'time':'4:59 pm',
            'gmt':'GMT'
        }
        response = requests.post(url, data)
        message_id = user.email[0:8]+ str(random.randint(1,1000))
        api_id = "q4rafshhhs"
        # response_data = response.json()
        print("response_data")
        print(response)
        res = response.text.split("|")
        print(res[0])
        if len(res)>1:
            api_id = res[2]
        else:
            api_id = "null"
        # print(response_data)
        message_save = Message(message=message,
                            source="routesms",type="schedule",response_status="response_status",destination_json = destination_json
                            ,response_message="ttest",response_code=res[0],user_id=user_id,total_sent="",response_successful="",date=mydate,time= mytime, total_rejected="",platform='fsfss',message_id=message_id,api_id=api_id)

        db.session.add(message_save)
        db.session.commit()
        if len(data)>1:


            for da in dataa:
            # message_save = Message(message=message,
            #                 source="routesms",type="schedule",response_status="response_status",destination_json = da
            #                 ,response_message="ttest",response_code=res[0],user_id=user_id,total_sent="",response_successful="",date=mydate,time= mytime, total_rejected="",platform='fsfss',message_id=message_id,api_id=api_id)

            # db.session.add(message_save)
            # db.session.commit()
                sms_save = SMSReport(message_id = message_id, campaign_id = "campaign_id", date = date, recepient = da, sender = "source", status = res[0],retries = 0,message=message,user_id=user_id)
            
                db.session.add(sms_save)
                db.session.commit()
        
        unfound_rates = []
        price = []
        p=0
        if len_message <151:
            multiplier = 1
            print('multipli')
            print(multiplier)
        elif len_message > 150 and len_message < 300 :       
            multiplier = 2
            print('multipli')
            print(multiplier)    
        elif len_message > 300 and len_message <450:
            multiplier = 3
            print('multipli')
            print(multiplier)
        elif len_message > 450 and len_message < 600:
            multiplier = 4
            print('multipli')
            print(multiplier)
        for dest in dataa:
            dest_code = str(dest)[:5]
            print("code")
            print(dest_code)
            rate_found = Rate.query.filter_by(code=dest_code).first()
            if rate_found:
                price.append(rate_found.cost)
                p += rate_found.cost
                p = p * multiplier
            else:
                unfound_rates.append(dest)
        user.balance = user.balance - p
        db.session.commit()
        print(user.balance) 
    return render_template('scheduleroutemessage.html',messages=messages,form=form,phonebook_all=phonebook_all,user=user)


@core.route('/schedule_message',methods=['GET', 'POST'])
@login_required
def schedule_message():
    form = MessageForm()
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    credit_balance = user.credit
    messages = Message.query.filter_by(user_id=user_id).all()
    phonebook_all= Phonebook.query.filter_by(user_id=user_id).all()
    data= []
    if request.method == 'POST':
        message = form.message.data
        date = form.date.data
        datee = form.date.data.strftime('%Y-%m-%d')
        len_message = len(message)
        if form.time.data:
            time = form.time.data
            # mytime = datetime.datetime.strptime(time,'%H%M').time()
            mytime = str(time)
            mydate = str(date)
            is_sch = True
            thedatetime = mydate + " " + mytime
            print("mytime")  
            print(thedatetime) 
        else:
            is_sch = False
            thedatetime = " "
            print("no time")
        print("date")  
        print(date) 
        # phonebook_id = form
        if form.phonebook.data:
            # print("Phonebook id")
            # print(form.phonebook.data)
            phonebooky = Contact.query.filter_by(phonebook_id=form.phonebook.data).all()
            # print("Phonebooky")
            # print(phonebooky)
            for number in phonebooky:
                data.append(number.number)
            print(data)
        # destination_dict = []
        destinations = form.destination.data
        if "," in destinations:
            data = destinations.split(",")
        else:
            dat = form.destination.data
            data.append(dat)
        if form.contacts.data:
            uploaded_file = request.files['contacts'] 
            print("file")
            print(uploaded_file.filename)
            filepath = os.path.join(current_app.root_path, uploaded_file.filename)
            uploaded_file.save(filepath)
            with open(filepath, encoding='utf-8-sig') as file:
                csv_file = csv.reader(file)
                for row in csv_file:
                    data.append(row[0])
        print("contacts")
        print(data)
        number_messages = len(data)
        print(number_messages)
        destination_json = json.dumps(data)
        endPoint = 'https://api.mnotify.com/api/sms/quick'
        apiKey = 'DGh55p4QDIFgIzskqW8unzHRhjHjnOJ1u07Apbq2T6iBG'
        data = {
        'recipient[]':data,
        'sender': 'ChampLabs',
        'message': message,
        'is_schedule': is_sch,
        'schedule_date': thedatetime
        }
        url = endPoint + '?key=' + apiKey
        if credit_balance > number_messages:
            response = requests.post(url, data)
            response_data = response.json()
            print(response_data)
            response_status = response_data['status']
            response_message = response_data['message']
            response_code = response_data['code']
            # response_successful = response_data['summary']['numbers_sent']
            # response_successful_json = json.dumps(response_successful)
            # total_sent = response_data['summary']['total_sent']
            # total_rejected = response_data['summary']['total_rejected']
            # type = response_data['summary']['type']
            # times=int(time)
            # print(times)
            # timed= datetime.datetime(time)
            print("new time")
            print(time)
            tx_ref = user.email[0:6]+  str(random.randint(1,1000))
            message_save = Message(message=message,
                            source="source",
                            type="schedule",response_status=response_status,destination_json = destination_json
                            ,response_message=response_message,response_code=response_code,user_id=user_id,total_sent="",response_successful="",date=mydate,time= mytime, total_rejected="",api_id=tx_ref)

            db.session.add(message_save)
            db.session.commit()
            
            if len_message <151:
                multiplier = 1
                print('multipli')
                print(multiplier)
            elif len_message > 150 and len_message < 300 :       
                multiplier = 2
                print('multipli')
                print(multiplier)    
            elif len_message > 300 and len_message <450:
                multiplier = 3
                print('multipli')
                print(multiplier)
            elif len_message > 450 and len_message < 600:
                multiplier = 4
                print('multipli')
                print(multiplier)
            num_messages = multiplier * number_messages
            credit_rem = user.credit - num_messages
            print("rem_credit")
            print(user.credit)
            print (credit_rem)
            userrr = User.query.get_or_404(user_id)
            userrr.credit = credit_rem
            print(response_data['status'])
            return response_data
        else:
            print("insufficient balance to send messages")
            return redirect(url_for('core.packages'))
 


    return render_template('schedulemessage.html',messages=messages,form=form,phonebook_all=phonebook_all,user=user)




@core.route('/mycontacts', methods=['GET', 'POST'])
@login_required
def mycontacts():
    form = ContactForm()
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    contacts = Contact.query.filter_by(user_id=user_id).all()

    return render_template('userportal/mycontacts.html',contacts=contacts,form=form,user=user)


@core.route('/myreports', methods=['GET', 'POST'])
@login_required
def myreports():
    form = ContactForm()
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    reports = Message.query.filter_by(user_id=user_id).all()

    return render_template('userportal/myreports.html',messages=reports,form=form,user=user)


@core.route('/myphonebooks', methods=['GET', 'POST'])
@login_required
def myphonebooks():
    form = ContactForm()
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    reports = Message.query.filter_by(user_id=user_id).all()
    phonebooks = Phonebook.query.filter_by(user_id=user.id).all()

    return render_template('userportal/myphonebooks.html',phonebooks=phonebooks,form=form,user=user)


@core.route('/addcontact', methods=['GET', 'POST'])
@login_required
def addcontact():
    form = ContactForm()
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    contacts = Contact.query.filter_by(user_id=user_id).all()

    phonebooks = Phonebook.query.all()
    # genre = request.form.get('geenre')
    if request.method == 'POST':
        name = form.name.data
        number = form.number.data
        phonebook = form.phonebook.data
        print("phonebook")
        print(phonebook)
        contact_save = Contact(name=name,
                        number=number,phonebook_id=phonebook,user_id=user_id)
        db.session.add(contact_save)
        db.session.commit()
        print("saved")
        return redirect(url_for('core.addcontact'))


    return render_template('addcontact.html',form=form,phonebooks=phonebooks,user=user,contacts=contacts)




@core.route('/uploadcontacts', methods=['GET', 'POST'])
@login_required
def uploadcontacts():
    form = ContactForm()
    phonebooks = Phonebook.query.all()

    user = User.query.filter_by(email=session['email']).first()
    user_id= user.id
    contacts = Contact.query.filter_by(user_id=user_id).all()

    if request.method == 'POST':
        phonebook = form.phonebook.data
        if form.contacts.data:
            uploaded_file = request.files['contacts'] 
            print("file")
            print(uploaded_file.filename)
            filepath = os.path.join(current_app.root_path, uploaded_file.filename)
            uploaded_file.save(filepath)
            with open(filepath, encoding='utf-8-sig') as file:
                csv_file = csv.reader(file)
                for row in csv_file:
                    number= row[0]
                    name = row[1]
                    # print("contacts")
                    # print(number)
                    # print(name)
                    contact_save = Contact(name=name,
                                    number=number,phonebook_id=phonebook)
                    db.session.add(contact_save)
                    db.session.commit()
                    return redirect(url_for('core.addcontact'))

        print("saved")
    return render_template('uploadcontact.html',form=form,phonebooks=phonebooks,user=user,contacts=contacts)







@core.route('/editcontact/<int:contact_id>', methods=['GET', 'POST'])
@login_required
def editcontact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    phonebooks = Phonebook.query.all()
    user = User.query.filter_by(email=session['email']).first()


    form = PhonebookForm()
    if request.method == 'POST':     
        contact.name = form.name.data
        contact.number = form.number.data
        contact.phonebook_id = form.phonebook.data
        db.session.commit() 
        print('updated')
        return redirect(url_for('core.addcontact'))

    elif request.method == 'GET':
        form.name.data = contact.name
        form.number.data = contact.number
        form.phonebook.data = contact.phonebook_id
    return render_template('updatecontact.html', form=form,contact=contact,phonebooks=phonebooks,user=user)






@core.route('/editphonebook/<int:phonebook_id>', methods=['GET', 'POST'])
@login_required
def editphonebook(phonebook_id):
    phonebook = Phonebook.query.get_or_404(phonebook_id)
    phonebooks = Phonebook.query.all()
    form = PhonebookForm()
    user = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':     
        phonebook.name = form.name.data
        db.session.commit()
        print('updated')
        return redirect(url_for('core.addphonebook'))
    elif request.method == 'GET':
        form.name.data = phonebook.name
    return render_template('updatephonebook.html', form=form,phonebook=phonebook,user=user)

@core.route('/phonebook/<int:phonebook_id>')
@login_required
def phonebook(phonebook_id):
    user = User.query.filter_by(email=session['email']).first()

    contacts = Contact.query.filter_by(phonebook_id=phonebook_id).all()
    return render_template('phonebook.html', contacts=contacts,user=user)





@core.route('/phonebook', methods=['GET', 'POST'])
@login_required
def addphonebook():
    user = User.query.filter_by(email=session['email']).first()

    form = PhonebookForm()
    phonebooks = Phonebook.query.filter_by(user_id=user.id)
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    # genre = request.form.get('geenre')
    if request.method == 'POST':
        name = form.name.data
        phonebook_save = Phonebook(name=name,user_id=user_id,numberofcontacts=+0
                       )
        db.session.add(phonebook_save)
        db.session.commit()
        print("saved")
        return redirect(url_for('core.addphonebook'))


    return render_template('addphonebook.html',form=form,phonebooks=phonebooks,user=user)



@core.route("/delete_phonebook/<int:phonebook_id>", methods=['POST','GET'])
@login_required
def delete_phonebook(phonebook_id):
    contacts = Contact.query.filter_by(phonebook_id=phonebook_id).all()
    phonebook = Phonebook.query.get_or_404(phonebook_id)
    db.session.delete(phonebook)
    db.session.commit()
    for contact in contacts:
        db.session.delete(contact)
        db.session.commit()


    # flash('Post has been deleted')
    return redirect(url_for('core.index'))


@core.route("/delete_contact/<int:contact_id>", methods=['POST','GET'])
@login_required
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    # flash('Post has been deleted')
    return redirect(url_for('core.index'))




@core.route("/delete_batch", methods=['POST','GET'])
@login_required
def delete_batch():

    if request.method == 'POST':
        ids = request.form.getlist('mycheckbox')
        print('ids')
        print(ids)
        for id in ids:
            contact = Contact.query.get_or_404(id)
            db.session.delete(contact)
            # for getid in request.form.getlist('mycheckbox'):  
            db.session.commit()
    # flash('Post has been deleted')
    return redirect(url_for('core.index'))




@core.route('/packages')
@login_required
def packages():
    # price = Package.query.get_or_404(id)
    packages = Package.query.all()
    userdemail = session['email']
    user =  User.query.filter_by(email=userdemail).first()
    name = user.name
    number = user.number
    # random_num = randint(1,1000)
    tx_ref = user.email[0:6]+ str(random.randint(1,1000))
    # tid = tid
    return render_template('choosepackage.html',packages=packages,useremail=userdemail,tx_reff=tx_ref,name=name,number=number,user=user)



@core.route("/confirmplan/<int:id>")
@login_required
def confirmplan(id):
    # price = Price.query.get_or_404(id)
    # loggeduser = session['email']
    # print("ogged:")
    # print(loggeduser)
    # user = User.query.filter_by(email=loggeduser).first()
    #         # user = User.query.filter_by(email=form.email.data).first()

    # print(user)
    # user.plan_id = id
    # user.rem_sessions = price.numsessions
    # user.rem_chatweeks = price.numchatweeks
    # db.session.commit()

    return redirect(url_for('core.index'))


@core.route("/confirmravepayment")
@login_required
def confirmravepayment():
    user = User.query.filter_by(email=session['email']).first()
    uid = user.id
    
    if request.args.get('status') == "successful":
        transaction_id = request.args.get('transaction_id')
        # user = User.query.filter_by(email=session['email']).first()
        status = request.args.get('status')
        tx_ref = request.args.get('tx_ref')
        amount = request.args.get('amount')
        # tid = request.args.get('tid')
        # print(tid)
        amount_dict = amount.split(' ')
        price = amount_dict[0]
        plan = Package.query.filter_by(amount=amount).first()
        sms = plan.sms
        current_balance = user.credit
        user.credit = current_balance + sms 
        # user.plan_id = plan.id
        print(plan.title)
        print(amount_dict)
        print(amount)
        payment = Payment(transaction_id=transaction_id,
                             tx_ref=tx_ref,
                             user_id =uid,status=status,amount=price,package_id = plan.id
                             )
        db.session.add(payment)
        db.session.commit()

        # flash("Pricing Created")
        return redirect(url_for('core.packages'))
    
    
    
@core.route('/adduser',methods=['GET','POST'])
def adduser():
    form = RegistrationForm()
    user = User.query.filter_by(email=session['email']).first()
    users = User.query.all()

    if request.method == 'POST':
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    name=form.name.data,
                    number=form.number.data,
                    routesms = form.routesms.data, mnotify = form.mnotify.data,role=form.role.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('core.index'))

    return render_template('adminportal/adduser.html',form=form,user=user,users=users)





@core.route('/edituser/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edituser(user_id):
    theuser = User.query.get_or_404(user_id)
    users = User.query.all()
    form = RegistrationForm()
    user = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':     
        theuser.name = form.name.data
        theuser.email =form.email.data
        theuser.username=form.username.data
        theuser.name=form.name.data
        theuser.number=form.number.data
        theuser.routesms = form.routesms.data
        theuser.mnotify = form.mnotify.data
        theuser.role=form.role.data
        db.session.commit()
        print('updated')
        return redirect(url_for('core.adduser'))
    elif request.method == 'GET':
        form.name.data = theuser.name
        form.email.data = theuser.email
        form.username.data = theuser.username
        form.number.data = theuser.number
        form.routesms.data = theuser.routesms
        form.mnotify.data = theuser.mnotify
        form.role.data = theuser.role
    return render_template('adminportal/edituser.html', form=form,theuser=theuser,user=user)

@core.route("/delete_user/<int:user_id>", methods=['POST','GET'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    # flash('Post has been deleted')
    return redirect(url_for('core.index'))


@core.route('/topup/<int:user_id>', methods=['GET', 'POST'])
@login_required
def topup(user_id):
    theuser = User.query.get_or_404(user_id)
    users = User.query.all()
    form = RegistrationForm()
    print(user_id)
    user = User.query.filter_by(email=session['email']).first()
    if request.method == 'POST':     
        theuser.balance = theuser.balance + int(form.amount.data)
        db.session.commit()
        print('updated')
        return redirect(url_for('core.adduser'))
    return redirect(url_for('core.adduser'))
    

