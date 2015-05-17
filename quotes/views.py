from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import Context

from projectmanager.views import render_to_pdf
from .models import Quote


@login_required
def quote(request, quote_id, type='html'):
    data = {
        'quote': get_object_or_404(Quote, pk=quote_id),
        'type': type,
    }
    if type == 'pdf':
        return render_to_pdf('quotes/pdf/quote.html', data)
    else:
        return render_to_response('quotes/pdf/quote.html', data, context_instance=Context(request))
