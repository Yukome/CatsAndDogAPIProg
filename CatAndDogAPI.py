import os
import asyncio
import aiohttp
from dotenv import load_dotenv

load_dotenv()

api_url_cats = 'https://api.api-ninjas.com/v1/cats'
api_url_dogs = 'https://api.api-ninjas.com/v1/dogs'

X_API_KEY = os.getenv('X_API_KEY')

async def get_breeds_cats_inf(session, breed):
    headers = {
        'X-Api-Key': X_API_KEY,
        'User-Agent': 'Chrome/91.0.4472.124',
        'Accept': 'application/json'
    }
    params = {'name': breed['name']}
    try:
        async with session.get(api_url_cats, headers=headers, params=params) as response:
            if response.status == 200:
                json = await response.json()
                if json and isinstance(json, list) and len(json) > 0:
                    info = json[0]
                    return (
                        breed['name'],
                        info.get('image_link', 'N/A'),
                        info.get('length', 'N/A'),
                        info.get('origin', 'N/A'),
                        info.get('min_weight', 'N/A'),
                        info.get('max_weight', 'N/A'),
                        info.get('min_life_expectancy', 'N/A'),
                        info.get('max_life_expectancy', 'N/A'),
                        info.get('shedding', 'N/A'),
                        info.get('family_friendly', 'N/A'),
                        info.get('playfulness', 'N/A'),
                        info.get('grooming', 'N/A'),
                        info.get('other_pets_friendly', 'N/A'),
                        info.get('children_friendly', 'N/A'),
                        info.get('intelligence', 'N/A'),
                        info.get('general_health', 'N/A')
                    )
            return (breed['name'],) + ('N/A',) * 10
    except Exception as e:
        print(f"Request failed: {str(e)}")
        return (breed['name'],) + ('N/A',) * 10

async def get_breeds_dogs_inf(session, breed):
    headers = {
        'X-Api-Key': X_API_KEY,
        'User-Agent': 'Chrome/91.0.4472.124',
        'Accept': 'application/json'
    }
    params = {'name': breed['name']}
    try:
        async with session.get(api_url_dogs, headers=headers, params=params) as response:
            if response.status == 200:
                json = await response.json()
                if json and isinstance(json, list) and len(json) > 0:
                    info = json[0]
                    return (
                        breed['name'],
                        info.get('image_link', 'N/A'),
                        info.get('min_height_male', 'N/A'),
                        info.get('max_height_male', 'N/A'),
                        info.get('min_weight_male', 'N/A'),
                        info.get('max_weight_male', 'N/A'),
                        info.get('min_height_female', 'N/A'),
                        info.get('max_height_female', 'N/A'),
                        info.get('min_weight_female', 'N/A'),
                        info.get('max_weight_female', 'N/A'),
                        info.get('min_life_expectancy', 'N/A'),
                        info.get('max_life_expectancy', 'N/A'),
                        info.get('shedding', 'N/A'),
                        info.get('barking', 'N/A'),
                        info.get('energy', 'N/A'),
                        info.get('protectiveness', 'N/A'),
                        info.get('trainability', 'N/A'),
                        info.get('good_with_children', 'N/A'),
                        info.get('good_with_other_dogs', 'N/A'),
                        info.get('good_with_strangers', 'N/A'),
                        info.get('grooming', 'N/A'),
                        info.get('drooling', 'N/A'),
                        info.get('coat_length', 'N/A'),
                        info.get('playfulness', 'N/A')
                    )
            return (breed['name'],) + ('N/A',) * 10
    except Exception as e:
        print(f"Request failed: {str(e)}")
        return (breed['name'],) + ('N/A',) * 10

async def get_breeds_async(breeds, is_cat=True):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for breed in breeds:
            if is_cat:
                tasks.append(get_breeds_cats_inf(session, breed))
            else:
                tasks.append(get_breeds_dogs_inf(session, breed))
        return await asyncio.gather(*tasks)

async def fetch_breeds():
    try:
        async with aiohttp.ClientSession() as session:
            params = {'min_life_expectancy': 1}
            headers = {
                'X-Api-Key': X_API_KEY,
                'User-Agent': 'Chrome/91.0.4472.124',
                'Accept': 'application/json'
            }
            async with session.get(
                    api_url_cats,
                    headers=headers,
                    params=params
            ) as resp_cats:
                if resp_cats.status != 200:
                    error = await resp_cats.text()
                    print(f"Cat API Error: {resp_cats.status} - {error}")
                    return None, None
                cats_data = await resp_cats.json()

            async with session.get(
                    api_url_dogs,
                    headers=headers,
                    params=params
            ) as resp_dogs:
                if resp_dogs.status != 200:
                    error = await resp_dogs.text()
                    print(f"Dog API Error: {resp_dogs.status} - {error}")
                    return None, None
                dogs_data = await resp_dogs.json()

            breeds_cats = cats_data if isinstance(cats_data, list) else cats_data.get('cats', [])
            breeds_dogs = dogs_data if isinstance(dogs_data, list) else dogs_data.get('dogs', [])

            print(f"Найдено {len(breeds_cats)} кошек и {len(breeds_dogs)} собак")

            if not breeds_cats or not breeds_dogs:
                print("Пустые данные. Проверьте параметры запроса.")
                return None, None

            return breeds_cats, breeds_dogs

    except Exception as e:
        print(f"Ошибка соединения: {str(e)}")
        return None, None

async def show_breeds_pages(combined_breeds):
    pages = {i + 1: {1: {'type': animal_type, 'breed': breed}}
             for i, (animal_type, breed) in enumerate(combined_breeds)}
    page = 1
    last_page = len(pages)

    while True:
        os.system('cls')
        print(f'Страница {page}/{last_page}')

        current_page_data = pages[page][1]
        animal_type = current_page_data['type']
        breed_data = current_page_data['breed']

        results = await get_breeds_async([breed_data], is_cat=(animal_type == 'cat'))
        breed_info = results[0]

        print(f"\n--- {'Кошка' if animal_type == 'cat' else 'Собака'} ---")
        print(f"Порода: {breed_info[0]}")

        if animal_type == 'cat':
            print(f"Ссылка на картинку: {breed_info[1]}")
            print(f"Длина: {breed_info[2]}")
            print(f"Место происхождения: {breed_info[3]}")
            print(f"Мин. вес: {breed_info[4]} фунтов")
            print(f"Макс. вес: {breed_info[5]} фунтов")
            print(f"Мин. продолжительность жизни: {breed_info[6]} лет")
            print(f"Макс. продолжительность жизни: {breed_info[7]} лет")
            print(f"Сколько шерсти линяет кошка (от 1 до 5): {breed_info[8]}")
            print(f"Насколько ласкова кошка к семье (от 1 до 5): {breed_info[9]}")
            print(f"Насколько игрив кот (от 1 до 5): {breed_info[10]}")
            print(f"Сколько работы требуется для правильного ухода за кошкой (от 1 до 5): {breed_info[11]}")
            print(f"Насколько хорошо кошка ладит с другими домашними животными в доме (от 1 до 5): {breed_info[12]}")
            print(f"Насколько хорошо кошка ладит с детьми (от 1 до 5): {breed_info[13]}")
            print(f"Оценка интеллекта (от 1 до 5): {breed_info[14]}")
            print(f"Общая оценка здоровья (от 1 до 5): {breed_info[15]}")
        else:
            print(f"Ссылка на картинку: {breed_info[1]}")
            print("--Пол: male--")
            print(f"Мин. рост: {breed_info[2]} дюймов")
            print(f"Макс. рост: {breed_info[3]} дюймов")
            print(f"Мин. вес: {breed_info[4]} фунтов")
            print(f"Макс. вес: {breed_info[5]} фунтов")
            print("--Пол: female--")
            print(f"Мин. рост: {breed_info[6]} дюймов")
            print(f"Макс. рост: {breed_info[7]} дюймов")
            print(f"Мин. вес: {breed_info[8]} фунтов")
            print(f"Макс. вес: {breed_info[9]} фунтов")
            print(f"Мин. продолжительность жизни: {breed_info[10]} лет")
            print(f"Макс. продолжительность жизни: {breed_info[11]} лет")
            print(f"Сколько шерсти линяет собака (от 1 до 5): {breed_info[12]}")
            print(f"Склонность к лаю (от 1 до 5): {breed_info[13]}")
            print(f"Энергичность (от 1 до 5): {breed_info[14]}")
            print(f"Защитные качества (от 1 до 5): {breed_info[15]}")
            print(f"Обучаемость (от 1 до 5): {breed_info[16]}")
            print(f"Насколько хорошо собака ладит с детьми (от 1 до 5): {breed_info[17]}")
            print(f"Насколько хорошо собака ладит с другими собаками (от 1 до 5): {breed_info[18]}")
            print(f"Насколько хорошо собака ладит с незнакомцами (от 1 до 5): {breed_info[19]}")
            print(f"Сколько работы требуется для правильного ухода за собакой (от 1 до 5): {breed_info[20]}")
            print(f"Насколько сильно проявляется слюнотечение (от 1 до 5): {breed_info[21]}")
            print(f"Насколько длинная шерсть (от 1 до 5): {breed_info[22]}")
            print(f"Насколько игрива собака (от 1 до 5): {breed_info[23]}")

        print("-" * 50)

        if page == 1 and last_page > 1:
            menu = '1-След. порода\n0-Выход\nВведите действие: '
        elif page == last_page and last_page > 1:
            menu = '2-Пред. порода\n0-Выход\nВведите действие: '
        elif last_page == 1:
            menu = '0-Выход\nВведите действие: '
        else:
            menu = '1-След. порода\n2-Пред. порода\n0-Выход\nВведите действие: '

        choice = input(menu).strip()

        if choice == '0':
            break
        elif choice == '1' and page < last_page:
            page += 1
        elif choice == '2' and page > 1:
            page -= 1
        else:
            print('Неверная команда')
            input('Нажмите Enter чтобы продолжить...')

async def pet_selection_test(breeds_cats, breeds_dogs):
    os.system('cls')
    print("=== Подбор домашнего животного ===")
    choice = -1
    while choice != 0:
        print("-Выберите тип животного:")
        print("1 - Кошка/кот")
        print("2 - Собака")
        print("0 - Назад")
        choice = input("Выбор: ").strip()

        if choice == '0':
            break
        elif choice == '1':
            await cat_questions(breeds_cats)
        elif choice == '2':
            await dog_questions(breeds_dogs)
        else:
            print('Неправильное значение')
            input('Нажмите Enter чтобы продолжить...')

async def cat_questions(breeds_cats):
    client_answers = {}
    try:
        print("\n-Насколько дружелюбного кота Вы хотели бы? (1-5)")
        friendly = int(input("Ответ: ").strip())
        if not 1 <= friendly <= 5:
            print("Должно быть число от 1 до 5")
            return
        client_answers['family_friendly'] = friendly

        print("\n-Насколько игривого кота Вы хотели бы? (1-5)")
        playfulness = int(input("Ответ: ").strip())
        if not 1 <= playfulness <= 5:
            print("Должно быть число от 1 до 5")
            return
        client_answers['playfulness'] = playfulness

        print("\n-Насколько сильно линяющим кот может быть (макс.)? (1-5)")
        shedding = int(input("Ответ: ").strip())
        if not 1 <= shedding <= 5:
            print("Должно быть число от 1 до 5")
            return
        client_answers['shedding'] = shedding

        print("\n-Насколько придирчивым к уходу кот может быть (макс.)? (1-5)")
        grooming = int(input("Ответ: ").strip())
        if not 1 <= grooming <= 5:
            print("Должно быть число от 1 до 5")
            return
        client_answers['grooming'] = grooming

        print("\n-Какая оценка здоровья может быть (мин.)? (1-5)")
        general_health = int(input("Ответ: ").strip())
        if not 1 <= general_health <= 5:
            print("Должно быть число от 1 до 5")
            return
        client_answers['general_health'] = general_health

    except ValueError as e:
        print('Неверная команда')
        return

    filtered_breeds = []
    for breed in breeds_cats:
        results = await get_breeds_async([breed], is_cat=True)
        breed_info = results[0]

        breed_shedding = breed_info[8] if breed_info[8] != 'N/A' else 0
        breed_friendly = breed_info[9] if breed_info[9] != 'N/A' else 0
        breed_playful = breed_info[10] if breed_info[10] != 'N/A' else 0
        breed_grooming = breed_info[11] if breed_info[11] != 'N/A' else 0
        breed_general_health = breed_info[15] if breed_info[15] != 'N/A' else 0

        if (int(breed_shedding) <= client_answers['shedding'] and
                int(breed_friendly) >= client_answers['family_friendly'] and
                int(breed_playful) >= client_answers['playfulness'] and
                int(breed_grooming) <= client_answers['grooming'] and
                int(breed_general_health) >= client_answers['general_health']):
            filtered_breeds.append(breed)

    if not filtered_breeds:
        print("\nНет подходящих пород по вашим критериям.")
        input("Нажмите Enter чтобы продолжить...")
        return

    pages = {i + 1: {'breed': breed}
             for i, breed in enumerate(filtered_breeds)}
    page = 1
    last_page = len(pages)

    while True:
        os.system('cls')
        print(f"=== Подходящие породы кошек (страница {page}/{last_page}) ===")
        print("Ваши предпочтения:")
        print(f"- Линька: {client_answers['shedding']}/5")
        print(f"- Дружелюбие: {client_answers['family_friendly']}/5")
        print(f"- Игривость: {client_answers['playfulness']}/5")
        print(f"- Уход: {client_answers['grooming']}/5")
        print(f"- Общее здоровье: {client_answers['general_health']}/5")
        print("-" * 50)

        current_breed = pages[page]['breed']
        results = await get_breeds_async([current_breed], is_cat=True)
        breed_info = results[0]

        print(f"\nПорода: {breed_info[0]}")
        print(f"Ссылка на картинку: {breed_info[1]}")
        print(f"Длина: {breed_info[2]}")
        print(f"Место происхождения: {breed_info[3]}")
        print(f"Мин. вес: {breed_info[4]} фунтов")
        print(f"Макс. вес: {breed_info[5]} фунтов")
        print(f"Мин. продолжительность жизни: {breed_info[6]} лет")
        print(f"Макс. продолжительность жизни: {breed_info[7]} лет")
        print(f"Линька: {breed_info[8]}/5 (ваш выбор: {client_answers['shedding']})")
        print(f"Дружелюбие: {breed_info[9]}/5 (ваш выбор: {client_answers['family_friendly']})")
        print(f"Игривость: {breed_info[10]}/5 (ваш выбор: {client_answers['playfulness']})")
        print(f"Уход: {breed_info[11]}/5 (ваш выбор: {client_answers['grooming']})")
        print(f"Насколько хорошо кошка ладит с другими домашними животными в доме (от 1 до 5): {breed_info[12]}")
        print(f"Насколько хорошо кошка ладит с детьми (от 1 до 5): {breed_info[13]}")
        print(f"Оценка интеллекта (от 1 до 5): {breed_info[14]}")
        print(f"Здоровье: {breed_info[15]}/5 (ваш выбор: {client_answers['general_health']})")

        if page == 1 and last_page > 1:
            menu = '1-След. порода\n0-Выход\nВведите действие: '
        elif page == last_page and last_page > 1:
            menu = '2-Пред. порода\n0-Выход\nВведите действие: '
        elif last_page == 1:
            menu = '0-Выход\nВведите действие: '
        else:
            menu = '1-След. порода\n2-Пред. порода\n0-Выход\nВведите действие: '

        choice = input(menu).strip()

        if choice == '0':
            break
        elif choice == '1' and page < last_page:
            page += 1
        elif choice == '2' and page > 1:
            page -= 1
        else:
            print('Неверная команда')
            input('Нажмите Enter чтобы продолжить...')

async def dog_questions(breeds_dogs):
    client_answers = {}
    try:
        print("\n-Насколько энергичную собаку Вы хотели бы (макс.)? (1-5)")
        energy = int(input("Ответ: ").strip())
        if not 1 <= energy <= 5:
            print("Должно быть число от 1 до 5")
            return
        client_answers['energy'] = energy

        print("\n-Насколько вокальную собаку Вы хотели бы (макс.)? (1-5)")
        barking = int(input("Ответ: ").strip())
        if not 1 <= barking <= 5:
            print("Должно быть число от 1 до 5")
            return
        client_answers['barking'] = barking

        print("\n-Насколько сильно линяющей собака может быть (макс.)? (1-5)")
        shedding = int(input("Ответ: ").strip())
        if not 1 <= shedding <= 5:
            print("Должно быть число от 1 до 5")
            return
        client_answers['shedding'] = shedding

        print("\n-Насколько придирчивой к уходу собака может быть (макс.)? (1-5)")
        grooming = int(input("Ответ: ").strip())
        if not 1 <= grooming <= 5:
            print("Должно быть число от 1 до 5")
            return
        client_answers['grooming'] = grooming

        print("\n-Насколько способной к обучению собака может быть (мин.)? (1-5)")
        trainability = int(input("Ответ: ").strip())
        if not 1 <= trainability <= 5:
            print("Должно быть число от 1 до 5")
            return
        client_answers['trainability'] = trainability

        print("\n-Насколько дружелюбной собака может быть (мин.)? (1-5)")
        good_with_strangers = int(input("Ответ: ").strip())
        if not 1 <= good_with_strangers <= 5:
            print("Должно быть число от 1 до 5")
            return
        client_answers['good_with_strangers'] = good_with_strangers

        print("\n-Насколько хорошие защитные качества может иметь собака (мин.)? (1-5)")
        protectiveness = int(input("Ответ: ").strip())
        if not 1 <= protectiveness <= 5:
            print("Должно быть число от 1 до 5")
            return
        client_answers['protectiveness'] = protectiveness

    except ValueError as e:
        print('Неверная команда')
        return

    filtered_breeds = []
    for breed in breeds_dogs:
        results = await get_breeds_async([breed], is_cat=False)
        breed_info = results[0]

        breed_shedding = breed_info[12] if breed_info[12] != 'N/A' else 0
        breed_barking = breed_info[13] if breed_info[13] != 'N/A' else 0
        breed_energy = breed_info[14] if breed_info[14] != 'N/A' else 0
        breed_protectiveness = breed_info[15] if breed_info[15] != 'N/A' else 0
        breed_trainability = breed_info[16] if breed_info[16] != 'N/A' else 0
        breed_good_with_strangers = breed_info[19] if breed_info[19] != 'N/A' else 0
        breed_grooming = breed_info[20] if breed_info[20] != 'N/A' else 0

        if (int(breed_shedding) <= client_answers['shedding'] and
                int(breed_barking) <= client_answers['barking'] and
                int(breed_energy) <= client_answers['energy'] and
                int(breed_protectiveness) >= client_answers['protectiveness'] and
                int(breed_trainability) >= client_answers['trainability'] and
                int(breed_good_with_strangers) >= client_answers['good_with_strangers'] and
                int(breed_grooming) <= client_answers['grooming']):
            filtered_breeds.append(breed)

    if not filtered_breeds:
        print("\nНет подходящих пород по вашим критериям.")
        input("Нажмите Enter чтобы продолжить...")
        return

    pages = {i + 1: {'breed': breed}
             for i, breed in enumerate(filtered_breeds)}
    page = 1
    last_page = len(pages)

    while True:
        os.system('cls')
        print(f"=== Подходящие породы собак (страница {page}/{last_page}) ===")
        print("Ваши предпочтения:")
        print(f"- Линька: {client_answers['shedding']}/5")
        print(f"- Лай/голос: {client_answers['barking']}/5")
        print(f"- Энергичность: {client_answers['energy']}/5")
        print(f"- Навыки защиты: {client_answers['protectiveness']}/5")
        print(f"- Обучаемость: {client_answers['trainability']}/5")
        print(f"- Дружелюбие: {client_answers['good_with_strangers']}/5")
        print(f"- Уход: {client_answers['grooming']}/5")
        print("-" * 50)

        current_breed = pages[page]['breed']
        results = await get_breeds_async([current_breed], is_cat=False)
        breed_info = results[0]

        print(f"\nПорода: {breed_info[0]}")
        print(f"Ссылка на картинку: {breed_info[1]}")
        print("--Пол: male--")
        print(f"Мин. рост: {breed_info[2]} дюймов")
        print(f"Макс. рост: {breed_info[3]} дюймов")
        print(f"Мин. вес: {breed_info[4]} фунтов")
        print(f"Макс. вес: {breed_info[5]} фунтов")
        print("--Пол: female--")
        print(f"Мин. рост: {breed_info[6]} дюймов")
        print(f"Макс. рост: {breed_info[7]} дюймов")
        print(f"Мин. вес: {breed_info[8]} фунтов")
        print(f"Макс. вес: {breed_info[9]} фунтов")
        print(f"Мин. продолжительность жизни: {breed_info[10]} лет")
        print(f"Макс. продолжительность жизни: {breed_info[11]} лет")
        print(f"Линька: {breed_info[12]}/5 (ваш выбор: {client_answers['shedding']})")
        print(f"Склонность к лаю: {breed_info[13]}/5 (ваш выбор: {client_answers['barking']})")
        print(f"Энергичность: {breed_info[14]}/5 (ваш выбор: {client_answers['energy']})")
        print(f"Защитные качества: {breed_info[15]}/5 (ваш выбор: {client_answers['protectiveness']})")
        print(f"Обучаемость: {breed_info[16]}/5 (ваш выбор: {client_answers['trainability']})")
        print(f"Дружелюбие: {breed_info[19]}/5 (ваш выбор: {client_answers['good_with_strangers']})")
        print(f"Уход: {breed_info[20]}/5 (ваш выбор: {client_answers['grooming']})")
        print(f"Насколько сильно проявляется слюнотечение (от 1 до 5): {breed_info[21]}")
        print(f"Насколько длинная шерсть (от 1 до 5): {breed_info[22]}")
        print(f"Насколько игрива собака (от 1 до 5): {breed_info[23]}")

        if page == 1 and last_page > 1:
            menu = '1-След. порода\n0-Выход\nВведите действие: '
        elif page == last_page and last_page > 1:
            menu = '2-Пред. порода\n0-Выход\nВведите действие: '
        elif last_page == 1:
            menu = '0-Выход\nВведите действие: '
        else:
            menu = '1-След. порода\n2-Пред. порода\n0-Выход\nВведите действие: '

        choice = input(menu).strip()

        if choice == '0':
            break
        elif choice == '1' and page < last_page:
            page += 1
        elif choice == '2' and page > 1:
            page -= 1
        else:
            print('Неверная команда')
            input('Нажмите Enter чтобы продолжить...')

async def main():
    breeds_cats, breeds_dogs = await fetch_breeds()
    if breeds_cats is None or breeds_dogs is None:
        print("Не удалось получить данные о породах. Проверьте подключение к интернету и API ключ.")
        exit(-1)

    while True:
        os.system('cls')
        print("=== Главное меню ===")
        print("1 - Просмотр пород (постранично)")
        print("2 - Тест подбора домашнего животного")
        print("0 - Выход")
        choice = input("Выберите действие: ").strip()

        if choice == '0':
            break
        elif choice == '1':
            combined_breeds = []
            max_len = max(len(breeds_cats), len(breeds_dogs))
            for i in range(max_len):
                if i < len(breeds_cats):
                    combined_breeds.append(('cat', breeds_cats[i]))
                if i < len(breeds_dogs):
                    combined_breeds.append(('dog', breeds_dogs[i]))
            await show_breeds_pages(combined_breeds)
        elif choice == '2':
            await pet_selection_test(breeds_cats, breeds_dogs)
        else:
            print('Неверная команда')
            input('Нажмите Enter чтобы продолжить...')

if __name__ == "__main__":
    asyncio.run(main())