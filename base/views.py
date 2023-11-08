from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import Token
from rest_framework.permissions import IsAuthenticated
from base.models import Product, Category
from .serializer import ProductSerializer,CategorySerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework import status


@api_view(["get"])
def index(req):
    return Response("test")


@api_view(['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def products(req, id=-1):
    if req.method == 'GET':
        if id > -1:
            try:
                temp_product = Product.objects.get(id=id)
                return Response(ProductSerializer(temp_product, many=False).data)
            except Product.DoesNotExist:
                return Response("not found")
        all_products = ProductSerializer(Product.objects.all(), many=True).data
        return Response(all_products)
    if req.method == 'POST':
        tsk_serializer = ProductSerializer(data=req.data)
        if tsk_serializer.is_valid():
            tsk_serializer.save()
            return Response(f"post {req} adedd")
        else:
            return Response(tsk_serializer.errors)
    if req.method == 'DELETE':
        try:
            temp_product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response("not found")

        temp_product.delete()
        return Response("del...")
    if req.method == 'PUT':
        try:
            temp_product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response("not found")

        ser = ProductSerializer(data=req.data)
        old_product = Product.objects.get(id=id)
        res = ser.update(old_product, req.data)
        return Response(res)



class Category_view(APIView):
    def get(self, request):
        my_model = Category.objects.all()
        serializer = CategorySerializer(my_model, many=True)
        return Response(serializer.data)
    def post(self, request):
        # usr =request.user
        # print(usr)
        serializer = CategorySerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def put(self, request, pk):
        my_model = Category.objects.get(pk=pk)
        serializer = CategorySerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request, pk):
        my_model = Category.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





@api_view(["post"])
def register(req):
    User.objects.create_user(
        username=req.data["username"], password=req.data["password"])
    return Response({"user_created ": req.data["username"]})


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(["get"])
@permission_classes([IsAuthenticated])
def member_only (req):
    return Response ({"secret":f"you are :{req.user}"})