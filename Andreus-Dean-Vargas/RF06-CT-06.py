"""
CT-06 - Edição de Vídeos (RF06)
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


class TestCT06EdicaoVideo(unittest.TestCase):
    """
    CT-06 - Edição de Vídeos
    
    Requisito: RF06 - O sistema deve permitir a edição de vídeos cadastrados
    
    Objetivo: Verificar se o sistema permite que um professor autenticado
    edite as informações de um vídeo existente em um curso.
    
    Pré-condições:
        - Usuário autenticado como professor
        - Deve existir um curso com pelo menos um vídeo cadastrado
    """
    
    URL_BASE = "https://testes-codefolio.web.app/"
    
    # Dados para edição
    NOVO_TITULO = "Vídeo Editado Automaticamente"
    NOVA_URL = "https://www.youtube.com/watch?v=9bZkp7q19f0"
    
    def setUp(self):
        """Configuração inicial do teste"""
        print("\n" + "="*70)
        print("INICIANDO CT-06 - EDIÇÃO DE VÍDEO")
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
        print("Finalizando CT-06")
        print("-"*70)
        # self.driver.quit()
    
    def test_ct06_edicao_video(self):
        """
        Objetivo: Verificar se o sistema permite editar um vídeo existente
        """
        
        # PASSO 1: Fazer login
        print("\n[PASSO 1] Fazendo login no sistema...")
        login(self.driver, self.URL_BASE)
        verificar_login(self.driver, self.wait)
        take_evidence(self.driver, self.id(), 1, "tela_inicial_apos_login")
        print("✓ Login realizado com sucesso")
        
        # PASSO 2-3: Navegar para Gerenciamento e selecionar curso
        print("\n[PASSO 2] Navegando para curso com vídeos...")
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
            time.sleep(2)
            
            # Seleciona primeiro curso
            botao_gerenciar = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//button[contains(., 'Gerenciar Curso')])[1]")
                )
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_gerenciar)
            time.sleep(1)
            botao_gerenciar.click()
            time.sleep(3)
            
            print("✓ Curso acessado")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_navegar_curso")
            self.fail(f"FALHA ao navegar: {e}")
        
        # PASSO 4: Acessar aba de Vídeos
        print("\n[PASSO 3] Acessando aba de Vídeos...")
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            aba_videos = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[contains(text(), 'VÍDEOS') or contains(text(), 'Vídeos')]")
                )
            )
            self.driver.execute_script("arguments[0].click();", aba_videos)
            time.sleep(3)
            
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            take_evidence(self.driver, self.id(), 2, "aba_videos_antes_edicao")
            print("✓ Aba de vídeos acessada")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_acessar_aba_videos")
            self.fail(f"FALHA ao acessar aba: {e}")
        
        # PASSO 5: Clicar no ícone de edição do primeiro vídeo
        print("\n[PASSO 4] Clicando no ícone de edição...")
        try:
            # Busca primeiro botão de edição na lista de vídeos
            icone_editar = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//*[contains(text(), 'Vídeos Cadastrados')]/following-sibling::div//button)[1]")
                )
            )
            
            self.driver.execute_script("arguments[0].click();", icone_editar)
            print("✓ Ícone de edição clicado")
            
            time.sleep(2)
            
            take_evidence(self.driver, self.id(), 3, "modal_edicao_video_aberto")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_abrir_edicao")
            self.fail(f"FALHA ao abrir edição: {e}")
        
        # PASSO 6: Editar título do vídeo
        print("\n[PASSO 5] Editando título do vídeo...")
        try:
            campo_titulo = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//label[contains(., 'Título')]/following-sibling::div//input")
                )
            )
            
            campo_titulo.clear()
            time.sleep(0.5)
            campo_titulo.send_keys(self.NOVO_TITULO)
            print(f"✓ Título alterado para: '{self.NOVO_TITULO}'")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_editar_titulo")
            self.fail(f"FALHA ao editar título: {e}")
        
        # PASSO 7: Editar URL do vídeo
        print("\n[PASSO 6] Editando URL do vídeo...")
        try:
            campo_url = self.driver.find_element(
                By.XPATH,
                "//label[contains(., 'URL')]/following-sibling::div//input"
            )
            
            campo_url.clear()
            time.sleep(0.5)
            campo_url.send_keys(self.NOVA_URL)
            print("✓ URL atualizada")
            
            time.sleep(1)
            
            take_evidence(self.driver, self.id(), 4, "formulario_video_editado")
            
        except Exception as e:
            print("⚠ Campo URL não encontrado")
        
        # PASSO 8: Salvar alterações
        print("\n[PASSO 7] Salvando alterações...")
        try:
            botao_salvar = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Salvar') or contains(., 'SALVAR')]")
                )
            )
            
            botao_salvar.click()
            print("✓ Botão 'Salvar' clicado")
            
            time.sleep(3)
            
            # Fechar modal de sucesso
            try:
                botao_ok = self.driver.find_element(By.XPATH, "//button[contains(., 'OK')]")
                botao_ok.click()
                time.sleep(1)
            except:
                pass
            
            take_evidence(self.driver, self.id(), 5, "apos_salvar_edicao")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_salvar")
            self.fail(f"FALHA ao salvar: {e}")
        
        # PASSO 9: Verificar se alterações foram salvas
        print("\n[PASSO 8] Verificando se vídeo foi editado...")
        try:
            time.sleep(2)
            
            video_editado = self.driver.find_element(
                By.XPATH,
                f"//*[contains(text(), '{self.NOVO_TITULO}')]"
            )
            
            if video_editado:
                print(f"✓ SUCESSO: Vídeo editado encontrado com título '{self.NOVO_TITULO}'!")
                
                take_evidence(self.driver, self.id(), 6, "video_editado_verificado")
                
                self.assertTrue(True, "Vídeo editado com sucesso")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_verificar_edicao")
            self.fail(f"FALHA: Alterações não foram salvas: {e}")
        
        print("\n" + "="*70)
        print("CT-06 - EDIÇÃO DE VÍDEO CONCLUÍDO")
        print("="*70)


if __name__ == "__main__":
    unittest.main()
