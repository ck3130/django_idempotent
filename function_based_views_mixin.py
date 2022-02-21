# Class for use with function-based views
import random
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

class IdempotentHelper:

    def __init__(self, request, environment, redirect_to=None):
        self.token = None
        self.request = request
        self.environment = environment
        self.test_name = 'test'
        self.bad_request = False
        self.redirect = None
        self.redirect_to = redirect_to

        self.create_token()
        self.idempotent_check()

    def create_token(self):

        idempo_token_list = self.request.session.__getitem__('idempo_token')
        token = random.randrange(999999)
        while token in idempo_token_list:
            token = random.randrange(999999)
        self.token = token

    def idempotent_check(self):
        if self.request.method == 'POST':            
            if self.environment.get(self.test_name) == 'true':
                pass
            else:
                idempo_token_list = self.request.session.__getitem__('idempo_token')
                token = self.request.POST['idempo_token']
                if not token:
                    self.bad_request = True
                    exception = 'There appears to be an issue with the Idempotent token. Please try your request again. If the problem persists contact easyHUB admin.'
                    self.redirect = render(self.request, '403.html',{'exception': exception}, status=403)
                if str(token) in idempo_token_list:
                    self.bad_request = True
                    self.redirect = HttpResponseRedirect(reverse(self.get_redirect_url()))
                else:
                    idempo_token_list.append(token)
                    self.request.session.__setitem__('idempo_token', idempo_token_list)

    def get_redirect_url(self):
        if not self.redirect_to:
            return 'home'
        else:
            return self.redirect_to 