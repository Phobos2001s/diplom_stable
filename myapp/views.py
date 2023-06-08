import django
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .models import Builds, Regions, VR1, VR25, VR24, VR23, VR22, VR21, VR20, VR19, VR18, VR17, VR16, \
    VR15, VR14, VR13, VR12, VR11, VR10, VR9, VR8, VR7, VR6, VR5, VR4, VR3, VR2
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


def load(request, doc_id):
    excel = Excel()
    wb = excel.load(os.path.join(Path(__file__).resolve().parent.parent, excel.EXCEL_PATH))
    data = {}
    try:
        doc = BuildDocs.objects.get(pk=doc_id)
        for i in range(len(wb.get_sheet_names())):
            table = wb.get_sheet_names()[i]
            raw_data = DatabaseController.db_to_df(table, doc.id)
            df = pandas.DataFrame.from_dict(raw_data)
            df = df.replace(-1, 'X')
            df = df.drop(columns=['id', 'doc_id', table[1:].lower() + '_id'])
            data[i] = {
                'title': table,
                'df': df
            }
            print(table)
            excel.df_to_wb(df, wb.get_sheet_by_name(table))
        excel.save(wb, str(doc.id))
    except Exception as e:
        print("Error during select: ", e)
    context = {'data': data}
    return render(request, 'test/excel_view.html', context)


def home(request):
    count_build = Builds.objects.count()
    count_workers = Builds.objects.aggregate(Sum("workers"))
    count_students = Builds.objects.aggregate(Sum("students"))
    context = {'count_build': count_build, 'count_workers': count_workers, 'count_students': count_students}
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'Добавить информацию'})


def info(request, id):
    query = request.GET.get('q')
    if id == 0:
        count_build = Builds.objects.filter(
            Q(id_reg=8) | Q(id_reg=9) | Q(id_reg=10) | Q(id_reg=11) | Q(id_reg=12) | Q(id_reg=13)
        ).count()

        count_workers = Builds.objects.filter(
            Q(id_reg=8) | Q(id_reg=9) | Q(id_reg=10) | Q(id_reg=11) | Q(id_reg=12) | Q(id_reg=13)
        ).aggregate(Sum("workers"))

        count_students = Builds.objects.filter(
            Q(id_reg=8) | Q(id_reg=9) | Q(id_reg=10) | Q(id_reg=11) | Q(id_reg=12) | Q(id_reg=13)
        ).aggregate(Sum("students"))

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
        context = {
            'build8': build8, 'build9': build9, 'build10': build10, 'build11': build11, 'build12': build12,
            'build13': build13, 'text8': text8, 'text9': text9, 'text10': text10, 'text11': text11, 'text12': text12,
            'text13': text13, 'flag': flag, 'id_info': id, 'count_build': count_build, 'count_workers': count_workers,
            'count_students': count_students
        }
        return render(request, 'blog/builds.html', context)
    else:
        flag = True
        text = Regions.objects.get(id=id)
        count_build = Builds.objects.filter(id_reg=id).count()
        count_workers = Builds.objects.filter(id_reg=id).aggregate(Sum("workers"))
        count_students = Builds.objects.filter(id_reg=id).aggregate(Sum("students"))
        if query is None:
            builds = Builds.objects.filter(id_reg=id)
        else:
            builds = Builds.objects.filter(
                Q(id_reg=id) &
                (Q(id__icontains=query) | Q(name__icontains=query))
            ).order_by('id')
        context = {
            'builds': builds, 'text': text, 'flag': flag, 'id_info': id, 'count_build': count_build,
            'count_workers': count_workers, 'count_students': count_students
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
        warning = "Организация не предоставила таких данных"
    context = {'title': title, 'VR': VR, 'flag': id, 'id_build': id_build, 'warning': warning}
    return render(request, 'blog/VR.html', context)


@login_required
def lk(request):
    query = request.GET.get('q')
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
    context = {'builds': buildsuser}
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
            upload(request, doc.id, path)

            return render(request, 'blog/lk.html', context)
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
    title = None
    if (vr is None) or (vr == ''):
        vr = 0
    else:
        vr = int(vr)
    buildinfo = request.GET.getlist('buildinfo[]')

    data = []
    namebuilds = []
    builds = []

    if (not regions) or (regions == ''):
        builds.append(BuildDocs.objects.select_related('build').all().order_by('build_id'))
    else:
        for region in regions:
            r = int(region)
            builds.append(BuildDocs.objects.select_related('build').filter(build__id_reg=r).order_by('build_id'))

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

    context = {'builds': builds, 'flag': flag, 'data': data, 'title': title, 'id': vr, 'region': region,
               'nameb': namebuilds}
    return render(request, 'blog/filter.html', context)

# def test(request):
#     builds = Builds.objects.all()
#     for build in builds:
#         buildoc = BuildDocs()
#         buildoc.build = build
#         buildoc.user = request.user
#         buildoc.save()
#     return render(request, 'blog/home.html')
