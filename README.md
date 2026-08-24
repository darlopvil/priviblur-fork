<div align="center">
  <h1>Priviblur (fork)</h1>
  <div>
  <a href="https://www.gnu.org/licenses/agpl-3.0.en.html">
    <img alt="Licencia: AGPLv3" src="https://shields.io/badge/License-AGPL%20v3-blue.svg">
  </a>
  </div>
  <h3>Frontend alternativo de Tumblr, con privacidad y sin JavaScript</h3>
</div>

<br/>

![Ejemplo](./screenshots/example.png)

Priviblur es un **proxy**: hace las peticiones a Tumblr en tu lugar, de modo que
puedas navegar sin ser rastreado. No requiere cuenta, funciona sin JavaScript y
es considerablemente más rápido que Tumblr.

---

## Sobre este fork

Este es un **fork personal** de [syeopite/priviblur](https://github.com/syeopite/priviblur),
que lleva sin actividad desde agosto de 2025 con los issues acumulados y varios
parches de terceros sin revisar.

No se hacen aportaciones al proyecto original ni se aceptan contribuciones
externas: este repositorio existe para mantener una instancia propia y para que
el código no se pierda. La licencia **AGPLv3** del original se respeta
íntegramente, junto con la autoría de [syeopite](https://github.com/syeopite) y
del resto de personas que contribuyeron al proyecto.

Si buscas el proyecto original, está aquí:
<https://github.com/syeopite/priviblur>

## Qué se ha arreglado

### El bloqueo que tumbaba todas las instancias

El fallo más grave del proyecto: `ServerDisconnectedError` en toda petición a
Tumblr, que según el despliegue también aparecía como `403 Forbidden` o como
HTML sin parsear.

La causa: `aiohttp` anuncia por defecto la extensión ALPN `http/1.1` en su
contexto SSL. Combinada con el juego de extensiones del ClientHello de Python,
el edge de Automattic cierra la conexión TCP nada más completar el handshake,
sin devolver un solo byte. Se resuelve construyendo el contexto SSL a mano, sin
llamar a `set_alpn_protocols()`.

HTTP/2 no es alternativa: Tumblr negocia h2 y acto seguido resetea el stream con
`PROTOCOL_ERROR`.

### Fallos que provocaban error 500

- `url_handler()` reventaba con cualquier URL sin hostname (`mailto:`, `tel:`,
  rutas relativas). Como se aplica a **todos** los enlaces del contenido, un
  solo post con un `mailto:` tumbaba la timeline entera.
- Los contadores de notas ausentes o nulos lanzaban `TypeError` al parsear.
- La caída de la caché con la aplicación en marcha convertía cada petición en un
  500. Ahora degrada a modo sin caché y se recupera sola.
- Enviar el formulario de ajustes incompleto lanzaba `KeyError`. Reproducible
  desde el navegador desmarcando una casilla.

### Errores que mentían sobre su causa

- El código interno `0` de Tumblr estaba mapeado a "blog no encontrado", así que
  un token de autorización caducado mostraba ese mensaje en todas las páginas.
  Ahora se distingue por el status HTTP, y se reconoce también el código `1013`.
- El manejador de respuestas no-200 afirmaba "Priviblur might have been
  ratelimited" ante cualquier código, incluido un 403. Ese mensaje falso mantuvo
  a la comunidad esperando meses a que pasara un rate limit inexistente.
- El fallback a inglés de las cadenas con plural nunca se activaba: Babel
  rellena las formas sin traducir con el propio identificador, así que
  `ngettext()` jamás lanza `KeyError` y la interfaz mostraba
  `post_note_count_plural` en pantalla.

### Interfaz

- Las alertas no tenían soporte de tema oscuro: se veían como cajas claras sobre
  el fondo negro.
- Se sirve un favicon propio. Antes, cada petición a `/favicon.ico` renderizaba
  la plantilla de error completa.

### Despliegue

- La imagen ya no incluye el repositorio git entero (232 MB → 197 MB). El hash
  del commit se inyecta con `--build-arg`.
- Base actualizada a Alpine 3.23 y añadido `tzdata`, sin el cual Alpine ignora
  `TZ` en silencio.
- Redis sustituido por **Valkey**, con límite de memoria y política LRU.
- El cache busting de los estáticos deriva del contenido de `assets/` y no del
  hash del commit, de modo que los cambios de CSS se propagan sin necesidad de
  hacer commit.

### Nuevas opciones de configuración

| Opción | Qué hace |
|---|---|
| `authorization_token` | Sobreescribe el bearer de Tumblr sin recompilar |
| `allow_external_embeds` | Renderiza los reproductores embebidos como iframes reales |
| `main_connect_timeout` y afines | Separa los timeouts de conexión y lectura |
| `connect_timeout` (caché) | Evita pagar 5 s por petición cuando la caché está caída |
| `media_connection_limit` | Limita el pool de conexiones del proxy de media |

Todas están documentadas en [`config.example.toml`](./config.example.toml).

## Instalación

> [!IMPORTANT]
> **La imagen oficial de Quay no sirve para este fork**: es la del proyecto
> original y no lleva ninguno de estos arreglos. Hay que construir desde el
> repositorio.

### Docker

```bash
git clone https://github.com/darlopvil/priviblur-fork
cd priviblur-fork

mkdir -p deploy
cp config.example.toml deploy/config.toml
# edita deploy/config.toml a tu gusto

PRIVIBLUR_COMMIT=$(git rev-parse --short HEAD) docker compose up -d --build
```

El `docker-compose.yml` del repositorio es genérico y no publica puertos al
host: asume un proxy inverso por delante. Para la configuración específica de
cada despliegue (redes externas, `TZ`, nombres de contenedor, puertos) se usa un
`docker-compose.override.yml`, que Compose fusiona automáticamente y que está en
el `.gitignore`.

### Manual

```bash
git clone https://github.com/darlopvil/priviblur-fork
cd priviblur-fork

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
pybabel compile -d locales -D priviblur

cp config.example.toml config.toml
python -m src.server
```

## Configuración

[Ejemplo comentado aquí](./config.example.toml)

> [!TIP]
> `domain` se escribe **sin esquema** (`ejemplo.com`, no `https://ejemplo.com`).
> El esquema se toma de la opción `https`.

## Desarrollo

```bash
pip install -r requirements-dev.txt
ruff check .
```

El linter cubre las familias de detección de errores (`B`, `PLE`, `PLW`, `DTZ`,
`RUF`, `ASYNC`), no solo las cuatro que traía el original. Debe pasar limpio
antes de cualquier commit.

Tras tocar `assets/` o las plantillas, recarga forzada en el navegador
(`Ctrl+Shift+R`).

## Licencia

AGPLv3, igual que el proyecto original. Cualquier instancia que se despliegue a
partir de este código debe ofrecer el código fuente a sus usuarios.
