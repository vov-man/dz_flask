#from hashlib import md5

import flask
import pydantic

from flask import jsonify, request
from flask.views import MethodView
#from sqlalchemy.exc import IntegrityError

import schema
from models import Session, Advertisements

app = flask.Flask("flask")


class HttpError(Exception):
    def __init__(self, status_code: int, message: str ):
        self.status_code = status_code
        self.message = message


def validate(validation_schema, validation_data):
    try:
        model = validation_schema(**validation_data)
        return model.dict(exclude_none=True)
    except pydantic.ValidationError as err:
        raise HttpError(400, err.errors())


@app.errorhandler(HttpError)
def error_handler(er: HttpError):
    response = jsonify({"status": "Error", "description": er.message})
    response.status_code = er.status_code
    return response


def get_advertisements(session, advertisements_id):
    advertisements = session.get(Advertisements, advertisements_id)
    if advertisements is None:
        raise HttpError(404, "the advertisements not found.")
    return advertisements


class AdvertisementsView(MethodView):
    def get(self, advertisements_id):
        with Session() as session:
            advertisements = get_advertisements(session, advertisements_id)
            return jsonify(
                {
                    "id": advertisements.id,
                    "title": advertisements.email,
                    "description": advertisements.description,
                    "creator": advertisements.creator,
                    "creation_time": advertisements.creation_time.isoformat(),
                }
            )

    def post(self):
        validated_json = validate(schema.CreateAdvertisements, request.json)
        with Session() as session:
            advertisements = Advertisements(**validated_json)
            session.add(advertisements)
            session.commit()
            return jsonify({"id": advertisements.id})


    def patch(self, advertisements_id):
        validated_json = validate(schema.UpdateAdvertisements, request.json)
        with Session() as session:
            advertisements = get_advertisements(session, advertisements_id)
            for field, value in validated_json.items():
                setattr(advertisements, field, value)
            session.add(advertisements)
            session.commit()
            return jsonify({"id": advertisements.id})


    def delete(self, advertisements_id):
        with Session() as session:
            advertisements = get_advertisements(session, advertisements_id)
            session.delete(advertisements)
            session.commit()
            return jsonify({"status": "success"})


advertisements_view = AdvertisementsView.as_view("advertisements")
app.add_url_rule(
    "/advertisements/<int:advertisements_id>",
    view_func=advertisements_view,
    methods=["GET", "PATCH", "DELETE"]
)
app.add_url_rule("/advertisements/", view_func=advertisements_view, methods=["POST"])

if __name__ == "__main__":
    app.run()
