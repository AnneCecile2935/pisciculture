from django.views.generic import CreateView
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin #restreindre l'accès aux admins
from django.urls import reverse_lazy
from .models import User
from .serializers import UserSerializer
from .forms import CustomUserCreationForm
from django.contrib import messages
from rest_framework.permissions import IsAdminUser
from rest_framework import status

class SignupView(UserPassesTestMixin,CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

    # Methode pour vérifier si l'utilisateur est un admin
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin

    # Méthode pour rediriger si l'utilisateur n'est pas admin
    def handle_no_permission(self):
        return redirect('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Utilisateur crée avec succès!")
        return response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            return Response(
                {"detail": "Vous ne pouvez pas supprimer votre propre compte"},
                status=status.HTTP_403_FORBIDDEN
            )
        self.check_object_permissions(request, user)
        return super().destroy(request, *args, **kwargs)
