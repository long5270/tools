from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend

from b2c.activities.sales.models.sales_activity_schedule import SalesActivitySchedule
from b2c.activities.sales.serializers.sales_activity_schedule import SalesActivityScheduleCreateSerializer, \
    SalesActivityScheduleListSerializer, SalesActivityScheduleDetailSerializer
from b2c.activities.sales.services import delete_sales_activity_schedule
from b2c.general.mixins import SalesExport, ExportModelMixin


class SalesActivityScheduleViewSet(mixins.ListModelMixin,
                                   mixins.CreateModelMixin,
                                   mixins.RetrieveModelMixin,
                                   ExportModelMixin,
                                   GenericViewSet):
    """
    秒杀预设周期

    create:
    秒杀周期创建 mb-create-sales-schedule

    retrieve:
    秒杀周期详情 mb-sales-schedule-detail
    """
    queryset = SalesActivitySchedule.objects.all()
    serializer_class = SalesActivityScheduleListSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = []
    export_class = SalesExport
    ordering = ('-id',)

    def get_queryset(self):
        queryset = super(SalesActivityScheduleViewSet, self).get_queryset()
        return queryset.filter(merchant=self.request.merchant_id)

    def get_serializer_class(self):
        if self.action == "create":
            return SalesActivityScheduleCreateSerializer
        if self.action == "retrieve":
            return SalesActivityScheduleDetailSerializer
        if self.action == "list" or self.action == "export":
            return self.serializer_class
        return serializers.Serializer

    def list(self, request, *args, **kwargs):
        """
        秒杀预设周期列表 code mb-sales-schedules
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        status = request.query_params.get("status")
        product_name = request.query_params.get("product_name")
        if status in ("1", "2", "3"):
            if status == "1":
                self.queryset = SalesActivitySchedule.objects.get_not_started()
            elif status == "2":
                self.queryset = SalesActivitySchedule.objects.get_started()
            elif status == "3":
                self.queryset = SalesActivitySchedule.objects.get_ended()
        if product_name:
            self.queryset = self.queryset.filter(sale_schedule_item__activity__title__contains=product_name)

        return super(SalesActivityScheduleViewSet, self).list(request, *args, **kwargs)

    @action(methods=["patch"], detail=True)
    def stop(self, request, *args, **kwargs):
        """
        秒杀预设周期结束 仅删除未开始的 code mb-stop-sales-schedule
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        delete_sales_activity_schedule(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
