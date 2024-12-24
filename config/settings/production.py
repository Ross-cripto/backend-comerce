
from .base import *
import dj_database_url



DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://neondb_owner:2rSRjM9bQevV@ep-holy-dawn-a5d8uh5c.us-east-2.aws.neon.tech/neondb?sslmode=require'
    )
}