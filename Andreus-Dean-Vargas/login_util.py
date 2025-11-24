"""Utilitário de login para testes."""
import time


def login(driver, url_base="https://testes-codefolio.web.app/"):
    """
    Faz login injetando token do Firebase no localStorage.
    
    Args:
        driver: Instância do WebDriver
        url_base: URL base da aplicação
    """
    # Credenciais do Bruno (temporário até você ter acesso de professor)
    FIREBASE_KEY = "--"
    FIREBASE_VALUE = """--"""
    
    print("🔐 Fazendo login com credenciais.")
    driver.get(url_base)
    
    driver.execute_script(
        "window.localStorage.setItem(arguments[0], arguments[1]);",
        FIREBASE_KEY,
        FIREBASE_VALUE
    )
    
    driver.refresh()
    time.sleep(2)
    print("✅ Login realizado")


def verificar_login(driver, wait):
    """
    Verifica se o login foi bem-sucedido.
    
    Args:
        driver: Instância do WebDriver
        wait: Instância do WebDriverWait
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    
    print("🔍 Verificando login...")
    time.sleep(3)
    
    # Verifica se botão de perfil está presente
    profile_button = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button[aria-label='Configurações da Conta']")
        )
    )
    
    print("✅ Login verificado com sucesso")