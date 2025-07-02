# target_code/sample_code.py

def greet(name):
    if name:
        print(f"Merhaba, {name}!")
    else:
        print("Merhaba!")

def calculate_sum(a, b):
    total = a + b
    return total

class MyClass:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def process_data(self, data_list):
        count = 0
        for item in data_list:
            if item > 0:
                count += 1
        return count

# Fonksiyonlar dışında kalan kod (Radon tarafından analiz edilmez)
if __name__ == "__main__":
    greet("Geliştirici")
    sum_result = calculate_sum(5, 3)
    print(f"Toplam: {sum_result}")
    my_obj = MyClass(10)
    print(my_obj.get_value())
    processed = my_obj.process_data([1, -2, 3, 0, 5])
    print(f"İşlenen veri adedi: {processed}")