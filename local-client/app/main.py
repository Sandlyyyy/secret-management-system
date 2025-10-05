#!/usr/bin/env python3
"""
Secure Vault - Enterprise Secret Management Platform
Главная точка входа приложения
"""

import os
import sys
import traceback

# Добавляем корневую директорию в путь для импортов
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    """Главная функция приложения"""
    print("🚀 Запуск Secure Vault...")
    print("🔐 Enterprise Secret Management Platform")
    print("💡 Тестовые пользователи:")
    print("   👑 admin / admin123")
    print("   👤 demo / demo123") 
    print("   👥 user / user123")
    print("   🧪 test / test123")
    print("\n📺 Режим: ПОЛНОЭКРАННЫЙ")
    print("💡 Управление:")
    print("   ESC - выход из полноэкранного режима")
    print("   F11 - переключение полноэкранного режима") 
    print("   ❌ - закрыть приложение")
    print("\n✨ Инициализация приложения...")
    
    try:
        from ui.app import SecureVaultApp
        app = SecureVaultApp()
        print("✅ Приложение инициализировано успешно!")
        print("🖥️  Запуск в полноэкранном режиме...")
        app.run()
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("\n🔧 Проверьте структуру проекта:")
        print("secure_vault/")
        print("├── core/")
        print("│   ├── __init__.py")
        print("│   ├── database.py")
        print("│   └── services.py")
        print("├── ui/")
        print("│   ├── __init__.py")
        print("│   ├── themes.py")
        print("│   ├── components/")
        print("│   │   ├── __init__.py")
        print("│   │   └── widgets.py")
        print("│   └── app.py")
        print("└── main.py")
        traceback.print_exc()
        
    except Exception as e:
        print(f"❌ Ошибка при запуске приложения: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()