from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.views.generic import UpdateView, ListView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from pprint import pprint

from .forms import ElementForm, ElementInElementFormSet
from .models import Element, ElementInElement
from .utils import paginate


# def index(request):
#     """Отображаем главную страничку со всеми элементами."""
#     elements_list = Element.objects.all()
#     page_obj = paginate(elements_list, request)
#     context = {'page_obj': page_obj}
#     return render(request, 'main/index.html', context)


class IndexList(ListView):
    model = Element
    template_name = 'main/index.html'
    context_object_name = 'page_obj'


def element_detail(request, element_id):
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


# def element_edit(request, element_id):
#     """Редактируем элемент."""
#     is_edit = True
#     element = get_object_or_404(
#         Element.objects.all(), id=element_id)
#     form = ElementForm(request.POST or None, instance=element)
#     formset = ElementInElementFormSet(request.POST or None, instance=element)
#     if (request.method == 'POST' and form.is_valid()
#             and formset.is_valid()):
#         element = form.save()
#         formset.instance = element
#         formset.save()
#         return redirect('main:element_detail', element_id=element_id)
#     return render(request, 'main/element_create.html',
#                   {'form': form, 'formset': formset,
#                    'is_edit': is_edit})


class ElementUpdate(UpdateView):
    model = Element
    form_class = ElementForm
    template_name = 'main/element_create.html'
    success_url = reverse_lazy('main:element_detail')
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
        return reverse('main:element_detail', kwargs={'element_id': self.object.id})


class ElementCreate(CreateView):
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
        if (self.request.method == 'POST' and form.is_valid()
                and formset.is_valid()):
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect('main:element_detail', element_id=self.object.id)
        else:
            return self.render_to_response(self.get_context_data(form=form))


# def element_create(request):
#     """Создаём элемент и связанные с ним элементы."""
#     form = ElementForm(request.POST or None)
#     formset = ElementInElementFormSet(request.POST or None)
#     if (request.method == 'POST' and form.is_valid()
#             and formset.is_valid()):
#         element = form.save()
#         formset.instance = element
#         formset.save()
#         return redirect('main:element_detail', element_id=element.id)
#     return render(request, 'main/element_create.html',
#                   {'form': form, 'formset': formset})


# class ElementCreate(CreateView):
#     model = Element
#     form_class = ElementForm
#     template_name = 'main/element_create.html'
#     success_url = reverse_lazy('main:index')