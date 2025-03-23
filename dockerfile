# Usa uma imagem leve do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /gateway

# Copia apenas o arquivo de dependências para otimizar o cache
COPY requirements.txt /gateway/

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta do Flask
EXPOSE 5001

# Define o comando para rodar o app
CMD ["python", "run.py"]
