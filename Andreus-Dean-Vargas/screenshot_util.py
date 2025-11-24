"""Utilitário para gerenciar screenshots dos testes."""
import os
from datetime import datetime


# Contador global de screenshots por teste
_screenshot_counters = {}


def reset_screenshot_counter(test_id):
    """
    Reseta o contador de screenshots para um teste.
    
    Args:
        test_id: ID do teste (ex: 'test_exemplo.TestClass.test_method')
    """
    _screenshot_counters[test_id] = 0


def get_screenshot_dir(test_id):
    """
    Retorna o diretório de screenshots para um teste específico.
    
    Args:
        test_id: ID do teste
        
    Returns:
        str: Caminho do diretório
    """
    # Extrai o nome do método de teste
    test_name = test_id.split('.')[-1]
    
    # Caminho absoluto base
    base_dir = r"C:\Users\ResTIC16\Documents\Codefolio-testes\codefolio-test\Andreus-Dean-Vargas\screenshots"
    test_dir = os.path.join(base_dir, test_name)
    
    # Cria o diretório se não existir
    os.makedirs(test_dir, exist_ok=True)
    
    return test_dir


def take_screenshot(driver, test_id, step_name=""):
    """
    Tira um screenshot e salva organizadamente.
    
    Args:
        driver: Instância do WebDriver
        test_id: ID do teste
        step_name: Nome descritivo do passo (opcional)
        
    Returns:
        str: Caminho do arquivo salvo
    """
    # Incrementa contador
    if test_id not in _screenshot_counters:
        _screenshot_counters[test_id] = 0
    
    _screenshot_counters[test_id] += 1
    count = _screenshot_counters[test_id]
    
    # Monta nome do arquivo
    timestamp = datetime.now().strftime("%H%M%S")
    
    if step_name:
        filename = f"{count:02d}_{step_name}_{timestamp}.png"
    else:
        filename = f"{count:02d}_screenshot_{timestamp}.png"
    
    # Salva screenshot
    screenshot_dir = get_screenshot_dir(test_id)
    filepath = os.path.join(screenshot_dir, filename)
    
    driver.save_screenshot(filepath)
    print(f"📸 Screenshot salvo: {filepath}")
    
    return filepath


def take_evidence(driver, test_id, evidence_number, description=""):
    """
    Tira screenshot de evidência numerada (ex: evidencia_01, evidencia_02).
    
    Args:
        driver: Instância do WebDriver
        test_id: ID do teste
        evidence_number: Número da evidência (1, 2, 3...)
        description: Descrição da evidência (opcional)
        
    Returns:
        str: Caminho do arquivo salvo
    """
    screenshot_dir = get_screenshot_dir(test_id)
    
    if description:
        filename = f"evidencia_{evidence_number:02d}_{description}.png"
    else:
        filename = f"evidencia_{evidence_number:02d}.png"
    
    filepath = os.path.join(screenshot_dir, filename)
    driver.save_screenshot(filepath)
    
    print(f"📋 Evidência {evidence_number} salva: {filepath}")
    
    return filepath
