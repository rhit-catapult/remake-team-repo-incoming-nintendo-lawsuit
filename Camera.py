#chatgpt
def scroll_camera(target_rect, screen_width, screen_height, map_width, map_height):
     camera_x = target_rect.centerx - screen_width // 2
     camera_y = target_rect.centery - screen_height // 2

    # Clamp to map bounds
     camera_x = max(0, min(camera_x, map_width - screen_width))
     camera_y = max(0, min(camera_y, map_height - screen_height))

     return camera_x, camera_y