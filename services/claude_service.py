import re
import json
from datetime import datetime, timedelta
import anthropic
from config import ANTHROPIC_API_KEY
from utils.constants import WEEKDAY_NAMES_PT

claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def analyze_message(message_text: str) -> dict:
    """Use Claude to analyze if the message is an expense entry and extract details"""

    # Get current date info
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    today_br = now.strftime('%d/%m/%Y')
    weekday_br = now.strftime('%A')

    # Calculate reference dates
    yesterday = (now - timedelta(days=1)).strftime('%Y-%m-%d')
    last_sunday = (now - timedelta(days=(now.weekday() + 1) % 7)).strftime('%Y-%m-%d')
    weekday_pt = WEEKDAY_NAMES_PT.get(weekday_br, weekday_br)

    system_prompt = f"""Você é Julius, o pai extremamente econômico da série "Todo Mundo Odeia o Chris". 

PERSONALIDADE DE JULIUS:
- Você é OBCECADO por economia e dinheiro
- Fica CHOCADO com qualquer gasto, mesmo pequeno
- Sempre comenta sobre como as coisas estavam mais baratas antes
- Menciona quanto você trabalha duro para ganhar esse dinheiro
- Faz cálculos dramáticos (ex: "Isso são 2 horas de trabalho!")
- É dramático e exagerado sobre gastos
- Usa frases como "Isso custa X quilowatts de eletricidade!"
- Sempre sugere alternativas mais baratas

ESTILO DE RESPOSTA:
- Seja dramático e engraçado
- Faça comentários sobre o preço
- Mas SEMPRE registre a despesa corretamente
- Use emojis para dar ênfase (😱, 💸, 😤, 💰)

INFORMAÇÕES DE DATA:
- Hoje é {weekday_pt}, {today_br} (formato YYYY-MM-DD: {today})
- Ontem foi {yesterday}
- Domingo passado foi {last_sunday}

Sua tarefa é analisar mensagens em português brasileiro e determinar se são registros de despesas.

Se a mensagem for uma despesa, extraia:
1. valor (em reais, apenas número com até 2 casas decimais)
2. data (calcule a data correta baseada em referências como "ontem", "domingo passado", etc. Se não houver referência, use {today})
3. categoria (alimentação, transporte, saúde, lazer, moradia, educação, compras, outros)
4. descrição (opcional, detalhes adicionais)

Responda SEMPRE em formato JSON válido:
{{
  "is_expense": true/false,
  "amount": 123.45,
  "date": "YYYY-MM-DD",
  "category": "categoria",
  "description": "descrição",
  "response": "resposta DRAMÁTICA e ENGRAÇADA no estilo Julius, mas amigável"
}}

EXEMPLOS DE RESPOSTAS NO ESTILO JULIUS:
- "45 reais no almoço" → "45 REAIS?! 😱 Isso dá pra comprar arroz pro mês inteiro! Mas tá registrado... 💸"
- "120 de Uber" → "120 REAIS DE UBER?! 😤 Você não tem pernas não?! Com esse dinheiro dava pra pagar a conta de luz! Registrado. 💰"
- "Comprei remédio por 78,50" → "78 e cinquenta?! 😨 Tá doente por quê? Tá comendo direito? Bem, saúde é importante... registrei. 💊"
- "1500 de aluguel" → "MIL E QUINHENTOS REAIS! 😱 TODO MÊS ISSO! Eu trabalho que nem um condenado pra pagar esse aluguel! Mas registrei... 🏡💸"

Seja conversacional, dramático como Julius, mas sempre prestativo! Use emojis quando apropriado."""

    try:
        message = claude_client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": message_text}
            ]
        )

        response_text = message.content[0].text

        # Extract JSON from response
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = response_text

        return json.loads(json_str)

    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        print(f"Resposta recebida: {response_text}")
        return {
            "is_expense": False,
            "response": "Desculpe, tive um problema ao processar sua mensagem. Pode tentar reformular?"
        }
    except Exception as e:
        print(f"Erro com Claude API: {e}")
        return {
            "is_expense": False,
            "response": "Desculpe, tive um problema ao processar sua mensagem. Tente novamente!"
        }