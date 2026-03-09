import pandas as pd
from utils import supabase

def buscar_lote(tabela, coluna, ids):
    res = []
    for i in range(0, len(ids), 500):
        batch = ids[i:i+500]
        data = supabase.table(tabela).select("*").in_(coluna, batch).execute()
        res.extend(data.data)
    return res

def main():
    df_csv = pd.read_csv("../data/input/aulas_tc_export.csv")
    ids = df_csv["id"].dropna().unique().tolist()

    db_aulas = {a["id"]: a for a in buscar_lote("aulasTc", "id", ids)}
    db_confs = {c["aula_id"]: c for c in buscar_lote("conference_meet", "aula_id", ids)}

    nao_encontradas, divergencias = [], []

    for _, row in df_csv.iterrows():
        aid, l_csv = row["id"], str(row["conferenceUrl"]).strip()
        
        if aid not in db_aulas:
            nao_encontradas.append({"id": aid, "motivo": "aula_nao_existe"})
            continue
        
        conf = db_confs.get(aid)
        if not conf:
            divergencias.append({"id": aid, "motivo": "conference_nao_existe", "link_csv": l_csv})
        elif str(conf.get("conferenceUrl")).strip() != l_csv:
            divergencias.append({"id": aid, "motivo": "link_diferente", "link_csv": l_csv})

    pd.DataFrame(nao_encontradas).to_csv("../data/output/aulas_nao_encontradas.csv", index=False)
    pd.DataFrame(divergencias).to_csv("../data/output/divergencias_links.csv", index=False)
    print(f"✅ Fim. Faltam: {len(nao_encontradas)} | Divergentes: {len(divergencias)}")

if __name__ == "__main__":
    main()