from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group,Permission

# Opciones para estados
Es1 = 'A'
Es2 = 'I'
ESTADO_OFERTA = [
    (Es1, 'Activo'),
    (Es2, 'Inactivo')
]

class TipoDeSancion(models.Model):

    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')    

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Tipos de Sanciones"

class TipoDePapeleta(models.Model):

    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')    

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Tipos de Papeletas"

class TipoEmpleado(models.Model):

    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')    

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Tipos de Empleados"

class TipoDocumento(models.Model):

    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')    

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Tipos de Documentos"

class UsuarioManager(BaseUserManager):

    def create_user(self, email, primerNombre, apellidoPaterno, segundoNombre, apellidoMaterno, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        if not primerNombre:
            raise ValueError('El usuario debe tener un primer nombre')
        if not segundoNombre:
            raise ValueError('El usuario debe tener un segundo nombre')        
        if not apellidoPaterno:
            raise ValueError('El usuario debe tener un apellido paterno')
        if not apellidoMaterno:
            raise ValueError('El usuario debe tener un apellido materno')

        user = self.model(
            email=self.normalize_email(email),
            primerNombre=primerNombre,
            segundoNombre=segundoNombre,
            apellidoPaterno=apellidoPaterno,
            apellidoMaterno=apellidoMaterno
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, primerNombre, segundoNombre,apellidoPaterno,apellidoMaterno, password):
        user = self.create_user(
            email=self.normalize_email(email),
            primerNombre=primerNombre,
            segundoNombre=segundoNombre,
            apellidoPaterno=apellidoPaterno,
            apellidoMaterno=apellidoMaterno,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=100, unique=True, error_messages={'unique': 'Este correo electrónico ya está en uso.'})
    nacionalidad = models.CharField(max_length=100)
    tipoDocumento = models.ForeignKey(TipoDocumento, null=True, on_delete=models.SET_NULL)
    numeroDocumento = models.CharField(max_length=100, unique=True, error_messages={'unique': 'Este DNI ya está en uso.'})   
    direccion = models.CharField(max_length=200)    
    primerNombre = models.CharField(max_length=100)
    segundoNombre = models.CharField(max_length=100, null=True, blank=True)
    apellidoPaterno = models.CharField(max_length=100)
    apellidoMaterno = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15) 
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)     
  
    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['primerNombre', 'segundoNombre', 'apellidoPaterno', 'apellidoMaterno']

    groups = models.ManyToManyField(
        Group,
        related_name='custom_users',  # Cambia este nombre
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_users_permissions',  # Cambia este nombre
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def nombre_completos(self):
        if self.segundoNombre:
            return "{} {} {} {}".format(self.apellidoPaterno, self.apellidoMaterno, self.primerNombre, self.segundoNombre)
        else:
            return "{} {} {}".format(self.apellidoPaterno, self.apellidoMaterno, self.primerNombre)

    def __str__(self):
        return self.nombre_completos()
  
    class Meta:
        verbose_name_plural = "Usuarios"

class Empleado(models.Model):

    usuario = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    tipoEmpleado = models.ForeignKey(TipoEmpleado, null=True, on_delete=models.SET_NULL)
    Cargo = models.CharField(max_length=100)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    
    def nombre_completo(self):
        return "{} {} {} {}, {}".format(self.usuario.apellidoPaterno, self.usuario.apellidoMaterno, self.usuario.primerNombre, self.usuario.segundoNombre, self.Cargo)

    def __str__(self):
        return self.nombre_completo()

    class Meta:
        verbose_name_plural = "Empleados"

class AgenteAeroportuario(models.Model):

    usuario = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)    
    CodAgente = models.CharField(max_length=10)
    
    def nombre_completo(self):
        return "{} {} {} {}, {}".format(self.usuario.apellidoPaterno, self.usuario.apellidoMaterno, self.usuario.primerNombre, self.usuario.segundoNombre, self.CodAgente)

    def __str__(self):
        return self.nombre_completo()

    class Meta:
        verbose_name_plural = "Agentes Aeroportuarios"

class Papeleta(models.Model):
    AgenteA = models.ForeignKey(AgenteAeroportuario, null=True, on_delete=models.SET_NULL)
    empleado = models.ForeignKey(Empleado, null=True, on_delete=models.SET_NULL)
    Area = models.CharField(max_length=20)
    tipoPapeleta = models.ForeignKey(TipoDePapeleta, null=True, on_delete=models.SET_NULL)
    fechaRegistro = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = "Papeletas"

class Descargo(models.Model):
    papeleta = models.ForeignKey(Papeleta, null=True, on_delete=models.SET_NULL)
    empleado = models.ForeignKey(Empleado, null=True, on_delete=models.SET_NULL)
    descripcion = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Descargos"

class Sancion(models.Model):
    empleado = models.ForeignKey(Empleado, null=True, on_delete=models.SET_NULL)
    tipoSancion = models.ForeignKey(TipoDeSancion, null=True, on_delete=models.SET_NULL)
    descripcion = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Sanciones"

