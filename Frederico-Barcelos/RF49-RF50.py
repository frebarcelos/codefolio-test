import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import traceback


class CodefolioTests(unittest.TestCase):

    def setUp(self):
        # Configurações
        self.TIMEOUT = 20
        self.URL_BASE = "https://testes.codefolio.com.br/"

        # --- DADOS DO FIREBASE ---
        self.FIREBASE_KEY = "FIREBASE_KEY_PLACEHOLDER"
        self.FIREBASE_VALUE = "FIREBASE_VALUE_PLACEHOLDER"

        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(5)
        self.wait = WebDriverWait(self.driver, self.TIMEOUT)
        
    def _login(self):
                """Injeta dados de autenticação no Local Storage para simular o login."""
                print("Injetando dados de autenticação no Local Storage...")
                self.driver.get(self.URL_BASE)
                try:
                    self.driver.execute_script(
                        "window.localStorage.setItem(arguments[0], arguments[1]);",
                        self.FIREBASE_KEY,
                        self.FIREBASE_VALUE
                    )
                    print("Injeção no Local Storage bem-sucedida.")
                except Exception as e:
                    print(f"Falha crítica ao injetar no Local Storage: {e}")
                    self.driver.quit()
                    raise RuntimeError("Falha no setup do Local Storage") from e
                self.driver.refresh()
                time.sleep(2) # Pausa para garantir que o login seja processado

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
        except:
            self.fail(f"Curso '{course_title}' não encontrado em nenhuma das abas.")

    def _navegar_para_pagina_de_video_logado(self):
        """Navega para a página de vídeo como um usuário logado."""
        self.verificar_login()
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



    def verificar_login(self):
        """Verifica se o login foi bem-sucedido."""
        print("Verificando se o login foi processado...")
        try:
            print("Aguardando 5s para o Firebase SDK processar o login...")
            time.sleep(5)
            profile_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Configurações da Conta']")))
            self.driver.execute_script("arguments[0].click();", profile_button)
            print("Clicou no botão de perfil para abrir o menu.")
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//li[normalize-space()='Sair']")))
            print("Login validado com sucesso!")
            self.driver.execute_script("document.body.click();")
        except Exception as e:
            print("--- ERRO NA VALIDAÇÃO DO LOGIN ---")
            print(f"Causa provável: O token no 'FIREBASE_VALUE' expirou ou está incorreto.")
            print(f"Exceção: {e}")
            self.fail("Falha na injeção de sessão do Firebase. O token pode estar expirado.")

    def tearDown(self):
        """Finaliza o teste, salva screenshot e fecha o driver."""
        if hasattr(self, 'driver') and self.driver:
            try:
                self.driver.save_screenshot(f"resultado_{self.id()}.png")
                print(f"Screenshot salvo como 'resultado_{self.id()}.png'")
            except:
                pass
            self.driver.quit()

    # --- Test Cases ---

    def test_01_assistir_video_logado(self):
        """Verifica se o usuário LOGADO consegue assistir a um vídeo de um curso."""
        print("\n--- EXECUTANDO: test_01_assistir_video_logado ---")
        self._login()
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
            video_iframe = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            self.driver.switch_to.frame(video_iframe)
            print("✓ Mudou para o contexto do iframe do vídeo")
            
            play_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ytp-large-play-button")))
            print("✓ Botão de play encontrado.")
            play_button.click()
            print("✓ Clicou no botão de play.")
            time.sleep(3)
            
            player_state_after_play = self.driver.execute_script("return document.getElementById('movie_player')?.getPlayerState()")
            self.assertEqual(player_state_after_play, 1, "O vídeo não começou a tocar após o clique no play.")
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
            video_iframe = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            self.driver.switch_to.frame(video_iframe)
            print("✓ Mudou para o contexto do iframe do vídeo")

            play_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ytp-large-play-button")))
            print("✓ Botão de play encontrado.")
            play_button.click()
            print("✓ Clicou no botão de play.")
            time.sleep(3)

            player_state_after_play = self.driver.execute_script("return document.getElementById('movie_player')?.getPlayerState()")
            self.assertEqual(player_state_after_play, 1, "O vídeo não começou a tocar após o clique no play.")
            print("✓ O vídeo está tocando.")
            self.driver.switch_to.default_content()
        except Exception as e:
            traceback.print_exc()
            self.fail(f"Falha durante o teste de assistir vídeo deslogado: {e}")

    def test_03_navegacao_logado(self):
        """Verifica a navegação entre vídeos para um usuário LOGADO."""
        print("\n--- EXECUTANDO: test_03_navegacao_logado ---")
        self._login()
        self._navegar_para_pagina_de_video_logado()
        self._realizar_teste_navegacao()

    def test_04_navegacao_deslogado(self):
        """Verifica a navegação entre vídeos para um usuário DESLOGADO."""
        print("\n--- EXECUTANDO: test_04_navegacao_deslogado ---")
        self.driver.get(self.URL_BASE) # Start fresh
        self._navegar_para_pagina_de_video_deslogado()
        self._realizar_teste_navegacao()

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
            # self.driver.quit()


if __name__ == "__main__":
    unittest.main()