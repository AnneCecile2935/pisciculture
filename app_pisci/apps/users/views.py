from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin #restreindre l'accès aux admins
from django.urls import reverse_lazy
from .models import User
from .serializers import UserSerializer
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view

class SignupView(UserPassesTestMixin,CreateView):
    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('user_list')
    template_name = 'users/user_form.html'

    # Methode pour vérifier si l'utilisateur est un admin
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    # Méthode pour rediriger si l'utilisateur n'est pas admin
    def handle_no_permission(self):
        messages.error(self.request, "Seuls les admins peuvent créer des utilisateurs")
        return redirect('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Utilisateur crée avec succès!")
        return response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            return Response(
                {"detail": "Vous ne pouvez pas supprimer votre propre compte"},
                status=status.HTTP_403_FORBIDDEN
            )
        # Règle métier : Seuls les superutilisateurs (via l'admin Django) peuvent supprimer un admin.
        if user.is_admin:
            return Response(
            {"detail": "Un admin ne peut pas supprimer un autre admin"},
            status=status.HTTP_403_FORBIDDEN
        )
        return super().destroy(request, *args, **kwargs)

class CustomLoginView(LoginView):
        template_name = 'registration/login.html'
        authentication_form = CustomAuthenticationForm

        def form_valid(self, form):
            response = super().form_valid(form)
            user = self.request.user
            display_name = user.username if user.username else user.email.split('@')[0]
            messages.success(self.request, f"Bonjour, {display_name}!")
            return response

        def form_invalid(self, form):
            messages.error(self.request, "Identifiants invalides")
            return super().form_invalid(form)



class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Vous avez été déconnecté avec succès.")
        return super().dispatch(request, *args, **kwargs)

class UserUpdateView(UserPassesTestMixin, UpdateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        # Seuls les admins peuvent modifier un utilisateur
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "Seuls les admins peuvent modifier les utilisateurs.")
        return redirect('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Utilisateur mis à jour avec succès !")
        return response

class UserListView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

@api_view(['GET'])
def user_list_json(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
