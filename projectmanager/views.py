import json
from cStringIO import StringIO
import csv
from datetime import datetime, timedelta

from django.db.models import Q
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.template.loader import get_template
from django.template import Context, RequestContext
from xhtml2pdf import pisa

from .forms import ProjectTimeForm, AddTaskForm
from .models import Project, ProjectTime, Task, Invoice
from .util import render_to_response


class JsonResponse(HttpResponse):
    def __init__(self, data):
        super(JsonResponse, self).__init__(json.dumps(data),
                                           content_type="application/json")


@login_required
def calendar(request):
    # get latest ProjectTime and use its project as the default
    latest_time = ProjectTime.objects.all().order_by('-created').first()
    if latest_time:
        initial = {'project': latest_time.project.id}
    else:
        initial = {}
    time_form = ProjectTimeForm(initial=initial)

    return render_to_response('projectmanager/calendar.html', {
        'time_form': time_form,
        'has_permission': True,
        'user': request.user,
    }, request)


TASK_FIELDS = ('id', 'task', 'completed')
@login_required
def project_task_data(request):
    # retrieve tasks that are incomplete or completed in the last day
    cutoff = datetime.now() - timedelta(1)
    f = Q(completed=False) | Q(completion_date__gt=cutoff)
    qs = Task.objects.filter(f).order_by('project_id') \
             .values_list('project_id', *TASK_FIELDS)

    data = {}
    for task in qs:
        if not data.get(task[0]):
            data[task[0]] = []
        data[task[0]].append(task[1:])
    return JsonResponse(data)


@login_required
@require_POST
def api_projecttime(request, pk=None):
    if pk:
        projecttime = get_object_or_404(ProjectTime, pk=pk)
    else:
        projecttime = ProjectTime(user=request.user)

    # TODO check permissions here

    print '>>', projecttime.pk
    form = ProjectTimeForm(request.POST, instance=projecttime)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'success': True,
            'event': _projecttime_to_json(projecttime),
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors,
        })

    # for param in ('start', 'end', 'description', 'task_id'):
    #     val = request.POST.get(param)
    #     if val:
    #         setattr(projecttime, param, val)
    #
    # try:
    #     projecttime.full_clean()
    # except ValidationError, e:
    #     return {
    #         'success': False,
    #         'errors': e.message_dict,
    #     }
    #
    # projecttime.save()
    # return {
    #   'success': True,
    # }


@login_required
def api_project_time_list(request):
    date_f = '%Y-%m-%d'
    try:
        date_start = datetime.strptime(request.GET.get('start', ''), date_f)
        date_end = datetime.strptime(request.GET.get('end', ''), date_f)
    except ValueError:
        return HttpResponseBadRequest(u'Invalid start or end date')

    time_qs = ProjectTime.objects.for_user(request.user).filter(
        Q(start__range=(date_start, date_end)) |          # start today
        Q(end__range=(date_start, date_end)) |            # working over midnight
        (Q(start__lt=date_start) & Q(end__gt=date_end))   # spanned multiple days
    ).order_by('start')

    json_data = []
    for projecttime in time_qs:
        json_data.append(_projecttime_to_json(projecttime))

    return JsonResponse(json_data)


@login_required
@require_POST
def api_project_time_add(request):
    form = ProjectTimeForm(request.POST,
                           instance=ProjectTime(user=request.user))
    return _api_project_time_form(form)


@login_required
@require_POST
def api_project_time_edit(request):
    time = ProjectTime.objects.get(pk=int(request.POST['id']))
    form = ProjectTimeForm(request.POST, instance=time)
    return _api_project_time_form(form)


@login_required
@require_POST
def api_project_time_move(request):
    time = ProjectTime.objects.get(pk=int(request.POST['id']))
    # be more relaxed with validation, other fields don't have to be validated.
    time.start = datetime.strptime(request.POST['start'], "%Y-%m-%d %H:%M")
    time.end = datetime.strptime(request.POST['end'], "%Y-%m-%d %H:%M")
    time.save()
    return JsonResponse({
        'status': True,
        'event': _projecttime_to_json(time),
    })


def _api_project_time_form(form):
    if form.is_valid():
        projecttime = form.save()
        return JsonResponse({
            'status': True,
            'event': _projecttime_to_json(projecttime),
        })
    else:
        return JsonResponse({
            'status': False,
            'errors': form.errors
        })


def _projecttime_to_json(projecttime):
    task = projecttime.task
    return  {
        '_id': projecttime.id,
        "_description": projecttime.description,
        '_task': [getattr(task, f) for f in TASK_FIELDS],
        '_project_id': task.project_id,
        'start': projecttime.start.strftime("%Y-%m-%d %H:%M"),
        'end': projecttime.end.strftime("%Y-%m-%d %H:%M"),
        'title': "{0}: {1}".format(projecttime.project, projecttime.task.task),
        # 'allDay': False,
        #'url': '',
    }


@login_required
def tasks(request, project_pk=None):
    task_qs = Task.objects.for_user(request.user)

    completed_tasks = task_qs.filter(completed=True).order_by('-completion_date')
    pending_tasks = task_qs.filter(completed=False).order_by('created')
    project_list = Project.objects.for_user(request.user).filter(archived=False)

    if not project_pk and 'tasks_latest_project_pk' in request.session:
        return redirect(tasks, request.session['tasks_latest_project_pk'])
    elif project_pk == 'all':
        project_pk = None

    if project_pk:
        project = get_object_or_404(Project, pk=project_pk)
        completed_tasks = completed_tasks.filter(project=project)
        pending_tasks = pending_tasks.filter(project=project)
        initial = {'project': project.pk}
        request.session['tasks_latest_project_pk'] = project.pk
    else:
        project = None
        initial = {}

    TaskListFormSet = modelformset_factory(Task, fields=('completed',), extra=0)

    if request.POST and 'task_list-INITIAL_FORMS' in request.POST:
        task_list_formset = TaskListFormSet(request.POST, queryset=pending_tasks, prefix='task_list')
        if task_list_formset.is_valid():
            task_list_formset.save()
            return redirect(request.path_info)
    else:
        task_list_formset = TaskListFormSet(queryset=pending_tasks, prefix='task_list')

    if request.POST and 'addtask-task' in request.POST:
        task_form = AddTaskForm(request.POST, prefix='addtask')
        if task_form.is_valid():
            task = task_form.save()
            return redirect(request.path_info)
    else:
        task_form = AddTaskForm(prefix='addtask', initial=initial)

    data = {
        'project': project,
        'completed_tasks': completed_tasks,
        'project_list': project_list,
        'task_form': task_form,
        'task_list_formset': task_list_formset,
        'has_permission': True,
        'user': request.user,
    }
    return render_to_response('projectmanager/tasks.html', data, request)


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = StringIO()
    status = pisa.CreatePDF(StringIO(html.encode("UTF-8")), dest=result)

    # pdf = pisa.pisaDocument(StringIO(html.encode("UTF-8")), result)
    if status.err:
        return HttpResponse(u"Error creating pdf")

    return HttpResponse(result.getvalue(), content_type='application/pdf')


@login_required
def invoice(request, invoice_id, output='html'):
    data = {
        'invoice': get_object_or_404(Invoice, pk=invoice_id),
        'type': output,
    }
    template_name = 'projectmanager/pdf/invoice.html'
    if output == 'pdf':
        return render_to_pdf(template_name, data)
    else:
        return render_to_response(template_name, data, request)


@login_required
def projecttime_summary(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)

    response = HttpResponse()

    writer = csv.writer(response)
    writer.writerow([
        'Date',
        'Time',
        'Task',
        'Description',
    ])

    for projecttime in project.get_projecttime().order_by('start'):
        writer.writerow([
            projecttime.start.date(),
            "%sh" % projecttime.total_time(),
            projecttime.task.task,
            unicode(projecttime.description),
        ])

    response['Content-Type'] = 'text/csv'
    response['Content-Disposition'] = 'attachment; filename="projecttime_summary_%s.csv"' % project.slug
    return response
