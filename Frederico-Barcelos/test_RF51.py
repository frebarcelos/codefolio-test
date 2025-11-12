import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from chrome_config import get_chrome_options
from webdriver_manager.chrome import ChromeDriverManager
import time
import traceback
import sys
from os.path import abspath, dirname

# Adiciona o diretório pai ao path para conseguir importar os utils
sys.path.insert(0, dirname(abspath(__file__)))
from login_util import login, verificar_login

class TestExtraMaterials(unittest.TestCase):

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
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            self.driver.execute_script("arguments[0].click();", comecar_button)
            return
        except:
            pass

        try:
            # Se não encontrar, clica na aba "Em Andamento" e tenta novamente
            print("Curso não encontrado na aba atual. Tentando a aba 'Em Andamento'...")
            em_andamento_tab = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Em Andamento']"))
            )
            em_andamento_tab.click()
            xpath = f"//h6[normalize-space()='{course_title}']/ancestor::div[contains(@class, 'MuiCard-root')]//button[normalize-space()='Continuar']"
            comecar_button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            self.driver.execute_script("arguments[0].click();", comecar_button)
            return
        except:
            pass

        try:
            # Se não encontrar, clica na aba "Concluídos" e tenta novamente
            print("Curso não encontrado na aba 'Em Andamento'. Tentando a aba 'Concluídos'...")
            concluidos_tab = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Concluídos']"))
            )
            concluidos_tab.click()
            xpath = f"//h6[normalize-space()='{course_title}']/ancestor::div[contains(@class, 'MuiCard-root')]//button[normalize-space()='Ver Curso']"
            comecar_button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
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

    def _verificar_aba_material_extra(self):
        """
        Clica na aba 'Materiais Extras' e verifica se o conteúdo correto é carregado.
        """
        try:
            print("Procurando e clicando na aba 'Materiais Extras'...")
            materiais_tab = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[normalize-space()='Materiais Extras']")
                )
            )
            materiais_tab.click()
            print("✓ Aba 'Materiais Extras' clicada.")

            print("Verificando se o conteúdo do material extra foi carregado...")
            material_extra_header = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h6[normalize-space()='Teste material extra']")
                )
            )
            self.assertTrue(material_extra_header.is_displayed(), "O cabeçalho do material extra não está visível.")
            print("✓ Conteúdo do material extra verificado com sucesso.")

        except Exception as e:
            traceback.print_exc()
            self.fail(f"Falha ao verificar a aba de materiais extras: {e}")

    def test_01_ver_material_extra_logado(self):
        """Verifica se o usuário LOGADO consegue ver os materiais extras."""
        print("\n--- EXECUTANDO: test_01_ver_material_extra_logado ---")
        login(self.driver)
        self._navegar_para_pagina_de_video_logado()
        self._verificar_aba_material_extra()

    def test_02_ver_material_extra_deslogado(self):
        """
        Verifica se, para um usuário DESLOGADO, ao clicar em 'Materiais Extras',
        a mensagem para fazer login é exibida.
        """
        print("\n--- EXECUTANDO: test_02_ver_material_extra_deslogado ---")
        self._navegar_para_pagina_de_video_deslogado()
        
        try:
            print("Procurando e clicando na aba 'Materiais Extras'...")
            materiais_tab = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[normalize-space()='Materiais Extras']")
                )
            )
            materiais_tab.click()
            print("✓ Aba 'Materiais Extras' clicada.")

            print("Verificando se a mensagem 'Você deve fazer login...' é exibida...")
            login_message = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//p[normalize-space()='Você deve fazer login para ver os materiais extras deste curso']")
                )
            )
            self.assertTrue(login_message.is_displayed(), "A mensagem para fazer login não foi encontrada para o usuário deslogado.")
            print("✓ Mensagem para fazer login verificada com sucesso.")

        except Exception as e:
            traceback.print_exc()
            self.fail(f"Falha ao verificar a mensagem de login para materiais extras: {e}")

if __name__ == "__main__":
    unittest.main()
