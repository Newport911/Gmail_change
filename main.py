import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# Функция для сохранения данных в CSV.
def save_to_csv(data):
    with open('user_data.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)


# Функция для изменения имени и фамилии
def change_name(driver, new_first_name, new_last_name):
    driver.get('https://myaccount.google.com/personal-info')
    time.sleep(3)  # Ожидание загрузки страницы

    # Поиск и клик по кнопке "Имя"
    name_button = driver.find_element(By.XPATH, "//span[text()='Имя']/..")
    name_button.click()

    # Ожидание загрузки страницы редактирования имени
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'firstName')))

    # Изменение имени
    first_name_input = driver.find_element(By.NAME, 'firstName')
    last_name_input = driver.find_element(By.NAME, 'lastName')

    first_name_input.clear()
    first_name_input.send_keys(new_first_name)

    last_name_input.clear()
    last_name_input.send_keys(new_last_name)

    # Сохранение изменений
    save_button = driver.find_element(By.XPATH, "//span[text()='Сохранить']/..")
    save_button.click()

    time.sleep(2)  # Ожидание завершения сохранения изменений


# Функция для изменения пароля
def change_password(driver, current_password, new_password):
    driver.get('https://myaccount.google.com/security')
    time.sleep(3)

    # Поиск и клик по кнопке "Пароль"
    password_button = driver.find_element(By.XPATH, "//span[text()='Пароль']/..")
    password_button.click()

    # Ввод текущего пароля
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'password')))
    current_password_input = driver.find_element(By.NAME, 'password')
    current_password_input.send_keys(current_password)
    current_password_input.send_keys(Keys.ENTER)

    # Ввод нового пароля
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'password')))
    new_password_input = driver.find_element(By.NAME, 'password')
    confirm_password_input = driver.find_element(By.NAME, 'confirmationPassword')

    new_password_input.send_keys(new_password)
    confirm_password_input.send_keys(new_password)

    # Сохранение изменений
    save_button = driver.find_element(By.XPATH, "//span[text()='Сменить пароль']/..")
    save_button.click()


# Основная функция для выполнения всех шагов
def main():
    # Запрос данных у пользователя
    email = input("Введите ваш email: ")
    current_password = input("Введите ваш текущий пароль: ")
    new_password = input("Введите ваш новый пароль: ")
    new_first_name = input("Введите ваше новое имя: ")
    new_last_name = input("Введите вашу новую фамилию: ")
    birthdate = input("Введите вашу дату рождения (ДД.ММ.ГГГГ): ")
    recovery_email = input("Введите резервный email: ")

    # Настройка Selenium
    options = Options()
    options.add_argument("--start-maximized")
    driver_service = Service('path_to_chromedriver')  # Укажите путь к вашему chromedriver
    driver = webdriver.Chrome(service=driver_service, options=options)

    try:
        # Открываем Gmail и логинимся
        driver.get('https://accounts.google.com/signin/v2/identifier?service=mail')

        # Ввод email
        email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "identifier")))
        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)

        # Ввод пароля
        password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "password")))
        password_input.send_keys(current_password)
        password_input.send_keys(Keys.ENTER)

        # Ожидание завершения загрузки
        time.sleep(5)

        # Изменение имени и фамилии
        change_name(driver, new_first_name, new_last_name)

        # Изменение пароля
        change_password(driver, current_password, new_password)

        # Сохранение данных в CSV
        save_to_csv([email, new_password, new_first_name, new_last_name, birthdate, recovery_email])

        print("Данные успешно изменены и сохранены.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
