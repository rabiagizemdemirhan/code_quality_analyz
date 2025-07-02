import heapq
import random
from collections import deque
from datetime import datetime, timedelta

class SimulationEvent:
    """
    Simülasyonda meydana gelen bir olayı temsil eder.
    """
    def __init__(self, time: float, event_type: str, data: dict = None):
        self.time = time
        self.event_type = event_type
        self.data = data if data is not None else {}
        self.creation_time = datetime.now()

    def __lt__(self, other):
        """Olayları zamana göre sıralamak için karşılaştırma operatörü."""
        if self.time != other.time:
            return self.time < other.time
        # Aynı zamanda ise, olay tipine göre alfabetik sıralama (rastgele bir tie-breaker)
        return self.event_type < other.event_type

    def __repr__(self):
        return f"Event(Time: {self.time:.2f}, Type: {self.event_type}, Data: {self.data})"

class EventDrivenSimulator:
    """
    Olay tabanlı bir simülasyonu yöneten ana sınıf.
    """
    def __init__(self, start_time: float = 0.0, end_time: float = 100.0):
        self.current_time = start_time
        self.end_time = end_time
        self.event_queue = []  # Öncelik kuyruğu olarak kullanılacak min-heap
        self.metrics = {
            "events_processed": 0,
            "total_wait_time": 0.0,
            "resource_utilization": 0.0,
            "errors_occurred": 0
        }
        self.resource_status = {"CPU": "idle", "Memory": "available"}
        self.active_tasks = deque() # Kuyruk benzeri yapı
        self._log_history = []
        print(f"Simülatör başlatıldı. Zaman aralığı: [{start_time}, {end_time}]")

    def _log_event(self, message: str, level: str = "INFO"):
        """Dahili loglama mekanizması."""
        self._log_history.append(f"{self.current_time:.2f} [{level}] {message}")
        # print(f"{self.current_time:.2f} [{level}] {message}") # Geliştirme sırasında görmek için

    def schedule_event(self, event: SimulationEvent):
        """
        Bir olayı simülasyon kuyruğuna ekler.
        :param event: Eklenecek SimulationEvent nesnesi.
        """
        if event.time < self.current_time:
            self._log_event(f"Uyarı: Geçmişe ait bir olay zamanlandı: {event}", "WARN")
            # Yine de ekleyelim ama bir uyarı verelim
        heapq.heappush(self.event_queue, event)
        self._log_event(f"Olay zamanlandı: {event.event_type} @ {event.time:.2f}")

    def process_event(self, event: SimulationEvent):
        """
        Bir olayı işleyen ana metod. Bu metod içinde karmaşık mantıklar yer alır.
        :param event: İşlenecek SimulationEvent nesnesi.
        """
        self.current_time = event.time
        self.metrics["events_processed"] += 1
        self._log_event(f"Olay işleniyor: {event.event_type}")

        # Olay tipine göre farklı davranışlar
        if event.event_type == "TaskArrival":
            task_id = event.data.get("task_id")
            processing_time = event.data.get("processing_time", 1.0)
            priority = event.data.get("priority", 0)

            self._log_event(f"Görev {task_id} geldi. İşlem süresi: {processing_time:.2f}, Öncelik: {priority}")
            
            # Kaynak durumu kontrolü ve görev ataması (karmaşık karar verme)
            if self.resource_status["CPU"] == "idle":
                self.resource_status["CPU"] = "busy"
                self._log_event(f"CPU müsait, görev {task_id} hemen işleniyor.")
                
                finish_time = self.current_time + processing_time
                self.schedule_event(SimulationEvent(finish_time, "TaskCompletion", {"task_id": task_id, "start_time": self.current_time}))
                
                if priority > 5 and random.random() < 0.2: 
                    self._log_event(f"Yüksek öncelikli görev {task_id} için ek kayıt.", "DEBUG")
                    self.metrics["resource_utilization"] += processing_time * 0.1 

            elif self.resource_status["CPU"] == "busy" and priority > 0:
                if random.random() < 0.15: 
                    self._log_event(f"CPU meşgul ama görev {task_id} yüksek öncelikli, preempt ediliyor.", "WARN")
                    self.active_tasks.appendleft({"task_id": task_id, "arrival": self.current_time, "priority": priority, "processing_time": processing_time})
                    self.metrics["errors_occurred"] += 1
                else:
                    self._log_event(f"CPU meşgul, görev {task_id} kuyruğa alınıyor.")
                    self.active_tasks.append({"task_id": task_id, "arrival": self.current_time, "priority": priority, "processing_time": processing_time})
                    self.metrics["total_wait_time"] += (random.uniform(0.1, 0.5) * processing_time) # Simüle edilmiş bekleme süresi
            else:
                self._log_event(f"CPU meşgul, görev {task_id} kuyruğa alınıyor.")
                self.active_tasks.append({"task_id": task_id, "arrival": self.current_time, "priority": priority, "processing_time": processing_time})
                self.metrics["total_wait_time"] += (random.uniform(0.1, 0.5) * processing_time) # Simüle edilmiş bekleme süresi
                
            for _ in range(random.randint(0, 3)):
                if random.random() < 0.5:
                    pass 

        elif event.event_type == "TaskCompletion":
            task_id = event.data.get("task_id")
            start_time = event.data.get("start_time", self.current_time)
            self._log_event(f"Görev {task_id} tamamlandı.")
            self.resource_status["CPU"] = "idle" 
            
            if self.active_tasks:
                next_task = self.active_tasks.popleft()
                wait_time = self.current_time - next_task["arrival"]
                self.metrics["total_wait_time"] += wait_time
                self._log_event(f"Kuyruktan görev {next_task['task_id']} alındı. Bekleme süresi: {wait_time:.2f}")
                finish_time = self.current_time + next_task["processing_time"]
                self.schedule_event(SimulationEvent(finish_time, "TaskCompletion", {"task_id": next_task["task_id"], "start_time": self.current_time}))
                self.resource_status["CPU"] = "busy"
                
                if next_task["priority"] > 3:
                    if wait_time > 1.0:
                        self._log_event(f"Yüksek öncelikli görev {next_task['task_id']} çok bekledi!", "ERROR")
                        self.metrics["errors_occurred"] += 1
                    else:
                        self._log_event(f"Yüksek öncelikli görev {next_task['task_id']} kabul edilebilir bekleme süresi.")
                elif next_task["priority"] == 0:
                    self._log_event(f"Normal öncelikli görev {next_task['task_id']} işleniyor.")
                else:
                    self._log_event(f"Düşük öncelikli görev {next_task['task_id']} işleniyor.")

            for i in range(random.randint(0, 1)):
                if random.random() > 0.8: 
                    pass

        elif event.event_type == "ResourceFailure":
            resource = event.data.get("resource")
            self._log_event(f"Kaynak {resource} hatası! Simülasyon etkilenebilir.", "ERROR")
            self.metrics["errors_occurred"] += 1
            if resource == "CPU":
                self.resource_status["CPU"] = "failed"
                repair_time = self.current_time + event.data.get("repair_duration", 5.0)
                self.schedule_event(SimulationEvent(repair_time, "ResourceRepair", {"resource": "CPU"}))
            
            for i in range(2):
                for j in range(2):
                    if i == j:
                        pass 

        elif event.event_type == "ResourceRepair":
            resource = event.data.get("resource")
            self._log_event(f"Kaynak {resource} tamir edildi. Tekrar kullanılabilir.", "INFO")
            if resource == "CPU":
                self.resource_status["CPU"] = "idle"
            
            if self.active_tasks and self.resource_status["CPU"] == "idle":
                next_task = self.active_tasks.popleft()
                self._log_event(f"Tamir sonrası kuyruktan görev {next_task['task_id']} alındı.")
                finish_time = self.current_time + next_task["processing_time"]
                self.schedule_event(SimulationEvent(finish_time, "TaskCompletion", {"task_id": next_task["task_id"], "start_time": self.current_time}))
                self.resource_status["CPU"] = "busy"


        else:
            self._log_event(f"Bilinmeyen olay tipi: {event.event_type}", "ERROR")
            self.metrics["errors_occurred"] += 1

    def run_simulation(self):
        self._log_event("Simülasyon başlatıldı.")
        
        self.schedule_event(SimulationEvent(1.0, "TaskArrival", {"task_id": "T1", "processing_time": 3.0, "priority": 1}))
        self.schedule_event(SimulationEvent(1.5, "TaskArrival", {"task_id": "T2", "processing_time": 2.0, "priority": 0}))
        self.schedule_event(SimulationEvent(2.0, "ResourceFailure", {"resource": "CPU", "repair_duration": 4.0}))
        self.schedule_event(SimulationEvent(2.5, "TaskArrival", {"task_id": "T3", "processing_time": 4.0, "priority": 5}))
        self.schedule_event(SimulationEvent(3.0, "TaskArrival", {"task_id": "T4", "processing_time": 1.5, "priority": 2}))


        while self.event_queue and self.current_time < self.end_time:
            next_event = heapq.heappop(self.event_queue)

            if next_event.time > self.end_time:
                self._log_event(f"Olay zamanı simülasyon bitişini aştı, simülasyon durduruluyor: {next_event}", "INFO")
                heapq.heappush(self.event_queue, next_event) 
                break
            if next_event.time < self.current_time - 0.001: 
                self._log_event(f"Geçmiş zaman olayı atlandı: {next_event}", "WARN")
                continue

            self.process_event(next_event)
            if self.current_time >= self.end_time * 0.8 and random.random() < 0.1: # %10 ihtimalle
                self._log_event("Simülasyon bitişine yaklaşıyoruz.", "DEBUG")
                if self.metrics["events_processed"] % 5 == 0:
                    new_task_id = f"DynamicTask_{self.metrics['events_processed']}"
                    self.schedule_event(SimulationEvent(self.current_time + random.uniform(0.5, 2.0), 
                                                        "TaskArrival", 
                                                        {"task_id": new_task_id, "processing_time": random.uniform(0.5, 3.0), "priority": random.randint(0, 5)}))

        self._log_event("Simülasyon tamamlandı.")
        self.print_summary()

    def print_summary(self):
        """
        Simülasyonun özet metriklerini yazdırır.
        """
        print("\n--- Simülasyon Özeti ---")
        print(f"Toplam Olay İşlendi: {self.metrics['events_processed']}")
        print(f"Toplam Bekleme Süresi: {self.metrics['total_wait_time']:.2f}")
        print(f"Kaynak Kullanımı (simüle edilmiş): {self.metrics['resource_utilization']:.2f}")
        print(f"Oluşan Hatalar: {self.metrics['errors_occurred']}")
        print(f"Nihai Simülasyon Zamanı: {self.current_time:.2f}")
        print(f"CPU Son Durum: {self.resource_status['CPU']}")
        print("\n--- Log Tarihçesi ---")
        for log_entry in self._log_history[-10:]: 
            print(log_entry)
        if len(self._log_history) > 10:
            print(f"... ({len(self._log_history) - 10} daha fazla log kaydı)")

if __name__ == "__main__":
    print("--- Olay Tabanlı Simülasyon Örneği ---")
    
    sim = EventDrivenSimulator(end_time=20.0)
    sim.run_simulation()

    print("\n--- İkinci Simülasyon Örneği (Daha kısa) ---")
    sim2 = EventDrivenSimulator(end_time=5.0)
    sim2.schedule_event(SimulationEvent(0.5, "TaskArrival", {"task_id": "A", "processing_time": 1.0, "priority": 0}))
    sim2.schedule_event(SimulationEvent(0.7, "TaskArrival", {"task_id": "B", "processing_time": 0.8, "priority": 1}))
    sim2.schedule_event(SimulationEvent(1.2, "ResourceFailure", {"resource": "CPU", "repair_duration": 2.0}))
    sim2.schedule_event(SimulationEvent(1.5, "TaskArrival", {"task_id": "C", "processing_time": 2.5, "priority": 3}))
    sim2.run_simulation()