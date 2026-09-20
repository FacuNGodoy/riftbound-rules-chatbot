# Publicar en Render

Hugging Face (Docker) ahora es pago. Este proyecto se publica como **Web Service** en Render.

## A. GitHub (hace falta: Render lee el repo)

1. Entrá a https://github.com/new
2. Repository name: `riftbound-rules-chatbot`
3. **Public**
4. **No** marques “Add a README” (ya hay uno)
5. Create repository

Después avisame y empujamos el código, o seguí B cuando el repo ya tenga archivos.

## B. Render

1. https://render.com → Sign up / Log in (podés usar **GitHub**).
2. Autorizá a Render a ver el repo `riftbound-rules-chatbot`.
3. Dashboard → **New** → **Web Service**.
4. Elegí el repo.
5. Settings:
   - Name: `riftbound-rules-chatbot`
   - Language / Runtime: **Docker**
   - Instance type: **Free**
   - Branch: `main`
6. **Environment Variables**:
   - `GEMINI_API_KEY` = tu clave de Google AI Studio (no la dejes visible en el repo)
   - `RIFTBOUND_VISION_PROVIDER` = `gemini`
7. **Create Web Service**

El primer deploy tarda varios minutos. El índice Chroma ya viene construido y
el servidor no instala PyTorch, porque el plan gratuito tiene 512 MB.

Cuando ponga **Live**, la URL es la de la app. El health check es `/health`.

Gemini recibe las fotos para identificar número y nombre. El backend cruza esa
identidad con `cards.json`; el texto de reglas de la carta no sale de la memoria
del modelo.

Si el build falla por RAM o timeout, mandame el log y lo ajustamos.
