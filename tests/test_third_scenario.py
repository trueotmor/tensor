import sys
import os
import logging
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.saby_download_page import SabyDownloadPage

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s - %(levelname)s - %(asctime)s - %(name)s',
    handlers=[logging.StreamHandler()]
)

def setup_download_directory():
    download_dir = tempfile.mkdtemp()
    logging.info(f"Директория для загрузок: {download_dir}")
    return download_dir

def setup_chrome_driver(download_dir):
    chrome_options = Options()
    
    # Настройки для автоматической загрузки файлов
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "safebrowsing.disable_download_protection": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    return driver

def test_third_scenario():
    logger = logging.getLogger(__name__)
    logger.info("🚀 Запуск третьего сценария")
        
    # Настраиваем директорию для загрузок
    download_dir = setup_download_directory()
    
    # Настраиваем драйвер
    driver = setup_chrome_driver(download_dir)
    
    try:
        download_page = SabyDownloadPage(driver, download_dir)

        # 1. Перейти на saby.ru
        logger.info("✅ 1. Переходим на saby.ru")
        download_page.open_page()

        # 2. Найти и перейти "Скачать локальные версии"
        logger.info("✅ 2. Переходим в раздел загрузок")
        download_page.navigate_to_downloads()

        # 3. Проверить, что перешли на страницу загрузок с правильными параметрами
        current_url = driver.current_url
        assert "/download" in current_url, f"Не перешли на правильную страницу загрузок. Текущий URL: {current_url}"
        logger.info(f"Успешно перешли на страницу загрузок: {current_url}")

        # 4. Убедиться, что выбран Saby Desktop
        logger.info("✅ 3. Проверяем выбор Saby Desktop")
        download_page.ensure_saby_desktop_selected()

        # 5. Убедиться, что выбрана Windows
        logger.info("✅ 4. Проверяем выбор Windows")
        download_page.ensure_windows_selected()

        # 6. Получить информацию о скачиваемом файле
        logger.info("✅ 5. Получаем информацию о файле для скачивания")
        download_info = download_page.get_download_info()
        
        logger.info(f"URL для скачивания: {download_info['url']}")
        logger.info(f"Информация о версии: {download_info['version_info']}")
        
        # В тестовом задании страница отличается от существующей. Для сравнения просто берем значение 6.50Мб
        expected_size_mb = 6.50
        logger.info(f"Ожидаемый размер: {expected_size_mb} МБ")

        # 7. Скачать веб-установщик
        logger.info("✅ 6. Скачиваем веб-установщик")
        download_page.download_web_installer()

        # 8. Убедиться, что плагин скачался
        logger.info("✅ 7. Ожидаем завершения загрузки")
        downloaded_file_path = download_page.wait_for_download_complete(timeout=20)
        logger.info(f"✅ Файл скачан: {downloaded_file_path}")

        # 9. Сравнить размер скачанного файла
        logger.info("✅ 8. Сравниваем размер скачанного файла")
        actual_size_mb = download_page.get_downloaded_file_size(downloaded_file_path)
        
        # Сравниваем с допуском 0.05 МБ
        tolerance = 0.05
        size_diff = abs(actual_size_mb - expected_size_mb)
        
        logger.info(f"Ожидаемый размер: {expected_size_mb:.2f} МБ")
        logger.info(f"Фактический размер: {actual_size_mb:.2f} МБ")
        logger.info(f"Разница: {size_diff:.2f} МБ")
        
        assert size_diff <= tolerance, (
            f"Размер файла не совпадает! Ожидалось: {expected_size_mb:.2f} МБ, "
            f"фактически: {actual_size_mb:.2f} МБ, разница: {size_diff:.2f} МБ"
        )
        
        logger.info(f"✅ Размер файла совпадает с ожидаемым ({expected_size_mb:.2f} МБ)")

        logger.info("🎉 ТРЕТИЙ СЦЕНАРИЙ УСПЕШНО ВЫПОЛНЕН!")

    except Exception as e:
        logger.error(f"❌ Ошибка в третьем сценарии: {e}", exc_info=True)
        driver.save_screenshot("error_download_scenario.png")
        logger.info("📸 Скриншот ошибки сохранен: error_download_scenario.png")
        raise
    
    finally:
        driver.quit()

if __name__ == "__main__":
    test_third_scenario()