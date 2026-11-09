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

### Lo que pasó al unir el PR #2
`gh pr merge` hace dos cosas: une el PR en GitHub y después cambia tu rama local a `main` y borra la rama. El merge en GitHub sí ocurrió, pero el cambio local falló por el error de arriba, así que la rama quedó sin borrar. Un comando puede fallar a medias, por eso hay que comprobar el estado (`gh pr view`, `git status`) antes de repetirlo.

Tras un squash, `git branch -d` se niega a borrar la rama local ("not fully merged"), porque el commit aplastado de `main` es distinto de los commits de tu rama. Se usa `git branch -D`, pero solo después de confirmar que el PR está unido. Para la rama remota: `git push origin --delete nombre-rama`.

**Cómo leer un error de un comando:** el mensaje empieza por la causa (`unknown flag: --delete`). Lo demás suele ser la ayuda del comando. Busca en esa ayuda la opción correcta (`-d, --delete-branch`). Una opción larga lleva dos guiones y una sola palabra unida por guiones; nunca lleva espacios.

**Pregunta: ¿qué haces cuando un comando de git o gh te da un error que no entiendes?**
Primero leo la primera línea del error, que casi siempre indica la causa exacta. Después ejecuto `comando --help` para ver la sintaxis correcta, y si sigue sin quedar claro, consulto la documentación oficial. Evito copiar comandos que no entiendo, sobre todo los que reescriben historial o borran ramas. Un senior no memoriza todo: sabe leer el error y encontrar la respuesta rápido.

## Conventional Commits
Formato `tipo: descripción`. Tipos: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`.

## Preguntas de entrevista

**1. ¿Diferencia entre `git add`, `git commit` y `git push`?**
Son tres zonas distintas. `add` mueve cambios al staging, donde decides qué entra en el siguiente commit. `commit` crea una foto permanente pero solo en tu repo local. `push` envía los commits al remoto, y solo entonces tus compañeros los ven. La separación permite hacer commits pequeños y limpios aunque hayas tocado muchos archivos.

**2. ¿Por qué trabajar en ramas y no commitear a `main`?**
`main` debe estar siempre estable porque de ahí salen los despliegues. Con ramas, cada cambio se desarrolla aislado, pasa revisión en un PR y se valida con CI antes de unirse. Los equipos suelen proteger `main` para impedir el push directo. Además permiten trabajo en paralelo y descartar experimentos sin rastro.

**3. ¿Qué significa `-u` en `git push -u origin rama`?**
*Set upstream*: enlaza la rama local con la remota. Después, `git push` y `git pull` funcionan sin argumentos y `git status` indica si estás adelantado o atrasado respecto al remoto. Solo hace falta la primera vez.

**4. ¿Qué es un Conventional Commit y por qué importa?**
Un formato de mensaje `tipo: descripción`. El historial se lee de un vistazo, se pueden generar changelogs automáticos y las herramientas de release calculan la versión según los tipos (`feat` sube minor, `fix` sube patch). Conecta directamente con release management.
