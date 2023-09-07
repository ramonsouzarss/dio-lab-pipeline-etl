import pandas as pd
import requests
import json
import openai

sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

# Carrega os dados da planilha
df = pd.read_csv('SDW2023.csv')

# Extrai a lista de IDs de usuários
user_ids = df['UserID'].tolist()
print(user_ids)

# Obtem os dados de usuário usando a API
def get_user(id):
    response = requests.get(f'{sdw2023_api_url}/users/{id}')
    return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))

# Integração com o ChatGPT
openai_api_key = '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'
openai.api_key = openai_api_key

# Mensagem de marketing
def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system", 
                "content": "Você é um especialista em marketing bancário para clientes pessoa-física."
            },
            {
                "role": "user", 
                "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres)."
            }
        ]
    )
    return completion.choices[0].message.content.strip('\"')

# Mensagem de funcionalidades
def generate_ai_features(user):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system", 
                "content": "Você é um especialista em crédito bancário para clientes pessoa-física."
            },
            {
                "role": "user", 
                "content": f"Crie uma mensagem para {user['name']} sobre os benefícios de utilizar o crédito oferecido pelo banco de forma inteligente e todas as funcionalidades do cartão de crédito (máximo de 100 caracteres)."
            }
        ]
    )
    return completion.choices[0].message.content.strip('\"')

for user in users:
    news = generate_ai_news(user)
    print(news)
    user['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": news
    })
    features = generate_ai_features(user)
    print(features)
    user['features'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": features
    })

# Atualiza a lista de "news" e "features" de cada user na API com as mensagens gerada pelo ChatGPT
def update_user(user):
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False

for user in users:
    success = update_user(user)
    print(f"User {user['name']} updated? {success}")
