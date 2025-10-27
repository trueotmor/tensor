import logging
from pages.saby_contacts_page import SabyContactsPage
from pages.tensor_main_page import TensorMainPage
from pages.tensor_about_page import TensorAboutPage

def test_first_scenario(driver):
    """Тест первого сценария: переход со страницы контактов Saby.ru на Tensor.ru"""
    logger = logging.getLogger(__name__)
    logging.info("Запуск первого сценария")

    saby_page = SabyContactsPage(driver)
    tensor_main = TensorMainPage(driver)
    tensor_about = TensorAboutPage(driver)

    # 1. Saby контакты
    logger.info("1. Открываем saby.ru")
    saby_page.open_page()
    
    logger.info("2. Открываем меню контактов")
    saby_page.click_contacts_button()
    
    logger.info("3. Переходим в контакты и ждем редирект в регион")
    saby_page.click_contacts_link()
    
    current_url = saby_page.get_current_url()
    assert "/contacts" in current_url, f"Не перешли на страницу контактов. Текущий URL: {current_url}"
    logger.info(f"4. Страница контактов загружена: {current_url}")

    # 2. Баннер Тензор
    logger.info("5. Кликаем на баннер Тензор")
    saby_page.click_tensor_banner()
    
    current_url = driver.current_url
    assert "tensor.ru" in current_url, f"Не перешли на tensor.ru. Текущий URL: {current_url}"
    logger.info(f"6. Перешли на tensor.ru: {current_url}")

    # 3. Проверка блока "Сила в людях"
    logger.info("7. Проверяем блок 'Сила в людях'")
    power_block = tensor_main.find_power_block()
    assert power_block.is_displayed(), "Блок 'Сила в людях' не найден"
    logger.info("Блок 'Сила в людях' найден и отображается")

    # 4. Переход в Подробнее
    logger.info("8. Кликаем на 'Подробнее'")
    tensor_main.click_details()
    
    current_url = driver.current_url
    assert "tensor.ru/about" in current_url, f"Не перешли на страницу about. Текущий URL: {current_url}"
    logger.info("9. Успешно перешли на страницу about")

    # 5. Проверка изображений
    logger.info("10. Проверяем размеры изображений")
    images = tensor_about.find_working_images()
    
    if len(images) == 0:
        raise AssertionError("Изображения не найдены на странице")
    elif len(images) < 2:
        logger.warning(f"Найдено менее 2 изображений ({len(images)})")
    else:
        # Получаем свежие элементы перед проверкой размеров
        images = tensor_about.find_working_images()
        first_size = images[0].size
        logger.info(f"Сравниваем размеры {len(images)} изображений")
        
        for i, img in enumerate(images[1:], 2):
            # Получаем свежий элемент для каждой итерации
            current_images = tensor_about.find_working_images()
            if i - 1 < len(current_images):
                img_size = current_images[i - 1].size
                assert img_size == first_size, f"Изображение {i} имеет другой размер: {img_size} vs {first_size}"
        
        logger.info(f"Все {len(images)} изображений одинакового размера: {first_size}")
    
    logger.info("ПЕРВЫЙ СЦЕНАРИЙ УСПЕШНО ВЫПОЛНЕН!")
