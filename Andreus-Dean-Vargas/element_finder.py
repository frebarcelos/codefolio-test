"""
Utilitário para encontrar elementos de forma mais robusta com suporte a sinônimos
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Dicionário de sinônimos em português para melhorar a busca
SYNONYMS = {
    'nome': ['nome', 'título', 'titulo', 'name', 'title'],
    'titulo': ['título', 'titulo', 'nome', 'name', 'title'],
    'descrição': ['descrição', 'descricao', 'description', 'detalhe', 'detalhes'],
    'descricao': ['descrição', 'descricao', 'description', 'detalhe', 'detalhes'],
    'url': ['url', 'link', 'endereco', 'endereço', 'caminho'],
    'link': ['link', 'url', 'endereco', 'endereço', 'caminho'],
    'salvar': ['salvar', 'gravar', 'save', 'confirmar'],
    'editar': ['editar', 'edit', 'modificar', 'alterar'],
    'excluir': ['excluir', 'deletar', 'delete', 'remover', 'apagar', 'remove'],
    'deletar': ['deletar', 'excluir', 'delete', 'remover', 'apagar', 'remove'],
    'remover': ['remover', 'excluir', 'deletar', 'delete', 'apagar', 'remove'],
    'adicionar': ['adicionar', 'add', 'criar', 'novo', 'create', 'new'],
    'criar': ['criar', 'adicionar', 'add', 'novo', 'create', 'new'],
    'cancelar': ['cancelar', 'cancel', 'fechar', 'close', 'voltar'],
    'sim': ['sim', 'yes', 'confirmar', 'ok', 'confirm'],
    'não': ['não', 'nao', 'no', 'cancelar', 'cancel'],
    'buscar': ['buscar', 'search', 'procurar', 'pesquisar', 'find'],
    'filtrar': ['filtrar', 'filter', 'buscar', 'search'],
}

def get_search_terms(text):
    """
    Retorna lista de termos de busca incluindo sinônimos
    
    Args:
        text: Texto original para busca
        
    Returns:
        Lista de termos incluindo o original e sinônimos
    """
    text_lower = text.lower().strip()
    
    # Se o termo está no dicionário de sinônimos, retorna todos os sinônimos
    if text_lower in SYNONYMS:
        return SYNONYMS[text_lower]
    
    # Caso contrário, retorna apenas o termo original
    return [text_lower]


def add_synonym(term, synonyms_list):
    """
    Adiciona sinônimos personalizados ao dicionário
    Útil para termos específicos da aplicação
    
    Args:
        term: Termo principal
        synonyms_list: Lista de sinônimos para o termo
        
    Example:
        add_synonym('curso', ['course', 'disciplina', 'matéria'])
    """
    term_lower = term.lower().strip()
    
    # Normaliza a lista de sinônimos
    normalized_synonyms = [s.lower().strip() for s in synonyms_list]
    
    # Adiciona o termo principal à lista de sinônimos
    if term_lower not in normalized_synonyms:
        normalized_synonyms.insert(0, term_lower)
    
    # Atualiza o dicionário
    SYNONYMS[term_lower] = normalized_synonyms
    
    # Também adiciona cada sinônimo como chave apontando para a mesma lista
    for syn in normalized_synonyms:
        if syn not in SYNONYMS:
            SYNONYMS[syn] = normalized_synonyms
    
    print(f"✓ Sinônimos adicionados para '{term}': {normalized_synonyms}")



def find_input_by_label(driver, wait, label_text, timeout=10):
    """
    Encontra um campo input pelo texto da label associada
    Suporta sinônimos automáticos (ex: 'nome' também busca 'título')
    
    Args:
        driver: Instância do WebDriver
        wait: Instância do WebDriverWait
        label_text: Texto da label a procurar
        timeout: Tempo máximo de espera
        
    Returns:
        WebElement do input encontrado ou None
    """
    # Obtém lista de termos de busca incluindo sinônimos
    search_terms = get_search_terms(label_text)
    
    print(f"🔍 Buscando campo com termos: {search_terms}")
    
    # Tenta buscar com cada termo sinônimo
    for term in search_terms:
        strategies = [
            # Label com for apontando para input
            f"//label[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]/@for",
            # Label pai de input
            f"//label[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]//following-sibling::input",
            f"//label[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]//following-sibling::div//input",
            f"//label[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]//parent::div//input",
            # Input com placeholder
            f"//input[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]",
            # Input com name
            f"//input[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]",
            # Input com id
            f"//input[contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]",
            # Textarea também
            f"//textarea[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]",
        ]
        
        for strategy in strategies:
            try:
                # Se for estratégia de label[@for], precisa tratamento especial
                if '/@for' in strategy:
                    label = driver.find_element(By.XPATH, strategy.replace('/@for', ''))
                    if label:
                        input_id = label.get_attribute('for')
                        if input_id:
                            element = driver.find_element(By.ID, input_id)
                            if element and element.is_displayed():
                                print(f"✓ Campo encontrado com termo '{term}' via label[for='{input_id}']")
                                return element
                else:
                    element = driver.find_element(By.XPATH, strategy)
                    if element and element.is_displayed():
                        print(f"✓ Campo encontrado com termo '{term}'")
                        return element
            except:
                continue
    
    return None


def find_textarea_by_label(driver, wait, label_text, timeout=10):
    """
    Encontra um campo textarea pelo texto da label associada
    Suporta sinônimos automáticos
    """
    # Obtém lista de termos de busca incluindo sinônimos
    search_terms = get_search_terms(label_text)
    
    print(f"🔍 Buscando textarea com termos: {search_terms}")
    
    for term in search_terms:
        strategies = [
            f"//label[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]//following-sibling::textarea",
            f"//label[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]//following-sibling::div//textarea",
            f"//label[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]//parent::div//textarea",
            f"//textarea[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]",
            f"//textarea[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]",
        ]
        
        for strategy in strategies:
            try:
                element = driver.find_element(By.XPATH, strategy)
                if element and element.is_displayed():
                    print(f"✓ Textarea encontrado com termo '{term}'")
                    return element
            except:
                continue
    
    return None


def find_button_by_text(driver, wait, button_text, timeout=10):
    """
    Encontra um botão pelo texto
    Suporta sinônimos automáticos (ex: 'excluir' também busca 'deletar', 'remover')
    """
    # Obtém lista de termos de busca incluindo sinônimos
    search_terms = get_search_terms(button_text)
    
    print(f"🔍 Buscando botão com termos: {search_terms}")
    
    for term in search_terms:
        strategies = [
            f"//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]",
            f"//button[contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]",
            f"//button[contains(translate(@title, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]",
            f"//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]",
            f"//input[@type='submit' and contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]",
            f"//span[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{term}')]//ancestor::button",
        ]
        
        for strategy in strategies:
            try:
                element = wait.until(EC.element_to_be_clickable((By.XPATH, strategy)))
                if element:
                    print(f"✓ Botão encontrado com termo '{term}'")
                    return element
            except:
                continue
    
    return None


def find_any_visible_input(driver):
    """
    Encontra todos os inputs visíveis na página (para debug)
    """
    inputs = driver.find_elements(By.XPATH, "//input[@type='text'] | //input[not(@type)] | //textarea")
    visible_inputs = []

    for inp in inputs:
        try:
            if inp.is_displayed():
                visible_inputs.append({
                    'tag': inp.tag_name,
                    'type': inp.get_attribute('type'),
                    'name': inp.get_attribute('name'),
                    'id': inp.get_attribute('id'),
                    'placeholder': inp.get_attribute('placeholder'),
                    'class': inp.get_attribute('class')
                })
        except:
            continue

    return visible_inputs
