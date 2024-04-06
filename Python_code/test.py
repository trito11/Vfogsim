from pyproj import Proj
from math import radians, cos, sin, asin, sqrt
def latlon_to_utm_zone(lat, lon):
    # Xác định zone number và zone letter cho tọa độ latitude và longitude
    zone_number = int((lon + 180) / 6) + 1
    zone_letter = 'CDEFGHJKLMNPQRSTUVWXX'[int((lat + 80) / 8)]

    # Khởi tạo một đối tượng Proj cho hệ thống toạ độ UTM
    utm_proj = Proj(proj='utm', zone=zone_number, ellps='WGS84', datum='WGS84', zone_letter=zone_letter)

    # Chuyển đổi tọa độ latitude và longitude sang UTM
    easting, northing = utm_proj(lon, lat)

    return zone_number, zone_letter

# Tọa độ latitude và longitude của điểm cụ thể
lat, lon = 60.17, 24.9323

# Xác định zone number và zone letter từ tọa độ latitude và longitude
zone_number, zone_letter = latlon_to_utm_zone(lat, lon)
print("Zone number:", zone_number)
print("Zone letter:", zone_letter)

from geopy.distance import geodesic
from pyproj import Proj, transform
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    # haversine formula 
    dlat = lat2 - lat1
    dlon = lon2 - lon1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371 * c
    # Convert kilometers to meters
    
    return km
def utm_to_latlon(easting, northing, zone_number, zone_letter):
    p1 = Proj(proj='utm', zone=zone_number, ellps='WGS84', datum='WGS84')
    lon, lat = p1(easting, northing, inverse=True)
    return lat, lon

def distance_between_points(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers

# Example coordinates
utm1 = (386112, 6671780, 35, 'V')
utm2 = (386112, 6671771, 35, 'V')

# Convert UTM to latitude and longitude
lat1, lon1 = utm_to_latlon(*utm1)
lat2, lon2 = utm_to_latlon(*utm2)
print(lat1, lon1)
print(lat2, lon2)
print(haversine(lat1, lon1, lat2, lon2)*1000)