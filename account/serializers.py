from django.contrib.auth import authenticate, get_user_model
from django.core import validators
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    password = PasswordSerializer()
    email = serializers.EmailField(label='Email address', max_length=254, validators=[
        UniqueValidator(queryset=get_user_model().objects.all(),
                        message=_('user with this Email address already exists.'))
    ])

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        # Never allow updating password on UserSerializer
        if hasattr(self.instance, 'id'):
            if 'password' in data:
                raise serializers.ValidationError(_('Cannot update password'))
            if 'email' in data:
                raise serializers.ValidationError(_('Cannot update email'))
        return data


class PasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(label=_('Current password'))
    password = serializers.CharField(label=_('Password'), validators=[
        validators.MinLengthValidator(8, _('Ensure password has at least 8 characters.')),
        validators.MaxLengthValidator(25, _('Ensure password has no more than 25 characters.'))
    ])
    repeat_password = serializers.CharField(label=_('Repeat Password'))

    def validate(self, attrs):
        current_password = attrs.get('current_password')
        password = attrs.get('password')
        repeat_password = attrs.get('repeat_password')
        if current_password and self.context.get('request').user:
            # two new passwords match
            if password != repeat_password:
                raise serializers.ValidationError(_('Password not matching (New password)'))
            # current password match
            credentials = {
                'email': self.context.get('request').user.email,
                'password': current_password
            }
            if not authenticate(**credentials):
                raise serializers.ValidationError(_('Current password not matching'))
        return attrs



