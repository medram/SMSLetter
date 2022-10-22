FROM python:3.8-slim

ENV USER=django
ENV PATH=${PATH}:/home/${USER}/.local/bin
ENV WORKERS=4

WORKDIR /app

# Updating system packages
RUN apt-get update && apt-get upgrade -y \
	&& apt-get install curl -y \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Create a user for django web application.
RUN useradd -m ${USER} && chown -R ${USER}:${USER} /app
USER ${USER}

# install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

# Copy all django files
COPY --chown=${USER}:${USER} . .

# Assets / static files
RUN python3 manage.py collectstatic --no-input --skip-checks

# Fixing files & folders permissions
RUN find . -type d -exec chmod 775 {} \; \
	&& find . -type f -exec chmod 664 {} \;

# Default port
ENV PORT=80

VOLUME ["/app"]
EXPOSE ${PORT}

HEALTHCHECK --interval=15s --timeout=14s --start-period=5s CMD curl -fsSLI http://127.0.0.1:${PORT} | grep -q "200 OK" || false

CMD gunicorn --bind 0.0.0.0:${PORT} -w ${WORKERS} app.wsgi
