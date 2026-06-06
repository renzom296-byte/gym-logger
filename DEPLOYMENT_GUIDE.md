# 💪 Gym Logger - Guía de Deployment

App de registro de cargas en Streamlit Cloud conectada a Supabase.

---

## 🚀 PASO 1: Preparar Supabase

### 1.1 Crear proyecto en Supabase (si no lo tienes)
1. Entra a [supabase.com](https://supabase.com)
2. Click en "Start your project"
3. Crea una cuenta o inicia sesión
4. Crea un nuevo proyecto
5. Anota la **URL del proyecto** y la **API Key (anon)**

### 1.2 Crear tablas en Supabase
1. En Supabase, ve a **SQL Editor**
2. Click en **New Query**
3. Copia TODO el contenido del archivo `supabase_setup.sql`
4. Pega en el editor y ejecuta
5. ¡Listo! Tus tablas están creadas

**Qué hace este SQL:**
- Crea tabla `routines`: tus ejercicios definidos
- Crea tabla `workout_logs`: cada registro de entrenamiento
- Crea índices para mejor rendimiento

---

## 🌐 PASO 2: Desplegar en Streamlit Cloud

### 2.1 Preparar repositorio en GitHub
1. Crea una carpeta en tu computadora: `gym-logger`
2. Dentro, copia estos archivos:
   - `gym_logger_app.py` (renómbralo a `app.py`)
   - `requirements.txt`
3. Crea un archivo `.gitignore` con esto:
   ```
   .streamlit/secrets.toml
   __pycache__/
   *.pyc
   ```

4. Sube todo a GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/tu-usuario/gym-logger.git
   git push -u origin main
   ```

### 2.2 Desplegar en Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Click en **Create app** (arriba a la derecha)
3. **GitHub repo**: `tu-usuario/gym-logger`
4. **Branch**: `main`
5. **File path**: `app.py`
6. Click en **Deploy**

⏳ Espera a que termine el deployment (1-2 minutos)

### 2.3 Configurar Secrets en Streamlit Cloud
1. Una vez deployada, ve a **⋯** (3 puntos) arriba a la derecha
2. Click en **Settings**
3. Ve a la pestaña **Secrets**
4. Pega esto, reemplazando con tus credenciales de Supabase:
   ```
   supabase_url = "https://tu-proyecto.supabase.co"
   supabase_key = "tu-anon-key-aqui"
   ```
5. Click en **Save**

⚠️ **IMPORTANTE**: 
- Usa tu **anon key**, NO la service role key
- Nunca compartas estas credenciales
- Están seguradas en Streamlit Cloud

6. La app se reiniciará automáticamente

---

## ✅ PASO 3: Verificar que funciona

1. Entra a tu app en Streamlit Cloud
2. En el sidebar, ve a **Configuración de Rutina**
3. Agrega un ejercicio: "Press de Banca"
4. Ve a **Registrar** y registra:
   - Peso: 80 kg
   - Reps: 8
   - RIR: 2
   - Dropset: No marcado
5. Click en **Guardar Registro**
6. Verifica que aparece en **Historial**

¡Si todo funciona, estás listo! 🎉

---

## 📱 Cómo usar la app

### Tab "Registrar" (📝)
- Selecciona ejercicio de tu rutina
- Ingresa: peso, reps, RIR (opcional), si hay dropset
- Agrega notas (por qué te pareció fácil/difícil)
- Click en **Guardar Registro**

### Tab "Dashboard" (📊)
- Resumen: total registros, peso máximo
- Gráficos de registros por ejercicio
- Contador de dropsets

### Tab "Progreso" (📈)
- Selecciona un ejercicio
- Ve gráficos de evolución: peso, reps, volumen
- Métricas: progreso total, días

### Tab "Historial" (📋)
- Tabla con todos tus registros
- Filtra por ejercicio y fechas
- Descarga como CSV

### Sidebar "Configuración de Rutina"
- Agrega ejercicios nuevos a tu rutina
- Elimina ejercicios que no uses
- Solo aparecen en "Registrar" los ejercicios de la rutina

---

## 🔄 Actualizar la app

Si modificas el código:

1. Edita `app.py` localmente
2. Guarda los cambios
3. Pushea a GitHub:
   ```bash
   git add .
   git commit -m "Descripción del cambio"
   git push
   ```
4. La app en Streamlit Cloud se actualiza automáticamente

---

## 🐛 Solución de problemas

**Error: "No module named supabase"**
- Verifica que `requirements.txt` está en el repositorio
- Streamlit Cloud instalará automáticamente, puede tardar 1-2 min

**Error: "Supabase connection error"**
- Verifica que copiaste la URL y key correcta
- Está en Supabase > Project Settings > API
- Asegúrate que las variables están en **Secrets** de Streamlit Cloud

**Datos no se guardan**
- Verifica que ejecutaste el SQL de `supabase_setup.sql`
- Las tablas deben existir en Supabase

**App es muy lenta**
- La primera carga es lenta (Streamlit inicia serverless)
- Las siguientes cargas son más rápidas
- Si está muy lenta, puede haber problema de conexión a Supabase

**¿Quiero hacer cambios locales antes de pushear?**
```bash
# Crea carpeta .streamlit
mkdir .streamlit

# Copia secrets_ejemplo.toml como secrets.toml
cp secrets_ejemplo.toml .streamlit/secrets.toml

# Edita .streamlit/secrets.toml con tus credenciales

# Ejecuta localmente
streamlit run app.py

# ¡Ahora puedes probar cambios antes de subirlos a GitHub!
```

---

## 📊 Qué registra cada vez

- **Ejercicio**: De tu rutina (selector)
- **Fecha**: Puedes cambiarla, por defecto hoy
- **Peso**: En kg (ej: 80)
- **Reps**: Repeticiones que hiciste (ej: 8)
- **RIR**: Reps In Reserve - cuántas reps más podrías haber hecho (ej: si hiciste 8 pero podías 10, RIR=2)
- **Dropset**: ¿Hiciste dropset? Checkbox
- **Notas**: Texto libre - cómo te sentiste, si fue difícil, etc

---

## 💡 Tips

✅ Sé consistente con los nombres de ejercicios
✅ RIR es útil para medir tu esfuerzo real (no solo peso)
✅ Notas te ayudan a recordar cómo te sentiste
✅ Descarga periódicamente como backup
✅ Mira los gráficos para ver tu progreso real

---

## 🆘 Contacto / Soporte

Si tienes problemas:
1. Verifica que copiaste correctamente la URL y key de Supabase
2. Revisa que el SQL se ejecutó sin errores
3. Asegúrate que las variables están en Secrets (no en el código)
4. Intenta redeployal app desde Streamlit Cloud

---

¡A entrenar! 💪
