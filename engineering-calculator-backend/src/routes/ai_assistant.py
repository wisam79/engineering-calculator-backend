from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import openai
import os
import json

ai_bp = Blueprint('ai', __name__)

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_base = os.getenv('OPENAI_API_BASE')

@ai_bp.route('/ai/analyze-structure', methods=['POST'])
@cross_origin()
def analyze_structure():
    """AI-powered structural analysis and recommendations"""
    try:
        data = request.get_json()
        structure_type = data.get('type', '')
        dimensions = data.get('dimensions', {})
        loads = data.get('loads', {})
        materials = data.get('materials', {})
        
        # Create a detailed prompt for structural analysis
        prompt = f"""
        أنت مهندس مدني خبير. قم بتحليل المنشأ التالي وقدم توصيات مفصلة:

        نوع المنشأ: {structure_type}
        الأبعاد: {json.dumps(dimensions, ensure_ascii=False)}
        الأحمال: {json.dumps(loads, ensure_ascii=False)}
        المواد: {json.dumps(materials, ensure_ascii=False)}

        يرجى تقديم:
        1. تحليل الأمان الإنشائي
        2. توصيات للتحسين
        3. تحذيرات من المخاطر المحتملة
        4. اقتراحات بديلة للتصميم
        5. تقدير التكلفة التقريبية

        الرد باللغة العربية بشكل مفصل ومهني.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مهندس مدني خبير متخصص في التحليل الإنشائي والتصميم."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        analysis = response.choices[0].message.content
        
        return jsonify({
            'analysis': analysis,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': f'خطأ في التحليل: {str(e)}',
            'success': False
        }), 500

@ai_bp.route('/ai/generate-code', methods=['POST'])
@cross_origin()
def generate_code():
    """Generate engineering calculation code based on requirements"""
    try:
        data = request.get_json()
        calculation_type = data.get('type', '')
        requirements = data.get('requirements', '')
        language = data.get('language', 'python')
        
        prompt = f"""
        قم بإنشاء كود {language} لحساب {calculation_type} بناءً على المتطلبات التالية:
        
        المتطلبات: {requirements}
        
        يجب أن يتضمن الكود:
        1. دوال واضحة ومنظمة
        2. تعليقات باللغة العربية
        3. معالجة الأخطاء
        4. أمثلة على الاستخدام
        5. وحدات القياس المناسبة
        
        اكتب الكود بشكل احترافي وقابل للقراءة.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مطور برمجيات متخصص في الحسابات الهندسية."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.3
        )
        
        code = response.choices[0].message.content
        
        return jsonify({
            'code': code,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': f'خطأ في إنشاء الكود: {str(e)}',
            'success': False
        }), 500

@ai_bp.route('/ai/optimize-design', methods=['POST'])
@cross_origin()
def optimize_design():
    """AI-powered design optimization suggestions"""
    try:
        data = request.get_json()
        current_design = data.get('design', {})
        constraints = data.get('constraints', {})
        objectives = data.get('objectives', [])
        
        prompt = f"""
        بصفتك مهندس تحسين التصميم، قم بتحليل التصميم الحالي واقتراح تحسينات:

        التصميم الحالي: {json.dumps(current_design, ensure_ascii=False)}
        القيود: {json.dumps(constraints, ensure_ascii=False)}
        الأهداف: {json.dumps(objectives, ensure_ascii=False)}

        قدم:
        1. تحليل نقاط القوة والضعف في التصميم الحالي
        2. اقتراحات محددة للتحسين
        3. تقدير تأثير كل تحسين على الأداء والتكلفة
        4. أولوية التنفيذ للتحسينات المقترحة
        5. مخاطر محتملة وكيفية تجنبها

        الرد باللغة العربية بشكل مفصل ومنظم.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت خبير في تحسين التصميم الهندسي والتحليل الاقتصادي."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1800,
            temperature=0.6
        )
        
        optimization = response.choices[0].message.content
        
        return jsonify({
            'optimization': optimization,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': f'خطأ في تحسين التصميم: {str(e)}',
            'success': False
        }), 500

@ai_bp.route('/ai/explain-calculation', methods=['POST'])
@cross_origin()
def explain_calculation():
    """Explain engineering calculations in simple terms"""
    try:
        data = request.get_json()
        calculation = data.get('calculation', '')
        result = data.get('result', '')
        level = data.get('level', 'intermediate')  # beginner, intermediate, advanced
        
        prompt = f"""
        اشرح الحساب الهندسي التالي بطريقة مفهومة للمستوى {level}:

        الحساب: {calculation}
        النتيجة: {result}

        يجب أن يتضمن الشرح:
        1. الهدف من الحساب
        2. المبادئ الأساسية المستخدمة
        3. خطوات الحساب بالتفصيل
        4. تفسير النتيجة وأهميتها
        5. تطبيقات عملية للحساب
        6. نصائح للتحقق من صحة النتيجة

        استخدم لغة واضحة ومناسبة للمستوى المطلوب.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مدرس هندسة مدنية متخصص في تبسيط المفاهيم المعقدة."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.5
        )
        
        explanation = response.choices[0].message.content
        
        return jsonify({
            'explanation': explanation,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': f'خطأ في الشرح: {str(e)}',
            'success': False
        }), 500

@ai_bp.route('/ai/safety-check', methods=['POST'])
@cross_origin()
def safety_check():
    """AI-powered safety analysis and compliance check"""
    try:
        data = request.get_json()
        project_details = data.get('project', {})
        location = data.get('location', '')
        building_code = data.get('code', 'SBC')  # Saudi Building Code by default
        
        prompt = f"""
        قم بفحص السلامة والامتثال للكود للمشروع التالي:

        تفاصيل المشروع: {json.dumps(project_details, ensure_ascii=False)}
        الموقع: {location}
        الكود المطبق: {building_code}

        قدم تقرير شامل يتضمن:
        1. فحص الامتثال لمتطلبات الكود
        2. تحليل عوامل الأمان
        3. تحديد المخاطر المحتملة
        4. توصيات لتحسين السلامة
        5. متطلبات إضافية حسب الموقع الجغرافي
        6. جدول زمني للفحوصات المطلوبة

        الرد باللغة العربية بشكل مفصل ومهني.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت خبير في السلامة الإنشائية والامتثال للأكواد الهندسية."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.4
        )
        
        safety_report = response.choices[0].message.content
        
        return jsonify({
            'safety_report': safety_report,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': f'خطأ في فحص السلامة: {str(e)}',
            'success': False
        }), 500

