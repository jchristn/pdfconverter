FROM python:3.11-slim

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and tools
RUN apt-get update && apt-get install -y \
    # LibreOffice and related packages
    libreoffice \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    libreoffice-draw \
    libreoffice-math \
    libreoffice-base \
    libreoffice-common \
    libreoffice-core \
    libreoffice-help-en-us \
    # Fonts
    fonts-liberation \
    fonts-liberation2 \
    # X11 and virtual display
    xvfb \
    # Locale dependencies
    locales \
    # Common tools
    iputils-ping \
    traceroute \
    dnsutils \
    vim \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Configure locales
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG="en_US.UTF-8"
ENV LANGUAGE="en_US:en"
ENV LC_ALL="en_US.UTF-8"

# Set up LibreOffice user directory
RUN mkdir -p /root/.config/libreoffice/4/user

# Create a basic user profile for LibreOffice
RUN echo '[Bootstrap]' > /root/.config/libreoffice/4/user/registrymodifications.xcu && \
    echo 'UserInstallation=$SYSUSERCONFIG/libreoffice/4/user' >> /root/.config/libreoffice/4/user/registrymodifications.xcu

# Set environment variables for Xvfb
ENV DISPLAY=":99"
ENV SCREEN_NUM="0"
ENV SCREEN_WHD="1280x1024x24"
ENV XVFB_WHD="1280x1024x24"

# Create directory for the application
WORKDIR /app

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose FastAPI port
EXPOSE 8000

# Create startup script
RUN echo '#!/bin/bash\n\
Xvfb :99 -screen 0 1280x1024x24 -ac +extension GLX +render -noreset &\n\
sleep 1\n\
python app.py' > /app/start.sh && \
chmod +x /app/start.sh

# Set the entrypoint to our startup script
CMD ["/app/start.sh"]