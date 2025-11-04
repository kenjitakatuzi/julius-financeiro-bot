import gspread
from google.oauth2.service_account import Credentials
from config import GOOGLE_CREDENTIALS_FILE, GOOGLE_SHEET_ID

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def get_sheets_client():
    """Initialize Google Sheets client"""
    try:
        creds = Credentials.from_service_account_file(
            GOOGLE_CREDENTIALS_FILE,
            scopes=SCOPES
        )
        return gspread.authorize(creds)
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo de credenciais '{GOOGLE_CREDENTIALS_FILE}' não encontrado")
    except Exception as e:
        raise Exception(f"Erro ao autenticar com Google Sheets: {str(e)}")


def add_expense_to_sheet(amount, date, category, description=""):
    """Add expense entry to Google Sheets"""
    try:
        client = get_sheets_client()
        sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1

        date_str = date.strftime('%d/%m/%Y')
        row = [date_str, amount, category, description]
        sheet.append_row(row)
        return True
    except Exception as e:
        print(f"Erro ao adicionar na planilha: {e}")
        return False


def get_all_expenses():
    """Get all expenses from Google Sheets"""
    try:
        client = get_sheets_client()
        sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1
        return sheet.get_all_records()
    except Exception as e:
        print(f"Erro ao buscar despesas: {e}")
        return []