"""
Basit bir İleri Beslemeli Yapay Sinir Ağı (Feedforward Neural Network) simülatörü.
Katmanlar, aktivasyon fonksiyonları ve basit ileri yayılım (forward pass) mekanizmalarını içerir.
Özellikle matris işlemleri ve iç içe döngülerle karmaşıklık yaratır.
"""

import numpy as np
import random
import os

class NeuralNetworkSimulator:
    """
    Öğrenilebilir ağırlıklara ve aktivasyon fonksiyonlarına sahip basit bir sinir ağı.
    """

    def __init__(self, layer_dims: list[int], activation_type: str = 'sigmoid'):
        """
        Sinir ağını başlatır.
        :param layer_dims: Her katmandaki nöron sayısını belirten liste (örn: [input_dim, hidden1_dim, output_dim]).
        :param activation_type: Kullanılacak aktivasyon fonksiyonunun tipi ('sigmoid' veya 'relu').
        """
        if len(layer_dims) < 2:
            raise ValueError("En az bir giriş ve bir çıkış katmanı olmalıdır.")

        self.num_layers = len(layer_dims)
        self.layer_dims = layer_dims
        self.weights = [] # Ağırlık matrisleri
        self.biases = []  # Bias vektörleri
        self.activation_type = activation_type.lower()

        self._initialize_parameters()
        self._set_activation_function()
        self._log_initialization()

    def _initialize_parameters(self):
        """Ağdaki ağırlık ve bias parametrelerini rastgele başlatır."""
        for l in range(1, self.num_layers):
            # Ağırlıklar: (önceki katmandaki nöron sayısı, mevcut katmandaki nöron sayısı)
            # Rastgele küçük değerlerle başlatılır
            W = np.random.randn(self.layer_dims[l-1], self.layer_dims[l]) * 0.01
            b = np.zeros((1, self.layer_dims[l])) # Biaslar: (1, mevcut katmandaki nöron sayısı)

            self.weights.append(W)
            self.biases.append(b)
        self._log_message("Ağ parametreleri başlatıldı.")

    def _sigmoid(self, Z):
        """Sigmoid aktivasyon fonksiyonu."""
        return 1 / (1 + np.exp(-Z))

    def _relu(self, Z):
        """ReLU aktivasyon fonksiyonu."""
        return np.maximum(0, Z)

    def _set_activation_function(self):
        """Seçilen aktivasyon fonksiyonunu ayarlar."""
        if self.activation_type == 'sigmoid':
            self.activation_func = self._sigmoid
        elif self.activation_type == 'relu':
            self.activation_func = self._relu
        else:
            raise ValueError(f"Desteklenmeyen aktivasyon tipi: {self.activation_type}")
        self._log_message(f"Aktivasyon fonksiyonu: {self.activation_type}")

    def _log_message(self, message: str):
        """Basit bir dahili loglama fonksiyonu."""
        # Gerçek bir uygulamada daha gelişmiş bir loglama sistemi olurdu.
        # Burada sadece karmaşıklığı artırmak için basit bir dosya yazma.
        log_dir = "nn_logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "nn_activity.log")
        try:
            with open(log_file, "a") as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        except IOError as e:
            print(f"Uyarı: Log dosyasına yazılamadı: {e}")

    def _log_initialization(self):
        """Başlatma bilgilerini loglar."""
        self._log_message("--- Neural Network Initialization ---")
        self._log_message(f"Katman boyutları: {self.layer_dims}")
        self._log_message(f"Toplam katman sayısı: {self.num_layers}")
        self._log_message(f"Kullanılan aktivasyon: {self.activation_type}")
        for i, (W, b) in enumerate(zip(self.weights, self.biases)):
            self._log_message(f"  Katman {i+1}: Ağırlık boyutu {W.shape}, Bias boyutu {b.shape}")
        self._log_message("------------------------------------")

    def forward_pass(self, X: np.ndarray) -> np.ndarray:
        """
        Giriş verisi üzerinde ileri yayılım (forward pass) gerçekleştirir.
        Her katman için matris çarpımı ve aktivasyon fonksiyonu uygular.
        :param X: Giriş verisi matrisi (örnek_sayısı, giriş_boyutu).
        :return: Çıkış katmanının aktivasyonları.
        """
        if X.shape[1] != self.layer_dims[0]:
            raise ValueError(f"Giriş boyutu ({X.shape[1]}) ağın giriş boyutuyla ({self.layer_dims[0]}) eşleşmiyor.")

        A = X # Mevcut aktivasyonlar, başlangıçta giriş katmanı
        self._log_message(f"İleri yayılım başlatıldı. Giriş boyutu: {X.shape}")

        for l in range(self.num_layers - 1): # Son katmana kadar iterasyon yap
            W = self.weights[l]
            b = self.biases[l]

            # Matris çarpımı (Z = A * W + b)
            # Bu kısım karmaşıklığı artıran ana döngüdür.
            Z = np.dot(A, W) + b
            
            # İç içe bir koşul ekleyelim
            if Z.mean() > 100:
                self._log_message(f"Katman {l+1} Z ortalaması yüksek: {Z.mean()}")
                if self.activation_type == 'sigmoid' and Z.min() < -10: # Daha da iç içe
                    Z = np.clip(Z, -10, 10) # Sayısal kararlılık için kırpma

            # Aktivasyon fonksiyonunu uygula
            A = self.activation_func(Z)
            self._log_message(f"Katman {l+1} çıkış boyutu: {A.shape}, Ortalama Aktivasyon: {A.mean():.4f}")
            
            # Rastgele bir kontrol veya küçük döngü
            if random.random() < 0.05: # %5 ihtimalle
                for _ in range(random.randint(1, 3)): # Küçük bir iç döngü
                    pass # Kasıtlı olarak boş döngü, karmaşıklığı artırmak için

        self._log_message("İleri yayılım tamamlandı.")
        return A

    def train_network_placeholder(self, X_train, y_train, epochs: int, learning_rate: float):
        """
        Ağın eğitim sürecini simüle eden bir yer tutucu fonksiyon.
        Gerçek bir eğitim döngüsü içermez, sadece yapısal karmaşıklık ekler.
        :param X_train: Eğitim giriş verisi.
        :param y_train: Eğitim hedef çıkış verisi.
        :param epochs: Eğitim dönem sayısı.
        :param learning_rate: Öğrenme oranı.
        """
        self._log_message(f"Eğitim başlatıldı. Dönem: {epochs}, Öğrenme oranı: {learning_rate}")
        
        for epoch in range(epochs):
            # Basit bir ileri geçiş simülasyonu
            output = self.forward_pass(X_train)
            
            # Loss hesaplama (yer tutucu)
            loss = np.mean((output - y_train) ** 2)
            
            # Geri yayılım (yer tutucu - detaylı implementasyon yok)
            # Burada normalde W ve b güncellenir.
            
            if (epoch + 1) % 10 == 0:
                self._log_message(f"Dönem {epoch+1}/{epochs}, Kayıp: {loss:.6f}")
                # Karmaşıklık eklemek için iç içe döngü
                if loss < 0.1:
                    for _ in range(random.randint(1, 5)):
                        pass
        
        self._log_message("Eğitim simülasyonu tamamlandı.")
        return loss

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Test verisi üzerinde tahmin yapar.
        :param X_test: Test giriş verisi.
        :return: Tahmin edilen çıkışlar.
        """
        self._log_message(f"Tahmin işlemi başlatıldı. Test boyutu: {X_test.shape}")
        predictions = self.forward_pass(X_test)
        # Sınıflandırma için eşikleme yapalım (örnek)
        if self.layer_dims[-1] == 1 and self.activation_type == 'sigmoid':
            predictions = (predictions >= 0.5).astype(int)
        
        self._log_message("Tahmin tamamlandı.")
        return predictions

    def save_model_params(self, filename: str = "nn_model_params.npy"):
        """
        Ağın ağırlıklarını ve biaslarını dosyaya kaydeder.
        :param filename: Kaydedilecek dosyanın adı.
        """
        self._log_message(f"Model parametreleri '{filename}' dosyasına kaydediliyor.")
        params = {
            "weights": self.weights,
            "biases": self.biases,
            "layer_dims": self.layer_dims,
            "activation_type": self.activation_type
        }
        try:
            np.save(filename, params)
            self._log_message("Model parametreleri başarıyla kaydedildi.")
        except Exception as e:
            self._log_message(f"Model parametreleri kaydedilirken hata: {e}")

    @staticmethod
    def load_model_params(filename: str = "nn_model_params.npy"):
        """
        Ağın ağırlıklarını ve biaslarını dosyadan yükler ve yeni bir NN örneği döndürür.
        :param filename: Yüklenecek dosyanın adı.
        :return: Yüklenen parametrelerle başlatılmış NeuralNetworkSimulator nesnesi.
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Model parametre dosyası bulunamadı: {filename}")
        
        try:
            params = np.load(filename, allow_pickle=True).item()
            # Yeni bir NN objesi oluşturup parametreleri manuel set edelim (basitlik için)
            nn = NeuralNetworkSimulator(params["layer_dims"], params["activation_type"])
            nn.weights = params["weights"]
            nn.biases = params["biases"]
            nn._log_message(f"Model parametreleri '{filename}' dosyasından yüklendi.")
            return nn
        except Exception as e:
            raise RuntimeError(f"Model parametreleri yüklenirken hata: {e}")

# Modülün doğrudan çalıştırılması için örnek kullanım
if __name__ == "__main__":
    from datetime import datetime # datetime zaten import edildiği için gerek yok

    print("--- Neural Network Simulator Örnekleri ---")

    # Basit bir ağ oluşturalım
    input_dim = 10
    hidden_dim1 = 20
    hidden_dim2 = 15
    output_dim = 1

    nn = NeuralNetworkSimulator(layer_dims=[input_dim, hidden_dim1, hidden_dim2, output_dim], activation_type='relu')

    # Örnek giriş verisi oluşturalım
    num_samples = 100
    X_sample = np.random.randn(num_samples, input_dim) # 100 örnek, 10 özellik
    y_sample = np.random.randint(0, 2, size=(num_samples, output_dim)) # Binary sınıflandırma hedefi

    print("\n--- İleri Yayılım Testi ---")
    output = nn.forward_pass(X_sample)
    print(f"Çıkış katmanı aktivasyonlarının boyutu: {output.shape}")
    print(f"Çıkış katmanı aktivasyonlarının ortalaması: {output.mean():.4f}")

    print("\n--- Eğitim Simülasyonu Testi ---")
    simulated_loss = nn.train_network_placeholder(X_sample, y_sample, epochs=50, learning_rate=0.01)
    print(f"Simüle edilmiş eğitim sonrası son kayıp: {simulated_loss:.6f}")

    print("\n--- Tahmin Testi ---")
    X_test_sample = np.random.randn(5, input_dim) # 5 test örneği
    predictions = nn.predict(X_test_sample)
    print(f"Tahmin edilen çıkışlar:\n{predictions}")

    print("\n--- Model Kaydetme/Yükleme Testi ---")
    model_file = "my_first_nn_model.npy"
    nn.save_model_params(model_file)
    try:
        loaded_nn = NeuralNetworkSimulator.load_model_params(model_file)
        print(f"Model '{model_file}' başarıyla yüklendi. Yüklenen ağ katmanları: {loaded_nn.layer_dims}")
        # Yüklenen modelle tekrar tahmin yap
        loaded_predictions = loaded_nn.predict(X_test_sample)
        print(f"Yüklenen modelden tahminler:\n{loaded_predictions}")
    except Exception as e:
        print(f"Model yüklenirken bir hata oluştu: {e}")
    finally:
        if os.path.exists(model_file):
            os.remove(model_file) # Geçici model dosyasını temizle
        log_dir = "nn_logs"
        if os.path.exists(log_dir) and os.listdir(log_dir):
            for f in os.listdir(log_dir):
                os.remove(os.path.join(log_dir, f))
            os.rmdir(log_dir) # Klasörü boşsa sil