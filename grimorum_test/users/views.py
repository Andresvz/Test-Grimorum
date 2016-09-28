# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render

from django.views.generic import View
from .models import User



class Login(View):
    model = User
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        next_url = request.GET.get('next', None)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            return redirect('/')

class Register(View):
    model = User
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        next_url = request.GET.get('next', None)
        user = User.objects.create(
            username=request.POST['username'],
            email=request.POST['email'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name']
            )
        user.set_password(request.POST['password'])
        user.save()
        user = authenticate(
            username=request.POST['username'], password=request.POST['password']
            )
        login(request, user)
        return redirect('/home')
