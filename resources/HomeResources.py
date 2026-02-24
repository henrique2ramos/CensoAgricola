from flask_restful import Resource


class HomeResources(Resource):
    def get(self):
        return {"message": "Welcome to the Censo Agrícola API!"}