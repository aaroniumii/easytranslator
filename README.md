# Easy Translator

Aplicación web sencilla que utiliza un proveedor de modelos (OpenAI o Gemini) para traducir textos entre idiomas y corregir gramática, ortografía y lógica dentro de un mismo idioma.

## Requisitos

- Python 3.11+
- Una clave válida de la API del proveedor que desees usar (OpenAI o Gemini)

## Configuración

1. Copia el archivo `.env.example` a `.env` y actualiza los valores necesarios.

```bash
cp .env.example .env
```

2. Edita `.env` e introduce tus credenciales:
   - Define `LLM_PROVIDER` con el valor `openai` o `gemini`.
   - Si utilizas OpenAI, especifica `OPENAI_API_KEY` y, opcionalmente, el modelo (`OPENAI_MODEL`) y el tiempo máximo de espera (`OPENAI_TIMEOUT`).
   - Si utilizas Gemini, especifica `GEMINI_API_KEY`. Opcionalmente, puedes ajustar el modelo (`GEMINI_MODEL`) o desactivar el pensamiento con `GEMINI_DISABLE_THINKING=true`.

## Ejecución local

Instala las dependencias y ejecuta el servidor con Uvicorn.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abre tu navegador y visita `http://localhost:8000` para acceder a la interfaz web.

## Ejecución con Docker Compose

1. Asegúrate de tener Docker y Docker Compose instalados.
2. Exporta tu clave de API de OpenAI en el entorno actual.

```bash
export OPENAI_API_KEY="tu_clave"
```

3. Levanta los servicios.

```bash
docker compose up --build
```

El traductor estará disponible en `http://localhost:8000`.

## Uso de la API

### Traducción

- **Endpoint:** `POST /api/translate`
- **Payload:**

```json
{
  "text": "Hola mundo",
  "source_language": "Español",
  "target_language": "Inglés"
}
```

- **Respuesta:**

```json
{
  "translated_text": "Hello world"
}
```

### Corrección

- **Endpoint:** `POST /api/correct`
- **Payload:**

```json
{
  "text": "Este es un texto con erorres",
  "language": "Español"
}
```

- **Respuesta:**

```json
{
  "corrected_text": "Este es un texto con errores"
}
```

## Licencia

Este proyecto se distribuye bajo la licencia MIT.
