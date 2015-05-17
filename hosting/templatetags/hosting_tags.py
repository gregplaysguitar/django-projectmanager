from django import template

from ..models import HostingClient


register = template.Library()


@register.assignment_tag()
def get_invoice_due_count():
    return sum(int(h.invoice_due) for h in HostingClient.objects.all())
