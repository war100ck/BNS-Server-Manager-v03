import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import subprocess
import os
import json
import time
import threading
from datetime import datetime
import sys

# Проверка наличия pywin32
try:
    import win32con
    import win32gui
    import win32process
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False
    print("Warning: pywin32 not installed. Window minimization features disabled.")
    print("Install: pip install pywin32")

# ==================== МНОГОЯЗЫЧНЫЕ СТРОКИ (УПРОЩЕННЫЕ) ====================
LANGUAGES = {
    "ru": {
        "window_title": "BNS Менеджер Серверов",
        "file_menu": "Файл",
        "settings_menu": "Настройки",
        "manage_menu": "Управление",
        "language_menu": "Язык",
        "help_menu": "Помощь",
        
        "save_config": "Сохранить конфигурацию",
        "load_config": "Загрузить конфигурацию",
        "exit": "Выход",
        
        "change_server_path": "Изменить путь к серверам",
        "add_daemon": "Добавить демон",
        "edit_daemon": "Редактировать демон",
        
        "start_all": "Запуск всех",
        "stop_all": "Остановить все",
        "check_status": "Проверить статус",
        "start_selected": "Запуск выбранных",
        "stop_selected": "Остановить выбранные",
        
        "russian": "Русский",
        "english": "English",
        "portuguese": "Português (Brasil)",
        
        "about": "О программе",
        
        "add_btn": "➕ Добавить",
        "edit_btn": "✏️ Редактировать",
        "delete_btn": "🗑️ Удалить",
        "move_up_btn": "↑ Вверх",
        "move_down_btn": "↓ Вниз",
        "start_all_btn": "▶ Запуск всех",
        "stop_all_btn": "⏹ Остановить все",
        "check_btn": "🔄 Проверить",
        "settings_btn": "⚙️ Настройки",
        
        "daemons_frame": "Демоны",
        "quick_launch_frame": "Быстрый запуск",
        "log_frame": "Лог выполнения",
        
        "start_selected_btn": "▶ Запуск выбранного",
        "stop_selected_btn": "⏹ Остановить выбранный",
        "restart_btn": "🔄 Перезапустить",
        
        "ready": "Готов",
        "running": "✅ Работает",
        "stopped": "❌ Остановлен",
        "crashed": "⚠ Упал",
        
        "config_saved": "Конфигурация сохранена",
        "config_loaded": "Конфигурация загружена",
        "daemon_added": "Демон '{name}' добавлен",
        "daemon_updated": "Демон '{name}' обновлен",
        "daemon_deleted": "Демон '{name}' удален",
        "daemon_moved_up": "Демон '{name}' перемещен вверх",
        "daemon_moved_down": "Демон '{name}' перемещен вниз",
        "daemon_started": "✅ {name} запущен (PID: {pid})",
        "daemon_stopped": "⏹ {name} остановлен",
        "daemon_force_stopped": "⚠ {name} принудительно остановлен",
        "daemon_crashed": "⚠ ВНИМАНИЕ: {name} неожиданно завершился!",
        "starting_all": "Запуск всех включенных демонов...",
        "all_started": "Все демоны запущены",
        "stopping_all": "Остановка всех демонов...",
        "all_stopped": "Все демоны остановлены",
        "checking_status": "Проверка статуса...",
        "status_checked": "Проверка статуса завершена",
        "log_cleared": "Лог очищен",
        
        "select_daemon": "Выберите демон",
        "daemon_disabled": "Демон отключен",
        "confirm_delete": "Удалить демон '{name}'?",
        "no_daemons": "Демоны не настроены",
        "ask_add_now": "Хотите добавить сейчас?",
        "server_path_not_found": "Папка с серверами не найдена!",
        "select_server_path": "Выберите папку с серверами BNS",
        "exe_file_not_found": "Укажите правильный путь к .exe файлу",
        "enter_daemon_name": "Введите название демона",
        "autodetect_no_daemons": "Демоны не найдены",
        "autodetect_found": "Добавлено {count} демонов",
        "about_title": "О программе",
        "about_text": "BNS Server Manager v3.0\n\nУправление серверами Blade & Soul\nПоддержка: Русский, English, Português\n\nФункции:\n• Добавление/редактирование демонов\n• Запуск/остановка всех или выбранных\n• Изменение порядка запуска\n• Автоопределение демонов\n• Запуск свернутыми (требует pywin32)\n• Многоязычный интерфейс\n\n Автор: WAR100CK",
        
        "log_starting": "Запуск: {name}",
        "log_file_not_found": "❌ Файл не найден: {path}",
        "log_error_starting": "❌ Ошибка запуска {name}: {error}",
        "log_error_stopping": "❌ Ошибка остановки {name}: {error}",
        "log_autodetect": "Автоопределение демонов...",
        "log_server_path_set": "Путь к серверам установлен: {path}",
        
        "tree_name": "Название",
        "tree_status": "Статус",
        "tree_path": "Путь",
        "tree_delay": "Задержка",
        
        "cm_stop": "⏹ Остановить",
        "cm_restart": "🔄 Перезапустить",
        "cm_start": "▶ Запустить",
        "cm_edit": "✏️ Редактировать",
        "cm_delete": "🗑️ Удалить",
        "cm_move_up": "↑ Вверх",
        "cm_move_down": "↓ Вниз",
        "cm_copy_path": "📋 Копировать путь",
        
        "add_title": "Добавить демон",
        "edit_title": "Редактировать демон",
        "name_label": "Название демона:",
        "path_label": "Путь к .exe файлу:",
        "delay_label": "Задержка запуска (сек):",
        "enabled_label": "Включен",
        "browse_btn": "Обзор",
        "add_btn_dialog": "Добавить",
        "autodetect_btn": "Автоопределение",
        "save_btn": "Сохранить",
        "cancel_btn": "Отмена",
        
        "status_running": "Работает: {running}/{total}",
        
        "settings_title": "Настройки",
        "settings_text": "Настройки сохранены в config.json\nИзменить путь: Настройки → Изменить путь к серверам",
        
        # Управление окнами (скрытые функции)
        "minimize_all": "Свернуть все",
        "show_all": "Показать все",
        "window_settings": "Свернуть при запуске",
        "minimize_selected": "Свернуть выбранные",
        "show_selected": "Показать выбранные",
        "all_minimized": "Все окна свернуты",
        "all_shown": "Все окна показаны",
        "minimized_selected": "Выбранные окна свернуты",
        "shown_selected": "Выбранные окна показаны",
        "win32_required": "Для управления окнами требуется pywin32\nУстановите: pip install pywin32",
        "start_minimized": "Запускать свернутыми",
        "minimize_on_start": "Свернуть окно при запуске",
    },
    
    "en": {
        "window_title": "BNS Server Manager",
        "file_menu": "File",
        "settings_menu": "Settings",
        "manage_menu": "Manage",
        "language_menu": "Language",
        "help_menu": "Help",
        
        "save_config": "Save Configuration",
        "load_config": "Load Configuration",
        "exit": "Exit",
        
        "change_server_path": "Change Server Path",
        "add_daemon": "Add Daemon",
        "edit_daemon": "Edit Daemon",
        
        "start_all": "Start All",
        "stop_all": "Stop All",
        "check_status": "Check Status",
        "start_selected": "Start Selected",
        "stop_selected": "Stop Selected",
        
        "russian": "Русский",
        "english": "English",
        "portuguese": "Português (Brasil)",
        
        "about": "About",
        
        "add_btn": "➕ Add",
        "edit_btn": "✏️ Edit",
        "delete_btn": "🗑️ Delete",
        "move_up_btn": "↑ Move Up",
        "move_down_btn": "↓ Move Down",
        "start_all_btn": "▶ Start All",
        "stop_all_btn": "⏹ Stop All",
        "check_btn": "🔄 Check",
        "settings_btn": "⚙️ Settings",
        
        "daemons_frame": "Daemons",
        "quick_launch_frame": "Quick Launch",
        "log_frame": "Execution Log",
        
        "start_selected_btn": "▶ Start Selected",
        "stop_selected_btn": "⏹ Stop Selected",
        "restart_btn": "🔄 Restart",
        
        "ready": "Ready",
        "running": "✅ Running",
        "stopped": "❌ Stopped",
        "crashed": "⚠ Crashed",
        
        "config_saved": "Configuration saved",
        "config_loaded": "Configuration loaded",
        "daemon_added": "Daemon '{name}' added",
        "daemon_updated": "Daemon '{name}' updated",
        "daemon_deleted": "Daemon '{name}' deleted",
        "daemon_moved_up": "Daemon '{name}' moved up",
        "daemon_moved_down": "Daemon '{name}' moved down",
        "daemon_started": "✅ {name} started (PID: {pid})",
        "daemon_stopped": "⏹ {name} stopped",
        "daemon_force_stopped": "⚠ {name} force stopped",
        "daemon_crashed": "⚠ WARNING: {name} crashed unexpectedly!",
        "starting_all": "Starting all enabled daemons...",
        "all_started": "All daemons started",
        "stopping_all": "Stopping all daemons...",
        "all_stopped": "All daemons stopped",
        "checking_status": "Checking status...",
        "status_checked": "Status check completed",
        "log_cleared": "Log cleared",
        
        "select_daemon": "Select a daemon",
        "daemon_disabled": "Daemon is disabled",
        "confirm_delete": "Delete daemon '{name}'?",
        "no_daemons": "No daemons configured",
        "ask_add_now": "Add now?",
        "server_path_not_found": "Server folder not found!",
        "select_server_path": "Select BNS server folder",
        "exe_file_not_found": "Specify correct path to .exe file",
        "enter_daemon_name": "Enter daemon name",
        "autodetect_no_daemons": "No daemons found",
        "autodetect_found": "Added {count} daemons",
        "about_title": "About",
        "about_text": "BNS Server Manager v3.0\n\nBlade & Soul Server Management\nLanguages: Русский, English, Português\n\nFeatures:\n• Add/edit daemons\n• Start/stop all or selected\n• Change startup order\n• Auto-detect daemons\n• Start minimized (requires pywin32)\n• Multi-language interface\n• Configuration saving\n\n Author: WAR100CK",
        
        "log_starting": "Starting: {name}",
        "log_file_not_found": "❌ File not found: {path}",
        "log_error_starting": "❌ Error starting {name}: {error}",
        "log_error_stopping": "❌ Error stopping {name}: {error}",
        "log_autodetect": "Auto-detecting daemons...",
        "log_server_path_set": "Server path set: {path}",
        
        "tree_name": "Name",
        "tree_status": "Status",
        "tree_path": "Path",
        "tree_delay": "Delay",
        
        "cm_stop": "⏹ Stop",
        "cm_restart": "🔄 Restart",
        "cm_start": "▶ Start",
        "cm_edit": "✏️ Edit",
        "cm_delete": "🗑️ Delete",
        "cm_move_up": "↑ Move Up",
        "cm_move_down": "↓ Move Down",
        "cm_copy_path": "📋 Copy path",
        
        "add_title": "Add Daemon",
        "edit_title": "Edit Daemon",
        "name_label": "Daemon name:",
        "path_label": "Path to .exe file:",
        "delay_label": "Start delay (sec):",
        "enabled_label": "Enabled",
        "browse_btn": "Browse",
        "add_btn_dialog": "Add",
        "autodetect_btn": "Auto-detect",
        "save_btn": "Save",
        "cancel_btn": "Cancel",
        
        "status_running": "Running: {running}/{total}",
        
        "settings_title": "Settings",
        "settings_text": "Settings saved in config.json\nChange path: Settings → Change Server Path",
        
        # Window management (hidden functions)
        "minimize_all": "Minimize all",
        "show_all": "Show all",
        "window_settings": "Minimize on start",
        "minimize_selected": "Minimize selected",
        "show_selected": "Show selected",
        "all_minimized": "All windows minimized",
        "all_shown": "All windows shown",
        "minimized_selected": "Selected windows minimized",
        "shown_selected": "Selected windows shown",
        "win32_required": "pywin32 required for window management\nInstall: pip install pywin32",
        "start_minimized": "Start minimized",
        "minimize_on_start": "Minimize window on start",
    },
    
    "pt": {
        "window_title": "Gerenciador de Servidores BNS",
        "file_menu": "Arquivo",
        "settings_menu": "Configurações",
        "manage_menu": "Gerenciar",
        "language_menu": "Idioma",
        "help_menu": "Ajuda",
        
        "save_config": "Salvar Configuração",
        "load_config": "Carregar Configuração",
        "exit": "Sair",
        
        "change_server_path": "Alterar Caminho dos Servidores",
        "add_daemon": "Adicionar Daemon",
        "edit_daemon": "Editar Daemon",
        
        "start_all": "Iniciar Todos",
        "stop_all": "Parar Todos",
        "check_status": "Verificar Status",
        "start_selected": "Iniciar Selecionados",
        "stop_selected": "Parar Selecionados",
        
        "russian": "Russo",
        "english": "Inglês",
        "portuguese": "Português (Brasil)",
        
        "about": "Sobre",
        
        "add_btn": "➕ Adicionar",
        "edit_btn": "✏️ Editar",
        "delete_btn": "🗑️ Excluir",
        "move_up_btn": "↑ Mover para Cima",
        "move_down_btn": "↓ Mover para Baixo",
        "start_all_btn": "▶ Iniciar Todos",
        "stop_all_btn": "⏹ Parar Todos",
        "check_btn": "🔄 Verificar",
        "settings_btn": "⚙️ Configurações",
        
        "daemons_frame": "Daemons",
        "quick_launch_frame": "Início Rápido",
        "log_frame": "Log de Execução",
        
        "start_selected_btn": "▶ Iniciar Selecionado",
        "stop_selected_btn": "⏹ Parar Selecionado",
        "restart_btn": "🔄 Reiniciar",
        
        "ready": "Pronto",
        "running": "✅ Executando",
        "stopped": "❌ Parado",
        "crashed": "⚠ Caiu",
        
        "config_saved": "Configuração salva",
        "config_loaded": "Configuração carregada",
        "daemon_added": "Daemon '{name}' adicionado",
        "daemon_updated": "Daemon '{name}' atualizado",
        "daemon_deleted": "Daemon '{name}' excluído",
        "daemon_moved_up": "Daemon '{name}' movido para cima",
        "daemon_moved_down": "Daemon '{name}' movido para baixo",
        "daemon_started": "✅ {name} iniciado (PID: {pid})",
        "daemon_stopped": "⏹ {name} parado",
        "daemon_force_stopped": "⚠ {name} forçado a parar",
        "daemon_crashed": "⚠ ATENÇÃO: {name} encerrou inesperadamente!",
        "starting_all": "Iniciando todos os daemons ativados...",
        "all_started": "Todos os daemons iniciados",
        "stopping_all": "Parando todos os daemons...",
        "all_stopped": "Todos os daemons parados",
        "checking_status": "Verificando status...",
        "status_checked": "Verificação de status concluída",
        "log_cleared": "Log limpo",
        
        "select_daemon": "Selecione um daemon",
        "daemon_disabled": "Daemon desativado",
        "confirm_delete": "Excluir daemon '{name}'?",
        "no_daemons": "Nenhum daemon configurado",
        "ask_add_now": "Adicionar agora?",
        "server_path_not_found": "Pasta do servidor não encontrada!",
        "select_server_path": "Selecione a pasta do servidor BNS",
        "exe_file_not_found": "Especifique o caminho correto para o arquivo .exe",
        "enter_daemon_name": "Digite o nome do daemon",
        "autodetect_no_daemons": "Nenhum daemon encontrado",
        "autodetect_found": "{count} daemons adicionados",
        "about_title": "Sobre",
        "about_text": "BNS Server Manager v3.0\n\nGerenciamento de Servidores Blade & Soul\nIdiomas: Russo, Inglês, Português\n\nRecursos:\n• Adicionar/editar daemons\n• Iniciar/parar todos ou selecionados\n• Alterar ordem de inicialização\n• Auto-detectar daemons\n• Iniciar minimizado (requer pywin32)\n• Interface multilíngue\n• Salvar configuração\n\n Autor: WAR100CK",
        
        "log_starting": "Iniciando: {name}",
        "log_file_not_found": "❌ Arquivo não encontrado: {path}",
        "log_error_starting": "❌ Erro ao iniciar {name}: {error}",
        "log_error_stopping": "❌ Erro ao parar {name}: {error}",
        "log_autodetect": "Detectando daemons automaticamente...",
        "log_server_path_set": "Caminho do servidor definido: {path}",
        
        "tree_name": "Nome",
        "tree_status": "Status",
        "tree_path": "Caminho",
        "tree_delay": "Atraso",
        
        "cm_stop": "⏹ Parar",
        "cm_restart": "🔄 Reiniciar",
        "cm_start": "▶ Iniciar",
        "cm_edit": "✏️ Editar",
        "cm_delete": "🗑️ Excluir",
        "cm_move_up": "↑ Mover para Cima",
        "cm_move_down": "↓ Mover para Baixo",
        "cm_copy_path": "📋 Copiar caminho",
        
        "add_title": "Adicionar Daemon",
        "edit_title": "Editar Daemon",
        "name_label": "Nome do daemon:",
        "path_label": "Caminho para arquivo .exe:",
        "delay_label": "Atraso de início (seg):",
        "enabled_label": "Ativado",
        "browse_btn": "Procurar",
        "add_btn_dialog": "Adicionar",
        "autodetect_btn": "Auto-detectar",
        "save_btn": "Salvar",
        "cancel_btn": "Cancelar",
        
        "status_running": "Executando: {running}/{total}",
        
        "settings_title": "Configurações",
        "settings_text": "Configurações salvas em config.json\nAlterar caminho: Configurações → Alterar Caminho dos Servidores",
        
        # Gerenciamento de janelas (funções ocultas)
        "minimize_all": "Minimizar todos",
        "show_all": "Mostrar todos",
        "window_settings": "Minimizar ao iniciar",
        "minimize_selected": "Minimizar selecionados",
        "show_selected": "Mostrar selecionados",
        "all_minimized": "Todas as janelas minimizadas",
        "all_shown": "Todas as janelas mostradas",
        "minimized_selected": "Janelas selecionadas minimizadas",
        "shown_selected": "Janelas selecionadas mostradas",
        "win32_required": "pywin32 necessário para gerenciamento de janelas\nInstale: pip install pywin32",
        "start_minimized": "Iniciar minimizado",
        "minimize_on_start": "Minimizar janela ao iniciar",
    }
}

# ==================== КЛАСС МЕНЕДЖЕРА КОНФИГУРАЦИИ ====================
class BNSConfigManager:
    CONFIG_FILE = "bns_config.json"
    
    def __init__(self):
        self.config = self.load_config()
        
    def load_config(self):
        """Загрузка конфигурации из файла"""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    defaults = {
                        "language": "ru",
                        "server_path": "",
                        "window_position": None,
                        "start_minimized": False,
                        "daemons": []
                    }
                    
                    for key, value in defaults.items():
                        if key not in config:
                            config[key] = value
                    
                    return config
            except Exception as e:
                print(f"Error loading config: {e}")
                pass
        
        # Конфигурация по умолчанию
        return {
            "language": "ru",
            "server_path": "",
            "window_position": None,
            "start_minimized": False,
            "daemons": []
        }
    
    def save_config(self):
        """Сохранение конфигурации в файл"""
        with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def add_daemon(self, name, exe_path, delay=2, enabled=True, start_minimized=False):
        """Добавление нового демона в конфигурацию"""
        daemon = {
            "name": name,
            "exe_path": exe_path,
            "delay": delay,
            "enabled": enabled,
            "start_minimized": start_minimized,
            "working_dir": os.path.dirname(exe_path)
        }
        self.config["daemons"].append(daemon)
        self.save_config()
    
    def insert_daemon(self, index, name, exe_path, delay=2, enabled=True, start_minimized=False):
        """Вставка демона на конкретную позицию"""
        daemon = {
            "name": name,
            "exe_path": exe_path,
            "delay": delay,
            "enabled": enabled,
            "start_minimized": start_minimized,
            "working_dir": os.path.dirname(exe_path)
        }
        self.config["daemons"].insert(index, daemon)
        self.save_config()
    
    def update_daemon(self, index, name=None, exe_path=None, delay=None, enabled=None, start_minimized=None):
        """Обновление демона"""
        if 0 <= index < len(self.config["daemons"]):
            daemon = self.config["daemons"][index]
            if name is not None:
                daemon["name"] = name
            if exe_path is not None:
                daemon["exe_path"] = exe_path
                daemon["working_dir"] = os.path.dirname(exe_path)
            if delay is not None:
                daemon["delay"] = delay
            if enabled is not None:
                daemon["enabled"] = enabled
            if start_minimized is not None:
                daemon["start_minimized"] = start_minimized
            self.save_config()
    
    def remove_daemon(self, index):
        """Удаление демона"""
        if 0 <= index < len(self.config["daemons"]):
            del self.config["daemons"][index]
            self.save_config()
    
    def move_daemon_up(self, index):
        """Перемещение демона вверх"""
        if 0 < index < len(self.config["daemons"]):
            self.config["daemons"][index], self.config["daemons"][index-1] = \
                self.config["daemons"][index-1], self.config["daemons"][index]
            self.save_config()
            return True
        return False
    
    def move_daemon_down(self, index):
        """Перемещение демона вниз"""
        if 0 <= index < len(self.config["daemons"]) - 1:
            self.config["daemons"][index], self.config["daemons"][index+1] = \
                self.config["daemons"][index+1], self.config["daemons"][index]
            self.save_config()
            return True
        return False
    
    def get_daemons(self):
        """Получение списка демонов"""
        return self.config["daemons"]
    
    def set_language(self, lang_code):
        """Установка языка"""
        if lang_code in LANGUAGES:
            self.config["language"] = lang_code
            self.save_config()
            return True
        return False
    
    def get_language(self):
        """Получение текущего языка"""
        return self.config.get("language", "ru")
    
    def set_start_minimized(self, value):
        """Установка запуска свернутыми по умолчанию"""
        self.config["start_minimized"] = value
        self.save_config()
        return True
    
    def get_start_minimized(self):
        """Получение настройки запуска свернутыми"""
        return self.config.get("start_minimized", False)

# ==================== ОСНОВНОЙ КЛАСС ПРИЛОЖЕНИЯ ====================
class BNSManagerApp:
    def __init__(self, root):
        self.root = root
        self.config_manager = BNSConfigManager()
        self.processes = {}
        self.current_lang = self.config_manager.get_language()
        self.tr = LANGUAGES[self.current_lang]
        
        # Загрузка иконки
        self.load_window_icon()
        
        self.setup_window()
        self.setup_ui()
        self.check_initial_config()
        
        self.auto_check_status()
    
    def load_window_icon(self):
        """Загрузка иконки окна"""
        icon_paths = [
            "icon.png",
            "icon.ico",
            os.path.join(os.path.dirname(__file__), "icon.png"),
            os.path.join(os.path.dirname(__file__), "icon.ico"),
            "C:\\BNS-Server\\Servers\\icon.png",
            "C:\\BNS-Server\\icon.png",
        ]
        
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                try:
                    if icon_path.endswith('.ico'):
                        self.root.iconbitmap(icon_path)
                    elif icon_path.endswith('.png'):
                        # Для PNG используем PhotoImage
                        icon = tk.PhotoImage(file=icon_path)
                        self.root.iconphoto(True, icon)
                        # Сохраняем ссылку, чтобы не удалилась сборщиком мусора
                        self.icon = icon
                    print(f"Icon loaded from: {icon_path}")
                    break
                except Exception as e:
                    print(f"Failed to load icon {icon_path}: {e}")
    
    def t(self, key, **kwargs):
        """Функция перевода"""
        text = self.tr.get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except:
                return text
        return text
    
    def setup_window(self):
        """Настройка главного окна"""
        self.root.title(self.t("window_title"))
        self.root.geometry("1325x650")
        
        self.center_window(self.root)
    
    def center_window(self, window):
        """Центрирование окна"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Создание интерфейса"""
        self.create_menu()
        self.create_toolbar()
        self.create_main_frames()
        self.create_status_bar()
    
    def create_menu(self):
        """Создание меню"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.t("file_menu"), menu=file_menu)
        file_menu.add_command(label=self.t("save_config"), command=self.save_config)
        file_menu.add_command(label=self.t("load_config"), command=self.load_config)
        file_menu.add_separator()
        file_menu.add_command(label=self.t("exit"), command=self.root.quit)
        
        # Меню Настройки
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.t("settings_menu"), menu=settings_menu)
        settings_menu.add_command(label=self.t("change_server_path"), 
                                 command=self.change_server_path)
        settings_menu.add_command(label=self.t("add_daemon"), 
                                 command=self.add_daemon_dialog)
        
        # Меню Управление
        manage_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.t("manage_menu"), menu=manage_menu)
        manage_menu.add_command(label=self.t("start_all"), command=self.start_all)
        manage_menu.add_command(label=self.t("stop_all"), command=self.stop_all)
        manage_menu.add_command(label=self.t("check_status"), command=self.check_all_status)
        if HAS_WIN32:
            manage_menu.add_separator()
            manage_menu.add_command(label=self.t("minimize_all"), 
                                  command=self.minimize_all_windows)
            manage_menu.add_command(label=self.t("show_all"), 
                                  command=self.show_all_windows)
        
        # Меню Язык
        language_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.t("language_menu"), menu=language_menu)
        language_menu.add_command(label=self.t("russian"), 
                                 command=lambda: self.change_language("ru"))
        language_menu.add_command(label=self.t("english"), 
                                 command=lambda: self.change_language("en"))
        language_menu.add_command(label=self.t("portuguese"), 
                                 command=lambda: self.change_language("pt"))
        
        # Меню Помощь
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.t("help_menu"), menu=help_menu)
        help_menu.add_command(label=self.t("about"), command=self.show_about)
    
    def create_toolbar(self):
        """Создание панели инструментов с кнопками перемещения"""
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Основные кнопки
        buttons = [
            (self.t("add_btn"), self.add_daemon_dialog),
            (self.t("edit_btn"), self.edit_daemon_dialog),
            (self.t("delete_btn"), self.delete_daemon),
            ("", None),
            (self.t("move_up_btn"), self.move_selected_up),
            (self.t("move_down_btn"), self.move_selected_down),
            ("", None),
            (self.t("start_all_btn"), self.start_all),
            (self.t("stop_all_btn"), self.stop_all),
            (self.t("check_btn"), self.check_all_status),
        ]
        
        if HAS_WIN32:
            buttons.extend([
                ("", None),
                ("🔽 " + self.t("minimize_all"), self.minimize_all_windows),
                ("🔼 " + self.t("show_all"), self.show_all_windows),
            ])
        
        for text, command in buttons:
            if text == "":
                sep = tk.Frame(toolbar, width=2, bg="gray", height=20)
                sep.pack(side=tk.LEFT, padx=2, pady=2)
            else:
                btn = tk.Button(toolbar, text=text, command=command)
                btn.pack(side=tk.LEFT, padx=2, pady=2)
    
    def create_main_frames(self):
        """Создание основных фреймов"""
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Левая панель
        left_frame = tk.LabelFrame(main_frame, text=self.t("daemons_frame"))
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.create_daemon_tree(left_frame)
        
        # Правая панель
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_quick_launch(right_frame)
        self.create_log_frame(right_frame)
    
    def create_daemon_tree(self, parent):
        """Создание дерева демонов"""
        columns = ("name", "status", "path", "delay")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", height=18)
        
        self.tree.heading("name", text=self.t("tree_name"))
        self.tree.heading("status", text=self.t("tree_status"))
        self.tree.heading("path", text=self.t("tree_path"))
        self.tree.heading("delay", text=self.t("tree_delay"))
        
        self.tree.column("name", width=200)
        self.tree.column("status", width=100)
        self.tree.column("path", width=450)
        self.tree.column("delay", width=80)
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<Double-1>", self.on_daemon_double_click)
        self.tree.bind("<Button-3>", self.show_context_menu)
    
    def create_quick_launch(self, parent):
        """Создание панели быстрого запуска"""
        quick_frame = tk.LabelFrame(parent, text=self.t("quick_launch_frame"))
        quick_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Первый ряд
        row1 = tk.Frame(quick_frame)
        row1.pack(fill=tk.X, pady=5)
        
        tk.Button(row1, text=self.t("start_selected_btn"), 
                 command=self.start_selected, bg="green", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(row1, text=self.t("stop_selected_btn"), 
                 command=self.stop_selected, bg="red", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(row1, text=self.t("restart_btn"), 
                 command=self.restart_selected, bg="blue", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Второй ряд (только если есть pywin32)
        if HAS_WIN32:
            row2 = tk.Frame(quick_frame)
            row2.pack(fill=tk.X, pady=5)
            
            tk.Button(row2, text="🔽 " + self.t("minimize_selected"), 
                     command=self.minimize_selected_windows, bg="orange", fg="white").pack(side=tk.LEFT, padx=5)
            tk.Button(row2, text="🔼 " + self.t("show_selected"), 
                     command=self.show_selected_windows, bg="purple", fg="white").pack(side=tk.LEFT, padx=5)
    
    def create_log_frame(self, parent):
        """Создание фрейма лога"""
        log_frame = tk.LabelFrame(parent, text=self.t("log_frame"))
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        log_buttons = tk.Frame(log_frame)
        log_buttons.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        tk.Button(log_buttons, text="🗑️", command=self.clear_log, width=3).pack(side=tk.RIGHT)
    
    def create_status_bar(self):
        """Создание статус-бара"""
        self.status_bar = tk.Label(self.root, text=self.t("ready"), 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    # ==================== ФУНКЦИИ ДЛЯ РАБОТЫ С ОКНАМИ ====================
    
    def minimize_window_by_pid(self, pid):
        """Сворачивание окна по PID"""
        if not HAS_WIN32:
            return False
            
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid:
                    hwnds.append(hwnd)
            return True
        
        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        
        for hwnd in hwnds:
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            return True
        
        return False
    
    def show_window_by_pid(self, pid):
        """Показ окна по PID"""
        if not HAS_WIN32:
            return False
            
        def callback(hwnd, hwnds):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
            return True
        
        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        
        for hwnd in hwnds:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            return True
        
        return False
    
    def minimize_all_windows(self):
        """Свернуть все окна демонов"""
        if not HAS_WIN32:
            messagebox.showwarning("Warning", self.t("win32_required"))
            return
            
        for daemon_name, process in self.processes.items():
            if process.poll() is None:
                self.minimize_window_by_pid(process.pid)
        
        self.log_message(self.t("all_minimized"), "success")
    
    def show_all_windows(self):
        """Показать все окна демонов"""
        if not HAS_WIN32:
            messagebox.showwarning("Warning", self.t("win32_required"))
            return
            
        for daemon_name, process in self.processes.items():
            if process.poll() is None:
                self.show_window_by_pid(process.pid)
        
        self.log_message(self.t("all_shown"), "success")
    
    def minimize_selected_windows(self):
        """Свернуть выбранные окна"""
        if not HAS_WIN32:
            messagebox.showwarning("Warning", self.t("win32_required"))
            return
            
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo(self.t("select_daemon"), self.t("select_daemon"))
            return
        
        for item in selection:
            daemon_name = self.tree.item(item)["values"][0]
            if daemon_name in self.processes:
                process = self.processes[daemon_name]
                if process.poll() is None:
                    self.minimize_window_by_pid(process.pid)
        
        self.log_message(self.t("minimized_selected"), "success")
    
    def show_selected_windows(self):
        """Показать выбранные окна"""
        if not HAS_WIN32:
            messagebox.showwarning("Warning", self.t("win32_required"))
            return
            
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo(self.t("select_daemon"), self.t("select_daemon"))
            return
        
        for item in selection:
            daemon_name = self.tree.item(item)["values"][0]
            if daemon_name in self.processes:
                process = self.processes[daemon_name]
                if process.poll() is None:
                    self.show_window_by_pid(process.pid)
        
        self.log_message(self.t("shown_selected"), "success")
    
    def start_daemon_with_window_mode(self, daemon):
        """Запуск демона с учетом настройки свернутого запуска"""
        try:
            exe_path = daemon["exe_path"]
            working_dir = daemon.get("working_dir", os.path.dirname(exe_path))
            start_minimized = daemon.get("start_minimized", False)
            
            if not os.path.exists(exe_path):
                self.log_message(self.t("log_file_not_found", path=exe_path), "error")
                return False
            
            self.log_message(f"Запуск: {daemon['name']}")
            
            # Флаги создания окна
            creation_flags = subprocess.CREATE_NEW_CONSOLE
            
            if start_minimized and HAS_WIN32:
                # Запуск с возможностью последующего сворачивания
                creation_flags = subprocess.CREATE_NEW_CONSOLE
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_SHOWMINIMIZED
                
                process = subprocess.Popen(
                    [exe_path],
                    cwd=working_dir,
                    creationflags=creation_flags,
                    startupinfo=startupinfo
                )
            else:
                # Обычный запуск
                process = subprocess.Popen(
                    [exe_path],
                    cwd=working_dir,
                    creationflags=creation_flags
                )
            
            self.processes[daemon["name"]] = process
            
            # Если нужно свернуть, делаем это через секунду
            if start_minimized and HAS_WIN32:
                threading.Thread(target=self.delayed_minimize, 
                               args=(process.pid,), daemon=True).start()
            
            self.log_message(self.t("daemon_started", name=daemon["name"], pid=process.pid), "success")
            
            self.refresh_daemon_list()
            return True
            
        except Exception as e:
            self.log_message(self.t("log_error_starting", name=daemon["name"], error=str(e)), "error")
            return False
    
    def delayed_minimize(self, pid, delay=1):
        """Отложенное сворачивание окна"""
        time.sleep(delay)
        self.minimize_window_by_pid(pid)
    
    # ==================== ФУНКЦИИ ПЕРЕМЕЩЕНИЯ ДЕМОНОВ ====================
    
    def move_selected_up(self):
        """Переместить выбранный демон вверх"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo(self.t("select_daemon"), self.t("select_daemon"))
            return
        
        item = selection[0]
        index = self.tree.index(item)
        
        if self.config_manager.move_daemon_up(index):
            daemon_name = self.tree.item(item)["values"][0]
            self.refresh_daemon_list()
            # Выделяем перемещенный элемент
            new_index = index - 1
            new_item = self.tree.get_children()[new_index]
            self.tree.selection_set(new_item)
            self.tree.see(new_item)
            self.log_message(self.t("daemon_moved_up", name=daemon_name), "success")
    
    def move_selected_down(self):
        """Переместить выбранный демон вниз"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo(self.t("select_daemon"), self.t("select_daemon"))
            return
        
        item = selection[0]
        index = self.tree.index(item)
        
        if self.config_manager.move_daemon_down(index):
            daemon_name = self.tree.item(item)["values"][0]
            self.refresh_daemon_list()
            # Выделяем перемещенный элемент
            new_index = index + 1
            new_item = self.tree.get_children()[new_index]
            self.tree.selection_set(new_item)
            self.tree.see(new_item)
            self.log_message(self.t("daemon_moved_down", name=daemon_name), "success")
    
    # ==================== ОСНОВНЫЕ ФУНКЦИИ ====================
    
    def check_initial_config(self):
        """Проверка начальной конфигурации"""
        if not self.config_manager.config.get("server_path"):
            self.ask_server_path()
        
        if not self.config_manager.get_daemons():
            if messagebox.askyesno(self.t("no_daemons"), self.t("ask_add_now")):
                self.add_daemon_dialog()
        
        self.refresh_daemon_list()
    
    def ask_server_path(self):
        """Запрос пути к серверам"""
        path = filedialog.askdirectory(title=self.t("select_server_path"))
        if path:
            self.config_manager.config["server_path"] = path
            self.config_manager.save_config()
            self.log_message(self.t("log_server_path_set", path=path))
            return True
        return False
    
    def add_daemon_dialog(self):
        """Диалог добавления демона"""
        dialog = tk.Toplevel(self.root)
        dialog.title(self.t("add_title"))
        dialog.geometry("500x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        self.center_dialog(dialog)
        self.create_daemon_form(dialog, mode="add")
    
    def edit_daemon_dialog(self):
        """Диалог редактирования демона"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo(self.t("select_daemon"), self.t("select_daemon"))
            return
        
        item = selection[0]
        index = self.tree.index(item)
        daemons = self.config_manager.get_daemons()
        
        if index >= len(daemons):
            return
        
        daemon = daemons[index]
        
        dialog = tk.Toplevel(self.root)
        dialog.title(self.t("edit_title"))
        dialog.geometry("500x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        self.center_dialog(dialog)
        self.create_daemon_form(dialog, mode="edit", daemon=daemon, index=index)
    
    def create_daemon_form(self, dialog, mode, daemon=None, index=None):
        """Создание формы"""
        row = 0
        
        # Название
        tk.Label(dialog, text=self.t("name_label")).grid(row=row, column=0, sticky=tk.W, padx=10, pady=10)
        name_var = tk.StringVar(value=daemon["name"] if daemon else "")
        tk.Entry(dialog, textvariable=name_var, width=40).grid(row=row, column=1, padx=10, pady=10)
        row += 1
        
        # Путь
        tk.Label(dialog, text=self.t("path_label")).grid(row=row, column=0, sticky=tk.W, padx=10, pady=10)
        path_var = tk.StringVar(value=daemon["exe_path"] if daemon else "")
        path_frame = tk.Frame(dialog)
        path_frame.grid(row=row, column=1, padx=10, pady=10, sticky=tk.EW)
        
        tk.Entry(path_frame, textvariable=path_var, width=30).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(path_frame, text=self.t("browse_btn"), 
                 command=lambda: self.browse_exe_file(path_var)).pack(side=tk.RIGHT, padx=(5, 0))
        row += 1
        
        # Задержка
        tk.Label(dialog, text=self.t("delay_label")).grid(row=row, column=0, sticky=tk.W, padx=10, pady=10)
        delay_var = tk.StringVar(value=str(daemon["delay"]) if daemon else "2")
        tk.Entry(dialog, textvariable=delay_var, width=10).grid(row=row, column=1, sticky=tk.W, padx=10, pady=10)
        row += 1
        
        # Включен
        enabled_var = tk.BooleanVar(value=daemon.get("enabled", True) if daemon else True)
        tk.Checkbutton(dialog, text=self.t("enabled_label"), 
                      variable=enabled_var).grid(row=row, column=0, sticky=tk.W, padx=10, pady=10)
        row += 1
        
        # Запуск свернутым (только если установлен pywin32)
        if HAS_WIN32:
            start_minimized_var = tk.BooleanVar(value=daemon.get("start_minimized", False) if daemon else False)
            tk.Checkbutton(dialog, text=self.t("minimize_on_start"), 
                          variable=start_minimized_var).grid(row=row, column=0, sticky=tk.W, padx=10, pady=10)
            row += 1
        
        # Кнопки
        btn_frame = tk.Frame(dialog)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        if mode == "add":
            tk.Button(btn_frame, text=self.t("add_btn_dialog"), 
                     command=lambda: self.save_new_daemon(dialog, name_var, path_var, 
                                                        delay_var, enabled_var, 
                                                        start_minimized_var if HAS_WIN32 else None),
                     bg="green", fg="white").pack(side=tk.LEFT, padx=10)
            tk.Button(btn_frame, text=self.t("autodetect_btn"), 
                     command=lambda: self.autodetect_daemons_with_order(dialog)).pack(side=tk.LEFT, padx=10)
        else:
            tk.Button(btn_frame, text=self.t("save_btn"), 
                     command=lambda: self.update_existing_daemon(dialog, index, name_var, 
                                                               path_var, delay_var, 
                                                               enabled_var, 
                                                               start_minimized_var if HAS_WIN32 else None),
                     bg="green", fg="white").pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text=self.t("cancel_btn"), 
                 command=dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    def save_new_daemon(self, dialog, name_var, path_var, delay_var, enabled_var, start_minimized_var=None):
        """Сохранение нового демона"""
        name = name_var.get().strip()
        path = path_var.get().strip()
        
        if not name:
            messagebox.showerror("Error", self.t("enter_daemon_name"))
            return
        
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", self.t("exe_file_not_found"))
            return
        
        try:
            delay = float(delay_var.get())
        except:
            delay = 2
        
        start_minimized = start_minimized_var.get() if start_minimized_var else False
        
        self.config_manager.add_daemon(name, path, delay, enabled_var.get(), start_minimized)
        self.refresh_daemon_list()
        self.log_message(self.t("daemon_added", name=name))
        dialog.destroy()
    
    def update_existing_daemon(self, dialog, index, name_var, path_var, delay_var, enabled_var, start_minimized_var=None):
        """Обновление демона"""
        name = name_var.get().strip()
        path = path_var.get().strip()
        
        if not name:
            messagebox.showerror("Error", self.t("enter_daemon_name"))
            return
        
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", self.t("exe_file_not_found"))
            return
        
        try:
            delay = float(delay_var.get())
        except:
            delay = 2
        
        start_minimized = start_minimized_var.get() if start_minimized_var else None
        
        self.config_manager.update_daemon(index, name, path, delay, enabled_var.get(), start_minimized)
        self.refresh_daemon_list()
        self.log_message(self.t("daemon_updated", name=name))
        dialog.destroy()
    
    def browse_exe_file(self, path_var):
        """Выбор .exe файла"""
        filename = filedialog.askopenfilename(
            title="Select .exe file",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if filename:
            path_var.set(filename)
    
    def autodetect_daemons_with_order(self, dialog):
        """Автоопределение демонов с правильным порядком запуска"""
        server_path = self.config_manager.config.get("server_path")
        if not server_path or not os.path.exists(server_path):
            messagebox.showerror("Error", self.t("server_path_not_found"))
            return
        
        self.log_message(self.t("log_autodetect"))
        
        # Правильный порядок запуска демонов BNS
        priority_order = [
            "CacheDaemon",
            "CacheGate",
            "AccountInventoryDaemon",
            "RankingDaemon",
            "PostOfficeDaemon",
            "LobbyDaemon",
            "MarketDealerDaemon",
            "MarketAgent",
            "ArenaLobby",
            "AchievementDaemon",
            "DuelBotDaemon",
            "GameDaemon"
        ]
        
        # Находим все .exe файлы
        detected = []
        for root_dir, dirs, files in os.walk(server_path):
            for file in files:
                if file.endswith(".exe"):
                    full_path = os.path.join(root_dir, file)
                    name = os.path.splitext(file)[0]
                    detected.append((name, full_path))
        
        if detected:
            # Сортируем по приоритету
            detected_sorted = []
            
            # Сначала добавляем демоны в порядке приоритета
            for priority_name in priority_order:
                for name, path in detected:
                    if name == priority_name:
                        # Проверяем, нет ли уже такого демона
                        existing = False
                        for d in self.config_manager.get_daemons():
                            if d["exe_path"] == path:
                                existing = True
                                break
                        
                        if not existing:
                            detected_sorted.append((name, path))
            
            # Затем добавляем остальные демоны (не из списка приоритета)
            for name, path in detected:
                if (name, path) not in detected_sorted:
                    # Проверяем, нет ли уже такого демона
                    existing = False
                    for d in self.config_manager.get_daemons():
                        if d["exe_path"] == path:
                            existing = True
                            break
                    
                    if not existing:
                        detected_sorted.append((name, path))
            
            # Добавляем демоны с правильным порядком
            for name, path in detected_sorted:
                # Определяем задержку по умолчанию
                delay = 2
                if name == "GameDaemon":
                    delay = 5  # GameDaemon запускаем последним с задержкой 5 секунд
                elif "Cache" in name or "Lobby" in name:
                    delay = 1  # Кэш и лобби быстрее
                
                self.config_manager.add_daemon(name, path, delay, True, False)
            
            self.refresh_daemon_list()
            count = len(detected_sorted)
            self.log_message(self.t("autodetect_found", count=count))
            
            # Показываем сообщение о порядке
            if count > 0:
                self.log_message("✅ Демоны добавлены в правильном порядке запуска", "success")
                self.log_message("Порядок запуска: Cache → Account → Ranking → Lobby → Market → GameDaemon")
            
            dialog.destroy()
        else:
            messagebox.showinfo("Info", self.t("autodetect_no_daemons"))
    
    def delete_daemon(self):
        """Удаление демона"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        index = self.tree.index(item)
        daemons = self.config_manager.get_daemons()
        
        if index < len(daemons):
            name = daemons[index]["name"]
            if messagebox.askyesno("Confirm", self.t("confirm_delete", name=name)):
                self.config_manager.remove_daemon(index)
                self.refresh_daemon_list()
                self.log_message(self.t("daemon_deleted", name=name))
    
    def refresh_daemon_list(self):
        """Обновление списка демонов"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        daemons = self.config_manager.get_daemons()
        for i, daemon in enumerate(daemons):
            status = self.t("stopped")
            if daemon["name"] in self.processes:
                process = self.processes[daemon["name"]]
                if process.poll() is None:
                    status = self.t("running")
                else:
                    status = self.t("crashed")
                    del self.processes[daemon["name"]]
            
            path = daemon["exe_path"]
            if len(path) > 60:
                path = "..." + path[-57:]
            
            self.tree.insert("", tk.END, values=(
                daemon["name"],
                status,
                path,
                daemon["delay"]
            ))
    
    def start_selected(self):
        """Запуск выбранного демона"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo(self.t("select_daemon"), self.t("select_daemon"))
            return
        
        item = selection[0]
        index = self.tree.index(item)
        daemons = self.config_manager.get_daemons()
        
        if index < len(daemons):
            daemon = daemons[index]
            if not daemon.get("enabled", True):
                messagebox.showinfo(self.t("daemon_disabled"), self.t("daemon_disabled"))
                return
            
            threading.Thread(target=lambda: self.start_daemon_with_window_mode(daemon), daemon=True).start()
    
    def start_all(self):
        """Запуск всех демонов в правильном порядке"""
        self.log_message("="*50)
        self.log_message(self.t("starting_all"))
        self.log_message("Запуск в порядке списка (сверху вниз)")
        
        def start_thread():
            daemons = self.config_manager.get_daemons()
            for daemon in daemons:
                if daemon.get("enabled", True):
                    self.start_daemon_with_window_mode(daemon)
                    time.sleep(daemon.get("delay", 2))
            
            self.log_message(self.t("all_started"), "success")
        
        threading.Thread(target=start_thread, daemon=True).start()
    
    def stop_daemon(self, daemon_name):
        """Остановка демона"""
        if daemon_name in self.processes:
            try:
                process = self.processes[daemon_name]
                process.terminate()
                process.wait(timeout=5)
                del self.processes[daemon_name]
                self.log_message(self.t("daemon_stopped", name=daemon_name))
                self.refresh_daemon_list()
                
            except subprocess.TimeoutExpired:
                process.kill()
                del self.processes[daemon_name]
                self.log_message(self.t("daemon_force_stopped", name=daemon_name), "warning")
                self.refresh_daemon_list()
                
            except Exception as e:
                self.log_message(self.t("log_error_stopping", name=daemon_name, error=str(e)), "error")
    
    def stop_selected(self):
        """Остановка выбранного демона"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo(self.t("select_daemon"), self.t("select_daemon"))
            return
        
        item = selection[0]
        daemon_name = self.tree.item(item)["values"][0]
        self.stop_daemon(daemon_name)
    
    def stop_all(self):
        """Остановка всех демонов в обратном порядке"""
        self.log_message("="*50)
        self.log_message(self.t("stopping_all"))
        self.log_message("Остановка в обратном порядке (снизу вверх)")
        
        daemons = self.config_manager.get_daemons()
        for daemon in reversed(daemons):
            if daemon["name"] in self.processes:
                self.stop_daemon(daemon["name"])
                time.sleep(1)
        
        self.log_message(self.t("all_stopped"))
    
    def restart_selected(self):
        """Перезапуск выбранного демона"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        index = self.tree.index(item)
        daemons = self.config_manager.get_daemons()
        
        if index < len(daemons):
            daemon = daemons[index]
            daemon_name = daemon["name"]
            
            if daemon_name in self.processes:
                self.stop_daemon(daemon_name)
                time.sleep(2)
            
            self.start_daemon_with_window_mode(daemon)
    
    def check_all_status(self):
        """Проверка статуса"""
        self.log_message(self.t("checking_status"))
        self.refresh_daemon_list()
        
        running = len([p for p in self.processes.values() if p.poll() is None])
        total = len(self.config_manager.get_daemons())
        
        self.status_bar.config(
            text=f"{self.t('status_running', running=running, total=total)} | {datetime.now().strftime('%H:%M:%S')}"
        )
        self.log_message(self.t("status_checked"))
    
    def auto_check_status(self):
        """Автоматическая проверка статуса"""
        self.check_all_status()
        self.root.after(10000, self.auto_check_status)
    
    def log_message(self, message, msg_type="info"):
        """Логирование"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        
        if msg_type == "error":
            self.log_text.tag_add("error", "end-2l", "end-1l")
            self.log_text.tag_config("error", foreground="red")
        elif msg_type == "success":
            self.log_text.tag_add("success", "end-2l", "end-1l")
            self.log_text.tag_config("success", foreground="green")
        elif msg_type == "warning":
            self.log_text.tag_add("warning", "end-2l", "end-1l")
            self.log_text.tag_config("warning", foreground="orange")
        
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Очистка лога"""
        self.log_text.delete(1.0, tk.END)
        self.log_message(self.t("log_cleared"))
    
    def on_daemon_double_click(self, event):
        """Двойной клик по демону"""
        selection = self.tree.selection()
        if selection:
            self.start_selected()
    
    def show_context_menu(self, event):
        """Контекстное меню с опциями перемещения"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        daemon_name = self.tree.item(item)["values"][0]
        
        menu = tk.Menu(self.root, tearoff=0)
        
        if daemon_name in self.processes:
            menu.add_command(label=self.t("cm_stop"), command=self.stop_selected)
            menu.add_command(label=self.t("cm_restart"), command=self.restart_selected)
            if HAS_WIN32:
                menu.add_separator()
                menu.add_command(label="🔽 " + self.t("minimize_selected"), 
                               command=self.minimize_selected_windows)
                menu.add_command(label="🔼 " + self.t("show_selected"), 
                               command=self.show_selected_windows)
        else:
            menu.add_command(label=self.t("cm_start"), command=self.start_selected)
        
        menu.add_separator()
        menu.add_command(label=self.t("cm_edit"), command=self.edit_daemon_dialog)
        menu.add_command(label=self.t("cm_delete"), command=self.delete_daemon)
        
        # Опции перемещения
        menu.add_separator()
        menu.add_command(label=self.t("cm_move_up"), command=self.move_selected_up)
        menu.add_command(label=self.t("cm_move_down"), command=self.move_selected_down)
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def change_server_path(self):
        """Изменение пути к серверам"""
        if self.ask_server_path():
            self.log_message(self.t("config_saved"), "success")
    
    def open_settings(self):
        """Открытие настроек"""
        messagebox.showinfo(self.t("settings_title"), self.t("settings_text"))
    
    def save_config(self):
        """Сохранение конфигурации"""
        self.config_manager.save_config()
        self.log_message(self.t("config_saved"), "success")
    
    def load_config(self):
        """Загрузка конфигурации"""
        filename = filedialog.askopenfilename(
            title="Select configuration file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.config_manager.config = json.load(f)
                    self.config_manager.save_config()
                    self.current_lang = self.config_manager.get_language()
                    self.tr = LANGUAGES[self.current_lang]
                    
                    for widget in self.root.winfo_children():
                        widget.destroy()
                    
                    self.setup_ui()
                    self.refresh_daemon_list()
                    self.log_message(self.t("config_loaded"), "success")
            except Exception as e:
                self.log_message(f"❌ Error loading: {str(e)}", "error")
    
    def show_about(self):
        """Показ информации о программе"""
        messagebox.showinfo(self.t("about_title"), self.t("about_text"))
    
    def center_dialog(self, dialog):
        """Центрирование диалогового окна"""
        self.center_window(dialog)
    
    def change_language(self, lang_code):
        """Смена языка интерфейса"""
        if self.config_manager.set_language(lang_code):
            self.current_lang = lang_code
            self.tr = LANGUAGES[lang_code]
            
            for widget in self.root.winfo_children():
                widget.destroy()
            
            self.setup_ui()
            self.refresh_daemon_list()
            self.log_message(self.t("config_saved"), "success")

def main():
    root = tk.Tk()
    app = BNSManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    if not HAS_WIN32:
        print("\n" + "="*60)
        print("Для сворачивания окон установите pywin32:")
        print("pip install pywin32")
        print("Функция 'Запускать свернутыми' будет недоступна")
        print("="*60 + "\n")
    
    main()