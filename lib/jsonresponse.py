from django.http import HttpResponse
from django.utils import simplejson

class JsonResponse(HttpResponse):
    def __init__(self, data):
        super(JsonResponse, self).__init__(simplejson.dumps(data), content_type="application/json")
