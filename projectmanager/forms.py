from django import forms
from models import Project, ProjectTime, Task



class ProjectTimeForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.filter(completed=False))
    
    def __init__(self, *args, **kwargs):
        super(ProjectTimeForm, self).__init__(*args, **kwargs)
        #self['project'].initial = ProjectTime.objects.all().order_by('-start')[0].project
        
        # hack to allow field ordering - http://code.djangoproject.com/ticket/6369
        self.fields.keyOrder = self.Meta.fields

    class Meta:
        model = ProjectTime
        fields = ('start', 'end', 'project', 'description', )



class AddTaskForm(forms.ModelForm):
    #task = forms.CharField()
    project = forms.ModelChoiceField(queryset=Project.objects.filter(completed=False))
    class Meta:
        model = Task
        exclude = ('completed', 'comments', )

        
        
