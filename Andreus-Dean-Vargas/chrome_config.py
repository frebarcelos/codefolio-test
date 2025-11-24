"""Configurações do Chrome para testes."""
import os
from selenium.webdriver.chrome.options import Options


def get_chrome_options():
    """Retorna opções configuradas do Chrome."""
    options = Options()
    
    # Headless se variável de ambiente estiver definida
    if os.getenv('HEADLESS_MODE') == '1':
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
    
    options.add_argument("--start-maximized")
    
    return options
