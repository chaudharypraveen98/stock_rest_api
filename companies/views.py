"""
ApiView is the base class for the api view . GenericAPIview extends the ApiView.
The GenericAPIview contains the mixins and verbose which makes the works easier.

Viewset have actions while ApiViews have the method attributes like get,put ,post etc
"""
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Stock
from .serializers import StockSerializer, LoginSerializer


@csrf_exempt
def stock_details(request, pk):
    try:
        instance = Stock.objects.get(pk=pk)
    except Stock.DoesNotExist as e:
        return JsonResponse({e: "given company stock not found."}, status=404)
    if request.method == 'GET':
        serializer = StockSerializer(instance)
        # we have set the suse in safe mode the serializer is unable to parse the dictionary
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        # first we need to parse the data which come from the user to json so we need a json parse
        stocks = JSONParser().parse(request)
        # if we provide another parameter to serializer then it means we are serializing the existing object
        serializer = StockSerializer(instance, data=stocks)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        instance.delete()
        # it is used for no content found
        return HttpResponse(status=204)


@csrf_exempt
def stock(request):
    if request.method == 'GET':
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        # we have set the safe = false because in safe mode the serializer is unable to parse the dictionary
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        # first we need to parse the data which come from the user to json so we need a json parser
        # always remember to send json post request from postman or curl
        stocks = JSONParser().parse(request)
        serializer = StockSerializer(data=stocks)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# It is a standalone generic views

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
    # authentication_classes = [BasicAuthentication]
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
        # For put for patch we first provide the instance of the class as the first parameter then the data
        # we want the the patch we provide the next argument partial is true
        # like serializer = StockSerializer(instance, data={"created_by":user.id},)
        serializer = StockSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class StockView(ListView):
    model = Stock
    template_name = 'companies/companies_list.html'


class GenericStockView(generics.GenericAPIView,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    # default lookup field is pk
    # we can set it by lookup_field = 'id'

    def get(self, request):
        return self.list(request)

    # def perform_create(self, serializer):
    #     serializer.save()

    def post(self, request):
        return self.create(request)

    def put(self, request, pk=None):
        return self.update(request, pk)

    def delete(self, request, pk=None):
        return self.delete(request, pk)


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
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        logout(request)
        return Response(status=204)


class StockViewSet(viewsets.ModelViewSet):
    permission_classes = []
    authentication_classes = []
    """
        This viewset automatically provides 'list' and 'detail' actions.
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    # actions are used to link related fields
    # @action(detail=True, methods=['Get'])
    # def choice(self):
    #     pass
    def post(self, request):
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class StockDetailView(DetailView):
    model = Stock
    template_name = 'companies/stock_detail.html'
