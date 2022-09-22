from django_todo_app.settings_env.common import *
db = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'tododb',
    'USER': '',
    'PASSWORD': '',
    'HOST': 'localhost',
    'PORT': '',
}
DATABASES = {'default': db, 'session': db, }