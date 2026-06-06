-- Tabla de Rutinas (ejercicios definidos)
CREATE TABLE routines (
  id BIGSERIAL PRIMARY KEY,
  exercise_name VARCHAR(255) NOT NULL UNIQUE,
  target_sets INT NOT NULL DEFAULT 3,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de Registros de Entrenamiento
CREATE TABLE workout_logs (
  id BIGSERIAL PRIMARY KEY,
  exercise_name VARCHAR(255) NOT NULL REFERENCES routines(exercise_name),
  date DATE NOT NULL,
  weight DECIMAL(10, 2) NOT NULL,
  reps INT NOT NULL,
  rir INT,
  is_dropset BOOLEAN DEFAULT FALSE,
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_workout_logs_exercise ON workout_logs(exercise_name);
CREATE INDEX idx_workout_logs_date ON workout_logs(date);

-- Insertar ejercicios de ejemplo (OPCIONAL - elimina esto si quieres empezar vacío)
INSERT INTO routines (exercise_name, target_sets) VALUES
  ('Press de Banca', 3),
  ('Sentadillas', 4),
  ('Peso Muerto', 3),
  ('Dominadas', 3),
  ('Press Hombro', 3),
  ('Remo Barra', 4);
