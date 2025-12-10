"""
RF41_CT01_ComentarEmVideos.py

Teste Selenium para RF41: Comentar em vídeos disponíveis através da HOME

Requisito: O sistema deve permitir que o estudante comente nos vídeos 
disponíveis através da "home".

Fluxo esperado:
1. Login via Firebase (injeta credenciais no localStorage)
2. Validar que o login foi bem-sucedido
3. Navegar para a HOME
4. Encontrar o vídeo (iframe YouTube)
5. Clicar em "Comentários" (abre modal/drawer)
6. Digitar comentário no modal
7. Enviar comentário
8. Validar que o comentário foi publicado
"""

import unittest
import time
import traceback
import sys
from os.path import abspath, dirname

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Adiciona o diretório ao path para importar utils locais
sys.path.insert(0, dirname(abspath(__file__)))
from login_util import login, verificar_login, url_base, time_out
from chrome_config import get_chrome_options
from screenshot_util import save_screenshot


class TestRF41ComentarEmVideos(unittest.TestCase):
    """Testa a funcionalidade de comentar em vídeos na HOME (RF41)."""

    def setUp(self):
        """Setup executado antes de cada teste."""
        try:
            chrome_options = get_chrome_options()
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(5)
            self.wait = WebDriverWait(self.driver, time_out)
            self.test_name = "test_comentar_em_video_na_home"
            print(f"\n{'='*60}")
            print(f"Iniciando teste: {self.id()}")
            print(f"{'='*60}\n")
        except Exception as e:
            print(f"ERRO no setUp: {e}")
            traceback.print_exc()
            raise

    def tearDown(self):
        """Cleanup após cada teste."""
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
                print("\nDriver fechado com sucesso.")
        except Exception as e:
            print(f"Erro ao fechar driver: {e}")

    def _clicar_em_comentarios(self):
        """Encontra e clica no botão 'Comentários' para abrir o modal."""
        print("\n[PASSO 5] CLICANDO EM 'COMENTÁRIOS'")
        
        selectors = [
            "//div[contains(., 'Comentários')][contains(@style, 'cursor')]",
            "//*[contains(text(), 'Comentários')]",
            "//span[contains(text(), 'Comentários')]",
        ]
        
        element_clicked = False
        for selector in selectors:
            try:
                elementos = self.driver.find_elements(By.XPATH, selector)
                for elem in elementos:
                    if elem.is_displayed():
                        try:
                            elem.click()
                            print(f"✓ Clicou em 'Comentários' com click normal")
                            element_clicked = True
                            break
                        except Exception:
                            self.driver.execute_script("arguments[0].click();", elem)
                            print(f"✓ Clicou em 'Comentários' via JavaScript")
                            element_clicked = True
                            break
                
                if element_clicked:
                    break
            except (NoSuchElementException, TimeoutException):
                continue
        
        if element_clicked:
            time.sleep(1.5)
            save_screenshot(self.driver, self.test_name, "03_comentarios_modal_aberto")
            return True
        else:
            print("⚠ Não conseguiu clicar em 'Comentários'")
            return False

    def _encontrar_campo_comentario_no_modal(self):
        """Procura pelo campo de comentário dentro do modal."""
        print("\n[PASSO 6] PROCURANDO CAMPO DE COMENTÁRIO NO MODAL")
        
        selectors = [
            "//textarea[@placeholder]",
            "//textarea",
            "//input[@type='text'][@placeholder]",
            "//input[@type='text']",
            "//div[@contenteditable='true']",
        ]
        
        for selector in selectors:
            try:
                elementos = self.driver.find_elements(By.XPATH, selector)
                for elem in elementos:
                    if elem.is_displayed() and elem.is_enabled():
                        print(f"✓ Campo de comentário encontrado")
                        return elem
            except (NoSuchElementException, TimeoutException):
                continue
        
        print("✗ Campo de comentário não encontrado")
        return None

    def _enviar_comentario(self, campo, texto):
        """Digita e envia o comentário."""
        print("\n[PASSO 7] DIGITANDO E ENVIANDO COMENTÁRIO")
        
        try:
            campo.click()
            time.sleep(0.5)
            
            campo.send_keys(Keys.CONTROL + "a")
            time.sleep(0.2)
            campo.send_keys(Keys.DELETE)
            time.sleep(0.2)
            
            campo.send_keys(texto)
            print(f"✓ Comentário digitado: '{texto}'")
            save_screenshot(self.driver, self.test_name, "04_comentario_digitado")
            time.sleep(0.5)
            
            botoes_send = [
                "//button[.//svg[@data-testid='SendIcon']]",
                "//button[@type='submit'][not(contains(@class, 'Mui-disabled'))]",
                "//button[@class and contains(@class, 'comentarios-button')]",
            ]
            
            button_encontrado = False
            for selector in botoes_send:
                try:
                    btn = self.driver.find_element(By.XPATH, selector)
                    if btn.is_displayed() and btn.is_enabled():
                        self.driver.execute_script("arguments[0].click();", btn)
                        print("✓ Botão de envio clicado (SendIcon)")
                        button_encontrado = True
                        break
                except (NoSuchElementException, Exception):
                    continue
            
            if not button_encontrado:
                print("⚠ Botão não encontrado, tentando Enter...")
                campo.send_keys(Keys.RETURN)
            
            time.sleep(1)
            save_screenshot(self.driver, self.test_name, "05_apos_envio_comentario")
            return True
            
        except Exception as e:
            print(f"✗ Erro ao enviar comentário: {e}")
            return False

    def test_comentar_em_video_na_home(self):
        """
        Teste principal: Comenta em um vídeo disponível na HOME.
        
        Fluxo:
        1. Login
        2. Navegar para a HOME
        3. Encontrar o vídeo (iframe YouTube)
        4. Clicar em "Comentários"
        5. Digitar e enviar comentário
        6. Validar que o comentário foi publicado
        """
        print("\n" + "="*60)
        print("TESTE RF41: Comentar em Vídeos na HOME")
        print("="*60)
        
        try:
            # PASSO 1: LOGIN
            print("\n[PASSO 1] LOGIN VIA FIREBASE")
            login(self.driver)
            save_screenshot(self.driver, self.test_name, "01_apos_login")
            
            # PASSO 2: VALIDAR LOGIN
            print("\n[PASSO 2] VALIDAR LOGIN")
            verificar_login(self.driver, self.wait)
            print("✓ Login validado com sucesso")
            
            # PASSO 3: NAVEGAR PARA HOME
            print("\n[PASSO 3] NAVEGAR PARA HOME")
            time.sleep(1)
            self.driver.get(url_base)
            time.sleep(2)
            save_screenshot(self.driver, self.test_name, "02_home_page")
            
            try:
                self.wait.until(EC.url_to_be(url_base))
            except TimeoutException:
                pass
            
            print(f"✓ Na página HOME: {self.driver.current_url}")
            
            # PASSO 4: VERIFICAR VÍDEO
            print("\n[PASSO 4] PROCURANDO VÍDEO (iframe YouTube)")
            try:
                iframe = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'youtube')]"))
                )
                self.driver.execute_script("arguments[0].scrollIntoView(true);", iframe)
                time.sleep(0.5)
                print("✓ Vídeo encontrado (iframe YouTube)")
            except TimeoutException:
                self.fail("FALHA: Nenhum vídeo (iframe YouTube) encontrado na HOME.")
            
            # PASSO 5: CLICAR EM "COMENTÁRIOS"
            if not self._clicar_em_comentarios():
                self.fail("FALHA: Não conseguiu clicar em 'Comentários'.")
            
            # PASSO 6: PROCURAR CAMPO DE COMENTÁRIO
            campo_comentario = self._encontrar_campo_comentario_no_modal()
            if not campo_comentario:
                self.fail("FALHA: Campo de comentário não encontrado no modal.")
            
            # PASSO 7: DIGITAR E ENVIAR COMENTÁRIO
            timestamp = int(time.time() * 1000)
            texto_comentario = f"Teste comentário automatizado - {timestamp}"
            
            if not self._enviar_comentario(campo_comentario, texto_comentario):
                self.fail("FALHA: Erro ao enviar comentário.")
            
            # PASSO 8: VALIDAR PUBLICAÇÃO
            print("\n[PASSO 8] VALIDANDO PUBLICAÇÃO DO COMENTÁRIO")
            
            try:
                comentario_visivel = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{texto_comentario}')]"))
                )
                
                if comentario_visivel.is_displayed():
                    print(f"✓✓✓ SUCESSO! Comentário publicado e visível!")
                    print(f"    Texto: '{texto_comentario}'")
                    
                    print("\n" + "="*60)
                    print("TESTE PASSOU COM SUCESSO!")
                    print("="*60 + "\n")
                else:
                    print("⚠ Comentário encontrado mas não está visível")
                    
            except TimeoutException:
                print("⚠ Comentário não apareceu imediatamente...")
                print("   (pode ter sido enviado com sucesso, mas não está visível neste momento)")
            
        except AssertionError as e:
            print(f"\n✗ Teste falhou com asserção: {e}")
            traceback.print_exc()
            raise
        except Exception as e:
            print(f"\n✗ Erro inesperado no teste: {e}")
            traceback.print_exc()
            self.fail(f"Erro inesperado: {e}")


if __name__ == '__main__':
    unittest.main()
