from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import secrets
from django import forms
import requests
import markdown2

from . import util

# Create form for search bar
class Query(forms.Form):
    query = forms.CharField(label="Search")

# Create form for new page
class NewEntryForm(forms.Form):
    title = forms.CharField(label="title")
    textarea = forms.CharField(label="content", widget=forms.Textarea)

# Index function for Home Page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": Query()
    })

# Function to render each entry
def entry(request, title):
    
    # Check if the entry exists
    if util.get_entry(title) == None:
        
        # If True, render not found page
        return render(request, "encyclopedia/notfound.html", {
            "form": Query(),
        })
    else:
        
        # Else, render entry
        return render(request, "encyclopedia/entry.html", {
            "data": markdown2.markdown(util.get_entry(title)),
            "title": title.capitalize(),
            "form": Query(),
        })

# Search function
def search(request):

    # Check request method
    if request.method == "POST":
        
        # Take in the data the user submitted and save it as form
        form = Query(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Get the query variable from the form
            query = form.cleaned_data["query"]

            # Check if page already exists, if not, then check all entries for matching string
            if util.get_entry(query) == None:
                entries = util.list_entries()
                results = []
                for entry in entries:
                    if query.lower() in entry.lower():
                        results.append(entry)
                
                return render(request, "encyclopedia/results.html", {
                    "results": results,
                    "query": query,
                    "form": Query(),
                })
            
            # If entry exists, redirect user to entry 
            else:
                return HttpResponseRedirect(f"/wiki/{query}")
    else:
        return HttpResponseRedirect("/")

# Get a random entry
def random(request):
    entries = util.list_entries()
    random_entry = secrets.choice(entries)
    return HttpResponseRedirect(f"/wiki/{random_entry}")

# New entry
def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newentry.html", {
            "newentry_form": NewEntryForm(),
            "form": Query(),
        })

    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = NewEntryForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["textarea"]

            entries = util.list_entries()
            if title in entries:
                return HttpResponse("Title already in use")
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(f"/wiki/{title}")

# Redirection for when users type /edit/ without a title
def editredir(request):
    return HttpResponseRedirect("/")

# Edit entry
def edit(request, title):
    if request.method == "GET":
        entry = util.get_entry(title)
        name = title

        class ExistingEntry(forms.Form):
            title = forms.CharField(label="title", initial=name)
            textarea = forms.CharField(label="content", widget=forms.Textarea, initial=entry)

        return render(request, "encyclopedia/editentry.html", {
            "title": title,
            "editform": ExistingEntry(),
            "form": Query()
        })

    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["textarea"]

            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}")
        else:
            return HttpResponse(f"There was an error saving the information. For validity is {form.is_valid()}")