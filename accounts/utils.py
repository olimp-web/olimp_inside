from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import *
#
# from django.views import

# class ObjectRegistrUserMixin:
#     model_form = None
#     template = None
#
#     def get(self, request):
#         form =  self.model_form()
#         return render(request, self.template, context={'form': form})
#
#     def post(self, request):
#         bound_form = self.model_form(request.POST)
#
#         if bound_form.is_valid():
#             new_obj = bound_form.save()
#             return redirect()