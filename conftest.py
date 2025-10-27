import pytest
import logging
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
    chrome_options = Options()
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    yield driver
    driver.quit()

@pytest.fixture(autouse=True)
def log_test_execution():
    logging.info("=" * 50)
    yield
    logging.info("=" * 50)