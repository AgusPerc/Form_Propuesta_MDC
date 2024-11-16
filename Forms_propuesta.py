import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from io import BytesIO

# Configuración de la página
st.set_page_config(
    page_title="Servicios de Cuidados - Generador de Propuestas",
    page_icon="👥",
    layout="centered"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton button {
        width: 100%;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    .stSelectbox {
        margin-bottom: 1rem;
    }
    .css-1d391kg {
        padding: 2rem;
    }
    .propuesta {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    @media print {
        .no-print {
            display: none;
        }
    }
    </style>
""", unsafe_allow_html=True)

def crear_html_propuesta(nombre, telefono, servicio, tarifa, referencia):
    fecha = datetime.now().strftime("%d de %B de %Y")
    
    html = f"""
    <div class="propuesta">
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #007bff;">SERVICIOS DE CUIDADOS PROFESIONALES</h1>
            <p style="color: #666;">Propuesta generada el {fecha}</p>
        </div>
        
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin-bottom: 2rem;">
            <h2>Propuesta para: {nombre}</h2>
        </div>
        
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin-bottom: 2rem;">
            <h3 style="color: #007bff;">Servicio Seleccionado: {servicio}</h3>
            <p>{get_descripcion_servicio(servicio)}</p>
            <h2 style="color: #28a745;">Tarifa por día: ${tarifa:,}</h2>
        </div>
        
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin-bottom: 2rem;">
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
        
        <div style="background-color: #e9ecef; padding: 1rem; border-radius: 5px; margin-bottom: 2rem;">
            <h3>Información de Contacto</h3>
            <p>Cliente: {nombre}</p>
            <p>Teléfono de contacto: {telefono}</p>
            <p>Nos encontró a través de: {referencia}</p>
        </div>
        
        <div style="text-align: center; margin-top: 2rem; padding-top: 1rem; border-top: 2px solid #007bff;">
            <p style="color: #666;">Esta propuesta es válida por 30 días a partir de la fecha de emisión.</p>
            <p style="color: #666;">Para más información o para programar una consulta, no dude en contactarnos.</p>
            <p style="color: #666;">¡Gracias por confiar en nuestros servicios profesionales de cuidado!</p>
        </div>
    </div>
    """
    return html

def get_descripcion_servicio(servicio):
    descripciones = {
        "Cuidador Auxiliar": "Asistencia en actividades diarias y compañía, brindando apoyo en las tareas cotidianas y garantizando el bienestar del paciente.",
        "Enfermero": "Atención de enfermería profesional y cuidados especializados, incluyendo administración de medicamentos y monitoreo de signos vitales.",
        "Enfermero Especializado": "Cuidados avanzados y monitoreo de condiciones complejas, con experiencia en el manejo de casos que requieren atención médica especializada."
    }
    return descripciones.get(servicio, "")

def download_pdf():
    try:
        # Convertir HTML a PDF usando pdfkit
        import pdfkit
        pdf = pdfkit.from_string(st.session_state.html_propuesta, False)
        return pdf
    except Exception as e:
        st.error(f"Error al generar PDF: {e}")
        return None

def main():
    # Título principal
    st.title("🏥 Generador de Propuestas de Servicios de Cuidados")
    
    # Crear tres columnas para una mejor organización
    col1, col2 = st.columns(2)
    
    with col1:
        # Campos del formulario
        nombre = st.text_input("Nombre del Cliente", key="nombre")
        telefono = st.text_input("Número de Teléfono", key="telefono")
    
    with col2:
        # Opciones de servicio con sus tarifas
        servicios = {
            "Cuidador Auxiliar": 1200,
            "Enfermero": 1500,
            "Enfermero Especializado": 1900
        }
        servicio = st.selectbox("Tipo de Servicio", list(servicios.keys()))
        
        # Opciones de referencia
        referencias = [
            "Recomendación",
            "Redes Sociales",
            "Búsqueda en Google",
            "Publicidad",
            "Otro"
        ]
        referencia = st.selectbox("¿Cómo se enteró de nosotros?", referencias)

    # Botón para generar propuesta
    if st.button("📄 Generar Propuesta"):
        if not nombre or not telefono:
            st.error("Por favor complete todos los campos")
        else:
            # Generar la propuesta
            html_propuesta = crear_html_propuesta(
                nombre,
                telefono,
                servicio,
                servicios[servicio],
                referencia
            )
            
            # Guardar la propuesta en session_state
            st.session_state.html_propuesta = html_propuesta
            
            # Mostrar la propuesta
            st.markdown("### Vista Previa de la Propuesta:")
            st.markdown(html_propuesta, unsafe_allow_html=True)
            
            # Botones para descargar
            col1, col2 = st.columns(2)
            
            with col1:
                # Descargar como HTML
                html_str = html_propuesta
                b64 = base64.b64encode(html_str.encode()).decode()
                href = f'<a href="data:text/html;base64,{b64}" download="propuesta_{nombre.lower().replace(" ", "_")}.html" class="stButton"><button style="background-color: #28a745;">⬇️ Descargar HTML</button></a>'
                st.markdown(href, unsafe_allow_html=True)
            
            with col2:
                # Botón para imprimir
                st.markdown("""
                    <button onclick="window.print()" style="width: 100%; padding: 0.5rem; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">
                        🖨️ Imprimir Propuesta
                    </button>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()