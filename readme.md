# Stock Rest API [DRF]:-
This api is based on the django rest framework with token authenication factor. It has all the get , put, delete and post method.


<h4>Topics -> djangorestframework, python, webdevelopment, API</h4>

### What We are going to do?

<ol>
    <li>Starting the stock_rest_api django Project</li>
    <li>Creating a companies app within the stock_rest_api Project</li>
    <li>Create a Stock in companies/models.py</li>
    <li>Writing serializers for companies model data</li>
    <li>Creating a view for handling the request made from the client</li>
    <li>Adding function handlers to routes</li>
</ol>

### Understanding Some Important Concepts  

### What is Django Framework?

Django is a Python-based free and open-source web framework that follows the model–template–views architectural pattern.

**Top Features of Django Framework**  

<ul>
    <li>Excellent Documentation</li>
    <li>SEO Optimized</li>
    <li>High Scalability</li>
    <li>Versatile in Nature</li>
    <li>Offers High Security</li>
    <li>Provides Rapid Development</li>
</ul>

### Django REST framework ?  

Django REST framework is a powerful and flexible toolkit for building Web APIs.

Some reasons you might want to use REST framework:
<ul>
    <li>The <a href="https://restframework.herokuapp.com/">Web browsable API</a> is a huge usability win for your developers.</li>
    <li><a href="api-guide/authentication/">Authentication policies</a> including packages for <a href="api-guide/authentication/#django-rest-framework-oauth">OAuth1a</a> and <a href="api-guide/authentication/#django-oauth-toolkit">OAuth2</a>.</li>
    <li><a href="api-guide/serializers/">Serialization</a> that supports both <a href="api-guide/serializers#modelserializer">ORM</a> and <a href="api-guide/serializers#serializers">non-ORM</a> data sources.</li>
    <li>Customizable all the way down - just use <a href="api-guide/views#function-based-views">regular function-based views</a> if you don't need the <a href="api-guide/generic-views/">more</a> <a href="api-guide/viewsets/">powerful</a> <a href="api-guide/routers/">features</a>.</li>
    <li>Extensive documentation, and <a href="https://groups.google.com/forum/?fromgroups#!forum/django-rest-framework">great community support</a>.</li>
    <li>Used and trusted by internationally recognised companies including <a href="https://www.mozilla.org/en-US/about/">Mozilla</a>, <a href="https://www.redhat.com/">Red Hat</a>, <a href="https://www.heroku.com/">Heroku</a>, and <a href="https://www.eventbrite.co.uk/about/">Eventbrite</a>.</li>
</ul>



## Step 1 -> Starting the Django Project  

Initialize a Django project by following command. **Python** must be installed on your system.

```
pip install Django
```


You can confirm the installation by checking the django version by following command

```
python -m django --version
```

**Starting the Project**

```
django-admin startproject stock_rest_api
```


You get the project structure like this

```
stock_rest_api/
    manage.py
    stock_rest_api/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

## Step 2 -> Creating a companies app within the stock_rest_api Project  

### What is a Django App?  

An app is a Web application that does something – e.g., a Weblog system, a database of public records or a small poll app. 

A project is a collection of configuration and apps for a particular website. A project can contain multiple apps. An app can be in multiple projects.

Creating the companies app

```
python manage.py startapp companies
```


That’ll create a directory companies, which is laid out like this:

```
companies/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

### Including your app and libraries in project  

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # framework for making rest api
    'rest_framework',

    # our main reusable components
    'companies.apps.CompaniesConfig',

    # authentication
    'rest_framework.authtoken',
]
```


## Step 3 -> Create a Stock model in companies/models.py  

### What is a Django Model?  

A model is the single, definitive source of truth about your data. It contains the essential fields and behaviors of the data you’re storing. Django follows the DRY Principle. 

The goal is to define your data model in one place and automatically derive things from it.

Let's create a Django Model.

A database contains a number of variable which are represented by fields in django model.

Each field is represented by an instance of a Field class – e.g., CharField for character fields and DateTimeField for datetimes. This tells Django what type of data each field holds.

```
from django.db import models


class Stock(models.Model):
    company_name = models.CharField(max_length=10)
    open_price = models.FloatField()
    close_price = models.FloatField()
    transaction = models.IntegerField()

    def __str__(self):
        return self.company_name
```


### Adding models to admin panel  

Django provides built-in admin panel to manage the data into model  

```
from django.contrib import admin
from .models import Stock

# Register your models here.
admin.site.register(Stock)
```


### Making migrations  

Once the model is defined, the django will automatically take schemas and table according to the fields supplied in the django model.

```
python manage.py makemigrations
python manage.py migrate
```


## Step 4 -> Writing serializers for companies model data  

### What are Serializers?  

Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types. 

Serializers also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the incoming data. 

### We are using Model Serializer. But Why?  

The <tt>ModelSerializer</tt> class provides a shortcut that lets you automatically create a <tt>Serializer</tt> class with fields that correspond to the Model fields.

### The <tt>ModelSerializer</tt> class is the same as a regular <tt>Serializer</tt> class, except that:

<ul>
    <li>It will automatically generate a set of fields for you, based on the model.</li>
    <li>It will automatically generate validators for the serializer, such as unique_together validators.</li>
    <li>It includes simple default implementations of <tt>.create()</tt> and <tt>.update()</tt>.</li>
</ul>


```
from rest_framework import serializers
from rest_framework.serializers import Serializer
from .models import Stock
from rest_framework import exceptions
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        # for some specific fields = ('companies','open_price')
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "user is inactive"
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Wrong credentials"
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password both"
            raise exceptions.ValidationError(msg)
        return data
```

Here we are using **ModelSerializer** for Stock model and **Default Serializer** for user authentication

**Default Serializer** has a built-in validate function for validating the data entered


## Step 5 -> Creating a view for handling the request made from the client.  

### What is a Django View?  

A view function, or view for short, is a Python function that takes a Web request and returns a Web response. 

### Http Methods  
<table class="table table-striped table-bordered">
    <thead>
        <tr>
            <th>HTTP Verb</th>
            <th>CRUD</th>
            <th>Entire Collection (e.g. /customers)</th>
            <th>Specific Item (e.g. /customers/{id})</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>POST</td>
            <td>Create</td>
            <td>201 (Created), 'Location' header with link to /customers/{id} containing new ID.</td>
            <td>404 (Not Found), 409 (Conflict) if resource already exists..</td>
        </tr>
        <tr>
            <td>GET</td>
            <td>Read</td>
            <td>200 (OK), list of customers. Use pagination, sorting and filtering to navigate big lists.</td>
            <td>200 (OK), single customer. 404 (Not Found), if ID not found or invalid.</td>
        </tr>
        <tr>
            <td>PUT</td>
            <td>Update/Replace</td>
            <td>405 (Method Not Allowed), unless you want to update/replace every resource in the entire collection.</td>
            <td>200 (OK) or 204 (No Content).  404 (Not Found), if ID not found or invalid.</td>
        </tr>
        <tr>
            <td>PATCH</td>
            <td>Update/Modify</td>
            <td>405 (Method Not Allowed), unless you want to modify the collection itself.</td>
            <td>200 (OK) or 204 (No Content).  404 (Not Found), if ID not found or invalid.</td>
        </tr>
        <tr>
            <td>DELETE</td>
            <td>Delete</td>
            <td>405 (Method Not Allowed), unless you want to delete the whole collection—not often desirable.</td>
            <td>200 (OK).  404 (Not Found), if ID not found or invalid.</td>
        </tr>
    </tbody>
</table>

**companies/views.py**  

```
from django.contrib.auth import login, logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Stock
from .serializers import StockSerializer, LoginSerializer

class StockApiView(APIView):
    def get(self, request):
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = StockSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StockApiViewDetail(APIView):
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, pk):
        try:
            return Stock.objects.get(pk=pk)
        except Stock.DoesNotExist as e:
            return Response({e: "given company stock not found."}, status=404)

    def get(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = StockSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        instance = self.get_object(pk)
        data = request.data
        serializer = StockSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

class LoginApiView(APIView):

    def post(self, request):
        print(request.user)
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)


class LogoutApiView(APIView):
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        logout(request)
        return Response(status=204)
```


We are using Django <tt>Response</tt> in-built function.  

Arguments:
<ul>
    <li><tt>data</tt>: The serialized data for the response.</li>
    <li><tt>status</tt>: A status code for the response.  Defaults to 200.  See also <a href="../status-codes/">status codes</a>.</li>
    <li><tt>template_name</tt>: A template name to use if <tt>HTMLRenderer</tt> is selected.</li>
    <li><tt>headers</tt>: A dictionary of HTTP headers to use in the response.</li>
    <li><tt>content_type</tt>: The content type of the response.  Typically, this will be set automatically by the renderer as determined by content negotiation, but there may be some cases where you need to specify the content type explicitly.</li>
</ul>



## Step 6 -> Adding function handlers to routes.(companies/urls.py)  

Whenever user visit the user, a function is called in view which takes care of response.

**stock_rest_api/urls.py**  

```
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from companies import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^companies/', include('companies.urls')),
]

```


**Adding sub path for companies app(companies/urls.py)**  

It defines the particular path for companies app 

```
from django.urls import path

from . import views

app_name = 'companies'
urlpatterns = [
    # IT IS FOR JSON RESPONSE SERIALIZER
    # path('', views.stock, name='list'),
    # path('', views.StockApiView.as_view(), name='list'),
    path('', views.GenericStockView.as_view(), name='list'),
    path('<int:pk>/', views.StockApiViewDetail.as_view(), name='detail'),
    # path('<int:pk>/', views.stock_details, name='detail'),
    path('login/', views.LoginApiView.as_view(), name="login"),
    path('logout/', views.LogoutApiView.as_view(), name="logout")
]
```

### Add Some styles to make it attractive


## Deployment
You can easily deploy on <a href="https://www.heroku.com/">Heroku</a>
You can read more about on <a href="https://www.analyticsvidhya.com/blog/2020/10/step-by-step-guide-for-deploying-a-django-application-using-heroku-for-free/">Analytics Vidhya Blog</a>


### **How to get the token:-** 

To get the access token you need to send a post request with the username and password at the url http://127.0.0.1:8000/companies/login if it is hosted locally.


## Web Preview / Output
<img src="rest.png" alt="django rest framework">

Placeholder text by
<a href="https://chaudharypraveen98.github.io/">Praveen Chaudhary</a> &middot; Images by<a href="hhttps://chaudharypraveen98.github.io/binarybeast/">Binary Beast</a>
