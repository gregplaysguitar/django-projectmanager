from collections import Mapping

from django.http import HttpResponse
from django.template.loader import get_template


def merge(dicts):
    """Merge an iterable of dictionaries into one."""
    
    d = {}
    for d_ in dicts:
        d.update(d_)
    return d


def render_to_response(template_name, context, request):
    # uses get_template and Template.render so we can pass the request,
    # and the template engine takes care of adding it and csrf
    # stuff to the context
    tpl = get_template(template_name)
    content = tpl.render(context, request=request)
    return HttpResponse(content)


def render(template=None):
    """Decorator to reduce view boilerplate; wrapped views should return a 
       dictionary or list of dictionaries which will be passed in to the 
       provided template, which can be specified either by argument to the 
       decorator or in the returned context.
       
       If a view returns a django HttpResponse subclass then that is returned
       instead. 
    """
    
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            res = view(request, *args, **kwargs)

            if isinstance(res, HttpResponse):
                return res
            elif not isinstance(res, Mapping):
                context = merge(res)
            else:
                context = res
            
            template_name = context.get('template', template)
            if not template_name:
                raise RuntimeError(u'No template supplied.')
            
            return render_to_response(template_name, context, request)
            
        return wrapper
    return decorator


def template_view_factory(template_name, context={}):
    """Returns a generic view which renders a template using the optional 
       context and request. """
    
    return lambda request: render_to_response(template_name, context, request)
