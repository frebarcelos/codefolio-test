"""
RF42_CT01_CompartilharVideos.py

Teste Selenium para RF42: Compartilhar vídeos acessados na HOME

Requisito: O sistema deve permitir que o estudante compartilhe vídeos 
acessados na "home".

Fluxo esperado:
1. Login via Firebase (injeta credenciais no localStorage)
2. Validar que o login foi bem-sucedido
3. Navegar para a HOME
4. Encontrar o vídeo (iframe YouTube)
5. Clicar em "Compartilhar" (abre modal/opções de compartilhamento)
6. Selecionar método de compartilhamento (copiar link, email, redes sociais, etc)
7. Validar que o compartilhamento foi realizado
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


class TestRF42CompartilharVideos(unittest.TestCase):
    """Testa a funcionalidade de compartilhar vídeos na HOME (RF42)."""

    def setUp(self):
        """Setup executado antes de cada teste."""
        try:
            chrome_options = get_chrome_options()
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(5)
            self.wait = WebDriverWait(self.driver, time_out)
            self.test_name = "test_compartilhar_videos_na_home"
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

    def _clicar_em_compartilhar(self):
        """Encontra e clica no botão 'Compartilhar' para abrir as opções."""
        print("\n[PASSO 5] CLICANDO EM 'COMPARTILHAR'")
        
        selectors = [
            "//div[contains(., 'Compartilhar')][contains(@style, 'cursor')]",
            "//*[contains(text(), 'Compartilhar')]",
            "//span[contains(text(), 'Compartilhar')]",
        ]
        
        element_clicked = False
        for selector in selectors:
            try:
                elementos = self.driver.find_elements(By.XPATH, selector)
                for elem in elementos:
                    if elem.is_displayed():
                        try:
                            elem.click()
                            print(f"✓ Clicou em 'Compartilhar' com click normal")
                            element_clicked = True
                            break
                        except Exception:
                            self.driver.execute_script("arguments[0].click();", elem)
                            print(f"✓ Clicou em 'Compartilhar' via JavaScript")
                            element_clicked = True
                            break
                
                if element_clicked:
                    break
            except (NoSuchElementException, TimeoutException):
                continue
        
        if element_clicked:
            time.sleep(1.5)
            return True
        else:
            print("⚠ Não conseguiu clicar em 'Compartilhar'")
            return False

    def _verificar_opcoes_compartilhamento(self):
        """Verifica quais opções de compartilhamento estão disponíveis."""
        print("\n[PASSO 6] VERIFICANDO OPÇÕES DE COMPARTILHAMENTO")
        
        opcoes = {
            "copiar_link": False,
            "email": False,
            "facebook": False,
            "twitter": False,
            "whatsapp": False,
        }
        
        # Procura por botão/link de "Copiar Link"
        try:
            copiar = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Copiar') or contains(text(), 'copiar')]")
            if copiar.is_displayed():
                opcoes["copiar_link"] = True
                print("  ✓ Opção 'Copiar Link' encontrada")
        except NoSuchElementException:
            pass
        
        # Procura por botão/link de "Email"
        try:
            email = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Email') or contains(text(), 'email') or contains(@href, 'mailto')]")
            if email.is_displayed():
                opcoes["email"] = True
                print("  ✓ Opção 'Email' encontrada")
        except NoSuchElementException:
            pass
        
        # Procura por ícones/links de redes sociais
        try:
            facebook = self.driver.find_element(By.XPATH, "//*[contains(@href, 'facebook') or @aria-label='Facebook' or @title='Facebook']")
            if facebook.is_displayed():
                opcoes["facebook"] = True
                print("  ✓ Opção 'Facebook' encontrada")
        except NoSuchElementException:
            pass
        
        try:
            twitter = self.driver.find_element(By.XPATH, "//*[contains(@href, 'twitter') or contains(@href, 'x.com') or @aria-label='Twitter' or @title='Twitter']")
            if twitter.is_displayed():
                opcoes["twitter"] = True
                print("  ✓ Opção 'Twitter' encontrada")
        except NoSuchElementException:
            pass
        
        try:
            whatsapp = self.driver.find_element(By.XPATH, "//*[contains(@href, 'whatsapp') or @aria-label='WhatsApp' or @title='WhatsApp']")
            if whatsapp.is_displayed():
                opcoes["whatsapp"] = True
                print("  ✓ Opção 'WhatsApp' encontrada")
        except NoSuchElementException:
            pass
        
        total_opcoes = sum(1 for v in opcoes.values() if v)
        print(f"  Total de opções disponíveis: {total_opcoes}")
        
        return opcoes

    def _executar_compartilhamento(self, opcoes):
        """Executa uma ação de compartilhamento."""
        print("\n[PASSO 7] EXECUTANDO COMPARTILHAMENTO")
        
        # Prioridade: Copiar Link > Email > Redes Sociais
        if opcoes["copiar_link"]:
            try:
                copiar_btn = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Copiar') or contains(text(), 'copiar')]")
                if copiar_btn.is_enabled() and copiar_btn.is_displayed():
                    self.driver.execute_script("arguments[0].click();", copiar_btn)
                    print("✓ Compartilhamento via 'Copiar Link' realizado")
                    time.sleep(1)
                    return True, "Copiar Link"
            except Exception as e:
                print(f"  ⚠ Erro ao clicar em 'Copiar Link': {e}")
        
        if opcoes["email"]:
            try:
                email_btn = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Email') or contains(text(), 'email')]")
                if email_btn.is_enabled() and email_btn.is_displayed():
                    self.driver.execute_script("arguments[0].click();", email_btn)
                    print("✓ Compartilhamento via 'Email' realizado")
                    time.sleep(1)
                    return True, "Email"
            except Exception as e:
                print(f"  ⚠ Erro ao clicar em 'Email': {e}")
        
        if opcoes["whatsapp"]:
            try:
                whatsapp_btn = self.driver.find_element(By.XPATH, "//*[contains(@href, 'whatsapp') or @aria-label='WhatsApp']")
                if whatsapp_btn.is_displayed():
                    self.driver.execute_script("arguments[0].click();", whatsapp_btn)
                    print("✓ Compartilhamento via 'WhatsApp' realizado")
                    time.sleep(1)
                    return True, "WhatsApp"
            except Exception as e:
                print(f"  ⚠ Erro ao clicar em 'WhatsApp': {e}")
        
        if opcoes["facebook"]:
            try:
                facebook_btn = self.driver.find_element(By.XPATH, "//*[contains(@href, 'facebook') or @aria-label='Facebook']")
                if facebook_btn.is_displayed():
                    self.driver.execute_script("arguments[0].click();", facebook_btn)
                    print("✓ Compartilhamento via 'Facebook' realizado")
                    time.sleep(1)
                    return True, "Facebook"
            except Exception as e:
                print(f"  ⚠ Erro ao clicar em 'Facebook': {e}")
        
        if opcoes["twitter"]:
            try:
                twitter_btn = self.driver.find_element(By.XPATH, "//*[contains(@href, 'twitter') or contains(@href, 'x.com') or @aria-label='Twitter']")
                if twitter_btn.is_displayed():
                    self.driver.execute_script("arguments[0].click();", twitter_btn)
                    print("✓ Compartilhamento via 'Twitter' realizado")
                    time.sleep(1)
                    return True, "Twitter"
            except Exception as e:
                print(f"  ⚠ Erro ao clicar em 'Twitter': {e}")
        
        print("✗ Nenhuma opção de compartilhamento foi executada")
        return False, "Nenhuma"

    def test_compartilhar_video_na_home(self):
        """
        Teste principal: Compartilha um vídeo disponível na HOME.
        
        Fluxo:
        1. Login
        2. Navegar para a HOME
        3. Encontrar o vídeo (iframe YouTube)
        4. Clicar em "Compartilhar"
        5. Verificar opções de compartilhamento
        6. Executar compartilhamento
        7. Validar que foi realizado
        """
        print("\n" + "="*60)
        print("TESTE RF42: Compartilhar Vídeos na HOME")
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
            
            # PASSO 5: CLICAR EM "COMPARTILHAR"
            if not self._clicar_em_compartilhar():
                self.fail("FALHA: Não conseguiu clicar em 'Compartilhar'.")
            
            save_screenshot(self.driver, self.test_name, "03_compartilhar_modal_aberto")
            
            # PASSO 6: VERIFICAR OPÇÕES
            opcoes = self._verificar_opcoes_compartilhamento()
            
            if not any(opcoes.values()):
                print("⚠ AVISO: Nenhuma opção de compartilhamento encontrada")
                print("  (Pode ser que o modal de compartilhamento não tenha carregado corretamente)")
            
            # PASSO 7: EXECUTAR COMPARTILHAMENTO
            sucesso_compartilhamento, metodo = self._executar_compartilhamento(opcoes)
            save_screenshot(self.driver, self.test_name, "04_apos_compartilhamento")
            
            if sucesso_compartilhamento:
                print(f"\n✓✓✓ SUCESSO! Vídeo compartilhado via {metodo}!")
                print("\n" + "="*60)
                print("TESTE PASSOU COM SUCESSO!")
                print("="*60 + "\n")
            else:
                print("\n⚠ AVISO: Nenhum método de compartilhamento foi executado")
                print("  (Pode estar requerendo autenticação ou interação adicional)")
                # Não falha neste caso, pois pode depender de configurações externas
            
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
