# from django.shortcuts import render
# Create your views here.
# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from db import db
from typing import Union, Dict


class NewsCategory(APIView):
    renderer_classes = [JSONRenderer]

    @staticmethod
    def getdata(collection_name: str) -> Union[Dict, None]:
        """
        Retrieves collection data from mongo db depending on collection name

        Args:
            collection_name (str): name of the collection to retrieve the data

        Returns:
            dictionary of the related collection data
        """
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

    def get(self, request, category: str):
        """
        Retrieves a category data via route 'categories/<category_name>/' route

        Args:
            category (str): category name to retrieve data
            request: request object
        Returns:
            category data if category otherwise no data json response
        """
        data = self.getdata(category)
        resp_status = status.HTTP_200_OK if data is not None else status.HTTP_404_NOT_FOUND

        collections = db.list_collection_names()
        collections_msg = 'No API categories at the moment.' \
            if not collections else ('Available categories are ' + ', '.join(collections))

        resp = data if data is not None else {'status': 404,
                                              'message': 'Category not found. {}'.format(collections_msg)}
        return Response(resp, status=resp_status)


class Categories(APIView):
    """
    Class definition for the categories routes
    """
    renderer_classes = [JSONRenderer]

    @staticmethod
    def category_meta_data() -> dict:
        """
        Returns a specific category data related details

        Returns:
            Dictionary of the category data
        """
        categories = db.list_collection_names()

        meta_data = {
            "source": "NewsApi",
            "description": "Latest news all around the globe",
            "categories": categories,
            "total_categories": len(categories)
        }

        return meta_data

    def get(self, request):
        """
        Route 'categories/' that retrieves the category meta data

        Returns:
            json response
        """
        data = self.category_meta_data()
        s = status.HTTP_200_OK if data is not None else status.HTTP_404_NOT_FOUND
        r = data if data is not None else {'status': 404}
        return Response(r, status=s)


class News(APIView):
    """
    Class definition of all the news route
    """
    renderer_classes = [JSONRenderer]

    @staticmethod
    def get_all_data():
        """
        Retrieves all the data related to the api that is categories and their data

        Returns:
            object of all the data and categories
        """
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
        """
        Route '/' to get all the data related to the api

        Returns:
            json response or 404 incase no data found
        """
        data = self.get_all_data()
        s = status.HTTP_200_OK if data is not None else status.HTTP_404_NOT_FOUND
        r = data if data is not None else {'status': 404}
        return Response(r, status=s)


class Error404(APIView):
    """
    View for handling 404 errors
    """
    renderer_classes = [JSONRenderer]

    @staticmethod
    def custom404(request, exception=None):
        """
        Called for custom 404 errors
        """
        s = status.HTTP_404_NOT_FOUND

        return Response({
            'status_code': 404,
            'error': 'The resource was not found'
        })
