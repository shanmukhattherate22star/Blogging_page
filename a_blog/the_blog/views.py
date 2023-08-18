from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from .forms import PostForm, EditForm, CategoryForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# Create your views here.
#def home(request):
#	return render(request, 'home.html', {})
def LikeView(request, pk):
    post = get_object_or_404(Post, id=pk)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
    	post.likes.remove(request.user)
    	liked = False
    else:
    	post.likes.add(request.user)
    	liked = True
    
    return HttpResponseRedirect(reverse('article_detail', args=[str(pk)]))



class HomeView(ListView):
	model = Post
	template_name = 'home.html'
	ordering = ['-post_date']

	def get_context_data(self, *args,  **kwargs):
		cat_menu = 	Category.objects.all()
		context = super(HomeView, self).get_context_data(*args,  **kwargs)
		context["cat_menu"] = cat_menu
		return context

def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    context = {
        'cat_menu_list': cat_menu_list
    }
    return render(request, 'category_list.html', context)


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-',''))
    context = {
        'cats': cats.title(),
        'category_posts': category_posts,
        'post': category_posts.first()  # Pass the first post in the context
    }
    return render(request, 'categories.html', context)


class ArticleDetailView(DetailView):
	model = Post
	template_name = 'article_details.html'

	def get_context_data(self, *args,  **kwargs):
		cat_menu = 	Category.objects.all()
		context = super(ArticleDetailView, self).get_context_data(*args,  **kwargs)
		stuff = get_object_or_404(Post, id = self.kwargs['pk'])
		total_likes = stuff.total_likes()
		liked = False
		if stuff.likes.filter(id=self.request.user.id).exists():
			liked = True
		context["cat_menu"] = cat_menu
		context["total_likes"] = total_likes
		context["liked"]= liked
		return context

class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    #fields = '__all__'
	# or fields=('title','body')create a list or tuple pass how many u want

class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    form_class = CategoryForm

    def get_success_url(self):
        return reverse('home')


class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'
    #fields = '__all__'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']  # Assign the current user to the profile
        return super().form_valid(form)

class UpdatePostView(UpdateView):
	model = Post
	template_name = 'update_post.html'
	form_class = EditForm

class DeletePostView(DeleteView):
	model = Post
	template_name = 'delete_post.html'
	success_url = reverse_lazy('home')


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('article_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})
