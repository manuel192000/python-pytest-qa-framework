# Git y GitHub

## Las tres zonas
Directorio de trabajo -> `git add` -> staging -> `git commit` -> repo local -> `git push` -> remoto (GitHub).

## Comandos

| Comando | Qué hace | Por qué | Cuándo |
|---|---|---|---|
| `git init` | Crea `.git` con el historial | Sin ella no hay control de versiones | Proyecto nuevo (en el trabajo usas `git clone`) |
| `git branch -m main` | Renombra la rama actual | `main` es el estándar | Tras `git init` |
| `git remote -v` | Lista remotos y URLs | Comprobar a dónde sube el código | Antes de un push |
| `git switch -c nombre` | Crea una rama y cambia a ella | Trabajar aislado de `main` | Antes de cada tarea |
| `git add -A` / `git add archivo` | Prepara cambios (staging) | Elegir qué entra en el commit | Antes de commitear |
| `git commit -m "msg"` | Guarda una foto con mensaje | Punto del historial al que volver | Al terminar una unidad de trabajo |
| `git push -u origin rama` | Sube la rama y la enlaza (upstream) | Respaldar y abrir PR | Primera vez que subes una rama |
| `gh pr create --base main` | Abre un Pull Request | Revisión y CI antes de llegar a `main` | Al terminar un cambio |
| `git status` | Muestra el estado | Saber dónde estás | Constantemente |
| `git log --oneline` | Historial resumido | Ver qué se hizo | Para revisar o buscar cambios |

## Flujo mínimo vs flujo de equipo

**Mínimo (proyecto personal, trabajando directo en `main`): 3 comandos.**
```
git add .                  # o: git add archivo
git commit -m "feat: ..."
git push
```

**De equipo (rama + Pull Request): los mismos 3, más 3 pasos que añaden seguridad.**
```
git switch -c feat/nombre          # 1. rama nueva (una vez por tarea)
git add .                          # \
git commit -m "feat: ..."          #  } los 3 de siempre
git push -u origin feat/nombre     # /  (-u solo la primera vez de esa rama)
gh pr create --base main --fill    # 2. pedir revisión
```
Opcional: `git status` antes del commit para ver qué entra (hábito, no obligatorio).

| Paso extra | Qué aporta | Quién lo exige |
|---|---|---|
| Rama (`switch -c`) | Aislar tu cambio de `main` | Todo equipo |
| `-u` en el primer push | Enlazar rama local y remota | Solo la primera vez |
| PR (`gh pr create`) | Revisión y CI antes de unir | Políticas de rama de `main` |

`git add .` y `git add -A` hacen lo mismo en las versiones modernas de git (añaden todo lo nuevo, cambiado y borrado). `git add archivo` es más preciso cuando solo quieres commitear parte de los cambios.

**Pregunta: ¿por qué en un equipo no se hace `git push` directo a `main`?**
Porque `main` es lo que se despliega y debe estar siempre estable. Si cada persona sube directo, un cambio roto o sin revisar llega a todos de inmediato. Con rama y PR, otra persona revisa el cambio, el CI ejecuta los tests y solo entonces se une. En muchos equipos `main` está protegida con una política de rama que bloquea el push directo, y eso es exactamente lo que se exige también en Azure DevOps. En un proyecto personal es opcional, pero practicarlo es lo que se valora en una entrevista.

## Resumen del flujo con una analogía

`main` es el documento oficial de la empresa. Una **rama** es una copia de trabajo temporal. Un **commit** es guardar una versión con un mensaje. **Push** es subir tu copia a GitHub. Un **Pull Request** es pedir que revisen tu copia antes de pasarla al documento oficial. **Merge** es aceptar. Después se borra la copia y se sincroniza `main` con `pull`.

- Una rama por **tarea** (no por cada cambio pequeño). Varios commits dentro de la misma rama son normales.
- `git switch -c` = crear la rama y cambiarte a ella (atajo de `git branch` + `git switch`).
- `-u` se usa en el **primer push de cada rama**, porque cada rama nueva necesita enlazarse con su copia en GitHub. Después basta `git push`.

## Herramientas: GitHub Desktop, terminal y web

| Acción | Terminal | GitHub Desktop | Web (github.com) |
|---|---|---|---|
| Crear rama | `git switch -c nombre` | Current Branch → New Branch | (crear desde el PR) |
| Preparar y commitear | `git add .` + `git commit -m` | Marcar archivos + escribir mensaje + Commit | No |
| Subir | `git push -u origin rama` | Publish branch / Push origin | No |
| Abrir PR | `gh pr create` | Create Pull Request | Compare & pull request |
| Revisar y aprobar | `gh pr review` | No | **Files changed** → Review |
| Unir | `gh pr merge` | No | **Squash and merge** |
| Sincronizar | `git pull` | Fetch / Pull origin | No |

En equipos profesionales se mezclan las tres: la **terminal** (o el editor) para el trabajo diario, la **web** para revisar y unir PRs, y las interfaces gráficas como Desktop son aceptadas pero menos comunes. Lo importante es entender qué comando hay detrás de cada botón, porque en una entrevista o en un pipeline (CI) solo hay terminal.

**Pregunta: ¿usas terminal o interfaz gráfica para git? ¿Importa?**
Uso la terminal para el trabajo diario porque es más rápida, funciona igual en cualquier máquina y en los pipelines de CI, y me obliga a entender qué hace cada operación. La web la uso para revisar y aprobar PRs, que es donde la interfaz visual de los diffs es mejor. No importa tanto la herramienta como entender el modelo (rama, commit, push, PR, merge): quien lo entiende puede usar cualquier cliente gráfico, pero quien solo conoce los botones se bloquea cuando algo falla.

## Unir un Pull Request y sincronizar

Flujo completo de un cambio: `git switch main` -> `git pull` -> `git switch -c rama` -> trabajar -> `git add` -> `git commit` -> `git push -u origin rama` -> `gh pr create` -> merge del PR -> `git switch main` -> `git pull`.

| Comando | Qué hace | Por qué | Cuándo |
|---|---|---|---|
| `gh pr merge N --squash --delete-branch` | Une el PR N a `main` aplastando sus commits en uno y borra la rama | Historial limpio: un commit por PR | Cuando el PR está revisado y el CI en verde |
| `git switch main` | Cambia a `main` (los archivos sin commitear te acompañan) | Volver a la rama principal | Tras unir un PR |
| `git pull` | Descarga y aplica los cambios del remoto (`fetch` + `merge`) | Tu `main` local se queda viejo si no lo haces | Siempre antes de crear una rama nueva |

Métodos de merge en un PR:
- **Merge commit:** conserva todos los commits y añade uno de unión.
- **Squash:** junta todos los commits del PR en uno solo. Historial lineal y legible.
- **Rebase:** reaplica los commits uno a uno sobre `main`, sin commit de unión.

Ejemplo: tu rama tiene 3 commits (`feat: add validators`, `fix: typo`, `docs: notes`).

| Método | Cómo queda `main` | Historial |
|---|---|---|
| Merge commit | Los 3 commits + 1 commit extra de unión ("Merge pull request #4") | Fiel pero con ruido y ramificado |
| **Squash** | **1 solo commit** con todos los cambios (usa el título del PR) | Limpio: un commit por PR |
| Rebase | Los 3 commits, uno detrás de otro, sin commit de unión | Lineal, conserva el detalle |

En la web, el botón verde "Merge pull request" usa merge commit por defecto; la flecha a su lado permite elegir Squash o Rebase. Con la terminal se elige con `gh pr merge -m` (merge), `-s` (squash) o `-r` (rebase). Muchos equipos fijan un único método permitido en la configuración del repo para que todos los PRs queden igual.

**Pregunta: ¿por qué hacer `git pull` en `main` antes de crear una rama?**
Porque la rama nace desde donde estás. Si tu `main` local está desactualizado, tu rama parte de una base vieja y al abrir el PR aparecen conflictos o cambios ajenos mezclados con los tuyos. Con `git pull` partes del estado más reciente del equipo. Hábito base: sincronizar, crear la rama, trabajar, abrir el PR.

**Pregunta: ¿cuándo usarías squash y cuándo merge commit?**
Squash cuando los commits intermedios del PR son ruido ("fix typo", "wip") y quieres un commit por funcionalidad en `main`; es lo más común en equipos que hacen PRs pequeños. Merge commit cuando cada commit de la rama tiene valor propio y quieres conservar el historial exacto, por ejemplo en ramas largas con varias personas. La contrapartida del squash es que pierdes el detalle de los commits individuales.

**Pregunta: ¿qué pasa con los archivos sin commitear al hacer `git switch`?**
Los archivos nuevos (untracked) siempre te acompañan porque no pertenecen a ninguna rama. Los cambios en archivos ya rastreados también viajan si no chocan con la rama destino; si chocan, git se niega a cambiar y te pide commitear o guardar con `git stash`.

## Errores comunes (y cómo leerlos)

| Error | Causa | Solución |
|---|---|---|
| `unknown flag: --delete` | Escribiste `--delete branch` (con espacio). La opción correcta es `--delete-branch`, con guion. Con el espacio, la terminal lee `--delete` como una opción y `branch` como otro argumento. | `gh pr merge 2 --squash --delete-branch` |
| `no matches found: bonita?` | Pegaste texto normal en la terminal; zsh lo interpretó como comando y el `?` como comodín de archivos. | Pega en la terminal solo comandos. |

| `Your local changes to the following files would be overwritten by checkout` | Tienes cambios sin commitear en un archivo y la rama destino tiene otra versión (o no lo tiene). Git se niega a cambiar para no perder tu trabajo. | Guardarlos con `git stash`, cambiar de rama, y recuperarlos con `git stash pop`. O commitearlos. |

### git stash
Guarda tus cambios sin commitear en un cajón temporal y deja el directorio limpio.

| Comando | Qué hace |
|---|---|
| `git stash` | Guarda los cambios y limpia el directorio |
| `git stash list` | Lista lo guardado |
| `git stash pop` | Recupera lo último guardado y lo quita del cajón |

**Cuándo:** necesitas cambiar de rama o hacer `git pull` pero tu trabajo a medias no está listo para un commit.

### git fetch --prune
Tu máquina guarda una copia de cómo ve el remoto (`origin/rama`). Esa copia no se actualiza sola cuando alguien borra una rama en GitHub y queda una referencia fantasma (se ve en `git branch -a`).
- `git fetch` actualiza esa copia con lo que hay en GitHub.
- `--prune` además elimina las referencias a ramas que ya no existen en el remoto.

**Cuándo:** de vez en cuando, y siempre en equipos que borran la rama tras cada merge. Para hacerlo automático: `git config --global fetch.prune true`.

**Pregunta: ¿qué diferencia hay entre `git fetch` y `git pull`?**
`fetch` solo descarga y actualiza tu copia del remoto, sin tocar tus archivos ni tu rama: es seguro y te deja revisar antes. `pull` es `fetch` más `merge` (o `rebase`): además integra esos cambios en tu rama actual. Uso `fetch` cuando quiero ver qué hay antes de integrar, y `pull` cuando sé que quiero actualizar mi rama.

### Lo que pasó al unir el PR #2
`gh pr merge` hace dos cosas: une el PR en GitHub y después cambia tu rama local a `main` y borra la rama. El merge en GitHub sí ocurrió, pero el cambio local falló por el error de arriba, así que la rama quedó sin borrar. Un comando puede fallar a medias, por eso hay que comprobar el estado (`gh pr view`, `git status`) antes de repetirlo.

Tras un squash, `git branch -d` se niega a borrar la rama local ("not fully merged"), porque el commit aplastado de `main` es distinto de los commits de tu rama. Se usa `git branch -D`, pero solo después de confirmar que el PR está unido. Para la rama remota: `git push origin --delete nombre-rama`.

**Cómo leer un error de un comando:** el mensaje empieza por la causa (`unknown flag: --delete`). Lo demás suele ser la ayuda del comando. Busca en esa ayuda la opción correcta (`-d, --delete-branch`). Una opción larga lleva dos guiones y una sola palabra unida por guiones; nunca lleva espacios.

**Pregunta: ¿qué haces cuando un comando de git o gh te da un error que no entiendes?**
Primero leo la primera línea del error, que casi siempre indica la causa exacta. Después ejecuto `comando --help` para ver la sintaxis correcta, y si sigue sin quedar claro, consulto la documentación oficial. Evito copiar comandos que no entiendo, sobre todo los que reescriben historial o borran ramas. Un senior no memoriza todo: sabe leer el error y encontrar la respuesta rápido.

## Conventional Commits
Formato `tipo: descripción`. El tipo describe **qué efecto tiene el cambio en el producto**, no si creas o modificas un archivo.

| Tipo | Cuándo | Efecto en la versión (SemVer) | Ejemplo |
|---|---|---|---|
| `feat` | Funcionalidad nueva para quien usa el producto/framework | minor | `feat: add login page object` |
| `fix` | Corrige un bug | patch | `fix: wait for toast before asserting` |
| `docs` | Solo documentación | ninguno | `docs: update roadmap` |
| `test` | Añade o ajusta tests sin tocar código de producto | ninguno | `test: add password boundary cases` |
| `refactor` | Reorganiza código sin cambiar su comportamiento | ninguno | `refactor: extract email regex` |
| `chore` | Mantenimiento y herramientas de desarrollo (config, dependencias, pre-commit) | ninguno | `chore: add pre-commit with ruff` |

Crear un archivo no lo convierte en `feat`: un README nuevo es `docs`, un `.pre-commit-config.yaml` es `chore`. Pregúntate: "¿cambia lo que hace el producto para quien lo usa?". Si sí, `feat` o `fix`; si no, el tipo que describe el trabajo. Algunos equipos añaden `ci:` (pipelines) y `build:` (empaquetado/dependencias).

## gh pr create: opciones y orden

**El orden es siempre: primero `git push`, después `gh pr create`.** Un PR compara dos ramas **en GitHub**, así que tu rama tiene que existir allí antes. (Si olvidas el push, `gh` suele ofrecerse a hacerlo, pero conviene no depender de eso.)

| Opción | Qué hace |
|---|---|
| `--base main` | Rama destino. Es opcional: por defecto usa la rama principal del repo. Se pone para ser explícito, y es necesaria si el destino NO es `main` (por ejemplo una rama `release/1.2`) |
| `--fill` | Rellena título y descripción con el mensaje de tu commit (o de tus commits) |
| `--title "..." --body "..."` | Los escribes tú a mano |
| `--draft` | Lo abre como borrador (aún no listo para revisar) |
| `--web` | Abre el formulario en el navegador |
| (sin opciones) | Modo interactivo: te pregunta título y descripción |

No hay una forma única: `--fill` es cómoda para cambios pequeños con buen mensaje de commit; para cambios grandes se escribe un `--title` y `--body` que expliquen el porqué, qué se probó y cómo revisarlo.

**Pregunta: ¿qué escribirías en la descripción de un PR para que sea fácil de revisar?**
Qué problema resuelve o qué necesidad cubre y por qué se eligió este enfoque; qué cambió a grandes rasgos (para orientar al revisor antes de abrir el diff); cómo se probó (tests ejecutados, pasos manuales); y si hay riesgos, decisiones discutibles o partes que no se tocaron a propósito. Un PR pequeño y enfocado, con descripción clara, se revisa más rápido y con mejor calidad que uno enorme sin contexto.

## Preguntas de entrevista

**1. ¿Diferencia entre `git add`, `git commit` y `git push`?**
Son tres zonas distintas. `add` mueve cambios al staging, donde decides qué entra en el siguiente commit. `commit` crea una foto permanente pero solo en tu repo local. `push` envía los commits al remoto, y solo entonces tus compañeros los ven. La separación permite hacer commits pequeños y limpios aunque hayas tocado muchos archivos.

**2. ¿Por qué trabajar en ramas y no commitear a `main`?**
`main` debe estar siempre estable porque de ahí salen los despliegues. Con ramas, cada cambio se desarrolla aislado, pasa revisión en un PR y se valida con CI antes de unirse. Los equipos suelen proteger `main` para impedir el push directo. Además permiten trabajo en paralelo y descartar experimentos sin rastro.

**3. ¿Qué significa `-u` en `git push -u origin rama`?**
*Set upstream*: enlaza la rama local con la remota. Después, `git push` y `git pull` funcionan sin argumentos y `git status` indica si estás adelantado o atrasado respecto al remoto. Solo hace falta la primera vez.

**4. ¿Qué es un Conventional Commit y por qué importa?**
Un formato de mensaje `tipo: descripción`. El historial se lee de un vistazo, se pueden generar changelogs automáticos y las herramientas de release calculan la versión según los tipos (`feat` sube minor, `fix` sube patch). Conecta directamente con release management.
