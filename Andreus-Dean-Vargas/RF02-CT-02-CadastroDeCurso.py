"""
CT-02 - Cadastro de Cursos (RF02)
Autor: Andreus Dean Ferreira Almeida Rodrigues Vargas
Data: 23/11/2024
"""

import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from chrome_config import get_chrome_options
from login_util import login, verificar_login
from screenshot_util import take_evidence

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class TestCT02CadastroCurso(unittest.TestCase):
    """
    CT-02 - Cadastro de Cursos
    
    Requisito: RF02 - O sistema deve permitir o cadastro de novos cursos
    
    Objetivo: Verificar se o sistema permite que um professor autenticado
    cadastre um novo curso com sucesso, preenchendo os campos obrigatórios.
    
    Pré-condições:
        - Usuário autenticado como professor
    """
    
    URL_BASE = "https://testes-codefolio.web.app/"
    
    # Dados do curso a ser cadastrado
    NOME_CURSO = "Curso de Teste Automatizado"
    DESCRICAO_CURSO = "Este é um curso criado através de teste automatizado para validar o RF02"
    
    def setUp(self):
        """Configuração inicial do teste"""
        print("\n" + "="*70)
        print("INICIANDO CT-02 - CADASTRO DE CURSO")
        print("="*70)
        
        options = get_chrome_options()
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 15)
    
    def tearDown(self):
        """Finalização do teste"""
        print("\n" + "-"*70)
        print("Finalizando CT-02")
        print("-"*70)
        # Mantém navegador aberto para análise
        # self.driver.quit()
    
    def test_ct02_cadastro_curso(self):
        """
        Objetivo: Verificar se o sistema permite cadastrar um novo curso
        """
        
        # PASSO 1: Fazer login
        print("\n[PASSO 1] Fazendo login no sistema...")
        login(self.driver, self.URL_BASE)
        verificar_login(self.driver, self.wait)
        take_evidence(self.driver, self.id(), 1, "tela_inicial_apos_login")
        print("✓ Login realizado com sucesso")
        
        # PASSO 2: Navegar para Gerenciamento de Cursos
        print("\n[PASSO 2] Navegando para Gerenciamento de Cursos...")
        try:
            # Clica no botão de configurações da conta
            profile_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[aria-label='Configurações da Conta']")
                )
            )
            self.driver.execute_script("arguments[0].click();", profile_button)
            print("✓ Menu de perfil aberto")
            
            time.sleep(1)
            
            # Clica em "Gerenciamento de Cursos"
            gerenciamento_item = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//li[normalize-space()='Gerenciamento de Cursos']")
                )
            )
            gerenciamento_item.click()
            
            # Aguarda carregar a página
            self.wait.until(EC.url_contains("/manage-courses"))
            print("✓ Página de gerenciamento carregada")
            
            # Evidência 02: Página de gerenciamento antes do cadastro
            time.sleep(2)
            take_evidence(self.driver, self.id(), 2, "pagina_gerenciamento_antes_cadastro")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_navegar_gerenciamento")
            self.fail(f"FALHA ao navegar para gerenciamento: {e}")
        
        # PASSO 3: Clicar em "Adicionar Novo Curso" ou similar
        print("\n[PASSO 3] Clicando em 'Adicionar Novo Curso'...")
        try:
            # Scroll para garantir que o botão esteja visível
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # Busca botão de adicionar (pode ter textos diferentes)
            botao_adicionar = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Adicionar') or contains(., 'Novo Curso') or contains(., 'Criar')]")
                )
            )
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_adicionar)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", botao_adicionar)
            print("✓ Botão 'Adicionar Curso' clicado")
            
            # Aguarda modal/formulário abrir
            time.sleep(2)
            
            # Evidência 03: Modal de cadastro aberto
            take_evidence(self.driver, self.id(), 3, "modal_cadastro_aberto")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_abrir_cadastro")
            self.fail(f"FALHA ao abrir formulário de cadastro: {e}")
        
        # PASSO 4: Preencher campo "Nome do Curso"
        print("\n[PASSO 4] Preenchendo campo 'Nome do Curso'...")
        try:
            campo_nome = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//label[contains(., 'Nome')]/following-sibling::div//input | //input[@placeholder*='Nome']")
                )
            )
            
            campo_nome.clear()
            time.sleep(0.5)
            campo_nome.send_keys(self.NOME_CURSO)
            print(f"✓ Nome do curso preenchido: '{self.NOME_CURSO}'")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_campo_nome")
            self.fail(f"FALHA ao preencher nome do curso: {e}")
        
        # PASSO 5: Preencher campo "Descrição"
        print("\n[PASSO 5] Preenchendo campo 'Descrição'...")
        try:
            # Busca campo de descrição (pode ser textarea ou input)
            campo_descricao = self.driver.find_element(
                By.XPATH,
                "//label[contains(., 'Descrição')]/following-sibling::div//textarea | //label[contains(., 'Descrição')]/following-sibling::div//input | //textarea[@placeholder*='Descrição']"
            )
            
            campo_descricao.clear()
            time.sleep(0.5)
            campo_descricao.send_keys(self.DESCRICAO_CURSO)
            print(f"✓ Descrição preenchida")
            
            time.sleep(1)
            
            # Evidência 04: Formulário preenchido
            take_evidence(self.driver, self.id(), 4, "formulario_preenchido")
            
        except Exception as e:
            print("⚠ Campo Descrição não encontrado (pode ser opcional)")
            take_evidence(self.driver, self.id(), 4, "formulario_sem_descricao")
        
        # PASSO 6: Salvar o curso
        print("\n[PASSO 6] Salvando o curso...")
        try:
            botao_salvar = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Salvar') or contains(., 'Criar') or contains(., 'Adicionar')]")
                )
            )
            
            self.driver.execute_script("arguments[0].click();", botao_salvar)
            print("✓ Botão 'Salvar' clicado")
            
            # Aguarda processar
            time.sleep(3)
            
            # Evidência 05: Após salvar
            take_evidence(self.driver, self.id(), 5, "apos_salvar")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_salvar")
            self.fail(f"FALHA ao salvar curso: {e}")
        
        # PASSO 7: Verificar se o curso aparece na lista
        print("\n[PASSO 7] Verificando se o curso foi cadastrado...")
        try:
            time.sleep(2)
            
            # Procura pelo nome do curso na página
            curso_cadastrado = self.driver.find_element(
                By.XPATH,
                f"//*[contains(text(), '{self.NOME_CURSO}')]"
            )
            
            if curso_cadastrado:
                print(f"✓ SUCESSO: Curso '{self.NOME_CURSO}' encontrado na lista!")
                
                # Evidência 06: Curso cadastrado na lista
                take_evidence(self.driver, self.id(), 6, "curso_cadastrado_lista")
                
                # Teste PASSOU
                self.assertTrue(True, "Curso cadastrado com sucesso")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_verificar_cadastro")
            self.fail(f"FALHA: Curso não encontrado na lista após cadastro: {e}")
        
        print("\n" + "="*70)
        print("CT-02 - CADASTRO DE CURSO CONCLUÍDO")
        print("="*70)


if __name__ == "__main__":
    unittest.main()