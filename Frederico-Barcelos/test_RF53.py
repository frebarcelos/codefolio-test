
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from chrome_config import get_chrome_options
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(abspath(__file__)))
from login_util import verificar_login, login, url_base, time_out
from screenshot_util import take_step_screenshot, reset_screenshot_counter

class TestQuizBloqueado(unittest.TestCase):

    def setUp(self):
        chrome_options = get_chrome_options()
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(5)
        self.wait = WebDriverWait(self.driver, time_out)
        reset_screenshot_counter(self.id())

    def _encontrar_e_clicar_curso(self, course_title):
        """Encontra e clica em um curso nas abas 'Em Andamento' ou 'Concluídos'."""
        try:
            xpath = f"//h6[normalize-space()='{course_title}']/ancestor::div[contains(@class, 'MuiCard-root')]//button[normalize-space()='Começar']"
            comecar_button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            self.driver.execute_script("arguments[0].click();", comecar_button)
            return
        except: pass
        try:
            print(f"Curso '{course_title}' não encontrado na aba atual. Tentando a aba 'Em Andamento'...")
            em_andamento_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Em Andamento']")))
            em_andamento_tab.click()
            xpath = f"//h6[normalize-space()='{course_title}']/ancestor::div[contains(@class, 'MuiCard-root')]//button[normalize-space()='Continuar']"
            comecar_button = WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].click();", comecar_button)
            return
        except: pass
        try:
            print(f"Curso '{course_title}' não encontrado na aba 'Em Andamento'. Tentando a aba 'Concluídos'...")
            concluidos_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Concluídos']")))
            concluidos_tab.click()
            xpath = f"//h6[normalize-space()='{course_title}']/ancestor::div[contains(@class, 'MuiCard-root')]//button[normalize-space()='Ver Curso']"
            comecar_button = WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].click();", comecar_button)
            return
        except TimeoutException:
            self.fail(f"FALHA: Tempo esgotado. O curso '{course_title}' não foi encontrado em nenhuma das abas.")
        except Exception as e:
            self.fail(f"FALHA: Ocorreu um erro inesperado ao procurar o curso '{course_title}': {e}")

    def tearDown(self):
        """Finaliza o teste e fecha o driver."""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

    def test_01_quiz_bloqueado_logado(self):
        """Verifica se o usuário LOGADO vê a mensagem de quiz bloqueado."""
        print("\n--- EXECUTANDO: test_01_quiz_bloqueado_logado ---")
        login(self.driver)
        take_step_screenshot(self.driver, self.id(), "apos_login")
        print("Navegando para a lista de cursos (logado)...")
        self.driver.get(f"{url_base}listcurso")
        try:
            self.wait.until(EC.url_contains("/listcurso"))
        except TimeoutException:
            self.fail("FALHA: Tempo esgotado ao esperar pela página de lista de cursos.")
        take_step_screenshot(self.driver, self.id(), "pagina_lista_cursos")
        print("✓ Página de lista de cursos carregada")

        course_title = "Curso Quiz - Frederico Barcelos"
        print(f"Clicando no curso '{course_title}'...")
        self._encontrar_e_clicar_curso(course_title)

        print("Verificando se estamos na página de aulas do curso...")
        try:
            self.wait.until(EC.url_contains("/classes?courseId="))
        except TimeoutException:
            self.fail("FALHA: Tempo esgotado ao esperar pela página de aulas do curso.")
        take_step_screenshot(self.driver, self.id(), "pagina_aulas_curso_quiz")
        print("✓ Página de aulas do curso carregada")

        print("Procurando e clicando no botão 'Quiz Bloqueado'...")
        try:
            quiz_bloqueado_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[./span/descendant::*[name()='svg'][@data-testid='LockIcon'] and normalize-space(.)='Quiz Bloqueado']")))
            self.driver.execute_script("arguments[0].click();", quiz_bloqueado_button)
            print("✓ Clicou no botão 'Quiz Bloqueado'.")
        except TimeoutException:
            self.fail("FALHA: Tempo esgotado. O botão 'Quiz Bloqueado' não foi encontrado ou não está clicável.")

        print("Verificando a aparição do toast de aviso...")
        toast_text = 'Você precisa assistir o vídeo "Senhor dos aneis orquestra" para liberar o quiz!'
        toast_xpath = f"//div[contains(@class, 'Toastify__toast--warning') and contains(., '{toast_text}')]"
        toast_locator = (By.XPATH, toast_xpath)

        print("Aguardando toast de aviso e tirando screenshot...")
        try:
            # A função de screenshot já espera o elemento.
            take_step_screenshot(self.driver, self.id(), "toast_aviso_presente", wait_for_element=toast_locator)
            toast_element = self.driver.find_element(*toast_locator) 
            self.assertTrue(toast_element.is_displayed(), "FALHA: O toast de aviso apareceu no DOM, mas não ficou visível.")
            print("✓ Toast de aviso apareceu e screenshot foi salvo.")
        except TimeoutException:
            self.fail("FALHA: Tempo esgotado ao esperar pelo aparecimento do toast de aviso.")

        print("Aguardando o desaparecimento do toast...")
        try:
            desapareceu = self.wait.until(EC.invisibility_of_element_located(toast_locator))
            self.assertTrue(desapareceu, "FALHA: O toast de aviso não desapareceu no tempo esperado.")
            print("✓ Toast de aviso desapareceu.")
        except TimeoutException:
            self.fail("FALHA: Tempo esgotado ao esperar pelo desaparecimento do toast de aviso.")
        
        print("--- TESTE test_01_quiz_bloqueado_logado CONCLUÍDO ---")


if __name__ == "__main__":
    unittest.main()
