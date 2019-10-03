'''Copyright 2018 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.'''

import logging
import requests
import json
import urllib.request
from flask import g, request
from flask_restplus import Resource
from app.models.theq import CSR, Office
from sqlalchemy import exc, or_, desc
from qsystem import api, oidc

dev = True

if dev:
    path = 'https://bcmaildirect.gov.bc.ca/JOB_TEST/auth=env_exam;f697697a090c4f349545a09d21b3eb08/JSON' \
           '/create:ENV-IPM-EXAM'
else:
    path = 'https://bcmaildirect.gov.bc.ca/JOB/auth=env_exam;f697697a090c4f349545a09d21b3eb08/JSON/create:ENV-IPM-EXAM'


@api.route("/exams_create/", methods=['POST'])
class ExamCreate(Resource):

    # TODO uncomment this when we go live
    #@oidc.accept_token(require_token=True)
    def post(self):
        print("==> In Python POST /exams_create/ endpoint")

        # TODO Change this when you go live
        csr = CSR.find_by_username('cfms-postman-operator')
        # office = Office.query.filter_by(office_id=csr.office_id).first()
        json_data = request.get_json()

        bcmp_exam_object = {}

        # Fill out Required Information First
        bcmp_exam_object['EXAM_CATEGORY'] = json_data.get('EXAM_CATEGORY', "Pesticide")
        bcmp_exam_object['STUDENT_phoneNumber'] = json_data.get('STUDENT_phoneNumber', "250-555-5555")
        bcmp_exam_object['STUDENT_fullname'] = json_data.get('STUDENT_fullName', "Sean Rumsby")
        bcmp_exam_object['STUDENT_emailAddress'] = json_data.get('STUDENT_emailAddress', "sean@olivewood.io")
        bcmp_exam_object['STUDENT_ADDRESS_line1'] = json_data.get('STUDENT_ADDRESS_line1', "420 Fort St.")
        bcmp_exam_object['STUDENT_ADDRESS_line2'] = json_data.get('STUDENT_ADDRESS_line2', "Suite 12")
        bcmp_exam_object['STUDENT_city'] = json_data.get('STUDENT_city', "Victoria")
        bcmp_exam_object['STUDENT_province'] = "BC"
        bcmp_exam_object['STUDENT_ADDRESS_postalCode'] = json_data.get('STUDENT_ADDRESS_postalCode', "V9W7X7")

        # Fill in optional data if it exists
        bcmp_exam_object['RECIPIENT_EMAIL_ADDRESS'] = ''
        if json_data.get('RECIPIENT_EMAIL_ADDRESS', '') is not '':
            bcmp_exam_object['RECIPIENT_EMAIL_ADDRESS'] = json_data.get('RECIPIENT_EMAIL_ADDRESS', None)

        bcmp_exam_object['REGISTRAR_name'] = ''
        if json_data.get('REGISTRAR_name', '') is not '':
            bcmp_exam_object['REGISTRAR_name'] = json_data.get('REGISTRAR_name', None)

        bcmp_exam_object['REGISTRATION_NOTES'] = ''
        if json_data.get('REGISTRATION_NOTES', '') is not '':
            bcmp_exam_object['REGISTRATION_NOTES'] = json_data.get('REGISTRATION_NOTES', None)

        bcmp_exam_object['PAYMENT_METHOD'] = ''
        if json_data.get('PAYMENT_METHOD', '') is not '':
            bcmp_exam_object['PAYMENT_METHOD'] = json_data.get('PAYMENT_METHOD', None)

        bcmp_exam_object['FEE_PAYMENT_METHODS'] = ''
        if json_data.get('FEE_PAYMENT_METHODS', '') is not '':
            bcmp_exam_object['FEE_PAYMENT_METHODS'] = json_data.get('FEE_PAYMENT_METHODS', None)

        print('Full Exam Object', bcmp_exam_object)

        req = urllib.request.Request(path, data=bytes(json.dumps(bcmp_exam_object), encoding="utf-8"), method='POST')
        req.add_header('Content-Type', 'application/json')
        print('request', req)

        response = urllib.request.urlopen(req).read()

        print('response', response)

        response_string = response.decode('utf-8')

        if 'ERROR' in response_string:
            return {'message': response_string}, 422
        else:
            json_response = json.loads(response_string)
            return{'message': json_response}, 201
