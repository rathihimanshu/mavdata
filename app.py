from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

os.environ.setdefault("AUTHLIB_INSECURE_TRANSPORT", "1")   # dev only
app = Flask(__name__)
app.secret_key = os.urandom(24)

oauth = OAuth(app)
oauth.register(
    name="oidc",
    client_id=os.getenv("COGNITO_CLIENT_ID"),
    client_secret=os.getenv("COGNITO_CLIENT_SECRET"),
    server_metadata_url=(
        "https://cognito-idp.us-east-1.amazonaws.com/"
        "us-east-1_c2IRp6oAp/.well-known/openid-configuration"
    ),
    client_kwargs={"scope": "openid email phone"},
)

@app.route("/")
def index():
    user = session.get("user")
    return (
        f'Hello {user["email"]} · <a href="/logout">Logout</a>'
        if user
        else 'Welcome! <a href="/login">Login</a>'
    )

@app.route("/login")
def login():
#    redirect_uri = url_for("authorize", _external=True)
#    return oauth.oidc.authorize_redirect(redirect_uri)
    return oauth.oidc.authorize_redirect("http://localhost:5001/authorize")

@app.route("/authorize")
def authorize():
    token = oauth.oidc.authorize_access_token()
    session["user"] = token["userinfo"]
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Listen on every interface so you can reach it from another device
    app.run(debug=True, host="0.0.0.0", port=5001) 
