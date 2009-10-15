from django.contrib import admin



class RestrictedByUsers(admin.ModelAdmin):
    """Restrict editing and viewing of items in the admin based on an ownership field.
    
    See: http://www.djangosnippets.org/snippets/1054/ and
         http://blog.dougalmatthews.com/2008/10/filter-the-django-modeladmin-set/"""
    user_field = 'users'    # The user field on the model
    is_many_field = True    # Is it a ManyToMany (True) or a ForeignKey (False)?
    save_callback = None

    def queryset(self, request):
        qs = self.model._default_manager.get_query_set()
        if not request.user.is_superuser:
            qs = qs.filter(**{self.user_field: request.user})
        return qs

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not self.is_many_field:
            setattr(obj, self.user_field, request.user)
        
        if self.save_callback: self.save_callback(request, obj)
        obj.save()
        
        if not request.user.is_superuser and self.is_many_field:
            getattr(obj, self.user_field).add(request.user)

    def has_change_permission(self, request, obj=None):
        if not obj or not obj.pk:
            return True # So they can see the change list page
        if request.user.is_superuser or self._belongs_to_user(obj, request.user):
            return True
        else:
            return False
    has_delete_permission = has_change_permission    

    def _belongs_to_user(self, obj, user):
        if self.is_many_field:
            return user in getattr(obj, self.user_field).all()
        else:
            return user == getattr(obj, self.user_field)
    