from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm

# Create your tests here.
form = MoveForm(instance="totoro")
print(form.lieu)