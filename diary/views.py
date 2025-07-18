from django.shortcuts import render, redirect, get_object_or_404
from .models import Entry
from .forms import EntryForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import json

@login_required
def entry_list(request):
    emotion = request.GET.get('emotion')
    entries = Entry.objects.filter(author=request.user).order_by('-created_at')
    selected_emotion_display = None

    if emotion:
        emotion_map = {
            'happy': '행복',
            'sad': '슬픔',
            'angry': '분노',
            'joy': '즐거움',
            'lethargy': '무기력'
        }
        emotion_code = emotion_map.get(emotion)
        if emotion_code:
            entries = entries.filter(emotion=emotion_code)
            selected_emotion_display = emotion_code

    return render(request, 'diary/entry_list.html', {
        'entries': entries,
        'selected_emotion': selected_emotion_display
    })



def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    return render(request, 'diary/entry_detail.html', {'entry': entry})

@login_required
def entry_create(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.author = request.user
            entry.save()
            return redirect('entry_list')
    else:
        form = EntryForm()
    return render(request, 'diary/entry_form.html', {'form': form})

@login_required
def entry_update(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.author = request.user
            entry.save()
            return redirect('entry_detail', pk=entry.pk)
    else:
        form = EntryForm(instance=entry)
    return render(request, 'diary/entry_form.html', {'form': form})

@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'POST':
        entry.delete()
        return redirect('entry_list')
    return render(request, 'diary/entry_confirm_delete.html', {'entry': entry})

@login_required
def emotion_chart(request):
    data = (
        Entry.objects
        .filter(author=request.user)
        .values('emotion')
        .annotate(count=Count('emotion'))
    )

    if not data.exists():
        labels = []
        counts = []
    else:
        emotion_map = {
            'happy': '행복',
            'sad': '슬픔',
            'angry': '분노',
            'joy': '즐거움',
            'lethargy': '무기력'
        }
        labels = [emotion_map.get(d['emotion'], d['emotion']) for d in data]
        counts = [d['count'] for d in data]

    context = {
        'emotion_labels': json.dumps(labels, ensure_ascii=False),
        'emotion_counts': json.dumps(counts),
    }
    return render(request, 'diary/emotion_chart.html', context)
