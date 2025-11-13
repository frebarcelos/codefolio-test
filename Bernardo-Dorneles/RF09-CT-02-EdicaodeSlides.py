import time
import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

class EdicaoSlideConteudoTest(unittest.TestCase):

    # Link URL novo slide
    LINK_NOVO = 'https://docs.google.com/presentation/d/e/2PACX-1vTAlD3_xMaoKzufd_BBuDCS9UC_Y2FLFAqP6ca6qgb4OReLnJKERm_UWo67u8JK8w/pub?start=false&loop=false&delayms=3000'

    def setUp(self):
        """Configuração inicial antes de cada teste"""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        self.wait = WebDriverWait(self.driver, 15)
        self.URL_BASE = "https://testes.codefolio.com.br/"

        self.EVIDENCE_DIR = "Bernardo-Dorneles/img/"
        os.makedirs(self.EVIDENCE_DIR, exist_ok=True)
        
        # Configuração de autenticação via Local Storage
        self.FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"
        self.FIREBASE_VALUE = """{"apiKey":"AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg","appName":"[DEFAULT]","createdAt":"1760400677093","displayName":"Bernardo Gomes Dorneles","email":"bernardodorneles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1762623423706","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocLO0jBvdkLbUox-pQeUPodOBF-co7iSXE_KehosP3OcjblGPRQ=s96-c","providerData":[{"displayName":"Bernardo Gomes Dorneles","email":"bernardodorneles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocLO0jBvdkLbUox-pQeUPodOBF-co7iSXE_KehosP3OcjblGPRQ=s96-c","providerId":"google.com","uid":"105856292510209699123"}],"stsTokenManager":{"accessToken":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjU0NTEzMjA5OWFkNmJmNjEzODJiNmI0Y2RlOWEyZGZlZDhjYjMwZjAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQmVybmFyZG8gR29tZXMgRG9ybmVsZXMiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTE8wakJ2ZGtMYlVveC1wUWVVUG9kT0JGLWNvN2lTWEVfS2Vob3NQM09jamJsR1BSUT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9yZWFjdC1uYS1wcmF0aWNhIiwiYXVkIjoicmVhY3QtbmEtcHJhdGljYSIsImF1dGhfdGltZSI6MTc2MjYyMzUwMSwidXNlcl9pZCI6Ik92S09rWUNLMmVUN3huM1FjVVRZblpTYjFSMzMiLCJzdWIiOiJPdktPa1lDSzJlVDd4bjNRY1FUWW5aU2IxUjMzIiwiaWF0IjoxNzYyNjczOTkwLCJleHAiOjE3NjI2Nzc1OTAsImVtYWlsIjoiYmVybmFyZG9kb3JuZWxlcy5hbHVub0B1bmlwYW1wYS5lZHUuYnIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjEwNTg1NjI5MjUxMDIwOTY5OTEyMyJdLCJlbWFpbCI6WyJiZXJuYXJkb2Rvcm5lbGVzLmFsdW5vQHVuaXBhbXBhLmVkdS5iciJdfSwic2lnbl9pbl9wcm9jSmlkZXIiOiJnb29nbGUuY29tIn19.a-W_CUqU0ZP81ZpURu49b6cBrClWk0nqcraFGw47ktTuK3mqtIovg_dqmbZ7s5GghCdk6_twFA6ihdPuFbyLpCX8PZLAIcyQFQBeVQ11ql3oCDeGiQogXKw-sM5TIIix4gTgsS7IXhr6uNbkFCysLUSuA8H-bp10VsiU7R8fHz0BQTj0qExL6SCqCw05F76HXBuzxwyknYj1FeX53jGFdOmAhbHl9eHAhSkl7pBmkLBFkHqW9FXW1ttDGtg4Vh9UD_Inb432gglN-ZBPHy2ukSSrTOex430IDjJTdfZOhRe-jhscMnfLYWRS-9B1Y-dF7r-SJcW1_PTdCVuhYOhh0A","expirationTime":1762677590230,"refreshToken":"AMf-vBzmGoli8pLckXIHEHFjBsq9tdclxZJyoH1JbcdFrcPLRxGaM1rX9B8XHnnJ_XN05JfnkqyH5bYKdBmFud2NNZehSZM4mSXlBQU5HTmmV4vCyBk6T76D7ne-jyrdpzFvhApdJyMx-vyjhqUzyv2uMVdTxfj-pb6kZXAGW_a9tW7q0OA9CJ_KF1eGqx3DcSemtemLSxyxNo0A3gXeMMADVdpIgH8KmQbcFVfqEgr2Lh4C11_njx-Myfov2byzlZpc1zCivD1xCX5LLoEOgcCWMCp8_BEeHtwLeFGRS4DDxxpPH2-WcGpLJINOxCbUFQYeCfVT0bzzGjPgBKA28TQTmv7T0x8uCVBTUHNoVwpmpt9zFqO4QncobWpTnVT4ns7eQyRlBBNdTjSc9133whnn9bT3Wzfar0U2zh9VgFzjftgpgSx3UCNzJkCTvmicr38knaKKfpxGP6dDdqG4Ohjf_Ji9mPxzQw"},"tenantId":null,"uid":"OvKOkYCK2eT7xn3QcQTYnZSb1R33","_redirectEventId":null}"""
        
        self.configurar_autenticacao()

    def configurar_autenticacao(self):
        """Configura a autenticação via Local Storage"""
        self.driver.get(self.URL_BASE)
        print("Injetando dados de autenticação no Local Storage...")
        try:
            self.driver.execute_script(
                "window.localStorage.setItem(arguments[0], arguments[1]);",
                self.FIREBASE_KEY,
                self.FIREBASE_VALUE
            )
            print("Injeção no Local Storage bem-sucedida.")
        except Exception as e:
            print(f"Falha ao injetar no Local Storage: {e}")
            self.driver.quit()
            raise
        self.driver.refresh()
        time.sleep(3)

    def test_edicao_conteudo_slide_rf9(self):
        """CT-02 - Edição de CONTEÚDO de Slides (RF9)"""
        print("\n=== INICIANDO CT-02 - EDIÇÃO DE CONTEÚDO DE SLIDE ===")
        resultado_foi_sucesso = False
        
        try:
            self.navegar_para_gerenciamento_cursos()
            curso_selecionado = self.selecionar_curso_existente()
            if not curso_selecionado:
                self.fail("Nenhum curso disponível para teste")
            
            self.navegar_para_secao_slides(capturar_evidencia=False)
            self.clicar_icone_edicao_slide()
            self.editar_conteudo_slide(self.LINK_NOVO) # Edita o conteúdo (link do slide)
            self.salvar_alteracoes_slide()
            self.fechar_modal_sucesso()
            resultado_foi_sucesso = self.verificar_edicao_conteudo_slide(self.LINK_NOVO) # Verifica o conteúdo
            
        except Exception as e:
            print(f"FALHA NO CT-02 (CONTEÚDO) DURANTE A EXECUÇÃO: {e}")
            self.driver.save_screenshot(self.EVIDENCE_DIR + "erro_inesperado_ct02_conteudo.png")
            self.fail(f"CT-02 (CONTEÚDO) - Falhou inesperadamente: {e}")
        
        self.assertTrue(resultado_foi_sucesso, 
                        "FALHA NA ASSERTIVA FINAL (CONTEÚDO): O conteúdo (link) do slide não foi salvo corretamente.")
        print("CT-02 (CONTEÚDO) - EDIÇÃO DE SLIDES CONCLUÍDO COM SUCESSO!")


    # --- MÉTODOS DE NAVEGAÇÃO E AÇÕES COMUNS ---

    def navegar_para_gerenciamento_cursos(self):
        """Navega para a página de gerenciamento de cursos"""
        print("Navegando para Gerenciamento de Cursos...")
        profile_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Configurações da Conta']")))
        self.driver.execute_script("arguments[0].click();", profile_button)
        gerenciamento_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//li[normalize-space()='Gerenciamento de Cursos']")))
        gerenciamento_button.click()
        self.wait.until(EC.url_contains("/manage-courses"))
        print("Navegação para Gerenciamento de Cursos concluída")

    def selecionar_curso_existente(self):
        """Seleciona um curso existente"""
        print("Selecionando curso existente...")
        time.sleep(3)
        try:
            gerenciar_buttons = self.driver.find_elements(By.XPATH, "//button[contains(., 'Gerenciar Curso')]")
            if gerenciar_buttons:
                print(f"Encontrados {len(gerenciar_buttons)} botões 'Gerenciar Curso'")
                gerenciar_buttons[0].click()
                time.sleep(3)
                if "adm-cursos" in self.driver.current_url:
                    print("Navegação para o curso bem-sucedida!")
                    print("Rolando até o final da página do curso...")
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    return "Curso Selecionado"
                else:
                    print("Não navegou para a página do curso")
                    return None
            else:
                print("Nenhum botão 'Gerenciar Curso' encontrado")
                return None
        except Exception as e:
            print(f"Erro ao selecionar curso: {e}")
            return None

    def navegar_para_secao_slides(self, capturar_evidencia=False):
        """Navega para a seção de slides do curso"""
        print("Navegando para seção de Slides...")
        time.sleep(3)
        
        slides_selectors = [
            "//*[contains(text(), 'SLIDES')]", "//*[contains(text(), 'Slides')]",
            "//button[contains(., 'SLIDES')]", "//button[contains(., 'Slides')]",
            "//*[@role='tab' and contains(., 'SLIDES')]", "//*[@role='tab' and contains(., 'Slides')]"
        ]
        
        for selector in slides_selectors:
            try:
                slides_element = self.driver.find_element(By.XPATH, selector)
                if slides_element.is_displayed() and slides_element.is_enabled():
                    print(f"Elemento de Slides encontrado: '{slides_element.text}'")
                    print("Clicando na aba Slides...")
                    self.driver.execute_script("arguments[0].click();", slides_element)
                    time.sleep(3)
                    
                    if self.verificar_secao_slides_ativa():
                        print("Navegação para Slides bem-sucedida!")
                        print("Rolando até o final da seção de slides...")
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                        
                        # (Este teste não captura o "antes")
                        
                        return
            except:
                continue
        
        raise Exception("Aba Slides não encontrada")

    def verificar_secao_slides_ativa(self):
        """Verifica se a seção de slides está ativa"""
        try:
            indicadores = ["//*[contains(text(), 'Gerenciar Slides')]", "//*[contains(text(), 'Slides Cadastrados')]"]
            for indicador in indicadores:
                if self.driver.find_element(By.XPATH, indicador).is_displayed():
                    print(f"Seção de Slides ativa - encontrado: {indicador}")
                    return True
            return False
        except:
            return False

    def clicar_icone_edicao_slide(self):
        """Encontra e clica no ícone de edição (lápis) do PRIMEIRO slide da lista"""
        print("Procurando o ícone de edição do primeiro slide...")
        time.sleep(3)
        try:
            icone_editar = self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//*[contains(text(), 'Slides Cadastrados')]/following-sibling::div//button)[1]")))
            print("Ícone de edição do primeiro slide encontrado!")
            print("Clicando no ícone de edição...")
            self.driver.execute_script("arguments[0].click();", icone_editar)
            time.sleep(3)
            
            if not self.verificar_modal_edicao_aberto():
                raise Exception("O modal de edição não abriu após o clique.")
        except Exception as e:
            print(f"Erro ao encontrar o primeiro ícone de edição: {e}")
            raise

    def verificar_modal_edicao_aberto(self):
        """Verifica se o modal de edição de slide foi aberto"""
        try:
            modal_indicators = ["//*[contains(text(), 'Editar Slide')]", "//*[contains(@class, 'dialog')]"]
            for indicator in modal_indicators:
                WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located((By.XPATH, indicator)))
                print(f"Modal de edição aberto (verificado por: {indicator})")
                return True
            return False
        except:
            return False

    def salvar_alteracoes_slide(self):
        """Salva as alterações do slide"""
        print("Salvando alterações do slide...")
        time.sleep(1)
        salvar_selectors = ["//button[contains(., 'Salvar')]", "//button[contains(., 'Save')]", "//button[@type='submit']"]
        for selector in salvar_selectors:
            try:
                salvar_btn = self.driver.find_element(By.XPATH, selector)
                print(f"Botão de salvar encontrado: {salvar_btn.text}")
                print("Clicando para salvar alterações...")
                salvar_btn.click()
                time.sleep(3)
                return
            except:
                continue
        raise Exception("Botão de salvar não encontrado")

    def fechar_modal_sucesso(self):
        """Verifica se há um modal de 'OK' ou 'Sucesso' e o fecha."""
        print("Verificando se há um modal de 'OK' ou 'Sucesso'...")
        try:
            ok_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'OK') or contains(., 'Ok') or contains(., 'Fechar')]")))
            print("Modal de 'OK' encontrado. Clicando...")
            ok_button.click()
            time.sleep(2)
        except Exception as e:
            print("Nenhum modal 'OK' de sucesso encontrado, continuando...")
            pass

    # --- FUNÇÕES ESPECÍFICAS DO TESTE DE CONTEÚDO (CORRIGIDAS) ---

    def editar_conteudo_slide(self, link_html):
        """Edita o conteúdo HTML (link) do slide"""
        print("Editando conteúdo HTML (link) do slide...")
        time.sleep(2)
        try:
            # --- SELETOR CORRIGIDO ---
            # Encontra o label "URL do Slide" e pega o input associado a ele
            campo_conteudo = self.wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, "//label[contains(., 'URL do Slide')]/following-sibling::div//input"
                ))
            )
            print("Campo 'URL do Slide (Google Apresentações)' encontrado.")
            
            campo_conteudo.send_keys(Keys.CONTROL + "a")
            campo_conteudo.send_keys(Keys.DELETE)
            time.sleep(0.5)
            campo_conteudo.clear()
            time.sleep(0.5)
            
            campo_conteudo.send_keys(link_html)
            print("Novo conteúdo link inserido.")
            
            time.sleep(1)
            print("Tirando screenshot - 2. Durante a Edição (Conteúdo)")
            self.driver.save_screenshot(self.EVIDENCE_DIR + "RF09-CT-02/evidencia_02_durante_edicao_conteudo.png")

        except Exception as e:
            print(f"Erro ao encontrar/editar campo 'URL do Slide': {e}")
            raise Exception("Campo 'URL do Slide (Google Apresentações)' não foi encontrado.")

    def verificar_edicao_conteudo_slide(self, link_esperado) -> bool:
        """Verifica se o CONTEÚDO (link) foi salvo e RETORNA True/False."""
        print("Verificando se o conteúdo (link) foi salvo...")
        try:
            # Precisamos reabrir o modal para verificar o valor do input
            print("Reabrindo o modal para verificação de conteúdo...")
            self.clicar_icone_edicao_slide() # Clica no mesmo primeiro ícone
            
            # --- SELETOR CORRIGIDO ---
            campo_conteudo = self.wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, "//label[contains(., 'URL do Slide')]/following-sibling::div//input"
                ))
            )
            
            # Pega o valor de dentro do input
            conteudo_atual = campo_conteudo.get_attribute('value')
            
            print("Tirando screenshot - 3. Depois da Edição (Conteúdo)")
            self.driver.save_screenshot(self.EVIDENCE_DIR + "RF09-CT-02/evidencia_03_depois_edicao_conteudo.png")

            # Fechar o modal para não atrapalhar
            try:
                fechar_btn = self.driver.find_element(By.XPATH, "//button[contains(., 'Cancelar') or contains(., 'Fechar')]")
                fechar_btn.click()
                time.sleep(1)
            except:
                pass # Se não achar, não é crítico

            if link_esperado in conteudo_atual:
                print("Verificação de conteúdo: SUCESSO")
                return True
            else:
                print("Verificação de conteúdo: FALHA (Conteúdo salvo não confere)")
                print(f"Esperado: {link_esperado}")
                print(f"Recebido: {conteudo_atual}")
                return False
        
        except Exception as e:
            print(f"Erro ao verificar conteúdo: {e}")
            self.driver.save_screenshot(self.EVIDENCE_DIR + "erro_verificacao_conteudo.png")
            return False

    def tearDown(self):
        """Limpeza após o teste"""
        if hasattr(self, 'driver') and self.driver:
            # self.driver.quit() 
            print("Teste finalizado. O navegador permanecerá aberto (tearDown comentado).")
            pass

if __name__ == "__main__":
    unittest.main()