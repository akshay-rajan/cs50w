from django.shortcuts import render
from django import forms
import markdown2
from random import randrange
import re

from . import util
from encyclopedia.forms import searchForm, newEntry, editEntry


def index(request):
    """ Return the home page showing the list of entries """

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": searchForm()
    })


def getpage(request, title):
    """ Implement the wiki page by converting MarkDown to HTML """

    entry_list = util.list_entries()


    # To ignore the case in user query
    for entry_name in entry_list:
        if entry_name.lower() == title.lower():
            title = entry_name
            return render(request, "encyclopedia/entry.html", {
                "title":title,
                "entry": markdown2.markdown(util.get_entry(title)),
                "form": searchForm()
            })

    # If the entry does not exist
    return render(request, "encyclopedia/error.html", {
        "error":"The page you are looking for does not exist!"
    })


def search(request):
    """ Take the user to an entry if found. Else, render a page containing all possible matches"""

    if request.method == "POST":
        form = searchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search"]
            entry_list = util.list_entries()

            # If the entry is found
            for entry_name in entry_list:
                if entry_name.lower() == query.lower():
                    query = entry_name
                    return getpage(request, query)

            # If the entry is not found
            matching_entries = []

            # Convert the query to a regular expression pattern (case-insensitive)
            pattern = re.compile(re.escape(query), re.IGNORECASE)
            for entry in entry_list:
                if pattern.search(entry):
                    matching_entries.append(entry)

            return render(request, "encyclopedia/search.html", {
                "form": searchForm(),
                "title": query,
                "entries": matching_entries
            })


def newpage(request):
    """ Create a new wiki entry and save it to the disk """

    if request.method == "POST":
        form = newEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["textarea"]

            # Check whether the title is valid
            entry_list = util.list_entries()
            for entry in entry_list:
                if title.lower() == entry.lower():
                    return render(request, "encyclopedia/error.html", {
                        "error":"An entry of the same name already exists!"
                    })

            # If valid, save the entry as a markdown file to the disc
            util.save_entry(title, content)
            # Redirect to the new html by calling the getpage() function created above
            return getpage(request, title)

    return render(request, "encyclopedia/newpage.html", {
        "form": searchForm(),
        "newentry": newEntry()
    })


def edit(request):
    """ Edit the current page """

    # Implement submit action
    if request.method == "POST":
        form = editEntry(request.POST)
        if form.is_valid():
            content = form.cleaned_data["textarea"]
            title = form.cleaned_data["title"]
            util.save_entry(title, content)
            return getpage(request, title)

    # Render a page which enables the editing, passing the current contents as the default value of the textarea
    title = request.GET.get("title")
    form = editEntry()
    form.fields["textarea"].initial = util.get_entry(title)
    form.fields["title"].initial = title
    return render(request, "encyclopedia/edit.html", {
        "edit_field": form,
        "form": searchForm()
    })


def random(request):
    """ Take user to a random encyclopedia entry """

    entries = util.list_entries()
    random_entry = entries[randrange(0,len(entries))]
    return getpage(request, random_entry)

