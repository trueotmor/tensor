import logging
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.saby_contacts_page import SabyContactsPage

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s - %(levelname)s - %(asctime)s - %(name)s',
    handlers=[logging.StreamHandler()]
)

def test_second_scenario():
    logger = logging.getLogger(__name__)
    logger.info("🚀 Запуск второго сценария")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        saby_page = SabyContactsPage(driver)

        # 1. Saby контакты
        logger.info("✅ 1. Открываем saby.ru")
        saby_page.open_page()
        
        logger.info("✅ 2. Открываем меню контактов")
        saby_page.click_contacts_button()
        
        logger.info("✅ 3. Переходим в контакты и ждем редирект в регион")
        saby_page.click_contacts_link()
        
        current_url = saby_page.get_current_url()
        assert "/contacts" in current_url, f"Не перешли на страницу контактов. Текущий URL: {current_url}"
        logger.info(f"✅ 4. Страница контактов загружена: {current_url}")

        # 2. Проверить, что определился ваш регион и есть список партнеров
        logger.info("✅ 5. Проверяем текущий регион")
        current_region = saby_page.get_current_region()
        assert current_region, "Регион не определился"
        logger.info(f"Текущий регион: {current_region}")
                
        logger.info("✅ 6. Проверяем наличие списка партнеров")
        partners = saby_page.get_partners()
        partners_count = len(partners) if partners else 0
        
        logger.info(f"Количество партнеров в текущем регионе: {partners_count}")
                
        # 3. Получаем информацию о партнерах
        partners_info = saby_page.get_partners_info()
        assert partners_count > 0, "Список партнеров пуст"
        
        # 4. Сохраняем исходные данные для сравнения
        original_region = current_region
        original_partners_count = partners_count
        original_partners_info = partners_info.copy()  # Сохраняем информацию о партнерах
        original_url = current_url
        original_title = saby_page.get_page_title()

        logger.info(f"Исходные данные: регион='{original_region}', партнеров={partners_count}, URL={original_url}")

        # 5. Меняем регион на Камчатский край
        logger.info("✅ 7. Открываем выбор региона")
        saby_page.open_region_chooser()
        
        logger.info("✅ 8. Выбираем Камчатский край")
        saby_page.select_kamchatka_region()
        
        # Ждем обновления данных после смены региона
        logger.info("Ждем обновления данных после смены региона")
        saby_page.wait_for_partners_updated()
        
        # 4. Проверить изменения
        logger.info("✅ 9. Проверяем смену региона")
        new_region = saby_page.get_current_region()
        assert "Камчатский" in new_region, f"Регион не сменился на Камчатский край. Текущий регион: {new_region}"
        logger.info(f"Регион изменился на: {new_region}")
        
        logger.info("✅ 10. Проверяем изменение списка партнеров")
        new_partners = saby_page.get_partners()
        new_partners_count = len(new_partners)
                
        logger.info(f"Количество партнеров в новом регионе: {new_partners_count}")
        
        # Получаем информацию о новых партнерах
        new_partners_info = saby_page.get_partners_info()
        for partner in new_partners_info:
            logger.info(f"Партнер в Камчатском крае: {partner['name']} - {partner.get('address', 'адрес не указан')}")
        
        # Проверяем что список партнеров изменился
        if new_partners_count != original_partners_count:
            logger.info(f"Количество партнеров изменилось: было {original_partners_count}, стало {new_partners_count}")
        else:
            # Если количество одинаковое, сравниваем содержимое
            original_names = {p['name'] for p in original_partners_info}
            new_names = {p['name'] for p in new_partners_info}
            
            assert original_names != new_names, "Список партнеров не изменился после смены региона"
            logger.info(f"Список партнеров изменился")
        
        logger.info("✅ 11. Проверяем URL")
        new_url = saby_page.get_current_url()
        assert new_url != original_url, "URL не изменился после смены региона"
        #TODO: убрать хардкод
        assert "41-kamchatskij-kraj" in new_url.lower(), f"URL не содержит информацию о выбранном регионе"
        logger.info(f"URL изменился и содержит регион: {new_url}")
        
        logger.info("✅ 12. Проверяем title")
        new_title = saby_page.get_page_title()
        assert new_title != original_title, "Title не изменился после смены региона"
        #TODO: убрать хардкод
        assert "Камчатский" in new_title, f"Title не содержит информацию о выбранном регионе. Текущий title: {new_title}"
        logger.info(f"Title изменился и содержит регион: {new_title}")
        
        logger.info("🎉 ВТОРОЙ СЦЕНАРИЙ УСПЕШНО ВЫПОЛНЕН!")
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        driver.save_screenshot("error_second_scenario.png")
        logger.info("📸 Скриншот ошибки сохранен: error_second_scenario.png")
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    test_second_scenario()