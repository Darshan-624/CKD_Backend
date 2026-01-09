# app/db/supabase.py
from supabase import create_client, Client
from app.core.config import settings

# Initialize Supabase Client
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
# 21
# male
# 1.01
# 2
# 180
# 2.3
# 136
# 9.5
# 30.5
# 3.5
# 1
# 1