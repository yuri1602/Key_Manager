DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'key_manager',        # Името на базата данни
        'USER': 'user',           # MySQL потребителско име
        'PASSWORD': 'password',       # Паролата за MySQL потребителя
        'HOST': 'localhost',          # Хост (по подразбиране localhost)
        'PORT': '3306',               # Портът за MySQL (по подразбиране 3306)
    }
}
