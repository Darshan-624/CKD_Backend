-- 1. Profiles (Permanent Data: Demographics + Medical History)
create table public.profiles (
  id uuid references auth.users not null primary key,
  name text,
  contact text,
  age int,                -- Stored permanently as requested
  gender text,            -- 'male' or 'female'
  hypertension int,       -- 1 = Yes, 0 = No
  diabetes int,           -- 1 = Yes, 0 = No
  created_at timestamp with time zone default timezone('utc'::text, now())
);

-- 2. Health Records (Single Block: Vitals + Labs for every checkup)
create table public.health_records (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references public.profiles(id) not null,
  specific_gravity float,
  albumin float,
  blood_glucose float,
  serum_creatinine float,
  sodium float,
  hemoglobin float,
  packed_cell_volume float,
  red_blood_cell_count float,
  entry_date timestamp with time zone default timezone('utc'::text, now())
);

-- 3. Predictions (Linked to a specific Health Record)
create table public.predictions (
  id uuid default uuid_generate_v4() primary key,
  record_id uuid references public.health_records(id) not null,
  user_id uuid references public.profiles(id) not null,
  ckd_prediction text,      -- 'Yes' or 'No'
  risk_probability float,   -- e.g., 0.998
  ckd_stage text,           -- e.g., 'Stage 3b'
  egfr_value float,         -- Calculated eGFR
  top_factors jsonb,        -- List of influencing factors (SHAP)
  created_at timestamp with time zone default timezone('utc'::text, now())
);
