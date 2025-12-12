import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from chrome_config import get_chrome_options
from webdriver_manager.chrome import ChromeDriverManager
import sys
from os.path import abspath, dirname

# Adiciona o diretório pai ao path para conseguir importar os utils
sys.path.insert(0, dirname(abspath(__file__)))
from login_util import login, url_base,time_out
from screenshot_util import take_step_screenshot, reset_screenshot_counter

class TestAcessarAvaliacoes(unittest.TestCase):

    def setUp(self):
        chrome_options = get_chrome_options()
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(5)
        self.wait = WebDriverWait(self.driver, time_out)
        reset_screenshot_counter(self.id())

    def tearDown(self):
        """Finaliza o teste e fecha o driver."""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

    def test_01_acessar_avaliacoes_logado(self):
        """
        Testa o acesso do aluno às avaliações dos cursos que ele realizou (LOGADO).
        """
        print("\n--- EXECUTANDO: test_01_acessar_avaliacoes_logado ---")
        
        # 1. Login
        login(self.driver)
        take_step_screenshot(self.driver, self.id(), "01_apos_login")

        # 2. Clicar em "Avaliações"
        try:
            print("Clicando no ícone de 'Avaliações'...")
            avaliacoes_link = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[@href='/minhas-avaliacoes']")
                )
            )
            self.driver.execute_script("arguments[0].click();", avaliacoes_link)
            self.wait.until(EC.url_contains("/minhas-avaliacoes"))
            take_step_screenshot(self.driver, self.id(), "02_pagina_avaliacoes")
            print("✓ Página de 'Minhas Avaliações' carregada.")
        except TimeoutException:
            self.fail("FALHA: Não foi possível encontrar ou clicar no link 'Avaliações' ou a página não carregou.")

        # 3. Acessar o curso "Curso Teste - Frederico Barcelos"
        try:
            print("Procurando pelo curso 'Curso Teste - Frederico Barcelos'...")
            course_card_xpath = "//h5[normalize-space()='Curso Teste - Frederico Barcelos']"
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, course_card_xpath))
            )
            take_step_screenshot(self.driver, self.id(), "03_curso_encontrado")
            print("✓ Curso encontrado.")
        except TimeoutException:
            self.fail("FALHA: Não foi possível encontrar o card do curso 'Curso Teste - Frederico Barcelos'.")

        # 4. Expandir as avaliações do curso
        try:
            print("Clicando para expandir as avaliações do curso...")
            expand_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//h5[normalize-space()='Curso Teste - Frederico Barcelos']/ancestor::div[contains(@class, 'MuiCard-root')]//button[contains(@class, 'MuiAccordionSummary-root')]")
                )
            )
            self.driver.execute_script("arguments[0].click();", expand_button)
            
            # Aguarda a animação de expansão e a visibilidade do conteúdo
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'MuiCollapse-entered')]//p[normalize-space()='Teste 1']")
                )
            )
            take_step_screenshot(self.driver, self.id(), "04_avaliacoes_expandidas")
            print("✓ Avaliações expandidas e conteúdo visível.")

        except TimeoutException:
            self.fail("FALHA: Não foi possível expandir as avaliações do curso ou o conteúdo não ficou visível a tempo.")
        except Exception as e:
            self.fail(f"FALHA: Ocorreu um erro inesperado ao expandir as avaliações: {e}")

    def test_02_acessar_avaliacoes_deslogado(self):
        """
        Testa que ao clicar em 'Avaliações' sem estar logado, o usuário é redirecionado para a página de login.
        """
        print("\n--- EXECUTANDO: test_02_acessar_avaliacoes_deslogado ---")
        
        # 1. Navegar para a página inicial
        self.driver.get(url_base)
        take_step_screenshot(self.driver, self.id(), "01_pagina_inicial_deslogado")

        # 2. Clicar em "Avaliações"
        try:
            print("Clicando no ícone de 'Avaliações' (deslogado)...")
            avaliacoes_link = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[@href='/minhas-avaliacoes']")
                )
            )
            self.driver.execute_script("arguments[0].click();", avaliacoes_link)
            
            # 3. Verificar redirecionamento para a página de login
            self.wait.until(EC.url_to_be(f"{url_base}login"))
            take_step_screenshot(self.driver, self.id(), "02_redirecionado_para_login")
            print("✓ Redirecionamento para a página de login verificado com sucesso.")
            
        except TimeoutException:
            self.fail("FALHA: Não foi possível clicar em 'Avaliações' ou o redirecionamento para a página de login não ocorreu como esperado.")
        except Exception as e:
            self.fail(f"FALHA: Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    unittest.main()
