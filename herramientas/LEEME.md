# Catálogo SOMEGA en 3D y realidad aumentada – estado y cómo seguir

Actualizado: 16-11-2026 (catálogo con extras)

## Enlace público
https://kugu777.github.io/Somega-3d/  (la S mayúscula es obligatoria)

- Repo GitHub: **kugu777/Somega-3d** (público). Cada vez que se sube algo a `main`, GitHub Actions publica la web sola (Pages → Source: GitHub Actions).
- Fichas: `#mesa` y `#enc` (por ejemplo https://kugu777.github.io/Somega-3d/#enc). Los enlaces antiguos `/mesa/` y `/encordadora/` redirigen a la ficha.
- **Enlace con configuración**: `#mesa:p16,tolva,rampa` abre la mesa con esos extras ya puestos (lo genera el botón "Compartir esta configuración"). Sirve también en `camara.html#mesa:p16,tolva`.
- Modo cámara: `camara.html` (`camara.html#mesa`, `camara.html#enc`).

## Qué hace la web
- **Catálogo** con las máquinas. Al tocar una se abre su ficha: 3D girando en 360° (botón ↻ 360°), medidas de la configuración elegida, botón "Ver en mi barco".
- **Configurador** en la ficha: grupos de opciones ("elige una", como la parrilla) y extras que se marcan o desmarcan. Se montan en su sitio en el 3D, en la realidad aumentada y en el modo cámara. "Ver 360°" enseña cada pieza sola.
- Botones "Pedir presupuesto" (de momento lleva a maquinariabatea.com) y "Compartir esta configuración".
- **Varias máquinas a la vez**: realidad aumentada (WebXR de Chrome). Se elige la máquina arriba, se toca el suelo para ponerla, y se puede girar 15°, mover o quitar. Se ven varias juntas.
- **Modo cámara** para móviles sin realidad aumentada: la cámara de fondo y la máquina encima. Usa el giroscopio, la inclinación o el acelerómetro si los hay; si no hay ninguno, se mira con el dedo. Arrastrando sobre la máquina se gira. La altura del móvil se ajusta a mano (1,40 m de serie). Las medidas son aproximadas.
- **iPhone**: visor de Apple (USDZ) para cada máquina y para las dos juntas.
- **Acabado**: inox metalizado mate, aristas dibujadas (más de 28°), sombras reales y un tono algo distinto en cada chapa.
- Las máquinas, sus opciones y los archivos están en **`lib/catalogo.js`** (lo usan `index.html` y `camara.html`).
- Las URLs de los modelos llevan versión (`V` en `lib/catalogo.js`, ahora `20261116a`). **Hay que subirla cada vez que se cambie un modelo** (y el `?v=` con que se importa `catalogo.js` en `index.html` y `camara.html`); si no, el móvil sigue usando el modelo viejo que tiene guardado.

## Máquinas
### Mesa vibradora 220 V
- STEP de origen (15-11, carpeta STEP_FINALES): `1_MESA_VIBRADORA_CON_PARRILLA_22.step`, `2_PARRILLA_16_COMPLETA.step`, `3_TOLVA_RECOGIDA.step`, `4_RAMPA_DE_SALIDA.step` y `5_MESA_CON_TODOS_LOS_EXTRAS.step` (este solo para comprobar). Todos con el mismo origen.
- Se parte en piezas (`mesa/`): `mesa-cuerpo.glb` (mesa sin parrilla), `parrilla-22.glb` (de serie), `parrilla-16.glb`, `tolva.glb` (tolva de recogida), `rampa.glb` (rampa de salida). La parrilla 22 son las piezas `PARRILLA_*`, `PLETINA_40x6_A/B` y `TUBO_10x10x1_L800_*` del STEP 1.
- iPhone: un USDZ por configuración en `mesa/usdz/` (`mesa-p22-t0-r0.usdz` … 8 en total).
- Medidas: 1161 × 810 × 1025 mm de serie; con la rampa de salida, 1352 mm de largo.
- Colores: todo inox; gomas y tacos en negro; caja Schneider XALD02 en **gris oscuro** con **pulsador_1 verde** y **pulsador_2 rojo**; pegatinas SOMEGA en azul; motovibradores y prensaestopa en gris oscuro.
- Tornillería completa en inox. No se quita ninguna pieza.

### Encordadora
- STEP de origen: `SOMEGA_chasis_encordadora (8).step`. Las piezas no tienen nombre: se distinguen por el color del dibujo.
- Medidas: 1983 × 749 × 1062 mm.
- Colores: todo inox, incluidas la tornillería, la caja del rótulo SOMEGA, la pata diagonal, los tirantes, y la **protección, el tubo y el brazo de reacción de la reductora**.
  - Negro: halador (con el cubo) y tacos de las patas.
  - Azul: motores hidráulicos y **reductora**.
  - Blanco: tuerca de nylon y brida del motor.
- Extra **Cartucho para carga de red** (`encordadora/cartucho-red.glb`, de `SOMEGA_chapa_cartuchos_maquina.step`, 728 × 287 × 322 mm, todo inox). De momento solo se ve suelto en 360° (`view: true` en `lib/catalogo.js`): falta saber dónde va montado en la encordadora. Se hace con `build_extra.py`.
- Extra **Cono de entrada de red** (`encordadora/cono-red.glb`, de `SOMEGA_cono_red_deformado.step`, 639 × 291 × 286 mm, todo inox). Solo suelto en 360°.
- Extra **Sinfín Ø80 paso 80 (tubo 1/2")** (`encordadora/sinfin.glb`, de `SOMEGA_sinfin_D80_P80_tubo1-2pulg_nucleo_chavetado.step` (15-11, el completo con el núcleo chavetado), todo inox). En el STEP está de pie; para verlo suelto se tumba (`lay: true`). Igual que el cartucho, de momento solo suelto en 360°.
- Correspondencia de colores del dibujo: ver `E` en `build_v2.py`. (3,13,50) y (70,85,93) son azul; (3,3,3), (1,1,1) y (139,147,156) son negro; los crema son blanco; el resto es inox.

### Pesadora ensacadora (en desarrollo)
- STEP de origen: `SOMEGA_pesadora_montaje_completo_v68 (2).step` (15-11, sin acabar). Ficha `#pes`.
- Medidas: 1801 × 905 × 1859 mm.
- Girada -90° en vertical respecto al STEP para que quede como la encordadora: largo en Z y la tolva de carga hacia el mismo lado que la tolva de la encordadora.
- Colores (`build_pesadora.py`, por nombre de pieza): todo inox; metacrilato de la ventana del armario del visor **transparente** (material `cristal`); botón del cierre de la tapa del armario (botón y cuerpo) **negro**; cristales del visor de peso (`visor_peso_lcd_*`) verdes; caja Schneider XALD02 gris oscuro con pulsador_1 verde y pulsador_2 rojo; bandas de rodadura de las ruedas (`rueda_ALEX_*_goma_*`) azules; bandas de cangilones (`banda_azul_*`) azules; tacos de goma de las patas (`base_niveladora_goma_*`) negros. Los reductores NMRV040 y el resto, inox.
- Malla más gruesa para que pese menos: `step2glb.py ... 1.0 0.6` (15 MB).

## Cómo añadir extras a una máquina
1. STEP de la máquina y de cada extra **con el mismo origen** (exportados desde el mismo conjunto).
2. `python3 step2glb.py` para cada uno (ver abajo).
3. Como `build_catalogo.py`: el origen se saca de la máquina y se aplica a todas las piezas (`write_glb(..., shift=SHIFT)`).
4. Si hay iPhone: un USDZ por configuración, como `catalogo_usdz.py`.
5. Añadir los grupos y extras a la máquina en `lib/catalogo.js` y subir `V`.

## Cómo añadir o cambiar una máquina
1. `python3 step2glb.py máquina.step raw.glb` (pasa el STEP a malla con sus colores, en metros y con el eje Y hacia arriba).
2. Asignar los colores a acabados reales: por nombre de pieza (como la mesa) o por color del dibujo (como la encordadora). Ver `build_v2.py`.
3. `build_v3.py`: tono distinto por chapa, normales suavizadas a 25° y GLB final, sin nombres de piezas.
4. `glb2usdz.py` para iPhone.
5. Añadir la máquina a `MACHINES` en `lib/catalogo.js`, subir la versión `V` y subir el cambio a `main`.
Hace falta: `cadquery-ocp`, `trimesh`, `pygltflib` y `usd-core` (pip).

## Móviles probados
- Móvil de Vicente (Android, sin "Servicios de Google Play para RA" ni app Google): no admite realidad aumentada; usar el modo cámara.
- Móvil de su hija: la realidad aumentada funciona.
- Samsung Galaxy de su pareja: con Samsung Internet no funciona; probar en Chrome.

## Pendiente
- Que Vicente pruebe el modo cámara en su móvil y diga qué sensor sale abajo a la izquierda.
- Confirmar el cambio del travesaño trasero 40×40 de la mesa nueva: misma medida exterior, distinto detalle.
- Montar el cartucho para carga de red, el cono de entrada de red y el sinfín en la encordadora: hace falta el STEP del conjunto con ellos puestos, o su posición.
- Botón "Pedir presupuesto": poner WhatsApp o correo de SOMEGA (ahora lleva a la web).
- Pesadora: actualizarla cuando esté acabada (mismo `build_pesadora.py`).
- Más máquinas cuando haya STEP.
