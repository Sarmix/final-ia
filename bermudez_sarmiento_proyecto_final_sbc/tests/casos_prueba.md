# Casos de Prueba — DiagMoto SBC

**Sistema:** Diagnóstico de Fallas en Motocicletas  
**Autores:** Manuel Bermudez · Wilson Sarmiento  
**Resultado global:** 10 / 10 casos correctos ✅

---

## Tabla de validación

| ID | Descripción | Síntomas de entrada | Reglas esperadas | Reglas aplicadas | Fallas esperadas | Urgencia esperada | Acción esperada | Aptitud esperada | Estado |
|----|-------------|---------------------|------------------|------------------|-----------------|-------------------|-----------------|-----------------|--------|
| C1 | Moto no enciende por batería descargada | `bateria_descargada` | R01, R18, R26 | R01, R18, R26 | electrica | media | programar_mantenimiento | usar_con_precaucion | ✅ |
| C2 | Falla mecánica: aceite bajo y humo azul | `nivel_aceite_bajo` + `humo_azul` | R03, R14, R25 | R03, R14, R25 | mecanica | alta | ir_taller_inmediato | no_apta_para_uso | ✅ |
| C3 | Frenos deficientes: pastillas al límite | `pastillas_desgastadas` | R04, R15, R25 | R04, R15, R25 | frenos | alta | ir_taller_inmediato | no_apta_para_uso | ✅ |
| C4 | Moto no enciende por falta de combustible | `sin_combustible` | R02, R22, R27 | R02, R22, R27 | combustible | baja | revision_basica | apta_para_uso | ✅ |
| C5 | Motor sobrecalentado | `motor_sobrecalentado` | R09, R16, R25 | R09, R16, R25 | refrigeracion | alta | ir_taller_inmediato | no_apta_para_uso | ✅ |
| C6 | Humo negro por carburación descalibrada | `humo_negro` | R06, R23, R27 | R06, R23, R27 | carburacion | baja | revision_basica | apta_para_uso | ✅ |
| C7 | Cadena suelta y llanta con presión baja | `cadena_suelta` + `llanta_baja` | R05, R08, R19, R20, R26 | R05, R08, R19, R20, R26 | neumaticos, transmision | media | programar_mantenimiento | usar_con_precaucion | ✅ |
| C8 | Múltiples fallas críticas simultáneas | `pastillas_desgastadas` + `motor_sobrecalentado` + `llanta_baja` | R04, R05, R09, R15, R16, R19, R25 | R04, R05, R09, R15, R16, R19, R25 | frenos, neumaticos, refrigeracion | alta | ir_taller_inmediato | no_apta_para_uso | ✅ |
| C9 | Fuga activa de aceite (manchas + nivel bajo) | `aceite_en_suelo` + `nivel_aceite_bajo` | R11, R13, R14, R17, R25 | R11, R13, R14, R17, R25 | fuga_aceite, mecanica | alta | ir_taller_inmediato | no_apta_para_uso | ✅ |
| C10 | Sin síntomas — caso borde sin conclusión | *(ninguno)* | *(ninguna)* | *(ninguna)* | *(ninguna)* | N/A | N/A | N/A | ✅ |

---

## Análisis de cobertura

### Por tipo de urgencia

| Urgencia | Casos que la activan |
|----------|----------------------|
| Alta | C2, C3, C5, C8, C9 |
| Media | C1, C7 |
| Baja | C4, C6 |

### Por tipo de falla

| Tipo de falla | Casos |
|---------------|-------|
| electrica | C1 |
| combustible | C4 |
| mecanica | C2, C9 |
| frenos | C3, C8 |
| neumaticos | C7, C8 |
| carburacion | C6 |
| transmision | C7 |
| refrigeracion | C5, C8 |
| fuga_aceite | C9 |

### Casos especiales cubiertos

| Situación | Caso |
|-----------|------|
| Sin síntomas (sin conclusión derivable) | C10 |
| Fallas múltiples simultáneas (2 fallas) | C7, C9 |
| Fallas múltiples simultáneas (3 fallas) | C8 |
| Urgencia máxima seleccionada entre varias | C8, C9 |
| Factor de certeza < 1.0 activo (R13, CF=0.95) | C9 |

---

## Notas de validación

- **C9** activa tanto R11 (`aceite_en_suelo`) como R13 (`aceite_en_suelo + nivel_aceite_bajo`), lo que produce dos fallas: `fuga_aceite` y `mecanica`. La urgencia resultante es `alta` en ambos casos, por lo que la selección de urgencia máxima no altera el resultado.
- **C8** tiene tres fallas simultáneas con urgencias `alta`, `alta` y `alta`. La urgencia máxima es `alta`, activando R25 correctamente.
- **C10** valida el manejo de casos sin conclusión: el motor retorna `tipo_fallas = []` y la interfaz muestra el mensaje de advertencia correspondiente sin errores de ejecución.
- Todos los casos fueron ejecutados automáticamente y los resultados obtenidos coinciden exactamente con los esperados (**10/10**).
