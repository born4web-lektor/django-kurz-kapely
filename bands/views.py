from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from bands.models import Band, Album, Song
from django.urls import reverse, reverse_lazy
from bands.forms import BandGenericForm, BandModelForm, AlbumModelForm
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView, \
    RedirectView

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin


def is_member_of_group(user, group_names):
    """Otestujeme clenstvi uzivatele ve skupinach, pokud je clenem alespon jedne z nich
    vrati to True jika False

    group_names = str, [name1, name2,....]
    """
    if isinstance(group_names, str):
        rights_exist = user.groups.filter(name=group_names).exists()
    else:
        rights_exist = user.groups.filter(name__in=group_names).exists()
    return rights_exist


def set_session_parametr_value(request, param_name, param_value):
    """"""
    if request and param_name:
        request.session[param_name] = param_value
        return True
    return False


def get_session_parametr_value(request, param_name, pop_data=False):
    object_value = None
    if request and param_name:
        try:
            if pop_data:
                object_value = request.session.pop(param_name)
            else:
                object_value = request.session[param_name]
        except:
            print(f"Parametr {param_name} neexistuje v request.session")
    return object_value


class UserRightsMixin:
    pristupova_prava = []  # seznam skupin ktera maji prava

    def user_has_rights(self, user):
        """"""
        return is_member_of_group(user, self.pristupova_prava)

    def get_context_rights(self):
        context = {'user_has_rights': self.user_has_rights(self.request.user)}
        return context


def print_view_inputs(request, *args, **kwargs):
    """Pomucka print vstupnich parametru View na konzoli"""
    print("----- vstupni parametry view -----")
    print(f"GET: {request.GET}")
    print(f"POST: {request.POST}")
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")
    print("----------------------------------")


# **********************************
# LISTING VIEWS
# **********************************
def band_list_view(request):
    """"""
    print("band_list_view")
    bands = Band.objects.all()
    return render(request,
                  template_name='band_listing_page_template.html',
                  context={'object_list': bands})


class BandListViewGeneric(View):
    """Band List View generic way"""
    def get(self, *args, **kwargs):
        """"""
        print("BandListViewGeneric->get")
        print_view_inputs(self.request, *args, **kwargs)
        bands = Band.objects.all()
        return render(self.request,
                      template_name='band_listing_page_template.html',
                      context={'object_list': bands})


class BandListView(ListView):
    """"""
    model = Band
    template_name = 'band_listing_page_template.html'
    extra_context = {
        # 'show_screen_icon': True,
        # 'show_screen_size': True,
    }

# **********************************
# DETAIL VIEWS
# **********************************
def band_detail_view(request, *args, **kwargs):
    """"""
    print("band_detail_view")
    print_view_inputs(request, *args, **kwargs)
    band = Band.objects.filter(pk=kwargs.get('pk')).first()
    if not band:
        return HttpResponseRedirect(reverse_lazy("bad-data"))
    return render(request,
                  template_name='band_detail_page_template.html',
                  context={'kapela': band})


class BandDetailViewGeneric(View):
    """Band List View generic way"""
    def get(self, *args, **kwargs):
        """"""
        # print("BandDetailViewGeneric->get")
        # print_view_inputs(self.request, *args, **kwargs)
        band = Band.objects.filter(pk=kwargs.get('pk')).first()
        if not band:
            return HttpResponseRedirect(reverse_lazy("bad-data"))
        return render(self.request,
                      template_name='band_detail_page_kapela_object_template.html',
                      context={'kapela': band})


class BandDetailView(DetailView):
    """"""
    model = Band
    template_name = 'band_detail_page_template.html'


class AlbumDetailView(DetailView):
    """"""
    model = Album
    template_name = 'album_detail_page_template.html'


class SongDetailView(DetailView):
    """"""
    model = Song
    template_name = 'song_detail_page_template.html'


# **********************************
# CREATE VIEWS
# **********************************
def band_manual_form_create_view(request, *args, **kwargs):
    """"""
    print("band_manual_form_create_view")
    print_view_inputs(request, *args, **kwargs)

    if request.method == "POST":
        band_name = request.POST.get("band_name")
        band_year = request.POST.get("band_year")
        print(f"Kapela: {band_name} - vznikla: {band_year}")
        return HttpResponseRedirect(reverse_lazy("ok-data"))

    context = {
    }

    return render(request,
                  template_name='band_modify_manual_form_page_template.html',
                  context=context)


def band_create_view_v1(request, *args, **kwargs):
    """"""
    print("band_create_view")
    print_view_inputs(request, *args, **kwargs)

    if request.method == "POST":
        form = BandGenericForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            new_band = Band(**form.cleaned_data)
            new_band.save()
            print(new_band)
            return HttpResponseRedirect(reverse_lazy("ok-data"))
        else:
            # Sem se asi nikdy nedostaneme
            return HttpResponseRedirect(reverse_lazy("bad-data"))
    else:
        formular = BandGenericForm()

    context = {
        "form": formular
    }

    return render(request,
                  template_name='band_modify_page_template.html',
                  context=context)


def band_create_view(request, *args, **kwargs):
    """"""
    print("band_create_view")
    print_view_inputs(request, *args, **kwargs)

    if request.method == "POST":
        form = BandModelForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            new_band = form.save(commit=False)
            new_band.still_active = True
            # new_band = Band(**form.cleaned_data)
            new_band.save()
            # print(new_band)
            return HttpResponseRedirect(reverse_lazy("ok-data"))
        else:
            # Sem se asi nikdy nedostaneme
            return HttpResponseRedirect(reverse_lazy("bad-data"))
    else:
        formular = BandModelForm()

    context = {
        "form": formular
    }

    return render(request,
                  template_name='band_modify_page_template.html',
                  context=context)


class BandCreateViewGeneric(View):
    """Band List View generic way"""
    def get(self, *args, **kwargs):
        """"""
        formular = BandModelForm()
        context = {
            "form": formular
        }
        return render(self.request,
                      template_name='band_modify_page_template.html',
                      context=context)

    def post(self, *args, **kwargs):
        """"""
        form = BandModelForm(self.request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy("ok-data"))
        else:
            return HttpResponseRedirect(reverse_lazy("bad-data"))


class BandCreateView(LoginRequiredMixin,
                     UserRightsMixin,
                     CreateView):
    """"""
    model = Band
    template_name = 'band_modify_page_template.html'
    form_class = BandModelForm
    success_url = reverse_lazy('bands:band-listing')

    pristupova_prava = ["editor", "administrator"]

    def get_context_data(self, **kwargs):
        """"""
        context = super().get_context_data(**kwargs)
        context.update(self.get_context_rights())
        print(context)
        print(self.request.session.values)
        return context


# **********************************
# UPDATE VIEWS
# **********************************
def band_update_view(request, pk, *args, **kwargs):
    """"""
    print("band_update_view")
    print_view_inputs(request, *args, **kwargs)

    try:
        instance = Band.objects.get(pk=pk)
    except Band.DoesNotExist:
        return HttpResponseRedirect(reverse_lazy("bad-data"))

    if request.method == "POST":
        form = BandModelForm(request.POST, instance=instance)
        if form.is_valid():
            print(f"Predana data: {form.cleaned_data}")
            form.save()
            return HttpResponseRedirect(reverse_lazy("ok-data"))
        else:
            # Sem se asi nikdy nedostaneme
            return HttpResponseRedirect(reverse_lazy("bad-data"))
    else:
        formular = BandModelForm(instance=instance)

    context = {
        "form": formular
    }

    return render(request,
                  template_name='band_modify_page_template.html',
                  context=context)


class BandUpdateViewGeneric(View):
    """Band List View generic way"""
    def get(self, *args, **kwargs):
        """"""
        try:
            instance = Band.objects.get(pk=kwargs.get('pk'))
            formular = BandModelForm(instance=instance)
        except Band.DoesNotExist:
            return HttpResponseRedirect(reverse_lazy("bad-data"))

        context = {
            "form": formular
        }
        return render(self.request,
                      template_name='band_modify_page_template.html',
                      context=context)

    def post(self, *args, **kwargs):
        """"""
        try:
            instance = Band.objects.get(pk=kwargs.get('pk'))
        except Band.DoesNotExist:
            return HttpResponseRedirect(reverse_lazy("bad-data"))

        form = BandModelForm(self.request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy("ok-data"))
        else:
            return HttpResponseRedirect(reverse_lazy("bad-data"))


class BandUpdateView(LoginRequiredMixin,
                     UserRightsMixin,
                     UpdateView):
    """"""
    model = Band
    template_name = 'band_modify_page_template.html'
    form_class = BandModelForm
    success_url = reverse_lazy('bands:band-listing')

    extra_context = {
        'show_screen_icon': True,
        'show_screen_size': True,
    }

    pristupova_prava = ["editor", "administrator"]

    def get_context_data(self, **kwargs):
        """"""
        # POKUS HNED SMAZEME
        self.request.session['pocet_kapel'] = Band.objects.all().count()
        print("Pocet kapel:", self.request.session.pop('pocet_kapel'))

        context = super().get_context_data(**kwargs)
        context.update(self.get_context_rights())
        print(context)
        print(self.request.session.values)
        return context


# **********************************
# DELETE VIEWS
# **********************************
def band_delete_view(request, pk, *args, **kwargs):
    """"""
    print("band_delete_view")
    print_view_inputs(request, *args, **kwargs)

    try:
        instance = Band.objects.get(pk=pk)
    except Band.DoesNotExist:
        return HttpResponseRedirect(reverse_lazy("bad-data"))

    if request.method == "POST":
        instance.delete()
        return HttpResponseRedirect(reverse_lazy("bands:band-listing"))

    context = {
        "kapela": instance
    }

    return render(request,
                  template_name='band_delete_page_template.html',
                  context=context)


class BandDeleteViewGeneric(View):
    """Band List View generic way"""
    def get(self, *args, **kwargs):
        """"""
        try:
            instance = Band.objects.get(pk=kwargs.get('pk'))
        except Band.DoesNotExist:
            return HttpResponseRedirect(reverse_lazy("bad-data"))

        context = {
            "kapela": instance
        }
        return render(self.request,
                      template_name='band_delete_page_template.html',
                      context=context)

    def post(self, *args, **kwargs):
        """"""
        try:
            instance = Band.objects.get(pk=kwargs.get('pk'))
        except Band.DoesNotExist:
            return HttpResponseRedirect(reverse_lazy("bad-data"))

        instance.delete()
        return HttpResponseRedirect(reverse_lazy("bands:band-listing"))


class BandDeleteView(DeleteView):
    """"""
    model = Band
    template_name = 'band_delete_page_template.html'
    success_url = reverse_lazy('bands:band-listing')


#
class TestGetParametru(TemplateView):
    """"""
    template_name = 'get_parametry_pokusy_template.html'

    # Interni parametry
    seradit = None
    kapela = None

    def get(self, request, *args, **kwargs):
        """"""
        print("TestGetParametru->get")
        self.seradit = request.GET.get('seradit', 'up')
        if self.seradit not in ['up', 'down']:
            self.seradit = 'up'
        try:
            self.kapela = Band.objects.get(pk=request.GET.get('kapela'))
        except Band.DoesNotExist:
            self.kapela = None
        # nacteni GET parametru
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """"""
        print("TestGetParametru->get_context_data")
        context = super().get_context_data(**kwargs)  # toto probehne standardne
        context['seradit'] = self.seradit
        context['kapela'] = self.kapela
        # tady je prostor pro nase data
        return context


class BandDoesNotExist:
    pass


class AlbumListView(ListView):
    """"""
    model = Album
    template_name = 'album_listing_page_template.html'
    extra_context = {
        # 'show_screen_icon': True,
        # 'show_screen_size': True,
    }

    # Interni parametry
    seradit = None
    kapela = None

    def get(self, request, *args, **kwargs):
        """"""
        print("TestGetParametru->get")
        self.seradit = request.GET.get('seradit', 'up')
        if self.seradit not in ['up', 'down']:
            self.seradit = 'up'
        try:
            self.kapela = Band.objects.filter(pk=request.GET.get('kapela')).first()
        except:
            self.kapela = None
        # nacteni GET parametru
        print(f"Kapela: {self.kapela}")
        print(f"Seradit: {self.seradit}")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """"""
        print("TestGetParametru->get_context_data")
        context = super().get_context_data(**kwargs)  # toto probehne standardne
        context['seradit'] = self.seradit
        context['kapela'] = self.kapela

        return context

    def get_queryset(self):
        """"""
        print("AlbumListView->get_queryset")
        queryset = super().get_queryset()
        if self.seradit == 'up':
            queryset = queryset.order_by('name')
        else:
            queryset = queryset.order_by('-name')

        if self.kapela:
            queryset = queryset.filter(band=self.kapela)

        return queryset


class AccountLoginConfirmationView(TemplateView):
    """"""
    template_name = 'account_login_confirmation_template.html'


class AccountLogoutConfirmationView(TemplateView):
    """"""
    template_name = 'account_logout_confirmation_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_pk = self.request.GET.get("urserid")
        if user_pk:
            context['prihlaseny_uzivatel'] = User.objects.filter(pk=int(user_pk)).first()
        else:
            context['prihlaseny_uzivatel'] = ""
        return context


class AccountLoginView(FormView):
    """"""
    template_name = 'account_login_page_template.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        """"""
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(reverse_lazy('confirm-login'))
        return super().form_valid(form)


class AccountLogoutView(RedirectView):
    """"""
    url = reverse_lazy('confirm-logout')

    uzivatel_odhlaseny = None

    def get(self, request, *args, **kwargs):
        """"""
        self.uzivatel_odhlaseny = request.user
        logout(request)
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        """"""
        user_pk = str(self.uzivatel_odhlaseny.pk)
        return reverse_lazy("confirm-logout") + "?userid=" + user_pk if user_pk else ""


class AccountLogoutYesNoView(TemplateView):
    """"""
    template_name = "account_logout_confirmation_yes_no_page_template.html"


class SessionListParametersView(LoginRequiredMixin,
                                TemplateView):
    """"""
    template_name = "session_list_parameters_page_template.html"


class BandAboutView(TemplateView):
    """"""
    template_name = "bands_about_page_template.html"


class AlbumCreateView(CreateView):
    template_name = "album_modify_page_template.html"
    form_class = AlbumModelForm
    model = Album
    success_url = reverse_lazy('bands:album-list')
    extra_context = {'user_has_rights': True}


class AlbumDeleteView(DeleteView):
    """"""
    model = Album
    template_name = 'album_delete_page_template.html'
    success_url = reverse_lazy('bands:album-listing')


class AlbumUpdateView(LoginRequiredMixin,
                      UserRightsMixin,
                      UpdateView):
    """"""
    model = Album
    template_name = 'album_modify_page_template.html'
    form_class = BandModelForm
    success_url = reverse_lazy('bands:band-listing')

    extra_context = {
        # 'show_screen_icon': True,
        # 'show_screen_size': True,
    }

    pristupova_prava = ["editor", "administrator"]

    def get_context_data(self, **kwargs):
        """"""
        context = super().get_context_data(**kwargs)
        context.update(self.get_context_rights())
        return context


class SongListView(ListView):
    """"""
    model = Song
    template_name = 'song_listing_page_template.html'
    extra_context = {
        'show_screen_icon': True,
        'show_screen_size': True,
    }