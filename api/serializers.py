from rest_framework import serializers

from products.models import product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = product
        # only added import fields to display
        fields = ('id', 'name', 'price')
