import django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.views.generic import TemplateView

from .models import Builds, Regions, VR1, VR25, VR24, VR23, VR22, VR21, VR20, VR19, VR18, VR17, VR16, \
    VR15, VR14, VR13, VR12, VR11, VR10, VR9, VR8, VR7, VR6, VR5, VR4, VR3, VR2, R1
import sqlite3

import pandas

from myapp import DatabaseController
from myapp.excel import Excel
import os
from pathlib import Path
from django.shortcuts import render, redirect

from myapp.models import BuildDocs
from django.db.models import Q, QuerySet, Sum
from . import forms


@login_required
def upload(request, doc_id, path):
    excel = Excel()
    wb = excel.load(os.path.join(Path(__file__).resolve().parent.parent, path))
    df_list = excel.read_df(wb)
    data = {}
    try:
        doc = BuildDocs.objects.get(pk=doc_id)
        for i in range(len(df_list)):
            table = wb.get_sheet_names()[i]
            data[i] = {
                'title': table,
                'df': df_list[i]
            }
            query_str = DatabaseController.df_to_query_str(df_list[i], doc.id, 1)
            DatabaseController.sql_clean(table, doc.id)
            DatabaseController.sql_insert(table, query_str)
    except Exception as e:
        print("Error during insert: ", e)
        DatabaseController.rollback()
    DatabaseController.commit()


@login_required
def postuser(request):
    doc_id = request.POST.get("doc_id")
    doc_id = int(doc_id)
    path = request.POST.get("path")
    upload(request, doc_id, path)
    return redirect('lk')


@login_required
def data_doc_search(request, path):
    excel = Excel()
    wb = excel.load(os.path.join(Path(__file__).resolve().parent.parent, path))
    df_list = excel.read_df1(wb)
    data = {}
    for i in range(len(df_list)):
        table = wb.get_sheet_names()[i]
        data[i] = {
            'title': table,
            'df': df_list[i]
        }
    return data


def text_diagram():
    data = [
        [1, 'Соотношение организаций, погдавших данные по форме N 85-К'],
        [2, 'Тип поселения, в которм расположены организации'],
        [3, 'Режим работы групп и численность воспитанников в них'],
        [4, 'Распределение персонала по уровню образования и полу'],
        [5, 'Сведения о помещениях организации'],
        [6, 'Оснащение дошкольной организации'],
        [7, 'Техническое оснащение для детей-инвалидов и детей с ОВЗ'],
        [8, 'Расходы организации'],
        [9, 'Источники финансирования внутренних затрат дошкольной образовательной организацией на внедрение и использование цифровых технологий']
    ]
    return data


def smart_card(id):
    if id == -1:
        count_build = Builds.objects.count()
        count_workers = Builds.objects.aggregate(Sum("workers"))
        count_students = Builds.objects.aggregate(Sum("students"))
        val1 = VR22.objects.select_related('r22').filter(r22_id=1).aggregate(Sum("value1"))
        val2 = VR25.objects.select_related('r25').filter(r25_id=1).aggregate(Sum("value1"))

        if val1['value1__sum'] is None:
            val1 = 0
        else:
            val1 = val1['value1__sum']
        if val2['value1__sum'] is None:
            val2 = 0
        else:
            val2 = val2['value1__sum']

    elif id == 0:
        count_build = Builds.objects.filter(
            Q(id_reg=8) | Q(id_reg=9) | Q(id_reg=10) | Q(id_reg=11) | Q(id_reg=12) | Q(id_reg=13)
        ).count()

        count_workers = Builds.objects.filter(
            Q(id_reg=8) | Q(id_reg=9) | Q(id_reg=10) | Q(id_reg=11) | Q(id_reg=12) | Q(id_reg=13)
        ).aggregate(Sum("workers"))

        count_students = Builds.objects.filter(
            Q(id_reg=8) | Q(id_reg=9) | Q(id_reg=10) | Q(id_reg=11) | Q(id_reg=12) | Q(id_reg=13)
        ).aggregate(Sum("students"))

        val1 = 0
        val2 = 0

        for i in range(8, 14):
            val1n = VR22.objects.select_related('r22').filter(r22_id=1, doc__build__id_reg=i).aggregate(Sum("value1"))
            val2n = VR25.objects.select_related('r25').filter(r25_id=1, doc__build__id_reg=i).aggregate(Sum("value1"))

            if val1n['value1__sum'] is None:
                val1 += 0
            else:
                val1 += val1n['value1__sum']
            if val2n['value1__sum'] is None:
                val2 += 0
            else:
                val2 += val2n['value1__sum']

    else:
        count_build = Builds.objects.filter(id_reg=id).count()
        count_workers = Builds.objects.filter(id_reg=id).aggregate(Sum("workers"))
        count_students = Builds.objects.filter(id_reg=id).aggregate(Sum("students"))
        val1 = VR22.objects.select_related('r22').filter(r22_id=1, doc__build__id_reg=id).aggregate(Sum("value1"))
        val2 = VR25.objects.select_related('r25').filter(r25_id=1, doc__build__id_reg=id).aggregate(Sum("value1"))

        if val1['value1__sum'] is None:
            val1 = 0
        else:
            val1 = val1['value1__sum']
        if val2['value1__sum'] is None:
            val2 = 0
        else:
            val2 = val2['value1__sum']

    if count_workers['workers__sum'] is None:
        count_workers = 0
    else:
        count_workers = count_workers['workers__sum']
    if count_students['students__sum'] is None:
        count_students = 0
    else:
        count_students = count_students['students__sum']

    card_data = [
        count_build,
        count_students,
        count_workers,
        val1,
        val2
    ]

    return card_data


def smart_diagram_name(id_dia):
    if id_dia == 2:
        name = [
            "Городская местность",
            "Сельская местность"
        ]
    elif id_dia == 3:
        name = [
            "Численность воспитанников кратковременного пребывания (5 часов и менее)",
            "Численность воспитанников сокращенного дня (8 - 10 часов)",
            "Численность воспитанников полного дня (10,5 - 12 часов)",
            "Численность воспитанников продленного дня (13 - 14 часов)",
            "Численность воспитанников"
        ]
    elif id_dia == 4:
        name = [
            "Из всех работников имеют высшее образование",
            "Высшее педагогическое образование",
            "Сред. проф. образование по программам подготовки специалистов среднего звена",
            "Сред. проф. педагогическое образование по программам подготовки специалистов среднего звена",
            "Из всех работников всего женщин"
        ]
    elif id_dia == 5:
        name = [
            "Кабинет заведующего",
            "Групповые комнаты",
            "Спальни",
            "Соляная комната/пещера",
            "Комнаты для специалистов",
            "Медицинский кабинет",
            "Изолятор",
            "Процедурный кабинет",
            "Методический кабинет",
            "Физкультурный/спортивный зал",
            "Музыкальный зал",
            "Плавательный бассейн",
            "Зимний сад/экологическая комната",
            "Подсобное помещение",
            "Лаборатория",
            "Места для личной гигиены",
            "Раздевальная",
            "Помещения для приготовления и раздачи пищи",
            "Кинозал",
            "Книгохранилище\библиотека",
            "Фитобар"
        ]
    elif id_dia == 6:
        name = [
            "интерактивной доски, ин. стола, демонстр. экрана с мультимед. проектором",
            "цифрового/интерактивного пола",
            "бизибордов",
            "стола для рисования в технике Эбру",
            "сухого бассейна",
            "светового стола для рисования песком",
            "печатных книг/журналов для чтения воспитанниками",
            "электронные средства обучения",
            "магнитных досок",
            "скалодрома",
            "батута"
        ]
    elif id_dia == 7:
        name = [
            "пандуса",
            "подъемника для детей",
            "лифта для детей",
            "инвалидных колясок",
            "книг для слабовидящих",
            "электронных обучающих материалов (игр и презентаций)",
            "стационарного спортивного оборудования (тренажеров)",
            "звуковые средства воспроизведения информации"
        ]
    elif id_dia == 8:
        name = [
            "Расходы - оплата труда и начисления на выплаты по оплате труда",
            "Расходы - оплата работ, услуг",
            "Расходы - социальное обеспечение",
            "Расходы - прочие расходы",
            "Поступление нефинансовых активов"
        ]
    elif id_dia == 9:
        name = [
            "Внут. затраты на внедр. и испол. цифр. тех. - собственные средства орг.",
            "Внут. затраты на внедр. и испол. цифр. тех. - средства бюджет. всех уровней",
            "Внут. затраты на внедр. и испол. цифр. тех. - прочие привлеч. средства",
            "Прочие привлеч. средства: некоммерч. орг.",
            "Прочие привлеч. средства: физических лиц"
        ]
    else:
        name = ["Подали данные по форме N 85-К", 'Не подали данные']
    return name


def smart_diagram_value(id, id_dia):
    if id == -1:
        if id_dia == 2:
            value1 = VR1.objects.select_related('r1').filter(r1="2", value=1).count()
            value2 = VR1.objects.select_related('r1').filter(r1="2", value=2).count()
            value = [value1, value2]
        elif id_dia == 3:
            value1 = VR2.objects.select_related('r2').filter(r2_id=1).aggregate(Sum("value"))
            value2 = VR2.objects.select_related('r2').filter(r2_id=2).aggregate(Sum("value"))
            value3 = VR2.objects.select_related('r2').filter(r2_id=3).aggregate(Sum("value"))
            value4 = VR2.objects.select_related('r2').filter(r2_id=4).aggregate(Sum("value"))
            value5 = VR2.objects.select_related('r2').filter(r2_id=5).aggregate(Sum("value"))
            value = [
                value1['value__sum'], value2['value__sum'], value3['value__sum'],
                value4['value__sum'], value5['value__sum']
            ]
        elif id_dia == 4:
            value2 = VR9.objects.select_related('r9').filter(r9_id=1).aggregate(Sum("value2"))
            value3 = VR9.objects.select_related('r9').filter(r9_id=1).aggregate(Sum("value3"))
            value4 = VR9.objects.select_related('r9').filter(r9_id=1).aggregate(Sum("value4"))
            value5 = VR9.objects.select_related('r9').filter(r9_id=1).aggregate(Sum("value5"))
            value6 = VR9.objects.select_related('r9').filter(r9_id=1).aggregate(Sum("value6"))
            value = [
                value2['value2__sum'], value3['value3__sum'],
                value4['value4__sum'], value5['value5__sum'], value6['value6__sum']
            ]
        elif id_dia == 5:
            value1 = VR16.objects.select_related('r16').filter(r16_id=1, value1=1).count()
            value2 = VR16.objects.select_related('r16').filter(r16_id=2, value1=1).count()
            value3 = VR16.objects.select_related('r16').filter(r16_id=3, value1=1).count()
            value4 = VR16.objects.select_related('r16').filter(r16_id=4, value1=1).count()
            value5 = VR16.objects.select_related('r16').filter(r16_id=5, value1=1).count()
            value6 = VR16.objects.select_related('r16').filter(r16_id=6, value1=1).count()
            value7 = VR16.objects.select_related('r16').filter(r16_id=7, value1=1).count()
            value8 = VR16.objects.select_related('r16').filter(r16_id=8, value1=1).count()
            value9 = VR16.objects.select_related('r16').filter(r16_id=9, value1=1).count()
            value10 = VR16.objects.select_related('r16').filter(r16_id=10, value1=1).count()
            value11 = VR16.objects.select_related('r16').filter(r16_id=11, value1=1).count()
            value12 = VR16.objects.select_related('r16').filter(r16_id=12, value1=1).count()
            value13 = VR16.objects.select_related('r16').filter(r16_id=13, value1=1).count()
            value14 = VR16.objects.select_related('r16').filter(r16_id=14, value1=1).count()
            value15 = VR16.objects.select_related('r16').filter(r16_id=15, value1=1).count()
            value16 = VR16.objects.select_related('r16').filter(r16_id=16, value1=1).count()
            value17 = VR16.objects.select_related('r16').filter(r16_id=17, value1=1).count()
            value18 = VR16.objects.select_related('r16').filter(r16_id=18, value1=1).count()
            value19 = VR16.objects.select_related('r16').filter(r16_id=19, value1=1).count()
            value20 = VR16.objects.select_related('r16').filter(r16_id=20, value1=1).count()
            value21 = VR16.objects.select_related('r16').filter(r16_id=21, value1=1).count()
            value = [
                value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, value11, value12,
                value13, value14, value15, value16, value17, value18, value19, value20, value21
            ]
        elif id_dia == 6:
            value1 = VR18.objects.select_related('r18').filter(r18_id=1, value1=1).count()
            value2 = VR18.objects.select_related('r18').filter(r18_id=2, value1=1).count()
            value3 = VR18.objects.select_related('r18').filter(r18_id=3, value1=1).count()
            value4 = VR18.objects.select_related('r18').filter(r18_id=4, value1=1).count()
            value5 = VR18.objects.select_related('r18').filter(r18_id=5, value1=1).count()
            value6 = VR18.objects.select_related('r18').filter(r18_id=6, value1=1).count()
            value7 = VR18.objects.select_related('r18').filter(r18_id=7, value1=1).count()
            value8 = VR18.objects.select_related('r18').filter(r18_id=8, value1=1).count()
            value9 = VR18.objects.select_related('r18').filter(r18_id=9, value1=1).count()
            value10 = VR18.objects.select_related('r18').filter(r18_id=10, value1=1).count()
            value11 = VR18.objects.select_related('r18').filter(r18_id=11, value1=1).count()
            value = [value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, value11]
        elif id_dia == 7:
            value1 = VR19.objects.select_related('r19').filter(r19_id=1, value1=1).count()
            value2 = VR19.objects.select_related('r19').filter(r19_id=2, value1=1).count()
            value3 = VR19.objects.select_related('r19').filter(r19_id=3, value1=1).count()
            value4 = VR19.objects.select_related('r19').filter(r19_id=4, value1=1).count()
            value5 = VR19.objects.select_related('r19').filter(r19_id=5, value1=1).count()
            value6 = VR19.objects.select_related('r19').filter(r19_id=6, value1=1).count()
            value7 = VR19.objects.select_related('r19').filter(r19_id=7, value1=1).count()
            value8 = VR19.objects.select_related('r19').filter(r19_id=8, value1=1).count()
            value = [
                value1, value2, value3, value4, value5, value6, value7, value8]
        elif id_dia == 8:
            value2 = VR22.objects.select_related('r22').filter(r22_id=2).aggregate(Sum("value1"))
            value3 = VR22.objects.select_related('r22').filter(r22_id=3).aggregate(Sum("value1"))
            value4 = VR22.objects.select_related('r22').filter(r22_id=4).aggregate(Sum("value1"))
            value5 = VR22.objects.select_related('r22').filter(r22_id=5).aggregate(Sum("value1"))
            value6 = VR22.objects.select_related('r22').filter(r22_id=6).aggregate(Sum("value1"))
            value = [
                value2['value1__sum'], value3['value1__sum'],
                value4['value1__sum'], value5['value1__sum'], value6['value1__sum']
            ]
        elif id_dia == 9:
            value2 = VR25.objects.select_related('r25').filter(r25_id=2).aggregate(Sum("value1"))
            value3 = VR25.objects.select_related('r25').filter(r25_id=3).aggregate(Sum("value1"))
            value4 = VR25.objects.select_related('r25').filter(r25_id=4).aggregate(Sum("value1"))
            value5 = VR25.objects.select_related('r25').filter(r25_id=5).aggregate(Sum("value1"))
            value6 = VR25.objects.select_related('r25').filter(r25_id=6).aggregate(Sum("value1"))
            value = [
                value2['value1__sum'], value3['value1__sum'],
                value4['value1__sum'], value5['value1__sum'], value6['value1__sum']
            ]
        else:
            value2 = Builds.objects.filter(link='docs/default/template.xlsx').count()
            b = Builds.objects.count()
            value1 = b - value2
            value = [value1, value2]
    elif id == 0:
        if id_dia == 2:
            value1 = 0
            value2 = 0
            for n in range(8, 14):
                value1 += VR1.objects.select_related('r1').filter(r1="2", value=1, doc__build__id_reg=n).count()
                value2 += VR1.objects.select_related('r1').filter(r1="2", value=2, doc__build__id_reg=n).count()
            value = [value1, value2]
        elif id_dia == 3:
            value1 = 0
            value2 = 0
            value3 = 0
            value4 = 0
            value5 = 0
            for n in range(8, 14):
                value1n = VR2.objects.select_related('r2').filter(r2_id=1, doc__build__id_reg=n).aggregate(Sum("value"))
                value2n = VR2.objects.select_related('r2').filter(r2_id=2, doc__build__id_reg=n).aggregate(Sum("value"))
                value3n = VR2.objects.select_related('r2').filter(r2_id=3, doc__build__id_reg=n).aggregate(Sum("value"))
                value4n = VR2.objects.select_related('r2').filter(r2_id=4, doc__build__id_reg=n).aggregate(Sum("value"))
                value5n = VR2.objects.select_related('r2').filter(r2_id=5, doc__build__id_reg=n).aggregate(Sum("value"))
                if value1n['value__sum'] is None:
                    value1 += 0
                else:
                    value1 += value1n['value__sum']
                if value2n['value__sum'] is None:
                    value2 += 0
                else:
                    value2 += value2n['value__sum']

                if value3n['value__sum'] is None:
                    value3 += 0
                else:
                    value3 += value3n['value__sum']
                if value4n['value__sum'] is None:
                    value4 += 0
                else:
                    value4 += value4n['value__sum']
                if value5n['value__sum'] is None:
                    value5 += 0
                else:
                    value5 += value5n['value__sum']
            value = [value1, value2, value3, value4, value5]
        elif id_dia == 4:
            value2 = 0
            value3 = 0
            value4 = 0
            value5 = 0
            value6 = 0
            for n in range(8, 14):
                value2n = VR9.objects.select_related('r9').filter(r9_id=1, doc__build__id_reg=n).aggregate(
                    Sum("value2"))
                value3n = VR9.objects.select_related('r9').filter(r9_id=1, doc__build__id_reg=n).aggregate(
                    Sum("value3"))
                value4n = VR9.objects.select_related('r9').filter(r9_id=1, doc__build__id_reg=n).aggregate(
                    Sum("value4"))
                value5n = VR9.objects.select_related('r9').filter(r9_id=1, doc__build__id_reg=n).aggregate(
                    Sum("value5"))
                value6n = VR9.objects.select_related('r9').filter(r9_id=1, doc__build__id_reg=n).aggregate(
                    Sum("value6"))
                if value2n['value2__sum'] is None:
                    value2 += 0
                else:
                    value2 += value2n['value2__sum']
                if value3n['value3__sum'] is None:
                    value3 += 0
                else:
                    value3 += value3n['value3__sum']
                if value4n['value4__sum'] is None:
                    value4 += 0
                else:
                    value4 += value4n['value4__sum']
                if value5n['value5__sum'] is None:
                    value5 += 0
                else:
                    value5 += value5n['value5__sum']
                if value6n['value6__sum'] is None:
                    value6 += 0
                else:
                    value6 += value6n['value6__sum']
            value = [value2, value3, value4, value5, value6]
        elif id_dia == 5:
            value1 = 0
            value2 = 0
            value3 = 0
            value4 = 0
            value5 = 0
            value6 = 0
            value7 = 0
            value8 = 0
            value9 = 0
            value10 = 0
            value11 = 0
            value12 = 0
            value13 = 0
            value14 = 0
            value15 = 0
            value16 = 0
            value17 = 0
            value18 = 0
            value19 = 0
            value20 = 0
            value21 = 0
            for n in range(8, 14):
                value1 += VR16.objects.select_related('r16').filter(r16_id=1, value1=1, doc__build__id_reg=n).count()
                value2 += VR16.objects.select_related('r16').filter(r16_id=2, value1=1, doc__build__id_reg=n).count()
                value3 += VR16.objects.select_related('r16').filter(r16_id=3, value1=1, doc__build__id_reg=n).count()
                value4 += VR16.objects.select_related('r16').filter(r16_id=4, value1=1, doc__build__id_reg=n).count()
                value5 += VR16.objects.select_related('r16').filter(r16_id=5, value1=1, doc__build__id_reg=n).count()
                value6 += VR16.objects.select_related('r16').filter(r16_id=6, value1=1, doc__build__id_reg=n).count()
                value7 += VR16.objects.select_related('r16').filter(r16_id=7, value1=1, doc__build__id_reg=n).count()
                value8 += VR16.objects.select_related('r16').filter(r16_id=8, value1=1, doc__build__id_reg=n).count()
                value9 += VR16.objects.select_related('r16').filter(r16_id=9, value1=1, doc__build__id_reg=n).count()
                value10 += VR16.objects.select_related('r16').filter(r16_id=10, value1=1, doc__build__id_reg=n).count()
                value11 += VR16.objects.select_related('r16').filter(r16_id=11, value1=1, doc__build__id_reg=n).count()
                value12 += VR16.objects.select_related('r16').filter(r16_id=12, value1=1, doc__build__id_reg=n).count()
                value13 += VR16.objects.select_related('r16').filter(r16_id=13, value1=1, doc__build__id_reg=n).count()
                value14 += VR16.objects.select_related('r16').filter(r16_id=14, value1=1, doc__build__id_reg=n).count()
                value15 += VR16.objects.select_related('r16').filter(r16_id=15, value1=1, doc__build__id_reg=n).count()
                value16 += VR16.objects.select_related('r16').filter(r16_id=16, value1=1, doc__build__id_reg=n).count()
                value17 += VR16.objects.select_related('r16').filter(r16_id=17, value1=1, doc__build__id_reg=n).count()
                value18 += VR16.objects.select_related('r16').filter(r16_id=18, value1=1, doc__build__id_reg=n).count()
                value19 += VR16.objects.select_related('r16').filter(r16_id=19, value1=1, doc__build__id_reg=n).count()
                value20 += VR16.objects.select_related('r16').filter(r16_id=20, value1=1, doc__build__id_reg=n).count()
                value21 += VR16.objects.select_related('r16').filter(r16_id=21, value1=1, doc__build__id_reg=n).count()
            value = [
                value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, value11, value12,
                value13,
                value14, value15, value16, value17, value18, value19, value20, value21
            ]
        elif id_dia == 6:
            value1 = 0
            value2 = 0
            value3 = 0
            value4 = 0
            value5 = 0
            value6 = 0
            value7 = 0
            value8 = 0
            value9 = 0
            value10 = 0
            value11 = 0
            for n in range(8, 14):
                value1 += VR18.objects.select_related('r18').filter(r18_id=1, value1=1, doc__build__id_reg=n).count()
                value2 += VR18.objects.select_related('r18').filter(r18_id=2, value1=1, doc__build__id_reg=n).count()
                value3 += VR18.objects.select_related('r18').filter(r18_id=3, value1=1, doc__build__id_reg=n).count()
                value4 += VR18.objects.select_related('r18').filter(r18_id=4, value1=1, doc__build__id_reg=n).count()
                value5 += VR18.objects.select_related('r18').filter(r18_id=5, value1=1, doc__build__id_reg=n).count()
                value6 += VR18.objects.select_related('r18').filter(r18_id=6, value1=1, doc__build__id_reg=n).count()
                value7 += VR18.objects.select_related('r18').filter(r18_id=7, value1=1, doc__build__id_reg=n).count()
                value8 += VR18.objects.select_related('r18').filter(r18_id=8, value1=1, doc__build__id_reg=n).count()
                value9 += VR18.objects.select_related('r18').filter(r18_id=9, value1=1, doc__build__id_reg=n).count()
                value10 += VR18.objects.select_related('r18').filter(r18_id=10, value1=1, doc__build__id_reg=n).count()
                value11 += VR18.objects.select_related('r18').filter(r18_id=11, value1=1, doc__build__id_reg=n).count()
            value = [value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, value11]
        elif id_dia == 7:
            value1 = 0
            value2 = 0
            value3 = 0
            value4 = 0
            value5 = 0
            value6 = 0
            value7 = 0
            value8 = 0
            for n in range(8, 14):
                value1 += VR19.objects.select_related('r19').filter(r19_id=1, value1=1, doc__build__id_reg=n).count()
                value2 += VR19.objects.select_related('r19').filter(r19_id=2, value1=1, doc__build__id_reg=n).count()
                value3 += VR19.objects.select_related('r19').filter(r19_id=3, value1=1, doc__build__id_reg=n).count()
                value4 += VR19.objects.select_related('r19').filter(r19_id=4, value1=1, doc__build__id_reg=n).count()
                value5 += VR19.objects.select_related('r19').filter(r19_id=5, value1=1, doc__build__id_reg=n).count()
                value6 += VR19.objects.select_related('r19').filter(r19_id=6, value1=1, doc__build__id_reg=n).count()
                value7 += VR19.objects.select_related('r19').filter(r19_id=7, value1=1, doc__build__id_reg=n).count()
                value8 += VR19.objects.select_related('r19').filter(r19_id=8, value1=1, doc__build__id_reg=n).count()
            value = [value1, value2, value3, value4, value5, value6, value7, value8]
        elif id_dia == 8:
            value2 = 0
            value3 = 0
            value4 = 0
            value5 = 0
            value6 = 0
            for n in range(8, 14):
                value2n = VR22.objects.select_related('r22').filter(r22_id=2, doc__build__id_reg=n).aggregate(Sum("value1"))
                value3n = VR22.objects.select_related('r22').filter(r22_id=3, doc__build__id_reg=n).aggregate(Sum("value1"))
                value4n = VR22.objects.select_related('r22').filter(r22_id=4, doc__build__id_reg=n).aggregate(Sum("value1"))
                value5n = VR22.objects.select_related('r22').filter(r22_id=5, doc__build__id_reg=n).aggregate(Sum("value1"))
                value6n = VR22.objects.select_related('r22').filter(r22_id=6, doc__build__id_reg=n).aggregate(Sum("value1"))
                if value2n['value1__sum'] is None:
                    value2 += 0
                else:
                    value2 += value2n['value1__sum']
                if value3n['value1__sum'] is None:
                    value3 += 0
                else:
                    value3 += value3n['value1__sum']
                if value4n['value1__sum'] is None:
                    value4 += 0
                else:
                    value4 += value4n['value1__sum']
                if value5n['value1__sum'] is None:
                    value5 += 0
                else:
                    value5 += value5n['value1__sum']
                if value6n['value1__sum'] is None:
                    value6 += 0
                else:
                    value6 += value6n['value1__sum']
            value = [value2, value3, value4, value5, value6]
        elif id_dia == 9:
            value2 = 0
            value3 = 0
            value4 = 0
            value5 = 0
            value6 = 0
            for n in range(8, 14):
                value2n = VR25.objects.select_related('r25').filter(r25_id=2, doc__build__id_reg=n).aggregate(Sum("value1"))
                value3n = VR25.objects.select_related('r25').filter(r25_id=3, doc__build__id_reg=n).aggregate(Sum("value1"))
                value4n = VR25.objects.select_related('r25').filter(r25_id=4, doc__build__id_reg=n).aggregate(Sum("value1"))
                value5n = VR25.objects.select_related('r25').filter(r25_id=5, doc__build__id_reg=n).aggregate(Sum("value1"))
                value6n = VR25.objects.select_related('r25').filter(r25_id=6, doc__build__id_reg=n).aggregate(Sum("value1"))
                if value2n['value1__sum'] is None:
                    value2 += 0
                else:
                    value2 += value2n['value1__sum']
                if value3n['value1__sum'] is None:
                    value3 += 0
                else:
                    value3 += value3n['value1__sum']
                if value4n['value1__sum'] is None:
                    value4 += 0
                else:
                    value4 += value4n['value1__sum']
                if value5n['value1__sum'] is None:
                    value5 += 0
                else:
                    value5 += value5n['value1__sum']
                if value6n['value1__sum'] is None:
                    value6 += 0
                else:
                    value6 += value6n['value1__sum']
            value = [value2, value3, value4, value5, value6]
        else:
            value2 = 0
            b = 0
            for n in range(8, 14):
                value2 += Builds.objects.filter(link='docs/default/template.xlsx', id_reg=n).count()
                b += Builds.objects.filter(id_reg=n).count()
            value1 = b - value2
            value = [value1, value2]
    else:
        if id_dia == 2:
            value1 = VR1.objects.select_related('r1').filter(r1="2", value=1, doc__build__id_reg=id).count()
            value2 = VR1.objects.select_related('r1').filter(r1="2", value=2, doc__build__id_reg=id).count()
            value = [value1, value2]
        elif id_dia == 3:
            value1 = VR2.objects.select_related('r2').filter(r2_id=1, doc__build__id_reg=id).aggregate(Sum("value"))
            value2 = VR2.objects.select_related('r2').filter(r2_id=2, doc__build__id_reg=id).aggregate(Sum("value"))
            value3 = VR2.objects.select_related('r2').filter(r2_id=3, doc__build__id_reg=id).aggregate(Sum("value"))
            value4 = VR2.objects.select_related('r2').filter(r2_id=4, doc__build__id_reg=id).aggregate(Sum("value"))
            value5 = VR2.objects.select_related('r2').filter(r2_id=5, doc__build__id_reg=id).aggregate(Sum("value"))
            if value1['value__sum'] is None:
                value1 = 0
            else:
                value1 = value1['value__sum']
            if value2['value__sum'] is None:
                value2 = 0
            else:
                value2 = value2['value__sum']
            if value3['value__sum'] is None:
                value3 = 0
            else:
                value3 = value3['value__sum']
            if value4['value__sum'] is None:
                value4 = 0
            else:
                value4 = value4['value__sum']
            if value5['value__sum'] is None:
                value5 = 0
            else:
                value5 = value5['value__sum']
            value = [value1, value2, value3, value4, value5]
        elif id_dia == 4:
            value2 = VR9.objects.select_related('r9').filter(r9_id=1, doc__build__id_reg=id).aggregate(Sum("value2"))
            value3 = VR9.objects.select_related('r9').filter(r9_id=1, doc__build__id_reg=id).aggregate(Sum("value3"))
            value4 = VR9.objects.select_related('r9').filter(r9_id=1, doc__build__id_reg=id).aggregate(Sum("value4"))
            value5 = VR9.objects.select_related('r9').filter(r9_id=1, doc__build__id_reg=id).aggregate(Sum("value5"))
            value6 = VR9.objects.select_related('r9').filter(r9_id=1, doc__build__id_reg=id).aggregate(Sum("value6"))
            if value2['value2__sum'] is None:
                value2 = 0
            else:
                value2 = value2['value2__sum']
            if value3['value3__sum'] is None:
                value3 = 0
            else:
                value3 = value3['value3__sum']
            if value4['value4__sum'] is None:
                value4 = 0
            else:
                value4 = value4['value4__sum']
            if value5['value5__sum'] is None:
                value5 = 0
            else:
                value5 = value5['value5__sum']
            if value6['value6__sum'] is None:
                value6 = 0
            else:
                value6 = value6['value6__sum']
            value = [value2, value3, value4, value5, value6]
        elif id_dia == 5:
            value1 = VR16.objects.select_related('r16').filter(r16_id=1, value1=1, doc__build__id_reg=id).count()
            value2 = VR16.objects.select_related('r16').filter(r16_id=2, value1=1, doc__build__id_reg=id).count()
            value3 = VR16.objects.select_related('r16').filter(r16_id=3, value1=1, doc__build__id_reg=id).count()
            value4 = VR16.objects.select_related('r16').filter(r16_id=4, value1=1, doc__build__id_reg=id).count()
            value5 = VR16.objects.select_related('r16').filter(r16_id=5, value1=1, doc__build__id_reg=id).count()
            value6 = VR16.objects.select_related('r16').filter(r16_id=6, value1=1, doc__build__id_reg=id).count()
            value7 = VR16.objects.select_related('r16').filter(r16_id=7, value1=1, doc__build__id_reg=id).count()
            value8 = VR16.objects.select_related('r16').filter(r16_id=8, value1=1, doc__build__id_reg=id).count()
            value9 = VR16.objects.select_related('r16').filter(r16_id=9, value1=1, doc__build__id_reg=id).count()
            value10 = VR16.objects.select_related('r16').filter(r16_id=10, value1=1, doc__build__id_reg=id).count()
            value11 = VR16.objects.select_related('r16').filter(r16_id=11, value1=1, doc__build__id_reg=id).count()
            value12 = VR16.objects.select_related('r16').filter(r16_id=12, value1=1, doc__build__id_reg=id).count()
            value13 = VR16.objects.select_related('r16').filter(r16_id=13, value1=1, doc__build__id_reg=id).count()
            value14 = VR16.objects.select_related('r16').filter(r16_id=14, value1=1, doc__build__id_reg=id).count()
            value15 = VR16.objects.select_related('r16').filter(r16_id=15, value1=1, doc__build__id_reg=id).count()
            value16 = VR16.objects.select_related('r16').filter(r16_id=16, value1=1, doc__build__id_reg=id).count()
            value17 = VR16.objects.select_related('r16').filter(r16_id=17, value1=1, doc__build__id_reg=id).count()
            value18 = VR16.objects.select_related('r16').filter(r16_id=18, value1=1, doc__build__id_reg=id).count()
            value19 = VR16.objects.select_related('r16').filter(r16_id=19, value1=1, doc__build__id_reg=id).count()
            value20 = VR16.objects.select_related('r16').filter(r16_id=20, value1=1, doc__build__id_reg=id).count()
            value21 = VR16.objects.select_related('r16').filter(r16_id=21, value1=1, doc__build__id_reg=id).count()
            value = [
                value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, value11, value12,
                value13, value14, value15, value16, value17, value18, value19, value20, value21
            ]
        elif id_dia == 6:
            value1 = VR18.objects.select_related('r18').filter(r18_id=1, value1=1, doc__build__id_reg=id).count()
            value2 = VR18.objects.select_related('r18').filter(r18_id=2, value1=1, doc__build__id_reg=id).count()
            value3 = VR18.objects.select_related('r18').filter(r18_id=3, value1=1, doc__build__id_reg=id).count()
            value4 = VR18.objects.select_related('r18').filter(r18_id=4, value1=1, doc__build__id_reg=id).count()
            value5 = VR18.objects.select_related('r18').filter(r18_id=5, value1=1, doc__build__id_reg=id).count()
            value6 = VR18.objects.select_related('r18').filter(r18_id=6, value1=1, doc__build__id_reg=id).count()
            value7 = VR18.objects.select_related('r18').filter(r18_id=7, value1=1, doc__build__id_reg=id).count()
            value8 = VR18.objects.select_related('r18').filter(r18_id=8, value1=1, doc__build__id_reg=id).count()
            value9 = VR18.objects.select_related('r18').filter(r18_id=9, value1=1, doc__build__id_reg=id).count()
            value10 = VR18.objects.select_related('r18').filter(r18_id=10, value1=1, doc__build__id_reg=id).count()
            value11 = VR18.objects.select_related('r18').filter(r18_id=11, value1=1, doc__build__id_reg=id).count()
            value = [value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, value11]
        elif id_dia == 7:
            value1 = VR19.objects.select_related('r19').filter(r19_id=1, value1=1, doc__build__id_reg=id).count()
            value2 = VR19.objects.select_related('r19').filter(r19_id=2, value1=1, doc__build__id_reg=id).count()
            value3 = VR19.objects.select_related('r19').filter(r19_id=3, value1=1, doc__build__id_reg=id).count()
            value4 = VR19.objects.select_related('r19').filter(r19_id=4, value1=1, doc__build__id_reg=id).count()
            value5 = VR19.objects.select_related('r19').filter(r19_id=5, value1=1, doc__build__id_reg=id).count()
            value6 = VR19.objects.select_related('r19').filter(r19_id=6, value1=1, doc__build__id_reg=id).count()
            value7 = VR19.objects.select_related('r19').filter(r19_id=7, value1=1, doc__build__id_reg=id).count()
            value8 = VR19.objects.select_related('r19').filter(r19_id=8, value1=1, doc__build__id_reg=id).count()
            value = [value1, value2, value3, value4, value5, value6, value7, value8]
        elif id_dia == 8:
            value2 = VR22.objects.select_related('r22').filter(r22_id=2, doc__build__id_reg=id).aggregate(Sum("value1"))
            value3 = VR22.objects.select_related('r22').filter(r22_id=3, doc__build__id_reg=id).aggregate(Sum("value1"))
            value4 = VR22.objects.select_related('r22').filter(r22_id=4, doc__build__id_reg=id).aggregate(Sum("value1"))
            value5 = VR22.objects.select_related('r22').filter(r22_id=5, doc__build__id_reg=id).aggregate(Sum("value1"))
            value6 = VR22.objects.select_related('r22').filter(r22_id=6, doc__build__id_reg=id).aggregate(Sum("value1"))
            if value2['value1__sum'] is None:
                value2 = 0
            else:
                value2 = value2['value1__sum']
            if value3['value1__sum'] is None:
                value3 = 0
            else:
                value3 = value3['value1__sum']
            if value4['value1__sum'] is None:
                value4 = 0
            else:
                value4 = value4['value1__sum']
            if value5['value1__sum'] is None:
                value5 = 0
            else:
                value5 = value5['value1__sum']
            if value6['value1__sum'] is None:
                value6 = 0
            else:
                value6 = value6['value1__sum']
            value = [value2, value3, value4, value5, value6]
        elif id_dia == 9:
            value2 = VR25.objects.select_related('r25').filter(r25_id=2, doc__build__id_reg=id).aggregate(Sum("value1"))
            value3 = VR25.objects.select_related('r25').filter(r25_id=3, doc__build__id_reg=id).aggregate(Sum("value1"))
            value4 = VR25.objects.select_related('r25').filter(r25_id=4, doc__build__id_reg=id).aggregate(Sum("value1"))
            value5 = VR25.objects.select_related('r25').filter(r25_id=5, doc__build__id_reg=id).aggregate(Sum("value1"))
            value6 = VR25.objects.select_related('r25').filter(r25_id=6, doc__build__id_reg=id).aggregate(Sum("value1"))
            if value2['value1__sum'] is None:
                value2 = 0
            else:
                value2 = value2['value1__sum']
            if value3['value1__sum'] is None:
                value3 = 0
            else:
                value3 = value3['value1__sum']
            if value4['value1__sum'] is None:
                value4 = 0
            else:
                value4 = value4['value1__sum']
            if value5['value1__sum'] is None:
                value5 = 0
            else:
                value5 = value5['value1__sum']
            if value6['value1__sum'] is None:
                value6 = 0
            else:
                value6 = value6['value1__sum']
            value = [value2, value3, value4, value5, value6]
        else:
            value2 = Builds.objects.filter(link='docs/default/template.xlsx', id_reg=id).count()
            b = Builds.objects.filter(id_reg=id).count()
            value1 = b - value2
            value = [value1, value2]
    return value


def home(request):
    card_data = smart_card(-1)
    q = request.GET.get('q')
    if (q is None) or (q == ''):
        q = 1
    else:
        q = int(q)
    name = smart_diagram_name(q)
    value = smart_diagram_value(-1, q)
    text_for_diagram = text_diagram()
    context = {'card_data': card_data, 'name': name, 'value': value, 'q': q, 'text_for_diagram': text_for_diagram}
    return render(request, 'blog/home.html', context)


def about(request):
    builds = Builds.objects.filter(id_reg=2)

    # for build in builds:
    #     print(build)
    #     buildoc = BuildDocs()
    #     buildoc.build = build
    #     buildoc.user = request.user
    #     buildoc.save()
    return render(request, 'blog/about.html', {'title': 'О ресурсе'})


def info(request, id):
    query = request.GET.get('q')
    if query is None:
        query = ''

    d = request.GET.get('d')
    if (d is None) or (d == ''):
        d = 1
    else:
        d = int(d)
    text_for_diagram = text_diagram()
    name = smart_diagram_name(d)
    value = smart_diagram_value(id, d)
    card_data = smart_card(id)

    if id == 0:
        flag = False
        text8 = Regions.objects.get(id=8)
        text9 = Regions.objects.get(id=9)
        text10 = Regions.objects.get(id=10)
        text11 = Regions.objects.get(id=11)
        text12 = Regions.objects.get(id=12)
        text13 = Regions.objects.get(id=13)

        if query is None:
            build8 = Builds.objects.filter(id_reg=8).order_by('id')
            build9 = Builds.objects.filter(id_reg=9).order_by('id')
            build10 = Builds.objects.filter(id_reg=10).order_by('id')
            build11 = Builds.objects.filter(id_reg=11).order_by('id')
            build12 = Builds.objects.filter(id_reg=12).order_by('id')
            build13 = Builds.objects.filter(id_reg=13).order_by('id')
        else:
            build8 = Builds.objects.filter(
                Q(id_reg=8) &
                (Q(id__icontains=query) | Q(name__icontains=query))
            ).order_by('id')
            build9 = Builds.objects.filter(
                Q(id_reg=9) &
                (Q(id__icontains=query) | Q(name__icontains=query))
            ).order_by('id')
            build10 = Builds.objects.filter(
                Q(id_reg=10) &
                (Q(id__icontains=query) | Q(name__icontains=query))
            ).order_by('id')
            build11 = Builds.objects.filter(
                Q(id_reg=11) &
                (Q(id__icontains=query) | Q(name__icontains=query))
            ).order_by('id')
            build12 = Builds.objects.filter(
                Q(id_reg=12) &
                (Q(id__icontains=query) | Q(name__icontains=query))
            ).order_by('id')
            build13 = Builds.objects.filter(
                Q(id_reg=13) &
                (Q(id__icontains=query) | Q(name__icontains=query))
            ).order_by('id')
        text = {
            "name": 'Воронеж'
        }
        builds_title = [
            text8.name,
            text9.name,
            text10.name,
            text11.name,
            text12.name,
            text13.name
        ]
        builds_data = [
            build8,
            build9,
            build10,
            build11,
            build12,
            build13
        ]
        diagram_data = [
            name,
            value
        ]
        context = {
            'builds_data': builds_data, 'builds_title': builds_title, 'text': text, 'flag': flag, 'id_info': id,
            'card_data': card_data, 'diagram_data': diagram_data, 'd': d, 'query': query, 'text_for_diagram': text_for_diagram
        }
        return render(request, 'blog/builds.html', context)
    else:
        flag = True
        text = Regions.objects.get(id=id)
        if query is None:
            builds = Builds.objects.filter(id_reg=id)
        else:
            builds = Builds.objects.filter(
                Q(id_reg=id) &
                (Q(id__icontains=query) | Q(name__icontains=query))
            ).order_by('id')

        diagram_data = [
            name,
            value
        ]
        context = {
            'builds': builds, 'text': text, 'flag': flag, 'id_info': id, 'card_data': card_data,
            'diagram_data': diagram_data, 'd': d, 'query': query, 'text_for_diagram': text_for_diagram
        }
        return render(request, 'blog/builds.html', context)


def buildinfo(request, id):
    build = Builds.objects.get(id=id)
    context = {'build': build}
    return render(request, 'blog/buildinfo.html', context)


def vr(request, id_build, id):
    warning = ''
    doc = BuildDocs.objects.get(build=id_build)
    title = ''
    VR = None
    if id == 1:
        title = 'Раздел 1. Сведения об организации'
        VR = VR1.objects.select_related('r1').filter(doc=doc).order_by('r1_id')

    elif id == 2:
        title = 'Раздел 2. Режим работы групп и численность воспитанников в них'
        VR = VR2.objects.select_related('r2').filter(doc=doc).order_by('r2_id')

    elif id == 3:
        title = 'Раздел 3. Образовательные программы дошкольного образования и формы их реализации'
        VR = VR3.objects.select_related('r3').filter(doc=doc).order_by('r3_id')

    elif id == 4:
        title = 'Раздел 4. Распределение групп по направленности и возрасту детей'
        VR = VR4.objects.select_related('r4').filter(doc=doc).order_by('r4_id')

    elif id == 5:
        title = 'Раздел 5. Распределение мест в группах по направленности и возрасту детей'
        VR = VR5.objects.select_related('r5').filter(doc=doc).order_by('r5_id')

    elif id == 6:
        title = 'Раздел 6. Численность воспитанников в группах'
        VR = VR6.objects.select_related('r6').filter(doc=doc).order_by('r6_id')

    elif id == 7:
        title = 'Раздел 7. Распределение воспитанников по возрасту'
        VR = VR7.objects.select_related('r7').filter(doc=doc).order_by('r7_id')

    elif id == 8:
        title = 'Раздел 8. Язык обучения и воспитания'
        VR = VR8.objects.select_related('r8').filter(doc=doc).order_by('r8_id')

    elif id == 9:
        title = 'Раздел 9. Распределение персонала по уровню образования и полу'
        VR = VR9.objects.select_related('r9').filter(doc=doc).order_by('r9_id')

    elif id == 10:
        title = 'Раздел 10. Распределение персонала по возрасту'
        VR = VR10.objects.select_related('r10').filter(doc=doc).order_by('r10_id')

    elif id == 11:
        title = 'Раздел 11. Распределение педагогических работников по стажу работы'
        VR = VR11.objects.select_related('r11').filter(doc=doc).order_by('r11_id')

    elif id == 12:
        title = 'Раздел 12. Численность внешних совместителей и работающих по договорам гражданско-правового характера'
        VR = VR12.objects.select_related('r12').filter(doc=doc).order_by('r12_id')

    elif id == 13:
        title = 'Раздел 13. Движение работников'
        VR = VR13.objects.select_related('r13').filter(doc=doc).order_by('r13_id')

    elif id == 14:
        title = 'Раздел 14. Характеристика здания (зданий)'
        VR = VR14.objects.select_related('r14').filter(doc=doc).order_by('r14_id')

    elif id == 15:
        title = 'Раздел 15. Характеристика материала стен здания (зданий)'
        VR = VR15.objects.select_related('r15').filter(doc=doc).order_by('r15_id')

    elif id == 16:
        title = 'Раздел 16. Сведения о помещениях дошкольной образовательной организации'
        VR = VR16.objects.select_related('r16').filter(doc=doc).order_by('r16_id')

    elif id == 17:
        title = 'Раздел 17. Наличие и использование площадей, квадратный метр'
        VR = VR17.objects.select_related('r17').filter(doc=doc).order_by('r17_id')

    elif id == 18:
        title = 'Раздел 18. Оснащение дошкольной образовательной организации'
        VR = VR18.objects.select_related('r18').filter(doc=doc).order_by('r18_id')

    elif id == 19:
        title = 'Раздел 19. Техническое оснащение для детей-инвалидов и детей с ОВЗ'
        VR = VR19.objects.select_related('r19').filter(doc=doc).order_by('r19_id')

    elif id == 20:
        title = 'Раздел 20. Электронные ресурсы дошкольной образовательной организации, единица'
        VR = VR20.objects.select_related('r20').filter(doc=doc).order_by('r20_id')

    elif id == 21:
        title = 'Раздел 21. Распределение объема средств организации по источникам их получения и видам деятельности'
        VR = VR21.objects.select_related('r21').filter(doc=doc).order_by('r21_id')

    elif id == 22:
        title = 'Раздел 22. Расходы организации'
        VR = VR22.objects.select_related('r22').filter(doc=doc).order_by('r22_id')

    elif id == 23:
        title = 'Раздел 23. Сведения о численности и оплате труда работников организации'
        VR = VR23.objects.select_related('r23').filter(doc=doc).order_by('r23_id')

    elif id == 24:
        title = 'Раздел 24. Затраты на внедрение и использование цифровых технологий дошкольной образовательной организацией в отчетном году, тысяч рублей (с одним десятичным знаком)'
        VR = VR24.objects.select_related('r24').filter(doc=doc).order_by('r24_id')

    elif id == 25:
        title = 'Раздел 25. Источники финансирования внутренних затрат дошкольной образовательной организацией на внедрение и использование цифровых технологий", тысяч рублей (с одним десятичным знаком)'
        VR = VR25.objects.select_related('r25').filter(doc=doc).order_by('r25_id')

    if not VR:
        warning = "Ошибка доступа: нет такой информации"
    context = {'title': title, 'VR': VR, 'flag': id, 'id_build': id_build, 'warning': warning}
    return render(request, 'blog/VR.html', context)


@login_required
def lk(request):
    query = request.GET.get('q')
    if query is None:
        query = ""
    if request.user.username == 'admin':
        if query is None:
            buildsuser = BuildDocs.objects.select_related('build').all().order_by('build_id')
        else:
            buildsuser = BuildDocs.objects.select_related('build').filter(
                Q(build__id__icontains=query) | Q(build__name__icontains=query)
            ).order_by('build_id')
    else:
        if query is None:
            buildsuser = BuildDocs.objects.select_related('build').filter(user=request.user).order_by('build_id')
        else:
            buildsuser = BuildDocs.objects.select_related('build').filter(
                Q(user=request.user) &
                (Q(build__id__icontains=query) | Q(build__name__icontains=query))
            ).order_by('build_id')

    v_data = [
        5,
        10,
        15,
        20,
        25,
        30,
        35,
        40,
        45,
        50
    ]

    default_page = 1
    page = request.GET.get('page', default_page)

    v = request.GET.get('v')
    if (v is None) or (v == ''):
        v = 10
    else:
        v = int(v)

    # Paginate items
    items_per_page = v
    paginator = Paginator(buildsuser, items_per_page)

    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(default_page)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)

    context = {'builds': buildsuser, 'query': query, "items_page": items_page, 'v': v, 'v_data': v_data}
    return render(request, 'blog/lk.html', context)


@login_required
def redact_data(request, build_id):
    buildsuser = BuildDocs.objects.select_related('build').filter(user=request.user).order_by('build_id')
    context = {'builds': buildsuser}
    if request.method == 'POST':
        form = forms.BuildsForm(request.POST, request.FILES, instance=Builds.objects.get(id=build_id))
        if form.is_valid():
            form.save()
            build = Builds.objects.get(pk=build_id)
            doc = BuildDocs.objects.get(build=build_id)
            path = str(build.link)
            data = data_doc_search(request, path)
            r1 = R1.objects.all()
            return render(request, 'blog/dop_red.html', {
                "data": data,
                'doc_id': doc.id,
                'path': path
            })

            # upload(request, doc.id, path)

            # return render(request, 'blog/lk.html', context)
    else:
        form = forms.BuildsForm(instance=Builds.objects.get(id=build_id))
    return render(request, 'blog/redact_data.html', {
        'form': form,
    })


@login_required
def userprofile(request):
    if request.method == 'POST':
        form = forms.UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog-home')
    else:
        form = forms.UpdateUserForm(instance=request.user)
    return render(request, 'blog/userprofile.html', {
        'form': form,
    })


def filter(request):
    regions = request.GET.getlist('regions[]')
    vr = request.GET.get('VR')

    query = request.GET.get('q')
    if query is None:
        query = ""

    title = None
    if (vr is None) or (vr == ''):
        vr = 0
    else:
        vr = int(vr)
    buildinfo = request.GET.getlist('buildinfo[]')

    data = []
    namebuilds = []

    if (not regions) or (regions == ''):
        if (query is None) or (query == ''):
            builds = BuildDocs.objects.select_related('build').all().order_by('build_id')
        else:
            builds = BuildDocs.objects.select_related('build').filter(
                Q(build__id__icontains=query) | Q(build__name__icontains=query)
            ).order_by('build_id')
    else:
        if (query is None) or (query == ''):

            builds = BuildDocs.objects.select_related('build').filter(build__id_reg__in = regions).order_by('build_id')

        else:
            for region in regions:
                builds = BuildDocs.objects.select_related('build').filter(
                    Q(build__id_reg__in = regions) &
                    (Q(build__id__icontains=query) | Q(build__name__icontains=query))
                ).order_by('build_id')

    if not buildinfo:
        flag = 0
    else:
        flag = 1
        if vr == 0:
            for d in buildinfo:
                title = 'Общие сведения'
                data.append(Builds.objects.get(pk=d))
        elif vr == 1:
            for d in buildinfo:
                title = 'Раздел 1. Сведения об организации'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR1.objects.select_related('doc', 'r1').filter(doc=doc).order_by('r1_id'))
        elif vr == 2:
            for d in buildinfo:
                title = 'Раздел 2. Режим работы групп и численность воспитанников в них'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR2.objects.select_related('doc', 'r2').filter(doc=doc).order_by('r2_id'))
        elif vr == 3:
            for d in buildinfo:
                title = 'Раздел 3. Образовательные программы дошкольного образования и формы их реализации'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR3.objects.select_related('doc', 'r3').filter(doc=doc).order_by('r3_id'))
        elif vr == 4:
            for d in buildinfo:
                title = 'Раздел 4. Распределение групп по направленности и возрасту детей'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR4.objects.select_related('doc', 'r4').filter(doc=doc).order_by('r4_id'))
        elif vr == 5:
            for d in buildinfo:
                title = 'Раздел 5. Распределение мест в группах по направленности и возрасту детей'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR5.objects.select_related('doc', 'r5').filter(doc=doc).order_by('r5_id'))
        elif vr == 6:
            for d in buildinfo:
                title = 'Раздел 6. Численность воспитанников в группах'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR6.objects.select_related('doc', 'r6').filter(doc=doc).order_by('r6_id'))
        elif vr == 7:
            for d in buildinfo:
                title = 'Раздел 7. Распределение воспитанников по возрасту'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR7.objects.select_related('doc', 'r7').filter(doc=doc).order_by('r7_id'))
        elif vr == 8:
            for d in buildinfo:
                title = 'Раздел 8. Язык обучения и воспитания'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR8.objects.select_related('doc', 'r8').filter(doc=doc).order_by('r8_id'))
        elif vr == 9:
            for d in buildinfo:
                title = 'Раздел 9. Распределение персонала по уровню образования и полу'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR9.objects.select_related('doc', 'r9').filter(doc=doc).order_by('r9_id'))
        elif vr == 10:
            for d in buildinfo:
                title = 'Раздел 10. Распределение персонала по возрасту'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR10.objects.select_related('doc', 'r10').filter(doc=doc).order_by('r10_id'))
        elif vr == 11:
            for d in buildinfo:
                title = 'Раздел 11. Распределение педагогических работников по стажу работы'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR11.objects.select_related('doc', 'r11').filter(doc=doc).order_by('r11_id'))
        elif vr == 12:
            for d in buildinfo:
                title = 'Раздел 12. Численность внешних совместителей и работающих по договорам гражданско-правового характера'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR12.objects.select_related('doc', 'r12').filter(doc=doc).order_by('r12_id'))
        elif vr == 13:
            for d in buildinfo:
                title = 'Раздел 13. Движение работников'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR13.objects.select_related('doc', 'r13').filter(doc=doc).order_by('r13_id'))
        elif vr == 14:
            for d in buildinfo:
                title = 'Раздел 14. Характеристика здания (зданий)'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR14.objects.select_related('doc', 'r14').filter(doc=doc).order_by('r14_id'))
        elif vr == 15:
            for d in buildinfo:
                title = 'Раздел 15. Характеристика материала стен здания (зданий)'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR15.objects.select_related('doc', 'r15').filter(doc=doc).order_by('r15_id'))
        elif vr == 16:
            for d in buildinfo:
                title = 'Раздел 16. Сведения о помещениях дошкольной образовательной организации'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR16.objects.select_related('doc', 'r16').filter(doc=doc).order_by('r16_id'))
        elif vr == 17:
            for d in buildinfo:
                title = 'Раздел 17. Наличие и использование площадей, квадратный метр'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR17.objects.select_related('doc', 'r17').filter(doc=doc).order_by('r17_id'))
        elif vr == 18:
            for d in buildinfo:
                title = 'Раздел 18. Оснащение дошкольной образовательной организации'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR18.objects.select_related('doc', 'r18').filter(doc=doc).order_by('r18_id'))
        elif vr == 19:
            for d in buildinfo:
                title = 'Раздел 19. Техническое оснащение для детей-инвалидов и детей с ОВЗ'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR19.objects.select_related('doc', 'r19').filter(doc=doc).order_by('r19_id'))
        elif vr == 20:
            for d in buildinfo:
                title = 'Раздел 20. Электронные ресурсы дошкольной образовательной организации, единица'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR20.objects.select_related('doc', 'r20').filter(doc=doc).order_by('r20_id'))
        elif vr == 21:
            for d in buildinfo:
                title = 'Раздел 21. Распределение объема средств организации по источникам их получения и видам деятельности'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR21.objects.select_related('doc', 'r21').filter(doc=doc).order_by('r21_id'))
        elif vr == 22:
            for d in buildinfo:
                title = 'Раздел 22. Расходы организации'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR22.objects.select_related('doc', 'r22').filter(doc=doc).order_by('r22_id'))
        elif vr == 23:
            for d in buildinfo:
                title = 'Раздел 23. Сведения о численности и оплате труда работников организации'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR23.objects.select_related('doc', 'r23').filter(doc=doc).order_by('r23_id'))
        elif vr == 24:
            for d in buildinfo:
                title = 'Раздел 24. Затраты на внедрение и использование цифровых технологий дошкольной образовательной организацией в отчетном году, тысяч рублей (с одним десятичным знаком)'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR24.objects.select_related('doc', 'r24').filter(doc=doc).order_by('r24_id'))
        elif vr == 25:
            for d in buildinfo:
                title = 'Раздел 25. Источники финансирования внутренних затрат дошкольной образовательной организацией на внедрение и использование цифровых технологий", тысяч рублей (с одним десятичным знаком)'
                doc = BuildDocs.objects.get(build=d)
                data.append(VR25.objects.select_related('doc', 'r25').filter(doc=doc).order_by('r25_id'))
        for d in buildinfo:
            namebuilds.append(Builds.objects.get(pk=d))
    region = Regions.objects.all()

    test = []
    for r in regions:
        test.append(int(r))
    regions = test

    data_filter = [
        [0, 'Общие сведения'],
        [1, 'Раздел 1'],
        [2, 'Раздел 2'],
        [3, 'Раздел 3'],
        [4, 'Раздел 4'],
        [5, 'Раздел 5'],
        [6, 'Раздел 6'],
        [7, 'Раздел 7'],
        [8, 'Раздел 8'],
        [9, 'Раздел 9'],
        [10, 'Раздел 10'],
        [11, 'Раздел 11'],
        [12, 'Раздел 12'],
        [13, 'Раздел 13'],
        [14, 'Раздел 14'],
        [15, 'Раздел 15'],
        [16, 'Раздел 16'],
        [17, 'Раздел 17'],
        [18, 'Раздел 18'],
        [19, 'Раздел 19'],
        [20, 'Раздел 20'],
        [21, 'Раздел 21'],
        [22, 'Раздел 22'],
        [23, 'Раздел 23'],
        [24, 'Раздел 24'],
        [25, 'Раздел 25']
    ]

    v_data = [
        5,
        10,
        15,
        20,
        25,
        30,
        35,
        40,
        45,
        50
    ]

    default_page = 1
    page = request.GET.get('page', default_page)

    v = request.GET.get('v')
    if (v is None) or (v == ''):
        v = 10
    else:
        v = int(v)

    # Paginate items
    items_per_page = v
    paginator = Paginator(builds, items_per_page)

    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(default_page)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)

    st = ""
    for r in regions:
        st = st + 'regions[]=' + str(r) + '&'



    context = {
        'builds': builds, 'flag': flag, 'data': data, 'title': title, 'id': vr, 'region': region, 'nameb': namebuilds,
        'regions': regions, 'data_filter': data_filter, 'vr': vr, 'query': query, "items_page": items_page, 'str': st,
        'v': v, 'v_data': v_data
    }
    return render(request, 'blog/filter.html', context)


def diagram(request):

    q = request.GET.get('q')
    if (q is None) or (q == ''):
        q = 0
    q = int(q)

    if q == 2:
        name = [
            "Городская местность",
            "Сельская местность"
        ]
        value1 = VR1.objects.select_related('r1').filter(r1="1", value=1).count()
        value2 = VR1.objects.select_related('r1').filter(r1="2", value=2).count()

        value = [value1, value2]

    elif q == 3:
        name = [
            "Численность воспитанников кратковременного пребывания (5 часов и менее)",
            "Численность воспитанников сокращенного дня (8 - 10 часов)",
            "Численность воспитанников полного дня (10,5 - 12 часов)",
            "Численность воспитанников продленного дня (13 - 14 часов)",
            "Численность воспитанников"
        ]
        value1 = VR2.objects.select_related('r2').filter(r2_id=1).aggregate(Sum("value"))
        value2 = VR2.objects.select_related('r2').filter(r2_id=2).aggregate(Sum("value"))
        value3 = VR2.objects.select_related('r2').filter(r2_id=3).aggregate(Sum("value"))
        value4 = VR2.objects.select_related('r2').filter(r2_id=4).aggregate(Sum("value"))
        value5 = VR2.objects.select_related('r2').filter(r2_id=5).aggregate(Sum("value"))

        value = [
            value1['value__sum'], value2['value__sum'], value3['value__sum'],
            value4['value__sum'], value5['value__sum']
        ]

    elif q == 4:
        name = [
            "Всего работников",
            "Из всех работников имеют высшее образование",
            "Высшее педагогическое образование",
            "Сред. проф. образование по программам подготовки специалистов среднего звена",
            "Сред. проф. педагогическое образование по программам подготовки специалистов среднего звена",
            "Из всех работников всего женщин"
        ]
        value1 = VR9.objects.select_related('r9').filter(r9_id=1).aggregate(Sum("value1"))
        value2 = VR9.objects.select_related('r9').filter(r9_id=1).aggregate(Sum("value2"))
        value3 = VR9.objects.select_related('r9').filter(r9_id=1).aggregate(Sum("value3"))
        value4 = VR9.objects.select_related('r9').filter(r9_id=1).aggregate(Sum("value4"))
        value5 = VR9.objects.select_related('r9').filter(r9_id=1).aggregate(Sum("value5"))
        value6 = VR9.objects.select_related('r9').filter(r9_id=1).aggregate(Sum("value6"))

        value = [
            value1['value1__sum'], value2['value2__sum'], value3['value3__sum'],
            value4['value4__sum'], value5['value5__sum'], value6['value6__sum']
        ]

    elif q == 5:
        name = [
            "Кабинет заведующего",
            "Групповые комнаты",
            "Спальни",
            "Соляная комната/пещера",
            "Комнаты для специалистов",
            "Медицинский кабинет",
            "Изолятор",
            "Процедурный кабинет",
            "Методический кабинет",
            "Физкультурный/спортивный зал",
            "Музыкальный зал",
            "Плавательный бассейн",
            "Зимний сад/экологическая комната",
            "Подсобное помещение",
            "Лаборатория",
            "Места для личной гигиены",
            "Раздевальная",
            "Помещения для приготовления и раздачи пищи",
            "Кинозал",
            "Книгохранилище\библиотека",
            "Фитобар"
        ]
        value1 = VR16.objects.select_related('r16').filter(r16_id=1, value1=1).count()
        value2 = VR16.objects.select_related('r16').filter(r16_id=2, value1=1).count()
        value3 = VR16.objects.select_related('r16').filter(r16_id=3, value1=1).count()
        value4 = VR16.objects.select_related('r16').filter(r16_id=4, value1=1).count()
        value5 = VR16.objects.select_related('r16').filter(r16_id=5, value1=1).count()
        value6 = VR16.objects.select_related('r16').filter(r16_id=6, value1=1).count()
        value7 = VR16.objects.select_related('r16').filter(r16_id=7, value1=1).count()
        value8 = VR16.objects.select_related('r16').filter(r16_id=8, value1=1).count()
        value9 = VR16.objects.select_related('r16').filter(r16_id=9, value1=1).count()
        value10 = VR16.objects.select_related('r16').filter(r16_id=10, value1=1).count()
        value11 = VR16.objects.select_related('r16').filter(r16_id=11, value1=1).count()
        value12 = VR16.objects.select_related('r16').filter(r16_id=12, value1=1).count()
        value13 = VR16.objects.select_related('r16').filter(r16_id=13, value1=1).count()
        value14 = VR16.objects.select_related('r16').filter(r16_id=14, value1=1).count()
        value15 = VR16.objects.select_related('r16').filter(r16_id=15, value1=1).count()
        value16 = VR16.objects.select_related('r16').filter(r16_id=16, value1=1).count()
        value17 = VR16.objects.select_related('r16').filter(r16_id=17, value1=1).count()
        value18 = VR16.objects.select_related('r16').filter(r16_id=18, value1=1).count()
        value19 = VR16.objects.select_related('r16').filter(r16_id=19, value1=1).count()
        value20 = VR16.objects.select_related('r16').filter(r16_id=20, value1=1).count()
        value21 = VR16.objects.select_related('r16').filter(r16_id=21, value1=1).count()

        value = [
            value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, value11, value12, value13,
            value14, value15, value16, value17, value18, value19, value20, value21
        ]

    elif q == 6:
        name = [
            "интерактивной доски, ин. стола, демонстр. экрана с мультимед. проектором",
            "цифрового/интерактивного пола",
            "бизибордов",
            "стола для рисования в технике Эбру",
            "сухого бассейна",
            "светового стола для рисования песком",
            "печатных книг/журналов для чтения воспитанниками",
            "электронные средства обучения",
            "магнитных досок",
            "скалодрома",
            "батута"
        ]
        value1 = VR18.objects.select_related('r18').filter(r18_id=1, value1=1).count()
        value2 = VR18.objects.select_related('r18').filter(r18_id=2, value1=1).count()
        value3 = VR18.objects.select_related('r18').filter(r18_id=3, value1=1).count()
        value4 = VR18.objects.select_related('r18').filter(r18_id=4, value1=1).count()
        value5 = VR18.objects.select_related('r18').filter(r18_id=5, value1=1).count()
        value6 = VR18.objects.select_related('r18').filter(r18_id=6, value1=1).count()
        value7 = VR18.objects.select_related('r18').filter(r18_id=7, value1=1).count()
        value8 = VR18.objects.select_related('r18').filter(r18_id=8, value1=1).count()
        value9 = VR18.objects.select_related('r18').filter(r18_id=9, value1=1).count()
        value10 = VR18.objects.select_related('r18').filter(r18_id=10, value1=1).count()
        value11 = VR18.objects.select_related('r18').filter(r18_id=11, value1=1).count()

        value = [
            value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, value11]

    elif q == 7:
        name = [
            "пандуса",
            "подъемника для детей",
            "лифта для детей",
            "инвалидных колясок",
            "книг для слабовидящих",
            "электронных обучающих материалов (игр и презентаций)",
            "стационарного спортивного оборудования (тренажеров)",
            "звуковые средства воспроизведения информации"
        ]
        value1 = VR19.objects.select_related('r19').filter(r19_id=1, value1=1).count()
        value2 = VR19.objects.select_related('r19').filter(r19_id=2, value1=1).count()
        value3 = VR19.objects.select_related('r19').filter(r19_id=3, value1=1).count()
        value4 = VR19.objects.select_related('r19').filter(r19_id=4, value1=1).count()
        value5 = VR19.objects.select_related('r19').filter(r19_id=5, value1=1).count()
        value6 = VR19.objects.select_related('r19').filter(r19_id=6, value1=1).count()
        value7 = VR19.objects.select_related('r19').filter(r19_id=7, value1=1).count()
        value8 = VR19.objects.select_related('r19').filter(r19_id=8, value1=1).count()

        value = [
            value1, value2, value3, value4, value5, value6, value7, value8]

    elif q == 8:
        name = [
            "Расходы - всего",
            "Расходы - оплата труда и начисления на выплаты по оплате труда",
            "Расходы - оплата работ, услуг",
            "Расходы - социальное обеспечение",
            "Расходы - прочие расходы",
            "Поступление нефинансовых активов"
        ]
        value1 = VR22.objects.select_related('r22').filter(r22_id=1).aggregate(Sum("value1"))
        value2 = VR22.objects.select_related('r22').filter(r22_id=2).aggregate(Sum("value1"))
        value3 = VR22.objects.select_related('r22').filter(r22_id=3).aggregate(Sum("value1"))
        value4 = VR22.objects.select_related('r22').filter(r22_id=4).aggregate(Sum("value1"))
        value5 = VR22.objects.select_related('r22').filter(r22_id=5).aggregate(Sum("value1"))
        value6 = VR22.objects.select_related('r22').filter(r22_id=6).aggregate(Sum("value1"))

        value = [
            value1['value1__sum'], value2['value1__sum'], value3['value1__sum'],
            value4['value1__sum'], value5['value1__sum'], value6['value1__sum']
        ]
    elif q == 9:
        name = [
            "Внут. затраты на внедр. и испол. цифр. тех. - всего",
            "Внут. затраты на внедр. и испол. цифр. тех. - собственные средства орг.",
            "Внут. затраты на внедр. и испол. цифр. тех. - средства бюджет. всех уровней",
            "Внут. затраты на внедр. и испол. цифр. тех. - прочие привлеч. средства",
            "Прочие привлеч. средства: некоммерч. орг.",
            "Прочие привлеченные средства: физических лиц"
        ]
        value1 = VR25.objects.select_related('r25').filter(r25_id=1).aggregate(Sum("value1"))
        value2 = VR25.objects.select_related('r25').filter(r25_id=2).aggregate(Sum("value1"))
        value3 = VR25.objects.select_related('r25').filter(r25_id=3).aggregate(Sum("value1"))
        value4 = VR25.objects.select_related('r25').filter(r25_id=4).aggregate(Sum("value1"))
        value5 = VR25.objects.select_related('r25').filter(r25_id=5).aggregate(Sum("value1"))
        value6 = VR25.objects.select_related('r25').filter(r25_id=6).aggregate(Sum("value1"))

        value = [
            value1['value1__sum'], value2['value1__sum'], value3['value1__sum'],
            value4['value1__sum'], value5['value1__sum'], value6['value1__sum']
        ]
    else:
        name = ["Подали данные по форме N 85-К", 'Не подали данные']
        value1 = Builds.objects.filter(link='docs/default/template.xlsx').count()
        b = Builds.objects.count()
        value2 = b - value1
        value = [value2, value1]
    context = {'name': name, 'value': value, 'q': q}
    return render(request, 'test/test_diagram.html', context)


# def test(request):
#     builds = Builds.objects.all()
#     for build in builds:
#         buildoc = BuildDocs()
#         buildoc.build = build
#         buildoc.user = request.user
#         buildoc.save()
#     return render(request, 'blog/home.html')


# def load(request, doc_id):
#     excel = Excel()
#     wb = excel.load(os.path.join(Path(__file__).resolve().parent.parent, excel.EXCEL_PATH))
#     data = {}
#     try:
#         doc = BuildDocs.objects.get(pk=doc_id)
#         for i in range(len(wb.get_sheet_names())):
#             table = wb.get_sheet_names()[i]
#             raw_data = DatabaseController.db_to_df(table, doc.id)
#             df = pandas.DataFrame.from_dict(raw_data)
#             df = df.replace(-1, 'X')
#             df = df.drop(columns=['id', 'doc_id', table[1:].lower() + '_id'])
#             data[i] = {
#                 'title': table,
#                 'df': df
#             }
#             print(table)
#             excel.df_to_wb(df, wb.get_sheet_by_name(table))
#         excel.save(wb, str(doc.id))
#     except Exception as e:
#         print("Error during select: ", e)
#     context = {'data': data}
#     return render(request, 'test/excel_view.html', context)
