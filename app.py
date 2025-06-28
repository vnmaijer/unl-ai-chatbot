from flask import Flask, redirect, url_for, session, request, render_template
from flask_session import Session
import msal
import openai
import os
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

app.config["SESSION_TYPE"] = "filesystem"
app.config["PREFERRED_URL_SCHEME"] = "https"

Session(app)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/auth-redirect"
SCOPE = ["User.Read"]

openai.api_key = os.getenv("OPENAI_API_KEY")

def _build_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY,
        client_credential=CLIENT_SECRET, token_cache=cache)

def _build_auth_url():
    return _build_msal_app().get_authorization_request_url(
        SCOPE,
        redirect_uri=url_for("authorized", _external=True)
    )

@app.route("/")
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    user_email = session["user"].get("preferred_username", "")
    if not user_email.endswith("@unl.nl"):
        return "Access denied", 403
    return render_template("chat.html", user=session["user"])

@app.route("/login")
def login():
    return redirect(_build_auth_url())

@app.route(REDIRECT_PATH)
def authorized():
    cache = msal.SerializableTokenCache()
    result = _build_msal_app(cache).acquire_token_by_authorization_code(
        request.args.get("code"),
        scopes=SCOPE,
        redirect_uri=url_for("authorized", _external=True)
    )
    if "id_token_claims" in result:
        session["user"] = result["id_token_claims"]
        return redirect(url_for("index"))
    else:
        return f"Login failed: {result}"

@app.route("/chat", methods=["POST"])
def chat():
    if not session.get("user"):
        return "Unauthorized", 401
    question = request.form.get("question")
    if not question:
        return "No input", 400
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": question}]
    )
    answer = response.choices[0].message.content
    return {"answer": answer}

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)
