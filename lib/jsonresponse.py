import json
from django.http import HttpResponse


class JsonResponse(HttpResponse):
    def __init__(self, data):
        super(JsonResponse, self).__init__(json.dumps(data), content_type="application/json")
