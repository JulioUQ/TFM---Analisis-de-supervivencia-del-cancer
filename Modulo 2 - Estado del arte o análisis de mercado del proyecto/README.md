# Módulo 2 — Estado del arte o análisis de mercado del proyecto

Este módulo contiene la revisión del estado del arte del TFM **“Supervivencia en Cáncer de Mama y Pulmón: Identificación de Biomarcadores Genómicos Pronósticos mediante Modelos Estadísticos Avanzados y Validación Cruzada en Cohortes Independientes”**.

El capítulo revisa la literatura científica relacionada con el análisis de supervivencia en oncología de precisión, con especial atención a modelos estadísticos, machine learning, deep learning, datos genómicos, cohortes públicas y estrategias de validación externa.

## Objetivo del módulo

El objetivo del Módulo 2 es construir el marco teórico y metodológico del TFM. Para ello, se revisan:

- la evolución histórica de los métodos de análisis de supervivencia;
- los modelos clásicos, de machine learning y de deep learning aplicados a datos censurados;
- el papel de los datos genómicos en la predicción del pronóstico oncológico;
- el estado del arte en cáncer de mama y cáncer de pulmón no microcítico;
- las cohortes TCGA, METABRIC y otras fuentes relevantes;
- las métricas habituales de evaluación;
- las brechas metodológicas que justifican el diseño experimental del TFM.

## Contenido principal del capítulo

El documento del Módulo 2 está estructurado en las siguientes secciones:

1. **Introducción al capítulo**
   - Contextualización del análisis de supervivencia en oncología de precisión.
   - Definición del enfoque de revisión documental.
   - Bases de datos y palabras clave utilizadas para la búsqueda bibliográfica.

2. **Evolución histórica de los métodos de supervivencia**
   - Kaplan-Meier.
   - Modelo de riesgos proporcionales de Cox.
   - Cox-LASSO.
   - Random Survival Forest.
   - DeepSurv y arquitecturas modernas.

3. **Machine learning para supervivencia**
   - Motivación del enfoque.
   - Random Survival Forest.
   - Gradient boosting para supervivencia.
   - Ventajas y limitaciones frente a modelos clásicos.

4. **Deep learning para supervivencia**
   - DeepSurv.
   - SurvivalNet.
   - Modelos multimodales y autoencoders.
   - Limitaciones de interpretabilidad y sobreajuste.

5. **Datos genómicos en predicción pronóstica**
   - TCGA.
   - METABRIC.
   - Expresión génica, mutaciones, CNV, metilación y datos clínicos.
   - Retos derivados de la alta dimensionalidad.

6. **Estado del arte en cáncer de mama**
   - Subtipos moleculares.
   - Herramientas pronósticas basadas en firmas génicas.
   - Estudios con TCGA-BRCA y METABRIC.

7. **Estado del arte en cáncer de pulmón no microcítico**
   - Heterogeneidad molecular.
   - Mutaciones y biomarcadores relevantes.
   - Modelos predictivos y estudios multi-ómicos.

8. **Validación cruzada entre conjuntos de datos**
   - Importancia de la validación externa.
   - Diferencias entre TCGA-BRCA y METABRIC.
   - Estrategias de armonización entre plataformas.

9. **Métricas de evaluación**
   - C-index.
   - Brier Score integrado.
   - Log-rank test.
   - Estratificación de riesgo.

10. **Síntesis comparativa y brechas de conocimiento**
    - Comparación por familias metodológicas.
    - Tabla resumen global.
    - Justificación metodológica del TFM.

## Estructura del directorio

```text
Modulo 2 - Estado del arte o análisis de mercado del proyecto/
├── Figuras y graficos/
│   └── Figuras utilizadas en el capítulo y versiones exportadas
├── Informacion complementaria/
│   └── Material auxiliar, lecturas, notas o recursos de apoyo
├── Versiones/
│   └── Versiones intermedias del capítulo
├── Comentarios tutor sobre V1-EstadoDelArte.md
├── TFM_Capitulo2_EstadoDelArte_completo.docx
├── TFM_Capitulo2_EstadoDelArte_completo.pdf
└── README.md
```

## Ficheros principales

| Fichero | Descripción |
|---|---|
| `TFM_Capitulo2_EstadoDelArte_completo.docx` | Versión editable del capítulo 2 |
| `TFM_Capitulo2_EstadoDelArte_completo.pdf` | Versión exportada para revisión o entrega |
| `Comentarios tutor sobre V1-EstadoDelArte.md` | Comentarios recibidos y puntos de mejora |
| `Figuras y graficos/` | Figuras metodológicas y comparativas |
| `Informacion complementaria/` | Documentación auxiliar |
| `Versiones/` | Histórico de versiones |

## Ideas clave del estado del arte

El capítulo identifica varias conclusiones que orientan el diseño del TFM:

- La validación externa sigue siendo limitada en muchos estudios de modelos predictivos oncológicos.
- Las comparaciones sistemáticas entre familias de modelos son escasas.
- La heterogeneidad de pipelines de preprocesamiento dificulta la comparación entre estudios.
- La validación cruzada entre TCGA-BRCA y METABRIC es especialmente relevante por sus diferencias de plataforma.
- La interpretabilidad de modelos complejos como DeepSurv requiere técnicas complementarias, como SHAP.
- Los modelos clásicos siguen siendo útiles como referencia, pero los enfoques no lineales pueden capturar interacciones clínicas y moleculares más complejas.

## Relación con el resto del TFM

Este módulo justifica las decisiones desarrolladas en el Módulo 3:

| Decisión del TFM | Fundamentación en el Módulo 2 |
|---|---|
| Uso de Kaplan-Meier | Baseline descriptivo ampliamente aceptado |
| Uso de Cox-LASSO | Modelo interpretable y útil en alta dimensionalidad |
| Uso de Random Survival Forest | Modelo robusto para no linealidad e interacciones |
| Uso de DeepSurv | Representante principal de deep learning en supervivencia |
| Métricas C-index e IBS | Evaluación de discriminación y calibración |
| Validación externa METABRIC ↔ TCGA-BRCA | Brecha metodológica detectada en la literatura |
| Interpretabilidad | Necesidad de traducir resultados a variables clínicas o biológicas |

## Flujo de trabajo recomendado para revisar el módulo

1. Leer primero el PDF completo del capítulo.
2. Revisar los comentarios del tutor.
3. Comprobar que cada afirmación relevante está respaldada por bibliografía.
4. Verificar la coherencia entre tablas, figuras y texto.
5. Revisar que las brechas de conocimiento conectan directamente con los objetivos del TFM.
6. Actualizar las figuras en `Figuras y graficos/` si se modifican tablas o conclusiones.
7. Mantener las versiones antiguas en `Versiones/` para trazabilidad.

## Convenciones de documentación

Se recomienda mantener:

- nombres de archivo claros y sin ambigüedad;
- versiones antiguas separadas del documento principal;
- comentarios del tutor en Markdown para facilitar seguimiento;
- figuras exportadas en formato reutilizable (`.png`, `.svg` o `.pdf`);
- referencias bibliográficas verificadas en fuentes académicas.

## Estado del módulo

El Módulo 2 funciona como base teórica para la implementación posterior. Su contenido debe permanecer alineado con los modelos y métricas realmente utilizados en el Módulo 3. Si se añade, elimina o modifica algún modelo en el análisis experimental, conviene actualizar este capítulo para evitar inconsistencias entre la revisión bibliográfica y la implementación.