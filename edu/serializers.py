from rest_framework import serializers
from .models import Autor, Editora

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nome']
        read_only_fields = ['id']

class EditoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editora
        fields = ['id', 'nome']
        read_only_fields = ['id']
