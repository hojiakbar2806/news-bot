from timezonefinder import TimezoneFinder


def get_timezone_from_coords(lat: float, lon: float) -> str:
    tf = TimezoneFinder()
    return tf.timezone_at(lat=lat, lng=lon) or "UTC"
