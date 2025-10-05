import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from core.database import Database, SecretType
from core.services import AuthService, SecretService, AuditService
from .themes import ThemeManager
from .components.widgets import ModernButton, SecretCard

class SecureVaultApp:
    def __init__(self):
        self.root = tk.Tk()
        self.theme = ThemeManager.get_theme()
        
        # Initialize services
        self.database = Database()
        self.auth_service = AuthService(self.database)
        self.secret_service = SecretService(self.database, self.auth_service)
        self.audit_service = AuditService(self.database)
        
        self._setup_window()
        self.show_login()
    
    def _setup_window(self):
        self.root.title("🔐 Secure Vault - Enterprise Secret Management")
        
        # Устанавливаем полноэкранный режим
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg=self.theme.colors.background)
        
        # Добавляем обработчики для выхода из полноэкранного режима
        self.root.bind("<Escape>", self._exit_fullscreen)
        self.root.bind("<F11>", self._toggle_fullscreen)
        
        # Добавляем кнопку закрытия в углу
        self._add_close_button()
    
    def _add_close_button(self):
        """Добавляет кнопку закрытия в правом верхнем углу"""
        close_btn = tk.Button(
            self.root,
            text="❌",
            command=self.root.quit,
            font=("Arial", 14),
            bg=self.theme.colors.error,
            fg="white",
            border=0,
            cursor="hand2"
        )
        close_btn.place(relx=0.98, rely=0.02, anchor="ne")
    
    def _exit_fullscreen(self, event=None):
        """Выход из полноэкранного режима по Escape"""
        self.root.attributes('-fullscreen', False)
        self.root.geometry("1000x700")
        self._center_window()
    
    def _toggle_fullscreen(self, event=None):
        """Переключение полноэкранного режима по F11"""
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
    
    def _center_window(self):
        """Центрирование окна при выходе из полноэкранного режима"""
        self.root.update_idletasks()
        width = 1000
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Button) or widget.cget("text") != "❌":
                widget.destroy()
    
    def show_login(self):
        self.clear_window()
        
        # Используем относительное позиционирование для адаптивности
        main_frame = tk.Frame(self.root, bg=self.theme.colors.background)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🔐 SECURE VAULT",
            font=("Arial", 36, "bold"),
            fg=self.theme.colors.primary,
            bg=self.theme.colors.background
        )
        title_label.pack(pady=(0, 20))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Enterprise Secret Management Platform",
            font=("Arial", 18),
            fg=self.theme.colors.text_secondary,
            bg=self.theme.colors.background
        )
        subtitle_label.pack(pady=(0, 60))
        
        # Login form
        form_frame = tk.Frame(main_frame, bg=self.theme.colors.surface, relief='raised', bd=2)
        form_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.7)
        
        # Test credentials
        info_label = tk.Label(
            form_frame,
            text="🚀 ДЕМО-РЕЖИМ - Тестовые пользователи:",
            font=("Arial", 14, "bold"),
            fg=self.theme.colors.primary,
            bg=self.theme.colors.surface
        )
        info_label.pack(pady=(40, 20))
        
        test_users = [
            "👑 Администратор: admin / admin123",
            "👤 Демо-пользователь: demo / demo123", 
            "👥 Обычный пользователь: user / user123",
            "🧪 Тестовый: test / test123"
        ]
        
        for user in test_users:
            tk.Label(
                form_frame,
                text=user,
                font=("Arial", 12),
                fg=self.theme.colors.text_secondary,
                bg=self.theme.colors.surface
            ).pack(pady=3)
        
        # Input fields
        input_frame = tk.Frame(form_frame, bg=self.theme.colors.surface)
        input_frame.pack(fill='x', pady=(40, 0), padx=60)
        
        # Username
        tk.Label(
            input_frame,
            text="Логин:",
            font=("Arial", 14, "bold"),
            fg=self.theme.colors.text_primary,
            bg=self.theme.colors.surface
        ).pack(anchor='w', pady=(20, 5))
        
        self.username_entry = tk.Entry(
            input_frame,
            font=("Arial", 16),
            bg="#0A0A0A",
            fg=self.theme.colors.text_primary,
            insertbackground=self.theme.colors.text_primary
        )
        self.username_entry.pack(fill='x', pady=(0, 20))
        self.username_entry.insert(0, "demo")
        
        # Password
        tk.Label(
            input_frame,
            text="Пароль:",
            font=("Arial", 14, "bold"),
            fg=self.theme.colors.text_primary,
            bg=self.theme.colors.surface
        ).pack(anchor='w', pady=(20, 5))
        
        self.password_entry = tk.Entry(
            input_frame,
            font=("Arial", 16),
            show="•",
            bg="#0A0A0A",
            fg=self.theme.colors.text_primary,
            insertbackground=self.theme.colors.text_primary
        )
        self.password_entry.pack(fill='x', pady=(0, 40))
        self.password_entry.insert(0, "demo123")
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Login button
        ModernButton(
            input_frame,
            "🔓 ВОЙТИ В СИСТЕМУ",
            self.login,
            width=400,
            height=60
        ).pack()
        
        # Status
        self.status_label = tk.Label(
            input_frame,
            text="",
            font=("Arial", 12),
            fg=self.theme.colors.error,
            bg=self.theme.colors.surface
        )
        self.status_label.pack(pady=20)
        
        # Footer hint
        hint_label = tk.Label(
            form_frame,
            text="💡 Нажмите ESC для выхода из полноэкранного режима | F11 для переключения",
            font=("Arial", 10),
            fg=self.theme.colors.text_secondary,
            bg=self.theme.colors.surface
        )
        hint_label.pack(side='bottom', pady=20)
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            self.status_label.config(text="❌ Введите логин и пароль")
            return
        
        self.status_label.config(text="⏳ Проверка учетных данных...")
        self.root.update()
        
        # Simulate network delay
        self.root.after(1000, lambda: self._perform_login(username, password))
    
    def _perform_login(self, username, password):
        if self.auth_service.login(username, password):
            self.status_label.config(text="✅ Успешный вход! Загрузка...", fg=self.theme.colors.success)
            self.root.after(1500, self.show_dashboard)
        else:
            self.status_label.config(text="❌ Неверный логин или пароль", fg=self.theme.colors.error)
    
    def show_dashboard(self):
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg="#050505", height=100)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        
        # User info
        user_info_frame = tk.Frame(header, bg="#050505")
        user_info_frame.pack(side='left', padx=40, pady=30)
        
        user = self.auth_service.get_current_user()
        tk.Label(
            user_info_frame,
            text=f"👋 {user.display_name}",
            font=("Arial", 20, "bold"),
            fg=self.theme.colors.text_primary,
            bg="#050505"
        ).pack(anchor='w')
        
        tk.Label(
            user_info_frame,
            text="Панель управления секретами",
            font=("Arial", 14),
            fg=self.theme.colors.text_secondary,
            bg="#050505"
        ).pack(anchor='w')
        
        # Controls
        controls_frame = tk.Frame(header, bg="#050505")
        controls_frame.pack(side='right', padx=40, pady=30)
        
        ModernButton(
            controls_frame,
            "➕ Новый запрос",
            self.show_request_dialog,
            width=160,
            height=45
        ).pack(side='left', padx=8)
        
        ModernButton(
            controls_frame,
            "📊 Аудит",
            self.show_audit_dialog,
            width=120,
            height=45,
            bg_color="#3498db",
            hover_color="#2980b9"
        ).pack(side='left', padx=8)
        
        ModernButton(
            controls_frame,
            "🔄 Обновить",
            lambda: self.show_dashboard(),
            width=120,
            height=45,
            bg_color="#333333",
            hover_color="#555555"
        ).pack(side='left', padx=8)
        
        ModernButton(
            controls_frame,
            "🚪 Выход",
            self.logout,
            width=120,
            height=45,
            bg_color=self.theme.colors.error,
            hover_color="#FF5252"
        ).pack(side='left', padx=8)
        
        # Content
        content = tk.Frame(self.root, bg=self.theme.colors.background)
        content.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Stats
        self.show_stats(content)
        # Secrets
        self.show_secrets(content)
    
    def show_stats(self, parent):
        stats_frame = tk.Frame(parent, bg=self.theme.colors.surface, relief='raised', bd=1)
        stats_frame.pack(fill='x', pady=(0, 30))
        
        user = self.auth_service.get_current_user()
        stats = self.audit_service.get_user_stats(user.username)
        
        stats_data = [
            (f"📊 Всего секретов: {stats['total']}", self.theme.colors.text_primary),
            (f"✅ Одобрено: {stats['approved']}", self.theme.colors.success),
            (f"⏳ Ожидание: {stats['pending']}", self.theme.colors.warning),
            (f"❌ Отклонено: {stats['rejected']}", self.theme.colors.error)
        ]
        
        for text, color in stats_data:
            frame = tk.Frame(stats_frame, bg=self.theme.colors.surface)
            frame.pack(side='left', expand=True, padx=30, pady=20)
            
            tk.Label(
                frame,
                text=text,
                font=("Arial", 14, "bold"),
                fg=color,
                bg=self.theme.colors.surface
            ).pack()
    
    def show_secrets(self, parent):
        # Title
        title_frame = tk.Frame(parent, bg=self.theme.colors.background)
        title_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="📁 МОИ СЕКРЕТЫ",
            font=("Arial", 24, "bold"),
            fg=self.theme.colors.primary,
            bg=self.theme.colors.background
        ).pack(anchor='w')
        
        # Secrets container with scroll
        container = tk.Frame(parent, bg=self.theme.colors.background)
        container.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(container, bg=self.theme.colors.background, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme.colors.background)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Load secrets
        secrets = self.secret_service.get_user_secrets()
        
        if not secrets:
            self.show_empty_state(scrollable_frame)
        else:
            for secret in secrets:
                SecretCard(
                    scrollable_frame,
                    secret,
                    on_copy=self.copy_secret,
                    on_view=self.view_secret
                ).pack(fill='x', pady=10, padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_empty_state(self, parent):
        empty_frame = tk.Frame(
            parent,
            bg=self.theme.colors.surface,
            relief='raised',
            bd=1
        )
        empty_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.4)
        
        tk.Label(
            empty_frame,
            text="📭 У вас пока нет секретов",
            font=("Arial", 24, "bold"),
            fg=self.theme.colors.text_secondary,
            bg=self.theme.colors.surface
        ).pack(expand=True, pady=(80, 20))
        
        tk.Label(
            empty_frame,
            text="Запросите ваш первый секрет для начала работы",
            font=("Arial", 16),
            fg=self.theme.colors.text_secondary,
            bg=self.theme.colors.surface
        ).pack(pady=(0, 40))
        
        ModernButton(
            empty_frame,
            "📝 Создать первый запрос",
            self.show_request_dialog,
            width=300,
            height=60
        ).pack(pady=20)
    
    def copy_secret(self, secret):
        value = self.secret_service.get_secret_value(secret.id)
        if value:
            messagebox.showinfo(
                "✅ Секрет скопирован!", 
                f"Значение секрета '{secret.name}' готово для использования!\n\n"
                f"🔐 {value}\n\n"
                "В реальном приложении это значение было бы скопировано в буфер обмена."
            )
        else:
            messagebox.showwarning(
                "⚠️ Доступ запрещен", 
                "Этот секрет еще не одобрен или у вас нет прав доступа."
            )
    
    def view_secret(self, secret):
        value = self.secret_service.get_secret_value(secret.id)
        if value:
            dialog = tk.Toplevel(self.root)
            dialog.title(f"🔐 {secret.name}")
            # Делаем диалог тоже полноэкранным
            dialog.attributes('-fullscreen', True)
            dialog.configure(bg=self.theme.colors.background)
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Добавляем кнопку закрытия для диалога
            close_dialog_btn = tk.Button(
                dialog,
                text="❌",
                command=dialog.destroy,
                font=("Arial", 14),
                bg=self.theme.colors.error,
                fg="white",
                border=0,
                cursor="hand2"
            )
            close_dialog_btn.place(relx=0.98, rely=0.02, anchor="ne")
            
            # Header
            header_frame = tk.Frame(dialog, bg=self.theme.colors.background)
            header_frame.pack(fill='x', padx=40, pady=40)
            
            tk.Label(
                header_frame,
                text=f"🔐 {secret.name}",
                font=("Arial", 24, "bold"),
                fg=self.theme.colors.primary,
                bg=self.theme.colors.background
            ).pack(anchor='w')
            
            tk.Label(
                header_frame,
                text=secret.description,
                font=("Arial", 16),
                fg=self.theme.colors.text_secondary,
                bg=self.theme.colors.background,
                wraplength=1200
            ).pack(anchor='w', pady=(10, 0))
            
            # Secret value
            value_frame = tk.Frame(dialog, bg=self.theme.colors.background)
            value_frame.pack(fill='both', expand=True, padx=40, pady=20)
            
            tk.Label(
                value_frame,
                text="Значение секрета:",
                font=("Arial", 18, "bold"),
                fg=self.theme.colors.text_primary,
                bg=self.theme.colors.background
            ).pack(anchor='w', pady=(0, 20))
            
            text_frame = tk.Frame(value_frame, bg=self.theme.colors.background)
            text_frame.pack(fill='both', expand=True)
            
            text_widget = scrolledtext.ScrolledText(
                text_frame,
                wrap=tk.WORD,
                font=("Consolas", 14),
                bg=self.theme.colors.surface,
                fg=self.theme.colors.text_primary,
                insertbackground=self.theme.colors.text_primary,
                relief='flat'
            )
            text_widget.pack(fill='both', expand=True)
            text_widget.insert('1.0', value)
            text_widget.config(state='disabled')
            
            # Buttons
            button_frame = tk.Frame(dialog, bg=self.theme.colors.background)
            button_frame.pack(fill='x', padx=40, pady=40)
            
            ModernButton(
                button_frame,
                "📋 Копировать в буфер",
                lambda: self.copy_secret_value(value, dialog),
                width=250,
                height=60
            ).pack(side='left', padx=(0, 20))
            
            ModernButton(
                button_frame,
                "❌ Закрыть",
                dialog.destroy,
                width=150,
                height=60,
                bg_color="#333333",
                hover_color="#555555"
            ).pack(side='left')
        else:
            messagebox.showwarning(
                "⚠️ Доступ запрещен", 
                "Этот секрет еще не одобрен или у вас нет прав доступа."
            )
    
    def copy_secret_value(self, value, parent):
        messagebox.showinfo(
            "✅ Скопировано!", 
            "Значение секрета скопировано в буфер обмена.",
            parent=parent
        )
    
    def show_request_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("📝 Запрос нового секрета")
        # Делаем диалог полноэкранным
        dialog.attributes('-fullscreen', True)
        dialog.configure(bg=self.theme.colors.background)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Добавляем кнопку закрытия для диалога
        close_dialog_btn = tk.Button(
            dialog,
            text="❌",
            command=dialog.destroy,
            font=("Arial", 14),
            bg=self.theme.colors.error,
            fg="white",
            border=0,
            cursor="hand2"
        )
        close_dialog_btn.place(relx=0.98, rely=0.02, anchor="ne")
        
        main_frame = tk.Frame(dialog, bg=self.theme.colors.background)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)
        
        # Title
        tk.Label(
            main_frame,
            text="📝 ЗАПРОС НОВОГО СЕКРЕТА",
            font=("Arial", 24, "bold"),
            fg=self.theme.colors.primary,
            bg=self.theme.colors.background
        ).pack(pady=(0, 40))
        
        # Secret type
        type_frame = tk.Frame(main_frame, bg=self.theme.colors.background)
        type_frame.pack(fill='x', pady=(0, 30))
        
        tk.Label(
            type_frame,
            text="Тип секрета:",
            font=("Arial", 16, "bold"),
            fg=self.theme.colors.text_primary,
            bg=self.theme.colors.background
        ).pack(anchor='w', pady=(0, 15))
        
        self.secret_type = tk.StringVar(value=SecretType.CUSTOM.value)
        
        types = [
            ("🗄️ База данных", SecretType.DATABASE),
            ("🔑 API Ключ", SecretType.API),
            ("☁️ Облачный сервис", SecretType.CLOUD),
            ("🛡️ Безопасность", SecretType.SECURITY),
            ("📧 Email", SecretType.EMAIL),
            ("📝 Пользовательский", SecretType.CUSTOM)
        ]
        
        type_buttons_frame = tk.Frame(type_frame, bg=self.theme.colors.background)
        type_buttons_frame.pack(fill='x')
        
        for text, secret_type in types:
            btn = tk.Radiobutton(
                type_buttons_frame,
                text=text,
                variable=self.secret_type,
                value=secret_type.value,
                font=("Arial", 14),
                fg=self.theme.colors.text_primary,
                bg=self.theme.colors.background,
                selectcolor=self.theme.colors.surface,
                activebackground=self.theme.colors.background,
                activeforeground=self.theme.colors.primary
            )
            btn.pack(side='left', padx=(0, 25))
        
        # Name
        tk.Label(
            main_frame,
            text="Название секрета:",
            font=("Arial", 16, "bold"),
            fg=self.theme.colors.text_primary,
            bg=self.theme.colors.background
        ).pack(anchor='w', pady=(0, 15))
        
        name_entry = tk.Entry(
            main_frame,
            font=("Arial", 16),
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            insertbackground=self.theme.colors.text_primary
        )
        name_entry.pack(fill='x', pady=(0, 30))
        
        # Description
        tk.Label(
            main_frame,
            text="Описание и назначение:",
            font=("Arial", 16, "bold"),
            fg=self.theme.colors.text_primary,
            bg=self.theme.colors.background
        ).pack(anchor='w', pady=(0, 15))
        
        desc_text = scrolledtext.ScrolledText(
            main_frame,
            height=12,
            font=("Arial", 14),
            bg=self.theme.colors.surface,
            fg=self.theme.colors.text_primary,
            insertbackground=self.theme.colors.text_primary,
            wrap=tk.WORD
        )
        desc_text.pack(fill='both', expand=True, pady=(0, 40))
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.theme.colors.background)
        button_frame.pack(fill='x')
        
        def submit_request():
            name = name_entry.get().strip()
            description = desc_text.get("1.0", "end-1c").strip()
            s_type = SecretType(self.secret_type.get())
            
            if not name:
                messagebox.showerror("Ошибка", "Введите название секрета", parent=dialog)
                return
            
            if not description:
                messagebox.showerror("Ошибка", "Введите описание секрета", parent=dialog)
                return
            
            if self.secret_service.request_secret(name, description, s_type):
                messagebox.showinfo(
                    "✅ Успех!", 
                    "Запрос на секрет отправлен на согласование!\n\n"
                    "Вы будете уведомлены, когда секрет будет одобрен.",
                    parent=dialog
                )
                dialog.destroy()
                self.show_dashboard()  # Refresh
            else:
                messagebox.showerror("Ошибка", "Не удалось отправить запрос", parent=dialog)
        
        ModernButton(
            button_frame,
            "📨 Отправить запрос",
            submit_request,
            width=250,
            height=60
        ).pack(side='left', padx=(0, 25))
        
        ModernButton(
            button_frame,
            "❌ Отмена",
            dialog.destroy,
            width=180,
            height=60,
            bg_color="#333333",
            hover_color="#555555"
        ).pack(side='left')
        
        name_entry.focus()
    
    def show_audit_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("📊 Журнал аудита")
        # Делаем диалог полноэкранным
        dialog.attributes('-fullscreen', True)
        dialog.configure(bg=self.theme.colors.background)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Добавляем кнопку закрытия для диалога
        close_dialog_btn = tk.Button(
            dialog,
            text="❌",
            command=dialog.destroy,
            font=("Arial", 14),
            bg=self.theme.colors.error,
            fg="white",
            border=0,
            cursor="hand2"
        )
        close_dialog_btn.place(relx=0.98, rely=0.02, anchor="ne")
        
        main_frame = tk.Frame(dialog, bg=self.theme.colors.background)
        main_frame.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Title
        tk.Label(
            main_frame,
            text="📊 ЖУРНАЛ АУДИТА",
            font=("Arial", 24, "bold"),
            fg=self.theme.colors.primary,
            bg=self.theme.colors.background
        ).pack(anchor='w', pady=(0, 30))
        
        # Logs table
        columns = ("Время", "Пользователь", "Действие", "Объект", "Статус")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20)
        
        # Увеличиваем размер шрифта и колонок для полноэкранного режима
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12), rowheight=30)
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        tree.column("Время", width=250)
        tree.column("Действие", width=180)
        tree.column("Статус", width=150)
        
        # Add data
        logs = self.audit_service.get_logs()
        for log in logs:
            time = log.timestamp.strftime("%d.%m.%Y %H:%M:%S")
            tree.insert("", "end", values=(time, log.user, log.action, log.resource, log.status))
        
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Close button
        btn_frame = tk.Frame(main_frame, bg=self.theme.colors.background)
        btn_frame.pack(fill='x', pady=(30, 0))
        
        ModernButton(
            btn_frame,
            "❌ Закрыть",
            dialog.destroy,
            width=180,
            height=60,
            bg_color="#333333",
            hover_color="#555555"
        ).pack(side='right')
    
    def logout(self):
        self.auth_service.logout()
        self.show_login()
    
    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
            self.root.quit()