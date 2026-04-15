
**Título:** Explainable AI in Clinical Decision Support Systems: A Meta-Analysis of Methods, Applications, and Usability Challenges **Autor(es):** Qaiser Abbas, Woonyoung Jeong y Seung Won Lee 
**Fecha de publicación:** 29 de agosto de 2025 
**Revista/Editorial:** Healthcare (MDPI) 
**Campo/Disciplina:** [[Inteligencia Artificial]],[[ Sistemas de Soporte a la Decisión Clínica]] , [[Informática Médica]]
**DOI/Enlace:** [https://doi.org/10.3390/healthcare13172154](https://doi.org/10.3390/healthcare13172154)

---

### Resumen Ejecutivo

Este estudio es una revisión sistemática y metaanálisis que sintetiza los hallazgos de 62 estudios revisados por pares publicados entre 2018 y 2025 sobre el uso de la Inteligencia Artificial Explicable (XAI) en los Sistemas de Soporte a la Decisión Clínica (CDSS). Los autores detallan cómo técnicas como SHAP, LIME y Grad-CAM dominan la explicabilidad en dominios como la radiología y la oncología. Sin embargo, la revisión revela brechas importantes en la validación clínica longitudinal, la evaluación de la usabilidad y las implicaciones éticas. En respuesta, el artículo propone un marco teórico orientado al diseño de herramientas empáticas con el clínico, asegurando un uso responsable de la IA en la medicina.

---

### Pregunta de Investigación y Objetivos

El estudio busca abordar los desafíos de la adopción clínica de la IA mediante los siguientes objetivos formales:

- Identificar y categorizar las técnicas de XAI utilizadas en los CDSS.
    
- Reportar y mapear los dominios clínicos y las aplicaciones de los CDSS basados en XAI.
    
- Evaluar la efectividad y la usabilidad de los resultados de las herramientas de XAI en los entornos clínicos.
    

---

### Argumento Central o Hipótesis

La falta de transparencia y explicabilidad (la naturaleza de "caja negra") de los modelos de inteligencia artificial de alto rendimiento es una barrera crítica que impide su adopción generalizada en la atención médica. La Inteligencia Artificial Explicable (XAI) no es solo una característica técnica adicional, sino una necesidad ética, legal y de seguridad del paciente que resulta fundamental para asegurar el control humano, la rendición de cuentas y la confianza clínica.

---

### Hallazgos y Conclusiones Clave

- **Técnicas predominantes:** SHAP, LIME y Grad-CAM emergieron como los métodos de XAI más adoptados.
    
- **Segmentación por datos:** Los métodos agnósticos al modelo (como SHAP) dominaron las tareas con datos tabulares, mientras que los enfoques específicos del modelo (como Grad-CAM) prevalecieron en dominios basados en imágenes, como la radiología y la patología.
    
- **Falta de inclusión de usuarios finales:** Solo el 29% de los estudios evaluados (18 de 62) reportaron la participación de médicos en las fases de desarrollo o diseño de evaluación de los modelos.
    
- **Deficiencias estadísticas:** Únicamente el 17.7% de los estudios realizó pruebas de significancia estadística formal para respaldar la integración técnica de XAI, lo que supone una debilidad metodológica preocupante.
    
- **Integración ética deficiente:** Aspectos éticos como el sesgo demográfico, el desequilibrio de datos y la estabilidad de las explicaciones solo fueron abordados de manera superficial en la mayoría de los trabajos.
    

---

### Metodología y Datos

- **Diseño de la investigación:** Revisión sistemática estructurada siguiendo estrictamente las pautas PRISMA.
    
- **Fuentes de Datos:** Se buscaron artículos en PubMed, IEEE Xplore, Scopus y Web of Science (enero 2018 a mayo 2025).
    
- **Tamaño de la muestra:** De un resultado inicial de 1824 registros, 62 estudios cumplieron con todos los criterios de inclusión para el análisis final.
    
- **Métodos analíticos:** Debido a la heterogeneidad de los datos y de las métricas clínicas, no se realizó un metaanálisis convencional del tamaño del efecto. Se aplicó una síntesis cuantitativa de solo texto basada en frecuencias y una evaluación rigurosa de calidad usando una lista de verificación adaptada de CONSORT-AI y STARD-AI.
    

---

### Marco Teórico

- **Taxonomía XAI:** El artículo se apoya en la distinción teórica clásica de la inteligencia explicable: métodos _agnósticos al modelo_ (ej. SHAP y LIME, que se aplican _post-hoc_) frente a métodos _específicos del modelo_ (ej. Grad-CAM o mecanismos de atención, integrados en redes neuronales profundas).
    
- **Marco TMEA (Task-Modality-Explanation Alignment):** Los autores introducen un marco teórico novedoso que postula que "la utilidad esperada de una explicación se maximiza cuando la clase de explicación se alinea funcionalmente con (i) el perfil de error de la tarea clínica y la necesidad de verificación, y (ii) la estructura de información de la modalidad".

---

### Resultados e Interpretación

- **Distribución de dominio:** La radiología (14 estudios) y la oncología (13 estudios) lideran abrumadoramente las especialidades médicas que implementan XAI.
    
- **Métricas de Evaluación XAI:** Se demostró que la interpretabilidad no se evaluó de manera uniforme. La _fidelidad_ (qué tanto se aproxima la explicación a la lógica original del modelo) se usó en 16 estudios, mientras que la _puntuación de confianza humana_ solo se evaluó en 9 estudios.
    
- **Confianza Clínica:** Se observó una correlación valiosa: "Los estudios que combinaron un alto rendimiento predictivo con una fuerte fidelidad en las explicaciones $(\ge0.85)$ informaron puntuaciones de confianza clínica entre 12 y 18 puntos porcentuales más altas", demostrando el valor pragmático de la transparencia.
    

---

### Limitaciones y Críticas

- Los autores anotan explícitamente sus propias limitaciones: su restricción a artículos revisados por pares en inglés puede haber introducido un sesgo de idioma o de publicación que omite literatura gris valiosa.
    
- Debido a la rápida evolución tecnológica de la XAI, técnicas muy recientes, como la explicabilidad basada en indicaciones para grandes modelos de lenguaje (LLMs), no estuvieron representadas plenamente en el conjunto de datos.
    
- El estudio indica que la comunidad académica actual "omite de forma crítica las perspectivas de pacientes, enfermeras o administradores de atención médica", sesgando fuertemente el panorama hacia una interpretación médico-céntrica.

---

### Contexto Académico

Esta investigación contrasta explícitamente con revisiones previas (ej. Tjoa et al., 2020) que se enfocaron principalmente en conceptos fundamentales de explicabilidad, proporcionando en su lugar una síntesis altamente empírica enfocada en la aplicabilidad clínica (el "mundo real"). Se alinea fuertemente con el incipiente entorno regulatorio global, reconociendo el "derecho a la explicación" dictado por la Ley de Inteligencia Artificial de la UE (EU AI Act) y las pautas de la FDA de EE.UU.

---

### Implicaciones Prácticas y Teóricas

- **Implicaciones Prácticas:** La integración de herramientas de XAI en la atención médica no debe ser únicamente un ejercicio algorítmico, sino un desafío sistemático que exige "pruebas de usabilidad en etapas tempranas del diseño" y "estudios de implementación longitudinal con bucles de retroalimentación" dentro de los sistemas EHR (Registro de Salud Electrónico).
    
- **Implicaciones Teóricas:** A través de su marco TMEA, los autores traducen las descripciones teóricas de la XAI en siete "proposiciones falsables", instando a los investigadores biomédicos a abandonar la aplicación aleatoria de métodos de interpretabilidad y reemplazarlos por una evaluación rigurosa basada en la intersección de la carga cognitiva humana y las restricciones de tiempo de la decisión médica.