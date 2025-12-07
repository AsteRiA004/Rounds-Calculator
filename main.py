import sys
import json
import pygame
import math
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QHBoxLayout, QLineEdit, QScrollArea
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1920, 1080)
        self.showMaximized()
        self.setWindowTitle("Rounds Calculator")

        self.program_directory = os.path.dirname(os.path.abspath(__file__))

        self.setWindowIcon(QIcon(os.path.join(self.program_directory, "assets/RoundsIconDark.png")))
        pygame.mixer.init()
        self.select_sound = pygame.mixer.Sound(os.path.join(self.program_directory, "assets/select.mp3"))
        self.undo_sound = pygame.mixer.Sound(os.path.join(self.program_directory, "assets/undo.mp3"))

        with open(os.path.join(self.program_directory, "assets/data.json"), "r") as f:
            self.data = json.load(f)

        self.cards_list = []
        
        # my label images
        self.my_label1 = QLabel(self)
        self.my_label2 = QLabel(self)
        self.my_label3 = QLabel(self)
        self.my_label4 = QLabel(self)
        self.my_label5 = QLabel(self)

        # my undo buttons
        self.my_button1 = QPushButton("↺", self)
        self.my_button2 = QPushButton("↺", self)
        self.my_button3 = QPushButton("↺", self)
        self.my_button4 = QPushButton("↺", self)
        self.my_button5 = QPushButton("↺", self)

        self.reset_button = QPushButton("❌", self)

        # my info label
        self.my_info_label = QLabel("Damage: 55.0\nMax bullet DPS: 54.46\nAttack speed: 100.0%\nReload time: 2.33s\nBullet speed: 100.0%\nHealth: 100.0\nLife steal: 0%\nAverage block damage: 0\nMaximum block damage: 0\nBlock cooldown: 4.75s", self)

        self.scroll1 = QScrollArea(self)

        # line edit
        self.line_edit = QLineEdit(self)      

        # pixmaps 
        self.background_pixmap = QPixmap(os.path.join(self.program_directory, "assets/RoundsBackground.png"))
        
        self.pixmap1 = QPixmap()
        self.pixmap2 = QPixmap()
        self.pixmap3 = QPixmap()
        self.pixmap4 = QPixmap()
        self.pixmap5 = QPixmap()
        
        self.all_labels = [self.my_label1, self.my_label2, self.my_label3, self.my_label4, self.my_label5]
        self.all_buttons = [self.my_button1, self.my_button2, self.my_button3, self.my_button4, self.my_button5]
        self.all_info_labels = [self.my_info_label]

        self.initUI()

    def initUI(self):
        central_widget = QWidget()  
        self.setCentralWidget(central_widget)
        
        self.background_label = QLabel(central_widget)
        self.background_label.setScaledContents(False)
        self.background_label.setPixmap(self.background_pixmap)
        
        for label in self.all_labels:
            label.setScaledContents(True)
            label.resize(260, 360)
            label.setMargin(0)
            label.hide()
   
        self.setStyleSheet("""
                     QLabel {
                        background-color: transparent; 
                        margin: 0px;
                        padding: 0px;
                         
                           }      
                           
                           
                           """)
        
        # undo buttons
        for btn in self.all_buttons:
            btn.setFixedSize(60, 60)
            btn.hide()
            btn.clicked.connect(self.undo)
            
        self.setStyleSheet("""
                QPushButton {
                            font-family: 'Segoe UI';
                            font-size: 30px;
                            border-radius: 30px;
                            border: 0px solid black;
                            background-color: transparent;
                            color: white
                           
                           
                            }
                QPushButton:hover {
                            background-color: #97c8db;
                            color: black
                            }
                            """)

        # reset button
        self.reset_button.setFixedSize(60, 60)
        self.reset_button.clicked.connect(self.reset)

        self.setStyleSheet("""
                QPushButton {
                            font-family: 'Segoe UI';
                            font-size: 30px;
                            border-radius: 30px;
                            border: 0px solid black;
                            background-color: transparent;
                            color: white
                           
                           
                            }
                QPushButton:hover {
                            background-color: #97c8db;
                            color: black
                            }
                            """)

        self.line_edit.setFixedHeight(45)
        self.line_edit.setToolTip("Input card name...")
        self.line_edit.setStyleSheet("""
                        font-family: 'Inter';
                        
                        font-size: 20px;                 
                                     
                                     """)
        self.line_edit.setFocus()
        self.line_edit.returnPressed.connect(self.submit)

        # scroll
        self.my_info_label.setWordWrap(True)
        self.scroll1.setWidgetResizable(True)
        self.scroll1.setWidget(self.my_info_label)
        self.scroll1.setFixedHeight(400)
        self.scroll1.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll1.setStyleSheet("""
                        background-color: transparent; 
                        font-size: 37px;
                        font-weight: bold;
                        font-family: 'Inter';
                        margin: 0px;
                        padding: 0px;
                        border: 2px white;
                        color: white;
                                         
                                         """)

        vbox1 = QVBoxLayout()     
        vbox1.setSpacing(0)
        vbox1.setContentsMargins(0, 0, 0, 0)
        vbox1.addWidget(self.my_label1, alignment = Qt.AlignHCenter | Qt.AlignTop)
        vbox1.addWidget(self.my_button1, alignment = Qt.AlignHCenter | Qt.AlignTop)

        vbox3 = QVBoxLayout()
        vbox3.setSpacing(0)
        vbox3.setContentsMargins(0, 0, 0, 0)
        vbox3.addWidget(self.my_label2, alignment = Qt.AlignHCenter | Qt.AlignTop)
        vbox3.addWidget(self.my_button2, alignment = Qt.AlignHCenter | Qt.AlignTop)

        vbox4 = QVBoxLayout()
        vbox4.setSpacing(0)
        vbox4.setContentsMargins(0, 0, 0, 0)
        vbox4.addWidget(self.my_label3, alignment = Qt.AlignHCenter | Qt.AlignTop)
        vbox4.addWidget(self.my_button3, alignment = Qt.AlignHCenter | Qt.AlignTop)

        vbox7 = QVBoxLayout()
        vbox7.setSpacing(0)
        vbox7.setContentsMargins(0, 0, 0, 0)
        vbox7.addWidget(self.my_label4, alignment = Qt.AlignHCenter | Qt.AlignTop)
        vbox7.addWidget(self.my_button4, alignment = Qt.AlignHCenter | Qt.AlignTop)

        vbox8 = QVBoxLayout()
        vbox8.setSpacing(0)
        vbox8.setContentsMargins(0, 0, 0, 0)
        vbox8.addWidget(self.my_label5, alignment = Qt.AlignHCenter | Qt.AlignTop)
        vbox8.addWidget(self.my_button5, alignment = Qt.AlignHCenter | Qt.AlignTop)


        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.scroll1)
        hbox1.addWidget(self.reset_button, alignment = Qt.AlignRight | Qt.AlignBottom)
        
        hbox2 = QHBoxLayout()
        hbox2.addLayout(vbox1)
        hbox2.addLayout(vbox3)
        hbox2.addLayout(vbox4)
        hbox2.addLayout(vbox7)
        hbox2.addLayout(vbox8)

        hbox3 = QHBoxLayout()
        hbox3.setContentsMargins(0, 0, 0, 0)
        hbox3.addWidget(self.line_edit, alignment = Qt.AlignBottom)

        vbox1 = QVBoxLayout()
        vbox1.addLayout(hbox1)
        vbox1.addLayout(hbox2)
        vbox1.addLayout(hbox3)

        vbox = QVBoxLayout()
        vbox.addLayout(vbox1)
        
        central_widget.setLayout(vbox)
        self.background_label.lower()

    def resizeEvent(self, event):
        try:
            self.background_label.setGeometry(0, 0, self.width(), self.height())
            
            scaled_pixmap = self.background_pixmap.scaled(
                self.width(),                    
                self.height(),                   
                Qt.KeepAspectRatioByExpanding,   
                Qt.SmoothTransformation          
            )
                    
            self.background_label.setPixmap(scaled_pixmap)
        
            super().resizeEvent(event)
        except:
            pass

    def submit(self):
        self.line_edit_text = self.line_edit.text().strip()
        self.line_edit_text = self.line_edit_text.title()

        #abbreviations
        if self.line_edit_text not in self.data: 
            if self.line_edit_text == "Abyssal":
                self.line_edit_text = "Abyssal Countdown"
            elif self.line_edit_text == "Bar" or self.line_edit_text == "Barr":
                self.line_edit_text = "Barrage"
            elif self.line_edit_text == "Big" or self.line_edit_text == "Big Bullets":
                self.line_edit_text = "Big Bullet"
            elif self.line_edit_text == "Bombs":
                self.line_edit_text = "Bombs Away"
            elif self.line_edit_text == "Bounce":
                self.line_edit_text = "Bouncy"
            elif self.line_edit_text == "Brawl":
                self.line_edit_text = "Brawler"
            elif self.line_edit_text == "Buck" or self.line_edit_text == "Shotgun":
                self.line_edit_text = "Buckshot"
            elif self.line_edit_text == "Bur":
                self.line_edit_text = "Burst"
            elif self.line_edit_text == "Careful" or self.line_edit_text == "Planning":
                self.line_edit_text = "Careful Planning"
            elif self.line_edit_text == "Cha":
                self.line_edit_text = "Chase"
            elif self.line_edit_text == "Chill" or self.line_edit_text == "Presence" or self.line_edit_text == "Chilling":
                self.line_edit_text = "Chilling Presence"
            elif self.line_edit_text == "Cold":
                self.line_edit_text = "Cold Bullets"
            elif self.line_edit_text == "Comb" or self.line_edit_text == "Com":
                self.line_edit_text = "Combine"
            elif self.line_edit_text == "Daz" or self.line_edit_text == "Dazz" or self.line_edit_text == "Dazzl":
                self.line_edit_text = "Dazzle"
            elif self.line_edit_text == "Dec":
                self.line_edit_text = "Decay"
            elif self.line_edit_text == "Def" or self.line_edit_text == "Defend":
                self.line_edit_text = "Defender"
            elif self.line_edit_text == "Demonic" or self.line_edit_text == "Dem" or self.line_edit_text == "Pact":
                self.line_edit_text = "Demonic Pact"
            elif self.line_edit_text == "Drill":
                self.line_edit_text = "Drill Ammo"
            elif self.line_edit_text == "Empow":
                self.line_edit_text = "Empower"
            elif self.line_edit_text == "Explosive":
                self.line_edit_text = "Explosive Bullet"
            elif self.line_edit_text == "Forward" or self.line_edit_text == "Fast For":
                self.line_edit_text = "Fast Forward"
            elif self.line_edit_text == "Frost" or self.line_edit_text == "Slam":
                self.line_edit_text = "Frost Slam"
            elif self.line_edit_text == "Glass" or self.line_edit_text == "Cannon":
                self.line_edit_text = "Glass Cannon"
            elif self.line_edit_text == "Gro":
                self.line_edit_text = "Grow"
            elif self.line_edit_text == "Healing" or self.line_edit_text == "Field" or self.line_edit_text == "Healing Sweep" or self.line_edit_text == "Best Card":
                self.line_edit_text = "Healing Field"
            elif self.line_edit_text == "Home" or self.line_edit_text == "Hom":
                self.line_edit_text = "Homing"
            elif self.line_edit_text == "Imp" or self.line_edit_text == "Impl":
                self.line_edit_text = "Implode"
            elif self.line_edit_text == "Lech":
                self.line_edit_text = "Leech"
            elif self.line_edit_text == "Lifesteal":
                self.line_edit_text = "Lifestealer"
            elif self.line_edit_text == "May" or self.line_edit_text == "Mayham":
                self.line_edit_text = "Mayhem"
            elif self.line_edit_text == "Op" or self.line_edit_text == "Overpow" or self.line_edit_text == "Power":
                self.line_edit_text = "Overpower"
            elif self.line_edit_text == "Para" or self.line_edit_text == "Paras" or self.line_edit_text == "Parasit":
                self.line_edit_text = "Parasite"
            elif self.line_edit_text == "Phoe" or self.line_edit_text == "Phoen" or self.line_edit_text == "Phoeni":
                self.line_edit_text = "Phoenix"
            elif self.line_edit_text == "Poi" or self.line_edit_text == "Poisn" or self.line_edit_text == "Poiso":
                self.line_edit_text = "Poison"
            elif "Pristine" in self.line_edit_text or "Perseverance" in self.line_edit_text or "Perserverence" in self.line_edit_text or self.line_edit_text == "Prist":
                self.line_edit_text = "Pristine Perseverence"
            elif self.line_edit_text == "Reload":
                self.line_edit_text = "Quick Reload"
            elif self.line_edit_text == "Quickshot":
                self.line_edit_text = "Quick Shot"
            elif self.line_edit_text == "Radar":
                self.line_edit_text = "Radar Shot"
            elif self.line_edit_text == "Rad" or self.line_edit_text == "Radi":
                self.line_edit_text = "Radiance"
            elif self.line_edit_text == "Ref" or self.line_edit_text == "Fresh":
                self.line_edit_text = "Refresh"
            elif self.line_edit_text == "Remot":
                self.line_edit_text = "Remote"
            elif self.line_edit_text == "Ricc" or self.line_edit_text == "Ricco" or self.line_edit_text == "Ricochet":
                self.line_edit_text = "Riccochet"
            elif self.line_edit_text == "Scav" or "Scaveng" in self.line_edit_text:
                self.line_edit_text = "Scavenger"
            elif self.line_edit_text == "Charge":
                self.line_edit_text = "Shield Charge"
            elif self.line_edit_text == "Up":
                self.line_edit_text = "Shields Up"
            elif self.line_edit_text == "Shock" or self.line_edit_text == "Wave":
                self.line_edit_text = "Shockwave"
            elif self.line_edit_text == "Silent" or self.line_edit_text == "Sile" or self.line_edit_text == "Silenc":
                self.line_edit_text = "Silence"
            elif self.line_edit_text == "Sneak":
                self.line_edit_text = "Sneaky"
            elif self.line_edit_text == "Static":
                self.line_edit_text = "Static Field"
            elif self.line_edit_text == "Steady":
                self.line_edit_text = "Steady Shot"
            elif self.line_edit_text == "Super" or self.line_edit_text == "Nova":
                self.line_edit_text = "Supernova"
            elif self.line_edit_text == "Tactic" or self.line_edit_text == "Tactical":
                self.line_edit_text = "Tactical Reload"
            elif self.line_edit_text == "Target":
                self.line_edit_text = "Target Bounce"
            elif self.line_edit_text == "Taste" or self.line_edit_text == "Blood":
                self.line_edit_text = "Taste of Blood"
            elif self.line_edit_text == "Tel" or self.line_edit_text == "Tp" or self.line_edit_text == "Tele" or self.line_edit_text == "Port":
                self.line_edit_text = "Teleport"
            elif self.line_edit_text == "Thrust" or self.line_edit_text == "Jet":
                self.line_edit_text = "Thruster"
            elif self.line_edit_text == "Time" or self.line_edit_text == "Detonation" or self.line_edit_text == "Timed":
                self.line_edit_text = "Timed Detonation"
            elif self.line_edit_text == "Toxic" or self.line_edit_text == "Cloud":
                self.line_edit_text = "Toxic Cloud"
            elif self.line_edit_text == "Trick":
                self.line_edit_text = "Trickster"
            elif self.line_edit_text == "Wind":
                self.line_edit_text = "Wind Up"
           
        self.line_edit.setText("")
        self.select_sound.play()
        if self.line_edit_text in self.data and len(self.cards_list) < 5:
            self.cards_list.append((self.line_edit_text))
            self.correct_label = self.all_labels[len(self.cards_list) - 1]
            self.correct_button = self.all_buttons[len(self.cards_list) - 1]
            self.correct_label.setPixmap(QPixmap(os.path.join(self.program_directory, f"assets/card_images2/{self.line_edit_text}")))
            self.pop_up_animation()
            self.calc()
               
    def pop_up_animation(self):
        self.correct_label.show()
        self.correct_button.show()
        
        self.pop_in_label = QPropertyAnimation(self.correct_label, b'geometry')
        self.pop_in_label.setDuration(500)
        self.pop_in_label.setStartValue(QRect(self.correct_label.x() + 100,  self.correct_label.y() + 300, 0, 0))
        self.pop_in_label.setEndValue(QRect(self.correct_label.x(), 414, 347, 481))
        self.pop_in_label.setEasingCurve(QEasingCurve.OutBounce)

        self.pop_in_label.start()

        self.pop_in_button = QPropertyAnimation(self.correct_button, b'geometry')
        self.pop_in_button.setDuration(500)
        self.pop_in_button.setStartValue(QRect(self.correct_button.x(),  self.correct_button.y(), 0, 0))
        self.pop_in_button.setEndValue(QRect(self.correct_label.x() + 41, 894, 60, 60))

        self.pop_in_button.start()

    def undo(self):
        
        button_clicked = self.sender()
        index = self.all_buttons.index(button_clicked)
        self.undo_sound.play()

        self.all_labels[index].hide()
        self.all_buttons[index].hide()

        if index < len(self.cards_list):
            del self.cards_list[index]
        self.update()

    def update(self):
         
        for i, card in enumerate(self.cards_list):
            self.all_labels[i].setPixmap(QPixmap(os.path.join(self.program_directory, f"assets/card_images2/{card}")))
            self.all_labels[i].show()
            self.all_buttons[i].show()

        for i in range(len(self.cards_list), 5):
            self.all_labels[i].hide()
            self.all_buttons[i].hide()
        
        self.line_edit.setFocus()
        self.calc()
             
    def calc(self):
        
        damage = 55.0
        bullet_dps = 54.46
        hp = 100.0
        bullet_speed = 100.0
        reload_speed = 2.33
        attack_speed = 100.0
        absolute_attack_speed = 0.35
        life_steal = 0
        bullet_slow = 0
        block_cooldown = 4.75
        bullet_bounces = 0
        aoe = 0
        max_block_damage = 0
        average_block_damage = 0
        max_empower_damage = 0
        average_empower_damage = 0

        burst_barrage_spray_counter = 0

        ammo = 3
        bullets = 1
 
        for card in self.cards_list:

            damage += damage * (self.data[card]['Damage'] / 100)
            
            hp += hp * (self.data[card]['HP'] / 100)

            bullet_speed = (100 + self.data[card]['BulletSpeed']) * bullet_speed / 100

            if card != 'Poison' and card != 'Quick Reload' and card != 'Fast Forward':
                reload_speed += self.data[card]['ReloadSpeed']
                
            if self.data[card]['AttackSpeed'] < 0:
                attack_speed = attack_speed * (1 - (self.data[card]['AttackSpeed'] / 100 / 2 / - 1))
                
            elif self.data[card]['AttackSpeed'] > 0:
                attack_speed = attack_speed * (1 + self.data[card]['AttackSpeed'] / 100)
                
            life_steal += self.data[card]['Lifesteal']

            bullet_bounces += self.data[card]['BulletBounces']

            bullets += self.data[card]['Bullets']
            if bullets < 1:
                bullets = 1

            ammo += self.data[card]['Ammo']
            if ammo < 1:
                ammo = 1

            if card == "Cold Bullets":
                bullet_slow += 70

            if card != 'Teleport' and card != 'Defender':
                block_cooldown += self.data[card]['BlockCooldown']
            
            if card == 'Spray' or card == 'Burst' or card == 'Barrage':
                burst_barrage_spray_counter += 1

        if 'Bombs Away' in self.cards_list:
            average_block_damage += (self.cards_list.count('Bombs Away') * 3 - 3 + self.data['Bombs Away']['AverageBlockDamage']) * self.cards_list.count('Bombs Away')
            max_block_damage += (self.cards_list.count('Bombs Away') * 3 - 3 + self.data['Bombs Away']['AverageBlockDamage']) * 6 * self.cards_list.count('Bombs Away')
        if 'Emp' in self.cards_list:
            average_block_damage += (-0.21675 * self.cards_list.count('Emp') ** 4 + 3.06133 * self.cards_list.count('Emp') ** 3 - 15.01175 * self.cards_list.count('Emp') ** 2 + 35.10717 * self.cards_list.count('Emp') - 17.44) * 10
            max_block_damage = average_block_damage * 3 * self.cards_list.count('Emp')
        if 'Frost Slam' in self.cards_list:
            average_block_damage += 0.7 * self.cards_list.count('Frost Slam') + 0.2
            max_block_damage += average_block_damage
        if 'Overpower' in self.cards_list:
            average_block_damage += 0.0772658 * hp ** 1.194407 * (0.3089098 + 0.6921858 * self.cards_list.count('Overpower'))
            max_block_damage += average_block_damage
        if 'Radar Shot' in self.cards_list:
            average_block_damage += damage * self.cards_list.count('Radar Shot') * 0.8
            max_block_damage += damage * self.cards_list.count('Radar Shot')
        if 'Saw' in self.cards_list:
            average_block_damage += self.data['Saw']['AverageBlockDamage']
            max_block_damage += self.data['Saw']['MaxBlockDamage']
        if 'Shockwave' in self.cards_list:
            max_block_damage = self.data['Shockwave']['MaxBlockDamage'] + 0.5  * (self.cards_list.count('Shockwave') - 1)
            average_block_damage += self.data['Shockwave']['AverageBlockDamage'] + 0.5 * (self.cards_list.count('Shockwave') - 1)
            
        if 'Silence' in self.cards_list:
            if self.cards_list.count('Silence') > 1:
                if self.cards_list.count('Silence') == 2:
                    max_block_damage += 17
                elif self.cards_list.count('Silence') == 3:
                    max_block_damage += 24
                elif self.cards_list.count('Silence') == 4:
                    max_block_damage += 30
                elif self.cards_list.count('Silence') == 5:
                    max_block_damage += 37
            else:
                max_block_damage += 10
            average_block_damage += max_block_damage / 2.5
        if 'Static Field' in self.cards_list:
            if self.cards_list.count('Static Field') > 1:
                if self.cards_list.count('Static Field') == 2:
                    max_block_damage += 118
                elif self.cards_list.count('Static Field') == 3:
                    max_block_damage += 162
                elif self.cards_list.count('Static Field') == 4:
                    max_block_damage += 208
                elif self.cards_list.count('Static Field') == 5:
                    max_block_damage += 252
            else:
                max_block_damage += 72
            average_block_damage += max_block_damage / 3
        if 'Supernova' in self.cards_list:
            if self.cards_list.count('Supernova') > 1:
                if self.cards_list.count('Supernova') == 2:
                    max_block_damage += 74
                elif self.cards_list.count('Supernova') == 3:
                    max_block_damage += 114
                elif self.cards_list.count('Supernova') == 4:
                    max_block_damage += 160
                elif self.cards_list.count('Supernova') == 5:
                    max_block_damage += 212
            else:
                max_block_damage += 40
            average_block_damage += max_block_damage * (0.75 + (0.04 * self.cards_list.count('Supernova')))

        if 'Poison' in self.cards_list or 'Quick Reload' in self.cards_list or 'Fast Forward' in self.cards_list:
            for card in self.cards_list:
                if card == 'Poison' or card == 'Quick Reload' or card  == 'Fast Forward':
                    reload_speed *= 1 - self.data[card]['ReloadSpeed'] / 100 
                    reload_speed = round(reload_speed, 2)   

        if 'Trickster' in self.cards_list:
            min_damage = damage
            min_damage = round(min_damage, 2)
            
            damage_without_trickster = 55
            for card in self.cards_list:
                if card != 'Trickster':
                    damage_without_trickster = damage_without_trickster + damage_without_trickster * (self.data[card]['Damage'] / 100)
                    
            max_damage = (6879.84556628 + 20382.15031542 * bullet_bounces + 39319.18522950 * bullet_bounces**2 - 12994.89520392 * bullet_bounces**3 + 978.54934284 * bullet_bounces**4 + self.cards_list.count('Trickster') * ( -10249.26834943 - 30535.80880626 * bullet_bounces - 58979.48617781 * bullet_bounces**2 + 19485.17613930 * bullet_bounces**3 - 1466.86568094 * bullet_bounces**4 ) + self.cards_list.count('Trickster')**2 * ( 3413.42278315 + 10184.07515760 * bullet_bounces + 19666.67594821 * bullet_bounces**2 - 6492.19760201 * bullet_bounces**3 + 488.44133809 * bullet_bounces**4 ) ) / 55 * damage_without_trickster
            max_damage = round(max_damage, 2)

        if 'Explosive Bullet' in self.cards_list or 'Timed Detonation' in self.cards_list:
            aoe = ((1.20 * damage + 19.48) - damage) * (self.cards_list.count('Explosive Bullet') + self.cards_list.count('Timed Detonation'))
            aoe = round(aoe, 2)
            damage = (1.20 * damage + 19.48) * (self.cards_list.count('Explosive Bullet') + self.cards_list.count('Timed Detonation'))
            
        if 'Teleport' in self.cards_list or 'Defender' in self.cards_list:
            for card in self.cards_list:
                if card == 'Teleport' or card == 'Defender':
                    block_cooldown *= 1 - self.data[card]['BlockCooldown'] / 100 
                    block_cooldown = round(block_cooldown, 2) 

        if 'Toxic Cloud' in self.cards_list:
            if 'Trickster' not in self.cards_list:
                if damage > 100:
                    damage = (damage * 2.72727 - (damage / 100 * 4 * damage / 600000))
                    damage += 0.25 * damage * (self.cards_list.count('Toxic Cloud') - 1)
                else: 
                    damage = damage * 2.72727 
                    damage += 0.25 * damage * (self.cards_list.count('Toxic Cloud') - 1)
            else:
                if max_damage > 100:
                    max_damage = (max_damage * 2.72727 - (max_damage / 100 * 4 * max_damage / 600000))
                    max_damage += 0.25 * max_damage * (self.cards_list.count('Toxic Cloud') - 1)
                else: 
                    max_damage = max_damage * 2.72727 
                    max_damage += 0.25 * max_damage * (self.cards_list.count('Toxic Cloud') - 1)

        if 'Trickster' not in self.cards_list:
            if damage > 55:
                damage_color = '#aacc6c'
            elif damage < 55:
                damage_color = '#f5644d'
            else:
                damage_color = 'white'
        else:
            if min_damage > 55:
                min_damage_color = '#aacc6c'
            elif min_damage < 55:
                min_damage_color = '#f5644d'
            else:
                min_damage_color = 'white'

            if max_damage > 55:
                max_damage_color = '#aacc6c'
            elif max_damage < 55:
                max_damage_color = '#f5644d'
            else:
                max_damage_color = 'white'
   
        if hp > 100:
            hp_color = '#aacc6c'
        elif hp < 100:
            hp_color = '#f5644d'
        else:
            hp_color = 'white'

        if bullet_speed > 100:
            bullet_speed_color = '#aacc6c'
        elif bullet_speed < 100:
            bullet_speed_color = '#f5644d'
        else:
            bullet_speed_color = 'white'

        if reload_speed > 2.33:
            reload_speed_color = '#f5644d'
        elif reload_speed < 2.33:
            reload_speed_color = '#aacc6c'
        else:
            reload_speed_color = 'white'

        if attack_speed > 100:
            attack_speed_color = '#aacc6c'
        elif attack_speed < 100:
            attack_speed_color = '#f5644d'
        else:
            attack_speed_color = 'white'

        if life_steal <= 0:
            life_steal_color = 'white'
        else:
            life_steal_color = '#aacc6c'

        if block_cooldown < 4.75:
            block_cooldown_color = '#aacc6c'
        elif block_cooldown > 4.75:
            block_cooldown_color = '#f5644d'
        else:
            block_cooldown_color = 'white'

        if aoe > 0:
            aoe_color = '#aacc6c'
        else:
            aoe_color = 'white'

        if average_block_damage > 0:
            average_block_damage_color = '#aacc6c'
        else:
            average_block_damage_color = 'white'

        if max_block_damage > 0:
            max_block_damage_color = '#aacc6c'
        else:
            max_block_damage_color = 'white'

        damage = round(damage, 2)
        if 'Grow' not in self.cards_list and 'Trickster' not in self.cards_list:
            damage_text = f"Damage: <span style='color:{damage_color};'>{damage}</span><br>"
        elif 'Grow' in self.cards_list and 'Trickster' not in self.cards_list:
            grow_count = self.cards_list.count('Grow')
            if grow_count == 1:
                grow_damage = 3.33
            else:   
                grow_damage = 3.33 * (grow_count * 1.5)
            damage_text = f"Damage: <span style='color:{damage_color};'>{damage}</span><span style='color:#aacc6c;'> +~ {grow_damage}%/frame at 60fps</span><br>"

        elif 'Trickster' in self.cards_list and 'Grow' not in self.cards_list:
            damage_text = f"Minimum damage: <span style='color:{min_damage_color};'>{min_damage}</span><br>Maximum damage: <span style='color:{max_damage_color};'>{max_damage}</span><br>"
        elif 'Trickster' in self.cards_list and 'Grow' in self.cards_list: 
            grow_count = self.cards_list.count('Grow')
            if grow_count == 1:
                grow_damage = 3.33
            else:   
                grow_damage = 3.33 * (grow_count * 1.5)
            damage_text = f"Minimum damage: <span style='color:{min_damage_color};'>{min_damage}</span><span style='color:#aacc6c;'> +~ {grow_damage}%/frame at 60fps</span><br>Maximum damage: <span style='color:{max_damage_color};'>{max_damage}</span><span style='color:#aacc6c;'> +~ {grow_damage}%/frame at 60fps</span><br>"

        if 'Empower' in self.cards_list and max_block_damage != 0:
            max_empower_damage = max_block_damage *  (1 + self.cards_list.count('Shield Charge'))
            average_empower_damage = average_block_damage * (1 + self.cards_list.count('Shield Charge'))
            
        if 'Shield Charge' in self.cards_list or 'Echo' in self.cards_list:
            if 'Shield Charge' in self.cards_list and 'Echo' not in self.cards_list:
                max_block_damage *= self.cards_list.count('Shield Charge') + 1
                average_block_damage *= self.cards_list.count('Shield Charge') + 1
            elif 'Echo' in self.cards_list and 'Shield Charge' not in self.cards_list:
                max_block_damage *= self.cards_list.count('Echo') + 1
                average_block_damage *= self.cards_list.count('Echo') + 1
            else: 
                max_block_damage *= 1 + (self.cards_list.count('Echo') + 1) * self.cards_list.count('Shield Charge') + (self.cards_list.count('Echo'))
                average_block_damage *= 1 + (self.cards_list.count('Echo') + 1) * self.cards_list.count('Shield Charge') + (self.cards_list.count('Echo'))
                      
        max_block_damage += max_empower_damage
        average_block_damage += average_empower_damage

        absolute_attack_speed /= attack_speed / 100
        
        how_often_i_can_shoot = math.ceil(ammo / bullets)
        
        if absolute_attack_speed < reload_speed:
            damage_loop = (absolute_attack_speed * (how_often_i_can_shoot - 1)) + reload_speed   
        else:
            damage_loop = absolute_attack_speed
        damage_loop_per_minute = 60 / damage_loop
        
        shots = bullets
        while shots < ammo:
            shots += bullets

        if burst_barrage_spray_counter < 2:
            if 'Trickster' not in self.cards_list:
                bullet_dps = damage_loop_per_minute * (damage * shots) / 60
            else:
                bullet_dps = damage_loop_per_minute * (max_damage * shots) / 60
        else: 
            if 'Trickster' not in self.cards_list:
                bullet_dps = damage_loop_per_minute * (damage * ammo) / 60
            else:
                bullet_dps = damage_loop_per_minute * (max_damage * ammo) / 60
      
        max_block_dps = 60 / (block_cooldown) * max_block_damage / 60

        max_block_dps = round(max_block_dps, 2)
        bullet_dps = round(bullet_dps, 2)
        hp = round(hp, 2)
        reload_speed = round(reload_speed, 2)
        attack_speed = round(attack_speed, 2)
        max_block_damage = round(max_block_damage, 2)
        average_block_damage = round(average_block_damage, 2)

        if bullet_dps > 54.46:
            bullet_dps_color = '#aacc6c'
        elif bullet_dps < 54.46:
            bullet_dps_color = '#f5644d'
        else:
            bullet_dps_color = 'white'

        if max_block_dps > 0:
            max_block_dps_color = '#aacc6c'
        else:
            max_block_dps_color = 'white'

        hp_text = f"Health: <span style='color:{hp_color};'>{hp}</span><br>"
        if 'Grow' not in self.cards_list:
            bullet_dps_text = f"Max bullet DPS: <span style='color:{bullet_dps_color};'>{bullet_dps}</span><br>"
        else:
            bullet_dps_text = f"Max bullet DPS: <span style='color:{bullet_dps_color};'>{bullet_dps}</span><span style='color:#aacc6c;'> +~ {grow_damage}%/frame at 60fps</span><br>"
        bullet_speed_text = f"Bullet speed: <span style='color:{bullet_speed_color};'>{bullet_speed}%</span><br>"
        reload_speed_text = f"Reload time: <span style='color:{reload_speed_color};'>{reload_speed}s</span><br>"
        if 'Demonic Pact' not in self.cards_list: 
            attack_speed_text = f"Attack speed: <span style='color:{attack_speed_color};'>{attack_speed}%</span><br>"
        else:
            attack_speed_text = f"Attack speed: <span style='color:{'#aacc6c'};'>∞</span><br>"
        life_steal_text = f"Life steal: <span style='color:{life_steal_color};'>{life_steal}%</span><br>"
        bullet_slow_text = f"Bullet slow: <span style='color:{'#aacc6c'};'>{bullet_slow}%</span><br>"
        average_block_damage_text = f"Average block damage: <span style='color:{average_block_damage_color};'>{average_block_damage}</span><br>"
        max_block_dps_text = f"Max block DPS: <span style='color:{max_block_dps_color};'>{max_block_dps}</span><br>"
        max_block_damage_text = f"Maximum block damage: <span style='color:{max_block_damage_color};'>{max_block_damage}</span><br>"
        block_cooldown_text = f"Block cooldown: <span style='color:{block_cooldown_color};'>{block_cooldown}s</span><br>"
        aoe_text = f"AoE damage: <span style='color:{aoe_color};'>~ {aoe}</span><br>"

        info_label_string = ""
        info_label_string += f"{damage_text}\n" 
        info_label_string += f"{bullet_dps_text}\n"
        if aoe != 0:
            info_label_string += f"{aoe_text}\n"
        info_label_string += f"{attack_speed_text}\n"
        info_label_string += f"{reload_speed_text}\n"
        info_label_string += f"{bullet_speed_text}\n"
        info_label_string += f"{hp_text}\n"
        info_label_string += f"{life_steal_text}\n"
        info_label_string += f"{max_block_damage_text}\n"
        if max_block_dps != 0:
            info_label_string += f"{max_block_dps_text}\n"
        info_label_string += f"{average_block_damage_text}\n"
        info_label_string += f"{block_cooldown_text}\n"
        if bullet_slow != 0:
            info_label_string += f"{bullet_slow_text}\n"

        self.my_info_label.setText(info_label_string)

    def reset(self):
        self.undo_sound.play()
        self.cards_list.clear()
        for label in self.all_labels:
            label.hide()
        for btn in self.all_buttons:
            btn.hide()
        self.calc()
        self.line_edit.setFocus()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    