# from django.shortcuts import render
# Create your views here.
# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from db import db


class NewsCategory(APIView):
    renderer_classes = [JSONRenderer]

    @staticmethod
    def getdata(collection_name):
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
        resp_status = status.HTTP_200_OK if data is not None else status.HTTP_404_NOT_FOUND

        collections = db.list_collection_names()
        collections_msg = 'No API categories at the moment.' \
            if not collections else ('Available categories are' + ' '.join(collections))

        resp = data if data is not None else {'status': 404,
                                              'message': 'Category not found. {}'.format(collections_msg)}
        return Response(resp, status=resp_status)


class News(APIView):
    renderer_classes = [JSONRenderer]

    @staticmethod
    def get_all_data():
        all_data = {
            "source": "NewsApi",
            "description": "Latest news all around the globe"
        }
        count = 0
        categories = {}
        for collection_name in db.list_collection_names():
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

    def get(self, request):
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
