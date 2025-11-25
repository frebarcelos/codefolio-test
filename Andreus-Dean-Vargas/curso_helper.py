"""
Helper para garantir que existe curso antes de executar testes
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from element_finder import find_input_by_label, find_textarea_by_label, find_button_by_text


def garantir_curso_existe(driver, wait, nome_curso, descricao_curso, url_base="https://testes-codefolio.web.app/"):
    """
    Verifica se existe curso. Se não existir, cria um.
    
    Args:
        driver: WebDriver do Selenium
        wait: WebDriverWait
        nome_curso: Nome do curso a criar (se necessário)
        descricao_curso: Descrição do curso a criar (se necessário)
        url_base: URL base da aplicação
        
    Returns:
        bool: True se curso já existia, False se foi criado
    """
    try:
        # Tenta encontrar botão "Gerenciar Curso"
        botao_gerenciar = driver.find_element(
            By.XPATH, 
            "//button[contains(., 'Gerenciar Curso')]"
        )
        print("✓ Curso existente encontrado")
        return True
        
    except:
        print("⚠ Nenhum curso encontrado. Criando curso para teste...")
        
        # Clica em "Criar Novo Curso"
        botao_criar = find_button_by_text(driver, wait, "criar")
        if not botao_criar:
            raise Exception("Botão 'Criar Novo Curso' não encontrado")
        
        driver.execute_script("arguments[0].click();", botao_criar)
        time.sleep(2)
        
        # Preenche nome do curso
        campo_nome = find_input_by_label(driver, wait, "nome")
        if campo_nome:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", campo_nome)
            time.sleep(0.5)
            
            # Clica e preenche usando send_keys
            campo_nome.click()
            time.sleep(0.3)
            campo_nome.clear()
            time.sleep(0.3)
            campo_nome.send_keys(nome_curso)
            time.sleep(0.5)
            
            print(f"✓ Nome do curso preenchido: '{nome_curso}'")
        
        # Preenche descrição (se houver)
        campo_desc = find_textarea_by_label(driver, wait, "descrição")
        if not campo_desc:
            campo_desc = find_input_by_label(driver, wait, "descrição")
        
        if campo_desc:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", campo_desc)
            time.sleep(0.5)
            
            # Clica e preenche usando send_keys
            campo_desc.click()
            time.sleep(0.3)
            campo_desc.clear()
            time.sleep(0.3)
            campo_desc.send_keys(descricao_curso)
            time.sleep(0.5)
            
            print("✓ Descrição do curso preenchida")
        
        # Salva o curso
        botao_salvar = find_button_by_text(driver, wait, "salvar")
        if not botao_salvar:
            raise Exception("Botão 'Salvar' não encontrado")
        
        driver.execute_script("arguments[0].click();", botao_salvar)
        print("✓ Curso criado com sucesso")
        time.sleep(3)
        
        # Volta para lista de cursos
        driver.get(f"{url_base}/manage-courses")
        time.sleep(2)
        
        return False


def garantir_video_existe(driver, wait, titulo_video, url_video):
    """
    Verifica se existe vídeo no curso. Se não existir, cria um.
    
    Args:
        driver: WebDriver do Selenium
        wait: WebDriverWait
        titulo_video: Título do vídeo a criar (se necessário)
        url_video: URL do vídeo a criar (se necessário)
        
    Returns:
        bool: True se vídeo já existia, False se foi criado
    """
    try:
        # Navega para aba de vídeos
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        aba_videos = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'VÍDEOS') or contains(text(), 'Vídeos')]")
            )
        )
        driver.execute_script("arguments[0].click();", aba_videos)
        time.sleep(3)
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Tenta encontrar algum vídeo cadastrado
        # Procura por botões de editar ou deletar (SVG icons) na área de vídeos
        try:
            # Procura por qualquer botão SVG (editar ou deletar) que indica vídeo existente
            icones = driver.find_elements(By.XPATH, "//button[@aria-label or @title]//svg")
            
            # Filtra apenas ícones que estão visíveis e não são do cabeçalho
            for icone in icones:
                if icone.is_displayed():
                    try:
                        # Tenta pegar o botão pai
                        botao = icone.find_element(By.XPATH, "./ancestor::button")
                        # Se o botão tem label que não é de navegação, é um vídeo
                        aria_label = botao.get_attribute("aria-label") or ""
                        if aria_label and "Configurações" not in aria_label and "Menu" not in aria_label:
                            print(f"✓ Vídeo existente encontrado (ícone detectado)")
                            return True
                    except:
                        continue
            
            # Se não encontrou ícones, tenta procurar cards de vídeo de outra forma
            # Procura por estruturas que contenham YouTube URL
            videos_com_url = driver.find_elements(By.XPATH, "//*[contains(@href, 'youtube.com') or contains(@src, 'youtube.com')]")
            if videos_com_url:
                print(f"✓ Vídeo existente encontrado ({len(videos_com_url)} vídeo(s))")
                return True
            
            # Se não encontrou nenhum vídeo
            raise Exception("Nenhum vídeo encontrado")
            
        except:
            print("⚠ Nenhum vídeo encontrado. Criando vídeo para teste...")
            
            # Scroll para o topo
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # Preenche título do vídeo usando label exato
            campo_titulo = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//label[contains(text(), 'Título do Vídeo')]/following-sibling::div//input")
                )
            )
            
            if campo_titulo:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", campo_titulo)
                time.sleep(1)
                campo_titulo.click()
                time.sleep(0.5)
                campo_titulo.clear()
                time.sleep(0.5)
                campo_titulo.send_keys(titulo_video)
                time.sleep(1)
            
            # Preenche URL do vídeo usando label exato
            campo_url = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//label[contains(text(), 'URL do Vídeo')]/following-sibling::div//input")
                )
            )
            
            if campo_url:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", campo_url)
                time.sleep(1)
                campo_url.click()
                time.sleep(0.5)
                campo_url.clear()
                time.sleep(0.5)
                campo_url.send_keys(url_video)
                time.sleep(1)
            
            # Adiciona o vídeo
            botao_adicionar = find_button_by_text(driver, wait, "adicionar")
            if botao_adicionar:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_adicionar)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", botao_adicionar)
                time.sleep(2)
                
                # IMPORTANTE: Precisa SALVAR o curso para o vídeo ser realmente adicionado
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)
                
                botao_salvar = find_button_by_text(driver, wait, "salvar")
                if botao_salvar:
                    driver.execute_script("arguments[0].click();", botao_salvar)
                    time.sleep(3)
                    
                    # Fechar modal de sucesso se aparecer
                    try:
                        botao_ok = find_button_by_text(driver, wait, "ok")
                        if botao_ok:
                            driver.execute_script("arguments[0].click();", botao_ok)
                            time.sleep(2)
                    except:
                        pass
                    
                    print(f"✓ Vídeo '{titulo_video}' criado com sucesso")
                    
                    # Após clicar em OK, reabrir o curso
                    time.sleep(2)
                    botao_gerenciar = wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "(//button[contains(., 'Gerenciar Curso')])[1]")
                        )
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_gerenciar)
                    time.sleep(1)
                    botao_gerenciar.click()
                    time.sleep(3)
                    
                    # Navegar para aba de vídeos novamente
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    
                    aba_videos = wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//*[contains(text(), 'VÍDEOS') or contains(text(), 'Vídeos')]")
                        )
                    )
                    driver.execute_script("arguments[0].click();", aba_videos)
                    time.sleep(3)
            
            return False
            
    except Exception as e:
        raise Exception(f"Erro ao garantir vídeo: {e}")
