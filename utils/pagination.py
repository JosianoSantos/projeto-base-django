from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, HttpResponseRedirect
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView


class PaginateUpdateView(UpdateView):
    success_url = None
    list_url = None
    create_url = None
    update_url = None

    # def get_success_url(self):
    #     params = urlparse.urlparse(self.request.META.get('HTTP_REFERER')).query
    #     return reverse(self.success_url)


class PaginateListView(ListView):
    paginate_by = 4

    def get(self, *args, **kwargs):
        request = self.request
        try:
            return super().get(*args, **kwargs)
        except Http404:
            if request.GET.get('page', 1) == 1:
                raise
            params = request.GET.copy()
            del params['page']
            return HttpResponseRedirect('%s?%s' % (request.path, params.urlencode()))

    def get_lines(self):
        lines = self.get_queryset()
        paginator = Paginator(lines, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            show_lines = paginator.page(1)
        except EmptyPage:
            show_lines = paginator.page(paginator.num_pages)
        return show_lines

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['params'] = self.request.GET.copy().urlencode()
        context['object_list'] = self.get_lines()
        return context
