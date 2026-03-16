

**Autor(es):** Cyriac Kandoth, Michael D. McLellan, Fabio Vandin, Kai Ye, Beifang Niu, Charles Lu, Mingchao Xie, Qunyuan Zhang, Joshua F. McMichael, Matthew A. Wyczalkowski, Mark D. M. Leiserson, Christopher A. Miller, John S. Welch, Matthew J. Walter, Michael C. Wendl, Timothy J. Ley, Richard K. Wilson, Benjamin J. Raphael y Li Ding. 
**Fecha de publicación:** 17 de octubre de 2013. 
**Revista/Editorial:** Nature. 
**Campo/Disciplina:** Genómica del Cáncer / Oncología. 
**DOI/Enlace:** 10.1038/nature12634.

---

### Resumen Ejecutivo

Este artículo presenta un análisis sistemático e integrado de mutaciones puntuales y pequeñas inserciones/deleciones en 3281 tumores de 12 tipos de cáncer, en el marco del proyecto Pan-Cancer de The Cancer Genome Atlas (TCGA). Los investigadores identifican 127 genes significativamente mutados (SMGs) en diversos procesos celulares, correlacionan estas mutaciones con resultados clínicos y mapean su trayectoria temporal dentro de la arquitectura clonal del tumor.

### Pregunta de Investigación y Objetivos

El estudio busca comprender los mecanismos subyacentes de la iniciación y progresión del cáncer mediante la evaluación de las similitudes y diferencias mutacionales entre 12 tipos distintos de cáncer. El objetivo principal es establecer vínculos entre la frecuencia y el contexto de las mutaciones con los tejidos de origen, factores ambientales, defectos en la reparación del ADN y la arquitectura clonal.

### Argumento Central o Hipótesis

El argumento central es que el análisis sistemático e integrado de grandes conjuntos de datos genómicos a través de múltiples tipos de tumores permite identificar un conjunto básico de genes y vías conductoras (drivers) del cáncer. Los autores sostienen que comprender esta arquitectura clonal y las mutaciones específicas de cada paciente es fundamental para el desarrollo de nuevos diagnósticos y la individualización del tratamiento oncológico.

### Hallazgos y Conclusiones Clave

- El análisis identificó 127 genes significativamente mutados (SMGs) implicados en una amplia gama de procesos celulares, incluyendo la señalización de quinasas, el control del ciclo celular y la modificación de histonas.
    
- La mayoría de los tumores presentan únicamente entre dos y seis mutaciones en estos SMGs, lo que indica que el número de mutaciones conductoras requeridas durante la oncogénesis es relativamente pequeño.
    
- El gen TP53 es el más frecuentemente mutado en toda la cohorte (presente en el 42% de las muestras).
    
- Las tasas de mutación varían significativamente según el tipo de cáncer; la leucemia mieloide aguda (LAML) presenta la frecuencia mediana más baja (0.28 mutaciones por megabase), mientras que el carcinoma escamoso de pulmón (LUSC) presenta la más alta (8.15 mutaciones por megabase).
    
- Las mutaciones en genes como BAP1, FBXW7 y TP53 se asocian de manera significativa con fenotipos perjudiciales y una peor supervivencia en varios tipos de cáncer.
    
- El análisis de la fracción alélica variante revela que mutaciones en genes como TP53 y DNMT3A tienden a aparecer temprano en la tumorigénesis (clon fundador), mientras que mutaciones en genes como KRAS y NRAS a menudo actúan como eventos de progresión en subclones.
    

### Metodología y Datos

El estudio procesó datos de secuenciación de exomas de 3281 tumores emparejados con tejido normal para identificar mutaciones somáticas a través de 12 tipos de cáncer. Se aplicaron filtros estrictos para asegurar la calidad, resultando en 617,354 mutaciones somáticas (mutaciones puntuales e indels cortos). Para la significancia estadística, se utilizó el paquete "MuSiC" para identificar SMGs. Las relaciones de co-ocurrencia y exclusividad se evaluaron mediante la prueba exacta de Fisher y el algoritmo Dendrix. El análisis de supervivencia se realizó con modelos de riesgos proporcionales de Cox. La arquitectura clonal se infirió utilizando las frecuencias alélicas variantes (VAF) y el algoritmo sciClone.

### Marco Teórico

El artículo se fundamenta en la teoría de la evolución somática del cáncer, que postula que las células tumorales adquieren mutaciones genéticas a lo largo del tiempo, experimentando una selección positiva para mutaciones "conductoras" (drivers) que otorgan ventajas de crecimiento o supervivencia. También se apoya en el concepto de heterogeneidad tumoral y evolución clonal para trazar la temporalidad de estas alteraciones.

### Resultados e Interpretación

El análisis del contexto de la secuencia reveló firmas mutacionales asociadas con factores ambientales, como el aumento de transversiones C>A en el cáncer de pulmón, indicativo de la exposición al humo del cigarrillo. Los análisis de agrupamiento mostraron que los tumores frecuentemente se agrupan por su tejido de origen basándose en el estado de mutación de los SMG (72% de los tumores), aunque existen solapamientos impulsados por mutaciones comunes como TP53. Los modelos de supervivencia indicaron que el impacto clínico de ciertas mutaciones varía según el tipo de tejido; por ejemplo, las mutaciones de BRCA2 se asocian con una mejor supervivencia en el cáncer de ovario, pero genes como BAP1 indican un mal pronóstico cruzando varios tipos de cáncer.

### Limitaciones y Críticas

Los propios autores señalan que los reordenamientos estructurales a gran escala no se incluyeron en este análisis, lo cual es una limitación en la comprensión total del panorama mutacional. Además, la resolución de los análisis de agrupamiento podría mejorarse si se incorporaran datos de número de copias, variantes estructurales, expresión génica, proteómica y metilación. El artículo no estratificó a los pacientes con leucemia mieloide aguda basándose en citogenética o en el estado de duplicación en tándem interna de FLT3 para el análisis de supervivencia de NPM1, lo que impide discernir efectos específicos en esa subpoblación.

### Contexto Académico

Este trabajo expande significativamente los estudios previos sobre genómica del cáncer al integrar datos en un formato "Pan-Cancer", en contraste con los estudios tradicionales centrados en un solo tipo de tejido. Validó descubrimientos previos sobre vías clásicas del cáncer (MAPK, PI3K) y destacó procesos celulares emergentes como la modificación de histonas y el splicing de ARN. Además, 66 de los genes identificados se superponen con la lista de genes conductores generada mediante métodos basados en la base de datos COSMIC, reforzando la fiabilidad de los hallazgos.

### Implicaciones Prácticas y Teóricas

A nivel teórico, el estudio confirma que la iniciación y progresión del cáncer dependen de un número sorprendentemente bajo de mutaciones clave y resalta la importancia de la evolución clonal. En la práctica clínica, los hallazgos proporcionan un marco para formular paneles de genes de referencia útiles para el diagnóstico y el pronóstico en varios puntos de intervención clínica. Además, subraya que conocer la estructura clonal del tumor de un paciente será fundamental para optimizar los tratamientos personalizados.

---
