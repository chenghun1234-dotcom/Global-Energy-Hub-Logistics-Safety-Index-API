import json
import os

def load_json(filename):
    path = os.path.join(os.path.dirname(__file__), '..', 'data', filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_route_safety(route_id):
    routes = load_json('routes.json')
    route = next((r for r in routes if r['route_id'] == route_id), None)
    
    if not route:
        return None
    
    # Logic: (Conflict Zone Index * 1.5) + Piracy Level + Chokepoints
    # Scale: 0 - 25 (approximated)
    score = (route['conflict_zone_index'] * 1.5) + route['piracy_threat_level'] + route['chokepoints']
    
    # Categorize
    if score < 5:
        risk = "Low"
    elif score < 12:
        risk = "Moderate"
    elif score < 20:
        risk = "High"
    else:
        risk = "Extreme"
        
    return {
        "route_name": route['name'],
        "safety_score": round(score, 2),
        "risk_category": risk,
        "parameters": {
            "conflict_index": route['conflict_zone_index'],
            "piracy_level": route['piracy_threat_level'],
            "chokepoints": route['chokepoints']
        }
    }

def calculate_energy_tax(country_code, quantity_m3, storage_months=0, product_value_per_m3=800):
    taxes = load_json('taxes.json')
    tax_info = taxes.get(country_code.upper())
    
    if not tax_info:
        return None
    
    total_value = quantity_m3 * product_value_per_m3
    
    # Import Tariff
    tariff_amount = total_value * tax_info['import_tariff_oil']
    
    # VAT (Applied after tariff in some regions, keeping it simple here)
    vat_amount = (total_value + tariff_amount) * tax_info['vat']
    
    # Education Tax (Typically a percentage of excise or VAT in Korea, simplified here)
    edu_tax_amount = vat_amount * tax_info['education_tax']
    
    # Storage Fees
    storage_cost = quantity_m3 * tax_info['storage_fee_per_month_m3'] * storage_months
    
    total_cost = total_value + tariff_amount + vat_amount + edu_tax_amount + storage_cost
    
    return {
        "country": tax_info['country_name'],
        "currency": "USD",
        "breakdown": {
            "product_value": round(total_value, 2),
            "import_tariff": round(tariff_amount, 2),
            "vat": round(vat_amount, 2),
            "education_tax": round(edu_tax_amount, 2),
            "storage_cost": round(storage_cost, 2)
        },
        "total_estimated_cost": round(total_cost, 2),
        "exemptions": tax_info['exemptions']
    }

def get_port_specs(port_id_or_name):
    ports = load_json('ports.json')
    q = port_id_or_name.lower()
    port = next((p for p in ports if q in p['id'].lower() or q in p['name'].lower()), None)
    return port
