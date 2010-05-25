from django import template
from projectmanager.models import HostingClient
from easy_tag import easy_tag
register = template.Library()




class InvoiceDueCountNode(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def render(self, context):
        
        context[self.varname] = sum(int(h.invoice_due) for h in HostingClient.objects.all())
        return ''
        
@register.tag()
@easy_tag
def get_invoice_due_count(_tag, _as, varname):
    return InvoiceDueCountNode(varname)


