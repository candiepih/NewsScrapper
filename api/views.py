# from django.shortcuts import render
# Create your views here.
# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pymongo
from rest_framework.renderers import JSONRenderer

password = "mutheeal.am."
client = pymongo.MongoClient(
            "mongodb+srv://candiepih:" + password + "@cluster0.1fcmf.mongodb.net/news?retryWrites=true&w=majority")
db = client["news"]


class NewsList(APIView):

    renderer_classes = [JSONRenderer]

    def getdata(self, collection_name):
        collection = db[collection_name]
        if collection.count_documents({}) > 0:
            cursor = collection.find({})
            document = {}
            for myDocument in cursor:
                document = myDocument
            document.pop('_id')
            return document
        else:
            return None

    def get_all_data(self):
        all_data = {
            "source": "extenews",
            "description": "Latest news all around the globe"
        }
        count = 0
        categories = {}
        for collection_name in db.collection_names():
            count += 1
            collection = db[collection_name]
            if collection.count_documents({}) > 0:
                cursor = collection.find({})
                document = {}
                for myDocument in cursor:
                    document = myDocument
                document.pop('_id')
                categories[collection_name] = document

        all_data["categories"] = categories
        all_data["totalCategories"] = count

        return all_data

    def get(self, request, category):
        if category.lower() != "all":
            data = self.getdata(category)
        else:
            data = self.get_all_data()

        s = status.HTTP_200_OK if data is not None else status.HTTP_404_NOT_FOUND
        r = data if data is not None else {'status': 404}
        return Response(r, status=s)


class Error404(APIView):
    renderer_classes = [JSONRenderer]

    def custom404(self, request, exception=None):
        s = status.HTTP_404_NOT_FOUND

        return Response({
            'status_code': 404,
            'error': 'The resource was not found'
        })
