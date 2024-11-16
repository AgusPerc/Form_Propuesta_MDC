import streamlit as st
import pandas as pd
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io

# Configuración de la página
st.set_page_config(
    page_title="Servicios de Cuidados - Generador de Propuestas",
    page_icon="👥",
    layout="wide"
)

# Estilos CSS mejorados con diseño responsivo
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Roboto', sans-serif;
        box-sizing: border-box;
    }
    
    .main {
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    .stButton button {
        width: 100%;
        background-color: #0066cc !important;
        color: white !important;
        font-weight: 500;
        padding: 0.75rem !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #0052a3 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stSelectbox {
        margin-bottom: 1.5rem;
    }
    
    .propuesta {
        background-color: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .servicio-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #0066cc;
    }
    
    .tarifa {
        font-size: 1.5rem;
        color: #28a745;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .contacto-info {
        background-color: #e9ecef;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
    }
    
    .footer {
        text-align: center;
        padding: 1.5rem;
        border-top: 2px solid #0066cc;
        margin-top: 2rem;
    }
    
    @media (max-width: 768px) {
        .propuesta {
            padding: 1rem;
        }
        
        .servicio-card {
            padding: 1rem;
        }
        
        .tarifa {
            font-size: 1.25rem;
        }
    }
    
    /* Ocultar elementos en la impresión */
    @media print {
        .stButton, .stSelectbox, .streamlit-expanderHeader {
            display: none !important;
        }
        
        .propuesta {
            box-shadow: none;
            padding: 0;
        }
    }
    </style>
""", unsafe_allow_html=True)

def crear_pdf(nombre, telefono, servicio, tarifa, referencia):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Estilo personalizado para el título
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0066cc'),
        spaceAfter=30,
        alignment=1
    )
    
    # Título
    story.append(Paragraph("SERVICIOS DE CUIDADOS PROFESIONALES", titulo_style))
    story.append(Spacer(1, 20))
    
    # Fecha
    fecha = datetime.now().strftime("%d de %B de %Y")
    story.append(Paragraph(f"Propuesta generada el {fecha}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Información del cliente
    story.append(Paragraph(f"<b>Cliente:</b> {nombre}", styles['Normal']))
    story.append(Paragraph(f"<b>Teléfono:</b> {telefono}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Servicio seleccionado
    story.append(Paragraph(f"<b>Servicio Seleccionado:</b> {servicio}", styles['Normal']))
    story.append(Paragraph(f"<b>Descripción:</b> {get_descripcion_servicio(servicio)}", styles['Normal']))
    story.append(Paragraph(f"<b>Tarifa por día:</b> ${tarifa:,}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Servicios incluidos
    servicios_incluidos = [
        ["✓", "Atención personalizada las 24 horas del día"],
        ["✓", "Personal altamente capacitado y certificado"],
        ["✓", "Protocolos estrictos de higiene y seguridad"],
        ["✓", "Seguimiento y reportes detallados"],
        ["✓", "Coordinación con profesionales de la salud"],
        ["✓", "Plan de cuidados personalizado"],
        ["✓", "Asistencia en emergencias"]
    ]
    
    tabla = Table(servicios_incluidos, colWidths=[30, 450])
    tabla.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    story.append(Paragraph("<b>Nuestros Servicios Incluyen:</b>", styles['Normal']))
    story.append(Spacer(1, 10))
    story.append(tabla)
    
    # Pie de página
    story.append(Spacer(1, 30))
    story.append(Paragraph("Esta propuesta es válida por 30 días a partir de la fecha de emisión.", styles['Normal']))
    story.append(Paragraph("Para más información o para programar una consulta, no dude en contactarnos.", styles['Normal']))
    story.append(Paragraph("¡Gracias por confiar en nuestros servicios profesionales de cuidado!", styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def get_descripcion_servicio(servicio):
    descripciones = {
        "Auxiliar de Enfermería": "Asistencia en actividades diarias, cuidados básicos y acompañamiento, brindando apoyo en las tareas cotidianas y garantizando el bienestar del paciente.",
        "Enfermero": "Atención de enfermería profesional y cuidados especializados, incluyendo administración de medicamentos, monitoreo de signos vitales y manejo de procedimientos de mayor complejidad."
    }
    return descripciones.get(servicio, "")

def main():
    st.title("🏥 Generador de Propuestas de Servicios de Cuidados")
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre del Cliente", key="nombre")
            telefono = st.text_input("Número de Teléfono", key="telefono")
        
        with col2:
            servicios = {
                "Auxiliar de Enfermería": 1200,
                "Enfermero": 1500
            }
            servicio = st.selectbox("Tipo de Servicio", list(servicios.keys()))
            
            referencias = [
                "Recomendación",
                "Redes Sociales",
                "Búsqueda en Google",
                "Publicidad",
                "Otro"
            ]
            referencia = st.selectbox("¿Cómo se enteró de nosotros?", referencias)

    if st.button("📄 Generar Propuesta"):
        if not nombre or not telefono:
            st.error("Por favor complete todos los campos")
        else:
            # Generar PDF
            pdf_buffer = crear_pdf(
                nombre,
                telefono,
                servicio,
                servicios[servicio],
                referencia
            )
            
            # Mostrar botón de descarga
            st.download_button(
                label="⬇️ Descargar PDF",
                data=pdf_buffer,
                file_name=f"propuesta_{nombre.lower().replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
            
            # Mostrar vista previa
            st.markdown("### Vista Previa de la Propuesta:")
            
            st.markdown(f"""
            <div class="propuesta">
                <div style="text-align: center; margin-bottom: 2rem;">
                    <h1 style="color: #0066cc;">SERVICIOS DE CUIDADOS PROFESIONALES</h1>
                    <p style="color: #666;">Propuesta generada el {datetime.now().strftime("%d de %B de %Y")}</p>
                </div>
                
                <div class="servicio-card">
                    <h2>Propuesta para: {nombre}</h2>
                </div>
                
                <div class="servicio-card">
                    <h3 style="color: #0066cc;">Servicio Seleccionado: {servicio}</h3>
                    <p>{get_descripcion_servicio(servicio)}</p>
                    <div class="tarifa">Tarifa por día: ${servicios[servicio]:,}</div>
                </div>
                
                <div class="servicio-card">
                    <h3>Nuestros Servicios Incluyen:</h3>
                    <ul style="list-style-type: none; padding-left: 0;">
                        <li style="margin: 0.5rem 0;">✓ Atención personalizada las 24 horas del día</li>
                        <li style="margin: 0.5rem 0;">✓ Personal altamente capacitado y certificado</li>
                        <li style="margin: 0.5rem 0;">✓ Protocolos estrictos de higiene y seguridad</li>
                        <li style="margin: 0.5rem 0;">✓ Seguimiento y reportes detallados</li>
                        <li style="margin: 0.5rem 0;">✓ Coordinación con profesionales de la salud</li>
                        <li style="margin: 0.5rem 0;">✓ Plan de cuidados personalizado</li>
                        <li style="margin: 0.5rem 0;">✓ Asistencia en emergencias</li>
                    </ul>
                </div>
                
                <div class="contacto-info">
                    <h3>Información de Contacto</h3>
                    <p>Cliente: {nombre}</p>
                    <p>Teléfono de contacto: {telefono}</p>
                    <p>Nos encontró a través de: {referencia}</p>
                </div>
                
                <div class="footer">
                    <p style="color: #666;">Esta propuesta es válida por 30 días a partir de la fecha de emisión.</p>
                    <p style="color: #666;">Para más información o para programar una consulta, no dude en contactarnos.</p>
                    <p style="color: #666;">¡Gracias por confiar en nuestros servicios profesionales de cuidado!</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
