import pytest
import logging
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Настройка логирования для всех тестов
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s - %(levelname)s - %(asctime)s - %(name)s',
    handlers=[logging.StreamHandler()]
)

@pytest.fixture
def driver():
    """Фикстура для создания и закрытия WebDriver
    
    Setup: Создает драйвер Chrome
    Teardown: Закрывает драйвер после завершения теста
    """
    chrome_options = Options()
    
    # Setup: создание драйвера
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    yield driver
    
    # Teardown: закрытие драйвера
    driver.quit()

@pytest.fixture
def temp_download_dir():
    """Фикстура для создания временной директории загрузок
    
    Setup: Создает временную директорию для скачанных файлов
    Teardown: Удаляет директорию и все файлы в ней после теста
    """
    # Setup: создание временной директории
    download_dir = tempfile.mkdtemp()
    logging.info(f"Создана временная директория для загрузок: {download_dir}")
    
    yield download_dir
    
    # Teardown: удаление временной директории
    try:
        shutil.rmtree(download_dir)
        logging.info(f"Временная директория удалена: {download_dir}")
    except Exception as e:
        logging.warning(f"Не удалось удалить временную директорию: {e}")

@pytest.fixture(autouse=True)
def test_logging():
    """Автоматическая фикстура для логирования начала и конца каждого теста"""
    logging.info("=" * 50)
    yield
    logging.info("=" * 50)
