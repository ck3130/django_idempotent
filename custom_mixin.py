# custom mixin for class-based views
from django.http import HttpResponseRedirect
from django.urls import reverse
import os

import random

class IdempotentMixin:
    idempo_redirect = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        idempo_token_list = self.request.session.__getitem__('idempo_token')
        token = random.randrange(999999)
        while token in idempo_token_list:
            token = random.randrange(999999)
        context['idempo_token'] = token
        return context

    def post(self, request, *args, **kwargs):       
        if os.environ.get('test') == 'true':
            return super().post(self, request, *args, **kwargs)
        else:

            idempo_token_list = self.request.session.__getitem__('idempo_token')
            token = self.request.POST['idempo_token']
            if str(token) in idempo_token_list:
                return HttpResponseRedirect(reverse(self.get_idempo_redirect()))
            else:
                idempo_token_list.append(token)
                self.request.session.__setitem__('idempo_token', idempo_token_list)
            return super().post(self, request, *args, **kwargs)

    def get_idempo_redirect(self):
        if not self.idempo_redirect:
            return 'home'
        else:
            return self.idempo_redirect