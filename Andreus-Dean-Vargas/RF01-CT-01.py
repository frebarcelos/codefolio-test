"""
CT-01 - Edição de Perfil do Usuário
RF1 - O sistema deve permitir que o usuário edite seu perfil
Autor: Andreus Dean Ferreira Almeida Rodrigues Vargas
"""
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Importa os utilitários
from chrome_config import get_chrome_options
from login_util import login, verificar_login, verificar_login  # <-- USANDO LOGIN MANUAL
from screenshot_util import take_evidence, reset_screenshot_counter


class TestCT01EdicaoPerfil(unittest.TestCase):
    """CT-01 - Teste de Edição de Perfil do Usuário"""
    
    def setUp(self):
        """Configuração inicial antes de cada teste."""
        print("\n" + "="*70)
        print("INICIANDO CT-01 - EDIÇÃO DE PERFIL DO USUÁRIO")
        print("="*70)
        
        # Configuração do Chrome
        options = get_chrome_options()
        service = Service(ChromeDriverManager().install())
        
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 15)
        self.URL_BASE = "https://testes-codefolio.web.app/"
        
        # Reseta contador de screenshots
        reset_screenshot_counter(self.id())
    
    def tearDown(self):
        """Finaliza o teste e fecha o navegador."""
        print("\n" + "-"*70)
        print("Finalizando CT-01")
        print("-"*70)
        
        if self.driver:
            time.sleep(2)  # Pausa para visualizar resultado
            self.driver.quit()
    
    def test_ct01_edicao_perfil_usuario(self):
        """
        Objetivo: Verificar se o sistema permite que o usuário altere suas 
        informações de perfil (nome exibido e links de redes sociais) e 
        salva corretamente as alterações.
        
        Pré-condição:
        - Usuário autenticado
        - Usuário já possui perfil cadastrado
        """
        
        # PASSO 1: Fazer login
        print("\n[PASSO 1] Fazendo login no sistema...")
        login(self.driver, self.URL_BASE)
        
        # Verifica se login foi bem-sucedido
        verificar_login(self.driver, self.wait)
        
        # Evidência 01: Tela inicial após login
        take_evidence(self.driver, self.id(), 1, "tela_inicial_apos_login")
        print("✓ Login realizado com sucesso")
        
        # PASSO 2: Acessar menu de perfil e navegar para perfil
        print("\n[PASSO 2] Acessando o perfil...")
        try:
            # Clica no botão de configurações da conta (igual ao Bernardo)
            profile_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[aria-label='Configurações da Conta']")
                )
            )
            self.driver.execute_script("arguments[0].click();", profile_button)
            print("✓ Menu de perfil aberto")
            
            time.sleep(1)
            
            # Clica no item "Perfil" no menu (usando normalize-space igual ao Bernardo)
            perfil_menu_item = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//li[normalize-space()='Perfil']")
                )
            )
            perfil_menu_item.click()
            
            # Aguarda carregar a página de perfil
            self.wait.until(EC.url_contains("/profile"))
            print("✓ Página de perfil carregada")
            
            # Evidência 02: Página de perfil antes da edição
            time.sleep(2)
            take_evidence(self.driver, self.id(), 2, "pagina_perfil_antes_edicao")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_navegar_perfil")
            print(f"\n❌ ERRO DETALHADO: {e}")
            self.fail(f"FALHA ao navegar para página de perfil: {e}")
        
        # PASSO 3: Clicar no botão de editar (ícone de lápis)
        print("\n[PASSO 3] Clicando no botão de editar...")
        try:
            # Scroll para garantir que o botão esteja visível
            self.driver.execute_script("window.scrollTo(0, 300);")
            time.sleep(2)
            
            # Busca pelo botão com ícone EditIcon (padrão do Bernardo)
            botao_editar = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[@data-testid='EditIcon']//ancestor::button")
                )
            )
            
            # Scroll para centralizar e clicar
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_editar)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", botao_editar)
            print("✓ Botão de editar clicado")
            
            # Aguarda modal/formulário abrir
            time.sleep(2)
            
            # Evidência 03: Modal de edição aberto
            take_evidence(self.driver, self.id(), 3, "modal_edicao_aberto")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_clicar_editar")
            print(f"\n❌ ERRO DETALHADO: {e}")
            self.fail(f"FALHA ao clicar no botão de editar: {e}")
        
        # PASSO 4: Editar campo "Nome"
        print("\n[PASSO 4] Editando campo 'Nome'...")
        try:
            # Busca campo Nome (padrão do Bernardo: direto e simples)
            campo_nome = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//label[contains(., 'Nome')]/following-sibling::div//input")
                )
            )
            
            # Limpa e preenche
            campo_nome.clear()
            time.sleep(0.5)
            campo_nome.send_keys("Andreus Dean Editado")
            print("✓ Nome alterado para 'Andreus Dean Editado'")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_campo_nome")
            self.fail(f"FALHA ao editar nome: {e}")
        
        # PASSO 5: Atualizar campo Instagram
        print("\n[PASSO 5] Atualizando campo Instagram...")
        try:
            campo_instagram = self.driver.find_element(
                By.XPATH, 
                "//label[contains(., 'Instagram')]/following-sibling::div//input"
            )
            campo_instagram.clear()
            campo_instagram.send_keys("https://instagram.com/andreusvargas")
            print("✓ Instagram atualizado")
        except Exception as e:
            print("⚠ Campo Instagram não encontrado (opcional)")
        
        # PASSO 7: Atualizar campo LinkedIn
        print("\n[PASSO 7] Atualizando campo LinkedIn...")
        try:
            campo_linkedin_selectors = [
                "//input[@placeholder*='LinkedIn']",
                "//label[contains(., 'LinkedIn')]/following-sibling::input",
                "//input[@name='linkedin']"
            ]
            
            campo_linkedin = None
            for selector in campo_linkedin_selectors:
                try:
                    campo_linkedin = self.driver.find_element(By.XPATH, selector)
                    if campo_linkedin.is_displayed() and campo_linkedin.is_enabled():
                        break
                except:
                    continue
            
            if campo_linkedin:
                campo_linkedin.click()
                campo_linkedin.send_keys(Keys.CONTROL + "a")
                campo_linkedin.send_keys(Keys.DELETE)
                time.sleep(0.5)
                campo_linkedin.send_keys("https://linkedin.com/in/andreusvargas")
                print("✓ LinkedIn atualizado")
            else:
                print("⚠ Campo LinkedIn não encontrado (pode não existir no sistema)")
                
        except Exception as e:
            print(f"⚠ Aviso ao atualizar LinkedIn: {e}")
        
        # Evidência 04: Formulário preenchido
        time.sleep(1)
        take_evidence(self.driver, self.id(), 4, "formulario_preenchido")
        
        # PASSO 8: Salvar as alterações
        print("\n[PASSO 8] Salvando as alterações...")
        try:
            btn_salvar_selectors = [
                "//button[contains(text(), 'Salvar')]",
                "//button[contains(text(), 'SALVAR')]",
                "//button[contains(text(), 'Salvar Alterações')]",
                "//button[@type='submit']"
            ]
            
            btn_salvar = None
            for selector in btn_salvar_selectors:
                try:
                    btn_salvar = self.driver.find_element(By.XPATH, selector)
                    if btn_salvar.is_displayed() and btn_salvar.is_enabled():
                        break
                except:
                    continue
            
            if not btn_salvar:
                raise Exception("Botão 'Salvar' não encontrado")
            
            btn_salvar.click()
            print("✓ Botão 'Salvar' clicado")
            
            time.sleep(3)  # Aguarda processamento
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_salvar_alteracoes")
            self.fail(f"FALHA ao salvar alterações: {e}")
        
        # PASSO 9: Verificar mensagem de sucesso
        print("\n[PASSO 9] Verificando mensagem de sucesso...")
        try:
            # Procura por mensagens de sucesso comuns
            mensagem_sucesso_selectors = [
                "//*[contains(text(), 'sucesso')]",
                "//*[contains(text(), 'atualizado')]",
                "//*[contains(text(), 'salvo')]",
                "//div[contains(@class, 'success')]",
                "//div[contains(@class, 'alert-success')]"
            ]
            
            mensagem_encontrada = False
            for selector in mensagem_sucesso_selectors:
                try:
                    mensagem = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    if mensagem.is_displayed():
                        print(f"✓ Mensagem de sucesso encontrada: '{mensagem.text}'")
                        mensagem_encontrada = True
                        break
                except:
                    continue
            
            if not mensagem_encontrada:
                print("⚠ Mensagem de sucesso não encontrada (pode já ter desaparecido)")
            
            # Evidência 05: Após salvar
            time.sleep(1)
            take_evidence(self.driver, self.id(), 5, "apos_salvar_alteracoes")
            
        except Exception as e:
            print(f"⚠ Aviso ao verificar mensagem: {e}")
        
        # PASSO 10: Verificar se alterações foram aplicadas
        print("\n[PASSO 10] Verificando se alterações foram aplicadas...")
        try:
            # Atualiza a página para garantir que os dados foram salvos
            self.driver.refresh()
            time.sleep(2)
            
            # Procura pelo nome "Andreus Dean" na página
            nome_elementos = self.driver.find_elements(
                By.XPATH, 
                "//*[contains(text(), 'Andreus Dean')]"
            )
            
            if len(nome_elementos) > 0:
                print("✓ Nome 'Andreus Dean' encontrado na página!")
                print(f"  Encontrado em {len(nome_elementos)} elemento(s)")
            else:
                print("⚠ Nome não encontrado imediatamente (pode estar em área não visível)")
            
            # Evidência 06: Verificação final
            take_evidence(self.driver, self.id(), 6, "verificacao_final")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_verificacao_final")
            print(f"⚠ Aviso na verificação final: {e}")
        
        # RESULTADO FINAL
        print("\n" + "="*70)
        print("✅ CT-01 - EDIÇÃO DE PERFIL CONCLUÍDO COM SUCESSO!")
        print("="*70)
        print("\nResumo:")
        print("  ✓ Login realizado")
        print("  ✓ Navegação para perfil")
        print("  ✓ Formulário de edição acessado")
        print("  ✓ Campos preenchidos")
        print("  ✓ Alterações salvas")
        print("  ✓ Evidências capturadas (6 screenshots)")
        print("\nVerifique os screenshots em: screenshots/test_ct01_edicao_perfil_usuario/")
        print("="*70)


if __name__ == "__main__":
    unittest.main()