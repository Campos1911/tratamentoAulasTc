import os, re, math, json, pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def parse_datetime(v):
    if pd.isna(v):
        return None
    try:
        dt = pd.to_datetime(v, dayfirst=True)          
        dt = dt + pd.Timedelta(hours=3) 
        return dt.isoformat()
    except:
        return None


def safe_int(v):
    try: 
        # Garante que converte floats como 20925257.0 para 20925257 antes de virar int
        return int(float(v)) if not pd.isna(v) else None
    except: 
        return None

def safe_float(v):
    if pd.isna(v) or v is None or str(v).strip() == "": 
        return None
    if isinstance(v, (int, float)): 
        return float(v)
    
    # Remove R$, espaços e caracteres não numéricos, preservando ponto e vírgula
    v_str = re.sub(r"[^\d,.-]", "", str(v).replace("R$", ""))
    
    if not v_str: return None

    # Tratamento de padrão brasileiro (1.250,50 -> 1250.50)
    if "," in v_str and "." in v_str:
        v_str = v_str.replace(".", "").replace(",", ".")
    elif "," in v_str:
        v_str = v_str.replace(",", ".")
        
    try:
        return float(v_str)
    except ValueError:
        return None

def clean_payload(data):
    # Melhorei para lidar com qualquer tipo de "vazio" que o Supabase rejeita
    return {k: (None if pd.isna(v) or v == "" or (isinstance(v, float) and math.isnan(v)) else v) for k, v in data.items()}

def registrar_log_csv(arquivo, aula_id, etapa, erro, payload):
    existe = os.path.isfile(arquivo)
    with open(arquivo, mode="a", newline="", encoding="utf-8") as f:
        pd.DataFrame([{
            "timestamp": datetime.utcnow().isoformat(),
            "aula_id": aula_id, "etapa": etapa, "erro": str(erro),
            "payload": json.dumps(payload, default=str, ensure_ascii=False)
        }]).to_csv(f, header=not existe, index=False)

def mapear_aula(row):
    return clean_payload({
        "id": safe_int(row["id"]), 
        "start": parse_datetime(row["Start"]),
        "finish": parse_datetime(row["Finish"]), 
        "units": safe_float(row["Units"]),
        "topic": row.get("Topic"), 
        "jobs_Id": safe_int(row.get("Job ID")),
        "status": row.get("Status"), 
        "disciplina": row.get("Disciplina (disciplina_1)"),
        "tipo_aula": row.get("Tipo Aula (tipo_aula)"), 
        "deleted": False
    })

def extrair_relacionados(row, prefixo, id_db, campos_map):
    lista = []
    for i in range(1, 11):
        item_id = safe_int(row.get(f"{prefixo} ID {i}"))
        if not item_id: continue
        
        payload = {"aulas_Id": safe_int(row["id"]), id_db: item_id, "removed": False}
        
        for csv_col, db_col in campos_map.items():
            val = row.get(f"{csv_col} {i}")
            
            col_nome_lower = str(csv_col).lower()
            db_nome_lower = str(db_col).lower()
            
            if "rate" in col_nome_lower or "rate" in db_nome_lower:
                res = safe_float(val)
            else:
                res = val
                
            payload[db_col] = res
            
        lista.append(clean_payload(payload))
    return lista