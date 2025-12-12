"""
RF45_CT01_NavegarEntreCursos.py

Teste Selenium para RF45: Navegar entre abas de Cursos e salvar screenshots.

Comportamento:
- Faz login via `login_util.login()` (injeção no localStorage)
- Abre o menu `Cursos` (usa SVG `data-testid='SmartDisplayIcon'` como seletor primário)
- Clica nas 3 abas: 'Disponíveis', 'Em Andamento', 'Concluídos' e salva screenshot de cada uma

Este teste é focado em navegar nas abas e gerar evidências visuais.
"""

import unittest
import time
import traceback
import sys
from os.path import abspath, dirname

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

sys.path.insert(0, dirname(abspath(__file__)))
from login_util import login, verificar_login, url_base, time_out
from chrome_config import get_chrome_options
from screenshot_util import save_screenshot


class TestRF45NavegarEntreCursos(unittest.TestCase):
    def setUp(self):
        chrome_options = get_chrome_options()
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(5)
        try:
            self.driver.maximize_window()
        except Exception:
            pass
        self.wait = WebDriverWait(self.driver, time_out)
        self.test_name = "test_navegar_entre_cursos_RF45"

    def tearDown(self):
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
        except Exception:
            pass

    def _abrir_area_cursos(self):
        # Seletor primário: SVG com data-testid
        xpaths = [
            "//svg[@data-testid='SmartDisplayIcon']/ancestor::div[1]",
            "//div[contains(@class,'topbarIconCont') and .//span[contains(normalize-space(),'Cursos')]]",
            "//div[.//span[normalize-space()='Cursos']]",
        ]
        for xp in xpaths:
            try:
                elems = self.driver.find_elements(By.XPATH, xp)
                for e in elems:
                    if e.is_displayed():
                        try:
                            e.click()
                        except Exception:
                            self.driver.execute_script('arguments[0].click();', e)
                        time.sleep(1)
                        return True
            except Exception:
                continue
        return False

    def _click_tab_and_shot(self, tab_texts, step_name):
        # tab_texts: list of possible text variants to try
        for txt in tab_texts:
            try:
                btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[normalize-space()='{txt}']")))
                try:
                    btn.click()
                except Exception:
                    self.driver.execute_script('arguments[0].click();', btn)
                time.sleep(1)
                save_screenshot(self.driver, self.test_name, step_name)
                return True
            except Exception:
                continue
        return False

    def test_navegar_entre_abas_cursos(self):
        print('\n' + '=' * 60)
        print('TESTE RF45: Navegar entre Cursos')
        print('=' * 60)
        try:
            login(self.driver)
            save_screenshot(self.driver, self.test_name, '01_apos_login')
            verificar_login(self.driver, self.wait)

            if not self._abrir_area_cursos():
                self.fail('Não conseguiu abrir área de Cursos')
            save_screenshot(self.driver, self.test_name, '02_area_cursos_aberta')

            # Disponíveis
            self._click_tab_and_shot(['Disponíveis', 'Disponiveis', 'Disponíveis '], '03_disponiveis')
            # Em Andamento
            self._click_tab_and_shot(['Em Andamento', 'Em andamento'], '04_em_andamento')
            # Concluídos
            self._click_tab_and_shot(['Concluídos', 'Concluidos', 'Concluídos '], '05_concluidos')

        except Exception as e:
            traceback.print_exc()
            self.fail(f'Erro inesperado: {e}')


if __name__ == '__main__':
    unittest.main()

"""
RF45_CT01_NavegarEntreCursos.py

Teste Selenium para RF45: Navegar entre Cursos (Disponíveis / Em Andamento / Concluídos)

Fluxo:
*** End Patch
    unittest.main()

"""
