from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from core.models import Papeleta, Empleado
from django.contrib.auth.decorators import login_required

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error_message = 'Correo electrónico o contraseña incorrectos'
    else:
        error_message = ''

    return render(request, 'admin_login.html', {'error_message': error_message})

@login_required
def obtener_Empleado_por_Agente(request):
    AgenteA_id = request.GET.get('AgenteA_id')
    empleados = Empleado.objects.filter(Papeleta__AgenteA_id=AgenteA_id, estado="A").order_by('usuario__apellidoPaterno')
    
    empleados_list = [{'id': empleado.id, 'nombre_completo': empleado.usuario.nombre_completos().upper()} for empleado in empleados]
    
    return JsonResponse({'empleados': empleados_list})

@login_required
def generar_PDF_papeleta(request):
    AgenteA = Papeleta.objects.filter(matricula__isnull=False).distinct()
    empleado = Empleado.objects.all()
    
    AgenteA_id = request.POST.get('agenteA_papeleta')
    empleado_id = request.POST.get('empleado_papeleta')
    
    Papeletas = Papeletas.objects.none()  # Crear un queryset vacío
    
    if AgenteA_id or empleado_id:
        # Aplicar los filtros solo si se proporciona al menos uno de los parámetros
        Papeletas = Papeleta.objects.all()
        
        if AgenteA_id:
            Papeletas = Papeletas.filter(AgenteA_id=AgenteA_id)
            empleado = empleado.filter(id=empleado_id, AgenteA_id=AgenteA_id)
            
        if empleado_id:
            Papeletas = Papeletas.filter(empleado_id=empleado_id).distinct()

       
    
    boletas_disponibles = Papeletas.exists()

    contexto = {
        'AgenteAs': AgenteA,
        'Papeletas': Papeletas,
        'boletas_disponibles': boletas_disponibles,
        'empleado_nombre': empleado,
        'AgenteA_id': AgenteA_id,
        'empleado_id': empleado_id,
        # Agrega aquí los demás datos necesarios para el template
    }

    return render(request, 'reporte_papeletas.html', contexto)

def generar_pdf_papeleta(request):
    papeleta_id = request.GET.get('papeleta_id')

    # Obtener la papeleta
    try:
        papeleta = Papeleta.objects.get(id=papeleta_id)
    except Papeleta.DoesNotExist:
        # Maneja el caso en que la papeleta no existe
        return HttpResponse('La papeleta no existe')

    # Crear un objeto HttpResponse con el encabezado PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=papeleta_{papeleta_id}.pdf'

    # Crear un objeto PDF usando reportlab
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Crear una lista para almacenar los elementos que se agregarán al PDF
    elements = []

    # Agregar el encabezado
    elements.append("Papeleta de {}".format(papeleta.AgenteA.nombre_completo()))

    # Crear una tabla para mostrar la información de la papeleta
    data = [
        ["Área:", papeleta.Area],
        ["Tipo de Papeleta:", papeleta.tipoPapeleta.nombre],
        ["Fecha de Registro:", str(papeleta.fechaRegistro)],
        # Agrega más campos de la papeleta según sea necesario
    ]

    # Estilo de la tabla
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Crea la tabla y aplica el estilo
    tabla = Table(data, colWidths=[100, 300])
    tabla.setStyle(table_style)

    # Agrega la tabla a la lista de elementos
    elements.append(tabla)

    # Crea el PDF con los elementos
    doc.build(elements)

    # Obtén el valor del buffer y escríbelo en la respuesta
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
