from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from services.sheets_service import get_all_expenses
from utils.constants import CATEGORY_EMOJIS, MONTH_NAMES_PT
import random


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    welcome_message = """
😤 *Olá! Eu sou o Julius, e vou cuidar do SEU DINHEIRO!*

Eu tô aqui pra te ajudar a CONTROLAR esses gastos que tão acabando com o seu bolso!

*Como usar:*
📝 Me conta CADA UM DOS SEUS GASTOS (e prepara pra ouvir umas verdades!).
📝 Eu vou registrar TUDO, absolutamente TUDO na planilha, com detalhes e tudo.
📝 E vou te lembrar que DINHEIRO NÃO CRESCE EM ÁRVORE! Ele CRESCE quando você planta TEMPO, rega com lágrimas de CANSAÇO e colhe as mãos cascudas do ESFORÇO!

*Exemplos:*
- "Gastei 45 reais no almoço"
  → EU: "45 REAIS?! 😱 Podia ter comido em casa!"

- "R$ 120 de Uber"
  → EU: "Você não tem PERNAS não?! 😤"

*Comandos:*
/help - Ajuda (e mais reclamações)
/stats - Ver quanto você JÁ GASTOU esse mês 💸

Pode começar... (não começa não, por favor) 💰💰💰💸💸💸
"""
    await update.message.reply_text(welcome_message, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_message = """
📋 *Comandos disponíveis:*

/start - Inicia o bot (e as reclamações!)
/help - Mostra esta mensagem
/stats - Mostra quanto você JOGOU FORA esse mês 💸

*Como registrar despesas:*
Só me contar! Eu vou registrar e RECLAMAR!

💰 *Exemplos:*
- "Gastei 50 reais no restaurante"
- "Paguei 120 de conta de luz"
- "R$ 35 no Uber"
- "Comprei um livro por 45,90"

🏷️ *Categorias:*
- Alimentação 🍽️ (Podia comer em casa!)
- Transporte 🚕 (Você tem pernas!)
- Saúde 💊 (Tá doente por quê?)
- Lazer 🎬 (Lazer?! E o dinheiro?)
- Moradia 🏡 (Esse aluguel tá me matando!)
- Educação 📖 (Pelo menos é pra estudar...)
- Compras 🛒 (Você PRECISA disso?!)
- Outros 📦 (Mais dinheiro jogado fora!)

Eu registro tudo... e RECLAMO de tudo! 😤
"""
    await update.message.reply_text(help_message, parse_mode='Markdown')


def get_julius_stats_intro(total: float) -> str:
    """Get Julius dramatic intro based on total spent"""
    if total < 500:
        intros = [
            f"😤 *{total:.2f} reais esse mês?!*\n\nBom... pelo menos você tá tentando economizar...",
            f"💸 *R$ {total:.2f}*\n\nPoderia ser pior, mas AINDA É DINHEIRO!",
            f"😑 *{total:.2f} reais*\n\nTá controlado... mas NÃO RELAXA não!"
        ]
    elif total < 1500:
        intros = [
            f"😱 *R$ {total:.2f}?!*\n\nRAPAZ(A)! Isso são VÁRIAS contas de luz!",
            f"💸💸 *{total:.2f} REAIS!*\n\nEu trabalho que nem um CONDENADO e você gasta assim?!",
            f"😤😤 *R$ {total:.2f}*\n\nMAS QUE ABSURDO! Olha o tamanho desse gasto!"
        ]
    elif total < 3000:
        intros = [
            f"😱😱 *R$ {total:.2f}?!?!*\n\nVOCÊ TÁ MALUCO(A)?! Isso dá pra pagar ALUGUEL!",
            f"💸💸💸 *{total:.2f} REAIS!!!*\n\nEU VOU TER QUE FAZER DOIS TURNOS POR SUA CAUSA!",
            f"😤😤😤 *R$ {total:.2f}*\n\nMAS É MUITO DINHEIRO! Você tá gastando igual RICAÇO!"
        ]
    else:
        intros = [
            f"😱😱😱 *R$ {total:.2f}?!?!?!*\n\nTEM CERTEZA DISSO?! VOCÊ VAI ME MATAR DO CORAÇÃO!",
            f"💸💸💸 *{total:.2f} REAIS?!*\n\nEU NEM GANHO ISSO NO MÊS! VOCÊ PERDEU O JUÍZO?!",
            f"😤😤😤 *R$ {total:.2f}!!!*\n\nVOCÊ TÁ QUERENDO ME DEIXAR NA RUA?! É ISSO?!"
        ]

    return random.choice(intros)


def get_julius_category_comment(category: str, amount: float, percentage: float) -> str:
    """Get Julius comment about specific category"""
    comments = {
        'Alimentação': [
            "😤 COMIDA DE RUA! Podia comer em casa!",
            "🍽️ Tem comida em casa, mas NÃO...",
            "😑 Restaurante de novo? A geladeira tá vazia?"
        ],
        'Transporte': [
            "😱 Você não tem PERNAS não?!",
            "🚕 Uber de novo?! Aprende a andar!",
            "😤 Com esse dinheiro de transporte dava pra comprar uma BICICLETA!"
        ],
        'Saúde': [
            "💊 Tá doente? Tá comendo direito?",
            "😟 Bem... saúde é importante, NÉ...",
            "💊 Da próxima vez toma chá de boldo!"
        ],
        'Lazer': [
            "😱😱 LAZER?! E EU AQUI TRABALHANDO!",
            "🎬 Cinema? Netflix é DE GRAÇA!",
            "😤 Diversão? O que é isso? Nunca ouvi falar!"
        ],
        'Moradia': [
            "😰 Esse aluguel tá me matando...",
            "🏡 TODO mês isso! TODO MÊS!",
            "💸 Metade do meu salário vai pra esse aluguel!"
        ],
        'Educação': [
            "📖 Pelo menos tá estudando...",
            "😌 Educação é importante... MAS NÃO EXAGERA!",
            "📚 Tá bom, isso é investimento... eu acho..."
        ],
        'Compras': [
            "😱 Você PRECISA disso?! PRECISA MESMO?!",
            "🛒 Mais compras?! A casa tá cheia!",
            "😤 Comprou o quê? Espero que seja NECESSÁRIO!"
        ],
        'Outros': [
            "😑 'Outros'? Quer dizer: dinheiro jogado fora!",
            "💸 Nem sabe no que gastou, né?!",
            "😤 Outros?! Eu quero DETALHES!"
        ]
    }

    category_comments = comments.get(category, ["😤 Mais dinheiro indo embora..."])

    # Add percentage comment if it's too high
    if percentage > 40:
        return f"{random.choice(category_comments)} E ainda é {percentage:.1f}% do total! 😱"
    elif percentage > 25:
        return f"{random.choice(category_comments)} {percentage:.1f}% foi nisso!"
    else:
        return random.choice(category_comments)


def get_julius_conclusion(total: float, avg_per_day: float) -> str:
    """Get Julius final dramatic conclusion"""
    if total < 500:
        conclusions = [
            f"\n💡 *Dica do Julius:*\nContinua assim! Dinheiro guardado é dinheiro ganho!\n\n_Mas não relaxa não, hein!_ 👀",
            f"\n😌 *Pelo menos você tá tentando...*\nMas {avg_per_day:.2f} por dia ainda pode melhorar!\n\n_Vamo economizar mais!_ 💰",
        ]
    elif total < 1500:
        conclusions = [
            f"\n😤 *Julius tá de olho!*\nR$ {avg_per_day:.2f} por dia? Dá pra reduzir!\n\n_Pensa bem antes de gastar!_ 💸",
            f"\n💸 *Tá gastando demais!*\nCom essa média de {avg_per_day:.2f}/dia, vai acabar na sarjeta!\n\n_Controla esses gastos!_ 😤",
        ]
    elif total < 3000:
        conclusions = [
            f"\n😱 *VOCÊ TÁ GASTANDO DEMAIS!*\nR$ {avg_per_day:.2f} POR DIA?! Isso é mais que o Malvo ganha!\n\n_PRECISA PARAR COM ISSO!_ 🚨",
            f"\n💸💸 *MAS QUE ABSURDO!*\n{avg_per_day:.2f} por dia vai te deixar pobre!\n\n_Eu avisei! EU AVISEI!_ 😤😤",
        ]
    else:
        conclusions = [
            f"\n😱😱😱 *VOCÊ VAI ME MATAR!*\nR$ {avg_per_day:.2f} POR DIA?! EU NEM GANHO ISSO!\n\n_PARA DE GASTAR AGORA!_ 🚨🚨🚨",
            f"\n💸💸💸 *EU VOU TER UM TRECO!*\nCom {avg_per_day:.2f} por dia você vai acabar DEVENDO!\n\n_PELO AMOR DE DEUS, PARA!_ 😤😤😤",
        ]

    return random.choice(conclusions)


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show monthly statistics with Julius personality"""
    try:
        records = get_all_expenses()

        if not records:
            await update.message.reply_text(
                "😌 *Nenhuma despesa registrada?*\n\n"
                "Boa! ASSIM que eu gosto! Dinheiro guardado é dinheiro ganho! 💰\n\n"
                "_Mas começa a registrar quando gastar, hein!_"
            )
            return

        # Calculate current month stats
        current_month = datetime.now().strftime('%m/%Y')
        monthly_total = 0
        monthly_count = 0
        categories = {}

        for record in records:
            date_str = record.get('Data', '')

            if current_month in date_str:
                monthly_count += 1
                amount_value = record.get('Valor', 0)

                try:
                    if isinstance(amount_value, (int, float)):
                        amount = float(amount_value)
                    else:
                        amount_str = str(amount_value).replace('R$', '').replace(',', '.').strip()
                        amount = float(amount_str)

                    monthly_total += amount
                    category = record.get('Categoria', 'Outros')
                    categories[category] = categories.get(category, 0) + amount
                except (ValueError, AttributeError):
                    print(f"Erro ao processar valor: {amount_value}")
                    continue

        if monthly_count == 0:
            await update.message.reply_text(
                f"😊 *Nenhum gasto em {MONTH_NAMES_PT[datetime.now().month]}?*\n\n"
                "PERFEITO! Continue assim! Dinheiro no bolso é o que importa! 💰"
            )
            return

        # Calculate additional stats
        avg_per_expense = monthly_total / monthly_count
        days_in_month = datetime.now().day
        avg_per_day = monthly_total / days_in_month if days_in_month > 0 else 0

        # Build message with Julius personality
        month_name = MONTH_NAMES_PT[datetime.now().month]

        # Dramatic intro
        stats_message = f"📊 *Relatório de {month_name}/{datetime.now().year}*\n"
        stats_message += "━━━━━━━━━━━━━━━━━━━━\n\n"
        stats_message += get_julius_stats_intro(monthly_total)
        stats_message += "\n\n━━━━━━━━━━━━━━━━━━━━\n"

        # Basic stats
        stats_message += f"\n📊 *Os números (que me dão dor de cabeça):*\n"
        stats_message += f"💸 *Total gasto:* R$ {monthly_total:.2f}\n"
        stats_message += f"📝 *Lançamentos:* {monthly_count} vezes!\n"
        stats_message += f"📊 *Média por gasto:* R$ {avg_per_expense:.2f}\n"
        stats_message += f"📅 *Média por dia:* R$ {avg_per_day:.2f}\n"

        # Equivalent calculations (Julius style)
        stats_message += f"\n💡 *Isso equivale a:*\n"
        light_bills = monthly_total / 150  # Assuming R$150 per light bill
        rice_bags = monthly_total / 25  # Assuming R$25 per rice bag
        stats_message += f"⚡ {light_bills:.1f} contas de luz\n"
        stats_message += f"🍚 {rice_bags:.0f} sacos de arroz de 5kg\n"
        stats_message += f"👔 {monthly_total / 50:.1f} horas do MEU trabalho!\n"

        stats_message += "\n━━━━━━━━━━━━━━━━━━━━\n"
        stats_message += "\n💸 *Onde foi parar O MEU DINHEIRO:*\n\n"

        # Sort categories by amount
        for category, total in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (total / monthly_total * 100) if monthly_total > 0 else 0
            emoji = CATEGORY_EMOJIS.get(category.capitalize(), '💰')

            stats_message += f"{emoji} *{category}:* R$ {total:.2f} ({percentage:.1f}%)\n"
            stats_message += f"   _{get_julius_category_comment(category, total, percentage)}_\n\n"

        stats_message += "━━━━━━━━━━━━━━━━━━━━"

        # Final Julius conclusion
        stats_message += get_julius_conclusion(monthly_total, avg_per_day)

        await update.message.reply_text(stats_message, parse_mode='Markdown')

    except Exception as e:
        error_msg = f"Erro ao buscar estatísticas: {str(e)}"
        print(error_msg)
        await update.message.reply_text(
            "❌ *Erro ao buscar estatísticas!*\n\n"
            "😤 Nem pra ver quanto você gastou funciona direito! "
            "Verifica se a planilha tá configurada!"
        )