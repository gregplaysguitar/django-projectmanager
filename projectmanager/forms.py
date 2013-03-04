from django import forms
from models import Project, ProjectTime, Task


def get_project_choices():
    return (('', '---------'), ('Recent', [(p.pk, p.name) for p in Project.objects.filter(completed=False, hidden=False)]), ('Other', [(p.pk, p.name) for p in Project.objects.filter(completed=False, hidden=True)]))


class ProjectTimeForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), required=False)
    
    def __init__(self, *args, **kwargs):
        super(ProjectTimeForm, self).__init__(*args, **kwargs)
        
        # hack to allow field ordering - http://code.djangoproject.com/ticket/6369
        self.fields.keyOrder = self.Meta.fields
        
        self.fields['project'].choices = get_project_choices()
        self.fields['task'].queryset = Task.objects.filter(completed=False)
        self.fields['task'].required = False
        self.fields['description'].required = False
    
    class Meta:
        model = ProjectTime
        fields = ('start', 'end', 'task', 'project', 'description', )

    def clean(self):
        data = self.cleaned_data
        
        if not data['task'] and not data['project']:
            raise forms.ValidationError('Please select a task or a project')
        
        if data['task'] and not data['project']:
            data['project'] = data['task'].project
        
        if not data['description']:
            if data['task']:
                data['description'] = data['task'].task
            else:
                raise forms.ValidationError('One of description or task is required.')
        
        return data
    
    def _post_clean(self):
        '''This triggers model validation, which fails badly if project is not set, so 
           only go ahead if there are no form errors.'''
        if not self.errors:
            super(ProjectTimeForm, self)._post_clean()
        

class AddTaskForm(forms.ModelForm):
    #task = forms.CharField()
    project = forms.ModelChoiceField(queryset=Project.objects.filter(completed=False))
    class Meta:
        model = Task
        exclude = ('completed', 'comments', )

        
        
