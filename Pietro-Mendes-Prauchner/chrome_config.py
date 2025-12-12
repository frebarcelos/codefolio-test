"""
Configuração do Chrome WebDriver para testes Selenium
"""

from selenium.webdriver.chrome.options import Options

def get_chrome_options():
    """Retorna as opções do Chrome configuradas para testes."""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    # Descomenta a linha abaixo para rodar em headless mode
    # chrome_options.add_argument("--headless")
    return chrome_options
