import os
from selenium.webdriver.chrome.options import Options

def get_chrome_options():
    """
    Cria e retorna um objeto de opções do Chrome com configurações padrão
    e modo headless se a variável de ambiente HEADLESS_MODE estiver definida.
    """
    chrome_options = Options()

    if os.getenv('HEADLESS_MODE') == '1':
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
    
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    
    return chrome_options
