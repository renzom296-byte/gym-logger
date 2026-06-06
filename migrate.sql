-- Agregar grupo muscular a rutinas
ALTER TABLE routines ADD COLUMN IF NOT EXISTS muscle_group TEXT DEFAULT 'Sin grupo';

-- Agregar unidad original al log (el peso siempre se guarda en kg)
ALTER TABLE workout_logs ADD COLUMN IF NOT EXISTS unit TEXT DEFAULT 'kg';

-- Grupos musculares de ejemplo PPL (opcional, puedes editarlos desde la app)
-- UPDATE routines SET muscle_group = 'Empuje' WHERE exercise_name IN ('Press de Banca', 'Press Hombro');
-- UPDATE routines SET muscle_group = 'Jale'   WHERE exercise_name IN ('Dominadas', 'Remo Barra');
-- UPDATE routines SET muscle_group = 'Piernas' WHERE exercise_name IN ('Sentadillas', 'Peso Muerto');
