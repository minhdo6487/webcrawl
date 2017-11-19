from django.contrib.contenttypes.models import ContentType

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.crawlingManage.tasks import task_number_one
from rest_framework.response import Response
# from rest_framework_mongoengine import viewsets
from django.http import HttpResponse

from lib.infomation_extract import extract_feed

from core.crawling.models import test_model

from api.crawlingManage.serializers import TestModelSerializer

import json
from django.core import serializers

@api_view(['GET'])
@permission_classes((AllowAny,))
def test_asynce(request):
    k = task_number_one.delay()

    url = "https://nhattao.com/"
    ef = extract_feed(url)
    data = ef.get_feed()
    # t_m = test_model.objects.create(
    #     email="minhdo6487@gmail.com",
    #     first_name="Minh",
    #     last_name="Do"
    # )
    # t_m.save()

    # ross = test_model.objects.filter(email='minhdo6487@gmail.com')
    # activity = test_model.objects.get(id=t_m.id)
    # activity_ = serializers.serialize('json', ross)
    # ross_all = test_model.objects.all()

    # ross_data = serializers.serialize('json', test_model.objects.filter(email='minhdo6487@gmail.com'))


    # return HttpResponse(ross, ross_all)
    return Response(
                        {
                            "status":"ok",
                            "data": k.task_id,
                            "data_resutl_fr_task": k.get(),
                            # 'ross': activity_,
                            # 'ross_ross': activity_
                            'rss_feed': data
                    })

# class TestModelViewSet(viewsets.ModelViewSet):
#     '''
#     Contains information about inputs/outputs of a single program
#     that may be used in Universe workflows.
#     '''
#     lookup_field = 'id'
#     serializer_class = TestModelSerializer
#     # return test_model.objects.all()
#     queryset = test_model.objects.all()
#
#     # def get_queryset(self):
#     #     return test_model.objects.all()