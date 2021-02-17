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


class NewsList(APIView):

    renderer_classes = [JSONRenderer]

    def getdata(self, collection_name):
        db = client["news"]
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

    def get(self, request, category):
        data = self.getdata(category)
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
