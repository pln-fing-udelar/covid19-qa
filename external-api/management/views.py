from rest_framework.response import Response
from rest_framework.views import APIView

from .models import QueryConf
from .serializers import ESQueryConfSerializer


class ESQueryConfAPIView(APIView):

    def get(self, request):
        es_query_conf = QueryConf.objects.filter(parameter_name='ES_QUERY_CONF').first()
        if not es_query_conf:
            return Response([])
        print(es_query_conf.conf)
        serializer = ESQueryConfSerializer(data=es_query_conf.conf, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

    def post(self, request):
        es_query_conf = QueryConf.objects.filter(parameter_name='ES_QUERY_CONF').first()
        if not es_query_conf:
            es_query_conf = QueryConf.objects.create(parameter_name='ES_QUERY_CONF')
        serializer = ESQueryConfSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        es_query_conf.conf = serializer.validated_data
        es_query_conf.save()
        return Response(serializer.validated_data)
