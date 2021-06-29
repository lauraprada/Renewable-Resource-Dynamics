from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'indicadora_tratamiento_precio_fijo': -99,
    'indicadora_tratamiento_captura_deterministica':-99,
    'real_world_currency_per_point': 1.00,
    'participation_fee': 0.00,
    'doc': "",
}

SESSION_CONFIGS = [
    {
        'name': 'bienes_comunes',
        'display_name': "Bienes comunes Aleatorio",
        'num_demo_participants': 4,
        'indicadora_tratamiento_precio_fijo': -99,
        'doc': """
        Las indicadoras de tratamiento asumen valores de 0 y 1.
        El valor por defecto es missing (-99)
        Si desea tratamientos aleatorizados por grupos, no modifique las indicadoras.
        """,
        'indicadora_tratamiento_captura_deterministica':-99,
        'app_sequence': ['bienes_comunes'],
    },
    {
        'name': 'bienes_comunes_fixed_determ',
        'treatment': 'fixed_determ',
        'display_name': "Bienes comunes precio fijo pez deterministico",
        'num_demo_participants': 4,
        'indicadora_tratamiento_precio_fijo': -99,
        'doc': """
        Las indicadoras de tratamiento asumen valores de 0 y 1.
        El valor por defecto es missing (-99)
        Si desea tratamientos aleatorizados por grupos, no modifique las indicadoras.
        """,
        'indicadora_tratamiento_captura_deterministica':-99,
        'app_sequence': ['bienes_comunes'],
    },
    {
        'name': 'bienes_comunes_fixed_stock',
        'treatment' : 'fixed_stock',
        'display_name': "Bienes comunes precio fijo pez estocástico",
        'num_demo_participants': 4,
        'indicadora_tratamiento_precio_fijo': -99,
        'doc': """
        Las indicadoras de tratamiento asumen valores de 0 y 1.
        El valor por defecto es missing (-99)
        Si desea tratamientos aleatorizados por grupos, no modifique las indicadoras.
        """,
        'indicadora_tratamiento_captura_deterministica':-99,
        'app_sequence': ['bienes_comunes'],
    },
    {
        'name': 'bienes_comunes_cond_determ',
        'treatment': 'cond_determ',
        'display_name': "Bienes comunes precio condicional pez deterministico",
        'num_demo_participants': 4,
        'indicadora_tratamiento_precio_fijo': -99,
        'doc': """
        Las indicadoras de tratamiento asumen valores de 0 y 1.
        El valor por defecto es missing (-99)
        Si desea tratamientos aleatorizados por grupos, no modifique las indicadoras.
        """,
        'indicadora_tratamiento_captura_deterministica':-99,
        'app_sequence': ['bienes_comunes'],
    },
    {
        'name': 'bienes_comunes_cond_stock',
        'treatment': 'cond_stock',
        'display_name': "Bienes comunes precio condicional pez estocástico",
        'num_demo_participants': 4,
        'indicadora_tratamiento_precio_fijo': -99,
        'doc': """
        Las indicadoras de tratamiento asumen valores de 0 y 1.
        El valor por defecto es missing (-99)
        Si desea tratamientos aleatorizados por grupos, no modifique las indicadoras.
        """,
        'indicadora_tratamiento_captura_deterministica':-99,
        'app_sequence': ['bienes_comunes'],
    },
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'es'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'COP'
USE_POINTS = True



# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


# Consider '', None, and '0' to be empty/false
DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

DEMO_PAGE_INTRO_HTML = """ """

# don't share this with anybody.
SECRET_KEY = 'y3u*$8gy-73&i^0)*)-6uyy93qgule-q^^aj#__zzyn7g7!pse'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
