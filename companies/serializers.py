from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework import serializers

from .models import Stock

"""
1. Nested serializers are used when we want the reverse the relationship between the objcets otherwise we can the 
depth method too. It will help to gain the linked the objects by one level or more.
2. When you are using the nested serializer always remember to name the variable as same as the related name in the models.py 
3. Limitation of the depth is that we can't control over the linked object like filtering and other stuffs.
4. Use the read only field when you want the field attribute of other model like this date = serializers.ReadOnlyField(source='bill_no.bill_date') 
5. HyperlinkedRelatedfield is used when we want the list 
6. hyperlinkedidentityfield  we want the detail
6. HyperlinkedModelSerializer is similiar to ModelSerializer but it lacks the id and have a extra url field to create a link
7. we can have the ModelSerializer with the url field by including the HyperlinkedRelatedField and HyperlinkedIdentityField
8. The extra_kwargs works only with HyperlinkedModelSerializer. By default the HyperlinkedRelatedfield assumes the
    view name to be <model_name>-detail and hyperlinkedidentityfield to be <model_name>-detail for standard routers
    tracks = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Object.something,
        read_only=True,
        view_name='track-detail'
    )
    HyperlinkedRelatedField will link all the relationship items
"""


# always use the in built ordering in model serializers
class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        # ordering = ['-date']
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
