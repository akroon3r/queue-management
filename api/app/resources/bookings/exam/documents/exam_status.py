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

@api.route("/exams_status/", methods=["GET"])
class ExamStatus(Resource):

    #oidc.accept_token(require_token=True)
    def post(self):
        print("==> In Python POST /exams_status/ endpoint")

        csr = CSR.find_by_username('cfms-postman-operator')
        #office = Office.query.filter_by(office_id=csr.office_id).first()

        # Parameter id_list ==> should be received by the end point as a comma separated string
        # of all exam ids that should have their status queried d
        value_list = request.args.get("id_list")