import pandas as pd
from utils import supabase, mapear_aula, extrair_relacionados, registrar_log_csv

CSV_ORIGINAL = "../data/input/aulas_tc_export.csv"
CSV_NAO_ENCONTRADAS = "../data/output/aulas_nao_encontradas.csv"
LOG_FILE = "../data/output/logs_criacao_aulas.csv"

def main():
    df_original = pd.read_csv(CSV_ORIGINAL)
    ids_faltantes = pd.read_csv(CSV_NAO_ENCONTRADAS)["id"].tolist()
    df_criar = df_original[df_original["id"].isin(ids_faltantes)]

    print(f"🚀 Criando {len(df_criar)} aulas...")

    for _, row in df_criar.iterrows():
        aula_payload = mapear_aula(row)
        aula_id = aula_payload["id"]
        
        try:
            # Upsert evita erro se a aula já existir por coincidência
            supabase.table("aulasTc").upsert(aula_payload).execute()
            
            # Tutores e Alunos
            tutores = extrair_relacionados(row, "Tutor", "tutores_Id", {"Pay rate": "payRate"})
            alunos = extrair_relacionados(row, "Student", "alunos_Id", {"Student attendance": "recipientAttendance", "Charge rate": "chargeRate"})
            
            if tutores: supabase.table("aulas_TutoresTc").upsert(tutores).execute()
            if alunos: supabase.table("aulas_AlunosTc").upsert(alunos).execute()
            print(f"✅ Aula {aula_id} processada.")
            
        except Exception as e:
            registrar_log_csv(LOG_FILE, aula_id, "criacao_completa", e, aula_payload)
            print(f"❌ Erro na aula {aula_id}")

if __name__ == "__main__":
    main()