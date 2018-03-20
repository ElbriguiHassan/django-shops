from django.conf import settings

APP_SETTINGS_NAMESPACE = 'DJANGO_SHOPS_'
STATUS_PENDING_APPROVAL = 0
STATUS_ACTIVE = 1


def get_or_set_default_settings(setting_name, default_values=None, settings_namespace=APP_SETTINGS_NAMESPACE):
    return getattr(settings, '{}{}'.format(settings_namespace, setting_name), default_values)


_app_settings = dict(
    STATUS_PENDING_APPROVAL=STATUS_PENDING_APPROVAL,
    STATUS_ACTIVE=STATUS_ACTIVE,
    DELETE_FROM_DB=True,

    USER_ALLOWED_FIELDS=(
        'email',
        'password',
        'id',
    )
)


class LazyAppSettings(object):
    def __getattr__(self, key):
        for setting, default_value in _app_settings.items():
            if setting == key:
                return get_or_set_default_settings(setting, default_value, APP_SETTINGS_NAMESPACE)
        raise AttributeError("'{}' is not defined in settings.".format(key))


app_settings = LazyAppSettings()


app_settings.DEFAULT_STATUS = app_settings.STATUS_ACTIVE

app_settings.STATUSES = (
    (app_settings.STATUS_PENDING_APPROVAL, 'Pending approval'),
    (app_settings.STATUS_ACTIVE, 'Active'),
)
