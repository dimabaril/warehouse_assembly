from django.core.paginator import Paginator

# from yatube.settings import POSTS_PER_PAGE
ELEMENT_PER_PAGE = 10


def paginate(posts_list, request):
    """Разбиваем контент на страницы."""
    paginator = Paginator(posts_list, ELEMENT_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
