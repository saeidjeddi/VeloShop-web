
DJANGO_MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


LOCAL_MIDDLEWARE = [
    
    'utils.erorr_status.JsonResponse404Middleware',
    'utils.erorr_status.JsonResponse403Middleware',
    

]

MIDDLEWARE = DJANGO_MIDDLEWARE + LOCAL_MIDDLEWARE