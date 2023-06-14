from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Subscription
from .filters import PostFilter
from .forms import newsForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'NEWS.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'new1.html'
    context_object_name = 'new1'


class NwCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post',)
    form_class = newsForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        form.instance.author = self.request.user.author
        return super().form_valid(form)


class ArCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post',)
    form_class = newsForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        form.instance.author = self.request.user.author
        return super().form_valid(form)



class NwDelete(DeleteView):
    model = Post
    template_name = 'nw_delete.html'
    success_url = reverse_lazy('post_list')


class ArDelete(DeleteView):
    model = Post
    template_name = 'ar_delete.html'
    success_url = reverse_lazy('post_list')


class newsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post',)
    form_class = newsForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('post_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(user=request.user, category=category,).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(Subscription.objects.filter(user=request.user, category=OuterRef('pk'),))).order_by('name')

    return render(request, 'sb/subscriptions.html', {'categories': categories_with_subscriptions},)
