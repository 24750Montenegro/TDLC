FROM python:3.14-slim

# graphviz trae el binario dot, que es lo unico que no se puede instalar con pip;
# fonts-dejavu-core es la fuente monoespaciada que usa el grafo (Consolas no existe aqui)
RUN apt-get update \
    && apt-get install -y --no-install-recommends graphviz fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    AFN_FUENTE="DejaVu Sans Mono"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "shuntingyard.py"]
