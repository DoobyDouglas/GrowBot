def calculate_light(width: float, depth: float) -> tuple[float]:
    square = width*depth/10000
    LED_min = square*300
    LED_max = square*400
    return square, int(LED_min), int(LED_max)
