from flask import Blueprint, request, jsonify
import math
import numpy as np
from flask_cors import cross_origin

engineering_bp = Blueprint('engineering', __name__)

@engineering_bp.route('/calculate/area', methods=['POST'])
@cross_origin()
def calculate_area():
    """Calculate area and perimeter using Shoelace formula"""
    try:
        data = request.get_json()
        coordinates = data.get('coordinates', [])
        
        if len(coordinates) < 3:
            return jsonify({'error': 'يجب إدخال 3 نقاط على الأقل'}), 400
        
        # Convert to float and validate
        points = []
        for coord in coordinates:
            try:
                x = float(coord['x'])
                y = float(coord['y'])
                points.append((x, y))
            except (ValueError, KeyError):
                return jsonify({'error': 'إحداثيات غير صحيحة'}), 400
        
        # Calculate area using Shoelace formula
        area = 0
        perimeter = 0
        n = len(points)
        
        for i in range(n):
            j = (i + 1) % n
            area += points[i][0] * points[j][1]
            area -= points[j][0] * points[i][1]
            
            # Calculate perimeter
            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]
            perimeter += math.sqrt(dx*dx + dy*dy)
        
        area = abs(area) / 2
        
        return jsonify({
            'area': round(area, 2),
            'perimeter': round(perimeter, 2),
            'area_text': f'المساحة: {area:.2f} متر مربع',
            'perimeter_text': f'المحيط: {perimeter:.2f} متر'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@engineering_bp.route('/calculate/beam', methods=['POST'])
@cross_origin()
def calculate_beam():
    """Calculate beam moments and deflections"""
    try:
        data = request.get_json()
        length = float(data.get('length', 0))
        load = float(data.get('load', 0))
        support_type = data.get('support', 'simply-supported')
        
        if length <= 0 or load <= 0:
            return jsonify({'error': 'يرجى إدخال قيم صحيحة'}), 400
        
        # Beam calculations based on support type
        if support_type == 'simply-supported':
            # Point load at center
            max_moment = (load * length) / 4
            max_shear = load / 2
            # Assuming E = 200 GPa, I = 1000 cm4
            E = 200000  # MPa
            I = 1000 * 1e-8  # m4 (converted from cm4)
            max_deflection = (load * 1000 * (length**3)) / (48 * E * 1e6 * I) * 1000  # mm
        elif support_type == 'fixed':
            # Fixed beam with point load at center
            max_moment = (load * length) / 8
            max_shear = load / 2
            E = 200000
            I = 1000 * 1e-8
            max_deflection = (load * 1000 * (length**3)) / (192 * E * 1e6 * I) * 1000  # mm
        elif support_type == 'cantilever':
            # Cantilever with point load at end
            max_moment = load * length
            max_shear = load
            E = 200000
            I = 1000 * 1e-8
            max_deflection = (load * 1000 * (length**3)) / (3 * E * 1e6 * I) * 1000  # mm
        else:
            return jsonify({'error': 'نوع إسناد غير مدعوم'}), 400
        
        return jsonify({
            'max_moment': round(max_moment, 2),
            'max_shear': round(max_shear, 2),
            'max_deflection': round(max_deflection, 2),
            'moment_text': f'العزم الأقصى: {max_moment:.2f} كيلو نيوتن.متر',
            'shear_text': f'القص الأقصى: {max_shear:.2f} كيلو نيوتن',
            'deflection_text': f'الانحراف الأقصى: {max_deflection:.2f} مم'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@engineering_bp.route('/calculate/concrete', methods=['POST'])
@cross_origin()
def calculate_concrete():
    """Calculate concrete volume and material quantities"""
    try:
        data = request.get_json()
        length = float(data.get('length', 0))
        width = float(data.get('width', 0))
        height = float(data.get('height', 0))
        element_type = data.get('type', 'slab')
        
        if length <= 0 or width <= 0 or height <= 0:
            return jsonify({'error': 'يرجى إدخال أبعاد صحيحة'}), 400
        
        # Calculate volume
        volume = length * width * height
        
        # Material calculations (typical mix ratios)
        cement = volume * 350  # kg per m3
        sand = volume * 0.5    # m3
        aggregate = volume * 0.8  # m3
        water = volume * 175   # liters
        
        # Cost estimation (example prices in local currency)
        cement_cost = cement * 0.15  # price per kg
        sand_cost = sand * 50        # price per m3
        aggregate_cost = aggregate * 60  # price per m3
        total_cost = cement_cost + sand_cost + aggregate_cost
        
        return jsonify({
            'volume': round(volume, 2),
            'cement': round(cement, 0),
            'sand': round(sand, 2),
            'aggregate': round(aggregate, 2),
            'water': round(water, 0),
            'total_cost': round(total_cost, 2),
            'volume_text': f'حجم الخرسانة: {volume:.2f} متر مكعب',
            'cement_text': f'الأسمنت: {cement:.0f} كيلوجرام',
            'sand_text': f'الرمل: {sand:.2f} متر مكعب',
            'aggregate_text': f'الحصى: {aggregate:.2f} متر مكعب',
            'water_text': f'الماء: {water:.0f} لتر',
            'cost_text': f'التكلفة التقديرية: {total_cost:.2f} ريال'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@engineering_bp.route('/calculate/steel', methods=['POST'])
@cross_origin()
def calculate_steel():
    """Calculate steel reinforcement quantities"""
    try:
        data = request.get_json()
        bars = int(data.get('bars', 0))
        diameter = float(data.get('diameter', 0))
        length = float(data.get('length', 0))
        
        if bars <= 0 or diameter <= 0 or length <= 0:
            return jsonify({'error': 'يرجى إدخال قيم صحيحة'}), 400
        
        # Calculate steel quantities
        total_length = bars * length
        bar_weight = (diameter**2) * 0.00617  # kg/m for steel
        total_weight = total_length * bar_weight
        total_tons = total_weight / 1000
        
        # Cost estimation
        steel_price_per_ton = 3500  # example price
        total_cost = total_tons * steel_price_per_ton
        
        return jsonify({
            'total_length': round(total_length, 2),
            'total_weight': round(total_weight, 2),
            'total_tons': round(total_tons, 3),
            'total_cost': round(total_cost, 2),
            'length_text': f'الطول الكلي: {total_length:.2f} متر',
            'weight_text': f'الوزن الكلي: {total_weight:.2f} كيلوجرام',
            'tons_text': f'الوزن بالطن: {total_tons:.3f} طن',
            'cost_text': f'التكلفة التقديرية: {total_cost:.2f} ريال'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@engineering_bp.route('/calculate/coordinate-transform', methods=['POST'])
@cross_origin()
def coordinate_transform():
    """Transform coordinates between UTM and Geographic"""
    try:
        data = request.get_json()
        transform_type = data.get('type', 'utm-to-geo')
        
        if transform_type == 'utm-to-geo':
            easting = float(data.get('easting', 0))
            northing = float(data.get('northing', 0))
            zone = int(data.get('zone', 36))
            
            # Simplified conversion (in real application, use pyproj or similar)
            # This is just for demonstration
            lat = northing / 111320
            lon = easting / 111320
            
            return jsonify({
                'latitude': round(lat, 6),
                'longitude': round(lon, 6),
                'result_text': f'خط العرض: {lat:.6f}°\nخط الطول: {lon:.6f}°'
            })
            
        elif transform_type == 'geo-to-utm':
            latitude = float(data.get('latitude', 0))
            longitude = float(data.get('longitude', 0))
            
            # Simplified conversion
            easting = longitude * 111320
            northing = latitude * 111320
            
            return jsonify({
                'easting': round(easting, 2),
                'northing': round(northing, 2),
                'result_text': f'الإحداثي الشرقي: {easting:.2f} متر\nالإحداثي الشمالي: {northing:.2f} متر'
            })
        
        else:
            return jsonify({'error': 'نوع تحويل غير مدعوم'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@engineering_bp.route('/calculate/slope', methods=['POST'])
@cross_origin()
def calculate_slope():
    """Calculate slope between two points"""
    try:
        data = request.get_json()
        x1 = float(data.get('x1', 0))
        y1 = float(data.get('y1', 0))
        x2 = float(data.get('x2', 0))
        y2 = float(data.get('y2', 0))
        
        delta_x = x2 - x1
        delta_y = y2 - y1
        
        if delta_x == 0:
            return jsonify({
                'slope': 'undefined',
                'result_text': 'الميل عمودي (غير محدد)'
            })
        
        slope = delta_y / delta_x
        percentage = slope * 100
        angle = math.degrees(math.atan(slope))
        ratio = f"1:{abs(delta_x / delta_y):.2f}" if delta_y != 0 else "غير محدد"
        
        return jsonify({
            'slope': round(slope, 4),
            'percentage': round(percentage, 2),
            'angle': round(angle, 2),
            'ratio': ratio,
            'slope_text': f'الميل: {slope:.4f}',
            'percentage_text': f'النسبة المئوية: {percentage:.2f}%',
            'angle_text': f'الزاوية: {angle:.2f}°',
            'ratio_text': f'النسبة: {ratio}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

