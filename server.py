import os
from flask import Flask, request
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse


# ACCOUNT_SID = 'AC***'
# API_KEY = 'SK***'
# API_KEY_SECRET = '***'
# PUSH_CREDENTIAL_SID = 'CR***'
# APP_SID = 'AP***'

ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
API_KEY = os.environ['TWILIO_API_KEY_SID']
API_KEY_SECRET = os.environ['TWILIO_API_KEY_SECRET']
APP_SID = os.environ['TWIML_APP_SID']
"""
Use a valid Twilio number by adding to your account via https://www.twilio.com/console/phone-numbers/verified
"""
# CALLER_NUMBER = '13254408525'

"""
The caller id used when a client is dialed.
"""
# CALLER_ID = 'client:quick_start'
IDENTITY = '9170395522326'


app = Flask(__name__)

"""
Creates an access token with VoiceGrant using your Twilio credentials.
"""
@app.route('/accessToken', methods=['GET', 'POST'])
def token():
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)
  # push_credential_sid = os.environ.get("PUSH_CREDENTIAL_SID", PUSH_CREDENTIAL_SID)
  app_sid = os.environ.get("APP_SID", APP_SID)

  grant = VoiceGrant(
    # push_credential_sid=push_credential_sid,
    outgoing_application_sid=app_sid
  )
  # to = request.values.get("to")
  # identity = request.values.get("identity")
  identity=(request.headers["identity"])
  print(request.headers["identity"])

  # identity = request.values["identity"] 
  # print(IDENTITY)
          # if request.values and request.values["identity"] else IDENTITY
  # identity="917039552326"
  # token = AccessToken(account_sid, api_key, api_key_secret)
  token = AccessToken(account_sid, api_key, api_key_secret, identity=identity)
  token.add_grant(grant)

  return token.to_jwt()

"""
Creates an endpoint that plays back a greeting.
"""
@app.route('/incoming', methods=['GET', 'POST'])
def incoming():
  resp = VoiceResponse()
  resp.say("Congratulations! You have received your first inbound call! Good bye.")
  return str(resp)

"""
Makes a call to the specified client using the Twilio REST API.
"""
@app.route('/placeCall', methods=['GET', 'POST'])
def placeCall():
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)

  client = Client(api_key, api_key_secret, account_sid)
  to = request.values.get("to")
  callerId = request.values.get("from")
  call = None
  client.calls.create(to=to,from_=callerId)
  # if to is None or len(to) == 0:
  #   call = client.calls.create(url=request.url_root + 'incoming', to='client:' + IDENTITY, from_=CALLER_ID)
  # elif to[0] in "+1234567890" and (len(to) == 1 or to[1:].isdigit()):
  #   call = client.calls.create(url=request.url_root + 'incoming', to=to, from_=CALLER_NUMBER)
  # else:
  #   call = client.calls.create(url=request.url_root + 'incoming', to='client:' + to, from_=CALLER_ID)
  return str(call)

"""
Creates an endpoint that can be used in your TwiML App as the Voice Request Url.

In order to make an outgoing call using Twilio Voice SDK, you need to provide a
TwiML App SID in the Access Token. You can run your server, make it publicly
accessible and use `/makeCall` endpoint as the Voice Request Url in your TwiML App.
"""
@app.route('/makeCall', methods=['GET', 'POST'])
def makeCall():
  # resp = VoiceResponse()
  # to = request.values.get("to")
  # callerId = "+" + request.values.get("from")
  # print("callerid ", callerId)
  # # if to is None or len(to) == 0:
  # #   resp.say("Congratulations! You have just made your first call! Good bye.")
  # # elif to[0] in "+1234567890" and (len(to) == 1 or to[1:].isdigit()):
  # #   resp.dial(callerId=CALLER_NUMBER).number(to)
  # resp.dial(callerId).number(to)
  # # resp.dial(callerId="+13254408525").number("+91703955226")
  # # else:
  # #   resp.dial(callerId=CALLER_ID).client(to)
  # return str(resp)
  """Returns TwiML instructions to Twilio's POST requests"""
  response = VoiceResponse()
  
  # we get this 'From' and 'To' from javascript main.js - btnDial function - params
  # record will be saved in twilio monitor logs 
  # dial = response.dial(caller_id='+19086638750',)
  dial = response.dial(caller_id=request.values.get("from"),record='record-from-ringing-dual')
  # dial = response.dial(caller_id=request.POST['From'],record='record-from-ringing-dual')
  # dial.number('+917039552326')
  dial.number(request.values.get("to"))

  return str(response)
  # return HttpResponse(
  #     str(response), content_type='application/xml; charset=utf-8'
  # )

@app.route('/', methods=['GET', 'POST'])
def welcome():
  resp = VoiceResponse()
  resp.say("Welcome to Twilio")
  return str(resp)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
