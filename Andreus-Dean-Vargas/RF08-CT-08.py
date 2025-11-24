"""
CT-08 - Cadastro de Slides (RF08)
Autor: Andreus Dean Ferreira Almeida Rodrigues Vargas
Data: 23/11/2024
"""

import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from chrome_config import get_chrome_options
from login_util import login, verificar_login
from screenshot_util import take_evidence

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class TestCT08CadastroSlide(unittest.TestCase):
    """
    CT-08 - Cadastro de Slides
    
    Requisito: RF08 - O sistema deve permitir o cadastro de slides em cursos
    
    Objetivo: Verificar se o sistema permite que um professor autenticado
    cadastre um novo slide (apresentação Google Slides) em um curso existente.
    
    Pré-condições:
        - Usuário autenticado como professor
        - Deve existir pelo menos um curso cadastrado
    """
    
    URL_BASE = "https://testes-codefolio.web.app/"
    
    # Dados do slide
    TITULO_SLIDE = "Apresentação de Teste Automatizado"
    URL_SLIDE = "https://docs.google.com/presentation/d/e/2PACX-1vQh5YD_sample/pub"
    
    def setUp(self):
        """Configuração inicial do teste"""
        print("\n" + "="*70)
        print("INICIANDO CT-08 - CADASTRO DE SLIDE")
        print("="*70)
        
        options = get_chrome_options()
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 15)
        # Screenshot counter gerenciado automaticamente
    
    def tearDown(self):
        """Finalização do teste"""
        print("\n" + "-"*70)
        print("Finalizando CT-08")
        print("-"*70)
        # self.driver.quit()
    
    def test_ct08_cadastro_slide(self):
        """
        Objetivo: Verificar se o sistema permite cadastrar um slide em um curso
        """
        
        # PASSO 1: Fazer login
        print("\n[PASSO 1] Fazendo login no sistema...")
        login(self.driver, self.URL_BASE)
        verificar_login(self.driver, self.wait)
        take_evidence(self.driver, self.id(), 1, "tela_inicial_apos_login")
        print("✓ Login realizado com sucesso")
        
        # PASSO 2: Navegar para Gerenciamento de Cursos
        print("\n[PASSO 2] Navegando para Gerenciamento de Cursos...")
        try:
            profile_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[aria-label='Configurações da Conta']")
                )
            )
            self.driver.execute_script("arguments[0].click();", profile_button)
            
            time.sleep(1)
            
            gerenciamento_item = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//li[normalize-space()='Gerenciamento de Cursos']")
                )
            )
            gerenciamento_item.click()
            
            self.wait.until(EC.url_contains("/manage-courses"))
            print("✓ Página de gerenciamento carregada")
            
            time.sleep(2)
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_navegar_gerenciamento")
            self.fail(f"FALHA ao navegar: {e}")
        
        # PASSO 3: Selecionar um curso
        print("\n[PASSO 3] Selecionando curso...")
        try:
            botao_gerenciar = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//button[contains(., 'Gerenciar Curso')])[1]")
                )
            )
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_gerenciar)
            time.sleep(1)
            botao_gerenciar.click()
            print("✓ Curso selecionado")
            
            time.sleep(3)
            
            # Scroll até o final da página
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            take_evidence(self.driver, self.id(), 2, "pagina_curso_antes_adicionar_slide")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_selecionar_curso")
            self.fail(f"FALHA ao selecionar curso: {e}")
        
        # PASSO 4: Navegar para aba de Slides
        print("\n[PASSO 4] Acessando aba de Slides...")
        try:
            # Busca aba de slides
            aba_slides = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[contains(text(), 'SLIDES') or contains(text(), 'Slides')]")
                )
            )
            
            self.driver.execute_script("arguments[0].click();", aba_slides)
            print("✓ Aba de slides acessada")
            
            time.sleep(3)
            
            # Scroll até o final
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            take_evidence(self.driver, self.id(), 3, "aba_slides_antes_cadastro")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_acessar_aba_slides")
            self.fail(f"FALHA ao acessar aba de slides: {e}")
        
        # PASSO 5: Preencher campo "Título do Slide"
        print("\n[PASSO 5] Preenchendo título do slide...")
        try:
            # Busca campo título
            campo_titulo = None
            seletores_titulo = [
                "//label[contains(., 'Título')]/following-sibling::div//input",
                "//input[@placeholder*='Título']",
                "//input[@name='titulo']"
            ]
            
            for seletor in seletores_titulo:
                try:
                    campo_titulo = self.driver.find_element(By.XPATH, seletor)
                    if campo_titulo.is_displayed():
                        break
                except:
                    continue
            
            if not campo_titulo:
                raise Exception("Campo 'Título' não encontrado")
            
            campo_titulo.clear()
            time.sleep(0.5)
            campo_titulo.send_keys(self.TITULO_SLIDE)
            print(f"✓ Título preenchido: '{self.TITULO_SLIDE}'")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_campo_titulo")
            self.fail(f"FALHA ao preencher título: {e}")
        
        # PASSO 6: Preencher campo "URL do Slide"
        print("\n[PASSO 6] Preenchendo URL do slide...")
        try:
            # Busca campo URL
            campo_url = None
            seletores_url = [
                "//label[contains(., 'URL')]/following-sibling::div//input",
                "//input[@placeholder*='URL']",
                "//input[@placeholder*='Google']",
                "//input[@name='url']"
            ]
            
            for seletor in seletores_url:
                try:
                    campo_url = self.driver.find_element(By.XPATH, seletor)
                    if campo_url.is_displayed():
                        break
                except:
                    continue
            
            if not campo_url:
                raise Exception("Campo 'URL' não encontrado")
            
            campo_url.clear()
            time.sleep(0.5)
            campo_url.send_keys(self.URL_SLIDE)
            print(f"✓ URL preenchida: '{self.URL_SLIDE}'")
            
            time.sleep(1)
            
            # Evidência 04: Formulário preenchido
            take_evidence(self.driver, self.id(), 4, "formulario_slide_preenchido")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_campo_url")
            self.fail(f"FALHA ao preencher URL: {e}")
        
        # PASSO 7: Clicar em "Adicionar Slide"
        print("\n[PASSO 7] Adicionando slide...")
        try:
            botao_adicionar = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Adicionar') or contains(., 'ADICIONAR')]")
                )
            )
            
            self.driver.execute_script("arguments[0].click();", botao_adicionar)
            print("✓ Botão 'Adicionar' clicado")
            
            # Aguarda processar
            time.sleep(3)
            
            # Fechar modal de sucesso se aparecer
            try:
                botao_ok = self.driver.find_element(By.XPATH, "//button[contains(., 'OK') or contains(., 'Ok')]")
                botao_ok.click()
                time.sleep(1)
            except:
                pass
            
            # Evidência 05: Após adicionar
            take_evidence(self.driver, self.id(), 5, "apos_adicionar_slide")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_adicionar_slide")
            self.fail(f"FALHA ao adicionar slide: {e}")
        
        # PASSO 8: Verificar se slide aparece na lista
        print("\n[PASSO 8] Verificando se slide foi cadastrado...")
        try:
            time.sleep(2)
            
            # Procura pelo título do slide na página
            slide_cadastrado = self.driver.find_element(
                By.XPATH,
                f"//*[contains(text(), '{self.TITULO_SLIDE}')]"
            )
            
            if slide_cadastrado:
                print(f"✓ SUCESSO: Slide '{self.TITULO_SLIDE}' encontrado na lista!")
                
                # Evidência 06: Slide na lista
                take_evidence(self.driver, self.id(), 6, "slide_cadastrado_lista")
                
                self.assertTrue(True, "Slide cadastrado com sucesso")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_verificar_cadastro")
            self.fail(f"FALHA: Slide não encontrado na lista: {e}")
        
        print("\n" + "="*70)
        print("CT-08 - CADASTRO DE SLIDE CONCLUÍDO")
        print("="*70)


if __name__ == "__main__":
    unittest.main()
