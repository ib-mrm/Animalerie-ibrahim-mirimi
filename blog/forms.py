# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 18:05:28 2022

@author: mirel
"""

from django import forms
 
from .models import Animal
 
class MoveForm(forms.ModelForm):
 
    class Meta:
        model = Animal
        fields = ('lieu',)