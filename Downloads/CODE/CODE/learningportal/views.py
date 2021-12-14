from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import ListView, CreateView, TemplateView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from learningportal.models import Content, WatchListItem, Contact
from main.models import WebsiteUser
from .forms import CustomUserCreationForm


class ContentDetailView(DetailView):
    model = Content

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["already_in_watchlist"] = WatchListItem.objects.filter(content__slug=self.kwargs['slug']).filter(
                user=self.request.user)
        else:
            context["already_in_watchlist"] = False
        # If the content is already in the watchlist, content page will show "remove from the watclist"
        # instead of "add to watchlist"
        return context


class WatchListItemListView(LoginRequiredMixin, ListView):
    ordering = ['-id', ]  # ordering from newer to older
    login_url = reverse_lazy('login')
    paginate_by = 12  # homepage is paginated

    def get_queryset(self):
        return WatchListItem.objects.filter(user=self.request.user).order_by('-id')


class Homepage(ListView):
    model = Content
    paginate_by = 12  # homepage is paginated
    ordering = ['-id', ]
    page_kwarg = 'page'
    template_name = 'learningportal/homepage.html'


def get_http_referer(request):
    # This is a helper function the outputs the previous url of an user.
    # This is used when user is sent back to an url after a request.
    if "HTTP_REFERER" in request.META:
        ref = request.META['HTTP_REFERER']
    else:
        ref = "NA"
    return ref


class ContactCreate(CreateView):
    model = Contact
    fields = ['name', 'email', 'phone', 'message']

    def get_success_url(self):
        return reverse("message_received")


class MessageReceived(TemplateView):
    template_name = "learningportal/message_received.html"


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ContentCreate(LoginRequiredMixin, CreateView):
    model = Content
    fields = ['title', 'short_description', 'text', 'video']
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # adding user information to the post
        return super().form_valid(form)


class WatchItemCreate(LoginRequiredMixin, CreateView):
    model = WatchListItem


@login_required
def deleteFromWatchlist(request, slug):
    kat = get_object_or_404(WatchListItem, content__slug=slug, user=request.user)
    #other users cannot delete each others watch list items
    kat.delete()

    return redirect(get_http_referer(request))


@login_required
def addToWatchList(request, slug):
    cont = Content.objects.get(slug=slug)
    kat = WatchListItem(content=cont, user=request.user)
    kat.save()

    return redirect(get_http_referer(request))


@login_required
def UserContentList(request):
    return redirect(reverse('selectedusercontent-list', kwargs={'id': request.user.id}))


class SelectedUserContentList(ListView):
    paginate_by = 20
    ordering = ['-id', ]
    page_kwarg = 'page'
    template_name = 'learningportal/user_content_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_user = WebsiteUser.objects.get(id=self.kwargs['id'])
        context["selected_user"] = selected_user
        context["same_user"] = selected_user == self.request.user
        #If the user is viewing his/her own content list (uploads) then he will be able to delete items.
        return context

    def get_queryset(self):
        return Content.objects.filter(user=WebsiteUser.objects.get(id=self.kwargs['id']))


def about(request):
    context = {
        "number_of_resources": Content.objects.all().count(),
        "number_of_users": WebsiteUser.objects.all().count(),
    }
    return render(request, "about.html", context=context)
