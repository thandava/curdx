import json
import os

import pymongo

from bson.objectid import ObjectId
from flask import Flask, request

from pyinfoblox import InfobloxWAPI
app = Flask(__name__)

mongo_client = pymongo.MongoClient('mongodb://sapasupu:4mMAjH1P3kyrLXK8R6wvzBhW72zHAe7vdUdTFIyNiVlfsJWIahB13q8SiFdyVeftgiWVLxZzriYGzGEGDjLOoA==@sapasupu.documents.azure.com:10255/?ssl=true&replicaSet=globaldb')

db = mongo_client.service_registry

profile_metadata_schema = {
    'figid': int , 'profile_id': str, 'id': int, 'description':str,
    'MATCH_TAGS': {'figid': int, 'tier': str, 'geo': str, 'owner_use':str, 'cloud_provider':str,
                    'country':str, 'region':str, 'environment':str, 'trust_worthy':bool,
                    'security_zone':int, 'application_name':str, 'security_profile':str}
}

def validate_against_schema(data, schema):
    '''
        generic function to validate user input against a specific schema
    '''
    if not data:
        raise ValueError("Invalid Input.")
    if type(schema) in [dict]:
        if len(data.keys()) != len(schema.keys()):
            raise ValueError("Invalid Input")
        for key in schema.keys():
            validate_against_schema(data.get(key, None), schema[key])
    elif not type(schema) in [list, set, tuple]:
        if type(data) == unicode:
            data = str(data)
        if type(data) != schema:
            raise TypeError("Data type does not match schema")
    else:
        if type(data) != type(schema):
            raise TypeError("Data type does not match schema")


@app.route("/service_registry/profile/metadata", methods=['GET', 'POST', 'PUT', 'DELETE'])
def profile_metadata():
    if request.method == 'POST':
        try:
            request_data = json.loads(request.data)
            validate_against_schema(request_data, profile_metadata_schema)
            profiles = db.profiles
            profile_id = profiles.insert_one(request_data).inserted_id
        except Exception as e:
            print("could not save profile metadata: " + str(e))
            return json.dumps({'code': 500, 'message': 'could not save profile'})
        return json.dumps({'code': 200, 'message': 'Successfully stored profile metadata'})
    if request.method == 'GET':
        id = request.args.get('id')
        #import pdb; pdb.set_trace()
        profiles = db.profiles
        try:
            profile = profiles.find_one({'id': int(id)})
            if profile:
                profile['_id'] = str(profile['_id'])
                return json.dumps({'profile': profile, 'code': 200})
            return json.dumps({'code': 400, 'message': 'no matching profile found.'})
        except Exception as e:
            print("could not save profile metadata: " + str(e))
            return json.dumps({'code': 500, 'message': 'could not find the profile requested.'})
    if request.method == 'DELETE':
        id = request.args.get('id')
        if not id:
            return json.dumps({'code': 400, 'message': 'please provide an id to match'})
        try:
            profiles = db.profiles
            result = profiles.delete_one({'id': int(id)})
            if result.deleted_count == 1:
                return json.dumps({'code': 200, 'message': 'successfully deleted profile with id %s' % id })
        except Exception as e:
            print("could not delte profile: " + str(e))
            return json.dumps({'code': 500, 'message': 'could not delte profile with id %s' % id})



@app.route("/service_registry/service/metadata", methods=['GET', 'POST', 'PUT', 'DELETE'])
def service_metadata():
    if request.method == 'POST':
        try:
            request_data = json.loads(request.data)
            #validate_against_schema(request_data, service_metadata_schema)
            services = db.services
            service_id = services.insert_one(request_data).inserted_id
        except Exception as e:
            print("could not save service metadata: " + str(e))
            return json.dumps({'code': 500, 'message': 'could not save service'})
        return json.dumps({'code': 200, 'message': 'Successfully stored service metadata'})
    if request.method == 'GET':
        id = request.args.get('id')
        services = db.services
        try:
            service= services.find_one({'id': int(id)})
            if service:
                service['_id'] = str(service['_id'])
                return json.dumps({'service': service, 'code': 200})
            return json.dumps({'code': 400, 'message': 'no matching service found.'})
        except Exception as e:
            print("could not save service metadata: " + str(e))
            return json.dumps({'code': 500, 'message': 'could not find the service requested.'})



@app.route("/service_registry/provider/metadata", methods=['GET', 'POST', 'PUT', 'DELETE'])
def provider_metadata():
    if request.method == 'POST':
        request_data = json.loads(request.data)
        #TODO: validate that request data has valid data and format.
        providers = db.providers
        try:
            provider_id = providers.insert_one(request_data).inserted_id
        except Exception as e:
            print("could not save provider metadata: " + str(e))
            return json.dumps({'code': 500, 'message': 'could not save provider'})
        return json.dumps({'code': 200, 'message': 'Successfully stored provider metadata'})
    if request.method == 'GET':
        id = request.args.get('id')
        #import pdb; pdb.set_trace()
        providers = db.providers
        try:
            provider= providers.find_one({'id': int(id)})
            if provider:
                provider['_id'] = str(provider['_id'])
                return json.dumps({'provider': provider, 'code': 200})
            return json.dumps({'code': 400, 'message': 'no matching provider found.'})
        except Exception as e:
            print("could not save provider metadata: " + str(e))
            return json.dumps({'code': 500, 'message': 'could not find the provider requested.'})


if __name__ == "__main__":
    app.run(host='0.0.0.0')
