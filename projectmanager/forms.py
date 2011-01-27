from django import forms
from models import Project, ProjectTime, Task


def get_project_choices():
    return (('Recent', [(p.pk, p.name) for p in Project.objects.filter(completed=False, hidden=False)]), ('Other', [(p.pk, p.name) for p in Project.objects.filter(completed=False, hidden=True)]))

class ProjectTimeForm(forms.ModelForm):
    project = forms.ChoiceField(choices=get_project_choices())
    def clean_project(self):
        return Project.objects.get(pk=self.cleaned_data['project'])
    
    def __init__(self, *args, **kwargs):
        super(ProjectTimeForm, self).__init__(*args, **kwargs)
        #self['project'].initial = ProjectTime.objects.all().order_by('-start')[0].project
        
        # hack to allow field ordering - http://code.djangoproject.com/ticket/6369
        self.fields.keyOrder = self.Meta.fields
        
        self['project'].field.choices = get_project_choices()

    class Meta:
        model = ProjectTime
        fields = ('start', 'end', 'project', 'description', )



class AddTaskForm(forms.ModelForm):
    #task = forms.CharField()
    project = forms.ModelChoiceField(queryset=Project.objects.filter(completed=False))
    class Meta:
        model = Task
        exclude = ('completed', 'comments', )

        
        
