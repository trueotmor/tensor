import logging

class TestSabyToTensor:
    def test_saby_to_tensor_flow(self, saby_contacts_page, tensor_about_page):
        """Первый сценарий: переход с Saby.ru на Tensor.ru и проверки"""
        
        # 1. Перейти на saby.ru в раздел "Контакты"
        saby_contacts_page.open_contacts()
        logging.info("Перешли в раздел Контакты на saby.ru")
        
        # 2. Найти баннер Тензор и кликнуть
        saby_contacts_page.click_tensor_banner()
        logging.info("Кликнули на баннер Тензор")
        
        # 3. Переключиться на новую вкладку и проверить URL
        windows = saby_contacts_page.driver.window_handles
        saby_contacts_page.driver.switch_to.window(windows[-1])
        assert "tensor.ru" in tensor_about_page.get_current_url()
        logging.info("Успешно перешли на tensor.ru")
        
        # 4. Проверить наличие блока "Сила в людях"
        assert tensor_about_page.is_power_in_people_displayed()
        logging.info("Блок 'Сила в людях' найден")
        
        # 5. Перейти в "Подробнее" и проверить URL
        tensor_about_page.click_details()
        assert tensor_about_page.get_current_url() == "https://tensor.ru/about"
        logging.info("Успешно перешли на страницу 'О тензоре'")
        
        # 6. Проверить размеры фотографий в разделе "Работаем"
        images_sizes = tensor_about_page.get_working_images_sizes()
        
        if len(images_sizes) > 1:
            first_size = images_sizes[0]
            for i, size in enumerate(images_sizes[1:], 1):
                assert size['width'] == first_size['width'], f"Ширина изображения {i} не совпадает"
                assert size['height'] == first_size['height'], f"Высота изображения {i} не совпадает"
        
        logging.info("Все изображения имеют одинаковые размеры")