from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Issue
from .forms import IssueUploadForm


def home(request):
    # Mostra a última edição em destaque e uma lista do histórico
    latest = Issue.objects.order_by('-start_date', '-created_at').first()
    others = Issue.objects.exclude(id=latest.id) if latest else Issue.objects.none()
    return render(request, 'issue_list.html', {'latest': latest, 'others': others})


def issue_detail(request, slug):
    issue = get_object_or_404(Issue, slug=slug)
    pages = issue.pages.all()
    return render(request, 'issue_detail.html', {'issue': issue, 'pages': pages})


def issue_upload(request):
    if request.method == 'POST':
        form = IssueUploadForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save()
            messages.success(request, 'Edição enviada com sucesso!')
            return redirect(issue.get_absolute_url())
        else:
            messages.error(request, 'Verifique os campos do formulário.')
    else:
        form = IssueUploadForm()
    return render(request, 'issue_upload.html', {'form': form})