from datetime import datetime as dt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class role(db.Model):
	__tablename__ = 'role'
	idrole = db.Column(db.Integer, primary_key=True, autoincrement=True)
	role = db.Column(db.String(30), nullable=False, unique=True)

	__table_args__ = (db.UniqueConstraint('role', name='_role_uc'),)

	def __init__(self, idrole, role):
		self.idrole = idrole
		self.role = role
	
	def __repr__(self):
		return "<task %r>" % self.idrole
    
def defaultroles():
	try:
		userrole = role(idrole=1, role='user')
		db.session.add(userrole)
		db.session.commit()
		print('role user inserted')
	except:
		print('Error')

	try:
		adminrole = role(idrole=2, role='admin')
		db.session.add(adminrole)
		db.session.commit()
		print('role admin inserted')
	except:
		print('Error')

class user(db.Model):
    __tablename__ = 'user'
    iduser = db.Column(db.Integer, primary_key=True, autoincrement=True, default=0)
    name = db.Column(db.String(45), nullable=False)
    surname = db.Column(db.String(45), nullable=False)
    username = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)    
    salt = db.Column(db.String(20), nullable=False, unique=True)
    usertype = db.Column(db.Integer, db.ForeignKey('role.idrole'), nullable=False)
    creationdate = db.Column(db.DateTime, default=dt.utcnow, nullable=False)
    
    def __init__(self, name, surname, username, email, password, salt, usertype=1):
        self.name = name
        self.surname = surname
        self.username = username
        self.email = email
        self.password = password
        self.salt = salt
        self.usertype = usertype

    def __repr__(self):
        return "<task %r>" % self.iduser	
    
class file(db.Model):
	__tablename__ = 'file'
	idfile = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(45), nullable=False)
	category = db.Column(db.String(20), nullable=False)
	extension = db.Column(db.String(45), nullable=False)
	iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)
	

	def __init__(self, name, category, extension, iduser, datecreated):
		self.name = name
		self.category = category
		self.extension = extension
		self.iduser = iduser
		self.datecreated = datecreated

	def __repr__(self):
		return "<task %r>" % self.idfile   
	
class detailsfile(db.Model):
    __tablename__ = 'detailsfile'
    idDetailsfile = db.Column(db.Integer, primary_key=True, autoincrement=True)
    iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)
    idfile = db.Column(db.Integer, db.ForeignKey('file.idfile'), primary_key=True)
    datecreated = db.Column(db.DateTime, default=dt.utcnow, nullable=False)

    def __init__(self, idfile, iduser, datecreated):
        self.iduser = iduser
        self.idfile = idfile
        self.datecreated = datecreated

    def __repr__(self):
        return "<task %r>" % self.idDetailsfile


class historial(db.Model):
	__tablename__ = 'historial'
	idchange = db.Column(db.Integer, primary_key=True, autoincrement=True)
	idfile = db.Column(db.Integer, db.ForeignKey('file.idfile'), primary_key=True)
	datemodified = db.Column(db.String(30), nullable=False)
	iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)
	idmodificationtype = db.Column(db.Integer, nullable=False)


	def __init__(self, idfile, datemodified, iduser, idmodificationtype):
		self.idfile = idfile
		self.datemodified = datemodified
		self.iduser = iduser
		self.idmodificationtype = idmodificationtype


	def __repr__(self):
		return "<task %r>" % self.idchange

class change(db.Model):
    __tablename__ = 'change'
    idcambio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    beforechange = db.Column(db.Integer, nullable=False)
    afterchange = db.Column(db.Integer, nullable=False)
    changeline = db.Column(db.Integer, nullable=False)
    changecolumn = db.Column(db.Integer, nullable=False)
    idchange = db.Column(db.Integer, db.ForeignKey('historial.idchange'), primary_key=True)

    def __init__(self, beforechange, afterchange, changeline, changecolumn):
        self.beforechange = beforechange
        self.afterchange = afterchange
        self.changeline = changeline
        self.changecolumn = changecolumn

    def __repr__(self):
        return "<task %r>" % self.idcambio


class version(db.Model):
	__tablename__ = 'version'
	idversion = db.Column(db.Integer, primary_key=True, autoincrement=True)
	idfile = db.Column(db.Integer, db.ForeignKey('file.idfile'), nullable=False)
	datecreated = db.Column(db.DateTime, default=dt.utcnow)

	def __init__(self, idfile, datecreated):
		self.idfile = idfile
		self.datecreated = datecreated

	def __repr__(self):
		return "<task %r>" % self.idversion

class error(db.Model):
	__tablename__ = 'error'
	iderror = db.Column(db.Integer, primary_key=True, autoincrement=True)
	iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)
	idfile = db.Column(db.Integer, db.ForeignKey('file.idfile'), nullable=False)
	description = db.Column(db.String(255), nullable=False)
	datereported = db.Column(db.DateTime, default=dt.utcnow)
	
	def __init__(self, iduser, idfile, description, datereported):
		self.iduser = iduser
		self.idfile = idfile
		self.description = description
		self.datereported = datereported

	def __repr__(self):
		return "<task %r>" % self.iderror
	
class licence(db.Model):
	__tablename__ = 'licence'
	idlicence = db.Column(db.Integer, primary_key=True, autoincrement=True)
	plan = db.Column(db.String(100), nullable=False)
	price = db.Column(db.Float, nullable=False)
	packages = db.Column(db.String(45), nullable=False)


	def __init__(self, plan, price, packages):
		self.plan = plan
		self.price = price
		self.packages = packages

	def __repr__(self):
		return "<task %r>" % self.idlicence

class detailsLicence(db.Model):
    __tablename__ = 'detailslicence'
    idDetailslicence = db.Column(db.Integer, primary_key=True, autoincrement=True)
    taxes = db.Column(db.Float, nullable=False)
    totalprice = db.Column(db.Float, nullable=False)
    idlicence = db.Column(db.Integer, db.ForeignKey('licence.idlicence'), nullable=False)

    def __init__(self, idlicence, taxes, totalprice):
        self.taxes = taxes
        self.totalprice = totalprice
        self.idlicence = idlicence

    def __repr__(self):
        return "<task %r>" % self.idDetailslicence

	
class comment(db.Model):
	__tablename__ = 'comment'
	idcomment = db.Column(db.Integer, primary_key=True, autoincrement=True)
	iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)
	idfile = db.Column(db.Integer, db.ForeignKey('file.idfile'), nullable=False)
	line = db.Column(db.Integer, nullable=False)
	comment = db.Column(db.Text, nullable=False)
	
	def __init__(self, iduser, idfile, line, comment):
		self.iduser = iduser
		self.idfile = idfile
		self.line = line
		self.comment = comment

	def __repr__(self):
		return "<task %r>" % self.idcomment
	
class preference(db.Model):
	__tablename__ = 'preference'
	idpreference = db.Column(db.Integer, primary_key=True, autoincrement=True)
	iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)
	fontsize = db.Column(db.Float, nullable=False)
	profile = db.Column(db.String(45), nullable=False)
	autosave = db.Column(db.Boolean, nullable=False)
	lang = db.Column(db.String(3), nullable=False)

	def __init__(self, iduser,  fontsize, profile, autosave, lang):
		self.iduser = iduser
		self.fontsize = fontsize
		self.profile = profile
		self.autosave = autosave
		self.lang = lang

	def __repr__(self):
		return "<task %r>" % self.idpreference

class preferences(db.Model):
    __tablename__ = 'preferences'
    idcolour = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idpreference = db.Column(db.Integer, db.ForeignKey('preference.idpreference'), nullable=False)
    iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)
    bkgcolour = db.Column(db.String(45), nullable=False)
    font = db.Column(db.String(45), nullable=False)
    fontcolour = db.Column(db.String(45), nullable=False)

    def __init__(self, iduser, bkgcolour, font, fontcolour, idpreference):
        self.iduser = iduser
        self.bkgcolour = bkgcolour
        self.font = font
        self.fontcolour = fontcolour
        self.idpreference = idpreference

    def __repr__(self):
        return "<task %r>" % self.idcolour

class paytransaction(db.Model):
	__tablename__ = 'paytransaction'
	idpaytransaction = db.Column(db.Integer, primary_key=True, autoincrement=True)
	iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)
	idlicence = db.Column(db.Integer, db.ForeignKey('licence.idlicence'), nullable=False)
	amount = db.Column(db.Float, nullable=False)
	datepaid = db.Column(db.DateTime, default=dt.utcnow)

	def __init__(self, iduser, idlicence, amount, datepaid):
		self.iduser = iduser
		self.idlicence = idlicence
		self.amount = amount
		self.datepaid = datepaid

	def __repr__(self):
		return "<task %r>" % self.idpaytransaction
	
class sessions(db.Model):
	__tablename__ = 'sessions'
	idsession = db.Column(db.Integer, primary_key=True, autoincrement=True)
	iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)
	datelogged = db.Column(db.DateTime, default=dt.utcnow)

	def __init__(self, iduser):
		self.iduser = iduser

	def __repr__(self):
		return "<task %r>" % self.idsession


