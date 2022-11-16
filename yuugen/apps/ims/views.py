from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


#from .serializers import ProductSerializer, CatalogueSerializer





# class CatalogueViewDetail(APIView):
# 	def get_object(self, slug_catalogue, slug_product):
# 		try:
# 			return Catalogue.objects.filter(slug_catalogue=catalogue_slug).get(slug_product=product_slug)
# 		except Catalogue.DoesNotExist:
# 			raise Http404

# 	def get(self, request, format=None):
# 		products = self.get_object(
# 			[Product.objects.filter(product__product__product_tag == product__catalogue__catalogue_name)])
# 		serializer = ProductSerilizer(products, many=True)
# 		return Response(serialize.data)


# class ProductViewDetail(APIView):
# 	def get_object(self, request, slug_product, format=None):
# 		try:
# 			return Product.objects.get(slug_product=product_slug)
# 		except DoesNotExist:
# 			raise Http404

# 	def get(self, request, format=None):
# 		products = self.get_object(product_slug)
# 		serializer = ProductSerializer(products, many=True)
# 		return Response(serializer.data)
