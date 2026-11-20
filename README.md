# Academia de Idiomas · Módulo para Odoo 19

Módulo de Odoo (Python + XML) para gestionar una academia de idiomas: cursos, sesiones, clases, alumnos, profesores, matrículas y facturación.

## Funcionalidades

- **Cursos y sesiones**: cada curso tiene sesiones con fecha, duración y número de plazas.
- **Ocupación calculada**: plazas libres y porcentaje de ocupación de cada sesión se calculan automáticamente (campos `compute`).
- **Validaciones de negocio** (`@api.constrains`):
  - no se pueden inscribir más alumnos que plazas tiene la sesión;
  - un profesor no puede tener dos sesiones que se solapen en el tiempo.
- **Matrículas con flujo de estados**: borrador → confirmada → pagada, con botones de acción.
- **Facturación** por alumno y curso, con estado del pago.
- **Vistas**: listas, formularios, kanban y calendario de sesiones.

## Modelo de datos

| Modelo | Relaciones principales |
| --- | --- |
| `academia.curso` | profesor, sesiones, clases, facturas |
| `academia.sesion` | curso, profesor, alumnos (Many2many) |
| `academia.clase` | curso, profesor, alumnos; día y franja horaria |
| `academia.alumno` | sesiones, clases, matrículas, facturas |
| `academia.profesor` | cursos, sesiones, clases |
| `academia.matricula` | alumno + sesión, con estado |
| `academia.facturacion` | alumno + curso, importe y estado |

## Instalación

1. Copia la carpeta `academia` en el directorio de addons de tu Odoo 19.
2. Reinicia Odoo y actualiza la lista de aplicaciones (modo desarrollador).
3. Busca **Academia de Idiomas** e instálala.

## Tecnologías

Python 3, ORM de Odoo, vistas XML, control de acceso con `ir.model.access.csv`.
