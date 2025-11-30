
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
sys.path.insert(0, dirname(abspath(__file__)))
from login_util import login, url_base, time_out
from screenshot_util import take_step_screenshot, reset_screenshot_counter

class TestReportarProblema(unittest.TestCase):

    def setUp(self):
        """Configura o driver Chrome e o WebDriverWait."""
        chrome_options = get_chrome_options()
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except (ValueError, Exception) as e:
            # Fallback para o caso de erro com o ChromeDriverManager
            print(f"Erro ao usar o ChromeDriverManager: {e}. Tentando caminho direto...")
            service = Service(executable_path=r"C:\Users\fre12\.wdm\drivers\chromedriver\win64\125.0.6422.141\chromedriver-win32\chromedriver.exe")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
        self.driver.implicitly_wait(5)
        self.wait = WebDriverWait(self.driver, time_out)
        reset_screenshot_counter(self.id())

    def _fechar_modal_se_presente(self):
        """Verifica e dispensa o modal de informação, se presente."""
        try:
            fechar_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Fechar']")))
            self.driver.execute_script("arguments[0].click();", fechar_button)
            print("✓ Botão 'Fechar' do modal clicado.")
        except TimeoutException:
            print("Nenhum modal com botão 'Fechar' encontrado. Prosseguindo...")


    def _encontrar_e_clicar_curso(self, course_title):
        """Encontra e clica em um curso nas abas 'Em Andamento' ou 'Concluídos'."""
        try:
            xpath = f"//h6[normalize-space()='{course_title}']/ancestor::div[contains(@class, 'MuiCard-root')]//button[normalize-space()='Começar']"
            comecar_button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            self.driver.execute_script("arguments[0].click();", comecar_button)
            print(f"✓ Clicou em 'Começar' para o curso '{course_title}'.")
            return
        except TimeoutException:
            pass
        try:
            print(f"Curso '{course_title}' não encontrado na aba inicial. Tentando a aba 'Em Andamento'...")
            em_andamento_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Em Andamento']")))
            em_andamento_tab.click()
            xpath = f"//h6[normalize-space()='{course_title}']/ancestor::div[contains(@class, 'MuiCard-root')]//button[normalize-space()='Continuar']"
            continuar_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].click();", continuar_button)
            print(f"✓ Clicou em 'Continuar' para o curso '{course_title}'.")
            return
        except TimeoutException:
            pass
        try:
            print(f"Curso '{course_title}' não encontrado na aba 'Em Andamento'. Tentando a aba 'Concluídos'...")
            concluidos_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Concluídos']")))
            concluidos_tab.click()
            xpath = f"//h6[normalize-space()='{course_title}']/ancestor::div[contains(@class, 'MuiCard-root')]//button[normalize-space()='Ver Curso']"
            ver_curso_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].click();", ver_curso_button)
            print(f"✓ Clicou em 'Ver Curso' para o curso '{course_title}'.")
            return
        except TimeoutException:
            self.fail(f"FALHA: Tempo esgotado. O curso '{course_title}' não foi encontrado em nenhuma das abas.")
        except Exception as e:
            self.fail(f"FALHA: Ocorreu um erro inesperado ao procurar o curso '{course_title}': {e}")


    def tearDown(self):
        """Finaliza o teste e fecha o driver."""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

    def test_01_reportar_problema_logado(self):
        """Verifica se o usuário LOGADO consegue reportar um problema em um vídeo."""
        print("\n--- EXECUTANDO: test_01_reportar_problema_logado ---")
        login(self.driver)
        take_step_screenshot(self.driver, self.id(), "apos_login")
        
        self.driver.get(f"{url_base}listcurso")
        try:
            self.wait.until(EC.url_contains("/listcurso"))
        except TimeoutException:
            self.fail("FALHA: Tempo esgotado ao esperar pela página de lista de cursos.")
        take_step_screenshot(self.driver, self.id(), "pagina_lista_cursos")

        course_title = "Curso Teste - Frederico Barcelos"
        self._encontrar_e_clicar_curso(course_title)

        try:
            self.wait.until(EC.url_contains("/classes?courseId="))
        except TimeoutException:
            self.fail("FALHA: Tempo esgotado ao esperar pela página de aulas do curso.")
        take_step_screenshot(self.driver, self.id(), "pagina_aulas_curso")
        
        self._fechar_modal_se_presente()
        
        print("Clicando no botão 'Reportar problema'...")
        try:
            report_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Reportar problema']")))
            self.driver.execute_script("arguments[0].click();", report_button)
        except TimeoutException:
            self.fail("FALHA: Botão 'Reportar problema' não foi encontrado ou não está clicável.")
        
        print("Aguardando o modal de reporte aparecer...")
        try:
            modal = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[aria-labelledby='report-dialog-title']")))
            self.assertTrue(modal.is_displayed(), "O modal de reporte não foi exibido.")
            take_step_screenshot(self.driver, self.id(), "modal_reporte_aberto", wait_for_element=(By.CSS_SELECTOR, "div[aria-labelledby='report-dialog-title']"))
            print("✓ Modal de reporte aberto.")
        except TimeoutException:
            self.fail("FALHA: Modal de reporte de problema não apareceu.")

        print("Preenchendo a descrição do problema...")
        try:
            description_field = self.wait.until(EC.visibility_of_element_located((By.ID, "report")))
            description_field.send_keys("O vídeo não está carregando corretamente.")
            take_step_screenshot(self.driver, self.id(), "descricao_preenchida")
            print("✓ Descrição preenchida.")
        except TimeoutException:
            self.fail("FALHA: Campo de descrição do problema não foi encontrado.")

        print("Clicando no botão 'Enviar Reporte'...")
        try:
            submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Enviar Reporte']")))
            self.driver.execute_script("arguments[0].click();", submit_button)
        except TimeoutException:
            self.fail("FALHA: Botão 'Enviar Reporte' não foi encontrado ou não está clicável.")

        print("Verificando a mensagem de sucesso ou erro...")
        
        # Prioriza a verificação de erro com espera explícita
        try:
            error_toast_locator = (By.XPATH, "//div[contains(@class, 'Toastify__toast--error')]")
            error_toast = self.wait.until(EC.visibility_of_element_located(error_toast_locator))
            error_text = error_toast.text
            take_step_screenshot(self.driver, self.id(), "reporte_com_erro", wait_for_element=error_toast_locator)
            self.fail(f"FALHA:Uma mensagem de erro foi exibida, ao submeter o report: '{error_text}'")
        
        except TimeoutException:
            # Se o toast de erro não apareceu, procuramos o de sucesso
            print("Nenhum toast de erro encontrado. Verificando a mensagem de sucesso...")
            try:
                success_toast_locator = (By.XPATH, "//div[contains(@class, 'Toastify__toast--success')]")
                self.wait.until(EC.visibility_of_element_located(success_toast_locator))
                take_step_screenshot(self.driver, self.id(), "reporte_enviado_sucesso", wait_for_element=success_toast_locator)
                print("✓ Reporte enviado com sucesso!")
            except TimeoutException:
                self.fail("FALHA: Nenhuma mensagem de feedback (sucesso ou erro) foi exibida após o envio do reporte.")

        print("--- TESTE test_01_reportar_problema_logado CONCLUÍDO ---")

if __name__ == "__main__":
    unittest.main()
