"""
RF44_CT01_AcessarCursosRecomendadosComPIN.py

Teste Selenium para RF44: Cursos Recomendados (Acessar com PIN)

Requisito: Permitir que o estudante acesse cursos recomendados a partir da home mediante inserção de um código PIN.
Fluxo:
1. Login via Firebase (injeta credenciais no localStorage)
2. Localizar o card do curso 'Grupo 2' na seção de recomendados (ou globalmente)
3. Clicar em 'Acessar'
4. Detectar modal de PIN e inserir 'grupo2'
5. Confirmar e validar acesso (mudança de URL ou conteúdo visível)
"""

import unittest
import time
import traceback
import sys
from os.path import abspath, dirname

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

sys.path.insert(0, dirname(abspath(__file__)))
from login_util import login, verificar_login, url_base, time_out
from chrome_config import get_chrome_options
from screenshot_util import save_screenshot


class TestRF44AcessarCursosComPIN(unittest.TestCase):
    def setUp(self):
        try:
            chrome_options = get_chrome_options()
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(5)
            try:
                self.driver.maximize_window()
            except Exception:
                pass
            self.wait = WebDriverWait(self.driver, time_out)
            self.test_name = "test_acessar_cursos_recomendados_com_pin"
            print(f"\n{'='*60}")
            print(f"Iniciando teste: {self.id()}")
            print(f"{'='*60}\n")
        except Exception as e:
            print(f"ERRO no setUp: {e}")
            traceback.print_exc()
            raise

    def tearDown(self):
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
                print("\nDriver fechado com sucesso.")
        except Exception as e:
            print(f"Erro ao fechar driver: {e}")

    def _encontrar_secao_recomendados(self):
        selectors = [
            "//section[.//h2[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'recomend')]]",
            "//div[contains(@class, 'recomend') or contains(@class, 'recomendados') or contains(., 'Cursos recomendados')]",
            "//*[contains(text(), 'Cursos recomendados') or contains(text(), 'Recomendados') or contains(text(), 'Cursos Recomendados')]",
        ]
        for sel in selectors:
            try:
                elems = self.driver.find_elements(By.XPATH, sel)
                for e in elems:
                    if e.is_displayed():
                        return e
            except Exception:
                continue
        return None

    def _detectar_modal_pin(self):
        try:
            pin_inputs = self.driver.find_elements(By.XPATH, "//input[@type='password'] | //input[contains(translate(@placeholder, 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'PIN')] | //input[contains(translate(@placeholder, 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CÓDIGO') or contains(translate(@placeholder, 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CODIGO')] | //input[contains(translate(@id,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'PIN')] | //input[contains(translate(@name,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'PIN')] | //input[contains(translate(@id,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'CODIGO') or contains(translate(@name,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'CODIGO')]")
            if any((el.is_displayed() for el in pin_inputs)):
                return True
            dialogs = self.driver.find_elements(By.XPATH, "//div[contains(@role,'dialog')] | //div[contains(@class,'modal')]")
            for d in dialogs:
                text = (d.text or '').lower()
                if 'pin' in text or 'código' in text or 'codigo' in text or 'insira o pin' in text:
                    return True
            pin_buttons = self.driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'PIN') or contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CÓDIGO')]")
            if any((b.is_displayed() for b in pin_buttons)):
                return True
            return False
        except Exception:
            return False

    def _enter_pin_and_submit(self, pin_value):
        """Tenta localizar um campo de PIN e submeter o valor. Retorna True se submetido."""
        try:
            # localizar input password ou com placeholder 'pin' ou 'código'
            inputs = self.driver.find_elements(By.XPATH, "//input[@type='password'] | //input[contains(translate(@placeholder,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'PIN')] | //input[contains(translate(@placeholder,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'CÓDIGO')] | //input[contains(@aria-label,'pin') or contains(translate(@aria-label,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'PIN')]")
            for inp in inputs:
                try:
                    if inp.is_displayed():
                        inp.clear()
                        inp.send_keys(pin_value)
                        time.sleep(0.3)
                        try:
                            inp.send_keys(Keys.ENTER)
                        except Exception:
                            pass
                        # tentar clicar em botão confirm se existir
                        try:
                            btn = self.driver.find_element(By.XPATH, "//button[normalize-space()='Confirmar' or normalize-space()='OK' or normalize-space()='Enviar' or contains(normalize-space(.),'Entrar')]")
                            if btn.is_displayed() and btn.is_enabled():
                                btn.click()
                        except Exception:
                            pass
                        return True
                except Exception:
                    continue
            return False
        except Exception:
            return False

    def _find_card_button_by_title_global(self, title_fragment):
        try:
            hdrs = self.driver.find_elements(By.XPATH, f"//h6[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{title_fragment.lower()}')]")
            for h in hdrs:
                try:
                    card = h.find_element(By.XPATH, "ancestor::div[contains(@class,'MuiCard-root')]")
                    # evitar locked
                    try:
                        lock = card.find_elements(By.XPATH, ".//svg[@data-testid='LockIcon']")
                        if lock and any((l.is_displayed() for l in lock)):
                            continue
                    except Exception:
                        pass
                    try:
                        btn = card.find_element(By.XPATH, ".//button[normalize-space()='Acessar' or contains(normalize-space(.),'Acessar')]")
                        if btn.is_displayed() and btn.is_enabled():
                            return btn
                    except Exception:
                        continue
                except Exception:
                    continue
        except Exception:
            return None
        return None

    def test_acessar_com_pin(self):
        print("\n" + "="*60)
        print("TESTE RF44: Cursos Recomendados (Acessar com PIN) — Grupo 2")
        print("="*60)
        try:
            print("\n[PASSO 1] LOGIN VIA FIREBASE")
            login(self.driver)
            save_screenshot(self.driver, self.test_name, "01_apos_login")

            print("\n[PASSO 2] VALIDAR LOGIN")
            verificar_login(self.driver, self.wait)
            print("✓ Login validado com sucesso")

            print("\n[PASSO 3] NAVEGAR PARA HOME")
            time.sleep(1)
            self.driver.get(url_base)
            time.sleep(2)
            save_screenshot(self.driver, self.test_name, "02_home_page")

            try:
                self.wait.until(EC.url_to_be(url_base))
            except TimeoutException:
                pass

            print("\n[PASSO 4] LOCALIZAR CARD 'GRUPO 2'")
            secao = self._encontrar_secao_recomendados()
            if not secao:
                print("⚠ Seção recomendados não encontrada na HOME — farei busca global")
            # tentar localizar pelo helper global primeiro
            btn = self._find_card_button_by_title_global('grupo 2')
            if not btn and secao:
                # tentar dentro da seção
                btn = self._find_card_button_by_title_global('grupo 2')

            if not btn:
                self.fail("FALHA: Não foi encontrado o card 'Grupo 2' com botão 'Acessar'.")

            print("✓ Botão 'Acessar' do Grupo 2 encontrado — abrindo")
            save_screenshot(self.driver, self.test_name, "03_curso_grupo2_encontrado")

            # clicar e detectar modal
            try:
                btn.click()
            except Exception:
                self.driver.execute_script('arguments[0].click();', btn)

            time.sleep(1)
            save_screenshot(self.driver, self.test_name, "04_apos_clique_acessar")

            # detectar modal de PIN (aguardar alguns segundos por carregamento lento)
            pin_shown = False
            for _ in range(6):
                if self._detectar_modal_pin():
                    pin_shown = True
                    break
                time.sleep(0.5)

            if not pin_shown:
                self.fail("FALHA: Ao clicar em 'Acessar' não foi apresentado prompt de PIN quando esperado.")

            print("✓ Prompt de PIN detectado — inserindo PIN")
            save_screenshot(self.driver, self.test_name, "05_modal_pin_visivel")

            if not self._enter_pin_and_submit('grupo2'):
                self.fail("FALHA: Não foi possível localizar/ preencher o campo de PIN.")

            time.sleep(2)
            save_screenshot(self.driver, self.test_name, "06_apos_submit_pin")

            # validação: mudança de URL ou conteúdo do curso visível
            new_url = self.driver.current_url
            if new_url != url_base:
                print(f"✓ Acesso realizado - nova URL: {new_url}")
            else:
                possible_content = self.driver.find_elements(By.XPATH, "//h1|//h2|//iframe[contains(@src,'youtube')]|//*[contains(@class,'course') or contains(@class,'aula')]")
                visible = any((el.is_displayed() for el in possible_content))
                if visible:
                    print("✓ Acesso realizado - conteúdo do curso visível")
                else:
                    self.fail("FALHA: Não foi possível validar acesso ao curso após inserir PIN.")

            print("\n" + "="*60)
            print("TESTE RF44: Concluído com sucesso")
            print("="*60 + "\n")

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
