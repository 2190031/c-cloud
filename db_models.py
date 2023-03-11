from datetime import datetime as dt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class role(db.Model):
	__tablename__ = 'role'
	idrole = db.Column(db.Integer, primary_key=True, autoincrement=True)
	role = db.Column(db.String(30), nullable=False)
	
	def __repr__(self):
		return "<task %r> % self.idrole"

class user(db.Model):
	__tablename__ = 'user'
	iduser = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(100), nullable=False)
	username = db.Column(db.String(45), nullable=False)
	name = db.Column(db.String(45), nullable=False)
	surname = db.Column(db.String(45), nullable=False)
	password = db.Column(db.String(45), nullable=False)
	usertype = db.Column(db.Integer, db.ForeignKey('role.idrole'), nullable=False)
	creationdate = db.Column(db.DateTime, default=dt.utcnow, nullable=False)

	def __repr__(self):
		return "<task %r> % self.iduser"
	
class file(db.Model):
	__tablename__ = 'file'
	idfile = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(45), nullable=False)
	category = db.Column(db.String(20), nullable=False)
	extension = db.Column(db.String(45), nullable=False)
	datecreated = db.Column(db.DateTime, default=dt.utcnow, nullable=False)
	iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)

	def __repr__(self):
		return "<task %r> % self.idfile"    

class historial(db.Model):
	__tablename__ = 'historial'
	idchange = db.Column(db.Integer, primary_key=True, autoincrement=True)
	idfile = db.Column(db.Integer, db.ForeignKey('file.idfile'), primary_key=True)
	datemodified = db.Column(db.String(30), nullable=False)
	iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)
	idmodificationtype = db.Column(db.Integer, nullable=False)
	beforechange = db.Column(db.Integer, nullable=False)
	afterchange = db.Column(db.Integer, nullable=False)
	changeline = db.Column(db.Integer, nullable=False)
	changecolumn = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return "<task %r> % self.idchange"

class version(db.Model):
	__tablename__ = 'version'
	idversion = db.Column(db.Integer, primary_key=True, autoincrement=True)
	idfile = db.Column(db.Integer, db.ForeignKey('file.idfile'), nullable=False)
	datecreated = db.Column(db.DateTime, default=dt.utcnow)

	def __repr__(self):
		return "<task %r> % self.idversion"

class error(db.Model):
	__tablename__ = 'error'
	iderror = db.Column(db.Integer, primary_key=True, autoincrement=True)
	iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)
	idfile = db.Column(db.Integer, db.ForeignKey('file.idfile'), nullable=False)
	description = db.Column(db.String(255), nullable=False)
	datereported = db.Column(db.DateTime, default=dt.utcnow)
	
	def __repr__(self):
		return "<task %r> % self.iderror"
	
class licence(db.Model):
	__tablename__ = 'license'
	idlicence = db.Column(db.Integer, primary_key=True, autoincrement=True)
	plan = db.Column(db.String(100), nullable=False)
	price = db.Column(db.Float, nullable=False)
	taxes = db.Column(db.Float, nullable=False)
	totalprice = db.Column(db.Float, nullable=False)
	packages = db.Column(db.String(45), nullable=False)

	def __repr__(self):
		return "<task %r> % self.idlicence"
	
class comment(db.Model):
	__tablename__ = 'comment'
	idcomment = db.Column(db.Integer, primary_key=True, autoincrement=True)
	iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)
	idfile = db.Column(db.Integer, db.ForeignKey('file.idfile'), nullable=False)
	line = db.Column(db.Integer, nullable=False)
	comment = db.Column(db.Text, nullable=False)
	
	def __repr__(self):
		return "<task %r> % self.idcomment"
	
class preference(db.Model):
	__tablename__ = 'preference'
	idpreference = db.Column(db.Integer, primary_key=True, autoincrement=True)
	iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)
	bkgcolour = db.Column(db.String(45), nullable=False)
	font = db.Column(db.String(45), nullable=False)
	fontcolour = db.Column(db.String(45), nullable=False)
	fontsize = db.Column(db.Float, nullable=False)
	profile = db.Column(db.String(45), nullable=False)
	autosave = db.Column(db.Boolean, nullable=False)
	lang = db.Column(db.String(3), nullable=False)

	def __repr__(self):
		return "<task %r> % self.idpreference"
	
class paytransaction(db.Model):
	__tablename__ = 'paytransaction'
	idpaytransaction = db.Column(db.Integer, primary_key=True, autoincrement=True)
	iduser = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)
	idlicence = db.Column(db.Integer, db.ForeignKey('licence.idlicence'), nullable=False)
	amount = db.Column(db.Float, nullable=False)
	datepaid = db.Column(db.DateTime, default=dt.utcnow)

	def __repr__(self):
		return "<task %r> % self.idpaytransaction"
	
class migration(db.Model):
	__tablename__ = 'migration'
	id = db.Column(db.Integer, primary_key=True)
	datemigration = db.Column(db.DateTime, default=dt.utcnow)
	
	def __repr__(self):
		return "<task %r> % self.id"
	
db_models = [user, file, version, comment, licence, preference, historial, paytransaction, error, role]