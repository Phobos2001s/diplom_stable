from django.db import models
from django.contrib.auth.models import User


class Builds(models.Model):
    name = models.TextField(max_length=300, verbose_name='Наименование оганизации')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Организации'
        verbose_name = 'Организация'


class TitleDoc(models.Model):
    build = models.ForeignKey(Builds, on_delete=models.CASCADE, verbose_name='Событие в котором учавствует пользователь')
    mail = models.EmailField(max_length=20, verbose_name='Почтовый адрес')
    year = models.IntegerField(verbose_name='Год подачии документа: 202_г')
    date1 = models.DateField(null=True, blank=True, verbose_name='О внесении изменений (при наличии) от')
    date1_id = models.IntegerField(null=True, blank=True, verbose_name='№')
    date2 = models.DateField(null=True, blank=True, verbose_name='О внесении изменений (при наличии) от')
    date2_id = models.IntegerField(null=True, blank=True, verbose_name='№')
    okud_code = models.CharField(max_length=7, verbose_name='Код формы по ОКУД', default='0609506')
    okpo_code = models.CharField(max_length=15, verbose_name='Код отчитывающейся организации по ОКПО (для обособленного подразделения и головного подразделения юридического лица - идентификационный номер)')
    link = models.FileField(null=True, blank=True, upload_to='docs/', verbose_name='Документ')

    def __str__(self):
        return self.build.name

    class Meta:
        verbose_name_plural = 'Титульные листы'
        verbose_name = 'Титульный лист'


class VR1(models.Model):
    TYPE_BUILD = [
        ('5', 'дошкольная образовательная организация;'),
        ('2', 'обособленное подразделение (филиал) дошкольной образовательной организации;'),
        ('3', 'обособленное подразделение (филиал) общеобразовательной организации;'),
        ('15', 'обособленное подразделение (филиал) профессиональной образовательной организации;'),
        ('6', 'обособленное подразделение (филиал) образовательной организации высшего образования;'),
        ('13', 'подразделения (группы), осуществляющие образовательную деятельность по образовательным программам дошкольного образования, присмотр и уход за детьми; организованные при общеобразовательной организации;'),
        ('16', 'подразделения (группы), осуществляющие образовательную деятельность по образовательным программам дошкольного образования, присмотр и уход за детьми; организованные при профессиональной образовательной организации;'),
        ('7', 'подразделения (группы), осуществляющие образовательную деятельность по образовательным программам дошкольного образования, присмотр и уход за детьми; организованные при образовательной организации высшего образования;'),
        ('8', 'подразделения (группы), осуществляющие образовательную деятельность по образовательным программам дошкольного образования, присмотр и уход за детьми; организованные при организации дополнительного образования детей;'),
        ('9', 'подразделения (группы), созданные при ином юридическом лице или юридическое лицо, осуществляющее образовательную деятельность по образовательным программам дошкольного образования, присмотр и уход за детьми (организации здравоохранения, социального обслуживания, науки, культуры и другие, осуществляющие образовательную деятельность по образовательным программам дошкольного образования, присмотр и уход за детьми в качестве дополнительной к своей основной деятельности);'),
        ('14', 'организация, осуществляющая присмотр и уход за детьми, без осуществления образовательной деятельности по программам дошкольного образования (организации, осуществляющие присмотр и уход за детьми в качестве как основной, так и дополнительной к своей основной деятельности). В данных организациях обеспечивается комплекс мер по организации питания и хозяйственно-бытового обслуживания детей, обеспечению соблюдения ими личной гигиены и режима дня;'),
        ('17', 'индивидуальный предприниматель.'),
    ]
    TYPE_CITY = [
        ('1', 'городская местность;'),
        ('2', 'сельская местность.'),
    ]
    STATUS_BUILD = [
        ('1', 'функционирует;'),
        ('2', 'организация временно не работает из-за проведения капитального ремонта или реконструкции;'),
        ('3', 'организация функционирует и одно из зданий находится в аварийном состоянии;'),
        ('4', 'деятельность приостановлена;'),
        ('5', 'организация функционирует и одно из зданий требует капитального ремонта.'),
    ]
    WORK_DAYS = [
        ('2', 'пятидневный;'),
        ('3', 'шестидневный;'),
        ('14', 'семидневный (круглосуточно).'),
    ]
    SOCIAL_UNIT = [
        ('1', 'наличие в дошкольной образовательной организации коллегиального органа управления с участием общественности (родители, работодатели);'),
        ('2', 'отсутствие в дошкольной образовательной организации коллегиального органа управления с участием общественности.'),
    ]
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    type_build = models.CharField(max_length=2, verbose_name='Тип организации', choices=TYPE_BUILD, default='5')
    type_city = models.CharField(max_length=1, verbose_name='Тип поселения', choices=TYPE_CITY, default='1')
    status_build = models.CharField(max_length=1, verbose_name='Статус организации', choices=STATUS_BUILD, default='1')
    work_days = models.CharField(max_length=2, verbose_name='Режим функционирования', choices=WORK_DAYS, default='2')
    social_unit = models.CharField(max_length=1, verbose_name='Наличие коллегиального органа с участием общественности', choices=SOCIAL_UNIT, default='2')

    class Meta:
        verbose_name_plural = 'VR1'
        verbose_name = 'VR1'


class R2(models.Model):
    name = models.CharField(max_length=300, verbose_name='Режим работы')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R2'
        verbose_name = 'R2'


class VR2(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r2 = models.ForeignKey(R2, on_delete=models.CASCADE, verbose_name='Режим работы')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value = models.IntegerField(verbose_name='Численность воспитанников, чел')

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR2'
        verbose_name = 'VR2'


class R3(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование программ')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R3'
        verbose_name = 'R3'


class VR3(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r3 = models.ForeignKey(R3, on_delete=models.CASCADE, verbose_name='Наименование программ')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.IntegerField(verbose_name='Всего реализуемых образовательных программ')
    value2 = models.IntegerField(verbose_name='Число образовательных программ реализуемых с использованием сетевой формы')
    value3 = models.IntegerField(verbose_name='Общее число заключенных договоров с организациями на реализацию образовательных программ с использованием сетевой формы')
    value4 = models.IntegerField(verbose_name='Численность воспитанников, обучающихся с применением сетевой формы')

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR3'
        verbose_name = 'VR3'


class R4R5R6(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R4R5R6'
        verbose_name = 'R4R5R6'


class VR4(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r4 = models.ForeignKey(R4R5R6, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.IntegerField(verbose_name='Всего групп')
    value2 = models.IntegerField(verbose_name='от 2-х месяцев до 1 года')
    value3 = models.IntegerField(verbose_name='от 1 года до 3-х лет')
    value4 = models.IntegerField(verbose_name='от 3-х до 5 лет')
    value5 = models.IntegerField(verbose_name='5 лет и старше')
    value6 = models.IntegerField(verbose_name='разновозрастные')

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR4'
        verbose_name = 'VR4'


class VR5(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r5 = models.ForeignKey(R4R5R6, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.IntegerField(verbose_name='Всего мест в группах')
    value2 = models.IntegerField(verbose_name='от 2-х месяцев до 1 года')
    value3 = models.IntegerField(verbose_name='от 1 года до 3-х лет')
    value4 = models.IntegerField(verbose_name='от 3-х до 5 лет')
    value5 = models.IntegerField(verbose_name='5 лет и старше')
    value6 = models.IntegerField(verbose_name='разновозрастные')

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR5'
        verbose_name = 'VR5'


class VR6(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r6 = models.ForeignKey(R4R5R6, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.IntegerField(verbose_name='Всего детей в группах')
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

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR6'
        verbose_name = 'VR6'


class R7(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование программ')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R7'
        verbose_name = 'R7'


class VR7(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r7 = models.ForeignKey(R7, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.IntegerField(verbose_name='Всего')
    value2 = models.IntegerField(verbose_name='0 лет')
    value3 = models.IntegerField(verbose_name='1 год')
    value4 = models.IntegerField(verbose_name='2 года')
    value5 = models.IntegerField(verbose_name='3 года')
    value6 = models.IntegerField(verbose_name='4 лет')
    value7 = models.IntegerField(verbose_name='5 лет')
    value8 = models.IntegerField(verbose_name='6 лет')
    value9 = models.IntegerField(verbose_name='7 лет и старше')

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR7'
        verbose_name = 'VR7'


class R8(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R8'
        verbose_name = 'R8'


class VR8(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r8 = models.ForeignKey(R8, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.CharField(max_length=3, verbose_name='Код языка по Общероссийскому классификатору информации о населении (ОКИН)')
    value2 = models.IntegerField(verbose_name='Численность воспитанников')

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR8'
        verbose_name = 'VR8'


class R9(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R9'
        verbose_name = 'R9'


class VR9(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r9 = models.ForeignKey(R9, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.IntegerField(verbose_name='Всего')
    value2 = models.CharField(max_length=5, verbose_name='высшее')
    value3 = models.CharField(max_length=5, verbose_name='из них педагогическое')
    value4 = models.CharField(max_length=5, verbose_name='среднее профессиональное образование по программам подготовки специалистов среднего звена')
    value5 = models.CharField(max_length=5, verbose_name='из них педагогическое')
    value6 = models.IntegerField(verbose_name='всего женщин')

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR9'
        verbose_name = 'VR9'


class R10R11(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R10R11'
        verbose_name = 'R10R11'


class VR10(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r10 = models.ForeignKey(R10R11, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    str = models.CharField(max_length=4, verbose_name='№ строки')
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

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR10'
        verbose_name = 'VR10'


class VR11(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r11 = models.ForeignKey(R10R11, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    str = models.CharField(max_length=4, verbose_name='№ строки')
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

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR11'
        verbose_name = 'VR11'


class R12(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R12'
        verbose_name = 'R12'


class VR12(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r12 = models.ForeignKey(R12, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.IntegerField(verbose_name='Всего')
    value2 = models.IntegerField(verbose_name=' них женщины')

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR12'
        verbose_name = 'VR12'


class R13(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R13'
        verbose_name = 'R13'


class VR13(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r13 = models.ForeignKey(R13, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.IntegerField(verbose_name='Число ставок по штату, ед.')
    value2 = models.IntegerField(verbose_name='Всего фактически занято')
    value3 = models.IntegerField(verbose_name='Фактически занято работниками списочного состава')
    value4 = models.IntegerField(verbose_name='Численность работников на начало отчетного года (без внешних совместителей и работающих по договорам гражданско- правового характера) ')
    value5 = models.IntegerField(verbose_name='Всего принято работников')
    value6 = models.IntegerField(verbose_name='Принято работников, являющимися выпускниками со средним профессиональным образованием по программам подготовки специалистов среднего звена')
    value7 = models.IntegerField(verbose_name='Принято работников, являющимися выпускниками с высшим образованием')
    value8 = models.IntegerField(verbose_name='Всего выбыло работников')
    value9 = models.IntegerField(verbose_name='Выбыло работников по собственному желанию')
    value10 = models.IntegerField(verbose_name='Численность работников на конец отчетного года (без совместителей и работающих по договорам гражданско-правового характера)')
    value11 = models.IntegerField(verbose_name='Число вакантных должностей')

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR13'
        verbose_name = 'VR13'


class R14(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R14'
        verbose_name = 'R14'


class VR14(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r14 = models.ForeignKey(R14, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    str = models.CharField(max_length=4, verbose_name='№ строки')
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

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR14'
        verbose_name = 'VR14'


class VR15(models.Model):
    CHOICES = [
        ('1', 'Да'),
        ('2', 'Нет'),
    ]
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    name = models.CharField(max_length=20, verbose_name='Здание №', default='Здание №1')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.CharField(null=True, blank=True, max_length=1, choices=CHOICES, default='2', verbose_name='каменные')
    value2 = models.CharField(null=True, blank=True, max_length=1, choices=CHOICES, verbose_name='кирпичные')
    value3 = models.CharField(null=True, blank=True, max_length=1, choices=CHOICES, verbose_name='панельные')
    value4 = models.CharField(null=True, blank=True, max_length=1, choices=CHOICES, verbose_name='блочные')
    value5 = models.CharField(null=True, blank=True, max_length=1, choices=CHOICES, verbose_name='деревянные')
    value6 = models.CharField(null=True, blank=True, max_length=1, choices=CHOICES, verbose_name='монолитные')
    value7 = models.CharField(null=True, blank=True, max_length=1, choices=CHOICES, verbose_name='смешанные')
    value8 = models.CharField(null=True, blank=True, max_length=1, choices=CHOICES, verbose_name='из прочих стеновых материалов')

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR15'
        verbose_name = 'VR15'


class R16(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R16'
        verbose_name = 'R16'


class VR16(models.Model):
    CHOICES = [
        ('1', 'Да'),
        ('2', 'Нет'),
    ]
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r16 = models.ForeignKey(R16, on_delete=models.CASCADE, verbose_name='Наименование')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.CharField(null=True, blank=True, max_length=1, choices=CHOICES, verbose_name='Наличие в организации')

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR16'
        verbose_name = 'VR16'


class R17(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R17'
        verbose_name = 'R17'


class VR17(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r17 = models.ForeignKey(R17, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Всего')
    value2 = models.IntegerField(null=True, blank=True, verbose_name='в том числе площадь, сданная в аренду и/или субаренду')
    value3 = models.IntegerField(null=True, blank=True, verbose_name='Площадь на правах собственности')
    value4 = models.IntegerField(null=True, blank=True, verbose_name='Площадь в оперативном управлении')
    value5 = models.IntegerField(null=True, blank=True, verbose_name='Арендованная площадь')
    value6 = models.IntegerField(null=True, blank=True, verbose_name='Площадь в другой форме владения')

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR17'
        verbose_name = 'VR17'


class R18(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R18'
        verbose_name = 'R18'


class VR18(models.Model):
    CHOICES = [
        ('1', 'Да'),
        ('2', 'Нет'),
    ]
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r18 = models.ForeignKey(R18, on_delete=models.CASCADE, verbose_name='Наименование')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.CharField(null=True, blank=True, max_length=1, choices=CHOICES, verbose_name='Наличие в организации')

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR18'
        verbose_name = 'VR18'


class R19(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R19'
        verbose_name = 'R19'


class VR19(models.Model):
    CHOICES = [
        ('1', 'Да'),
        ('2', 'Нет'),
    ]
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r19 = models.ForeignKey(R19, on_delete=models.CASCADE, verbose_name='Наименование')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.CharField(null=True, blank=True, max_length=1, choices=CHOICES, verbose_name='Наличие в организации')

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR19'
        verbose_name = 'VR19'


class R20(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R20'
        verbose_name = 'R20'


class VR20(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r20 = models.ForeignKey(R20, on_delete=models.CASCADE, verbose_name='Наименование')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Всего')
    value2 = models.CharField(null=True, blank=True, max_length=5, verbose_name='в том числе доступные для использования воспитанниками')

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR20'
        verbose_name = 'VR20'


class R21(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R21'
        verbose_name = 'R21'


class VR21(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r21 = models.ForeignKey(R21, on_delete=models.CASCADE, verbose_name='Наименование')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Всего')
    value2 = models.CharField(null=True, blank=True, max_length=20, verbose_name='из них по образовательной деятельности')

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR21'
        verbose_name = 'VR21'


class R22(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R22'
        verbose_name = 'R22'


class VR22(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r22 = models.ForeignKey(R22, on_delete=models.CASCADE, verbose_name='Наименование')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Всего')
    value2 = models.IntegerField(null=True, blank=True, verbose_name='из них осуществляемые за счет средств бюджетов всех уровней (субсидий)')

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR22'
        verbose_name = 'VR22'


class R23(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование показателей')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R23'
        verbose_name = 'R23'


class VR23(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r23 = models.ForeignKey(R23, on_delete=models.CASCADE, verbose_name='Наименование показателей')
    str = models.CharField(max_length=4, verbose_name='№ строки')
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

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR23'
        verbose_name = 'VR23'


class R24(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R24'
        verbose_name = 'R24'


class VR24(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r24 = models.ForeignKey(R24, on_delete=models.CASCADE, verbose_name='Наименование')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Всего')

    def __str__(self):
        return self.str

    class Meta:
        verbose_name_plural = 'VR24'
        verbose_name = 'VR24'


class R25(models.Model):
    name = models.CharField(max_length=300, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'R25'
        verbose_name = 'R25'


class VR25(models.Model):
    title_doc = models.ForeignKey(TitleDoc, on_delete=models.CASCADE, verbose_name='Шапка документа')
    r25 = models.ForeignKey(R25, on_delete=models.CASCADE, verbose_name='Наименование')
    str = models.CharField(max_length=4, verbose_name='№ строки')
    value1 = models.IntegerField(null=True, blank=True, verbose_name='Всего')

    def __str__(self):
        return self.str

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
