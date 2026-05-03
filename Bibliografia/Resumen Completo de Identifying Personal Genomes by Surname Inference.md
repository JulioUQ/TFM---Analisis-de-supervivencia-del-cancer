**Autor(es):** Melissa Gymrek, Amy L. McGuire, David Golan, Eran Halperin, Yaniv Erlich 
**Fecha de publicación:** 18 de enero de 2013 
**Revista/Editorial:** Science
**Campo/Disciplina:** [[Genética]] [[Bioinformática]] [[Reidentificacion]]
**DOI/Enlace:** [10.1126/science.1229566](https://www.google.com/search?q=http://dx.doi.org/10.1126/science.1229566)

---

### Resumen Ejecutivo

Este estudio demuestra que es posible recuperar los apellidos de individuos a partir de datos genómicos supuestamente anónimos mediante el análisis de repeticiones cortas en tándem del cromosoma Y (Y-STR) y el uso de bases de datos genealógicas recreativas de acceso público. Los autores establecen un método para triangular identidades específicas combinando estos apellidos inferidos con metadatos demográficos no protegidos por leyes de privacidad, como la edad y el estado de residencia. La investigación concluye que esta técnica representa un riesgo real para la privacidad en los conjuntos de datos genómicos públicos, habiendo identificado con éxito a varios participantes de proyectos de secuenciación de alto perfil.

### Pregunta de Investigación y Objetivos

El estudio busca investigar con qué facilidad se pueden inferir apellidos en una población general y demostrar la identificación de extremo a extremo de individuos utilizando únicamente información pública. Los objetivos específicos incluyen:

- Analizar cuantitativamente la probabilidad de identificación de varones en EE. UU. mediante la inferencia de apellidos.
    
- Evaluar la viabilidad de producir haplotipos Y-STR precisos a partir de tecnologías de secuenciación masiva (Illumina).
    
- Demostrar la técnica rastreando las identidades de participantes en proyectos de secuenciación pública.
    

### Argumento Central o Hipótesis

La premisa central es que los apellidos se heredan de forma patrilineal en la mayoría de las sociedades, lo que resulta en su co-segregación con los haplotipos del cromosoma Y. Debido a que las bases de datos genealógicas recreativas han acumulado cientos de miles de registros que vinculan estos haplotipos con apellidos, un genoma personal de un varón "anónimo" puede ser consultado en estos recursos gratuitos para revelar su identidad familiar y, eventualmente, su identidad individual mediante triangulación demográfica.

### Hallazgos y Conclusiones Clave

- **Tasa de éxito:** Se proyecta una tasa de recuperación exitosa de apellidos del **12% ($\pm2\%$)** para varones caucásicos en EE. UU. con una tasa de error del 5%.
    
- **Eficacia de la triangulación:** Mientras que la edad y el estado por sí solos coinciden con al menos 60,000 varones en el 50% de los casos, añadir el apellido reduce la lista mediana a solo **12 individuos**, facilitando la investigación individual.
    
- **Identificación real:** Los investigadores lograron identificar plenamente a 5 individuos de tres pedigríes de la colección CEU y a sus familias extendidas (casi 50 personas en total).
    
- **Accesibilidad:** La técnica no requiere acceso a bases de datos gubernamentales o privadas, basándose enteramente en recursos de Internet gratuitos.
    

### Metodología y Datos

- **Bases de datos consultadas:** Se utilizaron principalmente **Ysearch** y **SMGF**, que contienen aproximadamente 39,000 apellidos únicos en 135,000 registros.
    
- **Validación de algoritmos:** Se utilizó una cohorte de 911 individuos con apellidos conocidos de la base de datos **YBase** para probar un algoritmo de recuperación basado en el ancestro común más reciente (TMRCA).
    
- **Procesamiento genómico:** Se empleó el algoritmo **lobSTR** para perfilar STRs a partir de lecturas de secuenciación de Illumina.
    
- **Muestras de prueba:** Se analizaron genomas públicos de figuras conocidas como Craig Venter, John West y Michael Snyder, además de 32 genomas de la cohorte CEU (Utah) del Proyecto 1000 Genomas.
    

### Marco Teórico

El estudio se apoya en la genética de poblaciones y la genealogía genética. Utiliza la relación establecida entre la genética del cromosoma Y y la onomástica (estudio de los nombres). El marco analítico se basa en la teoría de la **triangulación de identidad**, donde múltiples puntos de datos no identificables por sí mismos (haplotipo, edad, estado) se vuelven identificables cuando se intersectan.

### Resultados e Interpretación

- **Craig Venter:** La búsqueda de su haplotipo devolvió el apellido "Venter" como coincidencia exacta; la combinación con su año de nacimiento (1946) y estado (California) redujo los resultados a solo dos varones, uno de los cuales era él.
    
- **Población CEU:** Se recuperaron apellidos con alta confianza en individuos de Utah debido al gran interés de esta población por la genealogía y el tamaño de sus familias, lo que aumenta exponencialmente la probabilidad de que un pariente lejano haya subido datos a la red.
    
- **Conexiones distantes:** La identificación fue posible incluso cuando los individuos estaban separados por **2 a 7 eventos de meiosis** (generaciones) de la persona que originalmente proporcionó el registro a la base de datos genealógica.
    

### Limitaciones y Críticas

- **Sesgo demográfico:** Los resultados son aplicables principalmente a grupos socioeconómicos con alta participación en servicios genealógicos, específicamente varones caucásicos de clase media y alta en EE. UU..
    
- **Factores de confusión:** La relación entre apellidos y haplotipos puede verse alterada por eventos de no-paternidad, mutaciones o adopciones.
    
- **Baja cobertura:** Algunos genomas secuenciados a baja profundidad (<5x) produjeron haplotipos demasiado dispersos para una recuperación exitosa.
    

### Contexto Académico

El trabajo se basa en advertencias previas de investigadores como **Lunshof et al.**, quienes especularon sobre este riesgo, y **Gitschier**, quien demostró empíricamente que se podían detectar apellidos potenciales en la cohorte CEU. Este artículo amplía esos trabajos al demostrar por primera vez la identificación completa a nivel de una sola persona.

### Implicaciones Prácticas y Teóricas

- **Seguridad de datos:** El estudio pone en duda la efectividad del "anonimato" mediante la simple eliminación de identificadores directos.
    
- **Políticas de privacidad:** Tras los hallazgos de este estudio, los Institutos Nacionales de Salud (NIH) de EE. UU. eliminaron información sobre edades de bases de datos públicas para mitigar riesgos.
    
- **Recomendaciones:** Los autores no sugieren detener el intercambio de datos, sino establecer políticas claras, educar a los participantes sobre los riesgos y legislar contra el uso indebido de la información genética.