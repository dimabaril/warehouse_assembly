from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, DeleteView, ListView, UpdateView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from pprint import pprint

from .forms import ElementForm, ElementInElementFormSet
from .models import Element, ElementInElement
from .utils import paginate


class IndexList(ListView):
    model = Element
    template_name = 'main/index.html'
    context_object_name = 'page_obj'


def element_detail(request, element_id):  # переписать на DetailView наверное
    """Отображаем элемент фильтруя по id и прочую инфу."""
    element = get_object_or_404(
        Element.objects.all(), id=element_id)

    # print(element.from_elems.all())  # set of ElementInElement
    # print(element.include.all())  # set of Element

    # elem_in_elem = (
    #     ElementInElement.objects.filter(from_elem=element)
    #     .select_related('to_elem'))
    elem_in_elems = element.from_elems.select_related('to_elem')

    context = {
        'element': element,
        'elem_in_elems': elem_in_elems,
        # 'include': include,
    }
    return render(request, 'main/element_detail.html', context)


class ElementDetail(DetailView):
    model = Element
    template_name = 'main/element_detail.html'
    # context_object_name = 'element'
    pk_url_kwarg = 'element_id'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['elem_in_elems'] = self.object.from_elems.select_related('to_elem')
        # data['include'] = self.object.include.all()
        # print(self.object.from_elems.last().to_elem.include.all())
        return data


class ElementCreate(LoginRequiredMixin, CreateView):
    model = Element
    form_class = ElementForm
    template_name = 'main/element_create.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ElementInElementFormSet(self.request.POST)
        else:
            data['formset'] = ElementInElementFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if (self.request.method == 'POST' and form.is_valid()  # Нужно ли здесь это? self.request.method == 'POST' and form.is_valid() большой вопрос, скорее нет.
                and formset.is_valid()):
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
            # return redirect('main:element_detail', element_id=self.object.id)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('main:element_detail', kwargs={'element_id': self.object.id})


class ElementUpdate(LoginRequiredMixin, UpdateView):
    model = Element
    form_class = ElementForm
    template_name = 'main/element_create.html'
    # success_url = reverse_lazy('main:element_detail')
    pk_url_kwarg = 'element_id'  # либо поправить юрл на <int:pk>

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['is_edit'] = True
        if self.request.POST:
            data['formset'] = ElementInElementFormSet(self.request.POST, instance=self.object)
        else:
            data['formset'] = ElementInElementFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if (self.request.method == 'POST' and form.is_valid()
                and formset.is_valid()):
            # Check if a record with the same from_elem and to_elem already exists
            # for element_in_element_form in formset:
            #     from_elem = element_in_element_form.cleaned_data.get('from_elem')
            #     to_elem = element_in_element_form.cleaned_data.get('to_elem')
            #     if ElementInElement.objects.filter(from_elem=from_elem, to_elem=to_elem).exists():
            #         return self.form_invalid(form)

            self.object = form.save()
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
            # return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('main:element_detail', kwargs={'element_id': self.object.id})


class ElementDelete(LoginRequiredMixin, DeleteView):
    model = Element
    success_url = reverse_lazy('main:index')
    pk_url_kwarg = 'element_id'
