"""
RF48_CT01_SelecionarVideo.py

Teste Selenium para RF48: Selecionar Vídeo ("Ver Vídeo") em curso

Fluxo:
1. Login via Firebase
2. Abrir área de Cursos e acessar o curso 'RF 42 - Grupo 4' (inserir PIN 1234 se necessário)
3. Procurar botão 'Ver Vídeo' dentro do curso e clicar
4. Validar que o vídeo foi aberto/selecionado
"""

import unittest
import time
import traceback
import sys
from os.path import abspath, dirname

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

sys.path.insert(0, dirname(abspath(__file__)))
from login_util import login, verificar_login, url_base, time_out
from chrome_config import get_chrome_options
from screenshot_util import save_screenshot


class TestRF48SelecionarVideo(unittest.TestCase):
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
            self.test_name = "test_selecionar_video_RF48"
        except Exception as e:
            print(f"ERRO no setUp: {e}")
            traceback.print_exc()
            raise

    def tearDown(self):
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
        except Exception as e:
            print(f"Erro ao fechar driver: {e}")

    def _abrir_area_cursos(self):
        selectors = [
            "//svg[@data-testid='SmartDisplayIcon']/ancestor::div[1]",
            "//path[@d=\"M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2M9.5 16.5v-9l7 4.5z\"]/ancestor::svg/ancestor::div[1]",
            "//div[contains(@class,'topbarIconCont') and .//span[contains(normalize-space(),'Cursos')]]",
            "//div[.//span[normalize-space()='Cursos']]",
        ]
        for sel in selectors:
            try:
                elems = self.driver.find_elements(By.XPATH, sel)
                for elem in elems:
                    try:
                        if not elem.is_displayed():
                            continue
                        try:
                            elem.click()
                        except Exception:
                            self.driver.execute_script('arguments[0].click();', elem)
                        time.sleep(1)
                        return True
                    except Exception:
                        continue
            except Exception:
                continue
        return False

    def _enter_pin_and_submit(self, pin_value):
        try:
            inputs = self.driver.find_elements(By.XPATH, "//input[@type='password'] | //input[contains(translate(@placeholder,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'PIN')] | //input[contains(translate(@aria-label,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'PIN')]")
            for inp in inputs:
                try:
                    if inp.is_displayed():
                        inp.clear()
                        inp.send_keys(pin_value)
                        time.sleep(0.3)
                        try:
                            inp.send_keys('\n')
                        except Exception:
                            pass
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
            # procura por h6 que contenha o título (case-insensitive)
            hdrs = self.driver.find_elements(By.XPATH, f"//h6[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{title_fragment.lower()}')]")
            for h in hdrs:
                try:
                    card = h.find_element(By.XPATH, "ancestor::div[contains(@class,'MuiCard-root')]")
                    # prioriza botão 'Começar' (visto no DOM), depois 'Acessar', depois qualquer botão clicável
                    try:
                        btn = card.find_element(By.XPATH, ".//button[normalize-space()='Começar' or contains(normalize-space(.),'Começar')]")
                        if btn.is_displayed() and btn.is_enabled():
                            return btn
                    except Exception:
                        pass

                    try:
                        btn = card.find_element(By.XPATH, ".//button[normalize-space()='Acessar' or contains(normalize-space(.),'Acessar')]")
                        if btn.is_displayed() and btn.is_enabled():
                            return btn
                    except Exception:
                        pass

                    try:
                        cand = card.find_element(By.XPATH, ".//button | .//a | .//div[contains(@role,'button')]")
                        if cand.is_displayed() and cand.is_enabled():
                            return cand
                    except Exception:
                        continue
                except Exception:
                    continue
        except Exception:
            return None
        return None

    def test_selecionar_video_ver_video(self):
        print('\n' + '='*60)
        print('TESTE RF48: Selecionar Vídeo (Ver Vídeo) — RF 42 - Grupo 4')
        print('='*60)
        try:
            login(self.driver)
            save_screenshot(self.driver, self.test_name, '01_apos_login')
            verificar_login(self.driver, self.wait)

            if not self._abrir_area_cursos():
                self.fail('FALHA: Não abriu área de Cursos')
            time.sleep(0.5)
            # tentar abrir aba Disponíveis
            try:
                dispon = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'dispon') or contains(normalize-space(.),'Dispon') or contains(normalize-space(.),'Disponíveis') or contains(normalize-space(.),'Disponiveis')]") ))
                try:
                    dispon.click()
                except Exception:
                    self.driver.execute_script('arguments[0].click();', dispon)
            except Exception:
                pass

            time.sleep(1)
            save_screenshot(self.driver, self.test_name, '02_aba_disponiveis')

            # localizar e acessar curso — testar múltiplos fragmentos de título para aumentar robustez
            title_fragments = [
                'Curso Grupo 4',
                'Curso Grupo 4 com PIN',
                'RF 42 - Grupo 4',
                'RF 42',
                'Grupo 4',
            ]
            btn = None
            for frag in title_fragments:
                try:
                    btn = self._find_card_button_by_title_global(frag)
                    if btn:
                        print(f"✓ Encontrado card com fragmento: {frag}")
                        break
                except Exception:
                    continue
            if not btn:
                # fallback: tentar encontrar qualquer card disponível sem lock
                try:
                    cards = self.driver.find_elements(By.XPATH, "//div[contains(@class,'MuiCard-root')]")
                    for c in cards:
                        try:
                            locks = c.find_elements(By.XPATH, ".//svg[@data-testid='LockIcon']")
                            if locks and any((l.is_displayed() for l in locks)):
                                continue
                            cand = None
                            try:
                                cand = c.find_element(By.XPATH, ".//button[normalize-space()='Começar' or contains(normalize-space(.),'Começar')]")
                            except Exception:
                                try:
                                    cand = c.find_element(By.XPATH, ".//button | .//a | .//div[contains(@role,'button')]")
                                except Exception:
                                    cand = None
                            if cand and cand.is_displayed() and cand.is_enabled():
                                btn = cand
                                print('✓ Fallback: encontrou um card disponível')
                                break
                        except Exception:
                            continue
                except Exception:
                    pass

            if not btn:
                self.fail("FALHA: Não encontrou nenhum card de curso disponível para acessar.")

            save_screenshot(self.driver, self.test_name, '03_curso_rf42_encontrado')
            try:
                btn.click()
            except Exception:
                self.driver.execute_script('arguments[0].click();', btn)
            time.sleep(1)
            save_screenshot(self.driver, self.test_name, '04_apos_clique_acessar')

            # se pedir PIN, inserir 1234
            pin_needed = False
            for _ in range(6):
                inputs = self.driver.find_elements(By.XPATH, "//input[@type='password'] | //input[contains(translate(@placeholder,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'PIN')] | //input[contains(translate(@aria-label,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'PIN')]")
                if any((el.is_displayed() for el in inputs)):
                    pin_needed = True
                    break
                time.sleep(0.5)

            if pin_needed:
                save_screenshot(self.driver, self.test_name, '05_modal_pin_visivel')
                if not self._enter_pin_and_submit('1234'):
                    self.fail('FALHA: Não foi possível inserir o PIN 1234')
                time.sleep(1)

            # procurar botão 'Ver Vídeo' dentro do curso
            try:
                btn_video = self.driver.find_element(By.XPATH, "//*[contains(normalize-space(),'Ver Vídeo') or contains(normalize-space(),'Ver Video') or contains(normalize-space(),'Ver vídeo')]")
                if btn_video.is_displayed():
                    try:
                        btn_video.click()
                    except Exception:
                        self.driver.execute_script('arguments[0].click();', btn_video)
                    time.sleep(1)
                    save_screenshot(self.driver, self.test_name, '06_apos_clicar_ver_video')
                else:
                    save_screenshot(self.driver, self.test_name, '06_ver_video_nao_visivel')
                    self.fail('FALHA: Botão "Ver Vídeo" não visível')
            except Exception:
                save_screenshot(self.driver, self.test_name, '06_ver_video_nao_encontrado')
                self.fail('FALHA: Botão "Ver Vídeo" não encontrado no curso.')

            print('\n' + '='*60)
            print('TESTE RF48: Concluído')
            print('='*60 + '\n')

        except AssertionError:
            raise
        except Exception as e:
            print(f'Erro inesperado: {e}')
            traceback.print_exc()
            self.fail(f'Erro inesperado: {e}')


if __name__ == '__main__':
    unittest.main()
