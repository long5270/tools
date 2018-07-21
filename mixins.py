from rest_framework.decorators import action
from django.shortcuts import HttpResponse
import xlwt
from io import BytesIO
from urllib import parse

class ExportModelMixin(object):

    @action(methods=["get"], detail=False)
    def export(self, request, *args, **kwargs):
        self.response = HttpResponse(content_type='application/vnd.ms-excel')
        excel_name = self.get_excel_name()
        print(excel_name)
        self.response['Content-Disposition'] = 'attachment;filename=' + parse.quote(excel_name, encoding="utf8") + '.xls'
        self.wb = xlwt.Workbook(encoding='utf-8')
        self.render_content()
        return self.response

    def get_excel_name(self):
        if self.export_class.excel_name:
            return self.export_class.excel_name
        return "Xxxxx"

    def render_content(self):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        header = self.export_class.header
        labels = self.export_class.labels if self.export_class.labels else {}
        data = [[labels.get(column, column) for column in header]]
        for item in serializer.data:
            data.append([item.get(column) for column in  header])
        sheet_prd = self.wb.add_sheet('sheet1')
        for row_index, row in enumerate(data):
            print(row)
            for column_index, column in enumerate(row):
                sheet_prd.write(row_index, column_index, column)
        output = BytesIO()
        self.wb.save(output)
        output.seek(0)
        self.response.write(output.getvalue())


class SalesExport:
    header = ["id","name", "period", "valid_order_count", "status", "started_at", "ended_at"]
    excel_name = "秒杀周期"

    labels = {
        'name': '名字',
        'period': '周期'
    }