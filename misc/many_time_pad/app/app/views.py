from app import app
from app import cfg
from flask import render_template,request,redirect,make_response,send_file

#serve index.html
@app.route("/")
def index():
    return render_template("index.html")

#encrypt messages that are POSTed to /encrypt
@app.route("/encrypt", methods=["POST"])
def encrypt():
    #truncate message if longer than 256 bytes, convert to byte string
    plaintext = request.form.get("message")[:256].encode()
    #pad message with \xff bytes
    plaintext += b'\xff' * (256 - len(plaintext))
    #xor byte string with secret key
    ciphertext = bytes([plaintext_byte ^ key_byte for plaintext_byte, key_byte in zip(plaintext, cfg.secret_byte_string)])
    #put the ciphertext in a response header
    resp = make_response(render_template("index.html"))
    resp.headers["ciphertext"] = repr(ciphertext)
    return resp

#send server source code to those who request it
@app.route("/source")
def source():
    return send_file("./views.py")

#secret admin page, the URL is the secret key so it is secure
@app.route("/" + cfg.secret_byte_string.decode())
def win():
    return(render_template("win.html"))


