import cv2
import sys
import os
import time

# Add src to path if needed for local execution
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.core.detector import MultiPersonDetector
from src.audio.engine import AudioEngine
from src.utils.ui import draw_hud
from src.utils.logger import TrafficLogger
from src.utils.config_loader import load_config

def main():
    # Load configuration
    config = load_config()
    
    print("========================================")
    print("   PEOPLE COUNTER - ELITE REMASTER AI   ")
    print("========================================")
    print("1) Analyze Static Image")
    print("2) Real-time Live Analytics")
    print("3) Generate Traffic Graph")
    print("q) Quit Application")
    
    choice = input("\nSelect an option: ").strip().lower()
    
    detector = MultiPersonDetector(
        min_detection_confidence=config['detection']['min_confidence']
    )
    audio = AudioEngine()
    logger = TrafficLogger(
        log_dir=config['logging']['log_dir'],
        filename=config['logging']['filename']
    )
    
    peak_count = 0
    session_total = 0
    
    if choice == '1':
        path = input("Enter image path: ").strip()
        if not os.path.exists(path):
            print("Error: File not found.")
            return
            
        img = cv2.imread(path)
        if img is None:
            print("Error: Could not read image.")
            return
            
        processed_img, count = detector.detect(img)
        processed_img = draw_hud(processed_img, count, count, count, config=config)
        
        if config['audio']['enabled']:
            audio.speak(f"Detected {count} people.")
        
        if config['logging']['enabled']:
            logger.log_event(count, count, count)
        
        cv2.imshow("People Counter - Elite Remaster", processed_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    elif choice == '2':
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return
            
        print("Starting Elite AI engine... Press 'q' to quit.")
        last_count = -1
        last_log_time = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            processed_frame, count = detector.detect(frame)
            processed_frame = draw_hud(processed_frame, count, session_total, peak_count, config=config)
            
            # Update stats
            if count > peak_count:
                peak_count = count
                
            if count != last_count:
                if count > last_count:
                    session_total += (count - last_count)
                    if config['audio']['enabled']:
                        audio.speak(f"Count: {count}")
                last_count = count
            
            # Log data at configured interval
            if config['logging']['enabled'] and (time.time() - last_log_time > config['logging']['interval_seconds']):
                logger.log_event(session_total, count, peak_count)
                last_log_time = time.time()
                
            cv2.imshow("People Counter - Elite Remaster (Live)", processed_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                if config['logging']['enabled']:
                    logger.log_event(session_total, count, peak_count) # Final log
                break
                
        cap.release()
        cv2.destroyAllWindows()
        print(f"\nSession Summary:")
        print(f"Total People Detected: {session_total}")
        print(f"Peak Concurrent People: {peak_count}")
        if config['logging']['enabled']:
            print(f"Log saved to: {logger.get_log_path()}")
            
    elif choice == '3':
        from src.visualize import plot_traffic
        log_file = os.path.join(config['logging']['log_dir'], config['logging']['filename'])
        plot_traffic(log_file)
        
    elif choice == 'q':
        print("Exiting Elite AI interface. Goodbye!")
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()
