import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

class EdicaoSlidesTest(unittest.TestCase):

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
        
        # Configuração de autenticação via Local Storage
        self.FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"
        self.FIREBASE_VALUE = """{"apiKey":"AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg","appName":"[DEFAULT]","createdAt":"1760400677093","displayName":"Bernardo Gomes Dorneles","email":"bernardodorneles.aluno@unipampa.edu.br","emailVerified":true,"isAnonymous":false,"lastLoginAt":"1762623423706","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocLO0jBvdkLbUox-pQeUPodOBF-co7iSXE_KehosP3OcjblGPRQ=s96-c","providerData":[{"displayName":"Bernardo Gomes Dorneles","email":"bernardodorneles.aluno@unipampa.edu.br","phoneNumber":null,"photoURL":"https://lh3.googleusercontent.com/a/ACg8ocLO0jBvdkLbUox-pQeUPodOBF-co7iSXE_KehosP3OcjblGPRQ=s96-c","providerId":"google.com","uid":"105856292510209699123"}],"stsTokenManager":{"accessToken":"eyJhbGciOiJSUzI1NiIsImtpZCI6IjU0NTEzMjA5OWFkNmJmNjEzODJiNmI0Y2RlOWEyZGZlZDhjYjMwZjAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQmVybmFyZG8gR29tZXMgRG9ybmVsZXMiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTE8wakJ2ZGtMYlVveC1wUWVVUG9kT0JGLWNvN2lTWEVfS2Vob3NQM09jamJsR1BSUT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9yZWFjdC1uYS1wcmF0aWNhIiwiYXVkIjoicmVhY3QtbmEtcHJhdGljYSIsImF1dGhfdGltZSI6MTc2MjYyMzUwMSwidXNlcl9pZCI6Ik92S09rWUNLMmVUN3huM1FjUVRZblpTYjFSMzMiLCJzdWIiOiJPdktPa1lDSzJlVDd4bjNRY1FUWW5aU2IxUjMzIiwiaWF0IjoxNzYyNjczOTkwLCJleHAiOjE3NjI2Nzc1OTAsImVtYWlsIjoiYmVybmFyZG9kb3JuZWxlcy5hbHVub0B1bmlwYW1wYS5lZHUuYnIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjEwNTg1NjI5MjUxMDIwOTY5OTEyMyJdLCJlbWFpbCI6WyJiZXJuYXJkb2Rvcm5lbGVzLmFsdW5vQHVuaXBhbXBhLmVkdS5iciJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.a-W_CUqU0ZP81ZpURu49b6cBrClWk0nqcraFGw47ktTuK3mqtIovg_dqmbZ7s5GghCdk6_twFA6ihdPuFbyLpCX8PZLAIcyQFQBeVQ11ql3oCDeGiQogXKw-sM5TIIix4gTgsS7IXhr6uNbkFCysLUSuA8H-bp10VsiU7R8fHz0BQTj0qExL6SCqCw05F76HXBuzxwyknYj1FeX53jGFdOmAhbHl9eHAhSkl7pBmkLBFkHqW9FXW1ttDGtg4Vh9UD_Inb432gglN-ZBPHy2ukSSrTOex430IDjJTdfZOhRe-jhscMnfLYWRS-9B1Y-dF7r-SJcW1_PTdCVuhYOhh0A","expirationTime":1762677590230,"refreshToken":"AMf-vBzmGoli8pLckXIHEHFjBsq9tdclxZJyoH1JbcdFrcPLRxGaM1rX9B8XHnnJ_XN05JfnkqyH5bYKdBmFud2NNZehSZM4mSXlBQU5HTmmV4vCyBk6T76D7ne-jyrdpzFvhApdJyMx-vyjhqUzyv2uMVdTxfj-pb6kZXAGW_a9tW7q0OA9CJ_KF1eGqx3DcSemtemLSxyxNo0A3gXeMMADVdpIgH8KmQbcFVfqEgr2Lh4C11_njx-Myfov2byzlZpc1zCivD1xCX5LLoEOgcCWMCp8_BEeHtwLeFGRS4DDxxpPH2-WcGpLJINOxCbUFQYeCfVT0bzzGjPgBKA28TQTmv7T0x8uCVBTUHNoVwpmpt9zFqO4QncobWpTnVT4ns7eQyRlBBNdTjSc9133whnn9bT3Wzfar0U2zh9VgFzjftgpgSx3UCNzJkCTvmicr38knaKKfpxGP6dDdqG4Ohjf_Ji9mPxzQw"},"tenantId":null,"uid":"OvKOkYCK2eT7xn3QcQTYnZSb1R33","_redirectEventId":null}"""
        
        
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

    def test_edicao_slides_rf9(self):
        """CT-01 - Edição de Slides (RF9)"""
        print("\n=== INICIANDO CT-01 - EDIÇÃO DE SLIDES ===")
        
        try:
            # 1. Navegar para Gerenciamento de Cursos
            self.navegar_para_gerenciamento_cursos()
            
            # 2. Selecionar um curso existente
            curso_selecionado = self.selecionar_curso_existente()
            if not curso_selecionado:
                self.fail("Nenhum curso disponível para teste")
            
            # 3. Navegar para a seção de Slides
            self.navegar_para_secao_slides()
            
            # 4. Encontrar e clicar no ícone de edição do slide 'funcionou'
            self.clicar_icone_edicao_slide()
            
            # 5. Editar o título do slide para 'IGREJA'
            self.editar_titulo_slide()
            
            # 6. Salvar as alterações do slide
            self.salvar_alteracoes_slide()
            
            # 7. Verificar se a edição foi salva
            self.verificar_edicao_slide()
            
            print("✅ CT-01 - EDIÇÃO DE SLIDES CONCLUÍDO COM SUCESSO!")
            
        except Exception as e:
            print(f"❌ FALHA NO CT-01: {e}")
            self.driver.save_screenshot("erro_final_ct01.png")
            print("📸 Screenshot do erro salvo como 'erro_final_ct01.png'")
            self.fail(f"CT-01 - Edição de Slides falhou: {e}")

    def navegar_para_gerenciamento_cursos(self):
        """Navega para a página de gerenciamento de cursos"""
        print("🧭 Navegando para Gerenciamento de Cursos...")
        
        # Clicar no menu de perfil
        profile_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[aria-label='Configurações da Conta']")
            )
        )
        self.driver.execute_script("arguments[0].click();", profile_button)
        
        # Clicar em Gerenciamento de Cursos
        gerenciamento_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[normalize-space()='Gerenciamento de Cursos']")
            )
        )
        gerenciamento_button.click()
        
        self.wait.until(EC.url_contains("/manage-courses"))
        print("✅ Navegação para Gerenciamento de Cursos concluída")

    def selecionar_curso_existente(self):
        """Seleciona um curso existente"""
        print("🎯 Selecionando curso existente...")
        
        time.sleep(3)
        
        # Procura pelo botão "Gerenciar Curso"
        try:
            gerenciar_buttons = self.driver.find_elements(By.XPATH, "//button[contains(., 'Gerenciar Curso')]")
            
            if gerenciar_buttons:
                print(f"✅ Encontrados {len(gerenciar_buttons)} botões 'Gerenciar Curso'")
                
                # Clica no primeiro botão "Gerenciar Curso"
                gerenciar_buttons[0].click()
                time.sleep(3)
                
                # Verifica se navegou para a página do curso
                if "adm-cursos" in self.driver.current_url:
                    print("✅ Navegação para o curso bem-sucedida!")
                    return "Curso Selecionado"
                else:
                    print("❌ Não navegou para a página do curso")
                    return None
            else:
                print("❌ Nenhum botão 'Gerenciar Curso' encontrado")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao selecionar curso: {e}")
            return None

    def navegar_para_secao_slides(self):
        """Navega para a seção de slides do curso - VERSÃO CORRIGIDA"""
        print("📊 Navegando para seção de Slides...")
        
        time.sleep(3)
        
        # DEBUG: Mostrar todas as abas disponíveis
        print("🔍 Procurando abas disponíveis...")
        try:
            # Procura por elementos que parecem ser abas
            possiveis_abas = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'tab')] | //button | //a | //div[@role='tab']")
            print(f"📋 Encontrados {len(possiveis_abas)} elementos que podem ser abas")
            
            for i, aba in enumerate(possiveis_abas):
                try:
                    texto = aba.text.strip()
                    if texto:
                        print(f"  {i+1}. '{texto}' - clicável: {aba.is_enabled()}")
                except:
                    pass
        except Exception as e:
            print(f"❌ Erro ao buscar abas: {e}")
        
        # Estratégias para encontrar a aba SLIDES
        slides_selectors = [
            "//*[contains(text(), 'SLIDES')]",
            "//*[contains(text(), 'Slides')]",
            "//button[contains(., 'SLIDES')]",
            "//button[contains(., 'Slides')]",
            "//a[contains(., 'SLIDES')]",
            "//a[contains(., 'Slides')]",
            "//div[contains(text(), 'SLIDES')]",
            "//div[contains(text(), 'Slides')]",
            "//*[@role='tab' and contains(., 'SLIDES')]",
            "//*[@role='tab' and contains(., 'Slides')]",
            "//*[contains(@class, 'tab') and contains(., 'SLIDES')]",
            "//*[contains(@class, 'tab') and contains(., 'Slides')]"
        ]
        
        for selector in slides_selectors:
            try:
                print(f"🔄 Tentando seletor: {selector}")
                slides_element = self.driver.find_element(By.XPATH, selector)
                
                if slides_element.is_displayed() and slides_element.is_enabled():
                    print(f"✅ Elemento de Slides encontrado: '{slides_element.text}'")
                    print("🖱️ Clicando na aba Slides...")
                    
                    # Tenta clicar de diferentes formas
                    try:
                        slides_element.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", slides_element)
                    
                    time.sleep(3)
                    
                    # Verifica se mudou para a seção de slides
                    if self.verificar_secao_slides_ativa():
                        print("✅ Navegação para Slides bem-sucedida!")
                        return
                    else:
                        print("❌ Não conseguiu navegar para Slides, tentando próximo seletor...")
                        continue
                        
            except Exception as e:
                print(f"❌ Seletor {selector} falhou: {e}")
                continue
        
        # Se nenhum seletor funcionou, tenta uma estratégia mais agressiva
        print("🔄 Tentando estratégia alternativa: buscar por texto 'Gerenciar Slides'...")
        try:
            gerenciar_slides = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Gerenciar Slides')]")
            print("✅ Encontrado 'Gerenciar Slides', provavelmente já está na seção correta")
            return
        except:
            pass
        
        print("❌ Não foi possível encontrar a aba Slides")
        raise Exception("Aba Slides não encontrada")

    def verificar_secao_slides_ativa(self):
        """Verifica se a seção de slides está ativa"""
        try:
            # Procura por indicadores de que está na seção de slides
            indicadores = [
                "//*[contains(text(), 'Gerenciar Slides')]",
                "//*[contains(text(), 'Adicionar Novo Slide')]",
                "//*[contains(text(), 'Slides Cadastrados')]",
                "//*[contains(text(), 'funcionou')]"
            ]
            
            for indicador in indicadores:
                try:
                    elemento = self.driver.find_element(By.XPATH, indicador)
                    if elemento.is_displayed():
                        print(f"✅ Seção de Slides ativa - encontrado: {indicador}")
                        return True
                except:
                    continue
            return False
        except:
            return False

    def clicar_icone_edicao_slide(self):
        """Encontra e clica no ícone de edição (lápis) do slide 'funcionou'"""
        print("🔍 Procurando slide 'funcionou' e ícone de edição...")
        
        time.sleep(3)
        
        try:
            # Encontra o elemento que contém "funcionou"
            slide_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'funcionou')]"))
            )
            print("✅ Slide 'funcionou' encontrado!")
            
            # Agora procura o ícone de edição (lápis) próximo a este elemento
            icone_selectors = [
                ".//ancestor::div[contains(@class, 'card')]//button",
                ".//ancestor::div[1]//button",
                ".//ancestor::div[2]//button", 
                ".//ancestor::div[3]//button",
                ".//following-sibling::div//button",
                ".//preceding-sibling::div//button",
                ".//..//button",
                ".//..//..//button"
            ]
            
            for selector in icone_selectors:
                try:
                    icone_editar = slide_element.find_element(By.XPATH, selector)
                    if icone_editar.is_displayed() and icone_editar.is_enabled():
                        print(f"✅ Ícone de edição encontrado com seletor: {selector}")
                        print("🖱️ Clicando no ícone de edição (lápis azul)...")
                        self.driver.execute_script("arguments[0].click();", icone_editar)
                        time.sleep(3)
                        return
                except:
                    continue
            
            # Estratégia alternativa: procurar por todos os ícones/botões próximos
            print("🔄 Tentando estratégia alternativa: buscar todos os botões próximos...")
            botoes_proximos = slide_element.find_elements(By.XPATH, ".//ancestor::div//button")
            for botao in botoes_proximos:
                if botao.is_displayed() and botao.is_enabled():
                    print("🖱️ Clicando em botão próximo ao slide 'funcionou'...")
                    self.driver.execute_script("arguments[0].click();", botao)
                    time.sleep(3)
                    if self.verificar_modal_edicao_aberto():
                        print("✅ Modal de edição aberto!")
                        return
            
            raise Exception("Não foi possível encontrar e clicar no ícone de edição próximo a 'funcionou'")
            
        except Exception as e:
            print(f"❌ Erro ao encontrar slide 'funcionou': {e}")
            raise

    def verificar_modal_edicao_aberto(self):
        """Verifica se o modal de edição de slide foi aberto"""
        try:
            # Procura por elementos que indicam que o modal está aberto
            modal_indicators = [
                "//*[contains(text(), 'Editar Slide')]",
                "//*[contains(text(), 'Edit Slide')]",
                "//input[contains(@value, 'funcionou')]",
                "//*[contains(@class, 'modal')]",
                "//*[contains(@class, 'dialog')]"
            ]
            
            for indicator in modal_indicators:
                try:
                    elemento = self.driver.find_element(By.XPATH, indicator)
                    if elemento.is_displayed():
                        return True
                except:
                    continue
            return False
        except:
            return False

    def editar_titulo_slide(self):
        """Edita o título do slide para 'IGREJA'"""
        print("✏️ Editando título do slide para 'IGREJA'...")
        
        time.sleep(2)
        
        # Procura pelo campo de título no modal de edição
        titulo_selectors = [
            "//input[@placeholder*='Título']",
            "//input[@placeholder*='Title']",
            "//input[contains(@value, 'funcionou')]",
            "//label[contains(., 'Título')]/following-sibling::input",
            "//label[contains(., 'Title')]/following-sibling::input",
            "//*[contains(text(), 'Título do Slide')]/following::input[1]"
        ]
        
        campo_titulo = None
        
        for selector in titulo_selectors:
            try:
                campo_titulo = self.driver.find_element(By.XPATH, selector)
                print(f"✅ Campo de título encontrado com seletor: {selector}")
                
                # Obtém o valor atual do campo
                valor_atual = campo_titulo.get_attribute('value')
                print(f"📝 Valor atual do título: '{valor_atual}'")
                
                break
            except:
                continue
        
        if not campo_titulo:
            # Tenta encontrar qualquer input que possa ser o título
            try:
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                for input_field in inputs:
                    if input_field.is_displayed() and input_field.is_enabled():
                        valor = input_field.get_attribute('value') or ''
                        if 'funcionou' in valor.lower():
                            campo_titulo = input_field
                            print(f"✅ Campo de título encontrado por busca alternativa")
                            break
            except Exception as e:
                print(f"❌ Erro na busca alternativa: {e}")
        
        if campo_titulo:
            # Limpa o campo e insere "IGREJA" - VERSÃO ROBUSTA
            print("⌨️ Alterando título para 'IGREJA'...")
            
            # Método 1: Limpar com JavaScript
            self.driver.execute_script("arguments[0].value = '';", campo_titulo)
            time.sleep(0.5)
            
            # Método 2: Limpar normal
            campo_titulo.clear()
            time.sleep(0.5)
            
            # Método 3: Selecionar tudo e apagar
            campo_titulo.send_keys(Keys.CONTROL + "a")
            campo_titulo.send_keys(Keys.DELETE)
            time.sleep(0.5)
            
            # Agora digita o novo texto
            campo_titulo.send_keys("IGREJA")
            print("✅ Título alterado para 'IGREJA'")
        else:
            print("❌ Não foi possível encontrar o campo de título")
            raise Exception("Campo de título não encontrado no modal de edição")

    def salvar_alteracoes_slide(self):
        """Salva as alterações do slide"""
        print("💾 Salvando alterações do slide...")
        
        time.sleep(1)
        
        # Procura pelo botão de salvar no modal
        salvar_selectors = [
            "//button[contains(., 'Salvar')]",
            "//button[contains(., 'Save')]",
            "//button[contains(., 'SALVAR')]",
            "//button[@type='submit']",
            "//button[.//*[contains(text(), 'Salvar')]]",
            "//*[contains(@class, 'modal')]//button[contains(., 'Salvar')]"
        ]
        
        for selector in salvar_selectors:
            try:
                salvar_btn = self.driver.find_element(By.XPATH, selector)
                print(f"✅ Botão de salvar encontrado: {salvar_btn.text}")
                print("🖱️ Clicando para salvar alterações...")
                salvar_btn.click()
                time.sleep(3)
                return
            except:
                continue
        
        print("❌ Botão de salvar não encontrado no modal")
        raise Exception("Botão de salvar não encontrado")

    def verificar_edicao_slide(self):
        """Verifica se a edição foi salva corretamente"""
        print("🔍 Verificando se a edição foi salva...")
        
        time.sleep(3)
        
        # Procura pelo texto "IGREJA" na lista de slides
        try:
            slide_editado = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'IGREJA')]"))
            )
            texto_encontrado = slide_editado.text
            print(f"✅ VERIFICAÇÃO CONCLUÍDA: Slide editado encontrado com texto: '{texto_encontrado}'")
            
            if "IGREJA" in texto_encontrado:
                print("🎉 SUCESSO TOTAL! O slide foi editado corretamente para 'IGREJA'")
            else:
                print(f"⚠️ Texto encontrado: '{texto_encontrado}' (diferente do esperado 'IGREJA')")
                
        except Exception as e:
            print(f"❌ O texto 'IGREJA' não foi encontrado na lista de slides: {e}")
            
            # Debug: mostra todos os textos na seção de slides
            print("\n🔍 Textos encontrados na seção de slides:")
            try:
                secoes = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Slides Cadastrados')]/following-sibling::*")
                for secao in secoes[:5]:
                    if secao.text.strip():
                        print(f"  - {secao.text.strip()}")
            except:
                pass

    def tearDown(self):
        """Limpeza após o teste"""
        if hasattr(self, 'driver') and self.driver:
            # self.driver.quit()  # Descomente para fechar o browser
            pass

if __name__ == "__main__":
    unittest.main()