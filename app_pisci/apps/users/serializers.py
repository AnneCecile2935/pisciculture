from rest_framework import serializers # module DRF pour créer des serialiseurs
from django.contrib.auth import get_user_model # récuprère le modèle User personnalisé dans user/models.py
from django.contrib.auth.hashers import make_password # fct django pour hacher les mots de passe

User = get_user_model()

# pour l'Admin
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        #indique que ce serializer est lié au model User qu'on a récupéré
        model = User
        # liste des champs du modele à inclure dans le JSON
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'is_admin', 'password']
        # Permet de personnaliser certains champs
        extra_kwargs = {
            'password': {
                'write_only': True, # ne sera jamais renvoyé dans la réponse
                'min_length': 8,
                'error_messages': {
                    'required': 'Le mot de passe est obligatoire',
                    'min_length': 'Le mot de passe doit contenir au moins 8 caractères',
                    'blank': 'Ce champ ne peut pas être vide'
                }, # ne mdp n'est jamais renvoyé en clair, peut seulement être envoyé
            },
            'is_admin': {
                'read_only': True, # champ non modifiable
                'error_messages': {
                    'read_only': 'Seul un administrateur peut modifier ce champ'
                }
            },
            'email': {
                'error_messages': {
                    'required': 'Une adresse email est obligatoire',
                    'invalid': 'Veuillez entrer une adresse email valide (ex: user@eaxmple.com)',
                    'blank': 'Ce champ ne peut pas être vide'
                }
            },
            'username': {
                'error_messages': {
                    'required': 'Un nom d\'utilisateur est obligatoire',
                    'blank': 'Un nom d\'utilisateur est obligatoire'
                }
            },
        }
        read_only_fields = ['is_staff']

    def to_internal_value(self, data):
        # Vérifie si is_admin ou is_staff sont présents dans les données
        if 'is_admin' in data:
            raise serializers.ValidationError({
                'is_admin': 'Seul un administrateur peut modifier ce champ'
            })
        if 'is_staff' in data:
            raise serializers.ValidationError({
                'is_staff': ["Ce champ ne peut pas être modifié via l\'API"]
            })
        return super().to_internal_value(data)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance,validated_data)
