"""
Bu modül, CSV dosyalarından veri okuma, işleme ve sonuçları analiz etme üzerine odaklanır.
Özellikle büyük veri kümeleri üzerinde performans ve karmaşıklık değerlendirmesi için tasarlanmıştır.
"""

import csv
import math
import os
import random
from datetime import datetime

class ComplexDataProcessor:
    """
    CSV verilerini işleyen, filtreleyen, dönüştüren ve özetleyen bir sınıf.
    Çok sayıda fonksiyonu ve iç içe mantığı içerir.
    """

    DEFAULT_THRESHOLD = 500
    LOG_FILE_PATH = "processor_logs.txt"

    def __init__(self, data_source_path):
        """
        Veri işlemcisini başlatır.
        :param data_source_path: İşlenecek CSV dosyasının yolu.
        """
        self.data_source = data_source_path
        self.processed_data = []
        self.analysis_results = {}
        self._initialize_logger()
        self._log(f"DataProcessor initialized with source: {data_source_path}")

    def _initialize_logger(self):
        """Dahili loglama dosyasını ayarlar."""
        try:
            with open(self.LOG_FILE_PATH, 'a') as f:
                f.write(f"--- Log Session Started: {datetime.now()} ---\n")
        except IOError as e:
            print(f"Hata: Log dosyası oluşturulamadı: {e}")

    def _log(self, message):
        """Mesajları log dosyasına yazar."""
        try:
            with open(self.LOG_FILE_PATH, 'a') as f:
                f.write(f"{datetime.now()}: {message}\n")
        except IOError as e:
            print(f"Hata: Log dosyasına yazılamadı: {e}")

    def load_data(self, skip_header=True):
        """
        CSV dosyasından verileri yükler.
        Her satırı bir liste olarak okur.
        :param skip_header: İlk satırı atlayıp atlamayacağını belirtir (başlık satırı).
        :return: Yüklenen verilerin bir listesi. Başarısız olursa boş liste.
        """
        data = []
        if not os.path.exists(self.data_source):
            self._log(f"Hata: Veri kaynağı bulunamadı: {self.data_source}")
            return []

        try:
            with open(self.data_source, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                if skip_header:
                    next(reader, None)  # Başlığı atla
                for row_num, row in enumerate(reader):
                    # Her satırın en az 3 sütunu olduğunu varsayalım (ID, Value, Category)
                    if len(row) >= 3:
                        try:
                            # İlk sütunu integer, ikinciyi float, üçüncüyü string yapmaya çalışalım
                            processed_row = [int(row[0]), float(row[1]), str(row[2])]
                            data.append(processed_row)
                        except ValueError as ve:
                            self._log(f"Satır {row_num+1} işlenirken tip dönüştürme hatası: {row} - {ve}")
                            continue # Hatalı satırı atla
                    else:
                        self._log(f"Satır {row_num+1} beklenenden az sütuna sahip: {row}")
            self._log(f"Veri yükleme tamamlandı. {len(data)} satır yüklendi.")
            self.processed_data = data
            return data
        except Exception as e:
            self._log(f"Veri yüklenirken genel hata oluştu: {e}")
            return []

    def filter_data_by_value(self, min_value=0.0, max_value=float('inf')):
        """
        Veriyi belirli bir değer aralığına göre filtreler (ikinci sütunu kullanır).
        :param min_value: Minimum değer (dahil).
        :param max_value: Maksimum değer (dahil).
        :return: Filtrelenmiş veri listesi.
        """
        if not self.processed_data:
            self._log("Filtreleme için işlenmiş veri yok.")
            return []

        filtered = []
        for item in self.processed_data:
            if min_value <= item[1] <= max_value:
                filtered.append(item)
            elif item[1] < min_value and item[1] % 2 == 0: # Ek karmaşıklık
                self._log(f"Değer minimum altında ama çift: {item[1]}")
        self._log(f"Veri {min_value}-{max_value} aralığında filtrelendi. {len(filtered)} satır kaldı.")
        return filtered

    def calculate_summary_statistics(self, data_subset=None):
        """
        Veri alt kümesi üzerinde özet istatistikleri (ortalama, medyan, standart sapma) hesaplar.
        Veri alt kümesi belirtilmezse, tüm işlenmiş veriyi kullanır.
        :param data_subset: İstatistiklerin hesaplanacağı veri listesi.
        :return: İstatistikleri içeren bir sözlük.
        """
        data_to_analyze = data_subset if data_subset is not None else self.processed_data

        if not data_to_analyze:
            self._log("İstatistik hesaplamak için veri yok.")
            return {"count": 0, "mean": 0.0, "median": 0.0, "std_dev": 0.0, "min": 0.0, "max": 0.0}

        values = [item[1] for item in data_to_analyze] # İkinci sütun değerleri

        count = len(values)
        total_sum = sum(values)
        mean = total_sum / count

        sorted_values = sorted(values)
        mid = count // 2
        median = (sorted_values[mid - 1] + sorted_values[mid]) / 2 if count % 2 == 0 else sorted_values[mid]

        sum_sq_diff = sum([(x - mean) ** 2 for x in values])
        std_dev = math.sqrt(sum_sq_diff / count) if count > 0 else 0.0

        min_val = min(values)
        max_val = max(values)

        stats = {
            "count": count,
            "mean": mean,
            "median": median,
            "std_dev": std_dev,
            "min": min_val,
            "max": max_val
        }
        self.analysis_results.update(stats)
        self._log(f"Özet istatistikleri hesaplandı: {stats}")
        return stats

    def categorize_data(self, threshold=DEFAULT_THRESHOLD):
        """
        Veriyi belirli bir eşiğe göre kategorize eder ve her kategori için sayım yapar.
        :param threshold: Kategorizasyon için kullanılacak eşik değeri.
        :return: Kategori sayımlarını içeren bir sözlük.
        """
        if not self.processed_data:
            self._log("Kategorizasyon için işlenmiş veri yok.")
            return {}

        categories = {}
        for item in self.processed_data:
            category_name = item[2] # Üçüncü sütun kategori adı
            if item[1] > threshold:
                category_name += "_HighValue"
            elif item[1] <= threshold / 2: # Farklı bir koşul ekleyelim
                category_name += "_LowValue"
            else:
                category_name += "_MediumValue"

            categories[category_name] = categories.get(category_name, 0) + 1
            
            # İç içe if/else blokları ile karmaşıklığı artıralım
            if category_name.startswith("A"):
                if item[0] % 5 == 0:
                    categories[category_name + "_DivisibleBy5"] = categories.get(category_name + "_DivisibleBy5", 0) + 1
                elif item[0] % 3 == 0:
                    categories[category_name + "_DivisibleBy3"] = categories.get(category_name + "_DivisibleBy3", 0) + 1
            
        self._log(f"Veri kategorize edildi. Sonuçlar: {categories}")
        return categories

    def _internal_recursive_helper(self, n, memo={}):
        """
        Yardımcı özyinelemeli fonksiyon (örnek karmaşıklık artışı için).
        Fibonacci benzeri bir hesaplama yapar.
        """
        if n in memo:
            return memo[n]
        if n <= 1:
            return n
        result = self._internal_recursive_helper(n-1, memo) + self._internal_recursive_helper(n-2, memo)
        memo[n] = result
        return result

    def perform_complex_operation(self, iterations=10, complexity_factor=5):
        """
        Sınıf içinde karmaşık, hesaplama yoğun bir işlem gerçekleştirir.
        Birden fazla döngü ve koşul içerir.
        :param iterations: Ana döngü iterasyon sayısı.
        :param complexity_factor: İç döngü karmaşıklığını artıran faktör.
        """
        self._log(f"Karmaşık işlem başlatıldı: iterasyon={iterations}, faktör={complexity_factor}")
        intermediate_results = []
        for i in range(iterations):
            current_sum = 0
            for j in range(i * complexity_factor):
                if j % 3 == 0 and j % 5 == 0:
                    current_sum += self._internal_recursive_helper(min(j // 10, 15)) # Özyinelemeli çağrı
                elif j % 3 == 0:
                    current_sum += math.sqrt(j)
                elif j % 5 == 0:
                    current_sum -= (j / 2.0)
                else:
                    current_sum += j * 0.1
                
                if current_sum > 1000: # Nested if
                    if random.random() < 0.1:
                        self._log(f"Yüksek değer ulaşıldı: {current_sum} at ({i}, {j})")
                    current_sum /= 2 # Değeri düşür

            intermediate_results.append(current_sum)
            # Bir başka iç içe döngü
            for k in range(min(i, 3)):
                if k % 2 == 0:
                    intermediate_results[i] += k
                else:
                    intermediate_results[i] -= k / 2
        
        final_result = sum(intermediate_results) / len(intermediate_results) if intermediate_results else 0
        self._log(f"Karmaşık işlem tamamlandı. Nihai ortalama: {final_result}")
        return final_result

    def save_analysis_results(self, output_file="analysis_summary.txt"):
        """
        Analiz sonuçlarını bir metin dosyasına kaydeder.
        :param output_file: Sonuçların yazılacağı dosyanın adı.
        """
        self._log(f"Analiz sonuçları '{output_file}' dosyasına kaydediliyor.")
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"--- Data Analysis Summary ({datetime.now()}) ---\n")
                for key, value in self.analysis_results.items():
                    f.write(f"{key}: {value}\n")
                
                f.write("\n--- Processed Data Sample (First 5 rows) ---\n")
                for i, row in enumerate(self.processed_data[:5]):
                    f.write(f"Row {i+1}: {row}\n")
                
            self._log("Analiz sonuçları başarıyla kaydedildi.")
        except Exception as e:
            self._log(f"Analiz sonuçları kaydedilirken hata oluştu: {e}")

# Modülün doğrudan çalıştırılması için örnek kullanım
if __name__ == "__main__":
    # Örnek bir CSV dosyası oluşturalım
    sample_csv_path = "sample_data.csv"
    with open(sample_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Value", "Category"])
        for i in range(1, 101):
            writer.writerow([i, round(random.uniform(100, 1000), 2), random.choice(["A", "B", "C", "D"])])
        writer.writerow([101, "bozuk", "X"]) # Hatalı satır
        writer.writerow([102, 550.2, "B"])
        writer.writerow([103, 1200.5, "A"])

    print(f"'{sample_csv_path}' oluşturuldu.")

    processor = ComplexDataProcessor(sample_csv_path)
    
    # Veriyi yükle
    loaded_data = processor.load_data()
    print(f"Yüklenen veri adedi: {len(loaded_data)}")

    # Veriyi filtrele ve istatistik hesapla
    filtered_high_value_data = processor.filter_data_by_value(min_value=700)
    print(f"700 üzeri değer içeren veri adedi: {len(filtered_high_value_data)}")
    
    stats_all = processor.calculate_summary_statistics()
    print(f"Tüm veri istatistikleri: {stats_all}")

    stats_filtered = processor.calculate_summary_statistics(filtered_high_value_data)
    print(f"Filtrelenmiş veri istatistikleri: {stats_filtered}")

    # Veriyi kategorize et
    categories = processor.categorize_data(threshold=600)
    print(f"Kategori dağılımı: {categories}")

    # Karmaşık işlemi çalıştır
    complex_op_result = processor.perform_complex_operation(iterations=20, complexity_factor=7)
    print(f"Karmaşık operasyon sonucu: {complex_op_result}")

    # Analiz sonuçlarını kaydet
    processor.save_analysis_results("final_analysis_summary.txt")
    print("Analiz özeti kaydedildi.")

    # Geçici dosyaları temizle
    # if os.path.exists(sample_csv_path):
    #     os.remove(sample_csv_path)
    # if os.path.exists("final_analysis_summary.txt"):
    #     os.remove("final_analysis_summary.txt")
    # if os.path.exists(processor.LOG_FILE_PATH):
    #     os.remove(processor.LOG_FILE_PATH)