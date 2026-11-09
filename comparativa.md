# Comparativa de herramientas DTF prepress — DTPrep vs Espadan DTF Studio

> Generado para planificar mejoras. Fuentes: lightningplugins.com/dtprep, dtprep.com, repo imanshirani/Espadan-DTF-Studio (clon en E:\Espadan-DTF-Studio), análisis previo analisis-dtf-prepress.html.
> Regla de licencia: no copiar código ni marca de DTPrep (comercial). Las mejoras se implementan de forma propia/inspirada.

---

## 1. DTPrep (Lightning Plugins) — comercial

### Hace
- Halftone interactivo en tiempo real (patrones: punto redondo y líneas; frecuencia y ángulo)
- Color knockout de **cualquier color de prenda** (no solo negro), incluyéndolo en la eliminación de fondo
- Limpieza automática de píxeles semitransparentes (white haze)
- Eliminación de puntos demasiado pequeños para imprimir
- Shadow color boost (restaura color perdido al halftonear)
- Halftone opcional en todo el diseño (efecto más suave)
- Export PNG print-ready compatible con RIPs principales
- Plugin Photoshop (PS 23.3+) + versión web (dtprep.com), sin Photoshop
- Funciona con Canva, Procreate, Affinity (exportar + subir)
- Varios modos de preview antes de confirmar
- Licenciamiento por suscripción (LemonSqueezy)

### No hace (según doc pública)
- No es open source ni gratuito
- Sin white knockout independiente documentado (el knockout de color de prenda cubre el caso)
- Sin protección específica de glow/brillos ni de texto fino documentada
- Sin control tonal separado (sombras/medios/luces) documentado
- Sin tamaño físico de impresión / LPI calculado por DPI documentado
- Sin presets JSON reutilizables documentados
- Sin máscaras de forma personalizadas (solo punto redondo y líneas)
- Sin comparación Before/After sincronizada documentada
- Sin cancelación/interrupción de renders ni procesamiento por strips documentado
- Sin tests automatizados públicos
- No es app de escritorio offline (web requiere conexión; plugin requiere Photoshop)

---

## 2. Espadan DTF Studio — open source (clonado en E:\Espadan-DTF-Studio)

### Hace
- Alpha channel halftoning (halftonea solo áreas semi-transparentes; preserva colores sólidos)
- Soft black knockout (Blend-If) con tolerancia
- White knockout independiente con tolerancia propia (v0.005)
- Reducción de cobertura (ink reduction) con target: all / black / white / both
- Protección de glow/brillos (preserve glow, protect highlights) con fuerza ajustable
- Protección de detalles finos (texto/líneas) por contraste local y geometría
- Control tonal por rangos (sombras / medios / luces) con transiciones suaves
- Tamaño físico de impresión (cm) + DPI + LPI, con cálculo de cell size (DPI/LPI), límite 60M px
- Preview en fondos negro/blanco/checkerboard + Before/After sincronizado + Fit/100%
- Presets reutilizables (JSON validado) + presets integrados (black fabric, white fabric, glow/neon, fine-line)
- Máscaras de forma personalizadas (imagen grayscale como matriz de punto)
- Patrones: Dot, Line, Square, Cross, Diamond + custom
- Ghost-line prevention (compresión de pantalla, dot gain control)
- Render en background (caché de entrada, debounce, strip-based, cancelación, espera del último resultado al exportar)
- Export PNG preservando DPI e ICC profile
- Carga con EXIF orientation
- UI PyQt6 con zoom/pan con rueda
- Tests (19 pasando) + build .exe (PyInstaller)
- App de escritorio offline (Python o .exe)

### No hace (gaps vs DTPrep y uso real)
- No knockout de color arbitrario de prenda: solo negro y blanco (DTPrep cubre cualquier color)
- No shadow color boost
- No eliminación explícita de puntos mínimos (min dot px) — no tiene control de min_dot
- No es web ni plugin de Photoshop (solo desktop Python/.exe)
- No es comercial/licenciado (sin soporte oficial)
- Patrones limitados a 5 formas + custom (DTPrep solo 2, pero @interfaz tiene 7)
- Procesamiento single-machine (no cloud/multi-usuario)
- No tiene QA/validación de imagen post-export documentada (DTF Forge sí tiene validate_image)
- No tiene dithering por error (Floyd-Steinberg) ni Bayer ordenado documentado (usa screening continuo)
- No tiene gang-sheet/nesting ni RIP completo (es prepress de imagen, no RIP)

---

## 3. Implicaciones para DTF Forge (proyecto propio del usuario)

### Ya cubre (y Espadan/DTPrep no todos)
- Knockout de color arbitrario de prenda (hex) — mejor que Espadan (solo B/W)
- Métodos de halftone: Bayer, Floyd-Steinberg, Lines
- min_dot_px (punto mínimo) — DTPrep lo tiene, Espadan no
- QA/validación de imagen post-export (validate_image)
- Salida 300 dpi, flatten alpha

### Le falta vs Espadan/DTPrep (candidatos para portar)
- Alpha channel halftoning (halftonear solo semi-transparentes)
- White knockout independiente
- Ink reduction con targets (all/black/white/both)
- Protección de glow/brillos y texto fino
- Control tonal por rangos (sombras/medios/luces)
- Tamaño físico de impresión (cm) + LPI calculado por DPI
- Presets JSON reutilizables
- Máscaras de forma personalizadas
- Before/After sincronizado + zoom/pan
- Cancelación/interrupción de renders + procesamiento por strips
- Preservación de DPI/ICC en export
- EXIF orientation al cargar
- Custom patterns (Square, Cross, Diamond, custom)
- Shadow color boost (de DTPrep)
- Limpieza de píxeles semitransparentes / white haze (de DTPrep)
- Eliminación de puntos demasiado pequeños (ya tiene min_dot, pero validar)

---

## 4. Reglas de licencia
- No copiar código ni marca de DTPrep (comercial). Implementar de forma propia/inspirada.
- Espadan es open source (MIT por repo); respetar licencia y atribución.
- DTF Forge es proyecto propio; puede reutilizar su propio código.
path">
C:/Users/Administrator/Desktop/comparativa-dtprep-espadan.md