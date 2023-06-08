from django.db import models
from django.contrib.auth.models import User


class Archive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    link = models.FileField(upload_to='docs/archive', verbose_name='Устаревший документ')
    date = models.DateTimeField()

    def __str__(self):
        return 'Замена от {}'.format(self.date.strftime('%d.%m.%Y %H:%M'))


class Regions(models.Model):
    name = models.TextField(max_length=50, verbose_name='Регионы и области')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Регионы и области'
        verbose_name = 'Регионы и области'


class Builds(models.Model):
    id_reg = models.ForeignKey(Regions, on_delete=models.CASCADE, verbose_name='Регион')
    name = models.TextField(max_length=300, verbose_name='Наименование оганизации')
    adres = models.TextField(max_length=300, blank=True, verbose_name='Юридический адрес')
    logo = models.ImageField(blank=True, verbose_name='Логотип', upload_to='images/')
    FIO = models.CharField(max_length=300, blank=True, verbose_name='ФИО руководителя')
    telephone = models.CharField(max_length=300, blank=True, null=True, verbose_name='Телефон')
    email = models.CharField(max_length=300, blank=True, null=True, verbose_name='Адрес электронной почты')
    site = models.CharField(max_length=300, blank=True, null=True, verbose_name='Адрес сайта организации')
    workers = models.IntegerField(blank=True, null=True, verbose_name='Количество педогогических работников')
    students = models.IntegerField(blank=True, null=True, verbose_name='Количество учеников')
    link = models.FileField(upload_to='docs/', verbose_name='Документ', default='docs/default/template.xlsx')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Организации'
        verbose_name = 'Организация'


class BuildDocs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    build = models.ForeignKey(Builds, on_delete=models.CASCADE, verbose_name='Организация')


    def __str__(self):
        return self.build.name

    class Meta:
        verbose_name_plural = 'Добавить документ'
        verbose_name = 'Добавить документ'


class R1(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R1'
        verbose_name = 'R1'


class R2(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R2'
        verbose_name = 'R2'


class R3(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R3'
        verbose_name = 'R3'


class R4_R5_R6(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R4_R5_R6'
        verbose_name = 'R4_R5_R6'


class R7(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R7'
        verbose_name = 'R7'


class R8(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R8'
        verbose_name = 'R8'


class R9(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R9'
        verbose_name = 'R9'


class R10_R11_R13(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R10_R11_R13'
        verbose_name = 'R10_R11_R13'


class R12(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R12'
        verbose_name = 'R12'


class R14(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R14'
        verbose_name = 'R14'


class R15(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R15'
        verbose_name = 'R15'


class R16(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R16'
        verbose_name = 'R16'


class R17(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R17'
        verbose_name = 'R17'


class R18(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R18'
        verbose_name = 'R18'


class R19(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R19'
        verbose_name = 'R19'


class R20(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R20'
        verbose_name = 'R20'


class R21(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R21'
        verbose_name = 'R21'


class R22(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R22'
        verbose_name = 'R22'


class R23(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R23'
        verbose_name = 'R23'


class R24(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R24'
        verbose_name = 'R24'


class R25(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R25'
        verbose_name = 'R25'


class VR1(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r1 = models.ForeignKey(R1, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value = models.IntegerField(verbose_name='код')

    class Meta:
        verbose_name_plural = 'VR1'
        verbose_name = 'VR1'


class VR2(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r2 = models.ForeignKey(R2, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value = models.IntegerField(verbose_name='Численность воспитанников, чел.')

    class Meta:
        verbose_name_plural = 'VR2'
        verbose_name = 'VR2'


class VR3(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r3 = models.ForeignKey(R3, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Всего реализуемых образовательных программ')
    value2 = models.IntegerField(null=True, blank=True, verbose_name='Число образовательных программ реализуемых с использованием сетевой формы')
    value3 = models.IntegerField(null=True, blank=True, verbose_name='Общее число заключенных договоров с организациями на реализацию образовательных программ с использованием сетевой формы')
    value4 = models.IntegerField(null=True, blank=True, verbose_name='Численность воспитанников, обучающихся с применением сетевой формы')

    class Meta:
        verbose_name_plural = 'VR3'
        verbose_name = 'VR3'


class VR4(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r4 = models.ForeignKey(R4_R5_R6, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(verbose_name='Всего групп')
    value2 = models.IntegerField(verbose_name='от 2-х месяцев до 1 года')
    value3 = models.IntegerField(verbose_name='от 1 года до 3-х лет')
    value4 = models.IntegerField(verbose_name='от 3-х до 5 лет')
    value5 = models.IntegerField(verbose_name='5 лет и старше')
    value6 = models.IntegerField(verbose_name='разновозрастные')

    class Meta:
        verbose_name_plural = 'VR4'
        verbose_name = 'VR4'


class VR5(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r5 = models.ForeignKey(R4_R5_R6, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(verbose_name='Всего групп')
    value2 = models.IntegerField(verbose_name='от 2-х месяцев до 1 года')
    value3 = models.IntegerField(verbose_name='от 1 года до 3-х лет')
    value4 = models.IntegerField(verbose_name='от 3-х до 5 лет')
    value5 = models.IntegerField(verbose_name='5 лет и старше')
    value6 = models.IntegerField(verbose_name='разновозрастные')

    class Meta:
        verbose_name_plural = 'VR5'
        verbose_name = 'VR5'


class VR6(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r6 = models.ForeignKey(R4_R5_R6, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(verbose_name='Всего групп')
    value2 = models.IntegerField(verbose_name='от 2-х месяцев до 1 года')
    value3 = models.IntegerField(verbose_name='от 1 года до 3-х лет')
    value4 = models.IntegerField(verbose_name='от 3-х до 5 лет')
    value5 = models.IntegerField(verbose_name='5 лет и старше')
    value6 = models.IntegerField(verbose_name='разновозрастные')
    value7 = models.IntegerField(verbose_name='с ограниченными возможностями здоровья')
    value8 = models.IntegerField(verbose_name='из них дети-инвалиды')
    value9 = models.IntegerField(verbose_name='дети-инвалиды, не учтенные в группах')
    value10 = models.IntegerField(verbose_name='имеющие иностранное гражданство или имеющие несколько гражданств')
    value11 = models.IntegerField(verbose_name='без гражданства')

    class Meta:
        verbose_name_plural = 'VR6'
        verbose_name = 'VR6'


class VR7(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r7 = models.ForeignKey(R7, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(verbose_name='Всего')
    value2 = models.IntegerField(verbose_name='0 лет')
    value3 = models.IntegerField(verbose_name='1 год')
    value4 = models.IntegerField(verbose_name='2 года')
    value5 = models.IntegerField(verbose_name='3 года')
    value6 = models.IntegerField(verbose_name='4 лет')
    value7 = models.IntegerField(verbose_name='5 лет')
    value8 = models.IntegerField(verbose_name='6 лет')
    value9 = models.IntegerField(verbose_name='7 лет и старше')

    class Meta:
        verbose_name_plural = 'VR7'
        verbose_name = 'VR7'


class VR8(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r8 = models.ForeignKey(R8, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(verbose_name='Численность воспитанников')

    class Meta:
        verbose_name_plural = 'VR8'
        verbose_name = 'VR8'


class VR9(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r9 = models.ForeignKey(R9, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(verbose_name='Всего')
    value2 = models.IntegerField(null=True, blank=True, verbose_name='Высшее образование')
    value3 = models.IntegerField(null=True, blank=True, verbose_name='Высшее педагогическое образование')
    value4 = models.IntegerField(null=True, blank=True, verbose_name='Среднее профессиональное образование по программам подготовки специалистов среднего звена')
    value5 = models.IntegerField(null=True, blank=True, verbose_name='среднее профессиональное педагогическое образование')
    value6 = models.IntegerField(verbose_name='Всего женщин')

    class Meta:
        verbose_name_plural = 'VR9'
        verbose_name = 'VR9'


class VR10(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r10 = models.ForeignKey(R10_R11_R13, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(verbose_name='Всего')
    value2 = models.IntegerField(verbose_name='моложе 25 лет')
    value3 = models.IntegerField(verbose_name='25-29')
    value4 = models.IntegerField(verbose_name='30-34')
    value5 = models.IntegerField(verbose_name='35-39')
    value6 = models.IntegerField(verbose_name='40-44')
    value7 = models.IntegerField(verbose_name='45-49')
    value8 = models.IntegerField(verbose_name='50-54')
    value9 = models.IntegerField(verbose_name='55-59')
    value10 = models.IntegerField(verbose_name='60-64')
    value11 = models.IntegerField(verbose_name='65 и старше')

    class Meta:
        verbose_name_plural = 'VR10'
        verbose_name = 'VR10'


class VR11(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r11 = models.ForeignKey(R10_R11_R13, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(verbose_name='Всего с общим стажем')
    value2 = models.IntegerField(verbose_name='с общим стажем до 3 лет')
    value3 = models.IntegerField(verbose_name='с общим стажем от 3 до 5 лет')
    value4 = models.IntegerField(verbose_name='с общим стажем от 5 до 10 лет')
    value5 = models.IntegerField(verbose_name='с общим стажем от 10 до 15 лет')
    value6 = models.IntegerField(verbose_name='с общим стажем от 15 до 20 лет')
    value7 = models.IntegerField(verbose_name='с общим стажем от 20 и более лет')
    value8 = models.IntegerField(verbose_name='Из общей численности работников имеют педагогический стаж (всего)')
    value9 = models.IntegerField(verbose_name='с педагогическим стажем до 3 лет')
    value10 = models.IntegerField(verbose_name='с педагогическим стажем от 3 до 5 лет')
    value11 = models.IntegerField(verbose_name='с педагогическим стажем от 5 до 10 лет')
    value12 = models.IntegerField(verbose_name='с педагогическим стажем от 10 до 15 лет')
    value13 = models.IntegerField(verbose_name='с педагогическим стажем от 15 до 20 лет')
    value14 = models.IntegerField(verbose_name='с педагогическим стажем от 20 и более лет')

    class Meta:
        verbose_name_plural = 'VR11'
        verbose_name = 'VR11'


class VR12(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r12 = models.ForeignKey(R12, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(verbose_name='Всего')
    value2 = models.IntegerField(verbose_name='Всего женщин')

    class Meta:
        verbose_name_plural = 'VR12'
        verbose_name = 'VR12'


class VR13(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r13 = models.ForeignKey(R10_R11_R13, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(verbose_name='Число ставок по штату, ед.')
    value2 = models.IntegerField(verbose_name='Всего фактически занято')
    value3 = models.IntegerField(verbose_name='Фактически занято работниками списочного состава')
    value4 = models.IntegerField(verbose_name='Численность работников на начало отчетного года (без внешних совместителей и работающих по договорам гражданско- правового характера)')
    value5 = models.IntegerField(verbose_name='Всего принято работников')
    value6 = models.IntegerField(verbose_name='Принято работников, являющимися выпускниками со средним профессиональным образованием по программам подготовки специалистов среднего звена')
    value7 = models.IntegerField(verbose_name='Принято работников, являющимися выпускниками с высшим образованием')
    value8 = models.IntegerField(verbose_name='Всего выбыло работников')
    value9 = models.IntegerField(verbose_name='Выбыло работников по собственному желанию')
    value10 = models.IntegerField(verbose_name='Численность работников на конец отчетного года (без совместителей и работающих по договорам гражданско-правового характера)')
    value11 = models.IntegerField(verbose_name='Число вакантных должностей')

    class Meta:
        verbose_name_plural = 'VR13'
        verbose_name = 'VR13'


class VR14(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r14 = models.ForeignKey(R14, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Всего')
    value2 = models.IntegerField(null=True, blank=True, verbose_name='Оборудовано водопроводом')
    value3 = models.IntegerField(null=True, blank=True, verbose_name='Оборудовано водоотведением (канализацией)')
    value4 = models.IntegerField(null=True, blank=True, verbose_name='Оборудовано центральным отоплением')
    value5 = models.IntegerField(null=True, blank=True, verbose_name='Оборудовано системой видеонаблюдения')
    value6 = models.IntegerField(null=True, blank=True, verbose_name='Требует капитального ремонта')
    value7 = models.IntegerField(null=True, blank=True, verbose_name='Находится в аварийном состоянии')
    value8 = models.IntegerField(null=True, blank=True, verbose_name='Имеет охрану')
    value9 = models.IntegerField(null=True, blank=True, verbose_name='Оборудовано автоматической пожарной сигнализацией')
    value10 = models.IntegerField(null=True, blank=True, verbose_name='Имеет дымовые извещатели')
    value11 = models.IntegerField(null=True, blank=True, verbose_name='Имеет пожарные краны и рукава')
    value12 = models.IntegerField(null=True, blank=True, verbose_name='Оборудовано кнопкой тревожной сигнализации')
    value13 = models.IntegerField(null=True, blank=True, verbose_name='Доступно для маломобильных групп населения')
    value14 = models.IntegerField(null=True, blank=True, verbose_name='Скорость Интернета ниже 256 Кбит/сек')
    value15 = models.IntegerField(null=True, blank=True, verbose_name='Скорость Интернета 256 - 511 Кбит/сек')
    value16 = models.IntegerField(null=True, blank=True, verbose_name='Скорость Интернета 512 Кбит/сек - 999 Кбит/сек')
    value17 = models.IntegerField(null=True, blank=True, verbose_name='Скорость Интернета 1.0 - 1.9 Мбит/сек')
    value18 = models.IntegerField(null=True, blank=True, verbose_name='Скорость Интернета 2.0 - 29.9 Мбит/сек')
    value19 = models.IntegerField(null=True, blank=True, verbose_name='Скорость Интернета 30.0 - 49.9 Мбит/сек')
    value20 = models.IntegerField(null=True, blank=True, verbose_name='Скорость Интернета 50.0 - 99.9 Мбит/сек')
    value21 = models.IntegerField(null=True, blank=True, verbose_name='Скорость Интернета 100 Мбит/сек и выше')

    class Meta:
        verbose_name_plural = 'VR14'
        verbose_name = 'VR14'


class VR15(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r15 = models.ForeignKey(R15, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Стены здания: каменные')
    value2 = models.IntegerField(null=True, blank=True, verbose_name='Стены здания: кирпичные')
    value3 = models.IntegerField(null=True, blank=True, verbose_name='Стены здания: панельные')
    value4 = models.IntegerField(null=True, blank=True, verbose_name='Стены здания: блочные')
    value5 = models.IntegerField(null=True, blank=True, verbose_name='Стены здания: деревянные')
    value6 = models.IntegerField(null=True, blank=True, verbose_name='Стены здания: монолитные')
    value7 = models.IntegerField(null=True, blank=True, verbose_name='Стены здания: смешанные')
    value8 = models.IntegerField(null=True, blank=True, verbose_name='Стены здания: из прочих стеновых материалов')

    class Meta:
        verbose_name_plural = 'VR15'
        verbose_name = 'VR15'


class VR16(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r16 = models.ForeignKey(R16, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Наличие в организации, код: да - 1, нет - 2')

    class Meta:
        verbose_name_plural = 'VR16'
        verbose_name = 'VR16'


class VR17(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r17 = models.ForeignKey(R17, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Всего')
    value2 = models.IntegerField(null=True, blank=True, verbose_name='Площадь, сданная в аренду и/или субаренду')
    value3 = models.IntegerField(null=True, blank=True, verbose_name='Площадь на правах собственности')
    value4 = models.IntegerField(null=True, blank=True, verbose_name='Площадь в оперативном управлении')
    value5 = models.IntegerField(null=True, blank=True, verbose_name='Арендованная площадь')
    value6 = models.IntegerField(null=True, blank=True, verbose_name='Площадь в другой форме владения')

    class Meta:
        verbose_name_plural = 'VR17'
        verbose_name = 'VR17'


class VR18(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r18 = models.ForeignKey(R18, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Наличие в организации, код: да - 1, нет - 2')

    class Meta:
        verbose_name_plural = 'VR18'
        verbose_name = 'VR18'


class VR19(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r19 = models.ForeignKey(R19, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Наличие в организации, код: да - 1, нет - 2')

    class Meta:
        verbose_name_plural = 'VR19'
        verbose_name = 'VR19'


class VR20(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r20 = models.ForeignKey(R20, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Всего')
    value2 = models.IntegerField(null=True, blank=True, verbose_name='в том числе доступные для использования воспитанниками')

    class Meta:
        verbose_name_plural = 'VR20'
        verbose_name = 'VR20'


class VR21(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r21 = models.ForeignKey(R21, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Всего')
    value2 = models.IntegerField(null=True, blank=True, verbose_name='из них по образовательной деятельности')

    class Meta:
        verbose_name_plural = 'VR21'
        verbose_name = 'VR21'


class VR22(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r22 = models.ForeignKey(R22, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Всего')
    value2 = models.IntegerField(null=True, blank=True, verbose_name='из них осуществляемые за счет средств бюджетов всех уровней (субсидий)')

    class Meta:
        verbose_name_plural = 'VR22'
        verbose_name = 'VR22'


class VR23(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r23 = models.ForeignKey(R23, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Средняя численность работников списочного состава (без внешних совместителей)')
    value2 = models.IntegerField(null=True, blank=True, verbose_name='Средняя численность работников внешних совместителей')
    value3 = models.IntegerField(null=True, blank=True, verbose_name='Фонд начисленной заработной платы работников, тыс. руб, списочного состава (без внешних совместителей) Всего')
    value4 = models.IntegerField(null=True, blank=True, verbose_name='Фонд начисленной заработной платы работников, тыс. руб, списочного состава (без внешних совместителей) в том числе по внутреннему совместительству')
    value5 = models.IntegerField(null=True, blank=True, verbose_name='Фонд начисленной заработной платы работников, тыс. руб, внешних совместителей')
    value6 = models.IntegerField(null=True, blank=True, verbose_name='Фонд начисленной заработной платы работников по источникам финансирования из всего списочного состава (без внешних совместителей) за счет средств бюджетов всех уровней (субсидий)')
    value7 = models.IntegerField(null=True, blank=True, verbose_name='Фонд начисленной заработной платы работников по источникам финансирования из всего списочного состава (без внешних совместителей) ОМС')
    value8 = models.IntegerField(null=True, blank=True, verbose_name='Фонд начисленной заработной платы работников по источникам финансирования из всего списочного состава (без внешних совместителей) средства от приносящей доход деятельности')
    value9 = models.IntegerField(null=True, blank=True, verbose_name='Фонд начисленной заработной платы работников по источникам финансирования из внешних совместителей за счет средств бюджетов всех уровней (субсидий)')
    value10 = models.IntegerField(null=True, blank=True, verbose_name='Фонд начисленной заработной платы работников по источникам финансирования из внешних совместителей ОМС')
    value11 = models.IntegerField(null=True, blank=True, verbose_name='Фонд начисленной заработной платы работников по источникам финансирования из внешних совместителей средства от приносящей доход деятельности')

    class Meta:
        verbose_name_plural = 'VR23'
        verbose_name = 'VR23'


class VR24(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r24 = models.ForeignKey(R24, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Всего')

    class Meta:
        verbose_name_plural = 'VR24'
        verbose_name = 'VR24'


class VR25(models.Model):
    doc = models.ForeignKey(BuildDocs, on_delete=models.CASCADE, verbose_name='Документ')
    r25 = models.ForeignKey(R25, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Всего')

    class Meta:
        verbose_name_plural = 'VR25'
        verbose_name = 'VR25'

















































#
# class Users(models.Model):
#     MAN = 'M'
#     WOMAN = 'W'
#     SEX = [
#         (MAN, 'Мужской'),
#         (WOMAN, 'Женский'),
#     ]
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     second_name = models.CharField(max_length=50, blank=True, verbose_name='Отчество', help_text='Отчество пользователя')
#     age = models.IntegerField(null=True, blank=True, verbose_name='Возраст', help_text='Полных лет пользователя')
#     city = models.CharField(max_length=50, blank=True, verbose_name='Город', help_text='Город, в котором живет пользователь')
#     sex = models.CharField(max_length=1, blank=True, verbose_name='Пол', choices=SEX, default=MAN, help_text='Пол пользователя')
#
#     def __str__(self):
#         return self.user.username
#
#     class Meta:
#         verbose_name_plural = 'Пользователи'
#         verbose_name = 'Пользователь'
#
#
# class Event(models.Model):
#     DONTSTART = '1'
#     STARTING = '2'
#     END = '3'
#     STATUS_EVENT = [
#         (DONTSTART, 'Не началось'),
#         (STARTING, 'В процессе'),
#         (END, 'Закончилось'),
#     ]
#     name = models.CharField(max_length=50, verbose_name='Название', help_text='Название мероприятия')
#     desctiption = models.TextField(null=True, blank=True, verbose_name='Описание', help_text='Описание мероприятия')
#     logo = models.ImageField(max_length=50, blank=True, verbose_name='Логотип', help_text='Логотип мероприятия', upload_to='images/')
#     status_event = models.CharField(max_length=1, verbose_name='Статус', choices=STATUS_EVENT, default=DONTSTART, help_text='Статус мероприятия')
#     data_start = models.DateField(null=True, verbose_name='Дата начала', help_text='Дата начала мероприятия')
#     data_end = models.DateField(null=True, verbose_name='Дата конца', help_text='Дата конца мероприятия')
#     city = models.TextField(max_length=50, verbose_name='Город', help_text='Город проведения мероприятия')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name_plural = 'События'
#         verbose_name = 'Событие'
#
#
# class Status(models.Model):
#     name = models.CharField(max_length=50, verbose_name='Роль', help_text='Роль человека на мероприятии')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name_plural = 'Статусы'
#         verbose_name = 'Статус'
#
#
# class UsersEvents(models.Model):
#     id_event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Событие в котором учавствует пользователь')
#     id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Участник события')
#     id_status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус участника в мероприятии')
#     date_reg = models.DateField(null=True, verbose_name='Дата регистрации', help_text='Дата регистрации на меропрятии')
#     link_certificate = models.FileField(null=True, blank=True, verbose_name='Сертификат', help_text='Сертификат участника мероприятия')
#     rating = models.IntegerField(null=True, blank=True, verbose_name='Занимеемое место', help_text='Занимеемое место на мероприятии')
#
#     class Meta:
#         unique_together = ('id_event', 'id_user')
#         verbose_name_plural = 'События и участники'
#         verbose_name = 'Событие и участник'
