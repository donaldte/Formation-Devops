# ============================================================
# STAGE 1 — BUILDER
# ============================================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY ../../requirements.txt /app/requirements.txt

# Install Python dependencies in a clean isolated folder
RUN pip install --upgrade pip \
    && pip install --prefix=/install -r /app/requirements.txt


# ============================================================
# STAGE 2 — RUNTIME
# ============================================================
FROM python:3.11-slim AS runtime

WORKDIR /app

# Create non-root user for security
RUN useradd -m appuser

# Copy installed dependencies
COPY --from=builder /install /usr/local

# Copy application code
COPY ./app /app/app

# Set working directory and permissions
RUN chown -R appuser:appuser /app

USER appuser

# Expose FastAPI default port
EXPOSE 8000

# HEALTHCHECK — Optional but recommended
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# ============================================================
# COMMAND
# ============================================================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
