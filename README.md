# Verificador de Aulas (TutorCruncher → Banco de Dados)

Script em **Python** para verificar se as **aulas exportadas do TutorCruncher** estão registradas corretamente no banco de dados e se o **link da conferência está correto**.

O fluxo consiste em:

1. Exportar as aulas do **TutorCruncher**
2. Preparar o CSV exportado
3. Executar os scripts de verificação

---

# 📦 Estrutura do Projeto

```
.
├── data
│   ├── input
│   │   └── aulas_tc_export.csv
│   │
│   └── output
│       └── (arquivos gerados pelo script 01)
│
├── scripts
│   ├── 01_*.py
│   ├── 02_*.py
│   └── 03_*.py
│
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

---

# ⚙️ Pré-requisitos

Antes de começar, instale:

- **Python 3.9 ou superior**
- **pip**

Verifique:

```bash
python --version
pip --version
```

---

# 🚀 Instalação

Clone o repositório:

```bash
git clone <url-do-repositorio>
cd <nome-do-projeto>
```

---

# 📚 Instalar Dependências

Instale as dependências usando o `requirements.txt`.

```bash
pip install -r requirements.txt
```

---

# 🔐 Configurar Variáveis de Ambiente

O projeto utiliza variáveis de ambiente para acessar o **Supabase**.

## 1️⃣ Criar o `.env`

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Windows (PowerShell):

```powershell
copy .env.example .env
```

---

## 2️⃣ Preencher as variáveis

O `.env.example` possui:

```env
SUPABASE_URL=
SUPABASE_KEY=
```

Preencha com os dados do seu projeto:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-do-supabase
```

---

## 3️⃣ Onde encontrar no Supabase

1. Acesse seu projeto no Supabase
2. Vá em **Settings**
3. Clique em **API**
4. Copie:

- **Project URL → SUPABASE_URL**
- **Anon Key ou Service Role Key → SUPABASE_KEY**

⚠️ Nunca publique seu `.env` no repositório.

---

# 📥 Exportar Dados do TutorCruncher

Antes de rodar os scripts:

1. Exporte as aulas no **TutorCruncher**
2. Aplique os filtros:

- **Data desejada**
- **Status: Planejado**

---

# 📝 Preparar o CSV

Após baixar o CSV:

### 1️⃣ Renomeie o arquivo

```
aulas_tc_export.csv
```

---

### 2️⃣ Ajuste os nomes das colunas

| Coluna original | Novo nome     |
| --------------- | ------------- |
| ID              | id            |
| Link da aula    | conferenceUrl |

---

### 3️⃣ Coloque o arquivo na pasta

```
./data/input
```

Caminho final:

```
data/input/aulas_tc_export.csv
```

---

# ▶️ Executar os Scripts

Execute **na ordem correta**.

---

## 1️⃣ Script 01

Processa os dados iniciais do CSV.

```bash
python scr/01_nome_do_script.py
```

Saídas geradas em:

```
./data/output
```

---

## 2️⃣ Script 02

Processa os dados gerados pelo primeiro script.

```bash
python scr/02_nome_do_script.py
```

---

## 3️⃣ Script 03

Executa a verificação final das aulas no banco de dados.

```bash
python scr/03_nome_do_script.py
```

---

# ✅ Resultado Esperado

Ao final da execução, o sistema irá:

- Verificar se as **aulas do TutorCruncher existem no banco**
- Validar se o **link da conferência está correto**
- Identificar **inconsistências entre os dados**

---

# 🛠 Tecnologias Utilizadas

- Python
- Processamento de CSV
- Variáveis de ambiente (`.env`)
- Supabase
