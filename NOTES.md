--------------------------------------------------------------------------------
# DJANGO API
--------------------------------------------------------------------------------

## ENV SETUP
>>> python -m venv <env-name>
>>> Set-ExecutionPolicy Unrestricted -Force (so poweshell allows execution of the script)
>>> <env-name>/Scripts/activate
once the env is activated:
>>> pip install django
>>> django-admin startproject <project-name>
in the project directory:
>>> python manage.py migrate (create DB)
>>> python manage.py createsuperuser(create admin user)`
<!-- DELETE ON PUBLISH -->
user: sowerbean
pwd: jsqjrln1997
>>> python manage.py runserver
-------------------------------------------------------------------------------

## Djando REST framework
>>> pip install pipenv
in the avtive env: 
>>> pipenv install djangorestframework
create app:
>>> python manage.py startapp <app-name>
add app to 'INSTALLED_APPS' in the 'cfm_data.settings' module
-------------------------------------------------------------------------------

### MODELS:
- create urls in 'cfm_data_api.urls'
- add created urls to app to 'cfm_data_api.urls'
- create models in 'cfm_data_api.models'
- make migrations to DB:
>>> python manage.py makemigrations
- register models in 'Admin.py'
### SERIALIZERS (tool for translating to and from JSON):
- create the 'cfm_data_api.serialiers.py'
- add serializers
### VIEWS:
- add views to 'cfm_data_api.views'
- create a 'router' and add views, both in 'cfm_data_api.urls' module

//PROBLEM: 'rest_framework' is not importing
=> restart 'vscode'

- apply migrations:
>>> python manage.py migrate
- rerun the server
>>> python manage.py runserver
-------------------------------------------------------------------------------

### RELASHIONSHIPS:
- create models with their relashionships in 'cfm_data_api.models'
- add serializers for each model in 'cfm_data_api.serializers'
- add views to 'cfm_data_api.views'
- register urls in 'cfm_data_api.urls'
- register models in 'cfm_data_api.admin'
-------------------------------------------------------------------------------

### PERMISSIONS:
ON INDIVIDUAL VIEWS:
- add urls to 'cfm_data.urls'
```python
    path('api-auth', include('rest_framework.urls'))
```
- add permissions to classes in 'cfm_data.views'
```python
    # the comma is needed at the end
    class...:
        ...
        permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
        ...
```
 OR IN APP SETTINGS:
 - add this variable to 'cfm_data.settings'
 ```python
    REST_FRAMEWORK = {
        # the comma is needed at the end of the tuple
        # its a string so that it can be read on parse
        'DEFAULT_PERMISSION_CLASSES' : ('rest_framework.permissions.IsAuthenticatedOrReadOnly',)
    }
 ```
-------------------------------------------------------------------------------

### POSTGRESQL INTEGRATION
- module 'cfm_data.settings'
```python

```
-------------------------------------------------------------------------------

### CRUD





-------------------------------------------------------------------------------
## NOTES:
- change back serializers from 'HyperLink' to regulars ones
- change database tables naming conventions
- 

------
# DB

pgShell
>>> CREATE DATABASE cfm_pro_db;
<!-- DELETE ON PUBLISH -->
>>> CREATE USER cfm_pro_sower_bean WITH PASSWORD 'cfm_pro_sower_bean_windows1997';
>>> CREATE USER cfm_pro_user WITH PASSWORD 'cfm_prowindows1997';
>>> ALTER ROLE cfm_pro_user SET client_encoding TO 'utf8';
>>> ALTER ROLE cfm_pro_user SET default_transaction_isolation TO 'read committed';
<!-- >>> ALTER ROLE cfm_pro_user SET timezone TO 'UTC'; -->
>>> GRANT ALL PRIVILEGES ON DATABASE <db-name> TO cfm_pro_user;
#PROBLEM : Reset migrations
>>> DELETE FROM django_migrations WHERE app = 'cfm_pro_api'

## DATA INTEGRITY
- check for empty site field in frontend froms
- these fields must be unique put together ('date', 'negociant', 'minerai', 'colis')
## BACKUP DATA
- create backup
>>> python manage.py dumpdata cfm_pro_api --format json --indent 4 > ./fixtures/backup_data.json 
- load backup
>>> python manage.py makemigrations
>>> python manage.py migrate
>>> python manage.py 
>>> python manage.py loaddata ./fixtures/backup_data.json ./fixtures/backup_data.json 
- territory data backup
>>> python manage.py dumpdata cfm_pro_api.Province --format json --indent 4 > ./fixtures/province_data.json
>>> python manage.py dumpdata cfm_pro_api.Territoire --format json --indent 4 > ./fixtures/territoire_data.json
>>> python manage.py dumpdata cfm_pro_api.Chefferie --format json --indent 4 > ./fixtures/chefferie_data.json
>>> python manage.py dumpdata cfm_pro_api.Groupement --format json --indent 4 > ./fixtures/groupement_data.json
village data failed due to special characters:
CommandError: Unable to serialize database: 'charmap' codec can't encode character '\u203f' in position 4: character maps to <undefined>
solution:
>>> python -Xutf8 manage.py dumpdata cfm_pro_api.Village --format json --indent 4 > ./fixtures/village_data.json

## PHONE NUMBERS
>>> pip install django-phonenumber-field
>>> pip install django-phonenumbers

## JWT
>>> pip install -U djoser
>>> pip install -U djangorestframework_simplejwt



## CREATE A LIST OF REQUIREMENTS
>>> pip freeze >requirements.txt



## CREATE A CUSTOM COMMANDS

- save this snippet to cmd.py
```python
from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        call_command('makemigrations')
        call_command('migrate')
        call_command('loaddata', '<file-name>.json')
```
- run cmd.py
>>> python manage.py cmd.py





##############################################################################

User field:

```python
User = serializers.HiddenField(default=serializers.CurrentUserDefault()) 
```

## PG SHELL PROBLEM
> PROBLEM:
'more' is not recognized as an internal or external command,
operable program or batch file.
> SOLUTION:
>>> \pset pager off

> PROBLEM:
'ERROR:  character with byte sequence 0xe2 0x95 0x94 in encoding "UTF8" 
has no equivalent in encoding "WIN1252"
> SOLUTION:
>>> SET client_encoding = 'UTF8';



## SHORD UUID

>>> pip install shortuuid

```python
import shortuuid

from shortuuid.django_fields import ShortUUIDField

class MyModel(models.Model):
    # A primary key ID of length 16 and a short alphabet.
    id = ShortUUIDField(
        length=16,
        max_length=40,
        prefix="id_",
        alphabet="abcdefg1234",
        primary_key=True,
    )

# CHOICES
class book(models.model):
    class GenreChoices(models.TextChoices):
        CRIME = 'C'
        FICTION = 'F'
        SCI_FI = 'S'
    name = models.CharField(max_length=120)
    genre = models.CharField(choices=GenreChoices.choices)
```

# FILTERS
>>> pip install django-filter

# DOCUMENTATION
>>> pip install drf spectacular
<!-- >>> pip install swagger-ui -->

# EMPTY DATABASE
>>> python manage.py dumpdata cfm_pro_api.Zone --format json --indent 4 > ./fixtures/zones_data.json
```sql
ALTER TABLE cooperatives DROP COLUMN address;
DROP TABLE cfm_pro_api_user CASCADE;
DROP TABLE cfm_pro_api_user_groups CASCADE;
DROP TABLE cfm_pro_api_user_user_permissions CASCADE;
DROP TABLE chantiers CASCADE;
DROP TABLE chefferies CASCADE;
DROP TABLE cooperatives CASCADE;
DROP TABLE django_admin_log CASCADE;
DROP TABLE django_content_type CASCADE;
DROP TABLE django_migrations CASCADE;
DROP TABLE django_session CASCADE;
DROP TABLE groupements CASCADE;
DROP TABLE lots CASCADE;
DROP TABLE minerais CASCADE;
DROP TABLE negociants CASCADE;
DROP TABLE profiles CASCADE;
DROP TABLE provinces CASCADE;
DROP TABLE sites CASCADE;
DROP TABLE territoires CASCADE;
DROP TABLE transporteurs CASCADE;
DROP TABLE villages CASCADE; 
DROP TABLE axes CASCADE; 
DROP TABLE zones CASCADE; 
```

# GeoDjango

- install postgresql
- install OSgeo4W form https://www.npackd.org/p/qgis64/3.24.2.1
- modify windows environment
set OSGEO4W_ROOT=C:\OSGeo4W
set GDAL_DATA=%OSGEO4W_ROOT%\share\gdal
set PROJ_LIB=%OSGEO4W_ROOT%\share\proj
set PATH=%PATH%;%OSGEO4W_ROOT%\bin
reg ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /f /d "%PATH%"
reg ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v GDAL_DATA /t REG_EXPAND_SZ /f /d "%GDAL_DATA%"
reg ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PROJ_LIB /t REG_EXPAND_SZ /f /d "%PROJ_LIB%"

# LOAD DATA

python manage.py loaddata ./fixtures/province_data_utf-8.json
python manage.py loaddata ./fixtures/territoire_data_utf-8.json
python manage.py loaddata ./fixtures/chefferie_data_utf-8.json
python manage.py loaddata ./fixtures/groupement_data_utf-8.json
python manage.py loaddata ./fixtures/village_data_utf-8.json
python manage.py loaddata ./fixtures/zone_data_utf-8.json

6249 bukavu ville
6311 kindu ville
6131 goma ville