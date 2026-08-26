from geopy.geocoders import Nominatim
from typing import Optional , Tuple


geolocator = Nominatim(user_agent = 'medical-appointement-app')

def get_coordinates(address: str) -> Optional[Tuple[float , float]]:
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude , location.longitude
    except  Exception  as e:
        print(f"Erreur de géocodage :  {e}")
    return None
