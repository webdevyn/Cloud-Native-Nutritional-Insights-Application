FROM python:3.9-slim
WORKDIR /app

# Copy backend and frontend explicitly
COPY project2_nutritional_insights/backend /app
COPY project2_nutritional_insights/frontend /app/frontend

COPY project2_nutritional_insights/backend/requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
