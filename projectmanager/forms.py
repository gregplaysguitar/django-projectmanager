from datetime import datetime, timedelta

from django import forms
from .models import Project, ProjectTime, Task


def get_project_choices(user):
    qs = Project.objects.filter(archived=False).for_user(user)
    recent = qs.filter(task__projecttime__created__gte= \
                       datetime.now() - timedelta(7)).distinct()[:5]
    other = qs.exclude(pk__in=(p.pk for p in recent))
    return (('Recent', [(p.pk, p.name) for p in recent]),
            ('Other', [(p.pk, p.name) for p in other]))


class ProjectTimeForm(forms.ModelForm):
    project = forms.ChoiceField(choices=[])
    def clean_project(self):
        return Project.objects.get(pk=self.cleaned_data['project'])

    task = forms.CharField(widget=forms.Select, required=False)
    def clean_task(self):
        task = self.cleaned_data.get('task')
        if task:
            try:
                return Task.objects.get(pk=task)
            except Task.DoesNotExist:
                raise forms.ValidationError(u'Select a valid task')
        return None

    new_task = forms.CharField(max_length=190, required=False)
    completed = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(ProjectTimeForm, self).__init__(*args, **kwargs)
        self['project'].field.choices = get_project_choices(request.user)

    class Meta:
        model = ProjectTime
        fields = ('start', 'end', 'project', 'task', 'new_task', 'completed',
                  'description', )

    def clean(self):
        data = self.cleaned_data
        if not data.get('task'):
            if not data.get('new_task'):
                raise forms.ValidationError(u'Specify a task')
            data['task'] = Task.objects.create(task=data['new_task'],
                                               project=data['project'])
        return data

    def save(self, *args, **kwargs):
        obj = super(ProjectTimeForm, self).save(*args, **kwargs)

        # only set completed if specified, otherwise leave alone
        # TODO let this form "uncomplete" tasks once we have recently-completed
        # available in the list
        if self.cleaned_data.get('completed'):
            self.cleaned_data['task'].completed = True
            if kwargs.get('commit', True):
                self.cleaned_data['task'].save()

        return obj


class AddTaskForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.none())

    class Meta:
        model = Task
        exclude = ('completed', )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(ProjectTimeForm, self).__init__(*args, **kwargs)
        self['project'].field.choices = \
            Project.objects.filter(archived=False).for_user(request.user)
