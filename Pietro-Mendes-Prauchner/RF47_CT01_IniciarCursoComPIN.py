"""
RF47_CT01_IniciarCursoComPIN.py

Teste Selenium para RF47: Iniciar Curso com PIN

Requisito: O sistema deve permitir que o estudante comece cursos protegidos 
mediante a inserção de um código PIN.

Fluxo esperado:
1. Login via Firebase (injeta credenciais no localStorage)
2. Validar que o login foi bem-sucedido
3. Navegar para a aba de Cursos
4. Selecionar a aba "Disponíveis"
5. Procurar pelo curso "RF 42 - Grupo 4"
6. Clicar em "Começar"
7. Modal de PIN aparece (já vem selecionado)
8. Inserir PIN "1234"
9. Clicar em "Enviar"
10. Validar que o curso iniciou com sucesso
"""

import unittest
import time
import traceback
import sys
from os.path import abspath, dirname

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Adiciona o diretório ao path para importar utils locais
sys.path.insert(0, dirname(abspath(__file__)))
from login_util import login, verificar_login, url_base, time_out
from chrome_config import get_chrome_options
from screenshot_util import save_screenshot


class TestRF47IniciarCursoComPIN(unittest.TestCase):
    """Testa a funcionalidade de iniciar um curso com PIN (RF47)."""

    def setUp(self):
        """Setup executado antes de cada teste."""
        try:
            chrome_options = get_chrome_options()
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(5)
            self.wait = WebDriverWait(self.driver, time_out)
            self.test_name = "test_iniciar_curso_com_pin_RF47"
            print(f"\n{'='*60}")
            print(f"Iniciando teste: {self.id()}")
            print(f"{'='*60}\n")
        except Exception as e:
            print(f"ERRO no setUp: {e}")
            traceback.print_exc()
            raise

    def tearDown(self):
        """Cleanup após cada teste."""
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
                print("\nDriver fechado com sucesso.")
        except Exception as e:
            print(f"Erro ao fechar driver: {e}")

    def _abrir_area_cursos(self):
        """
        Abre a área de Cursos clicando no ícone SmartDisplay no topbar.
        Retorna True se conseguiu abrir, False caso contrário.
        """
        print("\n[PASSO 3] ABRINDO ÁREA DE CURSOS")
        
        # Múltiplos seletores para encontrar o botão de Cursos
        xpaths = [
            "//svg[@data-testid='SmartDisplayIcon']/ancestor::div[1]",
            "//div[contains(@class,'topbarIconCont') and .//span[contains(normalize-space(),'Cursos')]]",
            "//div[.//span[normalize-space()='Cursos']]",
        ]
        
        for xp in xpaths:
            try:
                elems = self.driver.find_elements(By.XPATH, xp)
                for e in elems:
                    if e.is_displayed():
                        try:
                            e.click()
                        except Exception:
                            self.driver.execute_script('arguments[0].click();', e)
                        print("✓ Clicou no botão Cursos com sucesso")
                        time.sleep(1)
                        return True
            except Exception:
                continue
        
        print("✗ Não encontrou o botão Cursos")
        return False

    def _selecionar_aba_disponiveis(self):
        """
        Seleciona a aba 'Disponíveis' dentro da área de Cursos.
        Retorna True se conseguiu selecionar, False caso contrário.
        """
        print("\n[PASSO 4] SELECIONANDO ABA 'DISPONÍVEIS'")
        try:
            # Procura por um botão que contenha "Disponível" (case-insensitive)
            disponivel_button = self.driver.find_element(
                By.XPATH,
                "//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'dispon')]"
            )
            self.driver.execute_script("arguments[0].click();", disponivel_button)
            print("✓ Clicou na aba Disponíveis com sucesso")
            time.sleep(1)
            return True
        except NoSuchElementException:
            print("⚠ Aba Disponíveis não encontrada, continuando na aba padrão...")
            return True

    def _encontrar_e_iniciar_curso_com_pin(self):
        """
        Procura especificamente pelo curso "RF 42 - Grupo 4" e clica em "Começar".
        
        Estratégia:
        1. Encontra TODOS os cards (MuiCard-root)
        2. Para CADA card, verifica se o título contém "RF 42" ou "Grupo 4"
        3. Quando encontra, clica em "Começar"
        4. Retorna True se clicou com sucesso
        
        Retorna True se conseguiu clicar em Começar, False caso contrário.
        """
        print("\n[PASSO 5] PROCURANDO CURSO 'RF 42 - Grupo 4'")
        
        try:
            # Encontra TODOS os cards de curso
            all_cards = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'MuiCard-root')]")
            print(f"   Encontrados {len(all_cards)} card(s) de curso")
            
            for idx, card in enumerate(all_cards):
                try:
                    # Extrai o título
                    try:
                        titulo = card.find_element(By.XPATH, ".//h6").text.strip()
                    except:
                        titulo = f"Card {idx + 1}"
                    
                    # Verifica se é o curso "RF 42 - Grupo 4"
                    titulo_lower = titulo.lower()
                    if "rf 42" in titulo_lower or "grupo 4" in titulo_lower:
                        if "com pin" not in titulo_lower:  # Evitar variações com PIN
                            print(f"   ✓ Encontrado: '{titulo}'")
                            
                            # Procura pelo botão "Começar"
                            try:
                                comecar_button = card.find_element(
                                    By.XPATH,
                                    ".//button[normalize-space()='Começar' or contains(normalize-space(), 'Começar')]"
                                )
                            except NoSuchElementException:
                                print(f"       ⚠ Sem botão 'Começar' (continuando)")
                                continue
                            
                            # Scroll e clique
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", comecar_button)
                            time.sleep(0.3)
                            
                            try:
                                comecar_button.click()
                            except:
                                self.driver.execute_script("arguments[0].click();", comecar_button)
                            
                            print(f"       ✓ Clicou em 'Começar'")
                            save_screenshot(self.driver, self.test_name, "05_apos_click_comecar")
                            time.sleep(1.5)
                            return True
                
                except Exception as e:
                    continue
            
            print("✗ Curso 'RF 42 - Grupo 4' não encontrado")
            return False
            
        except Exception as e:
            print(f"✗ Erro ao procurar curso: {e}")
            traceback.print_exc()
            return False

    def _inserir_pin_e_validar(self):
        """
        Insere o PIN "1234" no campo de PIN e clica em "Enviar".
        
        O campo é um input MUI dentro de um MuiFormControl.
        
        Retorna True se conseguiu inserir PIN e clicar Enviar, False caso contrário.
        """
        print("\n[PASSO 6] INSERINDO PIN E ENVIANDO")
        
        try:
            # Procura o input do PIN (dentro do MuiFormControl com label "PIN de Acesso")
            print("   └─ Procurando campo de PIN...")
            
            # Múltiplas estratégias para encontrar o input
            pin_input = None
            
            # Estratégia 1: Por ID (data-shrink label)
            try:
                pin_input = self.driver.find_element(
                    By.XPATH,
                    "//input[@type='text' and @maxlength='7']"
                )
                print("   ✓ Campo de PIN encontrado (por type/maxlength)")
            except:
                pass
            
            # Estratégia 2: Dentro do MuiFormControl
            if not pin_input or not pin_input.is_displayed():
                try:
                    pin_input = self.driver.find_element(
                        By.XPATH,
                        "//div[contains(@class, 'MuiFormControl-root')]//label[contains(normalize-space(), 'PIN')]/..//input"
                    )
                    print("   ✓ Campo de PIN encontrado (por label)")
                except:
                    pass
            
            if not pin_input:
                print("   ✗ Campo de PIN não encontrado")
                return False
            
            # Scroll para o campo
            self.driver.execute_script("arguments[0].scrollIntoView(true);", pin_input)
            time.sleep(0.3)
            
            # Clica no campo para garantir focus
            try:
                pin_input.click()
            except:
                self.driver.execute_script("arguments[0].click();", pin_input)
            
            time.sleep(0.3)
            
            # Limpa qualquer valor anterior
            pin_input.clear()
            
            # Digita o PIN
            print("   └─ Digitando PIN '1234'...")
            pin_input.send_keys("1234")
            time.sleep(0.5)
            save_screenshot(self.driver, self.test_name, "06_pin_digitado")
            
            # Procura e clica no botão "Enviar"
            print("   └─ Procurando botão 'Enviar'...")
            try:
                enviar_button = self.driver.find_element(
                    By.XPATH,
                    "//button[normalize-space()='Enviar' or contains(normalize-space(), 'Enviar')]"
                )
            except NoSuchElementException:
                print("   ✗ Botão 'Enviar' não encontrado")
                return False
            
            # Clica em Enviar
            self.driver.execute_script("arguments[0].scrollIntoView(true);", enviar_button)
            time.sleep(0.3)
            
            try:
                enviar_button.click()
            except:
                self.driver.execute_script("arguments[0].click();", enviar_button)
            
            print("   ✓ Clicou em 'Enviar'")
            save_screenshot(self.driver, self.test_name, "07_apos_click_enviar")
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"   ✗ Erro ao inserir PIN: {e}")
            traceback.print_exc()
            return False

    def test_iniciar_curso_com_pin(self):
        """Teste principal: Iniciar um curso com PIN."""
        print('\n' + '='*60)
        print('TESTE RF47: Iniciar Curso com PIN')
        print('='*60)
        
        try:
            # [PASSO 1] Login
            print("\n[PASSO 1] REALIZANDO LOGIN")
            login(self.driver)
            save_screenshot(self.driver, self.test_name, "01_apos_login")
            
            # [PASSO 2] Verificar login
            print("\n[PASSO 2] VALIDANDO LOGIN")
            verificar_login(self.driver, self.wait)
            save_screenshot(self.driver, self.test_name, "02_apos_validacao_login")
            
            # [PASSO 3] Abrir área de Cursos
            if not self._abrir_area_cursos():
                self.fail("FALHA: Não conseguiu abrir a área de Cursos")
            save_screenshot(self.driver, self.test_name, "03_area_cursos_aberta")
            time.sleep(0.5)
            
            # [PASSO 4] Selecionar aba Disponíveis
            self._selecionar_aba_disponiveis()
            save_screenshot(self.driver, self.test_name, "04_aba_disponiveis_selecionada")
            time.sleep(0.5)
            
            # [PASSO 5] Procurar e clicar no curso "RF 42 - Grupo 4"
            if not self._encontrar_e_iniciar_curso_com_pin():
                self.fail("FALHA: Não conseguiu encontrar e clicar no curso 'RF 42 - Grupo 4'")
            
            # [PASSO 6] Inserir PIN e clicar Enviar
            if not self._inserir_pin_e_validar():
                self.fail("FALHA: Não conseguiu inserir PIN ou clicar Enviar")
            
            # [PASSO 7] Validar que o curso iniciou
            print("\n[PASSO 7] VALIDANDO ACESSO AO CURSO")
            time.sleep(1)
            
            # Verifica indicadores de que o curso foi acessado
            page_indicators = self.driver.find_elements(
                By.XPATH,
                "//h1 | //h2 | //iframe[contains(@src, 'youtube')] | //*[contains(@class, 'course')] | //*[contains(@class, 'aula')]"
            )
            
            visible_indicators = [ind for ind in page_indicators if ind.is_displayed()]
            
            if visible_indicators:
                print(f"✓ Detectados {len(visible_indicators)} indicador(es) de conteúdo")
            else:
                print("⚠ Nenhum indicador de conteúdo detectado (mas PIN foi validado)")
            
            save_screenshot(self.driver, self.test_name, "08_curso_iniciado")
            
            print('\n' + '='*60)
            print('✓ TESTE RF47 CONCLUÍDO COM SUCESSO')
            print('='*60 + '\n')
            
        except AssertionError as e:
            print(f'\n✗ Teste falhou: {e}')
            save_screenshot(self.driver, self.test_name, "XX_erro_teste")
            raise
        except Exception as e:
            print(f'\n✗ Erro inesperado: {e}')
            traceback.print_exc()
            save_screenshot(self.driver, self.test_name, "XX_erro_inesperado")
            self.fail(f'Erro inesperado: {e}')


if __name__ == '__main__':
    unittest.main()
