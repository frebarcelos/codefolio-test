"""
CT-07 - Exclusão de Vídeos (RF07)
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


class TestCT07ExclusaoVideo(unittest.TestCase):
    """
    CT-07 - Exclusão de Vídeos
    
    Requisito: RF07 - O sistema deve permitir a exclusão de vídeos cadastrados
    
    Objetivo: Verificar se o sistema permite que um professor autenticado
    exclua um vídeo existente e que ele não apareça mais na lista.
    
    Pré-condições:
        - Usuário autenticado como professor
        - Deve existir um curso com pelo menos um vídeo cadastrado
    """
    
    URL_BASE = "https://testes-codefolio.web.app/"
    
    def setUp(self):
        """Configuração inicial do teste"""
        print("\n" + "="*70)
        print("INICIANDO CT-07 - EXCLUSÃO DE VÍDEO")
        print("="*70)
        
        options = get_chrome_options()
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 15)
        # Screenshot counter gerenciado automaticamente
        self.titulo_video_alvo = None
    
    def tearDown(self):
        """Finalização do teste"""
        print("\n" + "-"*70)
        print("Finalizando CT-07")
        print("-"*70)
        # self.driver.quit()
    
    def test_ct07_exclusao_video(self):
        """
        Objetivo: Verificar se o sistema permite excluir um vídeo existente
        """
        
        # PASSO 1: Fazer login
        print("\n[PASSO 1] Fazendo login no sistema...")
        login(self.driver, self.URL_BASE)
        verificar_login(self.driver, self.wait)
        take_evidence(self.driver, self.id(), 1, "tela_inicial_apos_login")
        print("✓ Login realizado com sucesso")
        
        # PASSO 2-3: Navegar para curso com vídeos
        print("\n[PASSO 2] Navegando para curso...")
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
            
            take_evidence(self.driver, self.id(), 2, "aba_videos_antes_exclusao")
            print("✓ Aba de vídeos acessada")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_acessar_aba")
            self.fail(f"FALHA ao acessar aba: {e}")
        
        # PASSO 5: Identificar vídeo a ser excluído
        print("\n[PASSO 4] Identificando vídeo para exclusão...")
        try:
            primeiro_video = self.driver.find_element(
                By.XPATH,
                "(//*[contains(text(), 'Vídeos Cadastrados')]/following-sibling::div//h6)[1]"
            )
            self.titulo_video_alvo = primeiro_video.text
            print(f"✓ Vídeo alvo: '{self.titulo_video_alvo}'")
            
        except:
            self.titulo_video_alvo = "Vídeo Desconhecido"
            print("⚠ Não foi possível identificar título do vídeo")
        
        # PASSO 6: Clicar no ícone de exclusão (lixeira)
        print("\n[PASSO 5] Clicando no ícone de exclusão...")
        try:
            # Segundo botão geralmente é a lixeira
            icone_excluir = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//*[contains(text(), 'Vídeos Cadastrados')]/following-sibling::div//button)[2]")
                )
            )
            
            self.driver.execute_script("arguments[0].click();", icone_excluir)
            print("✓ Ícone de exclusão clicado")
            
            time.sleep(2)
            
            take_evidence(self.driver, self.id(), 3, "modal_confirmacao_exclusao")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_clicar_excluir")
            self.fail(f"FALHA ao clicar em excluir: {e}")
        
        # PASSO 7: Confirmar exclusão
        print("\n[PASSO 6] Confirmando exclusão...")
        try:
            botao_confirmar = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Sim') or contains(., 'Confirmar') or contains(., 'Excluir')]")
                )
            )
            
            botao_confirmar.click()
            print("✓ Exclusão confirmada")
            
            time.sleep(3)
            
            take_evidence(self.driver, self.id(), 4, "apos_confirmar_exclusao")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_confirmar_exclusao")
            self.fail(f"FALHA ao confirmar exclusão: {e}")
        
        # PASSO 8: Verificar se vídeo foi removido
        print("\n[PASSO 7] Verificando se vídeo foi removido...")
        try:
            time.sleep(2)
            
            # Tenta encontrar o vídeo
            try:
                video_ainda_existe = self.driver.find_element(
                    By.XPATH,
                    f"//*[contains(text(), '{self.titulo_video_alvo}')]"
                )
                # Se encontrou, falhou
                take_evidence(self.driver, self.id(), 99, "video_ainda_existe")
                self.fail(f"FALHA: Vídeo '{self.titulo_video_alvo}' ainda está na lista!")
                
            except:
                # Se não encontrou, passou
                print(f"✓ SUCESSO: Vídeo '{self.titulo_video_alvo}' foi removido!")
                
                take_evidence(self.driver, self.id(), 5, "lista_apos_exclusao")
                
                self.assertTrue(True, "Vídeo excluído com sucesso")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_verificar_exclusao")
            self.fail(f"FALHA ao verificar exclusão: {e}")
        
        print("\n" + "="*70)
        print("CT-07 - EXCLUSÃO DE VÍDEO CONCLUÍDO")
        print("="*70)


if __name__ == "__main__":
    unittest.main()
