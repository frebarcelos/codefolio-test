
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
import traceback
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(abspath(__file__)))
from login_util import verificar_login, login, url_base, time_out,id_deslogado
from screenshot_util import take_step_screenshot, reset_screenshot_counter

class TestWatchVideo(unittest.TestCase):

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
            # Tenta encontrar o curso na aba atual
            xpath = f"//h6[normalize-space()='{course_title}']/ancestor::div[contains(@class, 'MuiCard-root')]//button[normalize-space()='Começar']"
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
        except TimeoutException:
            self.fail(f"FALHA: Tempo esgotado. O curso '{course_title}' não foi encontrado em nenhuma das abas (Inicial, Em Andamento, Concluídos).")
        except Exception as e:
            self.fail(f"FALHA: Ocorreu um erro inesperado ao procurar o curso '{course_title}': {e}")

    def _navegar_para_pagina_de_video_logado(self):
        """Navega para a página de vídeo como um usuário logado."""
        verificar_login(self.driver, self.wait)
        print("Navegando para a lista de cursos (logado)...")
        self.driver.get(f"{url_base}listcurso")
        try:
            self.wait.until(EC.url_contains("/listcurso"))
        except TimeoutException:
            self.fail("FALHA: Tempo esgotado ao esperar pela página de lista de cursos (URL não contém '/listcurso').")
        take_step_screenshot(self.driver, self.id(), "pagina_lista_cursos")
        print("✓ Página de lista de cursos carregada")
        print("Clicando em um botão 'começar' para o curso específico...")
        course_title = "Curso Teste - Frederico Barcelos"
        self._encontrar_e_clicar_curso(course_title)
        print("Verificando se estamos na página de aulas...")
        try:
            self.wait.until(EC.url_contains("/classes?courseId="))
        except TimeoutException:
            self.fail("FALHA: Tempo esgotado ao esperar pela página de aulas do curso (URL não contém '/classes?courseId=').")
        take_step_screenshot(self.driver, self.id(), "pagina_aulas_curso")
        print("✓ Página de aulas carregada")

    def _navegar_para_pagina_de_video_deslogado(self):
        """Navega para a página de vídeo como um usuário deslogado."""
        print("Navegando diretamente para a página do curso (deslogado)...")
        public_course_url = f"{url_base}classes?courseId={id_deslogado}"
        self.driver.get(public_course_url)
        print("Verificando se estamos na página de aulas...")
        try:
            self.wait.until(EC.url_contains("/classes?courseId="))
        except TimeoutException:
            self.fail("FALHA: Tempo esgotado ao esperar pela página de aulas do curso (URL não contém '/classes?courseId=').")
        take_step_screenshot(self.driver, self.id(), "pagina_aulas_deslogado")
        print("✓ Página de aulas carregada")

    def tearDown(self):
        """Finaliza o teste, salva screenshot e fecha o driver."""
        if hasattr(self, 'driver') and self.driver:
            try:
                pass # Screenshot removido, agora gerenciado por take_step_screenshot
            except:
                pass
            self.driver.quit()

    def test_01_assistir_video_logado(self):
        """Verifica se o usuário LOGADO consegue assistir a um vídeo de um curso."""
        print("\n--- EXECUTANDO: test_01_assistir_video_logado ---")
        login(self.driver)
        take_step_screenshot(self.driver, self.id(), "apos_login")
        self._navegar_para_pagina_de_video_logado()
        try:
            print("Verificando e dispensando o modal de informação, se presente...")
            try:
                fechar_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Fechar']")))
                fechar_button.click()
                print("✓ Botão 'Fechar' do modal clicado.")
                time.sleep(1)
            except TimeoutException:
                print("Nenhum modal 'Fechar' encontrado ou clicável. Prosseguindo...")
            
            print("Verificando o elemento de vídeo (iframe)...")
            try:
                video_iframe = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            except TimeoutException:
                self.fail("FALHA: Tempo esgotado. O iframe do vídeo não foi encontrado na página.")

            self.driver.switch_to.frame(video_iframe)
            print("✓ Mudou para o contexto do iframe do vídeo")
            
            try:
                play_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ytp-large-play-button")))
                print("✓ Botão de play encontrado.")
                self.driver.execute_script("arguments[0].click();", play_button)
                print("✓ Clicou no botão de play.")
            except TimeoutException:
                print("Botão de play não encontrado, tentando iniciar via API...")

            print("Forçando início do vídeo via API do YouTube (sem som)...")
            self.driver.execute_script("document.getElementById('movie_player')?.mute();")
            self.driver.execute_script("document.getElementById('movie_player')?.playVideo();")
            
            # Loop de espera para o vídeo começar a tocar
            player_state_after_play = None
            for _ in range(5): # Tenta por 5 segundos
                player_state_after_play = self.driver.execute_script("return document.getElementById('movie_player')?.getPlayerState()")
                if player_state_after_play == 1:
                    break
                time.sleep(1)

            take_step_screenshot(self.driver, self.id(), "video_tocando")
            
            self.assertEqual(player_state_after_play, 1, f"O vídeo não começou a tocar (estado final: {player_state_after_play}).")
            print("✓ O vídeo está tocando.")
            self.driver.switch_to.default_content()
        except Exception as e:
            traceback.print_exc()
            self.fail(f"Falha durante o teste de assistir vídeo logado: {e}")

    def test_02_assistir_video_deslogado(self):
        """Verifica se o usuário DESLOGADO consegue assistir a um vídeo de um curso."""
        print("\n--- EXECUTANDO: test_02_assistir_video_deslogado ---")
        self._navegar_para_pagina_de_video_deslogado()
        try:
            print("Verificando o elemento de vídeo (iframe)...")
            try:
                video_iframe = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            except TimeoutException:
                self.fail("FALHA: Tempo esgotado. O iframe do vídeo não foi encontrado na página.")

            self.driver.switch_to.frame(video_iframe)
            print("✓ Mudou para o contexto do iframe do vídeo")

            try:
                play_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ytp-large-play-button")))
                print("✓ Botão de play encontrado.")
                self.driver.execute_script("arguments[0].click();", play_button)
                print("✓ Clicou no botão de play.")
            except TimeoutException:
                print("Botão de play não encontrado, tentando iniciar via API...")

            print("Forçando início do vídeo via API do YouTube (sem som)...")
            self.driver.execute_script("document.getElementById('movie_player')?.mute();")
            self.driver.execute_script("document.getElementById('movie_player')?.playVideo();")

            # Loop de espera para o vídeo começar a tocar
            player_state_after_play = None
            for _ in range(5): # Tenta por 5 segundos
                player_state_after_play = self.driver.execute_script("return document.getElementById('movie_player')?.getPlayerState()")
                if player_state_after_play == 1:
                    break
                time.sleep(1)

            take_step_screenshot(self.driver, self.id(), "video_tocando_deslogado")

            self.assertEqual(player_state_after_play, 1, f"O vídeo não começou a tocar (estado final: {player_state_after_play}).")
            print("✓ O vídeo está tocando.")
            self.driver.switch_to.default_content()
        except Exception as e:
            traceback.print_exc()
            self.fail(f"Falha durante o teste de assistir vídeo deslogado: {e}")

if __name__ == "__main__":
    unittest.main()
