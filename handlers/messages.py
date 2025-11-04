from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from services.claude_service import analyze_message
from services.sheets_service import add_expense_to_sheet
from handlers.commands import stats_command
from utils.constants import CATEGORY_EMOJIS, STATS_KEYWORDS, USER_NAME


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages"""
    user_message = update.message.text

    await update.message.chat.send_action(action="typing")

    # Check if user is asking for stats
    user_message_lower = user_message.lower()
    if any(keyword in user_message_lower for keyword in STATS_KEYWORDS):
        await stats_command(update, context)
        return

    # Analyze message with Claude
    result = analyze_message(user_message)

    if result.get('is_expense', False):
        amount = result.get('amount', 0)
        date_str = result.get('date', datetime.now().strftime('%Y-%m-%d'))
        category = result.get('category', 'Outros').capitalize()
        description = result.get('description', '')

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        except:
            date = datetime.now()

        success = add_expense_to_sheet(amount, date, category, description)

        if success:
            category_emoji = CATEGORY_EMOJIS.get(category, '💰')

            # Julius-style reaction based on amount
            julius_reaction = get_julius_reaction(amount, category).format(my_name=USER_NAME)

            confirmation = f"""
{julius_reaction}

✅ *Aff, ok, despesa registrada*

💵 *Valor:* R$ {amount:.2f}
📅 *Data:* {date.strftime('%d/%m/%Y')}
{category_emoji} *Categoria:* {category}
"""
            if description:
                confirmation += f"📝 *Descrição:* {description}\n"

            confirmation += "\n_Registrado na planilha... lá se vai mais dinheiro suado! 💸_"

            await update.message.reply_text(confirmation, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                "❌ Erro ao salvar na planilha. Pelo menos o dinheiro ainda tá na sua conta! 🤷"
            )
    else:
        # Get Claude's Julius-style response
        response = result.get('response', 'Como posso ajudar? E vai com calma nos gastos, hein! 😊')
        await update.message.reply_text(response)


def get_julius_reaction(amount: float, category: str) -> str:
    """Get Julius-style reaction based on amount and category"""

    if amount > 1000:
        reactions = [
            "{user_name}, QUE MERDA É ESSA?!! É isso, cê ficou maluco, tá ganhando em dólar é?!",
        ]
    elif amount < 20:
        reactions = [
            "😤 TUDO ISSO??? Se foi menos de VINTÃO, dava pra ter economizado!",
            "💸 Poderia ser pior, mas ainda assim é dinheiro jogado fora!",
            "😑 Tá, é pouquinho, mas eu trabalhei 5 dias pra conseguir esse mesmo valor!"
        ]
    elif amount < 50:
        reactions = [
            "😱 Olha o tamanho desse gasto! Isso dá quase 3 quilowatts de luz!",
            "💸 {my_name}!!! Esse dinheiro não cresce em árvore não! Pelo amor",
            "😤 Eu trabalho que nem um condenado pra você gastar assim!"
        ]
    elif amount < 100:
        reactions = [
            "😱😱 QUANTO?! Com esse dinheiro dava pra fazer compra pro mês!",
            "💸💸 Você tá maluco(a)?! Isso são 4 HORAS de trabalho meu!",
            "😤😤 Lá se vai o dinheiro do aluguel!"
        ]
    else:
        reactions = [
            "😱😱😱 TEM CERTEZA DISSO?! Com esse dinheiro dava pra pagar a CONTA DE LUZ DO ANO!",
            "💸💸💸 {my_name} VOCÊ PERDEU O JUÍZO?! EU VOU TER QUE FAZER DOIS TURNOS PRA RECUPERAR ISSO!",
            "😤😤😤 MAS QUE ABSURDO! Isso é QUASE o que eu ganho na SEMANA!"
        ]

    import random
    return random.choice(reactions)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors and notify user"""
    print(f'Erro: {context.error}')
    if update and update.message:
        await update.message.reply_text(
            "😅 Ops! Ocorreu um erro inesperado. Por favor, tente novamente."
        )