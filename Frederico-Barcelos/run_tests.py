import tkinter as tk
from tkinter import ttk, scrolledtext
import unittest
import sys
import os
import re
import threading
from io import StringIO
try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None
    print("AVISO: A biblioteca 'Pillow' não está instalada. As funcionalidades de visualização de screenshots não estarão disponíveis.")
    print("Para instalar, execute: pip install Pillow")

class TextRedirector(StringIO):
    """Um objeto 'file-like' para redirecionar o output para um widget de texto do Tkinter."""
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def write(self, string):
        # Garante que a atualização do widget seja feita na thread principal do Tkinter
        self.widget.after(0, self._insert_text, string)

    def _insert_text(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)

    def flush(self):
        pass

class TestRunnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Executor de Testes")
        self.root.geometry("800x600")

        # Define o diretório fixo para a descoberta de testes
        self.TEST_DIRECTORY = r'C:\Users\fre12\OneDrive\Documentos\GitHub\codefolio-test\Frederico-Barcelos'
        
        # Adiciona o diretório de testes ao path para encontrar módulos locais
        sys.path.insert(0, self.TEST_DIRECTORY)

        # --- Widgets ---
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para os controles
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=5)

        ttk.Label(controls_frame, text="Selecionar Teste:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.test_combobox = ttk.Combobox(controls_frame, state="readonly", width=50)
        self.test_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.run_selected_button = ttk.Button(controls_frame, text="Rodar Selecionado", command=self.on_run_selected)
        self.run_selected_button.pack(side=tk.LEFT, padx=5)

        self.run_all_button = ttk.Button(controls_frame, text="Rodar Todos", command=self.on_run_all)
        self.run_all_button.pack(side=tk.LEFT, padx=5)

        self.refresh_screenshots_button = ttk.Button(controls_frame, text="Atualizar Screenshots", command=self.on_refresh_screenshots)
        self.refresh_screenshots_button.pack(side=tk.LEFT, padx=5)

        self.headless_var = tk.BooleanVar()
        headless_check = ttk.Checkbutton(controls_frame, text="Rodar em modo Headless", variable=self.headless_var)
        headless_check.pack(side=tk.LEFT, padx=15)

        # Terminal
        # self.terminal = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, bg="black", fg="white", font=("Consolas", 12))
        # self.terminal.pack(fill=tk.BOTH, expand=True, pady=5)

        # PanedWindow para terminal e visualizador de screenshots
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, pady=5)

        # Frame para o terminal
        terminal_frame = ttk.Frame(paned_window)
        paned_window.add(terminal_frame, weight=1)
        self.terminal = scrolledtext.ScrolledText(terminal_frame, wrap=tk.WORD, bg="black", fg="white", font=("Consolas", 12))
        self.terminal.pack(fill=tk.BOTH, expand=True)

        # Frame para o visualizador de screenshots
        screenshot_viewer_frame = ttk.Frame(paned_window)
        paned_window.add(screenshot_viewer_frame, weight=1)

        ttk.Label(screenshot_viewer_frame, text="Screenshots do Teste:").pack(pady=(0, 5))
        self.screenshot_listbox = tk.Listbox(screenshot_viewer_frame, height=10)
        self.screenshot_listbox.pack(fill=tk.X, pady=(0, 5))
        self.screenshot_listbox.bind('<<ListboxSelect>>', self.on_screenshot_select)

        self.screenshot_label = ttk.Label(screenshot_viewer_frame)
        self.screenshot_label.pack(fill=tk.BOTH, expand=True)
        self.current_test_screenshots = [] # Para armazenar os caminhos completos dos screenshots

    def on_refresh_screenshots(self):
        """Recarrega a lista de screenshots para o teste selecionado na combobox."""
        display_name = self.test_combobox.get()
        if display_name and display_name in self.test_map:
            full_id = self.test_map[display_name]
            self.load_screenshots_for_test(full_id)
        else:
            print("Nenhum teste válido selecionado para atualizar os screenshots.")

        self.load_tests()

    def _get_test_map(self, suite):
        """Extrai um mapa de {nome_exibicao: id_completo} de uma TestSuite."""
        test_map = {}
        if hasattr(suite, '__iter__'):
            for test in suite:
                test_map.update(self._get_test_map(test))
        else:
            full_id = suite.id()
            method_name = full_id.split('.')[-1]
            
            # Cria o nome de exibição formatado
            display_name = re.sub(r'^test_\d+_', '', method_name).replace('_', ' ').capitalize()
            
            # Adiciona o mapeamento do nome amigável para o ID completo
            test_map[display_name] = full_id
        return test_map

    def load_tests(self):
        """Descobre e carrega os testes, criando um mapa de nomes amigáveis."""
        loader = unittest.TestLoader()
        self.full_suite = loader.discover(self.TEST_DIRECTORY)
        
        self.test_map = self._get_test_map(self.full_suite)
        test_names = sorted(self.test_map.keys()) # Ordena para uma exibição consistente
        
        if test_names:
            self.test_combobox['values'] = test_names
            self.test_combobox.current(0)
        else:
            self.test_combobox['values'] = ["Nenhum teste encontrado"]
            self.test_combobox.current(0)
            self.run_selected_button.config(state=tk.DISABLED)
            self.run_all_button.config(state=tk.DISABLED)

    def run_tests_in_thread(self, suite):
        """Inicia a execução dos testes em uma nova thread para não bloquear a GUI."""
        self.run_selected_button.config(state=tk.DISABLED)
        self.run_all_button.config(state=tk.DISABLED)
        self.terminal.delete('1.0', tk.END)

        thread = threading.Thread(target=self.execute_tests, args=(suite,))
        thread.start()
        self.check_thread(thread)

    def check_thread(self, thread):
        """Verifica se a thread de testes terminou e reativa os botões."""
        if thread.is_alive():
            self.root.after(100, lambda: self.check_thread(thread))
        else:
            self.run_selected_button.config(state=tk.NORMAL)
            self.run_all_button.config(state=tk.NORMAL)

    def execute_tests(self, suite):
        """Executa a suíte de testes e redireciona o output para o terminal da GUI."""
        if self.headless_var.get():
            os.environ['HEADLESS_MODE'] = '1'
        elif 'HEADLESS_MODE' in os.environ:
            del os.environ['HEADLESS_MODE']

        redirector = TextRedirector(self.terminal)
        
        # Salva o stdout e stderr originais
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        
        # Redireciona
        sys.stdout = redirector
        sys.stderr = redirector
        
        try:
            runner = unittest.TextTestRunner(stream=redirector, verbosity=2)
            result = runner.run(suite)

            # Adiciona um resumo de falhas e erros no final
            if not result.wasSuccessful():
                self.terminal.after(0, redirector._insert_text, "\n\n--- RESUMO DAS FALHAS ---\n")
                for test, err in result.errors:
                    self.terminal.after(0, redirector._insert_text, f"ERRO em: {test.id()}\n")
                for test, err in result.failures:
                    self.terminal.after(0, redirector._insert_text, f"FALHA em: {test.id()}\n")
        finally:
            # Restaura o stdout e stderr
            sys.stdout = original_stdout
            sys.stderr = original_stderr

    def on_run_selected(self):
        """Callback para o botão 'Rodar Selecionado'."""
        display_name = self.test_combobox.get()
        if display_name and display_name != "Nenhum teste encontrado":
            # Usa o mapa para encontrar o ID completo do teste a partir do nome de exibição
            full_id = self.test_map[display_name]
            
            suite = unittest.TestSuite()
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(full_id))
            self.run_tests_in_thread(suite)
            # Após a execução, carrega os screenshots para o teste que acabou de rodar
            self.load_screenshots_for_test(full_id)

    def on_run_all(self):
        """Callback para o botão 'Rodar Todos'."""
        self.run_tests_in_thread(self.full_suite)
        # Limpa o visualizador de screenshots ao rodar todos os testes
        self.screenshot_listbox.delete(0, tk.END)
        self.screenshot_label.config(image='')
        self.screenshot_label.image = None
        self.current_test_screenshots = []

    def on_screenshot_select(self, event):
        """Callback quando um screenshot é selecionado na lista."""
        if not self.screenshot_listbox.curselection():
            return
        
        index = self.screenshot_listbox.curselection()[0]
        file_path = self.current_test_screenshots[index]
        self.display_screenshot(file_path)

    def load_screenshots_for_test(self, test_id):
        """Carrega os screenshots de um teste específico e popula a listbox."""
        self.screenshot_listbox.delete(0, tk.END)
        self.screenshot_label.config(image='') # Limpa a imagem atual
        self.screenshot_label.image = None # Evita que a imagem seja coletada pelo GC
        self.current_test_screenshots = []

        if Image is None or ImageTk is None:
            self.screenshot_listbox.insert(tk.END, "Pillow não instalado. Screenshots desabilitados.")
            return

        test_name = test_id.split('.')[-1]
        screenshot_dir = os.path.join('test_screenshots', test_name)

        if os.path.exists(screenshot_dir):
            screenshots = sorted([f for f in os.listdir(screenshot_dir) if f.endswith('.png')])
            for i, filename in enumerate(screenshots):
                full_path = os.path.join(screenshot_dir, filename)
                self.current_test_screenshots.append(full_path)
                self.screenshot_listbox.insert(tk.END, filename)
            if screenshots:
                self.screenshot_listbox.selection_set(0)
                self.on_screenshot_select(None) # Exibe o primeiro screenshot
        else:
            self.screenshot_listbox.insert(tk.END, "Nenhum screenshot encontrado para este teste.")

    def display_screenshot(self, file_path):
        """Exibe um screenshot no label."""
        if not os.path.exists(file_path):
            return

        img = Image.open(file_path)
        
        # Redimensiona a imagem para caber no label, mantendo a proporção
        label_width = self.screenshot_label.winfo_width()
        label_height = self.screenshot_label.winfo_height()
        
        if label_width == 1 or label_height == 1: # Default size before widget is drawn
            label_width = 400 # Fallback default size
            label_height = 300

        img_width, img_height = img.size
        
        if img_width > label_width or img_height > label_height:
            ratio = min(label_width / img_width, label_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            img = img.resize((new_width, new_height), Image.LANCZOS)
        
        photo = ImageTk.PhotoImage(img)
        self.screenshot_label.config(image=photo)
        self.screenshot_label.image = photo # Keep a reference!

if __name__ == "__main__":
    root = tk.Tk()
    app = TestRunnerApp(root)
    root.mainloop()