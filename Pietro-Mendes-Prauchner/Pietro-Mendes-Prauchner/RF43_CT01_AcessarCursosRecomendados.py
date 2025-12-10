"""
RF43_CT01_AcessarCursosRecomendados.py

Teste Selenium para RF43: Cursos Recomendados (Acessar sem PIN)

Requisito: Permitir que o estudante acesse cursos recomendados que não exigem código PIN através da home.

Fluxo esperado:
1. Login via Firebase (injeta credenciais no localStorage)
2. Validar que o login foi bem-sucedido
3. Navegar para a HOME
4. Localizar a seção 'Cursos Recomendados'
5. Encontrar um curso que não exija PIN (sem ícone de cadeado / não desabilitado)
6. Acessar o curso
7. Validar que o acesso foi realizado (mudança de URL ou conteúdo do curso visível)
"""

import unittest
import time
import traceback
import sys
from os.path import abspath, dirname

from selenium import webdriver
from selenium.webdriver.common.by import By
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


class TestRF43AcessarCursosRecomendados(unittest.TestCase):
    """Testa acesso a cursos recomendados sem PIN (RF43)."""

    def setUp(self):
        try:
            chrome_options = get_chrome_options()
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(5)
            # garantir janela maximizada aqui (inicialização limpa a partir do zero)
            try:
                self.driver.maximize_window()
            except Exception:
                pass
            self.wait = WebDriverWait(self.driver, time_out)
            self.test_name = "test_acessar_cursos_recomendados_sem_pin"
            print(f"\n{'='*60}")
            print(f"Iniciando teste: {self.id()}")
            print(f"{'='*60}\n")
        except Exception as e:
            print(f"ERRO no setUp: {e}")
            traceback.print_exc()
            raise

    def tearDown(self):
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
                print("\nDriver fechado com sucesso.")
        except Exception as e:
            print(f"Erro ao fechar driver: {e}")

    def _encontrar_secao_recomendados(self):
        """Tenta localizar a seção de Cursos Recomendados na HOME."""
        selectors = [
            "//section[.//h2[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'recomend')]]",
            "//div[contains(@class, 'recomend') or containS(@class, 'recomendados') or contains(., 'Cursos recomendados')]",
            "//*[contains(text(), 'Cursos recomendados') or contains(text(), 'Recomendados') or contains(text(), 'Cursos Recomendados')]",
        ]

        for sel in selectors:
            try:
                elems = self.driver.find_elements(By.XPATH, sel)
                for e in elems:
                    if e.is_displayed():
                        return e
            except Exception:
                continue
        return None

    def _encontrar_curso_sem_pin(self, secao):
        """Procura dentro da seção por um curso que pareça não exigir PIN.
        Estratégia: busca por links/cards e descarta itens com ícone de cadeado ou classe disabled.
        Retorna o elemento clicável (link/card) ou None.
        """
        # procura por links ou botões dentro da seção
        candidates = []
        try:
            candidates = secao.find_elements(By.XPATH, ".//a|.//button|.//div[contains(@role,'button')]")
        except Exception:
            return None

        for c in candidates:
            try:
                if not c.is_displayed() or not c.is_enabled():
                    continue

                # Ignorar se tiver referência a PIN ou ícone de cadeado no texto/atributos
                txt = (c.text or "").lower()
                aria = (c.get_attribute('aria-label') or "").lower()
                href = (c.get_attribute('href') or "").lower()
                classes = (c.get_attribute('class') or "").lower()

                if 'pin' in txt or 'pin' in aria or 'pin' in href:
                    continue
                if 'lock' in txt or 'cadeado' in txt or 'lock' in aria or 'cadeado' in aria:
                    continue
                if 'locked' in classes or 'pin' in classes or 'bloque' in classes:
                    continue

                # se não aparenta requerer PIN, retornamos
                return c
            except Exception:
                continue

        return None

    def _acessar_curso(self, curso_elem):
        try:
            self.driver.execute_script('arguments[0].scrollIntoView(true);', curso_elem)
            time.sleep(0.3)
            try:
                curso_elem.click()
            except Exception:
                self.driver.execute_script('arguments[0].click();', curso_elem)
            time.sleep(1.5)
            # se a ação redirecionar diretamente para o YouTube, considerar falha
            cur = (self.driver.current_url or '').lower()
            if 'youtube.com' in cur or 'youtu.be' in cur:
                print('  → Redirecionou para YouTube — ignorando este candidato')
                return False
            return True
        except Exception as e:
            print(f"Erro ao acessar curso: {e}")
            return False

    def _is_youtube_target(self, element):
        """Retorna True se o elemento (ou seus descendentes) apontar para YouTube/iframe YouTube."""
        try:
            tag = (element.tag_name or '').lower()
            if tag == 'a':
                href = (element.get_attribute('href') or '').lower()
                if 'youtube.com' in href or 'youtu.be' in href:
                    return True

            # procurar outros links/iframes dentro do elemento
            try:
                links = element.find_elements(By.XPATH, ".//a[@href]")
                for a in links:
                    href = (a.get_attribute('href') or '').lower()
                    if 'youtube.com' in href or 'youtu.be' in href:
                        return True
            except Exception:
                pass

            try:
                iframes = element.find_elements(By.TAG_NAME, 'iframe')
                for f in iframes:
                    src = (f.get_attribute('src') or '').lower()
                    if 'youtube.com' in src or 'youtu.be' in src:
                        return True
            except Exception:
                pass

            return False
        except Exception:
            return False

    def _find_card_and_button_by_title(self, secao, title_text):
        """Procura dentro de `secao` um card que contenha `title_text` no h6 e retorna o botão 'Acessar' dentro do card, ou None."""
        try:
            # localizar h6 pelo texto dentro da seção
            h6_xpath = f".//h6[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{title_text.lower()}')]" 
            headers = secao.find_elements(By.XPATH, h6_xpath)
            for h in headers:
                try:
                    # sobe até o ancestor card (div com classe MuiCard-root) e busca botão 'Acessar'
                    card = h.find_element(By.XPATH, "ancestor::div[contains(@class,'MuiCard-root')]")
                    # garantir que não é um card bloqueado (LockIcon)
                    try:
                        lock = card.find_elements(By.XPATH, ".//svg[@data-testid='LockIcon']")
                        if lock and any((l.is_displayed() for l in lock)):
                            continue
                    except Exception:
                        pass

                    # extrai botão 'Acessar' dentro do card
                    try:
                        btn = card.find_element(By.XPATH, ".//button[normalize-space()='Acessar' or contains(normalize-space(.),'Acessar')]")
                        if btn.is_displayed() and btn.is_enabled():
                            return btn
                    except Exception:
                        # tentar achar qualquer botão clicável dentro do card
                        try:
                            cand = card.find_element(By.XPATH, ".//button | .//a | .//div[contains(@role,'button')]")
                            if cand.is_displayed() and cand.is_enabled():
                                return cand
                        except Exception:
                            continue
                except Exception:
                    continue
        except Exception:
            return None
        return None

    def _detectar_modal_pin(self):
        """Detecta a presença de um prompt/modal pedindo PIN/Código.
        Retorna True se detectar um campo de PIN ou texto solicitando PIN.
        """
        try:
            # procura por inputs que possam ser PIN (password, number) ou placeholders/labels com 'pin'/'código'
            pin_inputs = self.driver.find_elements(By.XPATH, "//input[@type='password'] | //input[contains(translate(@placeholder, 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'PIN')] | //input[contains(translate(@placeholder, 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CÓDIGO') or contains(translate(@placeholder, 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CODIGO')]")
            if any((el.is_displayed() for el in pin_inputs)):
                return True

            # procurar textos no modal/dialog
            dialogs = self.driver.find_elements(By.XPATH, "//div[contains(@role,'dialog')] | //div[contains(@class,'modal')]")
            for d in dialogs:
                text = (d.text or '').lower()
                if 'pin' in text or 'código' in text or 'codigo' in text or 'insira o pin' in text:
                    return True

            # procurar botões/labels relacionados a PIN
            pin_buttons = self.driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'PIN') or contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'CÓDIGO')]")
            if any((b.is_displayed() for b in pin_buttons)):
                return True

            return False
        except Exception:
            return False

    def test_acessar_curso_recomendado_sem_pin(self):
        """Fluxo de teste principal para RF43."""
        print("\n" + "="*60)
        print("TESTE RF43: Cursos Recomendados (Acessar sem PIN)")
        print("="*60)

        try:
            # PASSO 1: LOGIN
            print("\n[PASSO 1] LOGIN VIA FIREBASE")
            login(self.driver)
            save_screenshot(self.driver, self.test_name, "01_apos_login")

            # PASSO 2: VALIDAR LOGIN
            print("\n[PASSO 2] VALIDAR LOGIN")
            verificar_login(self.driver, self.wait)
            print("✓ Login validado com sucesso")

            # PASSO 3: NAVEGAR PARA HOME
            print("\n[PASSO 3] NAVEGAR PARA HOME")
            time.sleep(1)
            self.driver.get(url_base)
            time.sleep(2)
            save_screenshot(self.driver, self.test_name, "02_home_page")

            try:
                self.wait.until(EC.url_to_be(url_base))
            except TimeoutException:
                pass

            # PASSO 4: LOCALIZAR SEÇÃO RECOMENDADOS
            print("\n[PASSO 4] LOCALIZANDO 'CURSOS RECOMENDADOS'")
            # Antes de tudo, localizar a seção e tentar encontrar o card pelo título
            curso = None

            secao = self._encontrar_secao_recomendados()
            if not secao:
                self.fail("FALHA: Seção 'Cursos Recomendados' não encontrada na HOME.")
            print("✓ Seção 'Cursos Recomendados' encontrada")
            save_screenshot(self.driver, self.test_name, "03_secao_recomendados")

            # PASSO 5: ENCONTRAR CURSO QUE NÃO EXIJA PIN
            print("\n[PASSO 5] PROCURANDO CURSO SEM PIN")
            try:
                # usar um helper focado para localizar o card e o botão 'Acessar' pelo título
                curso = self._find_card_and_button_by_title(secao, 'TESTE RF29 - GRUPO 6')
                if curso:
                    print("✓ Encontrado card específico 'TESTE RF29 - GRUPO 6' e seu botão 'Acessar'")
                    save_screenshot(self.driver, self.test_name, "04_curso_rf29_encontrado")
            except Exception:
                curso = None

            # se não encontrou dentro da seção, tentar busca global pelo h6/título (fallback)
            if not curso:
                try:
                    hdrs = self.driver.find_elements(By.XPATH, "//h6[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'teste rf29') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'rf29')]")
                    for h in hdrs:
                        try:
                            card = h.find_element(By.XPATH, "ancestor::div[contains(@class,'MuiCard-root')]")
                            # checar lock
                            try:
                                lock = card.find_elements(By.XPATH, ".//svg[@data-testid='LockIcon']")
                                if lock and any((l.is_displayed() for l in lock)):
                                    continue
                            except Exception:
                                pass
                            try:
                                btn = card.find_element(By.XPATH, ".//button[normalize-space()='Acessar' or contains(normalize-space(.),'Acessar')]")
                                if btn.is_displayed() and btn.is_enabled():
                                    curso = btn
                                    print("✓ Encontrado globalmente o card 'TESTE RF29 - GRUPO 6' e seu botão 'Acessar'")
                                    save_screenshot(self.driver, self.test_name, "04_global_rf29_found")
                                    break
                            except Exception:
                                continue
                        except Exception:
                            continue
                except Exception:
                    pass

            # Se não encontrou o curso específico, usar heurística genérica
            if not curso:
                curso = self._encontrar_curso_sem_pin(secao)
            if not curso:
                print("⚠ Nenhum curso claramente sem PIN encontrado heurísticamente — tentando primeiro curso disponível como fallback")
                # monta lista de candidatos (reafind a cada tentativa porque o DOM pode mudar)
                xpath_candidates = ".//*[@onclick] | .//a | .//button | .//div[contains(@role,'button')] | .//div[contains(@class,'card')] | .//article | .//li//a | .//h3/.."
                candidates = []
                try:
                    candidates = secao.find_elements(By.XPATH, xpath_candidates)
                except Exception:
                    candidates = []

                # se não há candidatos internos, procurar globalmente por links de curso
                if not candidates:
                    try:
                        candidates = self.driver.find_elements(By.XPATH, "//a[contains(@href,'/curso') or contains(@href,'/course') or contains(@href,'curso') or contains(@href,'course')]")
                    except Exception:
                        candidates = []

                if not candidates:
                    self.fail("FALHA: Não foi encontrado nenhum item clicável na seção de recomendados nem links de curso na página.")

                # tentar vários candidatos até encontrar um que não solicite PIN
                max_try = min(len(candidates), 6)
                found = False
                for idx in range(max_try):
                    try:
                        # refind candidates list to avoid StaleElementReference
                        try:
                            current_list = secao.find_elements(By.XPATH, xpath_candidates)
                        except Exception:
                            current_list = self.driver.find_elements(By.XPATH, "//a[contains(@href,'/curso') or contains(@href,'/course') or contains(@href,'curso') or contains(@href,'course')]")

                        if idx >= len(current_list):
                            break
                        candidate = current_list[idx]
                        if not (candidate.is_displayed() and candidate.is_enabled()):
                            continue

                        # pular candidatos que apontam para YouTube
                        if self._is_youtube_target(candidate):
                            print(f"  → Pulando candidato #{idx+1} que aponta para YouTube")
                            continue

                        save_screenshot(self.driver, self.test_name, f"04_curso_candidato_{idx}")
                        print(f"Tentando candidato #{idx+1}...")
                        if not self._acessar_curso(candidate):
                            # tentar próximo
                            self.driver.get(url_base)
                            time.sleep(1)
                            continue

                        time.sleep(0.7)
                        if self._detectar_modal_pin():
                            print("  → Apareceu prompt de PIN neste candidato, tentando próximo...")
                            self.driver.get(url_base)
                            time.sleep(1)
                            continue
                        else:
                            curso = candidate
                            found = True
                            print("✓ Curso candidato sem PIN encontrado e acessado com sucesso")
                            break
                    except Exception:
                        continue

                if not found:
                    self.fail("FALHA: Testou candidatos na seção, todos solicitaram PIN ou não foram acessíveis.")
            else:
                print("✓ Curso candidato encontrado")
                save_screenshot(self.driver, self.test_name, "04_curso_encontrado")

            # PASSO 6: ACESSAR CURSO
            print("\n[PASSO 6] ACESSANDO CURSO")
            current_url = self.driver.current_url
            if not self._acessar_curso(curso):
                self.fail("FALHA: Erro ao tentar acessar o curso encontrado.")

            # Verificar se ao acessar o curso apareceu prompt de PIN
            time.sleep(0.7)
            if self._detectar_modal_pin():
                self.fail("FALHA: Ao tentar acessar o curso, apareceu prompt solicitando PIN.")

            # PASSO 7: VALIDAR ACESSO
            time.sleep(1)
            new_url = self.driver.current_url
            save_screenshot(self.driver, self.test_name, "05_apos_acesso_curso")

            # Validação heurística: URL mudou e não voltou para home, ou existe elemento de conteúdo do curso
            if new_url != current_url and new_url != url_base:
                print(f"✓ Acesso realizado - nova URL: {new_url}")
            else:
                # tentar verificar conteúdo de curso (ex: presença de título, aulas ou player)
                try:
                    possible_content = self.driver.find_elements(By.XPATH, "//h1|//h2|//iframe[contains(@src,'youtube')]|//*[contains(@class,'course') or contains(@class,'aula')]")
                    visible = any((el.is_displayed() for el in possible_content))
                    if visible:
                        print("✓ Acesso realizado - conteúdo do curso visível")
                    else:
                        self.fail("FALHA: Não foi possível validar acesso ao curso (URL inalterada e conteúdo não visível).")
                except Exception:
                    self.fail("FALHA: Não foi possível validar acesso ao curso após clique.")

            print("\n" + "="*60)
            print("TESTE RF43: Concluído com sucesso")
            print("="*60 + "\n")

        except AssertionError as e:
            print(f"\n✗ Teste falhou com asserção: {e}")
            traceback.print_exc()
            raise
        except Exception as e:
            print(f"\n✗ Erro inesperado no teste: {e}")
            traceback.print_exc()
            self.fail(f"Erro inesperado: {e}")


if __name__ == '__main__':
    unittest.main()
