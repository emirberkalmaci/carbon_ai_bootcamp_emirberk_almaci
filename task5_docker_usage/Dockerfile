FROM python:3.9-slim

WORKDIR /task2_docker

COPY requirements.txt /task2_docker
RUN pip install --no-cache-dir -r requirements.txt

COPY task2_rag_system /task2_docker

EXPOSE 2121

CMD ["streamlit", "run", "/task2_docker/task2_script.py", "--server.port=2121", "--server.baseUrlPath=chat"]