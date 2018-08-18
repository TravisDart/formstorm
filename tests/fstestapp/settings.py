DATABASES = {
    'default': {
        'NAME': 'db.sqlite3',
        'ENGINE': 'django.db.backends.sqlite3',
    },
}
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'tests',
]
SECRET_KEY = 'password'
