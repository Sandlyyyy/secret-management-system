import tkinter as tk
from ..themes import ThemeManager

class ModernButton(tk.Canvas):
    def __init__(self, parent, text, command, **kwargs):
        self.theme = ThemeManager.get_theme()
        self.width = kwargs.pop('width', 200)
        self.height = kwargs.pop('height', 40)
        self.bg_color = kwargs.pop('bg_color', self.theme.colors.primary)
        self.hover_color = kwargs.pop('hover_color', self.theme.colors.secondary)
        self.text_color = kwargs.pop('text_color', self.theme.colors.background)
        
        super().__init__(
            parent, 
            width=self.width, 
            height=self.height, 
            highlightthickness=0,
            bg=self.theme.colors.background
        )
        
        self.command = command
        self._text = text
        
        self._bind_events()
        self._draw_normal()
    
    def _bind_events(self):
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)
    
    def _draw_normal(self):
        self.delete("all")
        self.create_rectangle(
            2, 2, self.width-2, self.height-2,
            fill=self.bg_color, outline=self.bg_color, width=2
        )
        self.create_text(
            self.width//2, self.height//2,
            text=self._text, fill=self.text_color,
            font=("Arial", 12, "bold")  # Увеличили шрифт для полноэкранного режима
        )
    
    def _draw_hover(self):
        self.delete("all")
        self.create_rectangle(
            2, 2, self.width-2, self.height-2,
            fill=self.hover_color, outline=self.hover_color, width=2
        )
        self.create_text(
            self.width//2, self.height//2,
            text=self._text, fill=self.text_color,
            font=("Arial", 12, "bold")
        )
    
    def _draw_pressed(self):
        self.delete("all")
        self.create_rectangle(
            4, 4, self.width-2, self.height-2,
            fill=self.hover_color, outline=self.hover_color, width=2
        )
        self.create_text(
            self.width//2 + 1, self.height//2 + 1,
            text=self._text, fill=self.text_color,
            font=("Arial", 12, "bold")
        )
    
    def _on_enter(self, event):
        self._draw_hover()
    
    def _on_leave(self, event):
        self._draw_normal()
    
    def _on_click(self, event):
        self._draw_pressed()
    
    def _on_release(self, event):
        self._draw_hover()
        self.command()

class SecretCard(tk.Frame):
    def __init__(self, parent, secret, on_copy, on_view):
        self.theme = ThemeManager.get_theme()
        self.secret = secret
        self.on_copy = on_copy
        self.on_view = on_view
        
        super().__init__(
            parent,
            bg=self.theme.colors.surface,
            relief='raised',
            bd=1
        )
        
        self._setup_ui()
    
    def _setup_ui(self):
        content = tk.Frame(self, bg=self.theme.colors.surface)
        content.pack(fill='x', padx=20, pady=20)  # Увеличили отступы
        
        # Info section
        info_frame = tk.Frame(content, bg=self.theme.colors.surface)
        info_frame.pack(side='left', fill='x', expand=True)
        
        # Header with name and type
        header_frame = tk.Frame(info_frame, bg=self.theme.colors.surface)
        header_frame.pack(fill='x')
        
        tk.Label(
            header_frame,
            text=self.secret.name,
            font=("Arial", 16, "bold"),  # Увеличили шрифт
            fg=self.theme.colors.text_primary,
            bg=self.theme.colors.surface
        ).pack(side='left')
        
        # Type badge
        type_config = self._get_type_config()
        tk.Label(
            header_frame,
            text=type_config["text"],
            font=("Arial", 12, "bold"),  # Увеличили шрифт
            fg=type_config["color"],
            bg=self.theme.colors.surface
        ).pack(side='left', padx=(15, 0))
        
        # Description
        tk.Label(
            info_frame,
            text=self.secret.description,
            font=("Arial", 14),  # Увеличили шрифт
            fg=self.theme.colors.text_secondary,
            bg=self.theme.colors.surface,
            wraplength=600,  # Увеличили ширину обертки
            justify='left'
        ).pack(anchor='w', pady=(12, 0))
        
        # Metadata
        meta_frame = tk.Frame(info_frame, bg=self.theme.colors.surface)
        meta_frame.pack(anchor='w', pady=(15, 0))
        
        tk.Label(
            meta_frame,
            text=f"👤 {self.secret.owner}",
            font=("Arial", 12),  # Увеличили шрифт
            fg=self.theme.colors.text_secondary,
            bg=self.theme.colors.surface
        ).pack(side='left', padx=(0, 20))
        
        created_date = self.secret.created_at.strftime("%d.%m.%Y")
        tk.Label(
            meta_frame,
            text=f"📅 {created_date}",
            font=("Arial", 12),  # Увеличили шрифт
            fg=self.theme.colors.text_secondary,
            bg=self.theme.colors.surface
        ).pack(side='left')
        
        # Actions section
        action_frame = tk.Frame(content, bg=self.theme.colors.surface)
        action_frame.pack(side='right')
        
        # Status
        status_config = self._get_status_config()
        tk.Label(
            action_frame,
            text=status_config["text"],
            font=("Arial", 14, "bold"),  # Увеличили шрифт
            fg=status_config["color"],
            bg=self.theme.colors.surface
        ).pack(anchor='e')
        
        # Action buttons for approved secrets
        if self.secret.status.value == 'approved':
            btn_frame = tk.Frame(action_frame, bg=self.theme.colors.surface)
            btn_frame.pack(anchor='e', pady=(12, 0))
            
            ModernButton(
                btn_frame,
                "📋 Копировать",
                lambda: self.on_copy(self.secret),
                width=140,
                height=40
            ).pack(side='left', padx=(8, 0))
            
            ModernButton(
                btn_frame,
                "👁️ Показать",
                lambda: self.on_view(self.secret),
                width=130,
                height=40,
                bg_color="#3498db",
                hover_color="#2980b9"
            ).pack(side='left', padx=(8, 0))
    
    def _get_type_config(self):
        configs = {
            "database": {"text": "🗄️ БАЗА ДАННЫХ", "color": "#3498db"},
            "api": {"text": "🔑 API КЛЮЧ", "color": "#e74c3c"},
            "cloud": {"text": "☁️ ОБЛАКО", "color": "#f39c12"},
            "security": {"text": "🛡️ БЕЗОПАСНОСТЬ", "color": "#9b59b6"},
            "email": {"text": "📧 EMAIL", "color": "#2ecc71"},
            "custom": {"text": "📝 ПОЛЬЗАТЕЛЬСКИЙ", "color": "#95a5a6"}
        }
        return configs.get(self.secret.type.value, {"text": "📁 ДРУГОЕ", "color": "#95a5a6"})
    
    def _get_status_config(self):
        configs = {
            "approved": {"text": "✅ ОДОБРЕНО", "color": self.theme.colors.success},
            "pending": {"text": "⏳ ОЖИДАНИЕ", "color": self.theme.colors.warning},
            "rejected": {"text": "❌ ОТКЛОНЕНО", "color": self.theme.colors.error}
        }
        return configs.get(self.secret.status.value, {"text": "❓ НЕИЗВЕСТНО", "color": self.theme.colors.text_secondary})