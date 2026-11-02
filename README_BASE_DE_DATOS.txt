CAMPUSCONECTA - BASE DE DATOS EN ARCHIVOS QUE PUEDES ABRIR CON BLOC DE NOTAS

COMO INICIAR:
1. Descomprime la carpeta completa.
2. Debes tener Python 3 instalado en Windows.
3. Haz doble clic en iniciar_campusconecta.bat.
4. Deja abierta la ventana negra del servidor.
5. Abre tu navegador en http://127.0.0.1:8000
6. Usa CampusConecta normalmente. Los cambios se guardan en la carpeta base_de_datos.

ARCHIVOS:
- base_de_datos.json: copia consolidada de los datos.
- cc_users.json: cuentas y perfiles.
- cc_posts.json: publicaciones, fotos codificadas, comentarios y Me gusta.
- cc_groups.json: grupos.
- cc_history.json: historial de actividad.
- También se crean archivos cc_* adicionales para mensajes, notificaciones, calendario,
  seguidores y otros datos que la aplicación guarde con ese prefijo.

IMPORTANTE:
- Abre los archivos .json con Bloc de notas para consultar los datos. No cambies su estructura
  mientras la página está abierta; un JSON mal formado puede impedir que se cargue.
- No compartas archivos que contengan datos privados o contraseñas.
- Esta es una base de datos local para una demostración educativa. Solo funciona en esta
  computadora y no hace que otros estudiantes se conecten por internet.
- Para detener el servidor, vuelve a la ventana negra y presiona Ctrl+C.
- Si al hacer doble clic en el .bat aparece que no encuentra Python, instala Python 3 y vuelve
  a intentarlo.
