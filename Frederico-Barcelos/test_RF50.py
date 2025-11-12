
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from chrome_config import get_chrome_options
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(abspath(__file__)))
from login_util import login, verificar_login

class TestNavigateVideos(unittest.TestCase):

    def setUp(self):
        self.URL_BASE = "https://testes.codefolio.com.br/"
        self.TIMEOUT = 20

        chrome_options = get_chrome_options()

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(5)
        self.wait = WebDriverWait(self.driver, self.TIMEOUT)

    def _encontrar_e_clicar_curso(self, course_title):
        """Encontra e clica em um curso nas abas 'Em Andamento' ou 'Concluídos'."""
        try:
            # Tenta encontrar o curso na aba atual
            xpath = f"//h6[normalize-space()='teste123']/ancestor::div[contains(@class, 'MuiCard-root')]//button[normalize-space()='Começar']"
            comecar_button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable(
                    (By.XPATH, xpath)
                )
            )
            self.driver.execute_script("arguments[0].click();", comecar_button)
            return
        except:
            pass

        try:
            # Se não encontrar, clica na aba "Em Andamento" e tenta novamente
            print("Curso não encontrado na aba atual. Tentando a aba 'Em Andamento'...")
            em_andamento_tab = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[normalize-space()='Em Andamento']")
                )
            )
            em_andamento_tab.click()
            xpath = f"//h6[normalize-space()='{course_title}']/ancestor::div[contains(@class, 'MuiCard-root')]//button[normalize-space()='Continuar']"
            comecar_button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable(
                    (By.XPATH, xpath)
                )
            )
            self.driver.execute_script("arguments[0].click();", comecar_button)
            return
        except:
            pass

        try:
            # Se não encontrar, clica na aba "Concluídos" e tenta novamente
            print("Curso não encontrado na aba 'Em Andamento'. Tentando a aba 'Concluídos'...")
            concluidos_tab = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[normalize-space()='Concluídos']")
                )
            )
            concluidos_tab.click()
            xpath = f"//h6[normalize-space()='{course_title}']/ancestor::div[contains(@class, 'MuiCard-root')]//button[normalize-space()='Ver Curso']"
            comecar_button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable(
                    (By.XPATH, xpath)
                )
            )
            self.driver.execute_script("arguments[0].click();", comecar_button)
            return
        except:
            self.fail(f"Curso '{course_title}' não encontrado em nenhuma das abas.")

    def _navegar_para_pagina_de_video_logado(self):
        """Navega para a página de vídeo como um usuário logado."""
        verificar_login(self.driver, self.wait)
        print("Navegando para a lista de cursos (logado)...")
        self.driver.get(f"{self.URL_BASE}listcurso")
        self.wait.until(EC.url_contains("/listcurso"))
        print("✓ Página de lista de cursos carregada")
        print("Clicando em um botão 'começar' para o curso específico...")
        course_title = "Curso Teste - Frederico Barcelos"
        self._encontrar_e_clicar_curso(course_title)
        print("Verificando se estamos na página de aulas...")
        self.wait.until(EC.url_contains("/classes?courseId="))
        print("✓ Página de aulas carregada")

    def _navegar_para_pagina_de_video_deslogado(self):
        """Navega para a página de vídeo como um usuário deslogado."""
        print("Navegando diretamente para a página do curso (deslogado)...")
        public_course_url = f"{self.URL_BASE}classes?courseId=-OdiThGNeYgeZtQJbz1a"
        self.driver.get(public_course_url)
        print("Verificando se estamos na página de aulas...")
        self.wait.until(EC.url_contains("/classes?courseId="))
        print("✓ Página de aulas carregada")

    def tearDown(self):
        """Finaliza o teste, salva screenshot e fecha o driver."""
        if hasattr(self, 'driver') and self.driver:
            try:
                self.driver.save_screenshot(f"resultado_{self.id()}.png")
                print(f"Screenshot salvo como 'resultado_{self.id()}.png'")
            except:
                pass
            self.driver.quit()

    def _realizar_teste_navegacao(self):
        """Lógica de teste de navegação reutilizável."""
        print("Aguardando 5 segundos para a renderização completa da página...")
        time.sleep(5)
        print("Executando script para encontrar e clicar no botão 'próximo' via Shadow DOM...")
        js_script_click_next = """
        const selector = '[data-testid="ArrowForwardIcon"]';
        function findInShadowDom(selector) {
            function find(root) {
                const found = root.querySelector(selector);
                if (found) return found;
                const allElements = root.querySelectorAll('*');
                for (const element of allElements) {
                    if (element.shadowRoot) {
                        const foundInShadow = find(element.shadowRoot);
                        if (foundInShadow) return foundInShadow;
                    }
                }
                return null;
            }
            return find(document);
        }
        const icon = findInShadowDom(selector);
        if (icon) {
            const button = icon.closest('button');
            if (button && !button.disabled) {
                button.click();
                return true;
            }
        }
        return false;
        """
        clicked = self.driver.execute_script(js_script_click_next)
        self.assertTrue(clicked, "Não foi possível encontrar ou clicar no botão 'próximo' via script.")
        print("✓ Clicou no botão de próximo vídeo.")
        time.sleep(2)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        print("✓ Iframe do novo vídeo encontrado após a navegação.")
        print("✓ Teste de navegação entre vídeos simplificado concluído com sucesso!")
        if hasattr(self, 'driver') and self.driver:
            try:
                self.driver.save_screenshot("resultado_teste.png")
                print("Screenshot salvo como 'resultado_teste.png'")
            except:
                pass

    def test_03_navegacao_logado(self):
        """Verifica a navegação entre vídeos para um usuário LOGADO."""
        print("\n--- EXECUTANDO: test_03_navegacao_logado ---")
        login(self.driver)
        self._navegar_para_pagina_de_video_logado()
        self._realizar_teste_navegacao()

    def test_04_navegacao_deslogado(self):
        """Verifica a navegação entre vídeos para um usuário DESLOGADO."""
        print("\n--- EXECUTANDO: test_04_navegacao_deslogado ---")
        self.driver.get(self.URL_BASE) # Start fresh
        self._navegar_para_pagina_de_video_deslogado()
        self._realizar_teste_navegacao()

if __name__ == "__main__":
    unittest.main()
