import time
import numpy as np
import pandas as pd
import folium
import streamlit as st
import seaborn as sns
from collections import defaultdict
from matplotlib import pyplot as plt
from typing import Dict, List, Tuple
from models.location import Location
from utils.map import find_path, compute_distance
import time as tm
from typing import List, Dict, Tuple


# Get list of Vehicles
selected_vehicle = st.selectbox("Pilih Kendaraan", 
                              ["Mobil Box", "Truk Sedang", "Truk Besar"],
                              format_func=lambda x: x)

# Read location data
locations_data = pd.read_csv('kecamatan_sby.csv')
locations = [Location(row['Name'], row['Latitude'], row['Longitude']) for _, row in locations_data.iterrows()]

# Create a map centered at Surabaya
map_surabaya = folium.Map(location=[-7.25, 112.75], zoom_start=12)

# Get list of locations
start_location = st.selectbox("Pilih lokasi start", locations, format_func=lambda location: location.name)
end_location = st.selectbox("Pilih lokasi end", locations, format_func=lambda location: location.name)

# if st.button('Submit', use_container_width=True):
# Get distance and map path
kedalaman_maks = 25  
path_dict = find_path('kecamatan_sby.csv', start_location.name, end_location.name, kedalaman_maks)
distance = None

if path_dict:
    nodes = list(path_dict.keys())

    start_node = nodes[0]  
    end_node = nodes[-1]  

    start_coords = (path_dict[start_node]['Longitude'], path_dict[start_node]['Latitude'])
    end_coords = (path_dict[end_node]['Longitude'], path_dict[end_node]['Latitude'])

    folium.Marker(location=start_coords, popup=f"Start: {start_node}", icon=folium.Icon(color='green')).add_to(map_surabaya)
    folium.Marker(location=end_coords, popup=f"End: {end_node}", icon=folium.Icon(color='red')).add_to(map_surabaya)

    for node in nodes[1:-1]: 
        koordinat = (path_dict[node]['Longitude'], path_dict[node]['Latitude'])
        folium.Marker(location=koordinat, popup=f"Node: {node}", icon=folium.Icon(color='blue')).add_to(map_surabaya)

    for i in range(len(nodes) - 1):
        node_awal = nodes[i]
        node_akhir = nodes[i + 1]
        koordinat_awal = (path_dict[node_awal]['Longitude'], path_dict[node_awal]['Latitude'])
        koordinat_akhir = (path_dict[node_akhir]['Longitude'], path_dict[node_akhir]['Latitude'])

        folium.PolyLine(locations=[koordinat_awal, koordinat_akhir], color='blue', weight=5).add_to(map_surabaya)

    distance = compute_distance(start_coords, end_coords)

# Display map
with st.container(border=True):
    if path_dict:
        st.write(f"Jarak antara {start_location.name} dan {end_location.name} adalah {distance:.2f} km")
    else:
        st.write(f"Tidak ditemukan jalur dari {start_location.name} ke {end_location.name}")
    map_html = map_surabaya._repr_html_()
    st.components.v1.html(map_html, height=400)

# Data minuman (20 items)
items_minuman = [
    {"nama": "Red Bull Energy Drink, 8.4 Fl Oz", "dimension": "4.25 x 12.50 x 5.50", "priority": 7},
    {"nama": "V8 +ENERGY Orange Pineapple Energy Drink", "dimension": "4.25 x 6.33 x 5.17", "priority": 7},
    {"nama": "Starbucks Tripleshot Energy Mocha", "dimension": "2.08 x 2.08 x 4.5", "priority": 7},
    {"nama": "ZOA Energy Drink Pineapple Coconut", "dimension": "2.30 x 2.30 x 6.20", "priority": 7},
    {"nama": "vitaminwater xxx electrolyte", "dimension": "12 x 9.13 x 8.37", "priority": 7},
    {"nama": "neuroSONIC Superfruit Infusion", "dimension": "3.00 x 3.00 x 8.00", "priority": 8},
    {"nama": "Suja Organic Vitamin D and Zinc Shot", "dimension": "1.00 x 1.00 x 3.00", "priority": 9},
    {"nama": "MiO Vitamins Orange Tangerine", "dimension": "1.58 x 2.65 x 4.15", "priority": 9},
    {"nama": "Core Power Protein Shake Chocolate", "dimension": "2.64 x 2.64 x 7.06", "priority": 10},
    {"nama": "Premier Protein Shake Chocolate", "dimension": "4.00 x 4.00 x 4.00", "priority": 10},
    {"nama": "Great Value 2% Reduced Fat Milk", "dimension": "6.00 x 6.00 x 10.00", "priority": 8},
    {"nama": "Horizon Organic Growing Years Milk", "dimension": "3.88 x 3.88 x 9.27", "priority": 8},
    {"nama": "Horizon Organic Chocolate Milk", "dimension": "8.25 x 6.44 x 5.19", "priority": 8},
    {"nama": "fairlife Lactose Free 2% Milk", "dimension": "4.01 x 4.01 x 10.05", "priority": 8},
    {"nama": "Great Value Chocolate Milk", "dimension": "4.00 x 4.00 x 10.00", "priority": 8},
    {"nama": "Celestial Seasonings Peppermint Tea", "dimension": "2.50 x 5.50 x 3.12", "priority": 7},
    {"nama": "Bigelow Green Tea Classic", "dimension": "2.66 x 5.18 x 3.11", "priority": 7},
    {"nama": "Yogi Tea Green Tea Blueberry", "dimension": "2.69 x 3.06 x 4.31", "priority": 7},
    {"nama": "TAZO Matcha Latte Green Tea", "dimension": "3.80 x 2.40 x 7.70", "priority": 7},
    {"nama": "Jade Leaf Matcha Organic", "dimension": "1.00 x 1.00 x 1.00", "priority": 7}
]

# Data makanan (20 items)
items_makanan = [
    {"nama": "Indomie 5-pack", "dimension": "4.35 x 7.65 x 5.28", "priority": 10},
    {"nama": "Wonder Classic White Bread", "dimension": "4.50 x 4.25 x 14.50", "priority": 7},
    {"nama": "California Girl Sardines in Tomato Sauce", "dimension": "2.15 x 2.15 x 3.46", "priority": 9},
    {"nama": "Libby's Corned Beef", "dimension": "2.50 x 3.25 x 3.62", "priority": 9},
    {"nama": "SPAM Classic", "dimension": "2.20 x 4.00 x 3.30", "priority": 9},
    {"nama": "Great Value White Rice", "dimension": "4.50 x 2.50 x 7.25", "priority": 8},
    {"nama": "Quaker Oats Old Fashioned", "dimension": "7.12 x 4.75 x 10.75", "priority": 8},
    {"nama": "Campbell's Chicken Noodle Soup", "dimension": "3.00 x 3.00 x 4.40", "priority": 8},
    {"nama": "Prego Traditional Italian Sauce", "dimension": "3.50 x 3.50 x 7.00", "priority": 8},
    {"nama": "Cheerios Original Cereal", "dimension": "7.50 x 2.25 x 10.75", "priority": 7},
    {"nama": "Nature Valley Crunchy Granola Bars", "dimension": "7.62 x 1.75 x 5.75", "priority": 7},
    {"nama": "Skippy Creamy Peanut Butter", "dimension": "3.50 x 3.50 x 5.50", "priority": 8},
    {"nama": "Jif Natural Peanut Butter", "dimension": "3.50 x 3.50 x 5.50", "priority": 8},
    {"nama": "Nutella Chocolate Hazelnut Spread", "dimension": "3.25 x 3.25 x 4.75", "priority": 8},
    {"nama": "Kraft Mac & Cheese Original", "dimension": "7.25 x 1.75 x 5.75", "priority": 8},
    {"nama": "Barilla Spaghetti", "dimension": "10.75 x 1.25 x 3.75", "priority": 8},
    {"nama": "Rice Krispies Treats", "dimension": "8.00 x 2.75 x 10.75", "priority": 7},
    {"nama": "Oreo Original Cookies", "dimension": "7.75 x 2.00 x 10.25", "priority": 7},
    {"nama": "Ritz Original Crackers", "dimension": "7.50 x 2.25 x 10.75", "priority": 7},
    {"nama": "Doritos Nacho Cheese", "dimension": "10.75 x 3.00 x 15.00", "priority": 7}
]

# Data obat (20 items)
items_obat = [
    {"nama": "Advil Ibuprofen Tablets", "dimension": "2.00 x 4.00 x 5.50", "priority": 9},
    {"nama": "Tylenol Extra Strength", "dimension": "2.25 x 4.25 x 5.75", "priority": 9},
    {"nama": "Aleve Pain Reliever", "dimension": "2.50 x 4.50 x 6.00", "priority": 9},
    {"nama": "Bayer Aspirin", "dimension": "2.00 x 3.75 x 5.25", "priority": 9},
    {"nama": "Mucinex DM Expectorant", "dimension": "2.75 x 4.75 x 6.25", "priority": 9},
    {"nama": "Vicks NyQuil Cold & Flu", "dimension": "3.00 x 5.00 x 6.50", "priority": 8},
    {"nama": "Zyrtec Allergy Relief", "dimension": "2.25 x 4.25 x 5.75", "priority": 8},
    {"nama": "Claritin 24 Hour Allergy", "dimension": "2.50 x 4.50 x 6.00", "priority": 8},
    {"nama": "Benadryl Allergy Relief", "dimension": "2.75 x 4.75 x 6.25", "priority": 8},
    {"nama": "Pepto Bismol Original", "dimension": "3.00 x 5.00 x 6.50", "priority": 8},
    {"nama": "Tums Ultra Strength", "dimension": "2.25 x 4.25 x 5.75", "priority": 8},
    {"nama": "Robitussin Cough + Chest", "dimension": "2.50 x 4.50 x 6.00", "priority": 8},
    {"nama": "Dayquil Cold & Flu Relief", "dimension": "2.75 x 4.75 x 6.25", "priority": 8},
    {"nama": "Sudafed PE Sinus Pressure", "dimension": "2.00 x 4.00 x 5.50", "priority": 8},
    {"nama": "Excedrin Migraine Relief", "dimension": "2.25 x 4.25 x 5.75", "priority": 9},
    {"nama": "Motrin IB Pain Reliever", "dimension": "2.50 x 4.50 x 6.00", "priority": 9},
    {"nama": "Neosporin Original Ointment", "dimension": "1.00 x 2.00 x 4.00", "priority": 7},
    {"nama": "Band-Aid Flexible Fabric", "dimension": "3.75 x 0.75 x 5.25", "priority": 7},
    {"nama": "Preparation H Cream", "dimension": "1.50 x 2.50 x 4.50", "priority": 7},
    {"nama": "Centrum Adult Multivitamin", "dimension": "2.75 x 4.75 x 6.25", "priority": 7}
]

def calculate_volume(dimension_str: str) -> float:
    """
    Konversi dimensi string 'p x l x t' menjadi volume (m³)
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    try:
        p, l, t = map(float, dimension_str.split(' x '))
        volume = (p * l * t) / 1000000  # konversi ke m³
        return volume
    except:
        return None

def process_items(items_list: List[Dict], category: str) -> List[Dict]:
    """
    Memproses data items dan menambahkan volume
    Time Complexity: O(n) dimana n adalah jumlah items
    Space Complexity: O(n)
    """
    processed_items = []
    for item in items_list:
        volume = calculate_volume(item['dimension'])
        if volume:
            processed_item = {
                'nama': item['nama'],
                'volume': volume,
                'priority': item['priority'],
                'category': category  # Menambahkan kategori sesuai jenis item
            }
            processed_items.append(processed_item)
    return processed_items

# Proses semua items dengan kategori yang sesuai
minuman_processed = process_items(items_minuman, 'minuman')
makanan_processed = process_items(items_makanan, 'makanan')
obat_processed = process_items(items_obat, 'obat')

class PackageUnit:
    """Class untuk standardisasi packaging dengan batasan praktis"""
    def __init__(self, name: str, length: float, width: float, height: float):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.volume = self.calculate_volume()
        self.max_weight = self._set_weight_limit()
        self.practical_limits = self._set_practical_limits()
        self.handling_space = 0.3  # 30% untuk handling

    def calculate_volume(self) -> float:
        return self.length * self.width * self.height

    def _set_weight_limit(self) -> float:
        """Batas berat maksimum per package"""
        weight_limits = {
            "Small Box": 10,     # 10 kg
            "Medium Box": 20,    # 20 kg
            "Large Box": 30,     # 30 kg
            "Pallet": 1000       # 1 ton
        }
        return weight_limits.get(self.name, 10)

    def _set_practical_limits(self) -> Dict[str, Dict[str, int]]:
        """Batasan praktis jumlah item per kategori"""
        return {
            "Small Box": {
                "minuman": 12,     # 12 botol kecil
                "makanan": 24,     # 24 pack makanan
                "obat": 50         # 50 unit obat
            },
            "Medium Box": {
                "minuman": 24,     # 24 botol
                "makanan": 40,     # 40 pack
                "obat": 100        # 100 unit
            },
            "Large Box": {
                "minuman": 48,     # 48 botol
                "makanan": 80,     # 80 pack
                "obat": 200        # 200 unit
            }
        }.get(self.name, {})

    def check_item_fit(self, item: Dict) -> Tuple[bool, int, Dict[str, float]]:
        """
        Mengecek kapasitas dengan pertimbangan praktis
        Returns: (can_fit, max_quantity, metrics)
        """
        if item['volume'] > self.volume:
            return False, 0, {}

        # Hitung kapasitas berdasarkan volume dengan handling space
        usable_volume = self.volume * (1 - self.handling_space)
        volume_based_qty = int(usable_volume / item['volume'])

        # Ambil batasan praktis berdasarkan kategori
        practical_limit = self.practical_limits.get(item['category'], 0)

        # Tentukan quantity final (minimum dari semua batasan)
        final_qty = min(volume_based_qty, practical_limit)

        # Hitung metrik
        metrics = {
            'volume_efficiency': (final_qty * item['volume'] / self.volume) * 100,
            'weight_capacity': min(100, (final_qty * 0.5 / self.max_weight) * 100),  # Asumsi 0.5kg per item
            'practical_usage': (final_qty / practical_limit) * 100 if practical_limit > 0 else 0
        }

        return True, final_qty, metrics

# Inisialisasi package standar dengan ukuran realistis
standard_packages = {
    "Small Box": PackageUnit("Small Box", 0.3, 0.4, 0.3),
    "Medium Box": PackageUnit("Medium Box", 0.4, 0.6, 0.4),
    "Large Box": PackageUnit("Large Box", 0.6, 0.8, 0.6),
    "Pallet": PackageUnit("Pallet", 1.0, 1.2, 1.0)
}

def analyze_realistic_packaging():
    """Analisis packaging dengan pertimbangan praktis"""
    c = st.container(border=True, height=100, scrolling=True)
    c.text("\n=== Analisis Packaging Realistis ===")

    categories = {
        'minuman': minuman_processed,
        'makanan': makanan_processed,
        'obat': obat_processed
    }

    for category_name, items in categories.items():
        c.text(f"\nKategori: {category_name.upper()}")

        for item in items:
            c.text(f"\nItem: {item['nama']}")
            c.text(f"Volume: {item['volume']:.6f} m³")
            c.text(f"Priority: {item['priority']}")

            for package_name, package in standard_packages.items():
                can_fit, qty, metrics = package.check_item_fit(item)
                if can_fit and qty > 0:
                    c.text(f"\n{package_name}:")
                    c.text(f"- Quantity Praktis: {qty} unit")
                    c.text(f"- Efisiensi Volume: {metrics['volume_efficiency']:.1f}%")
                    c.text(f"- Kapasitas Berat: {metrics['weight_capacity']:.1f}%")
                    c.text(f"- Penggunaan Praktis: {metrics['practical_usage']:.1f}%")
                else:
                    c.text(f"\n{package_name}: Tidak sesuai untuk item ini")
                    
def create_vehicles():
    """
    Membuat dictionary kendaraan dengan spesifikasi dasar
    Format: {nama: [kapasitas_m3, efisiensi_bbm, handling_space]}
    """
    return {
        "Mobil Box": [10, 10, 0.3],      # 10 m³, 10 km/L, 30% space handling
        "Truk Sedang": [30, 6, 0.3],     # 30 m³, 6 km/L
        "Truk Besar": [70, 4, 0.3]       # 70 m³, 4 km/L
    }

def get_vehicle_capacity(vehicle_specs):
    """Menghitung kapasitas praktis kendaraan"""
    max_capacity, _, handling_space = vehicle_specs
    return max_capacity * (1 - handling_space)

def check_vehicle_load(current_load, item_volume, quantity, max_load):
    """
    Mengecek apakah barang bisa dimuat
    Returns: (bisa_dimuat, alasan)
    """
    needed_space = item_volume * quantity
    if current_load + needed_space <= max_load:
        return True, "OK"
    return False, "Volume melebihi kapasitas"

def calculate_shipping_cost(distance, load_volume, vehicle_specs):
    """
    Menghitung biaya pengiriman
    Parameters:
        distance: jarak dalam km
        load_volume: volume muatan dalam m³
        vehicle_specs: [kapasitas, efisiensi_bbm, handling_space]
    """
    max_capacity, fuel_efficiency, _ = vehicle_specs

    # Hitung konsumsi BBM
    fuel_consumption = distance / fuel_efficiency
    fuel_cost = fuel_consumption * 14500

    # Hitung faktor beban
    load_factor = 1 + (load_volume / max_capacity * 0.2)
    total_cost = fuel_cost * load_factor
    utilization = (load_volume / max_capacity) * 100

    return {
        'fuel_cost': fuel_cost,
        'utilization': utilization,
        'total_cost': total_cost
    }
    
class BoxType:
    """Definisi tipe box dan kapasitasnya"""
    SMALL = {"name": "Small Box", "volume": 0.036, "capacity": 12}
    MEDIUM = {"name": "Medium Box", "volume": 0.096, "capacity": 24}
    LARGE = {"name": "Large Box", "volume": 0.288, "capacity": 48}

def calculate_value_density(item: Dict) -> float:
    """
    Menghitung value density untuk sorting items
    Value density = priority/volume (makin tinggi makin baik)
    """
    return item['priority'] / item['volume']

def calculate_category_capacity(vehicle_capacity: float, percentages: Dict[str, float]) -> Dict[str, float]:
    """
    Menghitung kapasitas volume untuk setiap kategori
    Args:
        vehicle_capacity: Kapasitas total kendaraan
        percentages: Persentase alokasi per kategori
    Returns:
        Dictionary kapasitas volume per kategori
    """
    return {
        category: vehicle_capacity * percentage
        for category, percentage in percentages.items()
    }

def find_optimal_box_combination(item_volume: float, category_volume: float) -> List[Dict]:
    """
    Menentukan kombinasi box optimal untuk item
    Menggunakan pendekatan greedy untuk memaksimalkan penggunaan box besar
    """
    boxes = []
    remaining_volume = category_volume
    box_types = [BoxType.LARGE, BoxType.MEDIUM, BoxType.SMALL]

    for box_type in box_types:
        while remaining_volume >= box_type['volume']:
            potential_boxes = min(
                3,  # Maksimal 3 box per tipe
                int(remaining_volume / box_type['volume'])
            )
            if potential_boxes > 0:
                boxes.append({
                    'type': box_type['name'],
                    'count': potential_boxes,
                    'volume': box_type['volume'],
                    'capacity': box_type['capacity']
                })
                remaining_volume -= potential_boxes * box_type['volume']

    return boxes

def greedy_optimizer(items: List[Dict], vehicle_specs: List, max_capacity: float) -> Dict:
    """
    Implementasi algoritma Greedy untuk optimasi loading dengan multiple box sizes
    """
    start_time = time.time_ns()

    # Definisi persentase kategori
    category_percentages = {
        'makanan': 0.4,    # 40% kapasitas
        'minuman': 0.3,    # 30% kapasitas
        'obat': 0.3        # 30% kapasitas
    }

    # Hitung kapasitas per kategori
    category_capacities = calculate_category_capacity(
        max_capacity,
        category_percentages
    )

    # Initialize struktur data
    categorized_items = {cat: [] for cat in category_percentages.keys()}
    selected_items = {cat: [] for cat in category_percentages.keys()}
    remaining_capacity = category_capacities.copy()

    # Kategorisasi items
    for item in items:
        if item['category'] in categorized_items:
            categorized_items[item['category']].append(item)

    # Sort items berdasarkan value density
    for category in categorized_items:
        categorized_items[category].sort(
            key=calculate_value_density,
            reverse=True
        )

    # Proses seleksi untuk setiap kategori
    for category, items_list in categorized_items.items():
        remaining_volume = category_capacities[category]
        max_item_volume = remaining_volume * 0.3  # Maksimal 30% per item
        min_items_variety = min(5, len(items_list))  # Minimal 3-5 item berbeda

        for idx, item in enumerate(items_list):
            if idx >= min_items_variety:
                break

            # Alokasikan volume untuk item ini
            allocated_volume = min(
                max_item_volume,
                remaining_volume / (min_items_variety - idx)
            )

            # Hitung kombinasi box optimal
            boxes = find_optimal_box_combination(
                item['volume'],
                allocated_volume
            )

            if boxes:
                selected_items[category].append({
                    'item': item,
                    'boxes': boxes,
                    'total_volume': sum(box['volume'] * box['count']
                                      for box in boxes),
                    'total_quantity': sum(box['capacity'] * box['count']
                                        for box in boxes)
                })

                remaining_volume -= allocated_volume
                remaining_capacity[category] -= allocated_volume  # Perbarui remaining_capacity

    # Hitung metrics
    total_volume = sum(
        sum(item['total_volume'] for item in cat_items)
        for cat_items in selected_items.values()
    )

    total_value = sum(
        sum(item['item']['priority'] * item['total_quantity']
            for item in cat_items)
        for cat_items in selected_items.values()
    )

    category_metrics = {
        category: {
            'volume_used': category_capacities[category] - remaining_capacity[category],
            'utilization': ((category_capacities[category] - remaining_capacity[category])
                          / category_capacities[category] * 100)
        }
        for category in selected_items.keys()
    }

    return {
        'selected_items': selected_items,
        'total_volume': total_volume,
        'total_value': total_value,
        'execution_time': float(time.time_ns() - start_time) / 1e6,  # in milliseconds
        'utilization': (total_volume/max_capacity) * 100,
        'category_metrics': category_metrics
    }
def print_optimization_results(result: Dict):
    """Menampilkan hasil optimasi dalam format yang mudah dibaca"""
    label = "Hasil Optimasi Greedy"
    c = st.expander(label)
    c.text("\n=== Hasil Optimasi Greedy ===")
    c.text(f"Total Volume: {result['total_volume']:.2f} m³")
    c.text(f"Total Value: {result['total_value']}")
    c.text(f"Overall Utilization: {result['utilization']:.1f}%")

    c.text("\nUtilisasi per Kategori:")
    for category, metrics in result['category_metrics'].items():
        c.text(f"\n{category.upper()}:")
        c.text(f"Volume Used: {metrics['volume_used']:.2f} m³")
        c.text(f"Utilization: {metrics['utilization']:.1f}%")

        c.text("\nSelected Items:")
        for item_alloc in result['selected_items'][category]:
            c.text(f"\n- {item_alloc['item']['nama']}")
            c.text(f"  Total Quantity: {item_alloc['total_quantity']} units")
            for box in item_alloc['boxes']:
                c.text(f"  {box['type']}: {box['count']} box(es) "
                      f"({box['capacity']} units each)")

# Modifikasi fungsi test_greedy_optimization()
def test_greedy_optimization(selected_vehicle):
    """Testing optimasi untuk kendaraan yang dipilih"""
    vehicles = create_vehicles()
    optimized_items = {}
    c = st.container(border=True)

    # Hanya proses kendaraan yang dipilih
    specs = vehicles[selected_vehicle]
    c.text(f"\n{'='*20} Optimasi untuk {selected_vehicle} {'='*20}")

    # Hitung kapasitas praktis
    max_capacity = get_vehicle_capacity(specs)
    c.text(f"Kapasitas Praktis: {max_capacity:.2f} m³")

    # Gabungkan semua items dengan kategori yang benar
    all_items = (
        [dict(item, category='makanan') for item in makanan_processed] +
        [dict(item, category='minuman') for item in minuman_processed] +
        [dict(item, category='obat') for item in obat_processed]
    )

    # Jalankan optimasi
    result = greedy_optimizer(all_items, specs, max_capacity)
    print_optimization_results(result)
    optimized_items[selected_vehicle] = result

    return optimized_items

# Modifikasi fungsi test_vehicle_system()
def test_vehicle_system(optimized_items, vehicle_specs, start_location, end_location):
    """Function untuk testing sistem dengan data optimasi"""
    label = "Hasil Analisis Untuk Kendaraan Yang Dipilih"
    c = st.expander(label)
    
    # Header untuk kendaraan yang dipilih
    vehicle_name = list(optimized_items.keys())[0]  # Karena hanya ada satu kendaraan
    result = optimized_items[vehicle_name]
    
    c.text("\n================================================================================")
    c.text(f"ANALYSIS FOR {vehicle_name}")
    c.text("================================================================================\n")

    # Data untuk kendaraan yang dipilih
    total_volume = result['total_volume']
    utilization = (total_volume / get_vehicle_capacity(vehicle_specs[vehicle_name])) * 100
    total_value = result['total_value']
    
    c.text(f"Total Volume: {total_volume:,.2f} m³")
    c.text(f"Utilization: {utilization:,.1f}%")
    c.text(f"Total Value: {total_value:,.1f}")

    # Category Distribution Analysis
    c.text(f"\n{'='*40}")
    c.text("CATEGORY DISTRIBUTION ANALYSIS")
    c.text(f"{'='*40}\n")

    for category, data in result['selected_items'].items():
        total_qty = sum(item_alloc['total_quantity'] for item_alloc in data)

        c.text(f"{category.upper()}:")
        c.text(f"- Different Products: {len(data)}")
        c.text(f"- Total Quantity: {total_qty}")
        c.text(f"- Volume Used: {result['category_metrics'][category]['volume_used']:.2f} m³")
        c.text(f"- Utilization: {result['category_metrics'][category]['utilization']:.1f}%")

    # Shipping Cost Analysis
    c.text("\n================================================================================")
    c.text("SHIPPING COST ANALYSIS")
    c.text("================================================================================")

    distance = start_location.calculate_distance(end_location)
    c.text(f"\nJarak antara {start_location.name} dan {end_location.name}: {distance:.2f} km")

    specs = vehicle_specs[vehicle_name]
    total_volume = result['total_volume']
    max_load = get_vehicle_capacity(specs)

    c.text(f"\nKapasitas Maksimum: {specs[0]} m³")
    c.text(f"Kapasitas Praktis: {max_load:.2f} m³")
    c.text(f"Volume Terpakai: {total_volume:.2f} m³")
    c.text(f"Utilization: {(total_volume/max_load)*100:.1f}%")

    costs = calculate_shipping_cost(distance, total_volume, specs)

    c.text(f"\nBiaya Transportasi:")
    c.text(f"- Biaya BBM: Rp {costs['fuel_cost']:,.2f}")
    c.text(f"- Total Biaya: Rp {costs['total_cost']:,.2f}")

# Modifikasi pemanggilan fungsi
optimized_items = test_greedy_optimization(selected_vehicle)
vehicles = create_vehicles()
test_vehicle_system(optimized_items, vehicles, start_location, end_location)


class BoxType:
    """Box type definitions and capacities"""
    SMALL = {"name": "Small Box", "volume": 0.036, "capacity": 12}
    MEDIUM = {"name": "Medium Box", "volume": 0.096, "capacity": 24}
    LARGE = {"name": "Large Box", "volume": 0.288, "capacity": 48}

class KnapsackOptimizer:
    def __init__(self):
        self.memo = {}

    def _get_box_bounds(self, item_volume: float, remaining_capacity: float) -> Dict[str, int]:
        """Calculate maximum number of boxes possible for each type"""
        return {
            'small': min(3, int(remaining_capacity / BoxType.SMALL['volume'])),
            'medium': min(3, int(remaining_capacity / BoxType.MEDIUM['volume'])),
            'large': min(3, int(remaining_capacity / BoxType.LARGE['volume']))
        }

    def _solve_bounded_knapsack(self,
                                items: List[Dict],
                                capacity: float,
                                memo_key: str = '') -> Tuple[float, List[Dict]]:
        """Core bounded knapsack algorithm using dynamic programming"""
        if memo_key in self.memo:
            return self.memo[memo_key]

        if not items or capacity <= 0:
            return 0.0, []

        current_item = items[0]
        remaining_items = items[1:]
        box_bounds = self._get_box_bounds(current_item['volume'], capacity)

        best_value = 0.0
        best_selection = []

        for large_count in range(box_bounds['large'] + 1):
            for medium_count in range(box_bounds['medium'] + 1):
                for small_count in range(box_bounds['small'] + 1):
                    total_volume = (
                        large_count * BoxType.LARGE['volume'] +
                        medium_count * BoxType.MEDIUM['volume'] +
                        small_count * BoxType.SMALL['volume']
                    )

                    if total_volume > capacity:
                        continue

                    total_quantity = (
                        large_count * BoxType.LARGE['capacity'] +
                        medium_count * BoxType.MEDIUM['capacity'] +
                        small_count * BoxType.SMALL['capacity']
                    )

                    current_value = total_quantity * current_item['priority']

                    new_memo_key = f"{','.join([str(i['id']) for i in remaining_items])}_{capacity-total_volume}"
                    remaining_value, remaining_selection = self._solve_bounded_knapsack(
                        remaining_items,
                        capacity - total_volume,
                        new_memo_key
                    )

                    total_value = current_value + remaining_value

                    if total_value > best_value:
                        best_value = total_value
                        boxes = []
                        if large_count > 0:
                            boxes.append({
                                'type': BoxType.LARGE['name'],
                                'count': large_count,
                                'capacity': BoxType.LARGE['capacity']
                            })
                        if medium_count > 0:
                            boxes.append({
                                'type': BoxType.MEDIUM['name'],
                                'count': medium_count,
                                'capacity': BoxType.MEDIUM['capacity']
                            })
                        if small_count > 0:
                            boxes.append({
                                'type': BoxType.SMALL['name'],
                                'count': small_count,
                                'capacity': BoxType.SMALL['capacity']
                            })

                        best_selection = [{
                            'item': current_item,
                            'quantity': total_quantity,
                            'boxes': boxes,
                            'volume': total_volume
                        }] + remaining_selection

        self.memo[memo_key] = (best_value, best_selection)
        return best_value, best_selection

    def optimize_category(self,
                         items: List[Dict],
                         capacity: float,
                         min_items: int = 3,
                         max_items: int = 8) -> Tuple[List[Dict], float]:
        """Optimize single category using bounded knapsack"""
        self.memo = {}

        sorted_items = sorted(
            items,
            key=lambda x: (x['priority'] / x['volume']),
            reverse=True
        )

        # Add unique IDs for memoization
        for idx, item in enumerate(sorted_items):
            item['id'] = idx

        # Adjust parameters based on capacity
        if capacity >= 15.0:  # Truk Besar
            max_items = 12
            efficiency_factor = 0.97
        elif capacity >= 6.0:  # Truk Sedang
            max_items = 10
            efficiency_factor = 0.92
        else:  # Mobil Box
            max_items = 8
            efficiency_factor = 0.90

        # Limit items for optimization
        sorted_items = sorted_items[:max_items]

        # Calculate effective capacity with efficiency factor
        effective_capacity = capacity * efficiency_factor

        memo_key = f"{','.join([str(i['id']) for i in sorted_items])}_{effective_capacity}"
        _, selected = self._solve_bounded_knapsack(sorted_items, effective_capacity, memo_key)

        return selected, capacity - sum(item['volume'] for item in selected)

    def optimize(self,
                items: List[Dict],
                vehicle_specs: List,
                max_capacity: float) -> Dict:
        """Main optimization function for all categories"""
        start_time = tm.time()

        category_percentages = {
            'makanan': 0.4,
            'minuman': 0.3,
            'obat': 0.3
        }

        category_capacities = {
            cat: max_capacity * pct
            for cat, pct in category_percentages.items()
        }

        # Group items by category
        categorized_items = defaultdict(list)
        for item in items:
            categorized_items[item['category']].append(item)

        results = {}
        total_volume = 0
        total_value = 0

        for category, items_list in categorized_items.items():
            selected, remaining_cap = self.optimize_category(
                items_list,
                category_capacities[category]
            )

            category_volume = sum(item['volume'] for item in selected)
            category_value = sum(
                item['quantity'] * item['item']['priority']
                for item in selected
            )

            results[category] = {
                'selected_items': selected,
                'volume_used': category_volume,
                'utilization': (category_volume / category_capacities[category]) * 100
            }

            total_volume += category_volume
            total_value += category_value

        return {
            'selected_items': results,
            'total_volume': total_volume,
            'total_value': total_value,
            'execution_time': tm.time() - start_time,
            'utilization': (total_volume / max_capacity) * 100
        }

def print_knapsack_results(result: Dict):
    """Display optimization results with priority information"""
    print("\n=== Hasil Optimasi Knapsack ===")
    print(f"Total Volume: {result['total_volume']:.2f} m\u00b3")
    print(f"Total Value: {result['total_value']:.1f}")
    print(f"Overall Utilization: {result['utilization']:.1f}%")
    print(f"Execution Time: {result['execution_time']:.3f} seconds")

    print("\nDetail per Kategori:")
    for category, data in result['selected_items'].items():
        print(f"\n{category.upper()}:")
        print(f"Volume Used: {data['volume_used']:.2f} m\u00b3")
        print(f"Utilization: {data['utilization']:.1f}%")

        print("\nSelected Items:")
        for item in data['selected_items']:
            print(f"\n- {item['item']['nama']}")
            print(f"  Priority: {item['item']['priority']}")
            print(f"  Total Quantity: {item['quantity']} units")
            for box in item['boxes']:
                print(f"  {box['type']}: {box['count']} box(es) "
                      f"({box['capacity']} units each)")

                
def test_knapsack_optimization(selected_vehicle):
    """Test optimization for selected vehicle"""
    vehicles = create_vehicles()
    optimizer = KnapsackOptimizer()
    optimized_results = {}
    c = st.container(border=True)

    specs = vehicles[selected_vehicle]
    max_capacity = get_vehicle_capacity(specs)
    
    all_items = (
        [dict(item, category='makanan') for item in makanan_processed] +
        [dict(item, category='minuman') for item in minuman_processed] +
        [dict(item, category='obat') for item in obat_processed]
    )

    result = optimizer.optimize(all_items, specs, max_capacity)
    print_knapsack_results(result)
    optimized_results[selected_vehicle] = result

    return optimized_results

def display_detailed_results(optimized_results: dict):
    """
    Display detailed optimization results for all vehicles
    Args:
        optimized_results: Dictionary containing optimization results per vehicle
    """
    c = st.container(border=True)
    for vehicle_name, result in optimized_results.items():
        c.text(f"\n{'='*80}")
        c.text(f"VEHICLE: {vehicle_name}")
        c.text(f"{'='*80}")

        # Overall Statistics
        c.text("\nOVERALL STATISTICS:")
        c.text(f"Total Volume Used: {result['total_volume']:.2f} m³")
        c.text(f"Total Value Score: {result['total_value']:.1f}")
        c.text(f"Overall Utilization: {result['utilization']:.1f}%")
        c.text(f"Execution Time: {result['execution_time']:.3f} seconds")

        # Category-wise Details
        for category, data in result['selected_items'].items():
            c.text(f"\n{'-'*40}")
            c.text(f"CATEGORY: {category.upper()}")
            c.text(f"{'-'*40}")

            # Category Statistics
            c.text(f"\nCategory Statistics:")
            c.text(f"Volume Used: {data['volume_used']:.2f} m³")
            c.text(f"Space Utilization: {data['utilization']:.1f}%")

            # Selected Items Detail
            c.text(f"\nSelected Items ({len(data['selected_items'])} different products):")

            total_category_items = 0
            for item_data in data['selected_items']:
                c.text(f"\n- {item_data['item']['nama']}")
                c.text(f"  Total Quantity: {item_data['quantity']} units")
                # Display box details
                for box in item_data['boxes']:
                    c.text(f"  {box['type']}: {box['count']} box(es) "
                          f"({box['capacity']} units each)")
                total_category_items += item_data['quantity']

            c.text(f"\nTotal Items in Category: {total_category_items}")

def print_knapsack_results(result: Dict):
    """Display optimization results with priority information"""
    label = "Hasil Optimasi Knapsack"
    c = st.expander(label)
    c.text("\n=== Hasil Optimasi Knapsack ===")
    c.text(f"Total Volume: {result['total_volume']:.2f} m³")
    c.text(f"Total Value: {result['total_value']:.1f}")
    c.text(f"Overall Utilization: {result['utilization']:.1f}%")

    c.text("\nDetail per Kategori:")
    for category, data in result['selected_items'].items():
        c.text(f"\n{category.upper()}:")
        c.text(f"Volume Used: {data['volume_used']:.2f} m³")
        c.text(f"Utilization: {data['utilization']:.1f}%")

        c.text("\nSelected Items:")
        for item in data['selected_items']:
            c.text(f"\n- {item['item']['nama']}")
            c.text(f"  Priority: {item['item']['priority']}")  # Added priority
            c.text(f"  Total Quantity: {item['quantity']} units")
            for box in item['boxes']:
                c.text(f"  {box['type']}: {box['count']} box(es) "
                      f"({box['capacity']} units each)")

def display_comparative_analysis(optimized_results: dict, vehicle_specs: dict,
                               start_location, end_location):
    """Display analysis for selected vehicle"""
    label = "Hasil Analisis Untuk Kendaraan Yang Dipilih"
    c = st.expander(label)
    vehicle_name = list(optimized_results.keys())[0]
    result = optimized_results[vehicle_name]

    # Overall statistics
    c.text(f"\nANALYSIS FOR {vehicle_name}")
    c.text("=" * 40)
    total_volume = result['total_volume']
    utilization = (total_volume / get_vehicle_capacity(vehicle_specs[vehicle_name])) * 100
    total_value = result['total_value']

    c.text(f"Total Volume: {total_volume:,.2f} m³")
    c.text(f"Utilization: {utilization:,.1f}%")
    c.text(f"Total Value: {total_value:,.1f}")

    # Category analysis
    c.text("\nCATEGORY DISTRIBUTION")
    c.text("-" * 40)

    for category, data in result['selected_items'].items():
        items_count = len(data['selected_items'])
        total_qty = sum(item['quantity'] for item in data['selected_items'])

        c.text(f"\n{category.upper()}:")
        c.text(f"- Different Products: {items_count}")
        c.text(f"- Total Quantity: {total_qty}")
        c.text(f"- Volume Used: {data['volume_used']:.2f} m³")
        c.text(f"- Utilization: {data['utilization']:.1f}%")

    # Shipping cost
    distance = start_location.calculate_distance(end_location)
    c.text("\nSHIPPING COST ANALYSIS")
    c.text("-" * 40)
    c.text(f"Distance: {distance:.2f} km")

    specs = vehicle_specs[vehicle_name]
    max_load = get_vehicle_capacity(specs)
    costs = calculate_shipping_cost(distance, total_volume, specs)

    c.text(f"Maximum Capacity: {specs[0]} m³")
    c.text(f"Practical Capacity: {max_load:.2f} m³")
    c.text(f"Fuel Cost: Rp {costs['fuel_cost']:,.2f}")
    c.text(f"Total Cost: Rp {costs['total_cost']:,.2f}")

def test_and_display_optimization(selected_vehicle):
    vehicles = create_vehicles()
    optimized_results = test_knapsack_optimization(selected_vehicle)
    display_comparative_analysis(optimized_results, vehicles, start_location, end_location)
    return optimized_results

# Run optimization with selected vehicle
optimized_results = test_and_display_optimization(selected_vehicle)

class AlgorithmMetrics:
    """Class untuk menyimpan metrics hasil analisis algoritma"""
    def __init__(
        self,
        execution_time: float,
        space_complexity: int,
        total_value: float,
        total_volume: float,
        utilization: float,
        category_metrics: Dict,
        selected_items: Dict
    ):
        self.execution_time = execution_time
        self.space_complexity = space_complexity
        self.total_value = total_value
        self.total_volume = total_volume
        self.utilization = utilization
        self.category_metrics = category_metrics
        self.selected_items = selected_items

    def __str__(self) -> str:
        """String representation of metrics"""
        return (
            f"Execution Time: {self.execution_time:.4f}s\n"
            f"Space Complexity: {self.space_complexity}\n"
            f"Total Value: {self.total_value:.2f}\n"
            f"Total Volume: {self.total_volume:.2f}m³\n"
            f"Utilization: {self.utilization:.1f}%"
        )

    def to_dict(self) -> Dict:
        """Convert metrics to dictionary format"""
        return {
            'execution_time': self.execution_time,
            'space_complexity': self.space_complexity,
            'total_value': self.total_value,
            'total_volume': self.total_volume,
            'utilization': self.utilization,
            'category_metrics': self.category_metrics,
            'selected_items': self.selected_items
        }

class OptimizationAnalyzer:
    def __init__(self, greedy_results: Dict, knapsack_results: Dict):
        # Iterate over vehicle results and calculate metrics for each
        self.greedy_metrics = {
            vehicle: self._calculate_metrics(results, "Greedy") # Access the result using vehicle as key
            for vehicle, results in greedy_results.items()
        }
        self.knapsack_metrics = {
            vehicle: self._calculate_metrics(results, "Knapsack") # Access the result using vehicle as key
            for vehicle, results in knapsack_results.items()
        }

    def _calculate_metrics(self, results: Dict, algorithm_type: str) -> AlgorithmMetrics:
        """
        Menghitung berbagai metrics untuk analisis algoritma

        Args:
            results: Dictionary hasil optimasi
            algorithm_type: Tipe algoritma ("Greedy" atau "Knapsack")

        Returns:
            AlgorithmMetrics object dengan hasil perhitungan
        """
        # Calculate space complexity
        if algorithm_type == "Greedy":
            # O(n) space untuk sorting dan temporary arrays
            space_complexity = len(str(results['selected_items']))
        else:
            # O(n*W) space untuk dynamic programming table
            space_complexity = len(str(results['selected_items'])) * 2

        return AlgorithmMetrics(
            execution_time=results['execution_time'],
            space_complexity=space_complexity,
            total_value=results['total_value'],
            total_volume=results['total_volume'],
            utilization=results['utilization'],
            category_metrics=results.get('category_metrics', {}),
            selected_items=results['selected_items']
        )

    def analyze_time_complexity(self) -> Dict[str, Dict[str, str]]:
        """
        Analisis kompleksitas waktu kedua algoritma
        Returns:
            Dictionary dengan analisis kompleksitas
        """
        return {
            "Greedy": {
                "worst_case": "O(n log n)",
                "average_case": "O(n log n)",
                "best_case": "O(n log n)",
                "reason": "Dominated by sorting operation, where n is number of items"
            },
            "Knapsack": {
                "worst_case": "O(n * W)",
                "average_case": "O(n * W)",
                "best_case": "O(n * W)",
                "reason": "Dynamic programming approach, where n is items and W is capacity"
            }
        }

    def analyze_space_efficiency(self) -> Dict[str, float]:
        """
        Analisis efisiensi penggunaan memori
        Returns:
            Dictionary dengan metrics efisiensi ruang
        """
        return {
            "greedy_space_efficiency": 1 / self.greedy_metrics.space_complexity,
            "knapsack_space_efficiency": 1 / self.knapsack_metrics.space_complexity,
            "relative_efficiency": (self.greedy_metrics.space_complexity /
                                  self.knapsack_metrics.space_complexity)
        }

    def analyze_solution_quality(self) -> Dict[str, float]:
        """
        Analisis kualitas solusi berdasarkan multiple metrics
        Returns:
            Dictionary dengan metrics kualitas solusi
        """
        return {
            "value_ratio": (self.knapsack_metrics.total_value /
                          self.greedy_metrics.total_value),
            "volume_efficiency": {
                "greedy": self.greedy_metrics.utilization,
                "knapsack": self.knapsack_metrics.utilization
            },
            "execution_time_ratio": (self.knapsack_metrics.execution_time /
                                   self.greedy_metrics.execution_time)
        }

    def generate_comparison_visualizations(self) -> None:
        """
        Membuat visualisasi perbandingan algoritma
        """
        # Setup plotting style using Seaborn
        sns.set_theme()  # Use Seaborn's default theme
        #sns.set_style('darkgrid')  # Or choose a specific Seaborn style like 'darkgrid'

        # Get a list of vehicle names from either greedy_metrics or knapsack_metrics
        # (assuming they have the same vehicle names)
        vehicle_names = list(self.greedy_metrics.keys())

        for vehicle_name in vehicle_names:
            fig = plt.figure(figsize=(15, 10))

            # 1. Performance Metrics Comparison
            ax1 = plt.subplot(221)
            metrics = ['Total Value', 'Utilization (%)', 'Execution Time (ms)']
            greedy_vals = [self.greedy_metrics[vehicle_name].total_value, # Access metrics for the specific vehicle
                          self.greedy_metrics[vehicle_name].utilization,
                          self.greedy_metrics[vehicle_name].execution_time * 1000]
            knapsack_vals = [self.knapsack_metrics[vehicle_name].total_value, # Access metrics for the specific vehicle
                            self.knapsack_metrics[vehicle_name].utilization,
                            self.knapsack_metrics[vehicle_name].execution_time * 1000]


        x = np.arange(len(metrics))
        width = 0.35

        ax1.bar(x - width/2, greedy_vals, width, label='Greedy')
        ax1.bar(x + width/2, knapsack_vals, width, label='Knapsack')
        ax1.set_xticks(x)
        ax1.set_xticklabels(metrics)
        ax1.legend()
        ax1.set_title('Performance Metrics Comparison')

        # 2. Category-wise Utilization
        ax2 = plt.subplot(222)
        categories = list(self.greedy_metrics.category_metrics.keys())
        greedy_utils = [self.greedy_metrics.category_metrics[cat]['utilization']
                       for cat in categories]
        knapsack_utils = [self.knapsack_metrics.selected_items[cat]['utilization']
                         for cat in categories]

        width = 0.35
        ax2.bar([i - width/2 for i in range(len(categories))],
                greedy_utils,
                width,
                label='Greedy')
        ax2.bar([i + width/2 for i in range(len(categories))],
                knapsack_utils,
                width,
                label='Knapsack')
        ax2.set_xticks(range(len(categories)))
        ax2.set_xticklabels(categories)
        ax2.legend()
        ax2.set_title('Category-wise Utilization')

        plt.tight_layout()
        st.pyplot(fig)

    def generate_recommendations(self) -> Dict[str, str]:
        """
        Generate recommendations based on analysis
        Returns:
            Dictionary dengan rekomendasi penggunaan algoritma
        """
        quality_metrics = self.analyze_solution_quality()
        space_metrics = self.analyze_space_efficiency()

        recommendations = {
            "best_overall": "",
            "reasons": [],
            "use_cases": {
                "greedy": [],
                "knapsack": []
            }
        }

        # Analyze value ratio
        if quality_metrics["value_ratio"] > 1.1:
            recommendations["reasons"].append(
                "Knapsack menghasilkan nilai total yang lebih tinggi (>10%)"
            )
            recommendations["use_cases"]["knapsack"].append(
                "Optimasi nilai dengan constraint ketat"
            )
        else:
            recommendations["reasons"].append(
                "Greedy memberikan hasil yang kompetitif untuk nilai total"
            )
            recommendations["use_cases"]["greedy"].append(
                "Optimasi cepat dengan hasil yang baik"
            )

        # Analyze execution time
        if quality_metrics["execution_time_ratio"] > 2:
            recommendations["reasons"].append(
                "Greedy signifikan lebih cepat dalam eksekusi"
            )
            recommendations["use_cases"]["greedy"].append(
                "Scenario real-time atau batch processing besar"
            )

        # Analyze space efficiency
        if space_metrics["relative_efficiency"] < 0.5:
            recommendations["reasons"].append(
                "Greedy lebih efisien dalam penggunaan memori"
            )
            recommendations["use_cases"]["greedy"].append(
                "Sistem dengan keterbatasan memori"
            )

        # Make final recommendation
        if len(recommendations["use_cases"]["greedy"]) > len(recommendations["use_cases"]["knapsack"]):
            recommendations["best_overall"] = "Greedy Algorithm"
        else:
            recommendations["best_overall"] = "Knapsack Algorithm"

        return recommendations

def print_analysis_report(analyzer: OptimizationAnalyzer) -> None:
    """
    Mencetak laporan analisis komprehensif
    Args:
        analyzer: OptimizationAnalyzer object
    """
    label = "ANALISIS PERBANDINGAN ALGORITMA OPTIMASI"
    c = st.expander(label)
    c.text("=== ANALISIS PERBANDINGAN ALGORITMA OPTIMASI ===\n")

    # 1. Time Complexity Analysis
    c.text("1. ANALISIS KOMPLEKSITAS WAKTU")
    time_analysis = analyzer.analyze_time_complexity()
    for algo, complexity in time_analysis.items():
        c.text(f"\n{algo} Algorithm:")
        for case, value in complexity.items():
            c.text(f"  {case}: {value}")

    # 2. Space Efficiency
    c.text("\n2. ANALISIS EFISIENSI RUANG")
    space_analysis = analyzer.analyze_space_efficiency()
    c.text(f"Relative Space Efficiency: {space_analysis['relative_efficiency']:.2f}")

    # 3. Solution Quality
    c.text("\n3. ANALISIS KUALITAS SOLUSI")
    quality_metrics = analyzer.analyze_solution_quality()
    c.text(f"Value Ratio (Knapsack/Greedy): {quality_metrics['value_ratio']:.2f}")
    c.text("\nVolume Utilization:")
    c.text(f"  Greedy: {quality_metrics['volume_efficiency']['greedy']:.1f}%")
    c.text(f"  Knapsack: {quality_metrics['volume_efficiency']['knapsack']:.1f}%")
    c.text(f"\nExecution Time Ratio: {quality_metrics['execution_time_ratio']:.2f}")

    # 4. Recommendations
    c.text("\n4. REKOMENDASI")
    recommendations = analyzer.generate_recommendations()
    c.text(f"\nRekomendasi Algoritma: {recommendations['best_overall']}")
    c.text("\nAlasan:")
    for reason in recommendations['reasons']:
        c.text(f"- {reason}")

    c.text("\nUse Cases:")
    c.text("\nGreedy Algorithm:")
    for use_case in recommendations['use_cases']['greedy']:
        c.text(f"- {use_case}")
    c.text("\nKnapsack Algorithm:")
    for use_case in recommendations['use_cases']['knapsack']:
        c.text(f"- {use_case}")
        
class AlgorithmMetrics:
    """Class untuk menyimpan metrics hasil analisis algoritma"""
    def __init__(
        self,
        execution_time: float,
        space_complexity: int,
        total_value: float,
        total_volume: float,
        utilization: float,
        category_metrics: Dict,
        selected_items: Dict
    ):
        self.execution_time = execution_time
        self.space_complexity = space_complexity
        self.total_value = total_value
        self.total_volume = total_volume
        self.utilization = utilization
        self.category_metrics = category_metrics
        self.selected_items = selected_items

class OptimizationAnalyzer:
    """
    Sistem analisis perbandingan algoritma optimasi per kendaraan
    """
    def __init__(self, greedy_results: Dict[str, Dict], knapsack_results: Dict[str, Dict]):
        """
        Initialize analyzer with results for multiple vehicles

        Args:
            greedy_results: Dictionary with vehicle names as keys and optimization results as values
            knapsack_results: Dictionary with vehicle names as keys and optimization results as values
        """
        self.greedy_metrics = {
            vehicle: self._calculate_metrics(results, "Greedy")
            for vehicle, results in greedy_results.items()
        }
        self.knapsack_metrics = {
            vehicle: self._calculate_metrics(results, "Knapsack")
            for vehicle, results in knapsack_results.items()
        }

    def _calculate_metrics(self, results: Dict, algorithm_type: str) -> AlgorithmMetrics:
        """Calculate metrics for a single vehicle's results"""
        space_complexity = (
            len(str(results['selected_items'])) if algorithm_type == "Greedy"
            else len(str(results['selected_items'])) * 2
        )

        return AlgorithmMetrics(
            execution_time=results['execution_time'],
            space_complexity=space_complexity,
            total_value=results['total_value'],
            total_volume=results['total_volume'],
            utilization=results['utilization'],
            category_metrics=results.get('category_metrics', {}),
            selected_items=results['selected_items']
        )
    def generate_comparison_visualizations(self) -> None:
        """Generate visualizations for each vehicle with improved scaling"""
        sns.set_theme(style='whitegrid')

        for vehicle_name in self.greedy_metrics.keys():
            fig = plt.figure(figsize=(20, 12))

            # 1. Performance Metrics - Split into three separate subplots
            # Total Value
            ax1 = plt.subplot(231)
            metrics = ['Total Value']
            greedy_vals = [self.greedy_metrics[vehicle_name].total_value]
            knapsack_vals = [self.knapsack_metrics[vehicle_name].total_value]

            x = np.arange(len(metrics))
            width = 0.35

            bars1 = ax1.bar(x - width/2, greedy_vals, width, label='Greedy',
                           color=sns.color_palette()[0])
            bars2 = ax1.bar(x + width/2, knapsack_vals, width, label='Knapsack',
                           color=sns.color_palette()[1])

            def autolabel(bars, ax):
                for bar in bars:
                    height = bar.get_height()
                    ax.annotate(f'{height:.1f}',
                              xy=(bar.get_x() + bar.get_width() / 2, height),
                              xytext=(0, 3),
                              textcoords="offset points",
                              ha='center', va='bottom')

            autolabel(bars1, ax1)
            autolabel(bars2, ax1)
            ax1.set_xticks(x)
            ax1.set_xticklabels(metrics)
            ax1.legend()
            ax1.set_title('Total Value Comparison')

            # Utilization
            ax2 = plt.subplot(232)
            metrics = ['Utilization (%)']
            greedy_vals = [self.greedy_metrics[vehicle_name].utilization]
            knapsack_vals = [self.knapsack_metrics[vehicle_name].utilization]

            bars3 = ax2.bar(x - width/2, greedy_vals, width, label='Greedy',
                           color=sns.color_palette()[0])
            bars4 = ax2.bar(x + width/2, knapsack_vals, width, label='Knapsack',
                           color=sns.color_palette()[1])

            autolabel(bars3, ax2)
            autolabel(bars4, ax2)
            ax2.set_xticks(x)
            ax2.set_xticklabels(metrics)
            ax2.legend()
            ax2.set_title('Utilization Comparison')

            # Execution Time
            ax3 = plt.subplot(233)
            metrics = ['Execution Time (ms)']
            greedy_vals = [self.greedy_metrics[vehicle_name].execution_time * 1000]
            knapsack_vals = [self.knapsack_metrics[vehicle_name].execution_time * 1000]

            bars5 = ax3.bar(x - width/2, greedy_vals, width, label='Greedy',
                           color=sns.color_palette()[0])
            bars6 = ax3.bar(x + width/2, knapsack_vals, width, label='Knapsack',
                           color=sns.color_palette()[1])

            autolabel(bars5, ax3)
            autolabel(bars6, ax3)
            ax3.set_xticks(x)
            ax3.set_xticklabels(metrics)
            ax3.legend()
            ax3.set_title('Execution Time Comparison')

            # 2. Category-wise Utilization
            ax4 = plt.subplot(234)

            # Get categories from either metrics
            categories = list(set(
                list(self.greedy_metrics[vehicle_name].category_metrics.keys()) +
                list(self.knapsack_metrics[vehicle_name].selected_items.keys())
            ))

            def get_utilization(metrics, category):
                try:
                    if category in metrics.category_metrics:
                        return metrics.category_metrics[category]['utilization']
                    elif category in metrics.selected_items:
                        return metrics.selected_items[category]['utilization']
                    return 0
                except (KeyError, AttributeError):
                    return 0

            greedy_utils = [
                get_utilization(self.greedy_metrics[vehicle_name], cat)
                for cat in categories
            ]
            knapsack_utils = [
                get_utilization(self.knapsack_metrics[vehicle_name], cat)
                for cat in categories
            ]

            x = np.arange(len(categories))
            width = 0.35

            bars7 = ax4.bar(x - width/2, greedy_utils, width, label='Greedy',
                           color=sns.color_palette()[0])
            bars8 = ax4.bar(x + width/2, knapsack_utils, width, label='Knapsack',
                           color=sns.color_palette()[1])

            autolabel(bars7, ax4)
            autolabel(bars8, ax4)

            ax4.set_xticks(x)
            ax4.set_xticklabels(categories)
            ax4.legend()
            ax4.set_title('Category-wise Utilization (%)')

            # 3. Volume Comparison
            ax5 = plt.subplot(235)
            volume_metrics = ['Total Volume']

            greedy_volume = [self.greedy_metrics[vehicle_name].total_volume]
            knapsack_volume = [self.knapsack_metrics[vehicle_name].total_volume]

            x = np.arange(len(volume_metrics))

            bars9 = ax5.bar(x - width/2, greedy_volume, width, label='Greedy',
                           color=sns.color_palette()[0])
            bars10 = ax5.bar(x + width/2, knapsack_volume, width, label='Knapsack',
                           color=sns.color_palette()[1])

            autolabel(bars9, ax5)
            autolabel(bars10, ax5)

            ax5.set_xticks(x)
            ax5.set_xticklabels(volume_metrics)
            ax5.legend()
            ax5.set_title('Volume Comparison (m³)')

            # 4. Summary Text
            ax6 = plt.subplot(236)
            ax6.axis('off')

            greedy_metrics = self.greedy_metrics[vehicle_name]
            knapsack_metrics = self.knapsack_metrics[vehicle_name]

            summary_text = (
                f"Summary for {vehicle_name}:\n\n"
                f"Greedy Algorithm:\n"
                f"- Total Value: {greedy_metrics.total_value:.1f}\n"
                f"- Utilization: {greedy_metrics.utilization:.1f}%\n"
                f"- Execution Time: {greedy_metrics.execution_time*1000:.2f}ms\n\n"
                f"Knapsack Algorithm:\n"
                f"- Total Value: {knapsack_metrics.total_value:.1f}\n"
                f"- Utilization: {knapsack_metrics.utilization:.1f}%\n"
                f"- Execution Time: {knapsack_metrics.execution_time*1000:.2f}ms\n\n"
                f"Improvement with Knapsack:\n"
                f"- Value: {((knapsack_metrics.total_value/greedy_metrics.total_value)-1)*100:.1f}%\n"
                f"- Utilization: {(knapsack_metrics.utilization-greedy_metrics.utilization):.1f}%\n"
            )

            ax6.text(0, 1, summary_text, va='top', ha='left', fontsize=10)

            plt.suptitle(f'Algorithm Optimization Comparison - {vehicle_name}',
                        fontsize=16, y=1.02)
            plt.tight_layout()
            st.pyplot(fig)

def print_analysis_report(analyzer: OptimizationAnalyzer) -> None:
    """Print analysis report for all vehicles"""
    label = "ANALISIS PERBANDINGAN ALGORITMA OPTIMASI"
    c = st.expander(label)
    for vehicle_name in analyzer.greedy_metrics.keys():
        c.text(f"\n=== ANALISIS PERBANDINGAN ALGORITMA OPTIMASI - {vehicle_name} ===\n")

        greedy_metrics = analyzer.greedy_metrics[vehicle_name]
        knapsack_metrics = analyzer.knapsack_metrics[vehicle_name]

        c.text("1. METRICS PERFORMA")
        c.text(f"Total Value:")
        c.text(f"  Greedy: {greedy_metrics.total_value:.1f}")
        c.text(f"  Knapsack: {knapsack_metrics.total_value:.1f}")
        c.text(f"  Improvement: {((knapsack_metrics.total_value/greedy_metrics.total_value)-1)*100:.1f}%")

        c.text(f"\nUtilization:")
        c.text(f"  Greedy: {greedy_metrics.utilization:.1f}%")
        c.text(f"  Knapsack: {knapsack_metrics.utilization:.1f}%")
        c.text(f"  Difference: {(knapsack_metrics.utilization-greedy_metrics.utilization):.1f}%")

        c.text(f"\nExecution Time:")
        c.text(f"  Greedy: {greedy_metrics.execution_time*1000:.2f}ms")
        c.text(f"  Knapsack: {knapsack_metrics.execution_time*1000:.2f}ms")
        if greedy_metrics.execution_time > 0:
            c.text(f"  Ratio: {knapsack_metrics.execution_time/greedy_metrics.execution_time:.2f}x slower")
        else:
            c.text(f"  Ratio: more slower") # ERROR: Should handle division by zero

        c.text("\n2. CATEGORY-WISE ANALYSIS")
        # Get all unique categories
        categories = list(set(
            list(greedy_metrics.category_metrics.keys()) +
            list(knapsack_metrics.selected_items.keys())
        ))

        def get_utilization(metrics, category):
            try:
                if category in metrics.category_metrics:
                    return metrics.category_metrics[category]['utilization']
                elif category in metrics.selected_items:
                    return metrics.selected_items[category]['utilization']
                return 0
            except (KeyError, AttributeError):
                return 0

        for category in categories:
            c.text(f"\n{category.upper()}:")
            greedy_util = get_utilization(greedy_metrics, category)
            knapsack_util = get_utilization(knapsack_metrics, category)
            c.text(f"  Utilization:")
            c.text(f"    Greedy: {greedy_util:.1f}%")
            c.text(f"    Knapsack: {knapsack_util:.1f}%")
            c.text(f"    Difference: {knapsack_util-greedy_util:.1f}%")
            
greedy_result = test_greedy_optimization(selected_vehicle)
knapsack_result = test_knapsack_optimization(selected_vehicle)

# Inisialisasi analyzer
analyzer = OptimizationAnalyzer(greedy_result, knapsack_result) # Changed greedy_results to greedy_result and knapsack_results to knapsack_result

# Generate visualisasi
analyzer.generate_comparison_visualizations()

# Print laporan analisis
print_analysis_report(analyzer)