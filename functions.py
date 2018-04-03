while True:
    length = int(input("Введите длину строки"))
    if length<=100:
        break
    else:
        print("Длина строки должна быть меньше 101 символа")

paint = []
for i in range(length):
    paint.append(str(input("Введите символ")))

def get_answer(paint):
    for i in range(1,len(paint)-1):
        if ((paint[i] == paint[i+1]) or (paint[i-1] == paint[i])) and (paint[i] !='?'):
            return 'No'
        if (paint[i] == '?') and ((paint[i-1] == paint[i]) or (paint[i+1] == paint[i])):
            return 'Yes'
        if  (paint[i] == '?') and (paint[i + 1] != paint[i]):
            if paint[i+1]  == paint[i-1]:
                return 'Yes'
        if paint[0] == '?' or paint[len(paint)] == '?':
            return 'Yes'
        return 'No'

print(get_answer(paint))