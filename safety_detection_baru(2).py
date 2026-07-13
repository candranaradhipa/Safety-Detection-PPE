from tkinter import *
import tkinter as tk
import sys
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import math
import pygame
import threading
import time
from ultralytics import YOLO
import os

def get_base_dir():
    """Mengembalikan path ke direktori utama aplikasi"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return base_path

class APDDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Deteksi APD CCTV")
        
        # Initialize pygame for audio
        pygame.mixer.init()
        
        # Setup path resources
        self.BASE_DIR = get_base_dir()
        self.setup_paths()
        
        # Load model automatically
        try:
            self.model = YOLO(self.model_path)
            self.model_loaded = True
        except Exception as e:
            print(f"Failed to load model: {e}")
            self.model_loaded = False
        
        # Video variables
        self.cap = None
        self.video_path = None
        self.paused = False
        self.last_alarm_time = 0
        self.alarm_delay = 2  # seconds
        
        # Class names
        self.classNames = ['Gloves', 'Helmet', 'Mask', 'No-Gloves', 'No-Helmet', 
                         'No-Mask', 'No-Safety-Boots', 'No-Wearpack', 
                         'Safety-Boots', 'Wearpack']
        
        # Show welcome screen first
        self.show_welcome_screen()
        
    def setup_paths(self):
        """Mengatur path ke semua resource"""
        self.model_path = os.path.join(self.BASE_DIR, "model", "best.pt")
        self.alarm_path = os.path.join(self.BASE_DIR, "assets", "alarm.wav")
    
    def show_welcome_screen(self):
        """Menampilkan tampilan awal saat aplikasi dibuka"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container frame
        main_frame = Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Title with icon
        title_frame = Frame(main_frame)
        title_frame.pack(pady=(0, 20))
        
        # Load vest icon
        try:
            icon_path = os.path.join(self.BASE_DIR, "assets", "Safety Helmet.png")
            vest_icon = Image.open(icon_path)
            vest_icon = vest_icon.resize((40, 40), Image.LANCZOS)
            self.vest_photo = ImageTk.PhotoImage(vest_icon)
            Label(title_frame, image=self.vest_photo).pack(side=tk.LEFT, padx=10)
        except Exception as e:
            print(f"Error loading icon: {e}")
        
        Label(title_frame, text="Sistem Deteksi APD CCTV", 
            font=('Helvetica', 18, 'bold')).pack(side=tk.LEFT)
        
        # # Title
        # Label(main_frame, text="Sistem Deteksi APD CCTV", 
        #       font=('Helvetica', 18, 'bold')).pack(pady=(0, 20))
        
        # # Video placeholder
        # self.placeholder_img = Image.new('RGB', (640, 360), (240, 240, 240))
        # self.placeholder_photo = ImageTk.PhotoImage(self.placeholder_img)
        
        # video_placeholder = Label(main_frame, image=self.placeholder_photo, 
        #                         text="Video belum dimuat", compound=tk.CENTER,
        #                         font=('Helvetica', 12), fg='gray')
        # video_placeholder.pack(pady=(0, 20))
        
        # Video placeholder with framed border
        placeholder_frame = Frame(main_frame, highlightbackground="gray", 
                                highlightthickness=2, bd=0)
        placeholder_frame.pack(pady=(0, 20))
        
        self.placeholder_img = Image.new('RGB', (640, 360), (240, 240, 240))
        self.placeholder_photo = ImageTk.PhotoImage(self.placeholder_img)
        
        # Add text with border
        video_placeholder = Label(placeholder_frame, image=self.placeholder_photo, 
                                compound=tk.CENTER, bg='#F0F0F0',
                                text="Video not uploaded",
                                font=('Helvetica', 12), fg='gray',
                                borderwidth=2, relief="solid")
        video_placeholder.pack()
        
        # Button frame
        button_frame = Frame(main_frame)
        button_frame.pack()
        
        # Buttons with better styling
        button_style = {'font': ('Helvetica', 12), 'width': 15, 'padx': 10, 'pady': 5}
        
        Button(button_frame, text="Select Video", command=self.load_video, 
              **button_style).pack(side=tk.LEFT, padx=5)
        
        self.btn_start = Button(button_frame, text="Start Detection", 
                              state=tk.DISABLED, **button_style)
        self.btn_start.pack(side=tk.LEFT, padx=5)
        
        Button(button_frame, text="Exit", command=self.root.quit,
              **button_style).pack(side=tk.LEFT, padx=5)
        
        # Status bar at bottom
        self.status_bar = Label(self.root, text="Select video to start", 
                              bd=1, relief=tk.SUNKEN, anchor=tk.W, font=('Helvetica', 18, 'normal'))
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def setup_detection_ui(self):
        """Menyiapkan UI untuk mode deteksi"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Video display frame
        self.video_frame = Label(self.root)
        self.video_frame.pack(fill=tk.BOTH, expand=True)
        
        # Control panel
        control_frame = Frame(self.root)
        control_frame.pack(pady=10, fill=tk.X)
        
        # Buttons with consistent styling
        button_style = {'font': ('Helvetica', 12), 'width': 15, 'padx': 10, 'pady': 5}
        
        Button(control_frame, text="Select Video", command=self.load_video,
              **button_style).pack(side=tk.LEFT, padx=5)
        
        self.btn_start = Button(control_frame, text="Start Detection", 
                              command=self.start_detection, state=tk.NORMAL,
                              **button_style)
        self.btn_start.pack(side=tk.LEFT, padx=5)
        
        self.btn_pause = Button(control_frame, text="Pause", 
                              command=self.pause_detection, state=tk.DISABLED,
                              **button_style)
        self.btn_pause.pack(side=tk.LEFT, padx=5)
        
        Button(control_frame, text="Exit", command=self.root.quit,
              **button_style).pack(side=tk.LEFT, padx=5)
        
        # Safety status
        self.safety_status = Label(self.root, text="", font=('Helvetica', 18))
        self.safety_status.pack(pady=5, fill=tk.X)
        
        # Status bar
        model_status = "Model: Ready" if self.model_loaded else "Model: Load Failed"
        self.status_bar = Label(self.root, 
                              text=f"{model_status} | Video: {os.path.basename(self.video_path)}", 
                              bd=1, relief=tk.SUNKEN, anchor=tk.W, font=('Helvetica', 15, 'normal'))
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def load_video(self):
        self.video_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=(("Video Files", "*.mp4 *.avi *.mov *.wmv"), 
                      ("All Files", "*.*")))
        
        if self.video_path:
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                self.status_bar.config(text="Error: Open Failed")
                return
            
            # Setup GUI untuk mode deteksi
            self.setup_detection_ui()
            
            # Load first frame
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                
                self.video_frame.imgtk = imgtk
                self.video_frame.configure(image=imgtk)
                
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            video_name = os.path.basename(self.video_path)
            self.status_bar.config(text=f"Model: Ready | Video: {video_name}")
            self.btn_start.config(state=tk.NORMAL)
    
    def start_detection(self):
        if not self.model_loaded:
            self.status_bar.config(text="Error: Load Failed")
            return
            
        self.paused = False
        self.btn_start.config(state=tk.DISABLED)
        self.btn_pause.config(state=tk.NORMAL)
        
        # Reset video to beginning
        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        self.update_frame()
    
    def pause_detection(self):
        self.paused = True
        self.btn_pause.config(state=tk.DISABLED)
        self.btn_start.config(state=tk.NORMAL)
    
    def play_alert(self):
        """Memainkan suara alarm"""
        try:
            if os.path.exists(self.alarm_path):
                pygame.mixer.music.load(self.alarm_path)
                pygame.mixer.music.play()
            else:
                print(f"File alarm tidak ditemukan di: {self.alarm_path}")
        except Exception as e:
            print(f"Error memainkan alarm: {e}")
    
    def update_frame(self):
        if not self.paused and self.cap is not None and self.model_loaded:
            ret, img = self.cap.read()
            if ret:
                # Perform detection
                results = self.model(img, stream=True)
                
                # Default status
                status_text = "STATUS: SAFE"
                status_color = "green"
                box_color = (0, 255, 0)  # Green default
                
                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        
                        conf = math.ceil((box.conf[0] * 100)) / 100
                        cls = int(box.cls[0])
                        currentClass = self.classNames[cls]
                        
                        if conf > 0.1:
                            if currentClass in ['No-Wearpack', 'No-Helmet', 'No-Mask', 'No-Gloves', 'No-Safety-Boots']:
                                box_color = (0, 0, 255)  # Red
                                status_text = "STATUS: NOT SAFE"
                                status_color = "red"
                                
                                # Trigger alarm
                                if time.time() - self.last_alarm_time > self.alarm_delay:
                                    threading.Thread(target=self.play_alert, daemon=True).start()
                                    self.last_alarm_time = time.time()
                            
                            # Draw bounding box
                            cv2.rectangle(img, (x1, y1), (x2, y2), box_color, 2)
                            cv2.putText(img, f'{currentClass} {conf:.2f}', 
                                       (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 
                                       0.6, (255,255,255), 1)
                
                # Update status display
                self.safety_status.config(text=status_text, fg=status_color)
                
                # Convert to Tkinter format
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=img)
                
                self.video_frame.imgtk = imgtk
                self.video_frame.configure(image=imgtk)
                
                # Schedule next frame update
                self.root.after(30, self.update_frame)
            else:
                self.cap.release()
                self.status_bar.config(text="Finish Detect")

if __name__ == "__main__":
    root = Tk()
    app = APDDetectorApp(root)
    root.mainloop()