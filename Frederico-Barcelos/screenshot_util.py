import os
import re
import time # Nova importação
from selenium.webdriver.support.ui import WebDriverWait

# Dicionário global para manter a contagem de screenshots por teste
_screenshot_counters = {}

# Atraso configurável antes de tirar o screenshot, após o carregamento da página
SCREENSHOT_DELAY_SECONDS = 3

def take_step_screenshot(driver, test_id, step_name):
    """
    Tira um screenshot, numera e salva em uma pasta específica para o teste.
    
    :param driver: A instância do WebDriver do Selenium.
    :param test_id: O ID do teste (ex: self.id()), usado para nomear a pasta.
    :param step_name: Um nome descritivo para o passo (usado no nome do arquivo).
    """
    global _screenshot_counters
    
    # O ID completo é 'module.class.method'. Pegamos apenas o nome do método.
    test_name = test_id.split('.')[-1]

    # Inicia o contador para um novo teste, se não existir
    if test_name not in _screenshot_counters:
        _screenshot_counters[test_name] = 0
    
    _screenshot_counters[test_name] += 1
    counter = _screenshot_counters[test_name]

    # Cria o diretório para os screenshots do teste
    screenshot_dir = os.path.join('test_screenshots', test_name)
    os.makedirs(screenshot_dir, exist_ok=True)

    # Limpa o nome do passo para criar um nome de arquivo seguro
    safe_step_name = re.sub(r'[^a-zA-Z0-9_-]', '_', step_name)
    
    file_path = os.path.join(screenshot_dir, f"{counter:02d}_{safe_step_name}.png")

    try:
        # Espera a página carregar completamente antes de tirar o screenshot
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        # Adiciona um atraso extra para garantir que elementos dinâmicos carreguem
        time.sleep(SCREENSHOT_DELAY_SECONDS)
        driver.save_screenshot(file_path)
        print(f"✓ Screenshot salvo: {file_path}")
    except Exception as e:
        print(f"✗ Falha ao salvar screenshot em '{file_path}': {e}")

def reset_screenshot_counter(test_id):
    """Reseta o contador de screenshot para um teste específico, garantindo que cada execução comece do zero."""
    global _screenshot_counters
    test_name = test_id.split('.')[-1]
    if test_name in _screenshot_counters:
        del _screenshot_counters[test_name]
