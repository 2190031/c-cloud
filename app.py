import secrets
from flask import Flask, render_template, redirect, request, session, abort, jsonify
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from db_models import db, defaultroles, sessions, user, error
from createUserFolder import newUserFolder, toStandardName
import pathlib, google, requests, cachecontrol, os, traceback

from render_pages import *
from file_management import (
    load_file,
    create_file,
    load_file__blank,
    send_error_report,
    save_preference,
    upload_p_picture,
)
from user_session import login, signup, update_p_data, auth_update

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:c55h32o5n4Mg@localhost/c_cloud"
app.config["SECRET_KEY"] = "secret_key"
app.secret_key = "ODNFAOFNA09q09qpomao989j"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = (
    "621438977816-o6ee2tto4rgsk9isrvpv6mm1ctvnkagb.apps.googleusercontent.com"
)
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
    redirect_uri="http://127.0.0.1:5000/callback",
)

db.init_app(app)

with app.app_context():
    try:
        db.create_all()
        db.session.commit()
        defaultroles()
    except:
        print("error")


@app.route("/")
def index():
    return render_index()


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)
    if "state" in session:
        if not session["state"] == request.args["state"]:
            abort(500)

        credentials = flow.credentials
        request_session = requests.Session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID,
        )

        googleid = id_info.get("sub")
        google_name = id_info.get("name")
        google_email = id_info.get("email")
        google_picture = id_info.get("picture")
        if "family_name" in id_info:
            google_family_name = id_info["family_name"]
        else:
            google_family_name = None

        google_username = google_email.split("@")[0]
        google_user_verify = user.query.filter_by(google_id=googleid).first()

        if google_user_verify:
            session.clear()
            id = google_user_verify.iduser
            newsession = sessions(iduser=id)
            try:
                db.session.add(newsession)
                db.session.commit()

                _iduser = user.query.filter_by(google_id = googleid).first()
                print(_iduser)

                session["user_id"] = _iduser
                session["user_name"] = google_name
                session["user_email"] = id_info.get("email")
                session["google_picture"] = id_info.get("picture")
                session["user_username"] = google_user_verify.username

                return redirect("/")
            except Exception as e:
                print(traceback.format_exc())
                return jsonify({'error': str(e)})
        else:
            google_verify = user.query.filter_by(email=google_email).first()
        if google_verify:
            return redirect("/login")
        else:
            new_user = user(
                google_id=googleid,
                name=google_name,
                username=google_username,
                surname=google_family_name,
                password=None,
                salt=None,
                email=google_email,
                picture=google_picture,
                usertype=1,
            )
            db.session.add(new_user)
            db.session.commit()
            newUserFolder(google_username)

            return redirect("/login")
    else:
        return redirect("/")


@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    return signup()

@app.route("/login", methods=["GET", "POST"])
def log_in():
    return login()

@app.route("/loginG")
def login_google():
    if "google_id" in session or "user_id" in session:
        return redirect("/")
    else:
        state = secrets.token_urlsafe(16)  # Generar un valor único para 'state'
        session["state"] = state
        authorization_url, _ = flow.authorization_url(
            prompt="select_account", state=state
        )
        return redirect(authorization_url)


@app.route("/login")
def login_page():
    return render_login()

@app.route("/editor")
def editor():
    return render_editor()

@app.route("/create_file", methods=["POST"])
def create_files():
    return create_file()


@app.route("/dashboard")
def dashboard():
    return render_dashboard()


@app.route("/settings")
def settings():
    return render_settings()


@app.route("/profile")
def profile():
    return render_profile()


@app.route("/profile/profile_picture")
def profile_picture():
    return render_profile_picture()


@app.route("/create_file", methods=["POST"])
def create():
    return create_file()


@app.route("/load_file", methods=["POST"])
def open_file():
    return load_file()

@app.route("/load_file_blank/<string:file>", methods=["GET"])
def open_file_blank(file):
    return load_file__blank(file)

@app.route("/send_report", methods=["POST"])
def send_report():
    return send_error_report()


@app.route("/save_preferences", methods=["POST"])
def save_pref():
    return save_preference()

@app.route("/upload_profile_picture", methods=["POST"])
def upload_profile_picture():
    return upload_p_picture()

@app.route("/update_profile_data", methods=["POST"])
def update_profile_data():
    return update_p_data()

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/notfound")
def notfound():
    return render_notfound()


@app.route("/auth_update", methods=["POST"])
def auth():
    return auth_update()


@app.errorhandler(404)
def page_not_found(e):
    return render_template("notfound.html")


if __name__ == "__main__":
    app.run(debug=True)
