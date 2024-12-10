# Use Ubuntu as the base image
FROM ubuntu:22.04

# Install required system dependencies for GUI and PySide6
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libxkbcommon0 \
    libegl1-mesa \
    libgles2-mesa \
    libqt5gui5 \
    libqt5widgets5 \
    libqt5core5a \
    libxrender1 \
    libxi6 \
    x11-utils \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxcb-keysyms1 \
    libxcb-render-util0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-shm0 \
    && apt-get clean

# Set environment variables
ENV QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/qt6/plugins/platforms
ENV QT_XCB_GL_INTEGRATION=xcb_egl
ENV QT_DEBUG_PLUGINS=1
ENV QT_QPA_PLATFORM=offscreen


# Set working directory in the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy your application code
COPY skeleton.py /app/skeleton.py

# Set the default command to run your app
CMD ["python3", "/app/skeleton.py"]
