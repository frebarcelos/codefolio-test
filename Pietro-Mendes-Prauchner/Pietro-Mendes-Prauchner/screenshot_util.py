"""
screenshot_util.py

Utilitário para captura de screenshots durante testes Selenium.
Salva automaticamente em subpastas organizadas por teste dentro de screenshots/
"""

import os
from pathlib import Path
from datetime import datetime


def get_screenshot_dir(test_name):
    """
    Retorna o caminho da pasta de screenshots para um teste.
    Cria a pasta se não existir.
    
    Args:
        test_name (str): Nome do teste (ex: 'RF41_comentar_videos')
        
    Returns:
        str: Caminho absoluto da pasta de screenshots
    """
    # Caminho relativo a este script (agora screenshots está na mesma pasta)
    script_dir = Path(__file__).parent
    
    screenshot_base = script_dir / "screenshots" / test_name
    screenshot_base.mkdir(parents=True, exist_ok=True)
    
    return str(screenshot_base)


def save_screenshot(driver, test_name, step_name):
    """
    Captura e salva um screenshot do driver.
    
    Args:
        driver: Selenium WebDriver instance
        test_name (str): Nome do teste (ex: 'RF41_comentar_videos')
        step_name (str): Nome do passo/descrição (ex: 'antes_comentario')
        
    Returns:
        str: Caminho completo do arquivo salvo
    """
    try:
        screenshot_dir = get_screenshot_dir(test_name)
        
        # Formata nome com timestamp
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{step_name}_{timestamp}.png"
        filepath = os.path.join(screenshot_dir, filename)
        
        # Salva screenshot
        driver.save_screenshot(filepath)
        print(f"✓ Screenshot salvo: {filename}")
        
        return filepath
        
    except Exception as e:
        print(f"✗ Erro ao salvar screenshot: {e}")
        return None
