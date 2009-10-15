from django.contrib.auth import login, authenticate

class LogGregInMiddleware(object):
    def process_request(self, request):
        u = authenticate(username='greg', password='password1')
        if not request.user.is_authenticated():
            login(request, u)
        return None
