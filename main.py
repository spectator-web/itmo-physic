
# import math

# # Попытка импорта scipy.stats для расчёта коэффициента Стьюдента
# try:
#     from scipy import stats
#     SCIPY_AVAILABLE = True
# except ImportError:
#     SCIPY_AVAILABLE = False
#     print("Библиотека SciPy не установлена. Автоматический расчёт коэффициента Стьюдента недоступен.")
#     print("Установите её командой: pip install scipy\n")


# # ------------------------------------------------------------
# # 1. Чтение данных из файла (без изменений)
# # ------------------------------------------------------------
# def read_measurement_blocks(filename="labs/lab1.txt"):
#     """
#     Читает файл, содержащий блоки измерений, разделённые строками '---'.
#     Возвращает список кортежей: [(количество_измерений, [значения]), ...].
#     """
#     blocks = []
#     try:
#         with open(filename, 'r', encoding='utf-8') as f:
#             lines = [line.strip() for line in f if line.strip() != '']
#     except FileNotFoundError:
#         print(f"Ошибка: файл '{filename}' не найден.")
#         return []

#     i = 0
#     while i < len(lines):
#         if lines[i] == '---':
#             i += 1
#             block_lines = []
#             while i < len(lines) and lines[i] != '---':
#                 block_lines.append(lines[i])
#                 i += 1
#             if i < len(lines) and lines[i] == '---':
#                 i += 1

#             if block_lines:
#                 try:
#                     count = int(block_lines[0])
#                     values = [float(x.replace(',', '.')) for x in block_lines[1:]]
#                     if len(values) != count:
#                         print(f"Предупреждение: в блоке ожидалось {count} значений, получено {len(values)}")
#                     blocks.append((count, values))
#                 except ValueError as e:
#                     print(f"Ошибка преобразования чисел в блоке: {e}")
#         else:
#             i += 1

#     if not blocks:
#         print("В файле не найдено ни одного блока данных.")
#     return blocks


# # ------------------------------------------------------------
# # 2. Вспомогательная функция: парсинг числа (десятичного или дроби)
# # ------------------------------------------------------------
# def parse_number(s):
#     """Преобразует строку в число с плавающей точкой, поддерживает запятую и дробь вида a/b."""
#     s = s.strip().replace(',', '.')
#     if '/' in s:
#         parts = s.split('/')
#         if len(parts) == 2:
#             try:
#                 return float(parts[0]) / float(parts[1])
#             except ValueError:
#                 return None
#         else:
#             return None
#     else:
#         try:
#             return float(s)
#         except ValueError:
#             return None


# # ------------------------------------------------------------
# # 3. Обработка данных (расчёт статистик и полной погрешности)
# # ------------------------------------------------------------
# def process_data(blocks, t_coef, instr_error):
#     """
#     Выполняет статистическую обработку каждого блока измерений.
#     Выводит среднее, случайную погрешность (t·SEM), приборную погрешность,
#     полную погрешность, относительную погрешность и доверительный интервал.
#     """
#     if not blocks:
#         print("Нет данных для обработки. Сначала выполните пункт 1.")
#         return

#     print("\n--- ОБРАБОТКА ДАННЫХ (ПОЛНАЯ ПОГРЕШНОСТЬ) ---")
#     print(f"Коэффициент Стьюдента t = {t_coef:.3f}")
#     print(f"Приборная погрешность Δпр = {instr_error:.4f}")
#     print("-" * 70)

#     for i, (n, values) in enumerate(blocks, 1):
#         avg = sum(values) / n

#         # Выборочное СКО
#         if n > 1:
#             std_dev = math.sqrt(sum((x - avg) ** 2 for x in values) / (n - 1))
#         else:
#             std_dev = 0.0

#         # Стандартная погрешность среднего (SEM)
#         sem = std_dev / math.sqrt(n) if n > 0 else 0.0

#         # Случайная погрешность (доверительный интервал)
#         random_error = t_coef * sem

#         # Полная погрешность (квадратичное суммирование)
#         total_error = math.sqrt(random_error ** 2 + instr_error ** 2)

#         # Относительная погрешность в процентах
#         if avg != 0:
#             relative_error = (total_error / abs(avg)) * 100
#             rel_str = f"{relative_error:.2f}%"
#         else:
#             rel_str = "не определена (среднее = 0)"

#         print(f"Блок {i}: n = {n}")
#         print(f"  Среднее арифм.   = {avg:.6f}")
#         print(f"  СКО выборки      = {std_dev:.6f}")
#         print(f"  СКО среднего     = {sem:.6f}")
#         print(f"  Случайная погр.  = ±{random_error:.6f}  (t·SEM)")
#         print(f"  Приборная погр.  = ±{instr_error:.4f}")
#         print(f"  ПОЛНАЯ ПОГРЕШН.  = ±{total_error:.6f}")
#         print(f"  Относительная    = {rel_str}")
#         print(f"  Результат: {avg:.6f} ± {total_error:.6f}  ({rel_str})")
#         print(f"  Доверительный интервал: [{avg - total_error:.6f}, {avg + total_error:.6f}]\n")


# # ------------------------------------------------------------
# # 4. Ввод нового коэффициента Стьюдента (ручной)
# # ------------------------------------------------------------
# def set_t_coef():
#     while True:
#         s = input("Введите коэффициент Стьюдента (например, 2.0, 1.96, 2.58): ")
#         val = parse_number(s)
#         if val is not None and val > 0:
#             return val
#         print("Ошибка: введите положительное число.")


# # ------------------------------------------------------------
# # 5. Ввод новой приборной погрешности
# # ------------------------------------------------------------
# def set_instr_error():
#     while True:
#         s = input("Введите приборную погрешность (можно дробь, напр. 0.5 или 2/3): ")
#         val = parse_number(s)
#         if val is not None and val > 0:
#             return val
#         print("Ошибка: введите положительное число.")


# # ------------------------------------------------------------
# # 6. Вычисление коэффициента Стьюдента по вероятности и степени свободы
# # ------------------------------------------------------------
# def compute_student_t():
#     """
#     Запрашивает доверительную вероятность и число измерений (или степень свободы),
#     вычисляет коэффициент Стьюдента с помощью scipy.stats.t.ppf,
#     и предлагает установить его в качестве текущего.
#     Возвращает новое значение коэффициента или None, если не был изменён.
#     """
#     if not SCIPY_AVAILABLE:
#         print("Библиотека SciPy не установлена. Автоматический расчёт невозможен.")
#         print("Пожалуйста, установите SciPy или введите коэффициент вручную (пункт 3).")
#         return None

#     print("\n--- ВЫЧИСЛЕНИЕ КОЭФФИЦИЕНТА СТЬЮДЕНТА ---")
#     # Ввод доверительной вероятности
#     while True:
#         prob_str = input("Введите доверительную вероятность (например, 0.95, 0.99): ")
#         prob = parse_number(prob_str)
#         if prob is not None and 0 < prob < 1:
#             break
#         print("Ошибка: введите число между 0 и 1.")
    
#     # Ввод числа измерений (или напрямую степени свободы)
#     print("Введите количество измерений n (или непосредственно степень свободы).")
#     while True:
#         n_str = input("Число измерений (n) > 0: ")
#         n_val = parse_number(n_str)
#         if n_val is not None and n_val > 0:
#             # Если это число с плавающей точкой и близко к целому, преобразуем
#             if abs(n_val - round(n_val)) < 1e-9:
#                 n_int = int(round(n_val))
#             else:
#                 n_int = int(n_val)  # отбрасываем дробную часть
#             if n_int > 0:
#                 break
#         print("Ошибка: введите целое положительное число.")

#     df = n_int - 1  # степень свободы
#     try:
#         # Двусторонний квантиль: t_{1 - (1-p)/2, df}
#         t_value = stats.t.ppf((1 + prob) / 2, df)
#         print(f"\nДля доверительной вероятности P = {prob} и степени свободы df = {df}:")
#         print(f"  Коэффициент Стьюдента t = {t_value:.6f}")
#     except Exception as e:
#         print(f"Ошибка при вычислении: {e}")
#         return None

#     # Предложение установить это значение
#     ans = input("Установить этот коэффициент как текущий? (y/n): ").strip().lower()
#     if ans in ('y', 'yes', 'д', 'да'):
#         return t_value
#     else:
#         print("Коэффициент не изменён.")
#         return None


# # ------------------------------------------------------------
# # 7. Главная программа с меню
# # ------------------------------------------------------------
# def main():
#     filename = "labs/lab1.txt"   # путь к файлу по умолчанию
#     blocks = []                  # загруженные данные
#     t_student = 2.0              # коэффициент Стьюдента (по умолч.)
#     instr_error = 0.5           # приборная погрешность (по умолч. 0.5 с)

#     while True:
#         print("\n" + "=" * 60)
#         print("   ЛАБОРАТОРНАЯ РАБОТА: ОБРАБОТКА РЕЗУЛЬТАТОВ ИЗМЕРЕНИЙ")
#         print("=" * 60)
#         print("1. Распаковать данные из файла")
#         print("2. Обработать данные (расчёт погрешностей)")
#         print("3. Изменить коэффициент Стьюдента (ручной ввод) (текущий: {:.3f})".format(t_student))
#         print("4. Изменить приборную погрешность (текущая: {:.4f})".format(instr_error))
#         print("5. Вычислить коэффициент Стьюдента по вероятности и n")
#         print("6. Выход")
#         print("-" * 60)

#         choice = input("Выберите действие (1-6): ").strip()

#         match choice:
#             case "1":
#                 blocks = read_measurement_blocks(filename)
#                 if blocks:
#                     print("\n--- ЗАГРУЖЕННЫЕ БЛОКИ ---")
#                     for i, (count, vals) in enumerate(blocks, 1):
#                         print(f"Блок {i}: {count} измерений")
#                         print(f"  Значения: {vals}")
#                 else:
#                     print("Данные не загружены.")

#             case "2":
#                 process_data(blocks, t_student, instr_error)

#             case "3":
#                 t_student = set_t_coef()
#                 print(f"Коэффициент Стьюдента установлен: {t_student:.3f}")

#             case "4":
#                 instr_error = set_instr_error()
#                 print(f"Приборная погрешность установлена: {instr_error:.4f}")

#             case "5":
#                 new_t = compute_student_t()
#                 if new_t is not None:
#                     t_student = new_t
#                     print(f"Коэффициент Стьюдента установлен автоматически: {t_student:.6f}")

#             case "6":
#                 print("Выход из программы.")
#                 break

#             case _:
#                 print("Неверный пункт меню. Попробуйте снова.")


# if __name__ == "__main__":
#     main()

import math

# Попытка импорта scipy.stats для расчёта коэффициента Стьюдента
try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("Библиотека SciPy не установлена. Автоматический расчёт коэффициента Стьюдента недоступен.")
    print("Установите её командой: pip install scipy\n")


# ------------------------------------------------------------
# 1. Чтение данных из файла
# ------------------------------------------------------------
def read_measurement_blocks(filename="labs/lab1.txt"):
    """
    Читает файл, содержащий блоки измерений, разделённые строками '---'.
    Возвращает список кортежей: [(количество_измерений, [значения]), ...].
    """
    blocks = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() != '']
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.")
        return []

    i = 0
    while i < len(lines):
        if lines[i] == '---':
            i += 1
            block_lines = []
            while i < len(lines) and lines[i] != '---':
                block_lines.append(lines[i])
                i += 1
            if i < len(lines) and lines[i] == '---':
                i += 1

            if block_lines:
                try:
                    count = int(block_lines[0])
                    values = [float(x.replace(',', '.')) for x in block_lines[1:]]
                    if len(values) != count:
                        print(f"Предупреждение: в блоке ожидалось {count} значений, получено {len(values)}")
                    blocks.append((count, values))
                except ValueError as e:
                    print(f"Ошибка преобразования чисел в блоке: {e}")
        else:
            i += 1

    if not blocks:
        print("В файле не найдено ни одного блока данных.")
    return blocks


# ------------------------------------------------------------
# 2. Парсинг числа (десятичная запись или дробь)
# ------------------------------------------------------------
def parse_number(s):
    """Преобразует строку в число с плавающей точкой, поддерживает запятую и дробь вида a/b."""
    s = s.strip().replace(',', '.')
    if '/' in s:
        parts = s.split('/')
        if len(parts) == 2:
            try:
                return float(parts[0]) / float(parts[1])
            except ValueError:
                return None
        else:
            return None
    else:
        try:
            return float(s)
        except ValueError:
            return None


# ------------------------------------------------------------
# 3. Обработка данных (полная погрешность)
# ------------------------------------------------------------
def process_data(blocks, t_coef, instr_error):
    """
    Выполняет статистическую обработку каждого блока измерений.
    Выводит среднее, случайную погрешность (t·SEM), приборную погрешность,
    полную погрешность, относительную погрешность и доверительный интервал.
    """
    if not blocks:
        print("Нет данных для обработки. Сначала выполните пункт 1.")
        return

    print("\n--- ОБРАБОТКА ДАННЫХ (ПОЛНАЯ ПОГРЕШНОСТЬ) ---")
    print(f"Коэффициент Стьюдента t = {t_coef:.3f}")
    print(f"Приборная погрешность Δпр = {instr_error:.4f}")
    print("-" * 70)

    for i, (n, values) in enumerate(blocks, 1):
        avg = sum(values) / n

        # Выборочное СКО
        if n > 1:
            std_dev = math.sqrt(sum((x - avg) ** 2 for x in values) / (n - 1))
        else:
            std_dev = 0.0

        # Стандартная погрешность среднего (SEM)
        sem = std_dev / math.sqrt(n) if n > 0 else 0.0

        # Случайная погрешность (доверительный интервал)
        random_error = t_coef * sem

        # Полная погрешность (квадратичное суммирование)
        total_error = math.sqrt(random_error ** 2 + instr_error ** 2)

        # Относительная погрешность в процентах
        if avg != 0:
            relative_error = (total_error / abs(avg)) * 100
            rel_str = f"{relative_error:.2f}%"
        else:
            rel_str = "не определена (среднее = 0)"

        print(f"Блок {i}: n = {n}")
        print(f"  Среднее арифм.   = {avg:.6f}")
        print(f"  СКО выборки      = {std_dev:.6f}")
        print(f"  СКО среднего     = {sem:.6f}")
        print(f"  Случайная погр.  = ±{random_error:.6f}  (t·SEM)")
        print(f"  Приборная погр.  = ±{instr_error:.4f}")
        print(f"  ПОЛНАЯ ПОГРЕШН.  = ±{total_error:.6f}")
        print(f"  Относительная    = {rel_str}")
        print(f"  Результат: {avg:.6f} ± {total_error:.6f}  ({rel_str})")
        print(f"  Доверительный интервал: [{avg - total_error:.6f}, {avg + total_error:.6f}]\n")


# ------------------------------------------------------------
# 4. Ручной ввод коэффициента Стьюдента
# ------------------------------------------------------------
def set_t_coef():
    while True:
        s = input("Введите коэффициент Стьюдента (например, 2.0, 1.96, 2.58): ")
        val = parse_number(s)
        if val is not None and val > 0:
            return val
        print("Ошибка: введите положительное число.")


# ------------------------------------------------------------
# 5. Ввод приборной погрешности
# ------------------------------------------------------------
def set_instr_error():
    while True:
        s = input("Введите приборную погрешность (можно дробь, напр. 0.5 или 2/3): ")
        val = parse_number(s)
        if val is not None and val > 0:
            return val
        print("Ошибка: введите положительное число.")


# ------------------------------------------------------------
# 6. Автоматическое вычисление коэффициента Стьюдента (scipy)
# ------------------------------------------------------------
def compute_student_t():
    """
    Запрашивает доверительную вероятность и число измерений,
    вычисляет коэффициент Стьюдента с помощью scipy.stats.t.ppf,
    и предлагает установить его в качестве текущего.
    """
    if not SCIPY_AVAILABLE:
        print("Библиотека SciPy не установлена. Автоматический расчёт невозможен.")
        print("Пожалуйста, установите SciPy или введите коэффициент вручную (пункт 3).")
        return None

    print("\n--- ВЫЧИСЛЕНИЕ КОЭФФИЦИЕНТА СТЬЮДЕНТА ---")
    while True:
        prob_str = input("Введите доверительную вероятность (например, 0.95, 0.99): ")
        prob = parse_number(prob_str)
        if prob is not None and 0 < prob < 1:
            break
        print("Ошибка: введите число между 0 и 1.")
    
    while True:
        n_str = input("Число измерений (n) > 0: ")
        n_val = parse_number(n_str)
        if n_val is not None and n_val > 0:
            n_int = int(n_val) if n_val == int(n_val) else int(n_val)  # округление вниз
            if n_int > 0:
                break
        print("Ошибка: введите целое положительное число.")

    df = n_int - 1
    try:
        t_value = stats.t.ppf((1 + prob) / 2, df)
        print(f"\nДля P = {prob} и df = {df}: t = {t_value:.6f}")
    except Exception as e:
        print(f"Ошибка при вычислении: {e}")
        return None

    ans = input("Установить этот коэффициент как текущий? (y/n): ").strip().lower()
    if ans in ('y', 'yes', 'д', 'да'):
        return t_value
    else:
        print("Коэффициент не изменён.")
        return None


# ------------------------------------------------------------
# 7. Детальный отчёт по СКО для выбранного блока
# ------------------------------------------------------------
def detailed_sigma_report(blocks):
    """
    Запрашивает номер блока и выводит подробные вычисления СКО:
    - среднее;
    - для каждого измерения: №, значение, отклонение, квадрат отклонения;
    - сумма квадратов отклонений;
    - СКО выборки;
    - СКО среднего.
    """
    if not blocks:
        print("Нет загруженных блоков. Сначала выполните пункт 1.")
        return

    print("\n--- ПОДРОБНЫЙ ОТЧЁТ ПО СКО ВЫБОРКИ ---")
    
    # Выбор блока
    num_blocks = len(blocks)
    print(f"Доступно блоков: {num_blocks}")
    while True:
        try:
            idx_str = input(f"Введите номер блока (1..{num_blocks}): ")
            idx = int(idx_str)
            if 1 <= idx <= num_blocks:
                break
            else:
                print(f"Номер должен быть от 1 до {num_blocks}.")
        except ValueError:
            print("Ошибка: введите целое число.")
    
    n, values = blocks[idx - 1]
    avg = sum(values) / n

    print(f"\nБлок {idx}: n = {n}")
    print(f"Среднее арифметическое = {avg:.6f}\n")

    # Заголовок таблицы
    print(" №   Значение      Отклонение     Квадрат отклонения")
    print("---  ------------  -------------  ------------------")

    sum_sq = 0.0
    for i, x in enumerate(values, 1):
        dev = x - avg
        sq = dev ** 2
        sum_sq += sq
        print(f"{i:3d}  {x:11.6f}  {dev:13.6f}  {sq:18.6f}")

    print("\n" + "-" * 60)
    print(f"Сумма квадратов отклонений = {sum_sq:.6f}")

    if n > 1:
        std_dev = math.sqrt(sum_sq / (n - 1))
        sem = std_dev / math.sqrt(n)
        print(f"СКО выборки = sqrt({sum_sq:.6f} / {n-1}) = {std_dev:.6f}")
        print(f"СКО среднего = {std_dev:.6f} / sqrt({n}) = {sem:.6f}")
    else:
        print("Для одного измерения СКО не определено.")
    print("-" * 60 + "\n")


# ------------------------------------------------------------
# 8. Главная программа с меню
# ------------------------------------------------------------
def main():
    filename = "labs/lab1.txt"   # путь к файлу по умолчанию
    blocks = []                  # загруженные данные
    t_student = 2.0              # коэффициент Стьюдента (по умолч.)
    instr_error = 0.5            # приборная погрешность (по умолч. 0.5 с)

    while True:
        print("\n" + "=" * 60)
        print("   ЛАБОРАТОРНАЯ РАБОТА: ОБРАБОТКА РЕЗУЛЬТАТОВ ИЗМЕРЕНИЙ")
        print("=" * 60)
        print("1. Распаковать данные из файла")
        print("2. Обработать данные (расчёт погрешностей)")
        print("3. Изменить коэффициент Стьюдента (ручной ввод) (текущий: {:.3f})".format(t_student))
        print("4. Изменить приборную погрешность (текущая: {:.4f})".format(instr_error))
        print("5. Вычислить коэффициент Стьюдента по вероятности и n")
        print("6. Подробный отчёт по СКО выборки (для блока)")
        print("7. Выход")
        print("-" * 60)

        choice = input("Выберите действие (1-7): ").strip()

        match choice:
            case "1":
                blocks = read_measurement_blocks(filename)
                if blocks:
                    print("\n--- ЗАГРУЖЕННЫЕ БЛОКИ ---")
                    for i, (count, vals) in enumerate(blocks, 1):
                        print(f"Блок {i}: {count} измерений")
                        print(f"  Значения: {vals}")
                else:
                    print("Данные не загружены.")

            case "2":
                process_data(blocks, t_student, instr_error)

            case "3":
                t_student = set_t_coef()
                print(f"Коэффициент Стьюдента установлен: {t_student:.3f}")

            case "4":
                instr_error = set_instr_error()
                print(f"Приборная погрешность установлена: {instr_error:.4f}")

            case "5":
                new_t = compute_student_t()
                if new_t is not None:
                    t_student = new_t
                    print(f"Коэффициент Стьюдента установлен автоматически: {t_student:.6f}")

            case "6":
                detailed_sigma_report(blocks)

            case "7":
                print("Выход из программы.")
                break

            case _:
                print("Неверный пункт меню. Попробуйте снова.")


if __name__ == "__main__":
    main()