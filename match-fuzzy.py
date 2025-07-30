# Instalar bibliotecas necessárias
!pip install --quiet thefuzz[speedup] pandas-gbq google-auth

import pandas as pd
from thefuzz import process, fuzz
from google.colab import auth

# 1️⃣ Autenticação no Google
auth.authenticate_user()

# Bases fictícias com empresas, nomes e endereços
base_a = pd.DataFrame({
    'registro': [
        'Tech Solutions LTDA',
        'Alpha Digital Serviços ME',
        'João Paulo da Silva',
        'Maria Aparecida Souza',
        'Av. Paulista, 1234 – São Paulo'
    ]
})

base_b = pd.DataFrame({
    'registro': [
        'Tech Solutions',
        'Alpha Digital Serv.',
        'João P. Silva',
        'Maria Souza',
        'Avenida Paulista 1234 SP'
    ]
})

# Normalizar os textos
base_a['registro_norm'] = base_a['registro'].str.lower().str.strip()
base_b['registro_norm'] = base_b['registro'].str.lower().str.strip()

# Matching com emojis e sugestão
matches = []
for original in base_a['registro_norm']:
    match = process.extractOne(original, base_b['registro_norm'], scorer=fuzz.token_set_ratio)
    if match:
        similaridade = match[1]

        # Classificação da aderência com emojis
        if similaridade >= 90:
            status = "🔹 Alta aderência ✅"
        elif similaridade >= 80:
            status = "🟠 Aderência média ⚠️"
        else:
            status = "🔴 Baixa aderência ❌"

        matches.append({
            'Registro Base A': original.title(),
            'Melhor Match Base B': match[0].title(),
            'Similaridade (%)': f"{similaridade}%",
            'Status': status
        })

# Criar dataframe e ordenar
resultado = pd.DataFrame(matches)
resultado = resultado.sort_values(by='Similaridade (%)', ascending=False).reset_index(drop=True)

print("\n🔎 Resultado dos Matches com análise:\n")
resultado
