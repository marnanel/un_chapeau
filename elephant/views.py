from django.shortcuts import render
from django.http import HttpResponse
import json

def un_chapeau_response(d):
    return HttpResponse(
            content_type = 'text/json',
            content = json.dumps(d, indent=2, sort_keys=True),
            status = 200,
            reason = 'love and hugs',
            charset = 'UTF-8')

###########################

def instance(request):
    result = {
            'uri': 'http://127.0.0.1',
            'title': 'un_chapeau test',
            'description': 'just a test',
            'email': 'marnanel@thurman.org.uk',
            'version': 'un_chapeau 0.0.1',
            'urls': {},
            'languages': ['en_GB'],
            'contact_account': 'marnanel',
            }
    return un_chapeau_response(result)

###########################

def apps(request):
    result = {
            'id': 'wombat',
            'client_id': '5Acb78IHuX9DgH7RNiJCNk1J1mZJbTrzy1B2eOEa',
            'client_secret': 'i8L3q1T9ECg0cYCD2P3O319my9rIfyLD3YWjiZX5vwIL8XI4XhNNlN6YuAjkkxH2ruUrs6p5TQisU6FkAILoF1DTPKYsx95UqK8QrZ5Vo9IHhtxizfbI710Qn0a1Rq49',
            }
    return un_chapeau_response(result)
