from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TELEGRAM_TOKEN, validate_config
from handlers.commands import start, help_command, stats_command
from handlers.messages import handle_message, error_handler


def main():
    """Start the bot"""
    try:
        # Validate configuration
        validate_config()

        # Create the Application
        application = Application.builder().token(TELEGRAM_TOKEN).build()

        # Register handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("stats", stats_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)

        # Start the Bot
        print("=" * 50)
        print("🤖 Julius Financeiro")
        print("=" * 50)
        print("✅ Bot iniciado com sucesso!")
        print("📊 Integração com Google Sheets ativa")
        print("🤖 Claude AI integrado")
        print("=" * 50)
        print("\nPressione Ctrl+C para parar o bot\n")

        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except KeyboardInterrupt:
        print("\n\n👋 Bot encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar o bot: {e}")
        print("\nVerifique se:")
        print("1. O arquivo .env está configurado corretamente")
        print("2. O arquivo credentials.json existe ou GOOGLE_CREDENTIALS está definido")
        print("3. Todas as APIs estão configuradas")
        raise


if __name__ == '__main__':
    main()