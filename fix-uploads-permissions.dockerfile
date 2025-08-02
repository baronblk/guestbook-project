# Dockerfile um Upload-Berechtigungen zu korrigieren
# Version: 3.0.5-uploads-fix

FROM ghcr.io/baronblk/guestbook-project:3.0.4-portainer-logs

# Als root laufen um Berechtigungen zu setzen
USER root

# Upload-Verzeichnis Berechtigungen korrigieren
RUN mkdir -p /app/uploads && \
  chmod 755 /app/uploads && \
  chown -R www-data:www-data /app/uploads

# nginx muss auch auf die Dateien zugreifen können
RUN usermod -a -G www-data nginx || true

# Startup-Script erstellen für Runtime-Berechtigungen
RUN echo '#!/bin/bash\n\
  # Stelle sicher dass Upload-Verzeichnis existiert und korrekte Berechtigungen hat\n\
  mkdir -p /app/uploads\n\
  chmod 755 /app/uploads\n\
  chown -R www-data:www-data /app/uploads\n\
  \n\
  # Originales Startup-Script ausführen\n\
  exec "$@"' > /fix-permissions.sh && \
  chmod +x /fix-permissions.sh

# Neuer Entrypoint um Berechtigungen zur Laufzeit zu setzen
ENTRYPOINT ["/fix-permissions.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
