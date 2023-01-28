#models.py
from urllib import response
from structure import db,login_manager,app
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),nullable=True)
    date = db.Column(db.Date,nullable=True,default=datetime.utcnow)
    number = db.Column(db.Integer,nullable=True)
    profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    credit = db.Column(db.Integer,nullable=True,default=0)
    balance = db.Column(db.Float,nullable=True,default=0)
    mnotify = db.Column(db.String(255),nullable=True,default="no")
    routesms = db.Column(db.String(255),nullable=True,default="yes")
    role = db.Column(db.String(128),nullable=True,default="user")


    def __init__(self,email,username,password,name,number,role,mnotify,routesms):
        self.email = email
        self.username = username
        self.name = name
        self.number = number
        self.password_hash = generate_password_hash(password)
        self.role = role
        self.mnotify = mnotify
        self.routesms = routesms
        
        # self.credit = credit

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    # def check_credit(self,credit):
    #     return (self.credit)

    def __repr__(self):
        return f"Username {self.username}"


class Topup(db.Model):
    __tablename__= "topups"


    id = db.Column(db.Integer,primary_key=True)
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)
    users= db.relationship('User',backref='topups',lazy=True)    
    date = db.Column(db.Date,nullable=True,default=datetime.utcnow)
    status = db.Column(db.String(255),nullable=True)
    transaction_id = db.Column(db.String(255))
    reference = db.Column(db.String(255))
    
    
    
class Message(db.Model):
    __tablename__= "messages"


    id = db.Column(db.Integer,primary_key=True)
    message = db.Column(db.String(64))
    source = db.Column(db.String(64))
    date = db.Column(db.String(64))
    time = db.Column(db.String(64))

    type = db.Column(db.Integer,default="sms")
    destination = db.Column(db.Integer)
    destination_json = db.Column(db.JSON,nullable=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)
    users= db.relationship('User',backref='messages',lazy=True)    
    response_code = db.Column(db.String(20))
    response_message = db.Column(db.String(190))
    response_status = db.Column(db.String(20))
    response_successful = db.Column(db.JSON,nullable=True)
    total_sent = db.Column(db.String(20))
    total_rejected = db.Column(db.String(20))
    api_id = db.Column(db.String(100))
    message_id = db.Column(db.String(50))
    platform = db.Column(db.String(30))
    cost = db.Column(db.Integer)



    def __init__(self,message,source,type,user_id,response_code,response_message,response_status,destination_json,response_successful,total_sent,total_rejected,date,time,api_id,message_id,platform,cost):
        self.message = message
        self.source = source
        self.type = type
        # self.destination = destination
        self.user_id = user_id
        self.response_code = response_code
        self.response_message= response_message
        self.response_status = response_status
        self.destination_json = destination_json
        self.response_successful = response_successful
        self.total_sent = total_sent
        self.total_rejected = total_rejected
        self.time = time
        self.date = date
        self.api_id = api_id
        self.message_id = message_id
        self.platform = platform
        self.cost = cost
 

    def __repr__(self):
        return f"Message {self.message} {self.source} {self.type} {self.dest}"




class SMSReport(db.Model):
    __tablename__= "smsreports"


    id = db.Column(db.Integer,primary_key=True)
    message_id = db.Column(db.String(64))
    campaign_id = db.Column(db.String(64))
    date = db.Column(db.String(64))
    message = db.Column(db.String(64))
    recepient = db.Column(db.String(64))
    retries = db.Column(db.String(64))
    sender = db.Column(db.String(64))
    status = db.Column(db.String(64))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)
    users= db.relationship('User',backref='smsreports',lazy=True)
    cost = db.Column(db.Integer)




    def __init__(self,message_id,campaign_id,date,message,recepient,retries,sender,status,user_id,cost):
        self.message_id = message_id
        self.campaign_id = campaign_id
        self.message = message
        self.date = date
        self.recepient = recepient
        self.retries = retries
        self.sender = sender
        self.status = status
        self.user_id = user_id
        self.cost = cost
        


    def __repr__(self):
        return f"Message {self.message} "



class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    date = db.Column(db.Date,nullable=True,default=datetime.utcnow)
    number = db.Column(db.Integer)
    phonebook_id = db.Column(db.Integer,db.ForeignKey('phonebooks.id'),nullable=True)
    phonebooks= db.relationship('Phonebook',backref='contacts',lazy=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)
    users= db.relationship('User',backref='contacts',lazy=True)
            

    def __init__(self,name,number,phonebook_id,user_id):
        self.name = name
        self.number = number
        self.phonebook_id = phonebook_id
        self.user_id = user_id

    def __repr__(self):
        return f"Contact {self.name} {self.number} "



class Phonebook(db.Model):
    __tablename__ = "phonebooks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    numberofcontacts = db.Column(db.Integer,default=0,nullable=True)
    date = db.Column(db.Date,nullable=True,default=datetime.utcnow)

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)
    users= db.relationship('User',backref='phonebooks',lazy=True)    

    def __init__(self,name,numberofcontacts,user_id):
        self.name = name
        self.numberofcontacts = numberofcontacts
        self.user_id = user_id

    def __repr__(self):
        return f"Phonebook {self.name} {self.numberofcontacts} "





class Package(db.Model):
    __tablename__ = "packages"


    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(140),nullable=False)
    amount = db.Column(db.Text,nullable=False)
    features = db.Column(db.Text(64),nullable=False,default='default_profile.png')
    sms = db.Column(db.Integer,nullable= True,default=0)


    def __init__(self,title,amount,features,sms):
        self.title = title
        self.amount = amount
        self.features = features 
        self.sms = sms


    def __repr__(self):
        return f"Post ID: {self.id} -- {self.title}"



class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer,primary_key=True)
    amount = db.Column(db.Integer,nullable=True)
    date = db.Column(db.Date,nullable=True,default=datetime.utcnow)
    tx_ref = db.Column(db.String)
    transaction_id = db.Column(db.String)
    package_id = db.Column(db.Integer,db.ForeignKey('packages.id'),nullable=True)
    packages = db.relationship('Package',backref='payments',lazy=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)
    users = db.relationship('User',backref='payments',lazy=True)
    status = db.Column(db.String,nullable=True,default="Failed")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)




class SenderId(db.Model):
    __tablename__ = 'senderids'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    status = db.Column(db.String,nullable=True,default="Failed")
    api_status = db.Column(db.String,nullable=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)
    users = db.relationship('User',backref='senderids',lazy=True)

    def __init__(self,name,description,status,api_status,user_id):
        self.name = name
        self.description = description
        self.status = status
        self.api_status = api_status
        self.user_id = user_id


class Rate(db.Model):
    __tablename__ = 'rates'
    id = db.Column(db.Integer,primary_key=True)
    code = db.Column(db.String(10),nullable=True)
    cost = db.Column(db.Integer,nullable=True)
    country = db.Column(db.String(10),nullable=True)
    route = db.Column(db.String(30),nullable=True)

    def __init__(self,code, country,cost,route):
        self.code = code
        self.country = country
        self.cost = cost
        self.route = route



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
