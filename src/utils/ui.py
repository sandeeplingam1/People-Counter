import cv2

def draw_hud(image, num_faces, session_total=0, peak_count=0, config=None):
    """
    Draws a modern, unified HUD on the image using settings from config.
    """
    if config is None:
        # Defaults if config not provided
        hud_color = (0, 255, 255)
        text_color = (255, 255, 255)
        stats_color = (0, 255, 0)
        peak_color = (0, 0, 255)
        alpha = 0.5
    else:
        ui_cfg = config.get("ui", {})
        hud_color = tuple(ui_cfg.get("hud_color", [0, 255, 255])[::-1]) # BGR
        text_color = tuple(ui_cfg.get("text_color", [255, 255, 255])[::-1])
        stats_color = tuple(ui_cfg.get("stats_color", [0, 255, 0])[::-1])
        peak_color = tuple(ui_cfg.get("peak_color", [0, 0, 255])[::-1])
        alpha = ui_cfg.get("alpha", 0.5)

    height, width = image.shape[:2]
    
    # 1. Main Background Overlay (Right side for stats)
    overlay = image.copy()
    cv2.rectangle(overlay, (width - 250, 20), (width - 20, 150), (0, 0, 0), -1)
    
    # 2. Bottom Bar Background (Current count)
    cv2.rectangle(overlay, (20, height - 70), (350, height - 20), (0, 0, 0), -1)
    
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
    
    # --- Statistics Panel (Top Right) ---
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, "SESSION LOG", (width - 230, 45), font, 0.6, hud_color, 1, cv2.LINE_AA)
    cv2.line(image, (width - 230, 55), (width - 40, 55), hud_color, 1)
    
    cv2.putText(image, f"TOTAL: {session_total}", (width - 230, 85), font, 0.7, stats_color, 2)
    cv2.putText(image, f"PEAK:  {peak_count}", (width - 230, 125), font, 0.7, peak_color, 2)
    
    # --- Current Status (Bottom Left) ---
    font_bold = cv2.FONT_HERSHEY_DUPLEX
    text = f"ACTIVE COUNT: {num_faces}"
    cv2.putText(image, text, (30, height - 40), font_bold, 0.8, text_color, 2, cv2.LINE_AA)
    
    # Corner Accents
    cv2.line(image, (20, 20), (60, 20), hud_color, 2)
    cv2.line(image, (20, 20), (20, 60), hud_color, 2)
    
    return image
