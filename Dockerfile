# BASE MAGE
FROM python:3.11

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
    libegl1-mesa  \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables for Qt and X11
ENV QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/qt5/plugins/platforms
ENV QT_XCB_GL_INTEGRATION=xcb_egl
ENV QT_QPA_PLATFORM=minimal
ENV DISPLAY=:99

# Set working directory
WORKDIR /app

# Copy application and test files
COPY requirements.txt /app/requirements.txt
COPY skeleton.py /app/skeleton.py
COPY skeleton_unit_testing.py /app/skeleton_unit_testing.py

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app
ENV PYTHONWARNINGS="ignore::DeprecationWarning"

# Set the default command to run the application
CMD ["python3", "/app/skeleton.py"]
