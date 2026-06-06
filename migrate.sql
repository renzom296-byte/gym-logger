-- Agregar grupo muscular a rutinas
ALTER TABLE routines ADD COLUMN IF NOT EXISTS muscle_group TEXT DEFAULT 'Sin grupo';

-- Columnas de peso dual + unidad con la que se ingresó
ALTER TABLE workout_logs ADD COLUMN IF NOT EXISTS weight_kg  DECIMAL(10,2);
ALTER TABLE workout_logs ADD COLUMN IF NOT EXISTS weight_lb  DECIMAL(10,2);
ALTER TABLE workout_logs ADD COLUMN IF NOT EXISTS unit       TEXT DEFAULT 'kg';

-- Migrar registros existentes: la columna weight ya era kg
UPDATE workout_logs
SET
    weight_kg = weight,
    weight_lb = ROUND((weight * 2.20462)::NUMERIC, 2),
    unit      = 'kg'
WHERE weight_kg IS NULL;

-- Grupos musculares de ejemplo PPL (opcional)
-- UPDATE routines SET muscle_group = 'Empuje'  WHERE exercise_name IN ('Press de Banca', 'Press Hombro');
-- UPDATE routines SET muscle_group = 'Jale'    WHERE exercise_name IN ('Dominadas', 'Remo Barra');
-- UPDATE routines SET muscle_group = 'Piernas' WHERE exercise_name IN ('Sentadillas', 'Peso Muerto');
