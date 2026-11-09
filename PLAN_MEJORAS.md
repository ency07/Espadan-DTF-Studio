# Plan por fases — Mejoras de Espadan DTF Studio (inspiradas en DTPrep)

> Objetivo: mejorar el clon de Espadan (E:\Espadan-DTF-Studio) añadiendo features que DTPrep ofrece, implementadas de forma propia (no copiar código ni marca de DTPrep, comercial).
> Base: Espadan v0.005 (commit actual del clon). Branch de trabajo: `mejoras-dtprep` (no tocar `main`).
> Licencia: Espadan open source; DTPrep comercial — solo inspiración de features.

---

## Reglas de trabajo (heredadas del proyecto)
- Una fase por vez: implementar + test + revisar diff + commit en rama de test + push + verificar preview antes de la siguiente.
- No modificar `main`; todo en rama `mejoras-dtprep`.
- No copiar código/marca de DTPrep.
- Tests deben pasar (`python -B -m unittest discover -s tests -v`) antes de cada commit.
- Verificar encoding (UTF-8) y que el .exe compile (build.ps1) al final.

---

## Fase 0 — Preparación y baseline
**Objetivo:** entorno listo, baseline de tests, rama de trabajo.
- Crear rama `mejoras-dtprep` desde `main`.
- Ejecutar tests baseline y registrar resultado (19 pasando esperado).
- Documentar dependencias (requirements.txt) y versión Python (3.10+).
- Añadir marcador de versión interna: `0.005-dtprep.0` (sin tocar release oficial).
**Entregable:** rama creada, tests baseline verdes, commit "chore: baseline para mejoras dtprep".
**Criterio de aceptación:** tests 19/19, rama creada, diff vacío excepto rama.

---

## Fase 1 — Knockout de color arbitrario de prenda (garment color)
**Problema:** Espadan solo elimina negro (black_tolerance) y blanco (white_tolerance). DTPrep permite knockout de cualquier color de prenda.
**Cambios:**
- `halftone_core.py`: añadir parámetro `garment_color` (RGB) y `garment_tolerance`. Calcular distancia de color (euclidiana o CIE) entre cada píxel y el color de prenda; generar máscara de match con feather suave (smoothstep). Aplicar knockout sobre alpha (multiplicar por 1-match), respetando glow protection.
- Refactorizar `black_match`/`white_match` para derivar de un `garment_match` genérico cuando se provea `garment_color`; mantener compatibilidad con knockout_black/knockout_white (casos negro/blanco siguen funcionando como atajos).
- `halftone_ui.py`: añadir selector de color de prenda (color picker) + slider de tolerancia + toggle "knockout garment color". Mantener toggles black/white como presets rápidos.
- `presets.py`: añadir campo `garment_color` y `garment_tolerance` con defaults (negro #111111).
**Tests:** unitarios para match de color, feather, preservación de glow, compatibilidad backward (knockout_black sigue igual).
**Riesgo:** performance (distancia por píxel). Mitigar con procesamiento por strips (ya existe) y vectorización NumPy.
**Criterio de aceptación:** knockout de color arbitrario funcional, tests verdes, preview en UI.

---

## Fase 2 — Limpieza de píxeles semitransparentes (white haze removal)
**Problema:** Espadan no elimina stray transparent pixels que causan haze.
**Cambios:**
- `halftone_core.py`: añadir parámetro `clean_haze` (bool) y `haze_threshold` (0-255). Tras el render, aplicar filtro: píxeles con alpha por debajo del umbral y sin color significativo → alpha 0. Opcional: morphological opening sobre canal alpha para eliminar islas pequeñas.
- Integrar en el pipeline de strips (aplicar por strip para no romper memoria).
- `halftone_ui.py`: checkbox "Limpiar haze" + slider umbral en Advanced → Protection.
**Tests:** verificar que píxeles con alpha bajo se eliminan, que detalles válidos se preservan, que no afecta alpha alto.
**Criterio de aceptación:** haze cleanup funcional, tests verdes.

---

## Fase 3 — Shadow color boost
**Problema:** al halftonear se pierde color en sombras; DTPrep restaura.
**Cambios:**
- `halftone_core.py`: añadir parámetro `shadow_boost` (0-100). En zonas de sombra (light < 0.3), multiplicar RGB por factor (1 + boost/100 * (1-light)) antes de exportar, solo donde alpha > 0. Clampear a 255.
- Aplicar por strip, preservando ICC/DPI.
- `halftone_ui.py`: slider "Shadow boost" en Advanced → Tonal/Color.
**Tests:** verificar boost en sombras, no afecta luces, clampeo correcto.
**Criterio de aceptación:** shadow boost funcional, tests verdes.

---

## Fase 4 — Eliminación de puntos mínimos (min dot px)
**Problema:** Espadan no filtra puntos demasiado pequeños para imprimir.
**Cambios:**
- `halftone_core.py`: añadir parámetro `min_dot_px` (int). Tras renderizar alpha, aplicar filtro de área mínima: componentes conectados con área < min_dot_px² → alpha 0 (usar scipy o implementación propia con etiquetado; si no hay scipy, implementar con PIL/NumPy simple o skimage opcional).
- Decisión: implementar con NumPy + etiquetado simple (4-conectividad) para no añadir dependencia pesada; documentar límite.
- `halftone_ui.py`: slider "Punto mínimo (px)" en Advanced → Pattern.
**Tests:** verificar eliminación de islas pequeñas, preservación de áreas grandes.
**Criterio de aceptación:** min dot funcional, tests verdes, sin nueva dependencia obligatoria.

---

## Fase 5 — Halftone en todo el diseño (opcional, "full design halftone")
**Problema:** Espadan por defecto halftonea solo alpha (semi-transparentes). DTPrep permite halftonear todo el diseño para efecto más suave.
**Cambios:**
- `halftone_core.py`: añadir parámetro `halftone_entire` (bool). Si True, aplicar screening también a áreas opacas (alpha=1) usando la luminancia como tone, no solo alpha. Si False (default), comportamiento actual.
- `halftone_ui.py`: checkbox "Halftone en todo el diseño" en Advanced → Pattern.
**Tests:** verificar diferencia visual/numérica entre modos, no romper alpha halftone por defecto.
**Criterio de aceptación:** toggle funcional, tests verdes.

---

## Fase 6 — Preview modes adicionales + QA + tests + docs + build
**Cambios:**
- `halftone_ui.py`: añadir modos de preview (solo halftone, solo knockout, combinado) como selector; ya existe Before/After, extender.
- Añadir validación post-export (QA): verificar que no haya alpha parcial excesivo, dimensiones, DPI. Reutilizar idea de validate_image (implementación propia, no copiar de DTF Forge).
- Completar tests para todas las fases (objetivo: ≥40 tests).
- Actualizar README.md (features nuevas), CHANGELOG.md (v0.006 o v0.005-dtprep).
- Ejecutar build.ps1 y verificar .exe.
**Criterio de aceptación:** tests ≥40 pasando, .exe compila, README/CHANGELOG actualizados.

---

## Orden y dependencias
Fase 0 → 1 → 2 → 3 → 4 → 5 → 6 (secuencial; cada fase depende de la anterior por cambios en core).
Fases 2,3,4 pueden paralelizarse entre sí si se desea, pero se recomienda secuencial para revisar diffs.

## Riesgos
- Performance: garment color distance + haze cleanup + min dot en imágenes grandes. Mitigar con strips (ya existe) y cancelación.
- Regresión visual: tests de snapshot (imagen) recomendados; añadir tests de referencia con imágenes pequeñas.
- Licencia: no copiar DTPrep; implementaciones propias.

## Entregables por fase
- Commit en rama `mejoras-dtprep` por fase.
- Push + verificar (no hay preview web, pero tests + .exe).
- Nota en CHANGELOG por fase.

## Métricas de éxito
- Tests: 19 → ≥40.
- Features DTPrep cubiertas: knockout color arbitrario, haze cleanup, shadow boost, min dot, full-design halftone.
- .exe compila y corre.
- Sin regresión en features existentes (alpha halftone, presets, etc.).