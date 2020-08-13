from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse
from django.views import generic
from groups.models import Group,GroupMember
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from . import models
# Create your views here.
class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields=('name','description')
    model=Group
    template_name="group_form.html"

class SingleGroup(generic.DetailView):
    model=Group
    template_name="group_detail.html"
    

class ListGroups(generic.ListView):
    model=Group
    template_name="group_list.html"

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        
        except IntegrityError:
            messages.warning(self.request,"warning! already a member")
        
        else:
            messages.add_message(self.request,messages.INFO,"you are now a member")
        
        return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
   
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
    

    def get(self,request,*args,**kwargs):
        try:
            membership=GroupMember.objects.filter(user=self.request.user,group__slug=self.kwargs.get('slug')).get()
        
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,"sorry you are not in this group")
        else:
            membership.delete()
            messages.success(self.request,"you left the group")
        return super().get(request,*args,**kwargs)
        