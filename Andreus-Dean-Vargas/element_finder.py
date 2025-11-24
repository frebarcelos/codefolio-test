"""Utilitário para buscar elementos com múltiplos seletores XPath."""
from selenium.webdriver.common.by import By


def find_element_by_selectors(driver, selectors_list, wait_for_visible=True):
    """
    Busca elemento tentando múltiplos seletores XPath.
    
    Args:
        driver: Instância do WebDriver
        selectors_list: Lista de seletores XPath para tentar
        wait_for_visible: Se True, verifica se elemento está visível
        
    Returns:
        WebElement se encontrado, None caso contrário
    """
    for selector in selectors_list:
        try:
            element = driver.find_element(By.XPATH, selector)
            if wait_for_visible:
                if element.is_displayed():
                    return element
            else:
                return element
        except:
            continue
    
    return None


def find_input_field(driver, label_text, field_type="input"):
    """
    Busca campo de formulário por label.
    
    Args:
        driver: Instância do WebDriver
        label_text: Texto da label (ex: "Nome", "Título")
        field_type: Tipo do campo ("input", "textarea")
        
    Returns:
        WebElement se encontrado, None caso contrário
    """
    selectors = [
        f"//label[contains(., '{label_text}')]/following-sibling::div//{field_type}",
        f"//{field_type}[@placeholder*='{label_text}']",
        f"//{field_type}[@name='{label_text.lower()}']",
        f"//{field_type}[@id='{label_text.lower()}']"
    ]
    
    return find_element_by_selectors(driver, selectors)


def find_button(driver, button_text):
    """
    Busca botão por texto.
    
    Args:
        driver: Instância do WebDriver
        button_text: Texto do botão (ex: "Salvar", "Adicionar")
        
    Returns:
        WebElement se encontrado, None caso contrário
    """
    selectors = [
        f"//button[contains(., '{button_text}')]",
        f"//button[contains(., '{button_text.upper()}')]",
        f"//button[@aria-label='{button_text}']"
    ]
    
    return find_element_by_selectors(driver, selectors)
