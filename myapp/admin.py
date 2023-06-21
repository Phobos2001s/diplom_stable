from django import forms
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin


from .import models

admin.site.site_header = 'Административая часть системы'


class RegionResource(resources.ModelResource):
    class Meta:
        model = models.Regions


class RegionAdmin(ImportExportModelAdmin):
    resource_classes = [RegionResource]


class BuildResource(resources.ModelResource):
    class Meta:
        model = models.Builds


class BuildsAdmin(ImportExportModelAdmin):
    resource_classes = [BuildResource]
    list_display = ('id', 'id_reg', 'name')


class R1Resource(resources.ModelResource):
    class Meta:
        model = models.R1


class R1Admin(ImportExportModelAdmin):
    resource_classes = [R1Resource]


class R2Resource(resources.ModelResource):
    class Meta:
        model = models.R2


class R2Admin(ImportExportModelAdmin):
    resource_classes = [R2Resource]


class R3Resource(resources.ModelResource):
    class Meta:
        model = models.R3


class R3Admin(ImportExportModelAdmin):
    resource_classes = [R3Resource]


class R4R5R6Resource(resources.ModelResource):
    class Meta:
        model = models.R4_R5_R6


class R4R5R6Admin(ImportExportModelAdmin):
    resource_classes = [R4R5R6Resource]


class R7Resource(resources.ModelResource):
    class Meta:
        model = models.R7


class R7Admin(ImportExportModelAdmin):
    resource_classes = [R7Resource]


class R8Resource(resources.ModelResource):
    class Meta:
        model = models.R8


class R8Admin(ImportExportModelAdmin):
    resource_classes = [R8Resource]


class R9Resource(resources.ModelResource):
    class Meta:
        model = models.R9


class R9Admin(ImportExportModelAdmin):
    resource_classes = [R9Resource]


class R10R11R13Resource(resources.ModelResource):
    class Meta:
        model = models.R10_R11_R13


class R10R11R13Admin(ImportExportModelAdmin):
    resource_classes = [R10R11R13Resource]


class R12Resource(resources.ModelResource):
    class Meta:
        model = models.R12


class R12Admin(ImportExportModelAdmin):
    resource_classes = [R12Resource]


class R14Resource(resources.ModelResource):
    class Meta:
        model = models.R14


class R14Admin(ImportExportModelAdmin):
    resource_classes = [R14Resource]


class R15Resource(resources.ModelResource):
    class Meta:
        model = models.R15


class R15Admin(ImportExportModelAdmin):
    resource_classes = [R15Resource]


class R16Resource(resources.ModelResource):
    class Meta:
        model = models.R16


class R16Admin(ImportExportModelAdmin):
    resource_classes = [R16Resource]


class R17Resource(resources.ModelResource):
    class Meta:
        model = models.R17


class R17Admin(ImportExportModelAdmin):
    resource_classes = [R17Resource]


class R18Resource(resources.ModelResource):
    class Meta:
        model = models.R18


class R18Admin(ImportExportModelAdmin):
    resource_classes = [R18Resource]


class R19Resource(resources.ModelResource):
    class Meta:
        model = models.R19


class R19Admin(ImportExportModelAdmin):
    resource_classes = [R19Resource]


class R20Resource(resources.ModelResource):
    class Meta:
        model = models.R20


class R20Admin(ImportExportModelAdmin):
    resource_classes = [R20Resource]


class R21Resource(resources.ModelResource):
    class Meta:
        model = models.R21


class R21Admin(ImportExportModelAdmin):
    resource_classes = [R21Resource]


class R22Resource(resources.ModelResource):
    class Meta:
        model = models.R22


class R22Admin(ImportExportModelAdmin):
    resource_classes = [R22Resource]


class R23Resource(resources.ModelResource):
    class Meta:
        model = models.R23


class R23Admin(ImportExportModelAdmin):
    resource_classes = [R23Resource]


class R24Resource(resources.ModelResource):
    class Meta:
        model = models.R24


class R24Admin(ImportExportModelAdmin):
    resource_classes = [R24Resource]


class R25Resource(resources.ModelResource):
    class Meta:
        model = models.R25


class R25Admin(ImportExportModelAdmin):
    resource_classes = [R25Resource]


class BuildDocsAdmin(ImportExportModelAdmin):
    list_display = ('user', 'build')


admin.site.register(models.Regions, RegionAdmin)
admin.site.register(models.Builds, BuildsAdmin)
admin.site.register(models.BuildDocs, BuildDocsAdmin)

admin.site.register(models.R1, R1Admin)
admin.site.register(models.R2, R2Admin)
admin.site.register(models.R3, R3Admin)
admin.site.register(models.R4_R5_R6, R4R5R6Admin)
admin.site.register(models.R7, R7Admin)
admin.site.register(models.R8, R8Admin)
admin.site.register(models.R9, R9Admin)
admin.site.register(models.R10_R11_R13, R10R11R13Admin)
admin.site.register(models.R12, R12Admin)
admin.site.register(models.R14, R14Admin)
admin.site.register(models.R15, R15Admin)
admin.site.register(models.R16, R16Admin)
admin.site.register(models.R17, R17Admin)
admin.site.register(models.R18, R18Admin)
admin.site.register(models.R19, R19Admin)
admin.site.register(models.R20, R20Admin)
admin.site.register(models.R21, R21Admin)
admin.site.register(models.R22, R22Admin)
admin.site.register(models.R23, R23Admin)
admin.site.register(models.R24, R24Admin)
admin.site.register(models.R25, R25Admin)

admin.site.register(models.VR1)
admin.site.register(models.VR2)
admin.site.register(models.VR3)
admin.site.register(models.VR4)
admin.site.register(models.VR5)
admin.site.register(models.VR6)
admin.site.register(models.VR7)
admin.site.register(models.VR8)
admin.site.register(models.VR9)
admin.site.register(models.VR10)
admin.site.register(models.VR11)
admin.site.register(models.VR12)
admin.site.register(models.VR13)
admin.site.register(models.VR14)
admin.site.register(models.VR15)
admin.site.register(models.VR16)
admin.site.register(models.VR17)
admin.site.register(models.VR18)
admin.site.register(models.VR19)
admin.site.register(models.VR20)
admin.site.register(models.VR21)
admin.site.register(models.VR22)
admin.site.register(models.VR23)
admin.site.register(models.VR24)
admin.site.register(models.VR25)