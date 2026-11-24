from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from common.mixins import CacheMixin

from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm


# User login view.
class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    # success_ur = reverse_lazy('main:index')
    
    # Returns the page to redirect to after login.
    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse_lazy("user:logout"):
            return redirect_page
        return reverse_lazy('main:index')
    
    # Logs the user in and moves the anonymous session cart to them.
    def form_valid(self, form):
        session_key = self.request.session.session_key
        
        user = form.get_user()
        if user:
            auth.login(self.request, user)
            if session_key:
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(self.request, f"{user.username}, you are logged in")

        return HttpResponseRedirect(self.get_success_url())
                        
    # Adds the page title to the context.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Login'
        return context

# User registration view.
class UserRegistrationVIew(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:profile')
    
    # Saves the user, logs them in and moves the session cart.
    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.save()
        self.object = user

        if user:
            auth.login(self.request, user)
            
        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)
                
        messages.success(self.request, f"{user.username}, you have signed up and are logged in")
        return HttpResponseRedirect(self.get_success_url())
    
    # Adds the page title to the context.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Registration'
        return context


# Account view with profile editing.
class UserProfileView(LoginRequiredMixin, CacheMixin , UpdateView):
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    # Returns the current user as the object to edit.
    def get_object(self, queryset=None):
        return self.request.user
    
    # Shows a message about a successful profile update.
    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully")
        return super().form_valid(form)
    
    # Shows a message about a profile update error.
    def form_invalid(self, form):
        messages.error(self.request, "An error occurred")
        return super().form_invalid(form)
    
    # Adds the title and the user's cached orders to the context.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Account'

        # The query itself could be moved to a separate method of this view
        orders = Order.objects.filter(user=self.request.user).prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            ).order_by("-id")

        context['orders'] = self.set_get_cache(orders, f"user_{self.request.user.id}_orders", 60)
        return context

# User cart page view.
class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'

    # Adds the page title to the context.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Cart'
        return context

# Logs the user out and redirects to the home page.
@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, you have logged out")
    auth.logout(request)
    return redirect(reverse("main:index"))
