### 1. Descarga manual desde cBioPortal (A prueba de bloqueos)

Dado que las APIs públicas imponen restricciones, obtendremos los archivos base desde su portal oficial en tu navegador.

1. Entra en la página oficial de descargas de cBioPortal: [cBioPortal Datasets](https://www.cbioportal.org/datasets)
    
2. Usa el buscador de la página para localizar tus tres estudios clave y haz clic en el icono de descarga (suele ser un archivo `.tar.gz`):
    
    - Escribe **METABRIC** y descarga el estudio de cáncer de mama.
        
    - Escribe **TCGA PanCancer** y descarga los correspondientes a **Breast Invasive Carcinoma** y **Lung Adenocarcinoma**.
        
3. Crea una carpeta llamada `data` en el mismo directorio donde tienes tu _notebook_ o script de Python.
    
4. Mueve los tres archivos `.tar.gz` descargados dentro de esa carpeta `data`. Asegúrate de que los nombres coincidan con los esperados (ej. `brca_metabric.tar.gz`).
    

---

### 2. Pipeline de Python Actualizado (Extracción y Carga Local)

Con los archivos ya descargados en tu disco duro, este nuevo pipeline se encargará únicamente de descomprimirlos (si no lo has hecho ya) y de cargar de forma segura los archivos clínicos y de expresión en DataFrames de `pandas`.

Hemos eliminado toda la lógica de conexión web para garantizar que el código se ejecute sin problemas.

Python

```
import os
import tarfile
import pandas as pd

def extraer_y_cargar_estudio(study_id, data_dir="data"):
    """
    Descomprime el archivo .tar.gz local y carga los datos de supervivencia y expresión.
    """
    tar_path = os.path.join(data_dir, f"{study_id}.tar.gz")
    extract_path = os.path.join(data_dir, study_id)

    # 1. Extraer si el archivo .tar.gz existe y aún no se ha descomprimido
    if not os.path.exists(extract_path):
        if not os.path.exists(tar_path):
            raise FileNotFoundError(f"No se encontró el archivo: {tar_path}. ¡Asegúrate de descargarlo manualmente en la carpeta '{data_dir}'!")
            
        print(f"Descomprimiendo {study_id}...")
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(path=extract_path)
        print(f"Descompresión completada en {extract_path}")
    else:
        print(f"El estudio {study_id} ya estaba descomprimido.")

    # 2. Cargar datos clínicos (Supervivencia)
    clin_path = os.path.join(extract_path, "data_clinical_patient.txt")
    if not os.path.exists(clin_path):
        # A veces el archivo clínico puede tener un prefijo ligeramente distinto
        clin_file = [f for f in os.listdir(extract_path) if "clinical_patient" in f][0]
        clin_path = os.path.join(extract_path, clin_file)
        
    df_clin = pd.read_csv(clin_path, sep='\t', skiprows=4) 
    
    # 3. Cargar datos de expresión génica
    try:
        # Buscamos dinámicamente el archivo de mRNA
        expr_file = [f for f in os.listdir(extract_path) if "data_mrna" in f and f.endswith(".txt")][0]
        expr_path = os.path.join(extract_path, expr_file)
        print(f"Cargando expresión génica desde: {expr_file} (Esto puede tardar...)")
        df_expr = pd.read_csv(expr_path, sep='\t')
    except IndexError:
        print(f"Advertencia: No se encontró archivo de expresión mRNA (.txt) para {study_id}.")
        df_expr = pd.DataFrame() # Retorna DataFrame vacío para evitar cuelgues
    
    return df_clin, df_expr

# --- EJECUCIÓN DEL PIPELINE LOCAL ---

# Estos nombres deben coincidir con los archivos .tar.gz que descargaste (sin la extensión)
estudios = [
    "brca_metabric", 
    "brca_tcga_pan_can_atlas_2018", 
    "luad_tcga_pan_can_atlas_2018"
]

datos_proyecto = {}
directorio_base = "data"

for estudio in estudios:
    try:
        df_clin, df_expr = extraer_y_cargar_estudio(estudio, data_dir=directorio_base)
        datos_proyecto[estudio] = {'clinico': df_clin, 'expresion': df_expr}
        
        print(f"--- RESULTADOS PARA {estudio.upper()} ---")
        print(f"Pacientes clínicos: {df_clin.shape[0]}")
        print(f"Variables/Sondas de expresión: {df_expr.shape[0] if not df_expr.empty else 0}")
        print("-" * 40)
    except Exception as e:
        print(f"Error procesando {estudio}: {str(e)}\n")
```