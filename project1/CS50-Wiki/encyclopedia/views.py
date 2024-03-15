import re
import random
import markdown2
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render as _render, redirect
from django.contrib import messages
from django.urls import reverse
from functools import wraps
from . import util


def render(req, url, extra={}):
    """
    Hooking into render functionality and dynamically
    making entries list available for all views
    """
    alphabet_list = list(map(chr, range(65, 65 + 26)))
    extra.update(entries_options=util.list_entries(), 
    alphabet_list=alphabet_list,
    debug=settings.DEBUG)

    return _render(req, url, extra)


def referred_message(req, url, msg, level="success"):
    """Handle referred message  when a view is redirect

    Arguments:
        req [dict] -- redirect request object
        url [str]  --  referred url
        msg [str]  -- message to display
        level[str] -- message level. default: success
    """
    referred_url = req.META.get("HTTP_REFERER")
    if referred_url and url in referred_url:
        # dynamically creating message with specified level
        msg_type = getattr(messages, level, None)
        if msg_type:
            msg_type(req, msg)


def index(request):
    entry_list = util.list_entries()
    if request.method == "POST":
        letter = request.POST.get("letter")
        search = request.POST.get("search")
        # Handles searches from index sidebar
        if search is not None:
            search = search.lower().strip()
            for entry in entry_list:
                if search == entry.lower():
                    return redirect("wiki_entry", title=entry)

            entry_list = list(filter(lambda x: search in x.lower(), entry_list))
            if not entry_list:
                return redirect(notFound)

        # Handles A-Z sorted list in index main
        elif letter is not None:
            # map all letter and entry to lowercase
            letter = letter.strip().lower()
            # filter by entries starting with "letter"
            entry_list = list(
                filter(lambda x: x.lower().startswith(letter), entry_list)
            )

    context = {"entries": entry_list}
    return render(request, "encyclopedia/index.html", context)


def wiki_entry(request, title):
    """ Base wiki view to view all available entries"""
    context = {}
    entry_list = util.list_entries()

    # Filter the title  with case-insensitive search
    title = title.strip()
    wiki = [entry for entry in entry_list if title.lower() in entry.lower()]

    if not wiki or wiki is None:
        return redirect(notFound)

    # get Entry by its title
    entry = util.get_entry(wiki[0])
    context["title"] = title
    context["entry"] = markdown2.markdown(entry).strip()
    return render(request, "encyclopedia/base_entry.html", context)


def saveHandler(request, **kwargs):
    """Save Entry

    Arguments:
        request {obj} -- Django request

    Returns:
        [Django redirect] -- redirect view   'index/' or 'wiki/<title>'
    """
    # This view handle saving new and edit entries
    title = kwargs.get("title", "")
    content = kwargs.get("content", "")
    if content and title:
        title = title.strip()
        # re.sub(r"\s", "_", title.strip())
        entry = util.save_entry(title.strip(), str(content).strip())
        return redirect("wiki_entry", title=title)
    return redirect(notFound)


def create_update(request, title=""):
    """Creates or updates wiki entry

    Arguments:
        request {obj} -- Django request
        title {str} -- Name of Wiki entry to update

    Returns:
        [Django view] -- rendered view template 'edit-entry/'
    """

    context = {"config": "create"}
    previous_title = title
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        submit = request.POST.get("submit")
        hidden = request.POST.get("config")

        if submit is None:
            # User cancelled request
            if "create" in hidden:
                # Cancelled creating - redirect to index
                return redirect(index)
            else:
                # Cancelled updating - redirect to wiki entry
                return redirect(reverse("wiki_entry", kwargs={"title": title}))
        elif not title or not content:
            # Submitted but no content was added.
            # (mainly for creation since update already have content)
            # Redirect user to the same page to make changes
            messages.warn(
                request, f" You must add a title and content to create entry!"
            )
            return render(request, "encyclopedia/create_edit_entry.html", context)

        # Setup saving the entry
        action = "updated" if "edit" in hidden else "created"
        if action == "updated":
            # delete previous entry
            util.delete_entry(previous_title)
        messages.success(request, f" Your entry was {action} successfully!")
        return saveHandler(request, title=title, content=content)

    else:  # GET Request
        context = {"config": "create"}  # default value
        if title:
            entry = util.get_entry(title)
            if not entry or entry is None:
                return redirect(notFound)
            context["entry"] = entry
            context["config"] = "edit"

        # Convert entry from html to Markdown
        context.update(
            {
                "title": title,
                "unavailable_entry": util.list_entries(),
            }
        )
    return render(request, "encyclopedia/create_edit_entry.html", context)


def random_entry(request):
    """Random Wiki entry

    Arguments:
        request {obj} -- Django request

        Returns:
            [Django view] -- rendered view template   'delete-entry/'
    """

    entry_list = util.list_entries()
    if entry_list:
        rand_entry = random.choices(entry_list)[0]
        return HttpResponseRedirect(reverse("wiki_entry", args=(rand_entry,)))

    messages.error(request, f"Opp... Something went wrong!")
    return redirect(index)


def delete_entry(request, title, deletion=None):
    """Delete Wiki entry

    Arguments:
        request {obj} -- Django request
        title {str} -- Name of entry to detete

    Returns:
        [Django view] -- rendered view template   'delete-entry/'
    """

    context = {}
    if deletion:
        if title:
            if deletion == "delete":
                util.delete_entry(title)
                messages.error(request, f"{title} was deleted.")
                return redirect("index")
            else:
                messages.warning(request, f"Deleting was cancel {title}.")
                return redirect("wiki_entry", title=title)

    context["title"] = title
    return render(request, "encyclopedia/delete_entry.html", context)


def notFound(request):
    return render(request, "encyclopedia/notfound.html")


def handler_404(request, exception):
    return render(request, "encyclopedia/404.html")
