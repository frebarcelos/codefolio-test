"""
CT-03 - Edição de Cursos (RF03)
Autor: Andreus Dean Ferreira Almeida Rodrigues Vargas
Data: 23/11/2024
"""

import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from chrome_config import get_chrome_options
from login_util import login, verificar_login
from screenshot_util import take_evidence
from element_finder import find_input_by_label, find_textarea_by_label, find_button_by_text
from curso_helper import garantir_curso_existe

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class TestCT03EdicaoCurso(unittest.TestCase):
    """
    CT-03 - Edição de Cursos
    
    Requisito: RF03 - O sistema deve permitir a edição de cursos existentes
    
    Objetivo: Verificar se o sistema permite que um professor autenticado
    edite as informações de um curso existente.
    
    Pré-condições:
        - Usuário autenticado como professor
        - Deve existir pelo menos um curso cadastrado
    """
    
    URL_BASE = "https://testes-codefolio.web.app/"
    
    # Dados para edição
    NOVO_NOME = "Curso Editado Automaticamente"
    NOVA_DESCRICAO = "Descrição atualizada através de teste automatizado"
    
    # Dados do curso fallback (caso precise criar)
    NOME_CURSO_FALLBACK = "Curso para Teste de Edição"
    DESCRICAO_CURSO_FALLBACK = "Curso criado automaticamente para testar edição"
    
    def setUp(self):
        """Configuração inicial do teste"""
        print("\n" + "="*70)
        print("INICIANDO CT-03 - EDIÇÃO DE CURSO")
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
        print("Finalizando CT-03")
        print("-"*70)
        # self.driver.quit()
    
    def test_ct03_edicao_curso(self):
        """
        Objetivo: Verificar se o sistema permite editar um curso existente
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
            profile_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[aria-label='Configurações da Conta']")
                )
            )
            self.driver.execute_script("arguments[0].click();", profile_button)
            
            time.sleep(1)
            
            gerenciamento_item = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//li[normalize-space()='Gerenciamento de Cursos']")
                )
            )
            gerenciamento_item.click()
            
            self.wait.until(EC.url_contains("/manage-courses"))
            print("✓ Página de gerenciamento carregada")
            
            time.sleep(2)
            take_evidence(self.driver, self.id(), 2, "lista_cursos_antes_edicao")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_navegar_gerenciamento")
            self.fail(f"FALHA ao navegar: {e}")
        
        # PASSO 3: Verificar se existe curso, se não criar um
        print("\n[PASSO 3] Verificando se existe curso...")
        try:
            garantir_curso_existe(
                self.driver,
                self.wait,
                self.NOME_CURSO_FALLBACK,
                self.DESCRICAO_CURSO_FALLBACK,
                self.URL_BASE
            )
            
            print("\n[PASSO 3.1] Selecionando curso para editar...")
            time.sleep(2)
            
            botao_gerenciar = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//button[contains(., 'Gerenciar Curso')])[1]")
                )
            )
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_gerenciar)
            time.sleep(1)
            botao_gerenciar.click()
            print("✓ Curso selecionado")
            
            time.sleep(3)
            
            take_evidence(self.driver, self.id(), 3, "pagina_curso_antes_edicao")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_selecionar_curso")
            self.fail(f"FALHA ao selecionar curso: {e}")
        
        # PASSO 4: Clicar no botão de editar curso
        print("\n[PASSO 4] Clicando em 'Editar Curso'...")
        try:
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            botao_editar = find_button_by_text(self.driver, self.wait, "editar")
            
            if not botao_editar:
                raise Exception("Botão 'Editar' não encontrado")
            
            self.driver.execute_script("arguments[0].click();", botao_editar)
            print("✓ Botão 'Editar' clicado")
            
            time.sleep(2)
            
            take_evidence(self.driver, self.id(), 4, "modal_edicao_aberto")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_abrir_edicao")
            self.fail(f"FALHA ao abrir edição: {e}")
        
        # PASSO 5: Editar nome do curso
        print("\n[PASSO 5] Editando nome do curso...")
        try:
            campo_nome = find_input_by_label(self.driver, self.wait, "nome")
            
            if not campo_nome:
                raise Exception("Campo 'Nome' não encontrado")
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", campo_nome)
            time.sleep(0.5)
            
            campo_nome.clear()
            time.sleep(0.5)
            campo_nome.send_keys(self.NOVO_NOME)
            print(f"✓ Nome alterado para: '{self.NOVO_NOME}'")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_editar_nome")
            self.fail(f"FALHA ao editar nome: {e}")
        
        # PASSO 6: Editar descrição do curso
        print("\n[PASSO 6] Editando descrição do curso...")
        try:
            campo_descricao = find_textarea_by_label(self.driver, self.wait, "descrição")
            
            if not campo_descricao:
                campo_descricao = find_input_by_label(self.driver, self.wait, "descrição")
            
            if campo_descricao:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", campo_descricao)
                time.sleep(0.5)
                campo_descricao.clear()
                time.sleep(0.5)
                campo_descricao.send_keys(self.NOVA_DESCRICAO)
                print("✓ Descrição atualizada")
            else:
                print("⚠ Campo Descrição não encontrado (pode ser opcional)")
            
            time.sleep(1)
            
            take_evidence(self.driver, self.id(), 5, "formulario_editado")
            
        except Exception as e:
            print(f"⚠ Erro ao preencher descrição (pode ser opcional): {e}")
        
        # PASSO 7: Salvar alterações
        print("\n[PASSO 7] Salvando alterações...")
        try:
            botao_salvar = find_button_by_text(self.driver, self.wait, "salvar")
            
            if not botao_salvar:
                raise Exception("Botão 'Salvar' não encontrado")
            
            self.driver.execute_script("arguments[0].click();", botao_salvar)
            print("✓ Botão 'Salvar' clicado")
            
            time.sleep(3)
            
            take_evidence(self.driver, self.id(), 6, "apos_salvar_edicao")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_salvar_edicao")
            self.fail(f"FALHA ao salvar: {e}")
        
        # PASSO 8: Verificar se alterações foram salvas
        print("\n[PASSO 8] Verificando se alterações foram salvas...")
        try:
            time.sleep(2)
            
            curso_editado = self.driver.find_element(
                By.XPATH,
                f"//*[contains(text(), '{self.NOVO_NOME}')]"
            )
            
            if curso_editado:
                print(f"✓ SUCESSO: Curso editado encontrado com nome '{self.NOVO_NOME}'!")
                
                take_evidence(self.driver, self.id(), 7, "curso_editado_verificado")
                
                self.assertTrue(True, "Curso editado com sucesso")
            
        except Exception as e:
            take_evidence(self.driver, self.id(), 99, "erro_verificar_edicao")
            self.fail(f"FALHA: Alterações não foram salvas: {e}")
        
        print("\n" + "="*70)
        print("CT-03 - EDIÇÃO DE CURSO CONCLUÍDO")
        print("="*70)


if __name__ == "__main__":
    unittest.main()
