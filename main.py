def file_open(input_file='main_tasks/task2/input.txt', output_file='main_tasks/task2/output.txt'):
    with open(input_file, 'r') as f:
        count = int(f.readline())  
        lines = f.readlines().strip().split()
        data = list(map(int, lines))  # Четвертая строка - это список заправок
        
    # Вызываем функцию решения задачи
    result = (d, m, n, stops)

    # Записываем результат в выходной файл
    with open(output_file, 'w') as f:
        f.write(str(result))

    return result


print(file_open())