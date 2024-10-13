from flask import Flask, render_template, request, redirect, session
import requests
import warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

app = Flask(__name__)
 
@app.route('/portal')
def form():
    session['clientMac'] = request.args.get('client_mac')
    session['clientIp'] =request.args.get('uip')
    session['rcIp'] = request.args.get('nbiIP')
    session['clientUrl'] = request.args.get('url')
    session['startUrl'] = request.args.get('StartURL')
    return render_template('wisprPortal.html')

@app.route('/data/', methods = ['POST'])
def data():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        url = "https://" + session.get('rcIp') + ":443/portalintf"
        body = {
            "Vendor": "Ruckus",
            "RequestUserName": "api",
            "RequestPassword": "wlan integration key", #integration key
            "APIVersion": "1.0",
            "RequestCategory": "UserOnlineControl",
            "RequestType": "Login",
            "UE-IP": session.get('clientIp'),
            "UE-MAC": session.get('clientMac'),
            "UE-Username": name,
            "UE-Password": password
        }
        requests.post(url, json = body, verify = False)
        #print (response)
        if session.get('startUrl') != None:
            return redirect(session.get('startUrl'), code=302)
        else:
            return redirect(session.get('clientUrl'), code=302)
        
def main():
    app.secret_key = 'super secret key' #don't need to change this
    app.run(host='this_host_ip_address', port=5000)

if __name__ == "__main__":
	main()
