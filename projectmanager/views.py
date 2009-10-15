from projectmanager.models import Project, ProjectTime, Task, Invoice
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from datetime import time as time_module, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory


# pdf stuff
from django import http
from django.template.loader import get_template
from django.template import Context, RequestContext
import ho.pisa as pisa
import cStringIO as StringIO
import cgi


from forms import ProjectTimeForm, AddTaskForm


@login_required
def index(request):
	data = {
		'latest_time_list': ProjectTime.objects.for_user(request.user).order_by('-start'),
		'project_list': Project.objects.for_user(request.user).filter(completed=False).order_by('-start'),
		'completed_project_list': Project.objects.for_user(request.user).filter(completed=True).order_by('-start')
	}
	return render_to_response('projectmanager/index.html', data)	   




@login_required
def project_time(request, current_day = False, start_hour = 8, end_hour = 21):
	snap_hours = 0.25
	
	start_hour = int(start_hour)
	end_hour = int(end_hour)
	total_seconds = float((end_hour - start_hour) * 3600)
	
	if not current_day:
		return HttpResponseRedirect('/time/%s/' % datetime.today().date())
	else:
		data = {
			'current_day': current_day,
			'previous_day': (datetime.strptime(current_day, '%Y-%m-%d') - timedelta(1)).strftime('%Y-%m-%d'),
			'next_day': (datetime.strptime(current_day, '%Y-%m-%d') + timedelta(1)).strftime('%Y-%m-%d'),
			'start_hour': start_hour,
			'end_hour': end_hour,
			'snap_hours': snap_hours,
		}
		
		# process form submission
		if request.method == 'POST': 
			data['time_form'] = ProjectTimeForm(request.POST) 
			if data['time_form'].is_valid():
				data['time_form'].save()
				return HttpResponseRedirect(request.get_full_path())
		else:
			# get latest ProjectTime and use its project as the default
			formData = {
				'project': ProjectTime.objects.all().order_by('-start')[0].project.id
			}
			data['time_form'] = ProjectTimeForm(initial=formData) # An unbound form
	
		
		data['time_list'] = ProjectTime.objects.for_user(request.user).filter(start__gte="%s %s:00:00" % (current_day, start_hour), start__lte="%s %s:59:59" % (current_day, end_hour - 1)).order_by('start')
		for project_time in data['time_list']:
			# divide by a float to make sure we get the fractional part of the answer
#			print round((project_time.start - project_time.start.replace(hour=0, minute=0, second=0)).seconds * 100 / 86400.0, 2)
			
			project_time.display_info = {
				'percentage_position': round(((project_time.start - project_time.start.replace(hour=0, minute=0, second=0)).seconds - start_hour * 3600) * 100 / total_seconds, 2),
				'percentage_height': round((project_time.end - project_time.start).seconds * 100 / total_seconds, 2),
			}
		
		data['hour_dividers'] = []
		for i in range(start_hour, end_hour):
			data['hour_dividers'].append({'time': time_module(i, 0, 0).strftime('%H:%M'), 'percentage_position': (i - start_hour) * 100 / float(end_hour - start_hour)})
				
		return render_to_response('projectmanager/time.html', data)



	
@login_required
def tasks(request, project_pk=None):
    completed_task_list = Task.objects.for_user(request.user).filter(completed=True)
    pending_task_list = Task.objects.for_user(request.user).filter(completed=False)
    project_list = Project.objects.for_user(request.user).filter(completed=False)
    
    if project_pk:
        project = get_object_or_404(Project, pk=project_pk)
        completed_task_list = completed_task_list.filter(project=project)
        pending_task_list = pending_task_list.filter(project=project)
        initial = {'project': project.pk}
    else:
        project = None
        initial = {}
        
    TaskListFormSet = modelformset_factory(Task, fields=('completed',), extra=0)
    
    
    if request.POST and 'task_list-INITIAL_FORMS' in request.POST:
        task_list_formset = TaskListFormSet(request.POST, queryset=pending_task_list, prefix='task_list')
        if task_list_formset.is_valid():
            task_list_formset.save()
            return HttpResponseRedirect(request.path_info)
    else:        
        task_list_formset = TaskListFormSet(queryset=pending_task_list, prefix='task_list')
        
    if request.POST and 'addtask-task' in request.POST:
        task_form = AddTaskForm(request.POST, prefix='addtask')
        if task_form.is_valid():
            task = task_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        task_form = AddTaskForm(prefix='addtask', initial=initial)


	data = {
	    'project': project,
		'completed_task_list': completed_task_list,
		'project_list': project_list,
		'task_form': task_form,
		'task_list_formset': task_list_formset,
	}
	return render_to_response('projectmanager/tasks.html', data)
	




@login_required
def create_invoice_for_project(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	invoice = project.create_invoice()
	return HttpResponseRedirect('/admin/projectmanager/invoice/%d/' % invoice.id)
	



def render_to_pdf(template_src, context_dict):
	template = get_template(template_src)
	context = Context(context_dict)
	html  = template.render(context)
	result = StringIO.StringIO()
	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
	if not pdf.err:
		return http.HttpResponse(result.getvalue(), mimetype='application/pdf')
	return http.HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))


@login_required
def invoice(request, invoice_id, type='html'):
	data = {
		'invoice': get_object_or_404(Invoice, pk=invoice_id),
		'type': type,
	}
	if type == 'pdf':
		return render_to_pdf('projectmanager/pdf/invoice.html', data)
	else:
		return render_to_response('projectmanager/pdf/invoice.html', data, context_instance=RequestContext(request))
