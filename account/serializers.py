from django.contrib.auth import authenticate, get_user_model
from django.core import validators
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    password = serializers.CharField(label=_('Password'), write_only=True, validators=[
        validators.MinLengthValidator(8, _('Ensure password has at least 8 characters.')),
        validators.MaxLengthValidator(25, _('Ensure password has no more than 25 characters.'))
    ])
    email = serializers.EmailField(label='Email address', max_length=254, validators=[
        UniqueValidator(queryset=get_user_model().objects.all(),
                        message=_('user with this Email address already exists.'))
    ])

    class Meta:
        model = get_user_model()
        fields = '__all__'

    def validate(self, data):

        # Never allow updating password on UserSerializer
        if hasattr(self.instance, 'id'):
            if 'password' in data:
                raise serializers.ValidationError(_('Cannot update password'))
            if 'email' in data:
                raise serializers.ValidationError(_('Cannot update email'))
        return data

