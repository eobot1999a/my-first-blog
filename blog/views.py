from django.utils import timezone
from django.shortcuts import redirect
from blog.models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm


def post_list(request):
    posts = Post.objects.order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_detail2(request, pk, ps):
    if ps != "123456789": pk = 0
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail2.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
# dump(request.data)
            k = len(Post.objects.all())
            if k > 0:
                p = Post.objects.filter(pk=k)[0]  # last record
               # print('p='+p.title)

               # print('='+form.fields)
                #if p.title == request.POST.title and p.text == request.POST.text:
                #    return redirect('post_list')
            # endif
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
        # endif
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})
    # end if


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})