from django.contrib import admin
from .models import TipoDeSancion, TipoDePapeleta, TipoEmpleado, TipoDocumento, CustomUser, Empleado, AgenteAeroportuario, Papeleta, Descargo, Sancion

# Registra tus modelos aquí

@admin.register(TipoDeSancion)
class TipoDeSancionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado')

@admin.register(TipoDePapeleta)
class TipoDePapeletaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado')

@admin.register(TipoEmpleado)
class TipoEmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado')

@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'primerNombre', 'apellidoPaterno', 'segundoNombre', 'apellidoMaterno', 'is_staff', 'is_active')

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'tipoEmpleado', 'Cargo', 'estado')

@admin.register(AgenteAeroportuario)
class AgenteAeroportuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'CodAgente')

@admin.register(Papeleta)
class PapeletaAdmin(admin.ModelAdmin):
    list_display = ('AgenteA', 'empleado', 'Area', 'tipoPapeleta', 'fechaRegistro')

@admin.register(Descargo)
class DescargoAdmin(admin.ModelAdmin):
    list_display = ('papeleta', 'empleado', 'descripcion')

@admin.register(Sancion)
class SancionAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'tipoSancion', 'descripcion')
