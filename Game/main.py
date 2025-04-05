import sys
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QListWidget, QListWidgetItem, QStackedWidget,
                               QDialog, QFormLayout, QMessageBox, QTextEdit, QTreeWidget, QTreeWidgetItem)
from PySide6.QtCore import QTimer, Qt
from faker import Faker

fake = Faker()

# ------------------------
# OYUNDA KULLANILAN SINIFLAR
# ------------------------
class Website:
    def __init__(self, url, is_infected=False, protected=False):
        self.url = url
        self.is_infected = is_infected
        self.protected = protected       # Kullanıcı tarafından firewall kurulmuş mu?
        self.cracked = False             # Gerçek IP adresi tespit edildi mi?
        self.real_address = None         # Crack işleminden sonra gerçek IP
        self.ddos_count = 0              # DDoS saldırısı sayısı
        self.crashed = False             # Site çökme durumu
        self.infection_type = None       # Enfekte edici virüs türü (ör. Spyware, Trojan, vs.)
        self.locked = False              # Ransomware kilitleme durumu
        self.wiped = False               # Wiper etkisi

    def infect(self, virus_type=None):
        # Eğer firewall yok, site çökmediyse ve kilit/wipe durumu yoksa enfeksiyon gerçekleşir.
        if not self.protected and not self.crashed and not self.locked and not self.wiped:
            self.is_infected = True
            self.infection_type = virus_type

    def clean(self):
        # Temizlik, çökme veya kilit durumunda etkili olmayabilir.
        if not self.crashed and not self.locked and not self.wiped:
            self.is_infected = False
            self.infection_type = None

    def set_protection(self, status):
        # Koruma, site çökmediği sürece uygulanabilir.
        if not self.crashed:
            self.protected = status

    def crack(self):
        if not self.cracked and not self.crashed:
            self.cracked = True
            self.real_address = fake.ipv4()
            return True
        return False

    def ddos(self):
        if self.cracked and not self.crashed:
            self.ddos_count += 1
            if self.ddos_count >= 3:
                self.crashed = True
                return True
        return False

    def restart(self):
        if self.crashed or self.locked or self.wiped:
            self.crashed = False
            self.locked = False
            self.wiped = False
            self.ddos_count = 0
            self.is_infected = False
            self.infection_type = None
            self.cracked = False
            self.real_address = None
            return True
        return False

# Temel araç sınıfı
class SecurityTool:
    def __init__(self, name, price, power):
        self.name = name
        self.price = price
        self.power = power  # Genel etki oranı

    def __str__(self):
        return f"{self.name} (Fiyat: {self.price}, Güç: {self.power})"

# ------------------------
# ANTİVİRÜS VE İLGİLİ VIRÜS ARAÇLARI
# ------------------------
class Antivirus(SecurityTool):
    def __init__(self, name, price, power):
        super().__init__(name, price, power)
        
    def apply(self, website):
        # Eğer site enfekte ise, antivirüs temizleme denemesi yapar.
        if website.is_infected and not website.crashed:
            # Varsayılan antivirüs uygulaması
            if random.random() < self.power:
                website.clean()
                return True
        return False

# Yeni gelişmiş antivirüs sınıfı; vendor bilgileri, yanlış tespit riski ve firewall desteği içerir.
class AdvancedAntivirus(Antivirus):
    def __init__(self, vendor, price, detection_rate, false_positive_rate, has_firewall, premium, extra_features=None):
        # İsim, örneğin "Norton Antivirus Premium" şeklinde oluşturulsun.
        name = vendor + (" Premium" if premium else "")
        super().__init__(name, price, detection_rate)
        self.vendor = vendor
        self.false_positive_rate = false_positive_rate  # % olarak; örneğin 0.1 ise %10 yanlış tespit
        self.has_firewall = has_firewall
        self.premium = premium
        self.extra_features = extra_features or []
    def apply(self, website):
        if website.is_infected and not website.crashed:
            # Gelişmiş tespit şansı
            if random.random() < self.power:
                # Yanlış tespit riski
                if random.random() < self.false_positive_rate:
                    # Yanlış pozitif; temiz olmadığı halde yanlışlıkla temizlenme bildirimi
                    return "false_positive"
                website.clean()
                return True
        return False

# Virüs araçları: Temel virüs aracı ve alt sınıfları
class VirusTool(SecurityTool):
    def __init__(self, name, price, power):
        super().__init__(name, price, power)
        
    def apply(self, website):
        if not website.is_infected and not website.protected and not website.crashed:
            if random.random() < self.power:
                return True
        return False

class Spyware(VirusTool):
    def apply(self, website):
        if not website.is_infected and not website.protected and not website.crashed:
            if random.random() < self.power:
                website.infect("Spyware")
                return True
        return False

class Adware(VirusTool):
    def apply(self, website):
        if not website.is_infected and not website.protected and not website.crashed:
            if random.random() < self.power:
                website.infect("Adware")
                return True
        return False

class Trojan(VirusTool):
    def apply(self, website):
        if not website.is_infected and not website.protected and not website.crashed:
            if random.random() < self.power * 0.9:
                website.infect("Trojan")
                return True
        return False

class Worm(VirusTool):
    def apply(self, website):
        if not website.is_infected and not website.protected and not website.crashed:
            if random.random() < self.power:
                website.infect("Worm")
                return True
        return False

class Rootkit(VirusTool):
    def apply(self, website):
        if not website.is_infected and not website.protected and not website.crashed:
            if random.random() < self.power * 0.85:
                website.infect("Rootkit")
                return True
        return False

class Ransomware(VirusTool):
    def apply(self, website):
        if not website.is_infected and not website.protected and not website.crashed:
            if random.random() < self.power * 0.8:
                website.infect("Ransomware")
                website.locked = True
                return True
        return False

class Wiper(VirusTool):
    def apply(self, website):
        if not website.is_infected and not website.protected and not website.crashed:
            if random.random() < self.power * 0.75:
                website.infect("Wiper")
                website.wiped = True
                website.crashed = True
                return True
        return False

# ------------------------
# FARKLI GÜVENLİK ARAÇLARI: Firewall, HIPS, IDS
# ------------------------
class Firewall(SecurityTool):
    def __init__(self, name, price, power):
        super().__init__(name, price, power)
        
    def apply(self, website):
        website.set_protection(True)
        return True

class HIPS(SecurityTool):
    def __init__(self, name, price, power):
        super().__init__(name, price, power)
        
    def mitigate_infection(self, base_chance):
        reduction = self.power * 0.2
        return max(0.1, base_chance - reduction)

class IDS(SecurityTool):
    def __init__(self, name, price, power):
        super().__init__(name, price, power)
        
    def analyze(self, websites):
        anomalies = [site.url for site in websites if site.is_infected and not site.protected and not site.crashed]
        return anomalies

# ------------------------
# MARKET PENCERESİ
# ------------------------
class MarketDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Market - Güvenlik Araçları")
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        layout.addRow(QLabel("Satın alacağınız ürünü seçin:"))
        self.item_list = QListWidget()

        # Ürün listesine; hem eski antivirüs, virüs araçları, firewall, HIPS, IDS hem de gelişmiş antivirüs ürünleri ekleniyor.
        self.items = [
            # Geleneksel antivirüsler
            Antivirus("Basic Antivirus", 100, 0.65),
            Antivirus("Advanced Antivirus", 250, 0.80),
            # Gelişmiş antivirüs vendorleri (farklı markalar, özellikler, yanlış tespit riski, firewall desteği vb.)
            AdvancedAntivirus("Norton", 300, 0.85, 0.05, True, True, extra_features=["Zero Trust"]),
            AdvancedAntivirus("Kaspersky", 320, 0.88, 0.04, True, True, extra_features=["Signature Update"]),
            AdvancedAntivirus("Bitdefender", 340, 0.90, 0.03, True, True, extra_features=["AI Tespiti"]),
            AdvancedAntivirus("ESET NOD32", 280, 0.82, 0.06, False, False),
            AdvancedAntivirus("Avast", 260, 0.80, 0.07, True, False),
            AdvancedAntivirus("AVG", 250, 0.78, 0.08, False, False),
            AdvancedAntivirus("Vipre", 270, 0.79, 0.07, False, False),
            AdvancedAntivirus("SuperAntiSpyware", 290, 0.83, 0.06, False, False),
            AdvancedAntivirus("ClamAV", 0, 0.70, 0.02, False, False, extra_features=["Açık Kaynak"]),
            AdvancedAntivirus("HydraDragonAV", 0, 0.65, 0.20, False, False, extra_features=["Ücretsiz, Hantal"]),
            AdvancedAntivirus("Fortinet", 310, 0.84, 0.05, True, True),
            AdvancedAntivirus("Max Secure", 300, 0.82, 0.06, True, False),
            AdvancedAntivirus("Panda", 295, 0.80, 0.05, True, False),
            AdvancedAntivirus("Comodo", 280, 0.79, 0.04, True, True),
            AdvancedAntivirus("Trend Micro", 330, 0.86, 0.05, True, True),
            AdvancedAntivirus("GData", 305, 0.83, 0.06, True, False),
            AdvancedAntivirus("Arcabit", 270, 0.78, 0.07, False, False),
            AdvancedAntivirus("Spyhunter", 290, 0.80, 0.06, False, False),
            AdvancedAntivirus("Spybot Search And Destroy", 310, 0.81, 0.07, False, False),
            # Virüs araçları
            VirusTool("Generic Virus", 100, 0.60),
            Spyware("Spyware", 120, 0.60),
            Adware("Adware", 120, 0.60),
            Trojan("Trojan", 150, 0.65),
            Worm("Worm", 180, 0.70),
            Rootkit("Rootkit", 200, 0.70),
            Ransomware("Ransomware", 250, 0.75),
            Wiper("Wiper", 300, 0.80),
            # Güvenlik araçları
            Firewall("Standard Firewall", 150, 0.70),
            Firewall("Enterprise Firewall", 350, 0.85),
            HIPS("Basic HIPS", 120, 0.65),
            HIPS("Advanced HIPS", 300, 0.80),
            IDS("Simple IDS", 130, 0.60),
            IDS("Smart IDS", 320, 0.85),
        ]

        for item in self.items:
            desc = f"{item.name} - Fiyat: {item.price} Kredi, Güç: {item.power}"
            self.item_list.addItem(QListWidgetItem(desc))
        layout.addRow(self.item_list)
        purchase_button = QPushButton("Satın Al")
        purchase_button.clicked.connect(self.purchase_item)
        layout.addRow(purchase_button)
        self.setLayout(layout)

    def purchase_item(self):
        selected_items = self.item_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen satın alacağınız ürünü seçin.")
            return
        index = self.item_list.row(selected_items[0])
        selected_tool = self.items[index]
        self.parent.purchase(selected_tool)
        self.accept()

# ------------------------
# SITE İÇERİĞİ & DOSYA AĞACI DİYALOĞU
# ------------------------
class SiteContentDialog(QDialog):
    def __init__(self, website, parent=None):
        super().__init__(parent)
        self.website = website
        self.setWindowTitle(f"Site İçeriği - {website.url}")
        self.resize(600, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        content = fake.paragraph(nb_sentences=5)
        content_label = QLabel("Site İçeriği:")
        content_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(content_label)
        content_text = QTextEdit()
        content_text.setReadOnly(True)
        content_text.setText(content)
        layout.addWidget(content_text)

        status = f"Durum: {'ÇÖKÜK' if self.website.crashed else ('Kilitli' if self.website.locked else 'Normal')}"
        if self.website.infection_type:
            status += f" | Enfekte: {self.website.infection_type}"
        status_label = QLabel(status)
        status_label.setStyleSheet("font-style: italic;")
        layout.addWidget(status_label)

        if self.website.is_infected:
            tree_label = QLabel("Dosya Ağacı (Enfekte dosyalar):")
            tree_label.setStyleSheet("font-weight: bold;")
            layout.addWidget(tree_label)
            self.tree = QTreeWidget()
            self.tree.setHeaderHidden(True)
            root = QTreeWidgetItem([fake.word().capitalize()])
            for _ in range(random.randint(2, 5)):
                child = QTreeWidgetItem([fake.file_name(extension="txt")])
                for _ in range(random.randint(1, 3)):
                    subchild = QTreeWidgetItem([fake.file_name(extension="log")])
                    child.addChild(subchild)
                root.addChild(child)
            self.tree.addTopLevelItem(root)
            layout.addWidget(self.tree)
        else:
            clean_label = QLabel("Site temiz, dosya ağacı mevcut değil.")
            layout.addWidget(clean_label)
        self.setLayout(layout)

# ------------------------
# OYUN PANOSU
# ------------------------
class GameBoardWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.credits = 1000       # Başlangıç kredisi
        self.score = 0
        self.owned_tools = []     # Aktif satın alınmış araçlar
        self.tool_timers = []     # (tool, QTimer) çiftleri
        # Firewall uygulamaları için site bazlı timer saklanacak
        self.firewall_effects = {}  # {website: QTimer}
        # Antivirus imza güncelleme için geçici yükseltmeleri saklayalım
        self.upgraded_antiviruses = {}
        self.init_ui()
        self.generate_websites()
        self.init_timers()

    def init_ui(self):
        layout = QVBoxLayout()
        self.info_label = QLabel(f"Kredi: {self.credits} | Skor: {self.score}")
        layout.addWidget(self.info_label)
        self.website_list = QListWidget()
        layout.addWidget(self.website_list)
        btn_layout = QHBoxLayout()
        self.scan_btn = QPushButton("Siteyi Tara (Antivirüs)")
        self.scan_btn.clicked.connect(self.scan_website)
        btn_layout.addWidget(self.scan_btn)
        self.infect_btn = QPushButton("Siteyi Enfekte Et (Virüs)")
        self.infect_btn.clicked.connect(self.infect_website)
        btn_layout.addWidget(self.infect_btn)
        self.firewall_btn = QPushButton("Seçili Siteye Firewall Kur")
        self.firewall_btn.clicked.connect(self.deploy_firewall)
        btn_layout.addWidget(self.firewall_btn)
        self.hips_btn = QPushButton("HIPS Aktifleştir")
        self.hips_btn.clicked.connect(self.activate_hips)
        btn_layout.addWidget(self.hips_btn)
        self.ids_btn = QPushButton("IDS Çalıştır")
        self.ids_btn.clicked.connect(self.run_ids)
        btn_layout.addWidget(self.ids_btn)
        self.market_btn = QPushButton("Marketi Aç")
        self.market_btn.clicked.connect(self.open_market)
        btn_layout.addWidget(self.market_btn)
        self.view_content_btn = QPushButton("Site İçeriğini Görüntüle")
        self.view_content_btn.clicked.connect(self.view_site_content)
        btn_layout.addWidget(self.view_content_btn)
        self.crack_btn = QPushButton("Siteyi Crackle")
        self.crack_btn.clicked.connect(self.crack_website)
        btn_layout.addWidget(self.crack_btn)
        self.ddos_btn = QPushButton("DDoS Saldırısı")
        self.ddos_btn.clicked.connect(self.ddos_attack)
        btn_layout.addWidget(self.ddos_btn)
        self.restart_btn = QPushButton("Siteyi Yeniden Başlat")
        self.restart_btn.clicked.connect(self.restart_site)
        btn_layout.addWidget(self.restart_btn)
        self.upgrade_btn = QPushButton("Antivirus İmza Güncelle (100 kredi)")
        self.upgrade_btn.clicked.connect(self.upgrade_antivirus)
        btn_layout.addWidget(self.upgrade_btn)
        layout.addLayout(btn_layout)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
        self.setLayout(layout)

    def log_event(self, message):
        self.log_text.append(message)

    def generate_websites(self):
        self.websites = []
        self.website_list.clear()
        for _ in range(12):
            url = fake.url()
            infected = random.random() < 0.2
            website = Website(url, is_infected=infected, protected=False)
            self.websites.append(website)
            self.add_website_to_list(website)

    def add_website_to_list(self, website):
        if website.crashed:
            status = "ÇÖKÜK"
        elif website.is_infected:
            status = f"Enfekte ({website.infection_type})" if website.infection_type else "Enfekte"
        else:
            status = "Temiz"
        if website.protected:
            status += " (Firewall)"
        if website.cracked:
            status += " [Cracked]"
        item = QListWidgetItem(f"{website.url} - {status}")
        self.website_list.addItem(item)

    def update_website_list(self):
        self.website_list.clear()
        for website in self.websites:
            self.add_website_to_list(website)
        self.check_game_over()

    def init_timers(self):
        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.update_game)
        self.game_timer.start(4000)

    def update_game(self):
        for website in self.websites:
            # NOT: Artık global firewall uygulanmıyor; kullanıcı seçilen siteye kuruyor.
            if not website.crashed:
                if not website.is_infected and not website.protected and random.random() < 0.15:
                    website.infect()
                    self.log_event(f"{website.url} rastgele enfekte oldu.")
                if website.is_infected and random.random() < 0.05:
                    website.clean()
                    self.log_event(f"{website.url} kendiliğinden temizlendi.")
                if website.ddos_count > 0 and website.ddos_count < 3 and random.random() < 0.1:
                    website.ddos_count += 1
                    self.log_event(f"{website.url} üzerine rastgele DDoS etkisi oluştu.")
                if website.ddos_count >= 3:
                    website.crashed = True
                    self.log_event(f"{website.url} aşırı DDoS nedeniyle çöktü!")
        self.credits += 5  # Güncelleme bonusu
        self.update_website_list()
        self.info_label.setText(f"Kredi: {self.credits} | Skor: {self.score}")

    def check_game_over(self):
        lose = all(site.is_infected or site.crashed for site in self.websites)
        if lose:
            self.log_event("Tüm siteler enfekte/çökmüş! Oyun bitti.")
            QMessageBox.critical(self, "Oyun Bitti", "Tüm siteler enfekte veya çöktü. Oyun bitti!")
            self.game_timer.stop()

    # ------------------------
    # Aksiyon Fonksiyonları
    # ------------------------
    def scan_website(self):
        selected_items = self.website_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen taranacak site seçin.")
            return
        index = self.website_list.row(selected_items[0])
        website = self.websites[index]
        base_chance = 0.5
        result = None
        for tool in self.owned_tools:
            if isinstance(tool, Antivirus):
                # Eğer gelişmiş antivirüs kullanılıyorsa, apply() metodu "false_positive" dönebilir.
                res = tool.apply(website)
                if res == "false_positive":
                    self.score -= 10
                    self.credits -= 20
                    self.log_event(f"{website.url} yanlış pozitif sonucu! (-10 skor, -20 kredi)")
                    result = False
                    break
                elif res is True:
                    result = True
                    break
                else:
                    base_chance = max(base_chance, tool.power)
        if website.is_infected and not website.crashed:
            if result is None and random.random() < base_chance:
                website.clean()
                self.score += 15
                self.credits += 50
                self.log_event(f"{website.url} antivirüs tarafından temizlendi. +50 kredi kazandınız.")
                QMessageBox.information(self, "Sonuç", "Site temizlendi!")
            elif result is False:
                QMessageBox.information(self, "Sonuç", "Yanlış pozitif nedeniyle işlem yapıldı.")
            else:
                self.log_event(f"{website.url} antivirüs taramasından kaçtı.")
                QMessageBox.information(self, "Sonuç", "Tarama başarısız oldu.")
        else:
            self.log_event(f"{website.url} zaten temiz veya çökük durumda.")
            QMessageBox.information(self, "Sonuç", "Site zaten temiz.")
        self.update_website_list()
        self.info_label.setText(f"Kredi: {self.credits} | Skor: {self.score}")

    def infect_website(self):
        selected_items = self.website_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen enfekte edilecek site seçin.")
            return
        index = self.website_list.row(selected_items[0])
        website = self.websites[index]
        if website.is_infected or website.crashed:
            self.log_event(f"{website.url} zaten enfekte veya çökük.")
            QMessageBox.information(self, "Sonuç", "Site zaten enfekte veya çökük!")
            return
        virus_tool = None
        for tool in self.owned_tools:
            if isinstance(tool, VirusTool):
                if virus_tool is None or tool.power > virus_tool.power:
                    virus_tool = tool
        if virus_tool is None:
            QMessageBox.warning(self, "Uyarı", "Herhangi bir virüs aracı satın alınmamış!")
            return
        base_chance = virus_tool.power
        for tool in self.owned_tools:
            if isinstance(tool, HIPS):
                base_chance = tool.mitigate_infection(base_chance)
        if random.random() < base_chance:
            success = virus_tool.apply(website)
            if success:
                if isinstance(virus_tool, Worm):
                    self.score += 25
                    self.credits += 20
                    self.log_event(f"{website.url} Worm virüsüyle enfekte edildi, yayılma denemesi başlatılıyor. (+25 skor, +20 kredi)")
                    for other in self.websites:
                        if other != website and not other.is_infected and random.random() < 0.3:
                            other.infect("Worm")
                            self.log_event(f"{other.url} Worm virüsüyle otomatik enfekte oldu.")
                else:
                    self.score += 20
                    self.credits += 30
                    self.log_event(f"{website.url} {website.infection_type} saldırısıyla enfekte edildi. (+20 skor, +30 kredi)")
                QMessageBox.information(self, "Sonuç", "Site enfekte edildi!")
            else:
                self.log_event(f"{website.url} enfeksiyon saldırısını püskürttü.")
                QMessageBox.information(self, "Sonuç", "Enfeksiyon başarısız oldu.")
        else:
            self.log_event(f"{website.url} enfeksiyon saldırısı HIPS etkisiyle başarısız oldu.")
            QMessageBox.information(self, "Sonuç", "Enfeksiyon başarısız oldu.")
        self.update_website_list()
        self.info_label.setText(f"Kredi: {self.credits} | Skor: {self.score}")

    def deploy_firewall(self):
        selected_items = self.website_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen firewall kurulacak site seçin.")
            return
        index = self.website_list.row(selected_items[0])
        website = self.websites[index]
        # Kullanıcının firewall aracı varsa, ondan en iyisini seçiyoruz.
        fw_tool = None
        for tool in self.owned_tools:
            if isinstance(tool, Firewall):
                if fw_tool is None or tool.power > fw_tool.power:
                    fw_tool = tool
        if fw_tool is None:
            QMessageBox.warning(self, "Uyarı", "Herhangi bir firewall aracı satın alınmamış!")
            return
        # Seçilen siteye firewall kur.
        if fw_tool.apply(website):
            self.log_event(f"{website.url} için {fw_tool.name} başarıyla kuruldu.")
            QMessageBox.information(self, "Firewall", "Firewall başarıyla kuruldu!")
            # Firewall etkisi 30 saniye sürecek; ardından site koruması kaldırılır.
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(lambda: self.remove_firewall_effect(website))
            timer.start(30000)
            self.firewall_effects[website] = timer
            # Kullanılan firewall aracı devreden çıkar.
            self.owned_tools.remove(fw_tool)
        else:
            self.log_event("Firewall kurulamadı.")
            QMessageBox.information(self, "Firewall", "Firewall kurulamadı.")
        self.update_website_list()
        self.info_label.setText(f"Kredi: {self.credits} | Skor: {self.score}")

    def remove_firewall_effect(self, website):
        website.set_protection(False)
        self.log_event(f"{website.url} üzerindeki firewall etkisi sona erdi.")
        self.update_website_list()

    def activate_hips(self):
        hips_chance = 0.0
        for tool in self.owned_tools:
            if isinstance(tool, HIPS):
                hips_chance = max(hips_chance, tool.power)
        if random.random() < hips_chance:
            self.log_event("HIPS etkinleşti: Enfeksiyon girişimleri azalacak.")
            QMessageBox.information(self, "HIPS", "HIPS başarıyla etkinleşti!")
        else:
            self.log_event("HIPS etkinleştirilemedi.")
            QMessageBox.information(self, "HIPS", "HIPS etkinleştirilemedi.")

    def run_ids(self):
        ids_found = False
        log_messages = []
        for tool in self.owned_tools:
            if isinstance(tool, IDS):
                anomalies = tool.analyze(self.websites)
                if anomalies:
                    ids_found = True
                    log_messages.append("IDS tespitleri:")
                    for anomaly in anomalies:
                        log_messages.append(f" - {anomaly}")
        if ids_found:
            for msg in log_messages:
                self.log_event(msg)
            QMessageBox.information(self, "IDS", "Anormal aktiviteler log panelinde görüntülendi.")
        else:
            self.log_event("IDS: Her şey normal görünüyor.")
            QMessageBox.information(self, "IDS", "Her şey normal.")
    
    def open_market(self):
        market = MarketDialog(self)
        market.exec()

    def view_site_content(self):
        selected_items = self.website_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen görüntülenecek site seçin.")
            return
        index = self.website_list.row(selected_items[0])
        website = self.websites[index]
        dialog = SiteContentDialog(website, self)
        dialog.exec()

    def crack_website(self):
        selected_items = self.website_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen cracklenecek site seçin.")
            return
        index = self.website_list.row(selected_items[0])
        website = self.websites[index]
        if website.cracked:
            self.log_event(f"{website.url} zaten cracklenmiş.")
            QMessageBox.information(self, "Crack", "Site zaten cracklenmiş!")
            return
        if random.random() < 0.6:
            website.crack()
            self.credits += 20
            self.log_event(f"{website.url} cracklendi! Gerçek IP: {website.real_address} (+20 kredi)")
            QMessageBox.information(self, "Crack", f"Site cracklendi! Gerçek IP: {website.real_address}")
        else:
            self.log_event(f"{website.url} cracklenemedi.")
            QMessageBox.information(self, "Crack", "Crack işlemi başarısız oldu.")
        self.update_website_list()
        self.info_label.setText(f"Kredi: {self.credits} | Skor: {self.score}")

    def ddos_attack(self):
        selected_items = self.website_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen DDoS saldırısı yapılacak site seçin.")
            return
        index = self.website_list.row(selected_items[0])
        website = self.websites[index]
        if not website.cracked:
            self.log_event(f"{website.url} cracklenmediği için DDoS saldırısı yapılamaz.")
            QMessageBox.warning(self, "DDoS", "Site cracklenmeden DDoS saldırısı yapılamaz!")
            return
        if website.crashed:
            self.log_event(f"{website.url} zaten çökmüş durumda.")
            QMessageBox.information(self, "DDoS", "Site zaten çökmüş!")
            return
        if random.random() < 0.5:
            crashed = website.ddos()
            if crashed:
                self.score += 30
                self.credits += 40
                self.log_event(f"{website.url} DDoS saldırısı sonucu çöktü! (+30 skor, +40 kredi)")
                QMessageBox.information(self, "DDoS", "Site DDoS saldırısı sonucu çöktü!")
            else:
                self.score += 10
                self.credits += 20
                self.log_event(f"{website.url} DDoS saldırısı başarılı, ancak çökmedi. (+10 skor, +20 kredi)")
                QMessageBox.information(self, "DDoS", "DDoS saldırısı başarılı!")
        else:
            self.log_event(f"{website.url} DDoS saldırısı başarısız oldu.")
            QMessageBox.information(self, "DDoS", "DDoS saldırısı başarısız oldu.")
        self.update_website_list()
        self.info_label.setText(f"Kredi: {self.credits} | Skor: {self.score}")

    def restart_site(self):
        selected_items = self.website_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen yeniden başlatılacak site seçin.")
            return
        index = self.website_list.row(selected_items[0])
        website = self.websites[index]
        if not (website.crashed or website.locked or website.wiped):
            QMessageBox.information(self, "Restart", "Site çökük veya kilitli durumda değil.")
            return
        cost = 50
        if self.credits < cost:
            QMessageBox.warning(self, "Restart", "Yeterli kredi yok!")
            return
        self.credits -= cost
        website.restart()
        self.log_event(f"{website.url} {cost} kredi ödenerek yeniden başlatıldı.")
        QMessageBox.information(self, "Restart", "Site yeniden başlatıldı!")
        self.update_website_list()
        self.info_label.setText(f"Kredi: {self.credits} | Skor: {self.score}")

    def upgrade_antivirus(self):
        # Antivirus imza güncellemesi: 100 kredi ödeyerek tüm satın alınmış antivirüs araçlarının gücü 0.05 artar (30 saniye)
        if self.credits < 100:
            QMessageBox.warning(self, "Upgrade", "Yeterli kredi yok!")
            return
        self.credits -= 100
        self.log_event("Antivirus imza güncellemesi uygulandı: Tespit oranları geçici olarak yükseldi.")
        for tool in self.owned_tools:
            if isinstance(tool, Antivirus):
                if tool not in self.upgraded_antiviruses:
                    self.upgraded_antiviruses[tool] = tool.power
                    tool.power = min(tool.power + 0.05, 0.99)
        # 30 saniye sonra yükseltmeyi geri alacak timer
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(self.revert_antivirus_upgrade)
        timer.start(30000)
        self.log_event("Antivirus imza güncellemesi 30 saniye boyunca aktif.")
        self.info_label.setText(f"Kredi: {self.credits} | Skor: {self.score}")

    def revert_antivirus_upgrade(self):
        for tool, original_power in self.upgraded_antiviruses.items():
            tool.power = original_power
        self.upgraded_antiviruses.clear()
        self.log_event("Antivirus imza güncellemesi etkisi sona erdi.")
        self.info_label.setText(f"Kredi: {self.credits} | Skor: {self.score}")

    def purchase(self, tool):
        if self.credits >= tool.price:
            self.credits -= tool.price
            self.owned_tools.append(tool)
            self.log_event(f"{tool.name} satın alındı! (Etkin: 30 saniye)")
            QMessageBox.information(self, "Satın Alma", f"{tool.name} satın alındı!")
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(lambda: self.expire_tool(tool))
            timer.start(30000)
            self.tool_timers.append((tool, timer))
        else:
            QMessageBox.warning(self, "Satın Alma", "Yeterli kredi yok!")
        self.info_label.setText(f"Kredi: {self.credits} | Skor: {self.score}")

    def expire_tool(self, tool):
        if tool in self.owned_tools:
            self.owned_tools.remove(tool)
            self.log_event(f"{tool.name} süresi doldu ve devreden çıktı.")
            self.info_label.setText(f"Kredi: {self.credits} | Skor: {self.score}")

# ------------------------
# ANA OYUN PENCERESİ
# ------------------------
class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Siber Güvenlik Simülasyonu")
        self.setGeometry(100, 100, 1100, 750)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.game_board = GameBoardWidget(self)
        self.central_widget.addWidget(self.game_board)
        self.apply_styles()

    def apply_styles(self):
        style = """
        QWidget { background-color: #2b2b2b; color: #e0e0e0; font-family: Arial, sans-serif; font-size: 14px; }
        QPushButton { background: #007bff; color: white; border: 2px solid #0056b3; padding: 6px 12px; border-radius: 8px; }
        QPushButton:hover { background: #0056b3; }
        QLabel { color: #e0e0e0; }
        QLineEdit { background-color: #1e1e1e; color: #dcdcdc; border: 1px solid #3c3c3c; padding: 4px; }
        QTextEdit { background-color: #1e1e1e; color: #dcdcdc; border: 1px solid #3c3c3c; padding: 5px; }
        QListWidget { background-color: #1e1e1e; }
        QTreeWidget { background-color: #1e1e1e; }
        """
        self.setStyleSheet(style)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())
