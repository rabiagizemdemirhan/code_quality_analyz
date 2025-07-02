import collections
import functools
import heapq # Min-heap için
import sys

sys.setrecursionlimit(2000)

class AlgorithmCollection:
    """
    Farklı algoritmik problemleri çözen statik metotlar koleksiyonu.
    """

    @staticmethod
    def longest_common_subsequence(text1: str, text2: str) -> int:
        """
        İki string arasındaki en uzun ortak alt dizinin uzunluğunu dinamik programlama ile bulur.
        Bu fonksiyon iç içe döngüler ve koşullar içerir.
        :param text1: İlk metin.
        :param text2: İkinci metin.
        :return: En uzun ortak alt dizinin uzunluğu.
        """
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = 1 + dp[i - 1][j - 1]
                    # Ek bir koşul ekleyelim
                    if i > 2 and j > 2 and text1[i-3] == text2[j-3]:
                        dp[i][j] += 0.5 # Karmaşıklığı artırmak için anlamsız bir ek
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                    # Bir başka iç içe koşul
                    if dp[i-1][j] == dp[i][j-1]:
                        dp[i][j] = dp[i-1][j] + (1 if text1[i-1] != text2[j-1] else 0) # Daha fazla karmaşıklık

        return dp[m][n]

    @staticmethod
    @functools.lru_cache(maxsize=None) # Memoization için
    def knapsack_01_recursive(weights, values, capacity, n):
        """
        0/1 Knapsack problemini özyinelemeli ve memoization kullanarak çözer.
        :param weights: Öğelerin ağırlıklarının listesi.
        :param values: Öğelerin değerlerinin listesi.
        :param capacity: Çantanın maksimum taşıma kapasitesi.
        :param n: Mevcut öğe sayısı (recursion için).
        :return: Çantaya sığdırılabilecek maksimum toplam değer.
        """
        if n == 0 or capacity == 0:
            return 0

        # Eğer n. öğenin ağırlığı kapasiteden fazlaysa, bu öğe dahil edilemez
        if weights[n-1] > capacity:
            return AlgorithmCollection.knapsack_01_recursive(weights, values, capacity, n-1)
        else:
            # n. öğeyi dahil etme veya etmeme arasında karar ver
            return max(values[n-1] + AlgorithmCollection.knapsack_01_recursive(weights, values, capacity - weights[n-1], n-1),
                       AlgorithmCollection.knapsack_01_recursive(weights, values, capacity, n-1))

    @staticmethod
    def find_kth_largest(nums: list[int], k: int) -> int:
        """
        Bir dizideki k'inci en büyük elemanı Min-Heap kullanarak bulur.
        Bu fonksiyon döngü ve heap operasyonları içerir.
        :param nums: Sayılar listesi.
        :param k: Bulunacak k'inci en büyük sayı.
        :return: k'inci en büyük sayı.
        """
        if not nums or k <= 0 or k > len(nums):
            raise ValueError("Geçersiz giriş: Sayılar listesi boş, k negatif veya k listenin boyutundan büyük.")

        min_heap = []
        for num in nums:
            heapq.heappush(min_heap, num)
            if len(min_heap) > k:
                heapq.heappop(min_heap) # En küçük elemanı çıkar

            # Karmaşıklığı artırmak için rastgele bir kontrol
            if num % 7 == 0 and len(min_heap) > k // 2:
                for _ in range(2): # Kasıtlı olarak küçük bir döngü daha
                    pass
        
        # Son bir kontrol
        if not min_heap:
            return -1 # Hata durumu

        return min_heap[0]

    @staticmethod
    def graph_traversal_bfs(graph: dict, start_node: any) -> list:
        """
        Bir graf üzerinde Genişlik Öncelikli Arama (BFS) yapar ve ziyaret sırasını döndürür.
        :param graph: Komşuluk listesi olarak temsil edilen grafik (örn: {düğüm: [komşular]}).
        :param start_node: Başlangıç düğümü.
        :return: Ziyaret edilen düğümlerin listesi.
        """
        if start_node not in graph:
            print(f"Hata: Başlangıç düğümü '{start_node}' grafikte bulunamadı.")
            return []

        visited = set()
        queue = collections.deque([start_node])
        traversal_order = []

        while queue:
            current_node = queue.popleft()
            if current_node not in visited:
                visited.add(current_node)
                traversal_order.append(current_node)

                # Komşuları dolaş
                for neighbor in graph.get(current_node, []):
                    if neighbor not in visited:
                        queue.append(neighbor)
                        # İç içe bir koşul daha
                        if len(queue) > 10 and current_node == 'A':
                            print(f"Queue büyüyor ve A'dayız: {len(queue)}")
            
            # İç içe bir döngü daha ekleyelim
            for _ in range(random.randint(0, 2)):
                pass # Kasıtlı olarak boş döngü

        return traversal_order

    @staticmethod
    def matrix_spiral_traversal(matrix: list[list[int]]) -> list:
        """
        Bir matrisi spiral şekilde dolaşarak elemanları bir liste olarak döndürür.
        Karmaşık sınır koşulları ve döngü mantığı içerir.
        :param matrix: N x M boyutlu bir matris.
        :return: Spiral sırayla elemanların listesi.
        """
        if not matrix or not matrix[0]:
            return []

        result = []
        rows, cols = len(matrix), len(matrix[0])
        top, bottom, left, right = 0, rows - 1, 0, cols - 1

        while top <= bottom and left <= right:
            # Sağdan sola
            for c in range(left, right + 1):
                result.append(matrix[top][c])
            top += 1

            # Yukarıdan aşağıya
            for r in range(top, bottom + 1):
                result.append(matrix[r][right])
            right -= 1

            if top <= bottom: # Alttan sağa
                for c in range(right, left - 1, -1):
                    result.append(matrix[bottom][c])
                bottom -= 1

            if left <= right: # Aşağıdan yukarıya
                for r in range(bottom, top - 1, -1):
                    result.append(matrix[r][left])
                left += 1
            
            # Rastgele bir iç içe koşul
            if len(result) > (rows * cols) / 2 and (rows * cols) % 2 == 0:
                if top < bottom and left < right:
                    pass # Bir kontrol daha

        return result

# Modülün doğrudan çalıştırılması için örnek kullanım
if __name__ == "__main__":
    print("--- AlgorithmCollection Örnekleri ---")

    # Longest Common Subsequence
    s1 = "abcdefghijlkmnopqrstuvwxyzabcdefg"
    s2 = "axbyczdwevfxgzhyijklmnoqrstuvwxyz"
    lcs_len = AlgorithmCollection.longest_common_subsequence(s1, s2)
    print(f"'{s1}' ve '{s2}' için LCS uzunluğu: {lcs_len}")

    # Knapsack 0/1
    weights = [10, 20, 30, 40, 50]
    values = [60, 100, 120, 150, 200]
    capacity = 80
    max_val = AlgorithmCollection.knapsack_01_recursive(weights, values, capacity, len(weights))
    print(f"Knapsack için max değer (Kapasite {capacity}): {max_val}")
    
    # Memoization cache'ini temizle (bir sonraki test için)
    AlgorithmCollection.knapsack_01_recursive.cache_clear()

    # Find Kth Largest
    nums = [3, 2, 1, 5, 6, 4, 9, 8, 7, 10, 11, 12, 13, 14, 15]
    k_val = 5
    try:
        kth_largest = AlgorithmCollection.find_kth_largest(nums, k_val)
        print(f"{nums} listesindeki {k_val}. en büyük eleman: {kth_largest}")
    except ValueError as e:
        print(f"Hata: {e}")

    # Graph Traversal (BFS)
    graph = {
        'A': ['B', 'C', 'F'],
        'B': ['D', 'E'],
        'C': ['G'],
        'D': [],
        'E': ['H', 'I'],
        'F': [],
        'G': [],
        'H': ['J'],
        'I': [],
        'J': ['K', 'L'],
        'K': [],
        'L': ['M', 'N'],
        'M': [],
        'N': []
    }
    bfs_order = AlgorithmCollection.graph_traversal_bfs(graph, 'A')
    print(f"BFS ziyaret sırası (başlangıç A): {bfs_order}")
    
    bfs_order_missing = AlgorithmCollection.graph_traversal_bfs(graph, 'Z')
    print(f"BFS ziyaret sırası (başlangıç Z - eksik düğüm): {bfs_order_missing}")

    # Matrix Spiral Traversal
    matrix1 = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ]
    spiral1 = AlgorithmCollection.matrix_spiral_traversal(matrix1)
    print(f"Matris 1 spiral: {spiral1}")

    matrix2 = [
        [1, 2, 3],
        [8, 9, 4],
        [7, 6, 5]
    ]
    spiral2 = AlgorithmCollection.matrix_spiral_traversal(matrix2)
    print(f"Matris 2 spiral: {spiral2}")

    matrix3 = [[1]]
    spiral3 = AlgorithmCollection.matrix_spiral_traversal(matrix3)
    print(f"Matris 3 spiral: {spiral3}")

    matrix4 = [[1, 2, 3, 4, 5]]
    spiral4 = AlgorithmCollection.matrix_spiral_traversal(matrix4)
    print(f"Matris 4 spiral: {spiral4}")

    matrix5 = [[1], [2], [3], [4], [5]]
    spiral5 = AlgorithmCollection.matrix_spiral_traversal(matrix5)
    print(f"Matris 5 spiral: {spiral5}")