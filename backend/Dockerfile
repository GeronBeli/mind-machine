# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container to /usr/src/app
WORKDIR /usr/src/app/

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-deu \
    pngquant \
    unpaper \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download and build Ghostscript 10.05.1 from source
RUN wget https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10051/ghostscript-10.05.1.tar.gz && \
    tar -xzf ghostscript-10.05.1.tar.gz && \
    cd ghostscript-10.05.1 && \
    ./configure && \
    make -j$(nproc) && \
    make install && \
    cd .. && \
    rm -rf ghostscript-10.05.1 ghostscript-10.05.1.tar.gz




# Copy only the requirements.txt first to leverage Docker cache
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000


# Run the Python script to start the app
CMD python main.py