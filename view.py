from flask import Blueprint, request, render_template
import json
# import requests
# from requests.auth import HTTPBasicAuth
import opsgenie_sdk

PushingMessage = Blueprint("PushingMessage",__name__, template_folder="templates")

@PushingMessage.route("/", methods= ['POST', 'GET'])
def homepage():
    if request.method == 'POST':
        message = request.form['message']
        alias = request.form['alias']
        desc = request.form['desc']
        entity = request.form['entity']
        priority = request.form['priority']

        conf = opsgenie_sdk.configuration.Configuration()
        conf.api_key['Authorization'] = '<Your-API-Key>'

        api_client = opsgenie_sdk.api_client.ApiClient(configuration=conf)
        alert_api = opsgenie_sdk.AlertApi(api_client=api_client)
        
        body = opsgenie_sdk.CreateAlertPayload(
            message= message,
            alias= alias,
            description=desc,
            # responders=[{
            #     'name': 'team1',
            #     'type': 'team'
            # }],
            # visible_to=[
            # {'name': 'Sample',
            # 'type': 'team'}],
            # actions=['Restart', 'AnExampleAction'],
            # tags=['OverwriteQuietHours'],
            # details={'key1': 'value1',
            #         'key2': 'value2'},
            entity=entity,
            priority=priority
        )
        try:
            create_response = alert_api.create_alert(create_alert_payload=body)
            print(create_response)
            return render_template('alert_created.html')
        except opsgenie_sdk.ApiException as err:
            print("Exception when calling AlertApi->create_alert: %s\n" % err)

        return render_template("index.html")
    else:
        return render_template("index.html")    

@PushingMessage.route("/alert", methods= ['POST', 'GET'])
def getAlert():
    if request.method == 'POST':
        alert = request.form['alert']

        conf = opsgenie_sdk.configuration.Configuration()
        conf.api_key['Authorization'] = '<Your-API-Key>'
        api_client = opsgenie_sdk.api_client.ApiClient(configuration=conf)
        alert_api = opsgenie_sdk.AlertApi(api_client=api_client)
        try:
            get_response = alert_api.get_alert(identifier=alert, identifier_type='id')
            # print(get_response)
            string_data = (get_response.__dict__)['_data']
            dict_data = string_data.__dict__
            return render_template('response.html', data=dict_data)
            # return str(get_response)
        except opsgenie_sdk.ApiException as err:
            print("Exception when calling AlertApi->get_alert: %s\n" % err)

        return render_template("pull_alert.html")


    else:
        return render_template("pull_alert.html")    
