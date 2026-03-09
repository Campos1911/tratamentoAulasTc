import pandas as pd
import requests, time
from utils import supabase, mapear_aula, extrair_relacionados, registrar_log_csv

WEBHOOK_URL = "https://n8n-luma-n8n-teste.5ucjhf.easypanel.host/webhook/7fcb404f-9822-4702-a511-67573d645f3f"
CSV_DIVERGENCIAS = "../data/output/divergencias_links.csv"
CSV_ORIGINAL = "../data/input/aulas_tc_export.csv"

def main():
    try:
        df_div = pd.read_csv(CSV_DIVERGENCIAS)
        df_orig = pd.read_csv(CSV_ORIGINAL)
    except FileNotFoundError as e:
        print(f"❌ Erro: Arquivo não encontrado: {e}")
        return

    for _, row_div in df_div.iterrows():
        aula_id = row_div["id"]
        
        match = df_orig[df_orig["id"] == aula_id]
        if match.empty:
            registrar_log_csv("erro_links.csv", aula_id, "sync_link", "ID não encontrado no CSV original", {"id": aula_id})
            continue
        
        row = match.iloc[0]

        try:
            # 1. Mapeamento dos dados
            dados_aula = mapear_aula(row)
            tutores = extrair_relacionados(row, "Tutor", "tutores_Id", {"Pay rate": "payRate"})
            alunos = extrair_relacionados(row, "Student", "alunos_Id", {"Student attendance": "recipientAttendance", "Charge rate": "chargeRate"})
            
            # 2. Upsert na tabela principal (Aulas)
            supabase.table("aulasTc").upsert(dados_aula).execute()
            
            # 3. Tratamento de Tutores (Evitar Duplicidade)
            if tutores:
                # Forma garantida (Delete + Insert) para evitar duplicados sem depender de índices complexos:
                supabase.table("aulas_TutoresTc").delete().eq("aulas_Id", aula_id).execute()
                supabase.table("aulas_TutoresTc").insert(tutores).execute()

            # 4. Tratamento de Alunos (Evitar Duplicidade)
            if alunos:
                # Deleta as relações existentes para esta aula e insere as novas (mais seguro contra duplicados)
                supabase.table("aulas_AlunosTc").delete().eq("aulas_Id", aula_id).execute()
                supabase.table("aulas_AlunosTc").insert(alunos).execute()
            
            # 5. Lógica do Webhook
            status_aula = str(row.get("Status", "")).lower()
            if row_div["motivo"] == "conference_nao_existe" and "planejad" in status_aula:
                id_payload = int(aula_id) if str(aula_id).isdigit() else aula_id
                response = requests.post(WEBHOOK_URL, json={"aula_id": id_payload}, timeout=10)
                response.raise_for_status()
                
                print(f"🔗 Webhook enviado e registros sincronizados: {aula_id}")
                time.sleep(2) 
                
        except Exception as e:
            print(f"❌ Erro ao processar aula {aula_id}: {e}")
            registrar_log_csv("erro_links.csv", aula_id, "sync_link", str(e), {"id": aula_id})

if __name__ == "__main__":
    main()