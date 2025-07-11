from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Fact, Category, UserSavedFact
import random
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import JsonResponse


def random_fact(request):
    facts = Fact.objects.all()
    fact = random.choice(facts) if facts else None
    return render(request, 'random_fact.html', {'fact': fact})


def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})


@login_required
def saved_facts(request):
    saved = UserSavedFact.objects.filter(user=request.user).select_related('fact')
    return render(request, 'saved_facts.html', {'saved_facts': saved})


class FactForm(forms.ModelForm):
    class Meta:
        model = Fact
        fields = ['text', 'category']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введіть цікавий факт...'}),
            'category': forms.Select()
        }
        labels = {
            'text': 'Текст факту',
            'category': 'Категорія',
        }


def add_fact(request):
    if request.method == 'POST':
        form = FactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('random_fact'))
    else:
        form = FactForm()
    return render(request, 'add_fact.html', {'form': form})


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Назва категорії'})
        }
        labels = {
            'name': 'Назва категорії',
        }


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('categories'))
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})


def all_facts(request):
    category_id = request.GET.get('category')
    selected_category = int(category_id) if category_id and category_id.isdigit() else None
    if selected_category:
        facts = Fact.objects.filter(category_id=selected_category)
    else:
        facts = Fact.objects.all()
    categories = Category.objects.all()
    return render(request, 'all_facts.html', {'facts': facts, 'categories': categories, 'selected_category': selected_category})


def upvote_fact(request, fact_id):
    fact = get_object_or_404(Fact, id=fact_id)
    fact.rating = getattr(fact, 'rating', 0) + 1
    fact.save()
    return JsonResponse({'rating': fact.rating})

def downvote_fact(request, fact_id):
    fact = get_object_or_404(Fact, id=fact_id)
    fact.rating = getattr(fact, 'rating', 0) - 1
    fact.save()
    return JsonResponse({'rating': fact.rating})
