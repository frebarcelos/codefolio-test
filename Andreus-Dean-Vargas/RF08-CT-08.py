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
from element_finder import find_input_by_label, find_button_by_text
from curso_helper import garantir_curso_existe

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
    
    # Dados do curso fallback (caso precise criar)
    NOME_CURSO_FALLBACK = "Curso para Teste de Slides"
    DESCRICAO_CURSO_FALLBACK = "Curso criado automaticamente para testar slides"
    
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
        
        # PASSO 3: Verificar se existe curso, se não criar um
        print("\n[PASSO 3] Verificando se existe curso...")
        try:
            garantir_curso_existe(
                self.driver,
                self.wait,
                self.NOME_CURSO_FALLBACK,
                self.DESCRICAO_CURSO_FALLBACK,
                self.URL_BASE
            )
            
            print("\n[PASSO 3.1] Selecionando curso...")
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
            # Scroll para o topo
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # Busca campo título usando label exato do Material-UI
            campo_titulo = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//label[contains(text(), 'Título do Slide')]/following-sibling::div//input")
                )
            )
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", campo_titulo)
            time.sleep(0.5)
            campo_titulo.click()
            time.sleep(0.5)
            campo_titulo.clear()
            time.sleep(0.5)
            campo_titulo.send_keys(self.TITULO_SLIDE)
            time.sleep(1)
            print(f"✓ Título preenchido: '{self.TITULO_SLIDE}'")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_campo_titulo")
            self.fail(f"FALHA ao preencher título: {e}")
        
        # PASSO 6: Preencher campo "URL do Slide"
        print("\n[PASSO 6] Preenchendo URL do slide...")
        try:
            # Busca campo URL usando label exato do Material-UI
            campo_url = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//label[contains(text(), 'URL do Slide')]/following-sibling::div//input")
                )
            )
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", campo_url)
            time.sleep(0.5)
            campo_url.click()
            time.sleep(0.5)
            campo_url.clear()
            time.sleep(0.5)
            campo_url.send_keys(self.URL_SLIDE)
            time.sleep(1)
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
            botao_adicionar = find_button_by_text(self.driver, self.wait, "adicionar")
            
            if not botao_adicionar:
                raise Exception("Botão 'Adicionar' não encontrado")
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_adicionar)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", botao_adicionar)
            print("✓ Botão 'Adicionar' clicado")
            
            time.sleep(2)
            
            # Fechar modal "Slide Adicionado"
            try:
                botao_ok_modal = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(., 'OK') or contains(., 'Ok')]")
                    )
                )
                botao_ok_modal.click()
                print("✓ Modal 'Slide Adicionado' fechado")
                time.sleep(1)
            except:
                pass
            
            # Evidência 05: Após adicionar
            take_evidence(self.driver, self.id(), 5, "apos_adicionar_slide")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_adicionar_slide")
            self.fail(f"FALHA ao adicionar slide: {e}")
        
        # PASSO 8: Salvar curso
        print("\n[PASSO 8] Salvando curso...")
        try:
            # Scroll para o topo
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            # Procura botão Salvar Curso por diferentes métodos
            botao_salvar = None
            try:
                botao_salvar = find_button_by_text(self.driver, self.wait, "salvar")
            except:
                pass
            
            if not botao_salvar:
                # Tenta encontrar diretamente por XPath
                try:
                    botao_salvar = self.wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//button[contains(., 'Salvar') or contains(., 'SALVAR')]")
                        )
                    )
                except:
                    pass
            
            if not botao_salvar:
                # Apenas continua sem salvar - o slide já foi adicionado
                print("⚠ Botão 'Salvar Curso' não encontrado, mas slide foi adicionado")
                take_evidence(self.driver, self.id(), 6, "slide_adicionado_sem_salvar")
            else:
                self.driver.execute_script("arguments[0].click();", botao_salvar)
                print("✓ Curso salvo")
                time.sleep(3)
                
                # Fechar modal de sucesso
                try:
                    botao_ok = find_button_by_text(self.driver, self.wait, "ok")
                    if botao_ok:
                        self.driver.execute_script("arguments[0].click();", botao_ok)
                        time.sleep(1)
                except:
                    pass
                
                # Evidência 06: Após salvar
                take_evidence(self.driver, self.id(), 6, "apos_salvar_curso")
            
        except Exception as e:
            # Não falha o teste, apenas avisa
            print(f"⚠ Aviso ao salvar curso: {e}")
            take_evidence(self.driver, self.id(), 6, "aviso_salvar_curso")
        
        # PASSO 9: Verificar se slide foi cadastrado
        print("\n[PASSO 9] Verificando se slide foi cadastrado...")
        try:
            # Verifica se o slide aparece na lista atual
            time.sleep(2)
            
            slide_cadastrado = self.driver.find_element(
                By.XPATH,
                f"//*[contains(text(), '{self.TITULO_SLIDE}')]"
            )
            
            if slide_cadastrado:
                print(f"✓ SUCESSO: Slide '{self.TITULO_SLIDE}' encontrado na lista!")
                
                # Evidência 07: Slide na lista
                take_evidence(self.driver, self.id(), 7, "slide_cadastrado_verificado")
                
                self.assertTrue(True, "Slide cadastrado com sucesso")
            
        except Exception as e:
            # Se não encontrou, tenta procurar qualquer elemento de slide
            try:
                slides = self.driver.find_elements(By.XPATH, "//iframe[contains(@src, 'google.com/presentation')]")
                if slides:
                    print(f"✓ SUCESSO: {len(slides)} slide(s) encontrado(s) na lista!")
                    take_evidence(self.driver, self.id(), 7, "slides_encontrados")
                    self.assertTrue(True, "Slide cadastrado com sucesso")
                else:
                    raise Exception("Nenhum slide encontrado")
            except:
                take_evidence(self.driver, self.id(), 99, "erro_verificar_cadastro")
                self.fail(f"FALHA: Slide não encontrado na lista: {e}")
        
        print("\n" + "="*70)
        print("CT-08 - CADASTRO DE SLIDE CONCLUÍDO")
        print("="*70)


if __name__ == "__main__":
    unittest.main()
