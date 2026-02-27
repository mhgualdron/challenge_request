# Análisis y Optimización de Prompt Engineering: Resumen de Pólizas de Seguros

Este documento detalla el análisis del prompt original extraído de `LEGACY_PROMPT.md` y la propuesta de optimización para garantizar resúmenes precisos y estructurados de pólizas de seguros colombianas.

## 1. Análisis del Prompt Original

### Prompt Original
> "Resume el siguiente texto: [Texto de la póliza denso y técnico con plazos de 10-30 días, amparos de Vida, incapacidad, Circular 028, etc.]. Devuelve solo un resumen corto y preciso."

### Problemas Identificados (Análisis Técnico)
1.  **Falta de Estructura de Pensamiento:** Al solicitar directamente el resumen, el modelo tiende a omitir los plazos técnicos de notificación (30 días vs 10 días) que son críticos en seguros.
2.  **Riesgo de Omisión de Exclusiones/Coberturas:** El texto original mezcla amparos (Muerte/Incapacidad) con condiciones de pago. Sin una guía, el modelo puede dar peso excesivo a uno y olvidar el otro.
3.  **Ambigüedad en "Corto y Preciso":** Esta instrucción es subjetiva. En contextos legales, la precisión requiere terminología técnica específica (ej. "Beneficiario oneroso", "Mora"), no solo brevedad.
4.  **Incapacidad de Manejar Normativas:** El prompt ignora la mención a la "Circular Externa 028 de 2019 de la Superintendencia Financiera", un dato legal clave en Colombia que podría perderse.
5.  **Ausencia de Rol Experto:** Un modelo sin rol asignado podría resumir esto como un diario personal en lugar de un informe de riesgos para un comité técnico.

---

## 2. Técnicas Aplicadas para la Optimización

Se han incorporado las siguientes estrategias avanzadas de Prompt Engineering:

*   **System Role Persona (Instrucción de Rol):** "Eres un Analista Senior de Riesgos y Seguros con especialidad en el mercado jurídico colombiano".
*   **Chain-of-Thought (CoT):** Se obliga al modelo a realizar una triple verificación (Amparos -> Tiempos -> Pagos) antes de redactar.
*   **Few-Shot Examples:** Se proporciona un ejemplo de cómo transformar un clausulado complejo en una estructura balanceada.
*   **Estructura de Salida (Constraints de Formato):** Definición de 4 secciones obligatorias para evitar resúmenes incompletos.
*   **Negative Constraints:** Prohibición explícita de inventar datos (Alucinación) y de usar lenguaje informal.
*   **Constraint de Longitud:** Límite de 150 palabras para garantizar concisión técnica.

---

## 3. Propuesta de Prompt Optimizado

```markdown
### SYSTEM ROLE
Eres un Analista Senior de Riesgos y Seguros especializado en normatividad colombiana (Superintendencia Financiera). Tu objetivo es extraer y resumir las condiciones esenciales de un clausulado de póliza de seguros con precisión técnica absoluta.

### INSTRUCCIONES DE PROCESAMIENTO (Chain-of-Thought)
Para generar el resumen, realiza los siguientes pasos:
1. **Identificación de Riesgos:** Determina los valores asegurados y los eventos cubiertos (muerte, incapacidad, etc.).
2. **Cronograma Legal:** Identifica los plazos de aviso de revocación, noticia del siniestro y reportes a entidades financieras.
3. **Mecanismos de Pago:** Detecta la periodicidad y la incidencia de la mora según la Circular 028.
4. **Sintetiza:** Redacta el resultado final utilizando las secciones obligatorias.

### RESTRICCIONES NEGATIVAS
- NO inventes plazos ni montos; si no están en el texto, indica "No especificado".
- NO resumas el texto de forma narrativa continua; usa exclusivamente las secciones de abajo.
- NO omitas la distinción entre días hábiles y días calendario.
- Longitud máxima: 150 palabras.

### FORMATO DE SALIDA (OBLIGATORIO)

#### 1. Coberturas y Amparos
[Descripción técnica de eventos cubiertos y valores asegurados]

#### 2. Plazos de Notificación
[Tiempos exactos para revocación, siniestros y avisos al banco]

#### 3. Condiciones de Pago y Mora
[Periodicidad de pago y políticas bajo Circular 028 u otras normativas]

#### 4. Otras Condiciones
[Vigencia, cesión de cartera o requisitos de edad mencionables]

---

### EJEMPLO DE REFERENCIA (FEW-SHOT)
**Input:** "El seguro cubre vida por 50M. Se debe avisar del siniestro en 3 días. El pago es mensual."
**Output:**
#### 1. Coberturas y Amparos
Amparo básico de vida con capital asegurado de $50.000.000.
#### 2. Plazos de Notificación
Término de noticia de siniestro fijado en tres (3) días calendario.
#### 3. Condiciones de Pago y Mora
Esquema de recaudo mensual de prima.
#### 4. Otras Condiciones
No especificado.

---

### TEXTO DE LA PÓLIZA A PROCESAR:
[Pega aquí el contenido de la póliza de LEGACY_PROMPT.md]
```

---

## 4. Comparativa Entre Inputs de Muestra y Salida Esperada

| Aspecto | Comportamiento Prompt Original (Legacy) | Comportamiento Prompt Optimizado |
| :--- | :--- | :--- |
| **Manejo de Tiempos** | Podría confundir los 30 días de revocación con los 30 de siniestro. | Desglosa específicamente cada plazo en la sección 2. |
| **Detalle de Cobertura** | Generalmente dice "cubre muerte y desmembramiento". | Especifica "$98.500.000 en fallecimiento" e incluye causas (homicidio, SIDA, etc.). |
| **Referencia Legal** | Suele ignorar la Circular 028 por considerarla "texto de relleno". | Captura la importancia de la Circular 028 en la gestión de mora. |
| **Resiliencia** | Si el texto es muy largo, el resumen se vuelve superficial. | La estructura modular obliga a revisar cada punto clave sin pérdida de densidad. |
| **Formato** | Variable y difícil de extraer programáticamente. | Estructura Markdown reproducible y clara para el usuario final. |
