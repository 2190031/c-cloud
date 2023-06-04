from datetime import datetime as dt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class role(db.Model):
	__tablename__ = 'role'
	idrole = db.Column(db.Integer, primary_key=True, autoincrement=True)
	role = db.Column(db.String(30), nullable=False, unique=True)

	__table_args__ = (db.UniqueConstraint('role', name='_role_uc'),)

	def __init__(self, role):
		self.role = role
	
	def __repr__(self):
		return "<task %r>" % self.idrole
    
def defaultroles():
	try:
		userrole = role(role='user')
		db.session.add(userrole)
		db.session.commit()
		print('role user inserted')
	except:
		print('')

	try:
		adminrole = role(role='admin')
		db.session.add(adminrole)
		db.session.commit()
		print('role admin inserted')
	except:
		print('')

class user(db.Model):
    __tablename__ = 'user'
    iduser = db.Column(db.Integer, primary_key=True, autoincrement=True, default=0)
    google_id = db.Column(db.String(100), nullable=True, unique=True)
    name = db.Column(db.String(45), nullable=False)
    surname = db.Column(db.String(45), nullable=True)
    username = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=True)
    picture = db.Column(db.String(255), nullable=True)    
    salt = db.Column(db.String(100), nullable=True, unique=True)
    usertype = db.Column(db.Integer, db.ForeignKey('role.idrole'), nullable=False)
    creationdate = db.Column(db.DateTime, default=dt.utcnow, nullable=False)
    
    def __init__(self, name, surname, username, email, password, salt, picture=None, usertype=1, google_id=None):
        self.name = name
        self.surname = surname
        self.username = username
        self.email = email
        self.password = password
        self.picture = picture
        self.salt = salt
        self.usertype = usertype
        self.google_id = google_id

    def __repr__(self):
        return "<task %r>" % self.iduser	
    
class file(db.Model):
	__tablename__ = 'file'
	idfile = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(45), nullable=False)
	category = db.Column(db.String(20), nullable=False)
	extension = db.Column(db.String(45), nullable=False)

	def __init__(self, name, category, extension):
		self.name = name
		self.category = category
		self.extension = extension

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
	datemodified = db.Column(db.DateTime, default=dt.utcnow, nullable=False)
	iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)
	# idmodificationtype = db.Column(db.Integer, nullable=False)


	def __init__(self, idfile, datemodified, iduser
            #   , idmodificationtype
              ):
		self.idfile = idfile
		self.datemodified = datemodified
		self.iduser = iduser
		# self.idmodificationtype = idmodificationtype


	def __repr__(self):
		return "<task %r>" % self.idchange

# revisar
class change(db.Model):
    __tablename__ = 'change'
    idmodification = db.Column(db.Integer, primary_key=True, autoincrement=True)
    beforechange = db.Column(db.Integer, nullable=False)
    afterchange = db.Column(db.Integer, nullable=False)
    # changeline = db.Column(db.Integer, nullable=False)
    # changecolumn = db.Column(db.Integer, nullable=False) # implementar despues
    idchange = db.Column(db.Integer, db.ForeignKey('historial.idchange'), primary_key=True)

    def __init__(self, beforechange, afterchange, changeline, changecolumn):
        self.beforechange = beforechange
        self.afterchange = afterchange
        # self.changeline = changeline
        # self.changecolumn = changecolumn

    def __repr__(self):
        return "<task %r>" % self.idmodification


#No uso por ahora
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
	# idfile = db.Column(db.Integer, db.ForeignKey('file.idfile'), nullable=False)
	description = db.Column(db.String(255), nullable=False)
	datereported = db.Column(db.DateTime, default=dt.utcnow)
	
	def __init__(self, iduser, 
            #   idfile, 
              description, datereported):
		self.iduser = iduser
		# self.idfile = idfile
		self.description = description
		self.datereported = datereported

	def __repr__(self):
		return "<task %r>" % self.iderror
	
class licence(db.Model):
	__tablename__ = 'licence'
	idlicence = db.Column(db.Integer, primary_key=True, autoincrement=True)
	plan = db.Column(db.String(100),nullable=False,unique=True)
	price = db.Column(db.Float,nullable=False)
	max_storage_mb = db.Column(db.Integer,nullable=False)
	support_24_7 = db.Column(db.Boolean,nullable=False)
	automatic_backups = db.Column(db.Boolean,nullable=False)
	secure_access = db.Column(db.Boolean,nullable=False)
	file_capacity = db.Column(db.Integer,nullable=False)

	def __init__(self, plan, price, max_storage_mb, support_24_7, automatic_backups, secure_access, file_capacity):
		self.plan = plan
		self.price = price
		self.max_storage_mb = max_storage_mb
		self.support_24_7 = support_24_7
		self.automatic_backups = automatic_backups
		self.secure_access = secure_access
		self.file_capacity = file_capacity

	def __repr__(self):
		return "<task %r>" % self.idlicence

def defaultlicence():
    try:
        licence1 = licence(plan='Plan Premium', price=19.99, max_storage_mb=51200, support_24_7=True, automatic_backups=True, secure_access=True, file_capacity=5000)
        db.session.add(licence1)
        db.session.commit()
        print('Plan Premium inserted')
    except Exception as e:
        print('')

    try:
        licence2 = licence(plan='Plan Estandar', price=9.99, max_storage_mb=25600, support_24_7=True, automatic_backups=False, secure_access=True, file_capacity=50)
        db.session.add(licence2)
        db.session.commit()
        print('Plan Estandar inserted')
    except Exception as e:
       print('')


    try:
        licence3 = licence(plan='Plan Gratuito', price=0, max_storage_mb=500, support_24_7=False, automatic_backups=False, secure_access=True, file_capacity=5)
        db.session.add(licence3)
        db.session.commit()
        print('Plan Gratuito inserted')
    except Exception as e:
        print('')

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

#reparar
class preference(db.Model):
	__tablename__ = 'preference'
	idpreference = db.Column(db.Integer, primary_key=True, autoincrement=True)
	iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)
	profile_picture = db.Column(db.String(45), nullable=True)
	font = db.Column(db.String(45), nullable=True)
	fontsize = db.Column(db.Float, nullable=True)
	fontcolor = db.Column(db.String(7), nullable=True) # hex
	theme = db.Column(db.String(45), nullable=True)
	# autosave = db.Column(db.Boolean, nullable=False)
	# lang = db.Column(db.String(3), nullable=False)

	def __init__(self, iduser,  fontsize, profile,
            # autosave, lang,
            font, 
            # fontcolor, 
            theme):
		self.iduser = iduser
		self.profile_picture = profile
		self.font = font
		self.fontsize = fontsize
		self.theme = theme
		# self.autosave = autosave
		# self.lang = lang

	def __repr__(self):
		return "<task %r>" % self.idpreference

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


