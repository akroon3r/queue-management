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
from flask_restplus import Resource
from flask import request, g
from app.models.bookings import Room
from app.schemas.bookings import BookingSchema
from app.models.theq import CSR
from qsystem import api, api_call_with_retry, db, oidc


@api.route("/bookings/", methods=["POST"])
class BookingPost(Resource):

    booking_schema = BookingSchema()

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    def post(self):

        csr = CSR.find_by_username(g.oidc_token_info['username'])

        json_data = request.get_json()

        if not json_data:
            return {"message": "No input data received for creating a booking"}, 400

        booking, warning = self.booking_schema.load(json_data)

        if warning:
            logging.warning("WARNING: %s", warning)
            return {"message": warning}, 422

        if booking.office_id is None:
            booking.office_id = csr.office_id

        if booking.office_id == csr.office_id or csr.role.role_code == "LIAISON":
            db.session.add(booking)
            db.session.commit()

            result = self.booking_schema.dump(booking)

            return {"booking": result.data,
                    "errors": result.errors}, 201
        else:
            return {"The Booking Office ID and CSR Office ID do not match!"}, 403
