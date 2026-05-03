# CAPÍTULO 3: MATERIAL Y MÉTODOS

## 3.1 Introducción al capítulo

En este apartado introduciría brevemente que el capítulo describe el diseño metodológico completo del estudio: origen de los datos, criterios de selección, definición de variables de supervivencia, preprocesamiento, análisis exploratorio, implementación de modelos, métricas de evaluación, validación interna, validación externa y herramientas utilizadas.

**Objetivo del apartado:** dejar claro que este capítulo no presenta resultados, sino el procedimiento seguido para obtenerlos.

---

## 3.2 Diseño del estudio

### 3.2.1 Tipo de estudio

Aquí explicaría que se trata de un estudio observacional retrospectivo basado en análisis secundario de datos clínicos y genómicos procedentes de repositorios públicos.

### 3.2.2 Población de estudio

Se definirían las cohortes analizadas:

- METABRIC, cáncer de mama.
    
- TCGA-BRCA, cáncer de mama.
    
- Cohorte NSCLC / TCGA-LUAD-LUSC / MSK-CTDx, cáncer de pulmón no microcítico, según confirmes finalmente el origen exacto.
    

### 3.2.3 Endpoint principal

Definiría como endpoint primario la **supervivencia global** u **Overall Survival**, formada por dos variables:

- `duration`: tiempo de seguimiento en meses.
    
- `event`: indicador binario del evento, donde 1 indica fallecimiento y 0 indica censura.
    

### 3.2.4 Esquema general del flujo metodológico

Aquí incluiría una figura tipo pipeline:

**Figura propuesta:**  
**Figura 5. Flujo metodológico general del estudio.**  
Adquisición de datos → limpieza → definición de variables objetivo → análisis exploratorio → partición train/test → preprocesamiento → entrenamiento de modelos → evaluación → validación cruzada → interpretabilidad → comparación entre cohortes.

---

## 3.3 Conjuntos de datos utilizados

## 3.3.1 Cohorte METABRIC

Este apartado debe describir el dataset METABRIC: origen, tipo de cáncer, número inicial de registros, número de variables, variables clínicas, variables moleculares, variables de tratamiento y variables de supervivencia.

Aquí ya puedes incluir lo que tienes: METABRIC parte de **2.509 registros y 39 variables**, con información clínica, molecular, terapéutica y de supervivencia. Tras definir el endpoint de supervivencia global, el análisis se realiza sobre los pacientes con `Overall Survival (Months)` y `Overall Survival Status` disponibles.

## 3.3.2 Cohorte TCGA-BRCA

Dejaría este apartado preparado con la misma estructura que METABRIC:

- Fuente de datos.
    
- Identificador del dataset.
    
- Número inicial de pacientes.
    
- Número de variables.
    
- Variables clínicas disponibles.
    
- Variables moleculares disponibles.
    
- Variables de supervivencia.
    
- Diferencias principales respecto a METABRIC.
    
- Estado del preprocesamiento.
    

**Texto marcador para completar después:**  
“Este apartado se completará tras finalizar la adquisición, limpieza y preprocesamiento de la cohorte TCGA-BRCA, manteniendo los mismos criterios metodológicos aplicados a METABRIC para garantizar la comparabilidad entre cohortes.”

## 3.3.3 Cohorte de cáncer de pulmón no microcítico

Dejaría el título de forma flexible hasta que confirmes el origen exacto:

**Opción A:** Cohorte TCGA-LUAD/LUSC.  
**Opción B:** Cohorte NSCLC MSK-CTDx 2022.  
**Opción C:** Cohorte NSCLC procedente de cBioPortal.

El contenido seguiría la misma lógica:

- Fuente de datos.
    
- Subtipo tumoral: adenocarcinoma, escamoso o NSCLC agregado.
    
- Número de pacientes.
    
- Variables clínicas.
    
- Variables moleculares.
    
- Variables de supervivencia.
    
- Limitaciones de comparabilidad con cáncer de mama.
    

## 3.3.4 Tabla resumen de cohortes

**Tabla propuesta:**  
**Tabla 8. Características generales de los conjuntos de datos incluidos en el estudio.**

Columnas recomendadas:

|Cohorte|Tipo tumoral|Fuente|N inicial|N final analítico|Nº variables iniciales|Endpoint|Tasa de eventos|Estado del análisis|
|---|---|--:|--:|--:|--:|---|--:|---|
|METABRIC|Cáncer de mama|cBioPortal|2.509|1.981|39|Overall Survival|57,7%|Completado|
|TCGA-BRCA|Cáncer de mama|cBioPortal/GDC|Pendiente|Pendiente|Pendiente|Overall Survival|Pendiente|Pendiente|
|NSCLC|Pulmón no microcítico|Pendiente confirmar|Pendiente|Pendiente|Pendiente|Overall Survival|Pendiente|Pendiente|

---

## 3.4 Criterios de inclusión y exclusión

## 3.4.1 Criterios de inclusión

Incluiría criterios comunes a todos los datasets:

- Pacientes con diagnóstico oncológico primario.
    
- Disponibilidad de tiempo de supervivencia.
    
- Disponibilidad de estado del evento.
    
- Presencia de covariables clínicas y/o moleculares mínimas.
    
- Muestras primarias, si el dataset distingue muestra primaria frente a metástasis.
    

## 3.4.2 Criterios de exclusión

- Registros sin tiempo de supervivencia.
    
- Registros sin indicador de evento.
    
- Identificadores duplicados.
    
- Variables constantes o sin valor informativo.
    
- Variables que impliquen fuga de información, por ejemplo variables de recaída si el endpoint primario es supervivencia global.
    
- Variables redundantes o altamente colineales.
    

## 3.4.3 Diagrama de selección de pacientes

**Figura propuesta:**  
**Figura 6. Diagrama de flujo de inclusión y exclusión de pacientes por cohorte.**

Este diagrama puede mostrar, para cada dataset:

N inicial → eliminación por falta de supervivencia → eliminación de duplicados → eliminación de variables no válidas → N final analítico.

---

## 3.5 Variables del estudio

## 3.5.1 Variables objetivo

Explicar:

- `duration`: tiempo hasta evento o censura.
    
- `event`: evento observado.
    
- Codificación específica usada en cada dataset.
    

Para METABRIC:

- `Overall Survival (Months)` → `duration`.
    
- `Overall Survival Status` → `event`.
    
- `"1:DECEASED"` → 1.
    
- `"0:LIVING"` → 0.
    

## 3.5.2 Covariables clínicas

Incluir edad, estadio tumoral, grado histológico, tamaño tumoral, ganglios positivos, estado hormonal, estado HER2, tratamientos recibidos, etc.

## 3.5.3 Covariables moleculares

Incluir variables como PAM50, Integrative Cluster, TMB, mutation count o variables equivalentes disponibles en cada cohorte.

## 3.5.4 Variables excluidas del modelado

Aquí explicaría la eliminación de:

- Identificadores: `Patient ID`, `Sample ID`.
    
- Variables constantes: `Study ID`, `Cancer Type`, `Sample Type`, `Sex`, etc.
    
- Variables redundantes.
    
- Variables con fuga de información.
    
- Variables no comparables entre datasets.
    

## 3.5.5 Tabla de variables finales por cohorte

**Tabla propuesta:**  
**Tabla 9. Variables incluidas y excluidas en el modelado por conjunto de datos.**

Columnas recomendadas:

|Cohorte|Variables objetivo|Covariables clínicas|Covariables moleculares|Variables excluidas|Motivo de exclusión|
|---|---|---|---|---|---|
|METABRIC|duration, event|Edad, estadio, NPI, ganglios, tamaño tumoral...|PAM50, TMB, Integrative Cluster...|IDs, constantes, redundantes...|Varianza cero, fuga, colinealidad|
|TCGA-BRCA|Pendiente|Pendiente|Pendiente|Pendiente|Pendiente|
|NSCLC|Pendiente|Pendiente|Pendiente|Pendiente|Pendiente|

---

## 3.6 Preprocesamiento de datos

## 3.6.1 Eliminación de metadatos e identificadores

Explicar la eliminación de columnas que no aportan señal predictiva o que son identificadores únicos.

## 3.6.2 Tratamiento de valores perdidos

Explicar la estrategia:

- Variables objetivo: no se imputan; se eliminan registros con valores ausentes.
    
- Variables numéricas: imputación por mediana.
    
- Variables categóricas: imputación con categoría `Unknown`.
    

## 3.6.3 Tratamiento de tiempos de supervivencia iguales a cero

Explicar que los tiempos `T = 0` se desplazan a un valor mínimo positivo, por ejemplo `0.001` meses, para evitar problemas numéricos en Cox, RSF o modelos derivados.

## 3.6.4 Tratamiento de outliers

Describir la winsorización o recorte por percentiles, especialmente en variables como tamaño tumoral, ganglios positivos o TMB.

## 3.6.5 Codificación de variables categóricas

Explicar el uso de **One-Hot Encoding**, con `drop='first'` para evitar multicolinealidad perfecta y `handle_unknown='ignore'`.

## 3.6.6 Escalado de variables numéricas

Explicar el uso de `StandardScaler`, especialmente necesario para Cox y DeepSurv.

## 3.6.7 Construcción de matrices finales de modelado

Describir:

- `X_train`
    
- `X_test`
    
- `y_train`
    
- `y_test`
    
- arrays estructurados de `scikit-survival`
    
- matrices `numpy` para DeepSurv
    

## 3.6.8 Tabla resumen del preprocesamiento

**Tabla propuesta:**  
**Tabla 10. Operaciones de preprocesamiento aplicadas a las cohortes analizadas.**

|Paso|METABRIC|TCGA-BRCA|NSCLC|Justificación|
|---|---|---|---|---|
|Eliminación de IDs|Sí|Pendiente|Pendiente|Evitar variables no predictivas|
|Eliminación de constantes|Sí|Pendiente|Pendiente|Varianza cero|
|Imputación numérica|Mediana|Pendiente|Pendiente|Robustez ante outliers|
|Imputación categórica|Unknown|Pendiente|Pendiente|Mantener ausencia como categoría|
|Winsorización|Sí|Pendiente|Pendiente|Reducir influencia de extremos|
|One-Hot Encoding|Sí|Pendiente|Pendiente|Modelos requieren variables numéricas|
|Escalado|Sí|Pendiente|Pendiente|Cox/DeepSurv|

---

## 3.7 División train/test y validación interna

## 3.7.1 Partición de entrenamiento y prueba

Explicar la división 80/20 con estratificación por evento.

Para METABRIC:

- Train: 1.584 pacientes.
    
- Test: 397 pacientes.
    
- Tasa de eventos train: 57,77%.
    
- Tasa de eventos test: 57,68%.
    

## 3.7.2 Validación cruzada k-fold

Explicar que se empleará validación cruzada estratificada, preferiblemente 5-fold, para evaluar estabilidad de C-index e IBS.

## 3.7.3 Validación externa entre cohortes

Este apartado es clave para tu TFM. Incluiría:

- Entrenar en METABRIC y evaluar en TCGA-BRCA.
    
- Entrenar en TCGA-BRCA y evaluar en METABRIC.
    
- Evaluar el enfoque metodológico en NSCLC de forma independiente.
    
- No forzar validación externa directa mama ↔ pulmón salvo que haya variables armonizadas comparables.
    

Esta parte responde directamente a la brecha identificada en el estado del arte: falta de validación externa y escasa evaluación sistemática de transferibilidad entre TCGA-BRCA y METABRIC.

---

## 3.8 Modelos de supervivencia implementados

## 3.8.1 Kaplan-Meier

Describirlo como modelo no paramétrico, descriptivo y referencia basal para IBS.

## 3.8.2 Modelo de Cox con penalización LASSO

Describirlo como modelo semiparamétrico, interpretable y útil para selección de variables.

## 3.8.3 Random Survival Forest

Describirlo como modelo no paramétrico de machine learning capaz de capturar interacciones y relaciones no lineales.

## 3.8.4 DeepSurv

Describirlo como red neuronal basada en la pérdida de Cox, diseñada para estimar riesgo individual no lineal.

## 3.8.5 Tabla resumen de modelos

**Tabla propuesta:**  
**Tabla 11. Modelos de supervivencia implementados y función dentro del estudio.**

|Modelo|Familia|Entrada|Salida|Ventaja principal|Limitación principal|
|---|---|---|---|---|---|
|Kaplan-Meier|No paramétrico|duration, event|Curva S(t)|Interpretabilidad|No usa covariables|
|Cox-LASSO|Semiparamétrico|Covariables clínicas/moleculares|Riesgo individual|Interpretabilidad|Riesgos proporcionales|
|RSF|Machine Learning|Covariables procesadas|Riesgo y S(t)|No linealidad|Menor interpretabilidad|
|DeepSurv|Deep Learning|Covariables escaladas|Log-riesgo|Alta flexibilidad|Riesgo de sobreajuste/opacidad|

---

## 3.9 Métricas de evaluación

## 3.9.1 C-index

Métrica principal de discriminación.

## 3.9.2 Integrated Brier Score

Métrica de calibración y discriminación temporal.

## 3.9.3 Log-rank test

Comparación de curvas de supervivencia entre grupos.

## 3.9.4 Curvas de supervivencia y estratificación de riesgo

Explicar cómo se dividirán los pacientes en grupos de bajo y alto riesgo, o en cuartiles de riesgo.

## 3.9.5 Tabla resumen de métricas

**Tabla propuesta:**  
**Tabla 12. Métricas utilizadas para la evaluación de modelos de supervivencia.**

|Métrica|Qué evalúa|Interpretación|Modelos aplicables|
|---|---|---|---|
|C-index|Discriminación|Mayor es mejor|Cox, RSF, DeepSurv|
|IBS|Error temporal/calibración|Menor es mejor|KM, Cox, RSF, DeepSurv|
|Log-rank|Separación de curvas|p < 0,05 significativo|KM, grupos de riesgo|
|Brier Score temporal|Error por horizonte temporal|Menor es mejor|Cox, RSF, DeepSurv|

---

## 3.10 Interpretabilidad de los modelos

## 3.10.1 Interpretabilidad en Cox-LASSO

Coeficientes, hazard ratios e intervalos de confianza.

## 3.10.2 Interpretabilidad en RSF

Importancia por permutación, ranking de variables y, si procede, profundidad mínima.

## 3.10.3 Interpretabilidad en DeepSurv

Valores SHAP o análisis post-hoc de importancia global y local.

## 3.10.4 Comparación de biomarcadores entre modelos

Este apartado preparará el análisis posterior de concordancia entre modelos: variables que aparecen como importantes en Cox, RSF y DeepSurv.

---

## 3.11 Entorno computacional y reproducibilidad

Incluir:

- Python.
    
- pandas, numpy, scikit-learn.
    
- lifelines.
    
- scikit-survival.
    
- pycox.
    
- PyTorch.
    
- matplotlib/seaborn.
    
- random seed.
    
- estructura del repositorio.
    
- rutas de datos procesados.
    
- serialización de modelos.
    

---

## 3.12 Consideraciones éticas y de protección de datos

Aquí bastaría con recordar que el estudio usa datos públicos o anonimizados, sin reidentificación de pacientes, y que el repositorio no incluirá datos sensibles.

---

# CAPÍTULO 4: RESULTADOS

## 4.1 Introducción al capítulo

Este capítulo debe abrir con una frase clara:

“En este capítulo se presentan los resultados obtenidos tras aplicar el pipeline metodológico descrito en el Capítulo 3. La presentación se organiza por cohorte y por familia de modelos, separando los resultados descriptivos, los resultados de rendimiento predictivo y los análisis de interpretabilidad.”

Aquí no haría discusión profunda todavía. La interpretación crítica queda para el Capítulo 5.

---

## 4.2 Descripción de las cohortes analíticas finales

## 4.2.1 Cohorte METABRIC final

Incluir:

- N inicial.
    
- N final.
    
- Nº eventos.
    
- Nº censurados.
    
- Seguimiento mínimo, mediano y máximo.
    
- Tasa de eventos.
    
- Nº variables finales tras preprocesamiento.
    

Para METABRIC ya tienes:

- 1.981 pacientes finales.
    
- 1.144 eventos.
    
- 837 censurados.
    
- Tasa de eventos: 57,7%.
    
- Mediana de supervivencia: 156,3 meses.
    
- S(5 años): 0,780.
    
- S(10 años): 0,593.
    
- S(15 años): 0,445.
    
- S(20 años): 0,294.
    

## 4.2.2 Cohorte TCGA-BRCA final

Dejar preparado para completar.

## 4.2.3 Cohorte NSCLC final

Dejar preparado para completar.

## 4.2.4 Tabla comparativa de cohortes finales

**Tabla propuesta:**  
**Tabla 13. Características descriptivas de las cohortes finales incluidas en el análisis.**

|Cohorte|N final|Eventos|Censurados|Tasa eventos|Mediana seguimiento|Variables finales|
|---|--:|--:|--:|--:|--:|--:|
|METABRIC|1.981|1.144|837|57,7%|Pendiente/156,3 OS mediana|56|
|TCGA-BRCA|Pendiente|Pendiente|Pendiente|Pendiente|Pendiente|Pendiente|
|NSCLC|Pendiente|Pendiente|Pendiente|Pendiente|Pendiente|Pendiente|

---

## 4.3 Análisis exploratorio de datos

## 4.3.1 Distribución de variables clínicas

Aquí incluiría gráficos de barras para variables categóricas y distribuciones para variables numéricas.

**Figuras propuestas:**

- **Figura 7. Distribución de variables clínico-demográficas en METABRIC.**
    
- **Figura 8. Distribución de variables histopatológicas en METABRIC.**
    
- **Figura 9. Distribución de biomarcadores moleculares y subtipos en METABRIC.**
    

## 4.3.2 Valores perdidos por cohorte

**Figura propuesta:**  
**Figura 10. Porcentaje de valores perdidos por variable y cohorte.**

## 4.3.3 Correlaciones entre variables numéricas

Para METABRIC ya tienes el heatmap y la interpretación de correlaciones: TMB y mutation count son prácticamente redundantes; Overall Survival y Relapse Free Status están muy correlacionadas; NPI se asocia con grado, estadio y ganglios.

**Figura propuesta:**  
**Figura 11. Mapa de calor de correlaciones entre variables numéricas en METABRIC.**

## 4.3.4 Resumen de hallazgos exploratorios

Este apartado debe ser breve y descriptivo: qué variables parecen más informativas, qué variables son redundantes y qué variables serán vigiladas en el modelado.

---

## 4.4 Resultados Kaplan-Meier

## 4.4.1 Supervivencia global no estratificada

Presentar la curva KM global de METABRIC.

**Figura propuesta:**  
**Figura 12. Curva Kaplan-Meier de supervivencia global en METABRIC.**

## 4.4.2 Supervivencia por grupos clínicos

Incluir edad, estado ganglionar, estadio tumoral, NPI y grado histológico.

**Figura propuesta:**  
**Figura 13. Curvas Kaplan-Meier estratificadas por variables clínico-patológicas en METABRIC.**

## 4.4.3 Supervivencia por biomarcadores moleculares

Incluir PAM50, Integrative Cluster, 3-Gene classifier, ER, PR y HER2.

**Figura propuesta:**  
**Figura 14. Curvas Kaplan-Meier estratificadas por biomarcadores moleculares en METABRIC.**

## 4.4.4 Test log-rank univariante

Para METABRIC ya tienes un resultado fuerte: 16 de 20 variables analizadas presentan diferencias significativas. Las variables más discriminativas fueron estado ganglionar, edad, NPI, estadio tumoral y subtipos moleculares.

**Tabla propuesta:**  
**Tabla 14. Resultados del test log-rank univariante en METABRIC.**

Columnas:

|Variable|Nº grupos|Chi-cuadrado|p-valor|Significancia|Interpretación breve|
|---|--:|--:|--:|---|---|

---

## 4.5 Resultados del modelo Cox-LASSO

## 4.5.1 Selección de variables

Presentar:

- número de covariables iniciales;
    
- número de covariables candidatas;
    
- valor óptimo de alpha;
    
- variables seleccionadas.
    

Para METABRIC, Cox-LASSO selecciona 23 variables y alcanza C-index test de 0,676 e IBS de 0,186, mejorando al Kaplan-Meier marginal, cuyo IBS fue 0,218.

## 4.5.2 Rendimiento predictivo

**Tabla propuesta:**  
**Tabla 15. Rendimiento del modelo Cox-LASSO en METABRIC.**

|Métrica|Resultado|
|---|--:|
|C-index train|0,686|
|C-index test|0,676|
|Diferencia train-test|0,010|
|IBS Kaplan-Meier marginal|0,218|
|IBS Cox-LASSO|0,186|
|Mejora relativa IBS vs KM|14,4%|

## 4.5.3 Interpretabilidad del modelo Cox-LASSO

**Figura propuesta:**  
**Figura 15. Forest plot de hazard ratios del modelo Cox-LASSO en METABRIC.**

## 4.5.4 Evaluación del supuesto de riesgos proporcionales

Incluir test de Schoenfeld y explicar qué variables lo incumplen parcialmente.

**Tabla propuesta:**  
**Tabla 16. Evaluación del supuesto de riesgos proporcionales en Cox-LASSO.**

---

## 4.6 Resultados del modelo Random Survival Forest

## 4.6.1 Hiperparámetros seleccionados

Para METABRIC, el modelo RSF aparece con `n_estimators = 500` y `max_features = log2`.

## 4.6.2 Rendimiento predictivo

Según tus resultados, RSF obtiene C-index test de 0,706 e IBS de 0,1796, mejorando a Cox-LASSO tanto en discriminación como en calibración temporal.

**Tabla propuesta:**  
**Tabla 17. Rendimiento del modelo Random Survival Forest en METABRIC.**

|Métrica|Resultado|
|---|--:|
|C-index OOB|0,689|
|C-index train|0,817|
|C-index test|0,706|
|Diferencia train-test|0,111|
|IBS test|0,1796|
|Mejora IBS vs KM|17,5%|
|Mejora IBS vs Cox-LASSO|3,6%|

## 4.6.3 Importancia de variables

**Figura propuesta:**  
**Figura 16. Importancia de variables del modelo Random Survival Forest en METABRIC.**

## 4.6.4 Curvas de supervivencia predichas por grupos de riesgo

**Figura propuesta:**  
**Figura 17. Estratificación de pacientes por riesgo estimado mediante Random Survival Forest.**

---

## 4.7 Resultados del modelo DeepSurv

## 4.7.1 Arquitectura seleccionada

Para METABRIC, ya tienes una arquitectura óptima:

- capas: `[64, 64]`;
    
- dropout: 0,1;
    
- learning rate: 0,01;
    
- batch size: 256;
    
- batch normalization: sí.
    

## 4.7.2 Rendimiento predictivo

DeepSurv obtiene C-index test de 0,6877 e IBS de 0,1863. Su C-index mejora respecto a Cox-LASSO, pero su IBS es similar al de Cox y peor que RSF en METABRIC.

**Tabla propuesta:**  
**Tabla 18. Rendimiento del modelo DeepSurv en METABRIC.**

|Métrica|Resultado|
|---|--:|
|C-index train|0,7145|
|C-index test|0,6877|
|Diferencia train-test|0,0268|
|IBS test|0,1863|
|C-index CV 5-fold|0,6925 ± 0,0162|
|IBS CV 5-fold|0,1811 ± 0,0071|

## 4.7.3 Curva de aprendizaje

**Figura propuesta:**  
**Figura 18. Evolución de la pérdida de entrenamiento y validación en DeepSurv.**

## 4.7.4 Explicabilidad mediante SHAP

Tus resultados muestran como principales variables SHAP: edad al diagnóstico, ganglios positivos, Nottingham Prognostic Index, PAM50 LumA y estadio tumoral.

**Figura propuesta:**  
**Figura 19. Importancia global SHAP del modelo DeepSurv en METABRIC.**

---

## 4.8 Comparación global de modelos en METABRIC

Este será uno de los apartados centrales del Capítulo 4.

La tabla final de METABRIC debería incluir los cuatro modelos:

|Modelo|Tipo|C-index train|C-index test|IBS test|C-index CV|Covariables|
|---|---|--:|--:|--:|--:|--:|
|Kaplan-Meier|No paramétrico|—|—|0,2177|—|0|
|Cox-LASSO|Semiparamétrico|0,6864|0,6761|0,1863|0,679 ± 0,014|23|
|RSF|ML no paramétrico|0,7060 / 0,8171 según tabla final revisada|0,7060|0,1796|Pendiente/ver sección RSF|56|
|DeepSurv|Red neuronal|0,7145|0,6877|0,1863|0,693 ± 0,016|56|

Aquí conviene revisar la tabla final de RSF para evitar una pequeña inconsistencia: en una salida aparece `C-index train = 0.8171`, mientras que en la tabla comparativa final aparece `0.7060` como train para RSF. Yo lo corregiría antes de pasarlo a la memoria definitiva.

**Figura propuesta:**  
**Figura 20. Comparación de C-index e Integrated Brier Score entre modelos en METABRIC.**

---

## 4.9 Resultados en TCGA-BRCA

Este apartado debe quedar preparado con exactamente la misma estructura que METABRIC:

### 4.9.1 Descripción de la cohorte TCGA-BRCA

### 4.9.2 Kaplan-Meier y log-rank

### 4.9.3 Cox-LASSO

### 4.9.4 Random Survival Forest

### 4.9.5 DeepSurv

### 4.9.6 Comparación global de modelos en TCGA-BRCA

### 4.9.7 Variables pronósticas más relevantes en TCGA-BRCA

**Texto marcador:**  
“Este apartado se completará tras finalizar el preprocesamiento y modelado de TCGA-BRCA. La estructura de presentación será idéntica a la empleada para METABRIC, con el objetivo de facilitar una comparación directa entre ambas cohortes de cáncer de mama.”

---

## 4.10 Resultados en la cohorte de cáncer de pulmón no microcítico

Misma lógica:

### 4.10.1 Descripción de la cohorte NSCLC

### 4.10.2 Kaplan-Meier y log-rank

### 4.10.3 Cox-LASSO

### 4.10.4 Random Survival Forest

### 4.10.5 DeepSurv

### 4.10.6 Comparación global de modelos en NSCLC

### 4.10.7 Variables pronósticas más relevantes en NSCLC

**Texto marcador:**  
“Este apartado se completará tras confirmar el origen final de la cohorte de cáncer de pulmón no microcítico y tras adaptar el pipeline de preprocesamiento a las variables disponibles en dicho conjunto de datos.”

---

## 4.11 Validación cruzada y robustez de resultados

## 4.11.1 Validación cruzada interna por cohorte

**Tabla propuesta:**  
**Tabla 19. Resultados de validación cruzada interna por modelo y cohorte.**

|Cohorte|Modelo|C-index CV media|C-index CV sd|IBS CV media|IBS CV sd|
|---|---|--:|--:|--:|--:|
|METABRIC|Cox-LASSO|0,679|0,014|Pendiente|Pendiente|
|METABRIC|DeepSurv|0,6925|0,0162|0,1811|0,0071|
|TCGA-BRCA|Pendiente|Pendiente|Pendiente|Pendiente|Pendiente|
|NSCLC|Pendiente|Pendiente|Pendiente|Pendiente|Pendiente|

## 4.11.2 Estabilidad de los modelos

**Figura propuesta:**  
**Figura 21. Distribución del C-index por fold y modelo.**

**Figura propuesta:**  
**Figura 22. Distribución del IBS por fold y modelo.**

---

## 4.12 Validación externa y transferibilidad entre cohortes

Este apartado debe ser uno de los más importantes cuando tengas TCGA-BRCA.

## 4.12.1 Entrenamiento en METABRIC y evaluación en TCGA-BRCA

## 4.12.2 Entrenamiento en TCGA-BRCA y evaluación en METABRIC

## 4.12.3 Comparación de pérdida de rendimiento externa

**Tabla propuesta:**  
**Tabla 20. Validación externa cruzada entre cohortes de cáncer de mama.**

|Modelo|Entrenamiento|Evaluación externa|C-index interno|C-index externo|Δ C-index|IBS interno|IBS externo|Δ IBS|
|---|---|---|--:|--:|--:|--:|--:|--:|
|Cox-LASSO|METABRIC|TCGA-BRCA|Pendiente|Pendiente|Pendiente|Pendiente|Pendiente|Pendiente|
|RSF|METABRIC|TCGA-BRCA|Pendiente|Pendiente|Pendiente|Pendiente|Pendiente|Pendiente|
|DeepSurv|METABRIC|TCGA-BRCA|Pendiente|Pendiente|Pendiente|Pendiente|Pendiente|Pendiente|

**Figura propuesta:**  
**Figura 23. Matriz de rendimiento externo entre cohortes.**

---

## 4.13 Síntesis de resultados

Cerrar el capítulo con una tabla-resumen muy compacta.

**Tabla propuesta:**  
**Tabla 21. Síntesis global de resultados por cohorte y modelo.**

|Cohorte|Mejor modelo por C-index|Mejor modelo por IBS|Variables más relevantes|Observaciones|
|---|---|---|---|---|
|METABRIC|RSF|RSF|Edad, ganglios, NPI, estadio, PAM50|RSF mejor calibrado; DeepSurv mejora Cox en C-index|
|TCGA-BRCA|Pendiente|Pendiente|Pendiente|Pendiente|
|NSCLC|Pendiente|Pendiente|Pendiente|Pendiente|

---

# CAPÍTULO 5: DISCUSIÓN

## 5.1 Introducción al capítulo

Aquí abriría explicando que la discusión interpreta críticamente los resultados del Capítulo 4, los relaciona con los objetivos del TFM, los compara con la literatura revisada en el Capítulo 2 y analiza sus implicaciones metodológicas, clínicas y biológicas.

---

## 5.2 Resumen de los principales hallazgos

Este apartado debe responder de forma clara:

- Qué modelo funcionó mejor.
    
- Qué métrica favoreció a cada modelo.
    
- Qué variables fueron más relevantes.
    
- Qué resultados fueron consistentes entre modelos.
    
- Qué resultados fueron inesperados.
    

Para METABRIC, la idea principal preliminar sería:

“En la cohorte METABRIC, los modelos multivariantes superaron al Kaplan-Meier marginal, lo que confirma que las covariables clínicas y moleculares aportan información pronóstica individual. El Random Survival Forest obtuvo el mejor equilibrio entre discriminación y calibración temporal, mientras que DeepSurv mejoró a Cox-LASSO en C-index pero no en IBS.”

---

## 5.3 Interpretación de los resultados en METABRIC

## 5.3.1 Valor pronóstico de las variables clínicas clásicas

Discutir edad, estado ganglionar, NPI, estadio tumoral, tamaño tumoral y grado histológico.

## 5.3.2 Valor pronóstico de los subtipos moleculares

Discutir PAM50, Integrative Cluster, HER2, ER, PR y clasificadores moleculares.

## 5.3.3 Comparación entre señal clínica y señal molecular

Aquí puedes plantear una idea importante: en METABRIC, las variables clínicas clásicas parecen seguir teniendo un peso muy fuerte, incluso cuando se incorporan variables moleculares.

## 5.3.4 Interpretación de variables terapéuticas

Discutir el sesgo de indicación: quimioterapia, radioterapia, hormonoterapia y cirugía no deben interpretarse causalmente en un estudio observacional retrospectivo.

---

## 5.4 Comparación entre modelos

## 5.4.1 Kaplan-Meier como referencia basal

Discutir su utilidad descriptiva, pero también su limitación: no individualiza el riesgo.

## 5.4.2 Cox-LASSO: equilibrio entre rendimiento e interpretabilidad

Discutir que Cox-LASSO aporta interpretabilidad y selección de variables, pero limita relaciones no lineales y depende del supuesto de riesgos proporcionales.

## 5.4.3 Random Survival Forest: mejor rendimiento en METABRIC

Discutir que RSF parece capturar mejor relaciones no lineales e interacciones, con mejor C-index e IBS.

## 5.4.4 DeepSurv: mejora parcial y riesgo de sobreajuste

Discutir que DeepSurv mejora la discriminación respecto a Cox-LASSO, pero no supera a RSF en calibración. Esto es importante porque evita una conclusión simplista de “deep learning siempre es mejor”.

## 5.4.5 Interpretabilidad comparada

Comparar:

- Cox: hazard ratios.
    
- RSF: importancia de variables.
    
- DeepSurv: SHAP.
    

---

## 5.5 Robustez, validación cruzada y generalización

## 5.5.1 Estabilidad interna de los modelos

Discutir los resultados de validación cruzada.

## 5.5.2 Transferibilidad METABRIC ↔ TCGA-BRCA

Este apartado se completará cuando tengas TCGA-BRCA.

Aquí debes conectar con la brecha de conocimiento del Capítulo 2: la falta de validación externa es una limitación frecuente en la literatura, y tu TFM intenta abordarla de forma explícita.

## 5.5.3 Transferibilidad metodológica al cáncer de pulmón

Aquí discutiría si el pipeline funciona también en NSCLC, aunque no necesariamente se puedan comparar directamente los biomarcadores con cáncer de mama.

---

## 5.6 Comparación con la literatura científica

## 5.6.1 Comparación con estudios previos en cáncer de mama

Comparar los rangos de C-index obtenidos con los reportados en el Capítulo 2.

## 5.6.2 Comparación con estudios previos en cáncer de pulmón

Pendiente de completar tras los resultados NSCLC.

## 5.6.3 Aportación diferencial del TFM

Aquí destacaría:

- Comparación sistemática de cuatro familias de modelos.
    
- Uso de métricas de discriminación y calibración.
    
- Validación cruzada.
    
- Preparación de validación externa.
    
- Interpretabilidad mediante varios enfoques.
    
- Pipeline reproducible.
    

---

## 5.7 Implicaciones clínicas y biomédicas

## 5.7.1 Estratificación de riesgo individual

Discutir cómo los modelos podrían ayudar a identificar pacientes con peor pronóstico.

## 5.7.2 Potencial utilidad en medicina de precisión

Relacionar con oncología personalizada, subtipos moleculares y selección de pacientes de alto riesgo.

## 5.7.3 Limitaciones para la adopción clínica

Explicar que estos modelos no son herramientas clínicas listas para uso asistencial porque requieren validación externa, calibración prospectiva y evaluación en poblaciones más diversas.

---

## 5.8 Limitaciones del estudio

Este apartado debe ser muy sólido. Incluiría:

## 5.8.1 Limitaciones de los datos

- Datos retrospectivos.
    
- Valores perdidos.
    
- Diferencias de codificación entre datasets.
    
- Posible sesgo de selección.
    
- Falta de diversidad poblacional.
    
- Diferencias entre plataformas moleculares.
    

## 5.8.2 Limitaciones metodológicas

- Riesgo de sobreajuste.
    
- Alta dimensionalidad.
    
- Tamaño muestral limitado para DeepSurv.
    
- Interpretabilidad limitada de modelos complejos.
    
- Dependencia de hiperparámetros.
    

## 5.8.3 Limitaciones de validación

- Si la validación externa queda incompleta, declararlo.
    
- Si solo se valida dentro de METABRIC, no sobregeneralizar.
    
- Si TCGA-BRCA y METABRIC tienen variables no completamente equivalentes, discutirlo.
    

## 5.8.4 Limitaciones de causalidad

Aclarar que el estudio es predictivo, no causal. Especialmente para tratamientos, no interpretar efectos como beneficio o daño terapéutico.

---

## 5.9 Fortalezas del estudio

Incluir:

- Uso de cohortes reconocidas.
    
- Comparación multimodelo.
    
- Métricas complementarias.
    
- Validación cruzada.
    
- Interpretabilidad.
    
- Reproducibilidad del código.
    
- Separación clara entre análisis descriptivo, predictivo e interpretativo.
    

---

## 5.10 Líneas futuras

Propondría:

- Completar validación externa TCGA-BRCA ↔ METABRIC.
    
- Incorporar datos ómicos adicionales.
    
- Evaluar modelos multimodales.
    
- Usar calibración temporal avanzada.
    
- Explorar modelos de riesgos no proporcionales.
    
- Validar en cohortes clínicas independientes.
    
- Implementar SHAP/interpretabilidad para todos los modelos.
    
- Evaluar fairness y sesgos por edad, sexo, ancestría o subtipo tumoral.
    

---

## 5.11 Respuesta a los objetivos del TFM

Este apartado es muy útil antes de conclusiones. Lo organizaría como tabla.

**Tabla propuesta:**  
**Tabla 22. Grado de cumplimiento de los objetivos específicos del TFM.**

|Objetivo|Evidencia generada|Grado de cumplimiento|
|---|---|---|
|Implementar KM, Cox, RSF y DeepSurv|Modelos entrenados en METABRIC|Parcial/completo según datasets|
|Comparar C-index, IBS y log-rank|Tablas de resultados|Parcial/completo|
|Validar internamente|5-fold CV|Parcial/completo|
|Validar externamente|Pendiente TCGA-BRCA|Pendiente|
|Interpretar biomarcadores|Cox, RSF, SHAP|Parcial/completo|
|Comparar con literatura|Capítulo 2 + discusión|Pendiente completar|

---

## 5.12 Cierre de la discusión

Terminaría con un párrafo de síntesis:

“En conjunto, los resultados preliminares obtenidos en METABRIC sugieren que la incorporación de covariables clínicas y moleculares mejora la predicción de supervivencia respecto a una referencia marginal no individualizada. Los modelos no lineales, especialmente Random Survival Forest, parecen capturar mejor la complejidad pronóstica de la cohorte, aunque la ganancia frente a modelos interpretables como Cox-LASSO debe valorarse junto con la calibración, la estabilidad, la interpretabilidad y la capacidad de generalización externa. La incorporación posterior de TCGA-BRCA y de la cohorte de cáncer de pulmón permitirá determinar si estos patrones se mantienen en cohortes independientes y en otro tipo tumoral.”

---

# Orden recomendado de tablas y figuras

Como en tu documento actual ya existen tablas y figuras previas, yo continuaría la numeración así:

## Tablas principales nuevas

- **Tabla 8. Características generales de los conjuntos de datos incluidos.**
    
- **Tabla 9. Variables incluidas y excluidas en el modelado.**
    
- **Tabla 10. Operaciones de preprocesamiento aplicadas.**
    
- **Tabla 11. Modelos de supervivencia implementados.**
    
- **Tabla 12. Métricas de evaluación.**
    
- **Tabla 13. Características descriptivas de las cohortes finales.**
    
- **Tabla 14. Resultados log-rank en METABRIC.**
    
- **Tabla 15. Rendimiento Cox-LASSO en METABRIC.**
    
- **Tabla 16. Supuesto de riesgos proporcionales en Cox-LASSO.**
    
- **Tabla 17. Rendimiento RSF en METABRIC.**
    
- **Tabla 18. Rendimiento DeepSurv en METABRIC.**
    
- **Tabla 19. Validación cruzada interna.**
    
- **Tabla 20. Validación externa entre cohortes.**
    
- **Tabla 21. Síntesis global de resultados.**
    
- **Tabla 22. Cumplimiento de objetivos.**
    

## Figuras principales nuevas

- **Figura 5. Pipeline metodológico general.**
    
- **Figura 6. Diagrama de inclusión/exclusión de pacientes.**
    
- **Figura 7. Distribución clínico-demográfica en METABRIC.**
    
- **Figura 8. Distribución histopatológica en METABRIC.**
    
- **Figura 9. Distribución de biomarcadores moleculares en METABRIC.**
    
- **Figura 10. Valores perdidos por variable y cohorte.**
    
- **Figura 11. Heatmap de correlaciones en METABRIC.**
    
- **Figura 12. Kaplan-Meier global en METABRIC.**
    
- **Figura 13. Kaplan-Meier por variables clínico-patológicas.**
    
- **Figura 14. Kaplan-Meier por biomarcadores moleculares.**
    
- **Figura 15. Forest plot Cox-LASSO.**
    
- **Figura 16. Importancia de variables RSF.**
    
- **Figura 17. Estratificación de riesgo RSF.**
    
- **Figura 18. Curva de aprendizaje DeepSurv.**
    
- **Figura 19. Importancia SHAP DeepSurv.**
    
- **Figura 20. Comparación C-index e IBS entre modelos.**
    
- **Figura 21. C-index por fold y modelo.**
    
- **Figura 22. IBS por fold y modelo.**
    
- **Figura 23. Matriz de validación externa.**
    

---

# Recomendación final de organización

La estructura más limpia sería esta:

**Capítulo 3: Material y Métodos**  
Debe explicar exactamente cómo se obtienen los datos, cómo se limpian, cómo se definen las variables, cómo se entrenan los modelos y cómo se evalúan.

**Capítulo 4: Resultados**  
Debe presentar primero METABRIC, porque es lo que ya tienes avanzado, y después dejar secciones paralelas para TCGA-BRCA y NSCLC. Debe incluir tablas, curvas, métricas y rankings de importancia, pero con interpretación contenida.

**Capítulo 5: Discusión**  
Debe interpretar los resultados, compararlos con la literatura, explicar qué modelo parece más útil y por qué, reconocer limitaciones y dejar claro qué queda pendiente para completar la validación externa y los otros datasets.