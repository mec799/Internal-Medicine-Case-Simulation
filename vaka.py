# Dahiliye Vaka Simülasyonu - TUS Hazırlık Uygulaması
import streamlit as st
import openai
import json
import pandas as pd
import datetime
import time
import random

# Sayfa yapılandırması
st.set_page_config(
    page_title="Dahiliye Vaka Simülasyonu | Internal Medicine Case Simulation",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dil çeviri sözlüğü
translations = {
    "tr": {
        "app_title": "Dahiliye Vaka Simülasyonu",
        "api_settings": "API Ayarları",
        "api_key": "OpenAI API Anahtarı",
        "model_selection": "Model Seçimi",
        "difficulty_level": "Zorluk Seviyesi",
        "easy": "Kolay",
        "medium": "Orta",
        "hard": "Zor",
        "new_case": "🔄 Yeni Vaka Oluştur",
        "please_enter_api": "Lütfen OpenAI API anahtarını girin!",
        "creating_case": "Vaka oluşturuluyor... Lütfen bekleyin...",
        "api_missing": "OpenAI API anahtarı eksik!",
        "case_info": "👤 Hasta Bilgileri",
        "demographic": "Demografik",
        "anamnesis": "Anamnez",
        "physical_exam": "Fizik Muayene",
        "vital_signs": "📊 Vital Bulgular",
        "pulse": "Nabız",
        "blood_pressure": "Tansiyon",
        "temperature": "Ateş",
        "respiration": "Solunum",
        "oxygen": "O₂ Sat",
        "order_tests": "🔬 Tetkik İste",
        "laboratory": "Laboratuvar",
        "imaging": "Görüntüleme",
        "advanced_tests": "İleri Tetkikler",
        "invasive_tests": "İnvaziv Testler",
        "basic_biochem": "Temel Biyokimya ve Hematoloji",
        "hemogram": "Hemogram",
        "crp": "CRP",
        "sedimentation": "Sedimentasyon",
        "biochemistry": "Biyokimya",
        "electrolytes": "Elektrolitler",
        "urinalysis": "Tam İdrar Tetkiki",
        "coagulation": "Koagülasyon",
        "d_dimer": "D-Dimer",
        "blood_gas": "Kan Gazı",
        "cardiac_panel": "Kardiyak Panel",
        "troponin": "Troponin",
        "liver_function": "Karaciğer Fonk.",
        "endocrine_metabolic": "Endokrin ve Metabolik Testler",
        "thyroid_function": "Tiroid Fonk. Testleri",
        "glucose_profile": "Glikoz Profili",
        "lipid_profile": "Lipid Profili",
        "hormone_profile": "Hormon Profili",
        "other_lab_tests": "Diğer Laboratuvar Testleri",
        "rheumatologic": "Romatolojik Testler",
        "iron_profile": "Demir Profili",
        "tumor_markers": "Tümör Belirteçleri",
        "vitamin_b12": "B12 ve Folat",
        "xray_ultrasound": "Grafiler ve Ultrason",
        "ekg": "EKG",
        "chest_xray": "Akciğer Röntgen",
        "abdominal_usg": "Batın USG",
        "echocardiography": "Ekokardiyografi",
        "thyroid_usg": "Tiroid USG",
        "doppler_usg": "Doppler USG",
        "thorax_ct": "Toraks BT",
        "abdominal_ct": "Batın BT",
        "brain_ct": "Beyin BT",
        "brain_mri": "Beyin MR",
        "mri_angiography": "MR Anjiyografi",
        "pet_ct": "PET/CT",
        "other_imaging": "Diğer Görüntüleme Testleri",
        "scintigraphy": "Sintigrafi",
        "mammography": "Mamografi",
        "stress_test": "Efor Testi",
        "holter": "Holter EKG",
        "pulmonary_function": "Solunum Fonk. Testi",
        "eeg": "EEG",
        "emg": "EMG",
        "hepatitis_serology": "Hepatit Serolojisi",
        "ogtt": "OGTT",
        "gastroscopy": "Gastroskopi",
        "colonoscopy": "Kolonoskopi",
        "bronchoscopy": "Bronkoskopi",
        "bone_marrow": "Kemik İliği Biyopsisi",
        "liver_biopsy": "Karaciğer Biyopsisi",
        "kidney_biopsy": "Böbrek Biyopsisi",
        "lumbar_puncture": "Lomber Ponksiyon",
        "blood_culture": "Kan Kültürü",
        "test_results": "📊 Tetkik Sonuçları",
        "parameter": "Parametre",
        "value": "Değer",
        "reference_range": "Referans Aralığı",
        "status": "Durum",
        "normal": "✅ Normal",
        "abnormal": "⚠️ Anormal",
        "diagnosis": "🔍 Tanı",
        "what_diagnosis": "Tanınız nedir?",
        "evaluate_diagnosis": "Tanıyı Değerlendir",
        "evaluating": "Tanı değerlendiriliyor...",
        "congratulations": "✅ Tebrikler! Doğru tanı:",
        "explanation": "Açıklama:",
        "wrong_diagnosis": "❌ Yanlış tanı. Tekrar deneyin.",
        "feedback": "Geri Bildirim:",
        "hint": "💡 İpucu:",
        "show_answer": "Cevabı Göster",
        "correct_diagnosis": "🔍 Doğru tanı:",
        "show_summary": "📝 Vaka Özetini Göster",
        "case_summary": "### 📋 Vaka Özeti",
        "difficulty": "Zorluk",
        "diagnosis_summary": "Tanı",
        "solution_time": "Çözüm Süresi",
        "minute": "dakika",
        "second": "saniye",
        "patient_info": "Hasta Bilgileri",
        "vital_signs_summary": "Vital Bulgular",
        "diagnostic_findings": "Tanıya Yardımcı Bulgular",
        "all_values_normal": "Tüm değerler normal sınırlarda",
        "no_helpful_findings": "Tanıya yardımcı bulgu bulunamadı.",
        "learning_points": "Öğrenme Noktaları",
        "test_prep_notes": "TUS Hazırlık Notları",
        "case_findings": "Bu vakada karşılaştığınız bulgular ve tanı süreci TUS sınavında benzer şekilde sorulabilir. Özellikle laboratuvar değerlerindeki anormallikleri ve bunların klinik bulgularla ilişkisini hatırlayın.",
        "case_summary_for": "Bu vaka özeti, TUS hazırlığı için oluşturulmuştur.",
        "date": "Tarih",
        "print": "🖨️ Yazdır",
        "show_hint": "💡 İpucu Göster",
        "no_more_hints": "Başka ipucu kalmadı!",
        "hint_number": "💡 İpucu #",
        "welcome_title": "# 🩺 Dahiliye Vaka Simülasyonu",
        "welcome_message": "Bu uygulama, dahiliye vakalarında tanı koyma becerinizi geliştirmenize yardımcı olacak bir simülasyon aracıdır.",
        "how_to_use": "### Nasıl Kullanılır:",
        "step1": "1. Yan menüden OpenAI API anahtarınızı girin",
        "step2": "2. Model ve zorluk seviyesini seçin",
        "step3": "3. \"Yeni Vaka Oluştur\" butonuna tıklayın",
        "step4": "4. Hastanın anamnezi ve fizik muayenesini inceleyin",
        "step5": "5. İlgili tetkikleri isteyin",
        "step6": "6. Sonuçları değerlendirip tanınızı yazın",
        "step7": "7. Tanınız doğru olana kadar devam edin",
        "tips": "### İpuçları:",
        "tip1": "- Tanıya götürecek kilit bulguları tespit etmeye çalışın",
        "tip2": "- Gerçek klinik pratikteki gibi sistematik yaklaşın",
        "tip3": "- Zorluk seviyesini kendinize göre ayarlayın",
        "tip4": "- Her istediğiniz test, ilgisiz de olsa sonuç verecektir",
        "start_with_api": "Yan menüden API anahtarınızı girerek başlayın!",
        "useful_features": "### TUS Hazırlığı İçin Faydalı Özellikler:",
        "feature1": "✅ Gerçekçi vaka senaryoları",
        "feature2": "✅ Dahiliye odaklı vaka çeşitliliği",
        "feature3": "✅ 100+ farklı laboratuvar ve görüntüleme tetkiki",
        "feature4": "✅ Ayrıntılı test sonuçları ve raporlar",
        "feature5": "✅ Yapay zeka destekli tanı değerlendirmesi",
        "feature6": "✅ Zorluk seviyesine göre kişisel istatistikler",
        "feature7": "✅ Vaka özeti ve öğrenme noktaları",
        "info_note": "💡 Bu uygulamada, test sonuçları gerçek klinik durumu yansıtmak için detaylı olarak oluşturulmaktadır. Hastanın tanısıyla ilgisiz görünen testler bile sonuç verecektir.",
        "case_timer": "Vaka Çözüm Süresi",
        "language": "🌐 Dil / Language",
        "error_case_creation": "Vaka oluşturulurken hata oluştu"
    },
    "en": {
        "app_title": "Internal Medicine Case Simulation",
        "api_settings": "API Settings",
        "api_key": "OpenAI API Key",
        "model_selection": "Model Selection",
        "difficulty_level": "Difficulty Level",
        "easy": "Easy",
        "medium": "Medium",
        "hard": "Hard",
        "new_case": "🔄 Create New Case",
        "please_enter_api": "Please enter your OpenAI API key!",
        "creating_case": "Creating case... Please wait...",
        "api_missing": "OpenAI API key is missing!",
        "case_info": "👤 Patient Information",
        "demographic": "Demographics",
        "anamnesis": "History",
        "physical_exam": "Physical Examination",
        "vital_signs": "📊 Vital Signs",
        "pulse": "Pulse",
        "blood_pressure": "Blood Pressure",
        "temperature": "Temperature",
        "respiration": "Respiration",
        "oxygen": "O₂ Sat",
        "order_tests": "🔬 Order Tests",
        "laboratory": "Laboratory",
        "imaging": "Imaging",
        "advanced_tests": "Advanced Tests",
        "invasive_tests": "Invasive Tests",
        "basic_biochem": "Basic Biochemistry and Hematology",
        "hemogram": "Complete Blood Count",
        "crp": "CRP",
        "sedimentation": "ESR",
        "biochemistry": "Biochemistry",
        "electrolytes": "Electrolytes",
        "urinalysis": "Urinalysis",
        "coagulation": "Coagulation",
        "d_dimer": "D-Dimer",
        "blood_gas": "Blood Gas",
        "cardiac_panel": "Cardiac Panel",
        "troponin": "Troponin",
        "liver_function": "Liver Function",
        "endocrine_metabolic": "Endocrine and Metabolic Tests",
        "thyroid_function": "Thyroid Function Tests",
        "glucose_profile": "Glucose Profile",
        "lipid_profile": "Lipid Profile",
        "hormone_profile": "Hormone Profile",
        "other_lab_tests": "Other Laboratory Tests",
        "rheumatologic": "Rheumatological Tests",
        "iron_profile": "Iron Profile",
        "tumor_markers": "Tumor Markers",
        "vitamin_b12": "B12 and Folate",
        "xray_ultrasound": "X-rays and Ultrasound",
        "ekg": "ECG",
        "chest_xray": "Chest X-ray",
        "abdominal_usg": "Abdominal USG",
        "echocardiography": "Echocardiography",
        "thyroid_usg": "Thyroid USG",
        "doppler_usg": "Doppler USG",
        "thorax_ct": "Thorax CT",
        "abdominal_ct": "Abdominal CT",
        "brain_ct": "Brain CT",
        "brain_mri": "Brain MRI",
        "mri_angiography": "MRI Angiography",
        "pet_ct": "PET/CT",
        "other_imaging": "Other Imaging Tests",
        "scintigraphy": "Scintigraphy",
        "mammography": "Mammography",
        "stress_test": "Stress Test",
        "holter": "Holter ECG",
        "pulmonary_function": "Pulmonary Function Test",
        "eeg": "EEG",
        "emg": "EMG",
        "hepatitis_serology": "Hepatitis Serology",
        "ogtt": "OGTT",
        "gastroscopy": "Gastroscopy",
        "colonoscopy": "Colonoscopy",
        "bronchoscopy": "Bronchoscopy",
        "bone_marrow": "Bone Marrow Biopsy",
        "liver_biopsy": "Liver Biopsy",
        "kidney_biopsy": "Kidney Biopsy",
        "lumbar_puncture": "Lumbar Puncture",
        "blood_culture": "Blood Culture",
        "test_results": "📊 Test Results",
        "parameter": "Parameter",
        "value": "Value",
        "reference_range": "Reference Range",
        "status": "Status",
        "normal": "✅ Normal",
        "abnormal": "⚠️ Abnormal",
        "diagnosis": "🔍 Diagnosis",
        "what_diagnosis": "What is your diagnosis?",
        "evaluate_diagnosis": "Evaluate Diagnosis",
        "evaluating": "Evaluating diagnosis...",
        "congratulations": "✅ Congratulations! Correct diagnosis:",
        "explanation": "Explanation:",
        "wrong_diagnosis": "❌ Wrong diagnosis. Try again.",
        "feedback": "Feedback:",
        "hint": "💡 Hint:",
        "show_answer": "Show Answer",
        "correct_diagnosis": "🔍 Correct diagnosis:",
        "show_summary": "📝 Show Case Summary",
        "case_summary": "### 📋 Case Summary",
        "difficulty": "Difficulty",
        "diagnosis_summary": "Diagnosis",
        "solution_time": "Solution Time",
        "minute": "minute",
        "second": "second",
        "patient_info": "Patient Information",
        "vital_signs_summary": "Vital Signs",
        "diagnostic_findings": "Diagnostic Findings",
        "all_values_normal": "All values within normal range",
        "no_helpful_findings": "No diagnostic findings available.",
        "learning_points": "Learning Points",
        "test_prep_notes": "Exam Preparation Notes",
        "case_findings": "The findings and diagnostic process in this case may be tested in similar ways in medical exams. Pay special attention to the abnormalities in laboratory values and their correlation with clinical findings.",
        "case_summary_for": "This case summary was created for medical exam preparation.",
        "date": "Date",
        "print": "🖨️ Print",
        "show_hint": "💡 Show Hint",
        "no_more_hints": "No more hints available!",
        "hint_number": "💡 Hint #",
        "welcome_title": "# 🩺 Internal Medicine Case Simulation",
        "welcome_message": "This application is a simulation tool to help you improve your diagnostic skills in internal medicine cases.",
        "how_to_use": "### How to Use:",
        "step1": "1. Enter your OpenAI API key in the sidebar",
        "step2": "2. Select model and difficulty level",
        "step3": "3. Click the \"Create New Case\" button",
        "step4": "4. Review the patient's history and physical examination",
        "step5": "5. Order relevant tests",
        "step6": "6. Evaluate the results and submit your diagnosis",
        "step7": "7. Continue until your diagnosis is correct",
        "tips": "### Tips:",
        "tip1": "- Try to identify key findings that lead to the diagnosis",
        "tip2": "- Use a systematic approach as in real clinical practice",
        "tip3": "- Adjust the difficulty level to suit your needs",
        "tip4": "- Every test you order will give a result, even if not relevant",
        "start_with_api": "Start by entering your API key in the sidebar!",
        "useful_features": "### Useful Features for Medical Exam Preparation:",
        "feature1": "✅ Realistic case scenarios",
        "feature2": "✅ Internal medicine focused case variety",
        "feature3": "✅ 100+ different laboratory and imaging tests",
        "feature4": "✅ Detailed test results and reports",
        "feature5": "✅ AI-powered diagnosis evaluation",
        "feature6": "✅ Personal statistics based on difficulty level",
        "feature7": "✅ Case summary and learning points",
        "info_note": "💡 In this application, test results are created in detail to reflect the real clinical situation. Even tests that seem irrelevant to the patient's diagnosis will provide results.",
        "case_timer": "Case Solution Time",
        "language": "🌐 Dil / Language",
        "error_case_creation": "Error creating case"
    }
}

# Metinleri çevirmek için yardımcı fonksiyon
def t(key):
    """Seçilen dile göre çevrilmiş metni döndürür"""
    return translations[st.session_state.language].get(key, key)


# Oturum durum değişkenlerini tanımla
if 'language' not in st.session_state:
    st.session_state.language = "tr"  # Varsayılan dil Türkçe

if 'new_case' not in st.session_state:
    st.session_state.new_case = False

if 'case_created' not in st.session_state:
    st.session_state.case_created = False

if 'case_data' not in st.session_state:
    st.session_state.case_data = None

if 'tests_performed' not in st.session_state:
    st.session_state.tests_performed = {}

if 'diagnosis_feedback' not in st.session_state:
    st.session_state.diagnosis_feedback = None

if 'diagnosis_correct' not in st.session_state:
    st.session_state.diagnosis_correct = False

if 'hint_count' not in st.session_state:
    st.session_state.hint_count = 0
    
if 'case_history' not in st.session_state:
    st.session_state.case_history = []
    
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

if 'start_time' not in st.session_state:
    st.session_state.start_time = None
    
if 'elapsed_time' not in st.session_state:
    st.session_state.elapsed_time = 0
    
if 'stats' not in st.session_state:
    st.session_state.stats = {
        "total_cases": 0,
        "solved_cases": 0,
        "success_rate": 0,
        "avg_attempts": 0,
        "by_difficulty": {"Kolay": {"total": 0, "solved": 0}, "Orta": {"total": 0, "solved": 0}, "Zor": {"total": 0, "solved": 0}}
    }

# Yardımcı fonksiyonlar
def generate_report_date():
    """Rapor tarihi oluşturur"""
    days_ago = random.randint(0, 5)
    report_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
    return report_date.strftime("%d.%m.%Y %H:%M")

def create_timer_component():
    if st.session_state.start_time is not None:
        current_time = time.time()
        elapsed = current_time - st.session_state.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        
        # Kronometre HTML bileşeni
        st.markdown(f"""
        <div style="background-color: #f0f0f0; border-radius: 10px; padding: 10px; margin-bottom: 20px; text-align: center;">
            <h4 style="margin: 0; color: #333;">{t('case_timer')}</h4>
            <div style="font-size: 24px; font-weight: bold; color: #e74c3c;">
                {minutes:02d}:{seconds:02d}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sayfayı her 1 saniyede bir yenile (otomatik sayaç için)
        st.markdown("""
        <script>
            setTimeout(function(){
                window.location.reload();
            }, 1000);
        </script>
        """, unsafe_allow_html=True)


# OpenAI ile vaka oluşturma fonksiyonu
def create_enhanced_case(api_key, model, difficulty):
    """OpenAI API kullanarak yeni bir vaka oluşturur - Çok dilli ve genişletilmiş test seçenekleri ile"""
    openai.api_key = api_key
    
    # Dilin İngilizce olup olmadığını kontrol et
    is_english = st.session_state.language == "en"
    
    # Zorluk seviyesi çevirisi
    if is_english:
        difficulty_map = {"Kolay": "Easy", "Orta": "Medium", "Zor": "Hard"}
        difficulty_text = difficulty_map.get(difficulty, difficulty)
    else:
        difficulty_text = difficulty
    
    # Rastgele bir tıbbi sistem/kategori seç
    medical_systems = [
        "cardiovascular", "respiratory", "gastrointestinal", "renal", "neurological", 
        "endocrine", "hematologic", "rheumatologic", "infectious", "metabolic", 
        "dermatologic", "psychiatric", "oncologic", "immunologic", "geriatric"
    ]
    random_system = random.choice(medical_systems)
    
    # Sık görülen vakaları dışlama listesi
    if is_english:
        excluded_cases = [
            "Infective endocarditis", "Liver abscess", "Acute Pancreatitis", "Diabetic ketoacidosis",
            "Hypothyroidism", "Pulmonary embolism", "Systemic Lupus Erythematosus", "Gout", 
            "Portal hypertension", "Acute renal failure", "Urinary tract infection", 
            "Rheumatoid arthritis", "Pneumonia", "COPD exacerbation", "Myocardial infarction"
        ]
    else:
        excluded_cases = [
            "Enfektif endokardit", "Karaciğer absesi", "Akut Pankreatit", "Diyabetik ketoasidoz",
            "Hipotiroidi", "Pulmoner emboli", "Sistemik Lupus Eritematozus", "Gut", 
            "Portal hipertansiyon", "Akut böbrek yetmezliği", "Üriner sistem enfeksiyonu",
            "Romatoid artrit", "Pnömoni", "KOAH alevlenmesi", "Miyokard enfarktüsü"
        ]
    
    # Sistem mesajı ve prompt dilini ayarla
    if is_english:
        # İngilizce JSON şablonu - true/false değerleri sabit olarak atanmış
        english_json_template = '''
{
    "case_name": "Case title",
    "demographic": "Age, gender, occupation, etc.",
    "history": "Patient's history and complaints",
    "physical_examination": "Physical examination findings",
    "vital_signs": {
        "pulse": "Value (normal range)",
        "blood_pressure": "Value (normal range)",
        "temperature": "Value (normal range)",
        "respiratory_rate": "Value (normal range)",
        "oxygen_saturation": "Value (normal range)"
    },
    "correct_diagnosis": "Correct diagnosis of the case",
    "difficulty": "DIFFICULTY_PLACEHOLDER",
    "tests": {
        "cbc": {
            "relevance": "Relevant/Irrelevant",
            "results": [
                {"parameter": "WBC", "value": "Value", "reference": "Normal range", "abnormal": true},
                {"parameter": "RBC", "value": "Value", "reference": "Normal range", "abnormal": false}
            ]
        },
        "biochemistry": {
            "relevance": "Relevant/Irrelevant",
            "results": []
        }
    },
    "hints": [
        "Hint 1",
        "Hint 2",
        "Hint 3"
    ]
}
'''.replace("DIFFICULTY_PLACEHOLDER", difficulty_text)

        system_message = """You are a medical education expert who creates realistic and educational internal medicine cases.
IMPORTANT: 
1. Generate completely original cases that are different from any examples provided in the prompt
2. Ensure consistency between clinical symptoms, physical exam findings, and laboratory/imaging results
3. Be creative yet medically accurate - all lab values and findings should reflect real medical conditions"""

        prompt = f"""
        Create an original internal medicine patient case related to the {random_system} system. Difficulty level: {difficulty_text}
        
        VERY IMPORTANT: 
        1. Your case should NOT be any of these common diagnoses: {", ".join(excluded_cases)}
        2. This case will be used to develop real clinical scenario recognition skills for medical students
        3. Create a completely unique case with an interesting presentation
        4. Ensure complete consistency between the clinical presentation and test results
        
        The case should have the following characteristics:
        1. Detailed patient history, demographic information, complaints, and physical examination that introduce the patient and guide towards the diagnosis
        2. A clear correct diagnosis that is NOT one of the excluded cases listed above
        3. All tests and findings supporting the diagnosis should be consistent with each other
        4. Laboratory and imaging findings consistent with disease pathogenesis and clinical course
        
        FINDINGS IN TESTS RELATED TO DIAGNOSIS - CRITICAL POINT:
        If a test is marked "relevance": "Relevant", then that test's results must show abnormalities related to the diagnosis. The following examples are only for REFERENCE - DO NOT create cases with these exact diagnoses:
        
        * Example 1: Infective endocarditis → Microbiological growth in blood culture and vegetation on Echo
        * Example 2: Liver abscess → "Hypodense lesion" or "cystic formation" on USG and elevated CRP/WBC
        * Example 3: Pancreatitis → Elevated lipase/amylase and "pancreatic edema" on CT
        * Example 4: Hypothyroidism → Low fT3/fT4, high TSH, and "thyroiditis" findings on thyroid USG
        
        IN IMAGING TESTS:
        Imaging reports should clearly state pathological findings specific to the diagnosis. For example:
        * On chest X-ray → "Consolidation area in the right middle lobe"
        * On abdominal USG → "Multiple stones in the gallbladder and wall thickening"
        * On thorax CT → "Ground glass opacities and consolidation in the left lower lobe"
        
        IN LABORATORY TESTS:
        In laboratory results, each abnormal result should be marked as "abnormal": true and the values should be outside the reference range. For example:
        * Leukocytosis → WBC: "15.2 x10^3/μL", "reference": "4.5-11.0 x10^3/μL", "abnormal": true
        * Hyperglycemia → Glucose: "320 mg/dL", "reference": "70-100 mg/dL", "abnormal": true
        
        Return in JSON format. The format should be as follows:
        
        ```json
{english_json_template}
        ```
        
        FINAL CHECK:
        1. Make sure your case is NOT one of the excluded diagnoses
        2. Make sure all relevant tests have abnormal findings related to the diagnosis
        3. Imaging studies should contain specific pathological findings related to the diagnosis
        4. There should be consistency between tests
        5. Make sure abnormal values are marked as "abnormal": true
        6. Hints should be arranged from simple to complex on the path to diagnosis
        """
    else:
        # Türkçe JSON şablonu - true/false değerleri sabit olarak atanmış
        turkish_json_template = '''
{
    "vaka_adi": "Vaka başlığı",
    "demografik": "Yaş, cinsiyet, meslek, vb.",
    "anamnez": "Hastanın hikayesi ve şikayetleri",
    "fizik_muayene": "Fizik muayene bulguları",
    "vital_bulgular": {
        "nabiz": "Değer (normal aralık)",
        "tansiyon": "Değer (normal aralık)",
        "ates": "Değer (normal aralık)",
        "solunum_sayisi": "Değer (normal aralık)",
        "oksijen_saturasyonu": "Değer (normal aralık)"
    },
    "dogru_tani": "Vakanın doğru tanısı",
    "zorluk": "DIFFICULTY_PLACEHOLDER",
    "testler": {
        "hemogram": {
            "relevance": "İlgili/İlgisiz",
            "results": [
                {"parameter": "WBC", "value": "Değer", "reference": "Normal aralık", "abnormal": true},
                {"parameter": "RBC", "value": "Değer", "reference": "Normal aralık", "abnormal": false}
            ]
        },
        "biyokimya": {
            "relevance": "İlgili/İlgisiz",
            "results": []
        }
    },
    "ipuclari": [
        "İpucu 1",
        "İpucu 2",
        "İpucu 3"
    ]
}
'''.replace("DIFFICULTY_PLACEHOLDER", difficulty_text)

        # Türkçe'de tıbbi sistem adları
        tr_system_mapping = {
            "cardiovascular": "kardiyovasküler", 
            "respiratory": "solunum",
            "gastrointestinal": "gastrointestinal",
            "renal": "renal/böbrek", 
            "neurological": "nörolojik",
            "endocrine": "endokrin", 
            "hematologic": "hematolojik", 
            "rheumatologic": "romatolojik",
            "infectious": "enfeksiyon", 
            "metabolic": "metabolik",
            "dermatologic": "dermatolojik", 
            "psychiatric": "psikiyatrik", 
            "oncologic": "onkolojik",
            "immunologic": "immünolojik", 
            "geriatric": "geriatrik"
        }
        tr_system = tr_system_mapping.get(random_system, random_system)

        system_message = """Siz gerçekçi ve eğitici dahiliye vakaları oluşturan bir tıp eğitimi uzmanısınız.
ÖNEMLİ: 
1. Verilen örneklerden tamamen farklı özgün vakalar üretin
2. Klinik semptomlar, fizik muayene bulguları ve laboratuvar/görüntüleme sonuçları arasında tutarlılık sağlayın
3. Yaratıcı ancak tıbbi olarak doğru vakalar oluşturun - tüm laboratuvar değerleri ve bulgular gerçek tıbbi durumları yansıtmalıdır"""

        prompt = f"""
        {tr_system} sistemiyle ilgili özgün bir dahiliye vakası oluştur. Zorluk seviyesi: {difficulty_text}
        
        ÇOK ÖNEMLİ: 
        1. Vakan şu yaygın tanılardan HİÇBİRİ olmasın: {", ".join(excluded_cases)}
        2. Bu vaka, TUS öğrencilerinin gerçek klinik senaryoları tanıma becerilerini geliştirmek için kullanılacaktır
        3. İlgi çekici bir sunumla tamamen özgün bir vaka oluştur
        4. Klinik tablo ve tetkik sonuçları arasında tam bir uyum olmalıdır
        
        Vaka şu özelliklere sahip olmalıdır:
        1. Hastanın hikayesi, demografik bilgileri, şikayetleri ve fizik muayenesi gibi hastayı tanıtacak bilgiler detaylı ve tanıya yönlendirici şekilde olmalı
        2. Yukarıda listelenen dışlanmış vakalardan biri OLMAYAN net bir doğru tanı içermeli
        3. Tanıyı destekleyen tüm tetkikler ve bulgular birbiriyle uyumlu olmalı
        4. Hastalık patogenezine ve klinik seyre uygun laboratuvar ve görüntüleme bulguları içermeli
        
        TEŞHİS İLE İLGİLİ TESTLERDEKİ BULGULAR - KRİTİK NOKTA:
        Bir testin "relevance": "İlgili" olarak işaretlendiyse, o testin sonuçlarında mutlaka tanıyla ilişkili anormallikler olmalıdır. Aşağıdaki örnekler SADECE REFERANS içindir - bu tanılarla aynı vakaları OLUŞTURMAYIN:
        
        * Örnek 1: Enfektif endokardit → Kan kültüründe mikrobiyolojik üreme ve EKO'da vejetasyon
        * Örnek 2: Karaciğer absesi → USG'de "hipodens lezyon" veya "kistik oluşum" ve CRP/WBC yüksekliği
        * Örnek 3: Pankreatit → Lipaz/amilaz yüksekliği ve BT'de "pankreasta ödem"
        * Örnek 4: Hipotiroidi → Düşük sT3/sT4, yüksek TSH ve tiroid USG'de "tiroidit" bulguları
        
        GÖRÜNTÜLEMEDEKİ BULGULAR:
        Görüntüleme raporları, tanıya özgü patolojik bulguları açıkça belirtmelidir. Örneğin:
        * Akciğer röntgeninde → "Sağ orta lobda konsolidasyon alanı"
        * Batın USG'de → "Safra kesesinde çoklu taşlar ve duvar kalınlaşması"
        * Toraks BT'de → "Sol alt lobda buzlu cam opasiteleri ve konsolidasyon"
        
        LABORATUVAR TESTLERİNDE:
        Laboratuvar sonuçlarında, her anormal sonuç "abnormal": true olarak işaretlenmeli ve değerler referans aralığının dışında olmalıdır. Örneğin:
        * Lökositoz → WBC: "15.2 x10^3/μL", "reference": "4.5-11.0 x10^3/μL", "abnormal": true
        * Hiperglisemi → Glikoz: "320 mg/dL", "reference": "70-100 mg/dL", "abnormal": true
        
        JSON formatında döndür. Formatı aşağıdaki gibi olsun:
        
        ```json
{turkish_json_template}
        ```
        
        SON KONTROL:
        1. Vakanın dışlanmış tanılardan biri OLMADIĞINDAN emin ol
        2. İlgili tüm testlerde tanıyla ilişkili anormal bulgular olduğundan emin ol
        3. Görüntüleme tetkiklerinde tanıya özgü spesifik patolojik bulgular içermeli
        4. Testler arası tutarlılık olmalı
        5. Anormal değerlerin "abnormal": true olarak işaretlendiğinden emin ol
        6. İpuçları tanıya giden yolda basitten karmaşığa doğru dizilmiş olmalı
        """
    
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9  # Daha yüksek çeşitlilik için temperature artırıldı
        )
        
        content = response.choices[0].message.content
        
        # JSON içeriğini çıkar
        json_str = content.split("```json")[1].split("```")[0] if "```json" in content else content
        
        # JSON temizleme
        json_str = json_str.strip()
        case_data = json.loads(json_str)
        
        # İngilizce-Türkçe alan adı dönüşümü
        if is_english:
            # İngilizce formatı Türkçe API'ye uyumlu hale getir
            mapped_data = {
                "vaka_adi": case_data.get("case_name", ""),
                "demografik": case_data.get("demographic", ""),
                "anamnez": case_data.get("history", ""),
                "fizik_muayene": case_data.get("physical_examination", ""),
                "vital_bulgular": {
                    "nabiz": case_data["vital_signs"].get("pulse", ""),
                    "tansiyon": case_data["vital_signs"].get("blood_pressure", ""),
                    "ates": case_data["vital_signs"].get("temperature", ""),
                    "solunum_sayisi": case_data["vital_signs"].get("respiratory_rate", ""),
                    "oksijen_saturasyonu": case_data["vital_signs"].get("oxygen_saturation", "")
                },
                "dogru_tani": case_data.get("correct_diagnosis", ""),
                "zorluk": case_data.get("difficulty", difficulty_text),
                "testler": {},
                "ipuclari": case_data.get("hints", [])
            }
            
            # Test adı dönüşümleri
            test_name_mapping = {
                "cbc": "hemogram",
                "biochemistry": "biyokimya",
                "urinalysis": "tam_idrar_tetkiki",
                "crp": "crp",
                "esr": "sedimentasyon",
                "coagulation": "koagulasyon",
                "d_dimer": "d_dimer",
                "blood_gas": "kan_gazi",
                "cardiac_panel": "kardiyak_panel",
                "troponin": "troponin",
                "liver_function": "karaciger_fonksiyon_testleri",
                "thyroid_function": "tiroid_fonksiyon_testleri",
                "glucose_profile": "glikoz_profili",
                "lipid_profile": "lipid_profili",
                "hormone_profile": "hormon_profili",
                "rheumatologic": "romatolojik_testler",
                "iron_profile": "iron_profili",
                "tumor_markers": "tumor_belirtecleri",
                "vitamin_b12": "vitamin_b12_folat",
                "ecg": "ekg",
                "chest_xray": "akciger_rontgen",
                "abdominal_usg": "batin_usg",
                "echocardiography": "ekokardiyografi",
                "thyroid_usg": "tiroid_usg",
                "doppler_usg": "doppler_usg",
                "thorax_ct": "toraks_bt",
                "abdominal_ct": "batin_bt",
                "brain_ct": "beyin_bt",
                "brain_mri": "beyin_mr",
                "mri_angiography": "mr_anjiografi",
                "pet_ct": "pet_ct",
                "scintigraphy": "sintigrafi",
                "mammography": "mamografi",
                "stress_test": "efor_testi",
                "holter_ecg": "holter_ekg",
                "pulmonary_function": "solunum_fonksiyon_testi",
                "eeg": "eeg",
                "emg": "emg",
                "hepatitis_serology": "hepatit_serolojisi",
                "ogtt": "ogtt",
                "gastroscopy": "gastroskopi",
                "colonoscopy": "kolonoskopi",
                "bronchoscopy": "bronkoskopi",
                "bone_marrow_biopsy": "kemik_iligi_biyopsisi",
                "liver_biopsy": "karaciger_biyopsisi",
                "kidney_biopsy": "bobrek_biyopsisi",
                "lumbar_puncture": "lomber_ponksiyon",
                "blood_culture": "kan_kulturu"
            }
            
            # Testleri dönüştür
            for eng_test_name, test_data in case_data.get("tests", {}).items():
                tr_test_name = test_name_mapping.get(eng_test_name, eng_test_name)
                
                # Relevance değerini çevir
                relevance = "İlgili" if test_data.get("relevance", "").lower() == "relevant" else "İlgisiz"
                
                test_entry = {
                    "relevance": relevance,
                }
                
                # Sonuçları da ekle
                if "results" in test_data:
                    test_entry["results"] = test_data["results"]
                elif "result" in test_data:
                    test_entry["result"] = test_data["result"]
                
                mapped_data["testler"][tr_test_name] = test_entry
            
            return mapped_data
        else:
            # Türkçe format zaten uyumlu
            return case_data
    except Exception as e:
        st.error(f"{t('error_case_creation')}: {str(e)}")
        return None
# Tanı değerlendirme fonksiyonu
def get_ai_feedback(api_key, model, case_data, diagnosis):
    """Kullanıcının tanısını değerlendirir - çok dilli"""
    openai.api_key = api_key
    
    # Dilin İngilizce olup olmadığını kontrol et
    is_english = st.session_state.language == "en"
    
    # Doğru tanı bilgisini al
    if is_english:
        correct_diagnosis = case_data.get('dogru_tani', '')  # Türkçe anahtar kullanılıyor çünkü veri yapısı hala Türkçe
        prompt = f"""
        The correct diagnosis for this patient is:
        {correct_diagnosis}
        
        The diagnosis provided by the student:
        {diagnosis}
        
        How accurate is this diagnosis? If correct, explain why it is correct. If incorrect, explain the differences between the student's diagnosis and the actual diagnosis, and point out the findings they may have overlooked.
        
        Return your response in the following format:
        
        ```json
        {{
            "correct": true or false,
            "explanation": "Explanation and feedback about the diagnosis",
            "hint": "A hint to help the student (if the diagnosis is incorrect)"
        }}
        ```
        """
        system_message = "You are a medical professor evaluating a medical student's case diagnosis."
    else:
        correct_diagnosis = case_data.get('dogru_tani', '')
        prompt = f"""
        Aşağıdaki hastanın gerçek tanısı:
        {correct_diagnosis}
        
        Öğrenci tarafından verilen tanı:
        {diagnosis}
        
        Bu tanı ne kadar doğru? Doğru ise, neden doğru olduğunu belirt. Yanlış ise, öğrencinin tanısı ile gerçek tanı arasındaki farkları ve göz ardı ettiği bulguları açıkla.
        
        Yanıtını şu formatta döndür:
        
        ```json
        {{
            "dogru_mu": true veya false,
            "aciklama": "Tanı hakkında açıklama ve geri bildirim",
            "ipucu": "Öğrenciye yardımcı olacak bir ipucu (eğer tanı yanlışsa)"
        }}
        ```
        """
        system_message = "Siz bir tıp profesörüsünüz ve bir TUS öğrencisinin vaka tanısını değerlendiriyorsunuz."
    
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        content = response.choices[0].message.content
        
        # JSON içeriğini çıkar
        json_str = content.split("```json")[1].split("```")[0] if "```json" in content else content
        
        # JSON temizleme
        json_str = json_str.strip()
        feedback_data = json.loads(json_str)
        
        # İngilizce Türkçe alan adı dönüşümü
        if is_english:
            if "correct" in feedback_data:
                # İngilizce yanıtı Türkçe formatla eşleştir
                mapped_data = {
                    "dogru_mu": feedback_data.get("correct", False),
                    "aciklama": feedback_data.get("explanation", ""),
                    "ipucu": feedback_data.get("hint", "")
                }
                return mapped_data
            else:
                return feedback_data
        else:
            return feedback_data
    except Exception as e:
        error_msg = "Error evaluating diagnosis" if is_english else "Tanı değerlendirirken hata oluştu"
        st.error(f"{error_msg}: {str(e)}")
        if is_english:
            return {"dogru_mu": False, "aciklama": "Evaluation could not be performed.", "ipucu": "Please try again."}
        else:
            return {"dogru_mu": False, "aciklama": "Değerlendirme yapılamadı.", "ipucu": "Tekrar deneyin."}
        
# Vaka özeti oluşturma fonksiyonu
def create_case_summary(case_data, tests_performed):
    """Vaka özeti oluşturur - çok dilli"""
    st.markdown(t("case_summary"))
    
    # Geçen süreyi biçimlendir
    elapsed_time = st.session_state.elapsed_time
    elapsed_minutes = int(elapsed_time // 60)
    elapsed_seconds = int(elapsed_time % 60)
    
    # Seçili dile göre zaman formatı
    if st.session_state.language == "en":
        time_str = f"{elapsed_minutes} {t('minute')} {elapsed_seconds} {t('second')}"
    else:
        time_str = f"{elapsed_minutes} {t('minute')} {elapsed_seconds} {t('second')}"
    
    # Vaka adı ve tanı bilgisini doğru dilden al
    if st.session_state.language == "en":
        case_title = case_data.get('vaka_adi', '')  # Veri yapısı hala Türkçe
        diagnosis = case_data.get('dogru_tani', '')
        difficulty = case_data.get('zorluk', '')
        
        # Zorluk seviyesini İngilizce'ye çevir
        difficulty_map = {"Kolay": "Easy", "Orta": "Medium", "Zor": "Hard"}
        difficulty = difficulty_map.get(difficulty, difficulty)
        
        demographic = case_data.get('demografik', '')
        history = case_data.get('anamnez', '')
        physical_exam = case_data.get('fizik_muayene', '')
        
        # Vital bulguları al
        vitals = {
            "pulse": case_data['vital_bulgular'].get('nabiz', ''),
            "blood_pressure": case_data['vital_bulgular'].get('tansiyon', ''),
            "temperature": case_data['vital_bulgular'].get('ates', ''),
            "respiratory_rate": case_data['vital_bulgular'].get('solunum_sayisi', ''),
            "oxygen_saturation": case_data['vital_bulgular'].get('oksijen_saturasyonu', '')
        }
        
        hints = case_data.get('ipuclari', [])
    else:
        # Türkçe için doğrudan al
        case_title = case_data.get('vaka_adi', '')
        diagnosis = case_data.get('dogru_tani', '')
        difficulty = case_data.get('zorluk', '')
        demographic = case_data.get('demografik', '')
        history = case_data.get('anamnez', '')
        physical_exam = case_data.get('fizik_muayene', '')
        
        # Vital bulguları al
        vitals = {
            "pulse": case_data['vital_bulgular'].get('nabiz', ''),
            "blood_pressure": case_data['vital_bulgular'].get('tansiyon', ''),
            "temperature": case_data['vital_bulgular'].get('ates', ''),
            "respiratory_rate": case_data['vital_bulgular'].get('solunum_sayisi', ''),
            "oxygen_saturation": case_data['vital_bulgular'].get('oksijen_saturasyonu', '')
        }
        
        hints = case_data.get('ipuclari', [])
    
    summary_html = f"""
    <div style="font-family: Arial, sans-serif; background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
        <h3 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">{case_title}</h3>
        <p><strong>{t('difficulty')}:</strong> {difficulty}</p>
        <p><strong>{t('diagnosis_summary')}:</strong> {diagnosis}</p>
        <p><strong>{t('solution_time')}:</strong> {time_str}</p>
        
        <hr>
        
        <h4 style="color: #2c3e50;">{t('patient_info')}</h4>
        <p><strong>{t('demographic')}:</strong> {demographic}</p>
        <p><strong>{t('anamnesis')}:</strong> {history}</p>
        <p><strong>{t('physical_exam')}:</strong> {physical_exam}</p>
        
        <h4 style="color: #2c3e50;">{t('vital_signs_summary')}</h4>
        <ul>
            <li><strong>{t('pulse')}:</strong> {vitals['pulse']}</li>
            <li><strong>{t('blood_pressure')}:</strong> {vitals['blood_pressure']}</li>
            <li><strong>{t('temperature')}:</strong> {vitals['temperature']}</li>
            <li><strong>{t('respiration')}:</strong> {vitals['respiratory_rate']}</li>
            <li><strong>{t('oxygen')}:</strong> {vitals['oxygen_saturation']}</li>
        </ul>
        
        <h4 style="color: #2c3e50;">{t('diagnostic_findings')}</h4>
    """
    
    # İstenen testlerden tanıya yardımcı olanları listele
    relevant_tests = []
    for test_name, test_data in case_data['testler'].items():
        if test_data.get('relevance', '') == 'İlgili':
            relevant_tests.append(test_name)
    
    if relevant_tests:
        summary_html += "<ul>"
        for test_name in relevant_tests:
            test_data = case_data['testler'][test_name]
            
            # Test adını doğru dile çevir
            if st.session_state.language == "en":
                # Türkçe -> İngilizce test adı dönüşümü
                test_name_map = {
                    "hemogram": "Complete Blood Count",
                    "biyokimya": "Biochemistry",
                    "tam_idrar_tetkiki": "Urinalysis",
                    "crp": "CRP",
                    "sedimentasyon": "ESR",
                    "koagulasyon": "Coagulation",
                    "d_dimer": "D-Dimer",
                    "kan_gazi": "Blood Gas",
                    "kardiyak_panel": "Cardiac Panel",
                    "troponin": "Troponin",
                    "karaciger_fonksiyon_testleri": "Liver Function Tests",
                    "tiroid_fonksiyon_testleri": "Thyroid Function Tests",
                    "glikoz_profili": "Glucose Profile",
                    "lipid_profili": "Lipid Profile",
                    "hormon_profili": "Hormone Profile",
                    "romatolojik_testler": "Rheumatological Tests",
                    "iron_profili": "Iron Profile",
                    "tumor_belirtecleri": "Tumor Markers",
                    "vitamin_b12_folat": "Vitamin B12 and Folate",
                    "ekg": "ECG",
                    "akciger_rontgen": "Chest X-ray",
                    "batin_usg": "Abdominal USG",
                    "ekokardiyografi": "Echocardiography",
                    "tiroid_usg": "Thyroid USG",
                    "doppler_usg": "Doppler USG",
                    "toraks_bt": "Thorax CT",
                    "batin_bt": "Abdominal CT",
                    "beyin_bt": "Brain CT",
                    "beyin_mr": "Brain MRI",
                    "mr_anjiografi": "MRI Angiography",
                    "pet_ct": "PET/CT",
                    "sintigrafi": "Scintigraphy",
                    "mamografi": "Mammography",
                    "efor_testi": "Stress Test",
                    "holter_ekg": "Holter ECG",
                    "solunum_fonksiyon_testi": "Pulmonary Function Test",
                    "eeg": "EEG",
                    "emg": "EMG",
                    "hepatit_serolojisi": "Hepatitis Serology",
                    "ogtt": "OGTT",
                    "gastroskopi": "Gastroscopy",
                    "kolonoskopi": "Colonoscopy",
                    "bronkoskopi": "Bronchoscopy",
                    "kemik_iligi_biyopsisi": "Bone Marrow Biopsy",
                    "karaciger_biyopsisi": "Liver Biopsy",
                    "bobrek_biyopsisi": "Kidney Biopsy",
                    "lomber_ponksiyon": "Lumbar Puncture",
                    "kan_kulturu": "Blood Culture"
                }
                displayed_test_name = test_name_map.get(test_name, test_name.replace('_', ' ').title())
            else:
                displayed_test_name = test_name.replace('_', ' ').title()
            
            summary_html += f"<li><strong>{displayed_test_name}:</strong> "
            
            if "results" in test_data:
                abnormal_results = []
                for result in test_data["results"]:
                    if result.get("abnormal", False):
                        abnormal_results.append(f"{result['parameter']}: {result['value']} ({result['reference']})")
                
                if abnormal_results:
                    summary_html += "<ul>"
                    for result in abnormal_results:
                        summary_html += f"<li>{result}</li>"
                    summary_html += "</ul>"
                else:
                    summary_html += t("all_values_normal")
            else:
                summary_html += f"{test_data.get('result', '')}"
            
            summary_html += "</li>"
        summary_html += "</ul>"
    else:
        summary_html += f"<p>{t('no_helpful_findings')}</p>"
    
    summary_html += f"""
        <h4 style="color: #2c3e50;">{t('learning_points')}</h4>
        <ul>
    """
    
    # İpuçlarını öğrenme noktaları olarak ekle
    if hints:
        for hint in hints:
            summary_html += f"<li>{hint}</li>"
    
    summary_html += f"""
        </ul>
        
        <hr>
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px;">
            <h4 style="color: #2c3e50;">{t('test_prep_notes')}</h4>
            <p>{t('case_findings')}</p>
        </div>
        
        <p style="text-align: center; color: #666; font-size: 12px; margin-top: 30px;">
            {t('case_summary_for')}<br>
            {t('date')}: {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}</p>
    </div>
    """
    
    st.markdown(summary_html, unsafe_allow_html=True)
    
    # Yazdırma butonu
    st.markdown(f"""
    <button onclick="window.print()" style="background-color: #4CAF50; color: white; padding: 10px 20px; 
    border: none; border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 10px;">
    {t('print')}</button>
    """, unsafe_allow_html=True)


# Yan menü
with st.sidebar:
    st.title(f"🩺 {t('app_title')}")
    st.markdown("---")
    
    st.subheader(t("api_settings"))
    api_key = st.text_input(t("api_key"), type="password")
    
    st.subheader(t("model_selection"))
    model = st.selectbox(
        "AI Model",
        ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=0
    )
    
    st.subheader(t("difficulty_level"))
    difficulty = st.select_slider(
        t("difficulty_level"),
        options=[t("easy"), t("medium"), t("hard")],
        value=t("medium")
    )
    
    # Yeni vaka butonu
    st.markdown("---")
    if st.button(t("new_case"), use_container_width=True):
        if not api_key:
            st.error(t("please_enter_api"))
        else:
            # İstatistikleri güncelle
            if st.session_state.case_created and not st.session_state.new_case and st.session_state.case_data:
                current_case = st.session_state.case_data
                diff = current_case.get('zorluk', t('medium'))
                
                # Vaka geçmişine ekle
                case_record = {
                    "vaka_adi": current_case.get('vaka_adi', 'Bilinmeyen Vaka'),
                    "zorluk": diff,
                    "dogru_tani": current_case.get('dogru_tani', 'Bilinmeyen'),
                    "cozuldu": st.session_state.diagnosis_correct,
                    "tarih": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
                    "denemeler": st.session_state.attempts
                }
                st.session_state.case_history.append(case_record)
                
                # İstatistikleri güncelle
                st.session_state.stats["total_cases"] += 1
                st.session_state.stats["by_difficulty"][diff]["total"] += 1
                
                if st.session_state.diagnosis_correct:
                    st.session_state.stats["solved_cases"] += 1
                    st.session_state.stats["by_difficulty"][diff]["solved"] += 1
                
                total_attempts = sum([case.get('denemeler', 0) for case in st.session_state.case_history if case.get('cozuldu', False)])
                solved_count = len([case for case in st.session_state.case_history if case.get('cozuldu', False)])
                
                if solved_count > 0:
                    st.session_state.stats["avg_attempts"] = round(total_attempts / solved_count, 1)
                
                if st.session_state.stats["total_cases"] > 0:
                    st.session_state.stats["success_rate"] = round((st.session_state.stats["solved_cases"] / st.session_state.stats["total_cases"]) * 100, 1)
            
            # Yeni vaka oluştur
            st.session_state.new_case = True
            st.session_state.case_created = False
            st.session_state.tests_performed = {}
            st.session_state.diagnosis_feedback = None
            st.session_state.diagnosis_correct = False
            st.session_state.hint_count = 0
            st.session_state.attempts = 0
            st.rerun()

    # Dil seçimi
    st.markdown("---")
    language_selection = st.selectbox(
        "🌐 Dil / Language",
        ["Türkçe", "English"],
        index=0 if st.session_state.language == "tr" else 1
    )

    # Dil değişimini kontrol et
    if language_selection == "Türkçe" and st.session_state.language != "tr":
        st.session_state.language = "tr"
        st.rerun()
    elif language_selection == "English" and st.session_state.language != "en":
        st.session_state.language = "en"
        st.rerun()

# Başlangıç mesajı
if not st.session_state.case_created and not st.session_state.new_case:
    st.markdown(t("welcome_title"))
    
    st.markdown(t("welcome_message"))
    
    st.markdown(t("how_to_use"))
    st.markdown(t("step1"))
    st.markdown(t("step2"))
    st.markdown(t("step3"))
    st.markdown(t("step4"))
    st.markdown(t("step5"))
    st.markdown(t("step6"))
    st.markdown(t("step7"))
    
    st.markdown(t("tips"))
    st.markdown(t("tip1"))
    st.markdown(t("tip2"))
    st.markdown(t("tip3"))
    st.markdown(t("tip4"))
    
    st.markdown(t("start_with_api"))

    # Örnek vaka görseli
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("aii.png", caption=t("app_title"))
    
    with col2:
        st.markdown(t("useful_features"))
        
        st.markdown(t("feature1"))
        st.markdown(t("feature2"))
        st.markdown(t("feature3"))
        st.markdown(t("feature4"))
        st.markdown(t("feature5"))
        st.markdown(t("feature6"))
        st.markdown(t("feature7"))
    
    st.info(t("info_note"))

# Yeni vaka oluştur
if st.session_state.new_case and not st.session_state.case_created:
    if api_key:
        with st.spinner(t('creating_case')):
            st.session_state.case_data = create_enhanced_case(api_key, model, difficulty)
            if st.session_state.case_data:
                st.session_state.case_created = True
                st.session_state.new_case = False
                st.session_state.tests_performed = {}
                st.session_state.diagnosis_feedback = None
                st.session_state.diagnosis_correct = False
                st.session_state.hint_count = 0
                st.session_state.start_time = time.time()  # Kronometreyi başlat
    else:
        st.error(t("api_missing"))
        st.session_state.new_case = False

# Vaka gösterimi
if st.session_state.case_created and st.session_state.case_data:
    case_data = st.session_state.case_data
    
    # Vaka üst bölümü
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.title(f"📋 {case_data['vaka_adi']}")
        
        if case_data['zorluk'] == t("easy") or case_data['zorluk'] == "Kolay":
            st.markdown(f"**{t('difficulty')}:** 🟢 {t('easy')}")
        elif case_data['zorluk'] == t("medium") or case_data['zorluk'] == "Orta":
            st.markdown(f"**{t('difficulty')}:** 🟠 {t('medium')}")
        else:
            st.markdown(f"**{t('difficulty')}:** 🔴 {t('hard')}")
    
    with col2:
        if not st.session_state.diagnosis_correct:
            if st.button(t("show_hint"), use_container_width=True):
                if "ipuclari" in st.session_state.case_data and len(st.session_state.case_data["ipuclari"]) > st.session_state.hint_count:
                    hint = st.session_state.case_data["ipuclari"][st.session_state.hint_count]
                    st.session_state.hint_count += 1
                    st.info(f"{t('hint_number')}{st.session_state.hint_count}: {hint}")
                else:
                    st.warning(t("no_more_hints"))
    
    with col3:
        # Kronometre bileşenini göster
        create_timer_component()

    # Ana içerik - Hasta bilgileri
    st.markdown(f"### {t('case_info')}")
    st.markdown(f"**{t('demographic')}:** {case_data['demografik']}")
    st.markdown(f"**{t('anamnesis')}:** {case_data['anamnez']}")
    st.markdown(f"**{t('physical_exam')}:** {case_data['fizik_muayene']}")
    
    # Vital bulgular
    st.markdown(f"#### {t('vital_signs')}")
    cols = st.columns(5)
    with cols[0]:
        st.metric(t("pulse"), case_data['vital_bulgular']['nabiz'].split(" ")[0])
    with cols[1]:
        st.metric(t("blood_pressure"), case_data['vital_bulgular']['tansiyon'].split(" ")[0])
    with cols[2]:
        st.metric(t("temperature"), case_data['vital_bulgular']['ates'].split(" ")[0])
    with cols[3]:
        st.metric(t("respiration"), case_data['vital_bulgular']['solunum_sayisi'].split(" ")[0])
    with cols[4]:
        st.metric(t("oxygen"), case_data['vital_bulgular']['oksijen_saturasyonu'].split(" ")[0])
    
    # Tetkik isteme bölümü - Daha fazla test ve kategoriler
    st.markdown(f"### {t('order_tests')}")
    
    # Testleri sekmeler halinde gruplandır
    tabs = st.tabs([t("laboratory"), t("imaging"), t("advanced_tests"), t("invasive_tests")])

    with tabs[0]:  # Laboratuvar testleri
        st.markdown(f"#### {t('basic_biochem')}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button(t("hemogram"), key="hemogram", use_container_width=True):
                st.session_state.tests_performed["hemogram"] = case_data["testler"].get("hemogram", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "WBC", "value": "8.2 x10^3/μL", "reference": "4.5-11.0 x10^3/μL", "abnormal": False},
                        {"parameter": "RBC", "value": "4.8 x10^6/μL", "reference": "4.2-5.8 x10^6/μL", "abnormal": False},
                        {"parameter": "Hemoglobin", "value": "14.2 g/dL", "reference": "13.5-17.5 g/dL", "abnormal": False},
                        {"parameter": "Hematokrit", "value": "42.5%", "reference": "38.8-50.0%", "abnormal": False},
                        {"parameter": "MCV", "value": "87.5 fL", "reference": "80.0-97.0 fL", "abnormal": False},
                        {"parameter": "MCHC", "value": "33.4 g/dL", "reference": "32.0-36.0 g/dL", "abnormal": False},
                        {"parameter": "Platelet", "value": "250 x10^3/μL", "reference": "150-450 x10^3/μL", "abnormal": False},
                        {"parameter": "Lenfosit", "value": "2.1 x10^3/μL", "reference": "1.0-4.8 x10^3/μL", "abnormal": False},
                        {"parameter": "Nötrofil", "value": "5.0 x10^3/μL", "reference": "1.8-7.8 x10^3/μL", "abnormal": False}
                    ]
                })
            
            if st.button(t("crp"), key="crp", use_container_width=True):
                st.session_state.tests_performed["crp"] = case_data["testler"].get("crp", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "CRP", "value": "3.2 mg/L", "reference": "0-5 mg/L", "abnormal": False}
                    ]
                })
                
            if st.button(t("sedimentation"), key="sedimentasyon", use_container_width=True):
                st.session_state.tests_performed["sedimentasyon"] = case_data["testler"].get("sedimentasyon", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "Sedimentasyon", "value": "10 mm/saat", "reference": "0-15 mm/saat", "abnormal": False}
                    ]
                })
        
        with col2:
            if st.button(t("biochemistry"), key="biyokimya", use_container_width=True):
                st.session_state.tests_performed["biyokimya"] = case_data["testler"].get("biyokimya", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "Glukoz", "value": "92 mg/dL", "reference": "70-100 mg/dL", "abnormal": False},
                        {"parameter": "Üre", "value": "28 mg/dL", "reference": "15-43 mg/dL", "abnormal": False},
                        {"parameter": "Kreatinin", "value": "0.9 mg/dL", "reference": "0.7-1.3 mg/dL", "abnormal": False},
                        {"parameter": "AST", "value": "22 U/L", "reference": "5-40 U/L", "abnormal": False},
                        {"parameter": "ALT", "value": "25 U/L", "reference": "5-40 U/L", "abnormal": False},
                        {"parameter": "ALP", "value": "85 U/L", "reference": "40-130 U/L", "abnormal": False},
                        {"parameter": "GGT", "value": "30 U/L", "reference": "8-61 U/L", "abnormal": False},
                        {"parameter": "Total Bilirubin", "value": "0.8 mg/dL", "reference": "0.3-1.2 mg/dL", "abnormal": False},
                        {"parameter": "Direkt Bilirubin", "value": "0.2 mg/dL", "reference": "0.0-0.3 mg/dL", "abnormal": False},
                        {"parameter": "Sodyum", "value": "140 mmol/L", "reference": "136-145 mmol/L", "abnormal": False},
                        {"parameter": "Potasyum", "value": "4.2 mmol/L", "reference": "3.5-5.1 mmol/L", "abnormal": False},
                        {"parameter": "Kalsiyum", "value": "9.6 mg/dL", "reference": "8.6-10.2 mg/dL", "abnormal": False},
                        {"parameter": "Albumin", "value": "4.2 g/dL", "reference": "3.5-5.2 g/dL", "abnormal": False},
                        {"parameter": "Total Protein", "value": "7.0 g/dL", "reference": "6.4-8.3 g/dL", "abnormal": False}
                    ]
                })
                
            if st.button(t("electrolytes"), key="elektrolitler", use_container_width=True):
                st.session_state.tests_performed["elektrolitler"] = case_data["testler"].get("elektrolitler", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "Sodyum", "value": "140 mmol/L", "reference": "136-145 mmol/L", "abnormal": False},
                        {"parameter": "Potasyum", "value": "4.2 mmol/L", "reference": "3.5-5.1 mmol/L", "abnormal": False},
                        {"parameter": "Klor", "value": "102 mmol/L", "reference": "98-107 mmol/L", "abnormal": False},
                        {"parameter": "Kalsiyum", "value": "9.6 mg/dL", "reference": "8.6-10.2 mg/dL", "abnormal": False},
                        {"parameter": "Magnezyum", "value": "2.0 mg/dL", "reference": "1.7-2.4 mg/dL", "abnormal": False},
                        {"parameter": "Fosfor", "value": "3.4 mg/dL", "reference": "2.5-4.5 mg/dL", "abnormal": False}
                    ]
                })
                
            if st.button(t("urinalysis"), key="tam_idrar_tetkiki", use_container_width=True):
                st.session_state.tests_performed["tam_idrar_tetkiki"] = case_data["testler"].get("tam_idrar_tetkiki", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "pH", "value": "6.0", "reference": "4.5-8.0", "abnormal": False},
                        {"parameter": "Dansite", "value": "1.020", "reference": "1.005-1.030", "abnormal": False},
                        {"parameter": "Protein", "value": "Negatif", "reference": "Negatif", "abnormal": False},
                        {"parameter": "Glukoz", "value": "Negatif", "reference": "Negatif", "abnormal": False},
                        {"parameter": "Keton", "value": "Negatif", "reference": "Negatif", "abnormal": False},
                        {"parameter": "Bilirubin", "value": "Negatif", "reference": "Negatif", "abnormal": False},
                        {"parameter": "Eritrosit", "value": "0-2 /HPF", "reference": "0-3 /HPF", "abnormal": False},
                        {"parameter": "Lökosit", "value": "0-2 /HPF", "reference": "0-5 /HPF", "abnormal": False},
                        {"parameter": "Nitrit", "value": "Negatif", "reference": "Negatif", "abnormal": False}
                    ]
                })
        
        with col3:
            if st.button(t("coagulation"), key="koagulasyon", use_container_width=True):
                st.session_state.tests_performed["koagulasyon"] = case_data["testler"].get("koagulasyon", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "PT", "value": "12.5 sn", "reference": "11.0-14.0 sn", "abnormal": False},
                        {"parameter": "aPTT", "value": "32 sn", "reference": "25-35 sn", "abnormal": False},
                        {"parameter": "INR", "value": "1.1", "reference": "0.8-1.2", "abnormal": False},
                        {"parameter": "Fibrinojen", "value": "310 mg/dL", "reference": "200-400 mg/dL", "abnormal": False}
                    ]
                })
                
            if st.button(t("d_dimer"), key="d_dimer", use_container_width=True):
                st.session_state.tests_performed["d_dimer"] = case_data["testler"].get("d_dimer", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "D-Dimer", "value": "0.4 mg/L", "reference": "0-0.5 mg/L", "abnormal": False}
                    ]
                })
                
            if st.button(t("blood_gas"), key="kan_gazi", use_container_width=True):
                st.session_state.tests_performed["kan_gazi"] = case_data["testler"].get("kan_gazi", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "pH", "value": "7.40", "reference": "7.35-7.45", "abnormal": False},
                        {"parameter": "pO2", "value": "95 mmHg", "reference": "83-108 mmHg", "abnormal": False},
                        {"parameter": "pCO2", "value": "40 mmHg", "reference": "35-45 mmHg", "abnormal": False},
                        {"parameter": "HCO3", "value": "24 mmol/L", "reference": "22-26 mmol/L", "abnormal": False},
                        {"parameter": "Baz açığı", "value": "0 mmol/L", "reference": "-2 - +2 mmol/L", "abnormal": False},
                        {"parameter": "Laktat", "value": "1.2 mmol/L", "reference": "0.5-2.2 mmol/L", "abnormal": False}
                    ]
                })
        
        with col4:
            if st.button(t("cardiac_panel"), key="kardiyak_panel", use_container_width=True):
                st.session_state.tests_performed["kardiyak_panel"] = case_data["testler"].get("kardiyak_panel", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "CK-MB", "value": "3.2 ng/mL", "reference": "0-5.0 ng/mL", "abnormal": False},
                        {"parameter": "Troponin I", "value": "0.02 ng/mL", "reference": "0-0.04 ng/mL", "abnormal": False},
                        {"parameter": "NT-proBNP", "value": "80 pg/mL", "reference": "0-125 pg/mL", "abnormal": False}
                    ]
                })
                
            if st.button(t("troponin"), key="troponin", use_container_width=True):
                st.session_state.tests_performed["troponin"] = case_data["testler"].get("troponin", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "Troponin I", "value": "0.02 ng/mL", "reference": "0-0.04 ng/mL", "abnormal": False},
                        {"parameter": "Troponin T", "value": "0.005 ng/mL", "reference": "0-0.01 ng/mL", "abnormal": False}
                    ]
                })
                
            if st.button(t("liver_function"), key="karaciger_fonksiyon_testleri", use_container_width=True):
                st.session_state.tests_performed["karaciger_fonksiyon_testleri"] = case_data["testler"].get("karaciger_fonksiyon_testleri", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "Albümin", "value": "4.2 g/dL", "reference": "3.5-5.2 g/dL", "abnormal": False},
                        {"parameter": "Globülin", "value": "2.8 g/dL", "reference": "2.3-3.5 g/dL", "abnormal": False},
                        {"parameter": "PT", "value": "12.5 sn", "reference": "11.0-14.0 sn", "abnormal": False},
                        {"parameter": "INR", "value": "1.1", "reference": "0.8-1.2", "abnormal": False}
                    ]
                })

        st.markdown(f"#### {t('endocrine_metabolic')}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button(t("thyroid_function"), key="tiroid_fonksiyon_testleri", use_container_width=True):
                st.session_state.tests_performed["tiroid_fonksiyon_testleri"] = case_data["testler"].get("tiroid_fonksiyon_testleri", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "TSH", "value": "2.1 μIU/mL", "reference": "0.4-4.0 μIU/mL", "abnormal": False},
                        {"parameter": "sT4", "value": "1.2 ng/dL", "reference": "0.8-1.8 ng/dL", "abnormal": False},
                        {"parameter": "sT3", "value": "3.2 pg/mL", "reference": "2.3-4.2 pg/mL", "abnormal": False},
                        {"parameter": "Anti-TPO", "value": "12 IU/mL", "reference": "0-35 IU/mL", "abnormal": False}
                    ]
                })
        
        with col2:
            if st.button(t("glucose_profile"), key="glikoz_profili", use_container_width=True):
                st.session_state.tests_performed["glikoz_profili"] = case_data["testler"].get("glikoz_profili", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "Açlık kan şekeri", "value": "92 mg/dL", "reference": "70-100 mg/dL", "abnormal": False},
                        {"parameter": "HbA1c", "value": "5.4%", "reference": "4.0-5.6%", "abnormal": False},
                        {"parameter": "İnsülin", "value": "8.5 μU/mL", "reference": "2.6-24.9 μU/mL", "abnormal": False},
                        {"parameter": "C-peptid", "value": "2.2 ng/mL", "reference": "1.1-4.4 ng/mL", "abnormal": False}
                    ]
                })
        
        with col3:
            if st.button(t("lipid_profile"), key="lipid_profili", use_container_width=True):
                st.session_state.tests_performed["lipid_profili"] = case_data["testler"].get("lipid_profili", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "Total Kolesterol", "value": "180 mg/dL", "reference": "< 200 mg/dL", "abnormal": False},
                        {"parameter": "HDL", "value": "50 mg/dL", "reference": "> 40 mg/dL", "abnormal": False},
                        {"parameter": "LDL", "value": "110 mg/dL", "reference": "< 130 mg/dL", "abnormal": False},
                        {"parameter": "Trigliserit", "value": "120 mg/dL", "reference": "< 150 mg/dL", "abnormal": False},
                        {"parameter": "Non-HDL Kolesterol", "value": "130 mg/dL", "reference": "< 160 mg/dL", "abnormal": False}
                    ]
                })
        
        with col4:
            if st.button(t("hormone_profile"), key="hormon_profili", use_container_width=True):
                st.session_state.tests_performed["hormon_profili"] = case_data["testler"].get("hormon_profili", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "FSH", "value": "7.2 mIU/mL", "reference": "1.5-12.4 mIU/mL", "abnormal": False},
                        {"parameter": "LH", "value": "5.5 mIU/mL", "reference": "1.7-8.6 mIU/mL", "abnormal": False},
                        {"parameter": "Östradiol", "value": "30 pg/mL", "reference": "15-350 pg/mL", "abnormal": False},
                        {"parameter": "Progesteron", "value": "0.8 ng/mL", "reference": "0.2-1.5 ng/mL", "abnormal": False},
                        {"parameter": "Testosteron", "value": "450 ng/dL", "reference": "280-1100 ng/dL", "abnormal": False},
                        {"parameter": "DHEA-S", "value": "250 μg/dL", "reference": "80-560 μg/dL", "abnormal": False},
                        {"parameter": "Prolaktin", "value": "12 ng/mL", "reference": "4-15 ng/mL", "abnormal": False}
                    ]
                })
        
        st.markdown(f"#### {t('other_lab_tests')}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button(t("rheumatologic"), key="romatolojik_testler", use_container_width=True):
                st.session_state.tests_performed["romatolojik_testler"] = case_data["testler"].get("romatolojik_testler", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "ANA", "value": "Negatif", "reference": "Negatif", "abnormal": False},
                        {"parameter": "Anti-dsDNA", "value": "Negatif", "reference": "Negatif", "abnormal": False},
                        {"parameter": "RF", "value": "10 IU/mL", "reference": "0-14 IU/mL", "abnormal": False},
                        {"parameter": "Anti-CCP", "value": "Negatif", "reference": "Negatif", "abnormal": False},
                        {"parameter": "C3", "value": "110 mg/dL", "reference": "90-180 mg/dL", "abnormal": False},
                        {"parameter": "C4", "value": "30 mg/dL", "reference": "10-40 mg/dL", "abnormal": False}
                    ]
                })

        
        with col2:
            if st.button(t("iron_profile"), key="iron_profili", use_container_width=True):
                st.session_state.tests_performed["iron_profili"] = case_data["testler"].get("iron_profili", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "Demir", "value": "90 μg/dL", "reference": "65-175 μg/dL", "abnormal": False},
                        {"parameter": "Ferritin", "value": "120 ng/mL", "reference": "30-400 ng/mL", "abnormal": False},
                        {"parameter": "Demir Bağlama Kapasitesi", "value": "350 μg/dL", "reference": "250-450 μg/dL", "abnormal": False},
                        {"parameter": "Transferrin Satürasyonu", "value": "25%", "reference": "20-50%", "abnormal": False}
                    ]
                })
        
        with col3:
            if st.button(t("tumor_markers"), key="tumor_belirtecleri", use_container_width=True):
                st.session_state.tests_performed["tumor_belirtecleri"] = case_data["testler"].get("tumor_belirtecleri", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "CEA", "value": "2.1 ng/mL", "reference": "0-5.0 ng/mL", "abnormal": False},
                        {"parameter": "AFP", "value": "5.2 ng/mL", "reference": "0-9.0 ng/mL", "abnormal": False},
                        {"parameter": "CA 19-9", "value": "15 U/mL", "reference": "0-37 U/mL", "abnormal": False},
                        {"parameter": "CA 125", "value": "12 U/mL", "reference": "0-35 U/mL", "abnormal": False},
                        {"parameter": "CA 15-3", "value": "14 U/mL", "reference": "0-30 U/mL", "abnormal": False},
                        {"parameter": "PSA", "value": "0.8 ng/mL", "reference": "0-4.0 ng/mL", "abnormal": False}
                    ]
                })
        
        with col4:
            if st.button(t("vitamin_b12"), key="vitamin_b12_folat", use_container_width=True):
                st.session_state.tests_performed["vitamin_b12_folat"] = case_data["testler"].get("vitamin_b12_folat", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "B12 vitamini", "value": "420 pg/mL", "reference": "200-900 pg/mL", "abnormal": False},
                        {"parameter": "Folik asit", "value": "9.5 ng/mL", "reference": "3.1-20.5 ng/mL", "abnormal": False}
                    ]
                })

    with tabs[1]:  # Görüntüleme testleri
        st.markdown(f"#### {t('xray_ultrasound')}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button(t("ekg"), key="ekg", use_container_width=True):
                st.session_state.tests_performed["ekg"] = case_data["testler"].get("ekg", {
                    "relevance": "İlgisiz",
                    "result": "Normal sinüs ritmi. Hız 72 atım/dakika. Normal QRS morfolojisi. Normal ST segmenti ve T dalgaları. PR ve QT intervalleri normal sınırlarda."
                })
            
            if st.button(t("chest_xray"), key="akciger_rontgen", use_container_width=True):
                st.session_state.tests_performed["akciger_rontgen"] = case_data["testler"].get("akciger_rontgen", {
                    "relevance": "İlgisiz",
                    "result": "PA akciğer grafisinde her iki akciğer alanları açık, sinüsler serbest. Kalp gölgesi normal. Mediastinal genişleme yok. Kemik yapılar doğal."
                })
            
            if st.button(t("abdominal_usg"), key="batin_usg", use_container_width=True):
                st.session_state.tests_performed["batin_usg"] = case_data["testler"].get("batin_usg", {
                    "relevance": "İlgisiz",
                    "result": "Karaciğer normal boyut ve ekojenitede. Safra kesesi, safra yolları, pankreas, dalak ve her iki böbrek normal görünümde. Batın içi serbest sıvı izlenmedi."
                })
        
        with col2:
            if st.button(t("echocardiography"), key="ekokardiyografi", use_container_width=True):
                st.session_state.tests_performed["ekokardiyografi"] = case_data["testler"].get("ekokardiyografi", {
                    "relevance": "İlgisiz",
                    "result": "Sol ventrikül boyutları ve duvar kalınlıkları normal. Ejeksiyon fraksiyonu %60. Bölgesel duvar hareket kusuru yok. Kapak fonksiyonları normal. Perikardiyal efüzyon yok."
                })
            
            if st.button(t("thyroid_usg"), key="tiroid_usg", use_container_width=True):
                st.session_state.tests_performed["tiroid_usg"] = case_data["testler"].get("tiroid_usg", {
                    "relevance": "İlgisiz",
                    "result": "Tiroid bezi boyutları normal. Parankim ekojenitesi homojen. Nodül veya kitle izlenmedi."
                })
            
            if st.button(t("doppler_usg"), key="doppler_usg", use_container_width=True):
                st.session_state.tests_performed["doppler_usg"] = case_data["testler"].get("doppler_usg", {
                    "relevance": "İlgisiz",
                    "result": "İncelenen arteryel ve venöz yapılarda akım paternleri normal. Tromboz veya stenoz bulgusu saptanmadı."
                })
        
        with col3:
            if st.button(t("thorax_ct"), key="toraks_bt", use_container_width=True):
                st.session_state.tests_performed["toraks_bt"] = case_data["testler"].get("toraks_bt", {
                    "relevance": "İlgisiz",
                    "result": "Her iki akciğer parankimi normal. Mediastende patolojik boyutta lenf nodu saptanmadı. Plevral efüzyon yok. Kemik yapılar doğal."
                })
            
            if st.button(t("abdominal_ct"), key="batin_bt", use_container_width=True):
                st.session_state.tests_performed["batin_bt"] = case_data["testler"].get("batin_bt", {
                    "relevance": "İlgisiz",
                    "result": "Karaciğer, safra kesesi, pankreas, dalak, böbrekler ve adrenal bezler normal görünümde. Batın içi lenf nodları normal boyutlarda. Serbest sıvı yok."
                })
            
            if st.button(t("brain_ct"), key="beyin_bt", use_container_width=True):
                st.session_state.tests_performed["beyin_bt"] = case_data["testler"].get("beyin_bt", {
                    "relevance": "İlgisiz",
                    "result": "Serebral ve serebellar hemisferler normal. Ventriküler sistem normal genişlikte. Shift, kitle etkisi veya kanama bulgusu yok. Kemik yapılar doğal."
                })
        
        with col4:
            if st.button(t("brain_mri"), key="beyin_mr", use_container_width=True):
                st.session_state.tests_performed["beyin_mr"] = case_data["testler"].get("beyin_mr", {
                    "relevance": "İlgisiz",
                    "result": "Serebral ve serebellar parankimde sinyal değişikliği yok. Ventriküler sistem normal. Kontrastlanan lezyon saptanmadı. Diffüzyon kısıtlaması yok."
                })
            
            if st.button(t("mri_angiography"), key="mr_anjiografi", use_container_width=True):
                st.session_state.tests_performed["mr_anjiografi"] = case_data["testler"].get("mr_anjiografi", {
                    "relevance": "İlgisiz",
                    "result": "İncelenen arteryel yapılarda stenoz, oklüzyon veya anevrizma saptanmadı. Vasküler yapılar normal kalibrasyonda ve konturlu."
                })
            
            if st.button(t("pet_ct"), key="pet_ct", use_container_width=True):
                st.session_state.tests_performed["pet_ct"] = case_data["testler"].get("pet_ct", {
                    "relevance": "İlgisiz",
                    "result": "Tüm vücut taramasında patolojik FDG tutulumu gösteren odak izlenmedi."
                })
        
        st.markdown(f"#### {t('other_imaging')}")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button(t("scintigraphy"), key="sintigrafi", use_container_width=True):
                st.session_state.tests_performed["sintigrafi"] = case_data["testler"].get("sintigrafi", {
                    "relevance": "İlgisiz",
                    "result": "Radyoaktif madde tutulumunda anormal odak saptanmadı."
                })
        
        with col2:
            if st.button(t("mammography"), key="mamografi", use_container_width=True):
                st.session_state.tests_performed["mamografi"] = case_data["testler"].get("mamografi", {
                    "relevance": "İlgisiz",
                    "result": "Her iki meme parankimi homojen dansitede. Kitle, asimetri veya mikrokalsifikasyon izlenmedi. BIRADS 1."
                })

    with tabs[2]:  # İleri Tetkikler
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button(t("stress_test"), key="efor_testi", use_container_width=True):
                st.session_state.tests_performed["efor_testi"] = case_data["testler"].get("efor_testi", {
                    "relevance": "İlgisiz",
                    "result": "Hedef kalp hızına ulaşıldı. İskemik semptom veya EKG değişikliği saptanmadı. Egzersiz kapasitesi normal."
                })
            
            if st.button(t("holter"), key="holter_ekg", use_container_width=True):
                st.session_state.tests_performed["holter_ekg"] = case_data["testler"].get("holter_ekg", {
                    "relevance": "İlgisiz",
                    "result": "24 saatlik kayıtta ortalama kalp hızı 70/dk. Anlamlı ritim bozukluğu, AV blok veya iskemik değişiklik saptanmadı."
                })
        
        with col2:
            if st.button(t("pulmonary_function"), key="solunum_fonksiyon_testi", use_container_width=True):
                st.session_state.tests_performed["solunum_fonksiyon_testi"] = case_data["testler"].get("solunum_fonksiyon_testi", {
                    "relevance": "İlgisiz",
                    "result": "FEV1, FVC ve FEV1/FVC değerleri normal sınırlarda. Obstrüktif veya restriktif pattern saptanmadı."
                })
            
            if st.button(t("eeg"), key="eeg", use_container_width=True):
                st.session_state.tests_performed["eeg"] = case_data["testler"].get("eeg", {
                    "relevance": "İlgisiz",
                    "result": "Normal uyanıklık EEG aktivitesi. Epileptiform aktivite veya fokal yavaşlama saptanmadı."
                })
        
        with col3:
            if st.button(t("emg"), key="emg", use_container_width=True):
                st.session_state.tests_performed["emg"] = case_data["testler"].get("emg", {
                    "relevance": "İlgisiz",
                    "result": "Sinir iletim çalışmalarında motor ve duyusal yanıtlar normal. İğne EMG'de denervasyon bulgusu saptanmadı."
                })
            
            if st.button(t("hepatitis_serology"), key="hepatit_serolojisi", use_container_width=True):
                st.session_state.tests_performed["hepatit_serolojisi"] = case_data["testler"].get("hepatit_serolojisi", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "HBsAg", "value": "Negatif", "reference": "Negatif", "abnormal": False},
                        {"parameter": "Anti-HBs", "value": "Pozitif", "reference": "Negatif/Pozitif", "abnormal": False},
                        {"parameter": "Anti-HBc IgM", "value": "Negatif", "reference": "Negatif", "abnormal": False},
                        {"parameter": "Anti-HBc Total", "value": "Negatif", "reference": "Negatif", "abnormal": False},
                        {"parameter": "Anti-HCV", "value": "Negatif", "reference": "Negatif", "abnormal": False}
                    ]
                })
        
        with col4:
            if st.button(t("ogtt"), key="ogtt", use_container_width=True):
                st.session_state.tests_performed["ogtt"] = case_data["testler"].get("ogtt", {
                    "relevance": "İlgisiz",
                    "results": [
                        {"parameter": "Açlık kan şekeri", "value": "90 mg/dL", "reference": "70-100 mg/dL", "abnormal": False},
                        {"parameter": "2. saat kan şekeri", "value": "120 mg/dL", "reference": "<140 mg/dL", "abnormal": False}
                    ]
                })

    with tabs[3]:  # İnvaziv Testler
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button(t("gastroscopy"), key="gastroskopi", use_container_width=True):
                st.session_state.tests_performed["gastroskopi"] = case_data["testler"].get("gastroskopi", {
                    "relevance": "İlgisiz",
                    "result": "Özofagus, mide ve duodenum mukozası normal görünümde. Patolojik lezyon saptanmadı."
                })
            
            if st.button(t("colonoscopy"), key="kolonoskopi", use_container_width=True):
                st.session_state.tests_performed["kolonoskopi"] = case_data["testler"].get("kolonoskopi", {
                    "relevance": "İlgisiz",
                    "result": "Tüm kolon segmentleri değerlendirildi. Mukoza normal görünümde. Polip veya kitle saptanmadı."
                })
        
        with col2:
            if st.button(t("bronchoscopy"), key="bronkoskopi", use_container_width=True):
                st.session_state.tests_performed["bronkoskopi"] = case_data["testler"].get("bronkoskopi", {
                    "relevance": "İlgisiz",
                    "result": "Trakeobronşiyal ağaç normal görünümde. Endobronşiyal lezyon görülmedi. Sekresyon normal."
                })
            
            if st.button(t("bone_marrow"), key="kemik_iligi_biyopsisi", use_container_width=True):
                st.session_state.tests_performed["kemik_iligi_biyopsisi"] = case_data["testler"].get("kemik_iligi_biyopsisi", {
                    "relevance": "İlgisiz",
                    "result": "Normosellüler kemik iliği. Tüm hücre serileri normal maturasyon göstermekte. Malign hücre infiltrasyonu veya displazi bulgusu yok."
                })
        
        with col3:
            if st.button(t("liver_biopsy"), key="karaciger_biyopsisi", use_container_width=True):
                st.session_state.tests_performed["karaciger_biyopsisi"] = case_data["testler"].get("karaciger_biyopsisi", {
                    "relevance": "İlgisiz",
                    "result": "Normal hepatik parankimal mimari. İnflamasyon, fibrozis veya malign değişiklik saptanmadı."
                })
            
            if st.button(t("kidney_biopsy"), key="bobrek_biyopsisi", use_container_width=True):
                st.session_state.tests_performed["bobrek_biyopsisi"] = case_data["testler"].get("bobrek_biyopsisi", {
                    "relevance": "İlgisiz",
                    "result": "Glomerüller, tübüller, interstisyum ve damarlar normal görünümde. İmmünofloresan incelemede immün kompleks birikimi saptanmadı."
                })
        
        with col4:
            if st.button(t("lumbar_puncture"), key="lomber_ponksiyon", use_container_width=True):
                st.session_state.tests_performed["lomber_ponksiyon"] = case_data["testler"].get("lomber_ponksiyon", {
                    "relevance": "İlgisiz",
                    "result": "BOS basıncı normal. Berrak görünümde. Hücre sayımı, protein ve glukoz değerleri normal sınırlarda. Mikroorganizma görülmedi."
                })
            
            if st.button(t("blood_culture"), key="kan_kulturu", use_container_width=True):
                st.session_state.tests_performed["kan_kulturu"] = case_data["testler"].get("kan_kulturu", {
                    "relevance": "İlgisiz",
                    "result": "İnkübasyon süresince üreme saptanmadı."
                })
    
    # Sonuçları göster
    if st.session_state.tests_performed:
        st.markdown(f"### {t('test_results')}")
        
        for test_name, test_data in st.session_state.tests_performed.items():
            # Test adını doğru dile çevir
            formatted_test_name = test_name.replace('_', ' ').title()
            
            # Sonuç kartı oluştur
            st.markdown(f"**{formatted_test_name}**")
            
            if "results" in test_data:
                # Tablo formatında sonuçlar (laboratuvar testleri)
                results_data = []
                for result in test_data["results"]:
                    status = t("abnormal") if result.get("abnormal", False) else t("normal")
                    
                    results_data.append({
                        t("parameter"): result["parameter"],
                        t("value"): result["value"],
                        t("reference_range"): result["reference"],
                        t("status"): status
                    })
                
                df = pd.DataFrame(results_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                # Metin formatında sonuçlar (görüntüleme ve diğer testler)
                st.markdown(f"<div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; border-left: 4px solid #4CAF50;'>{test_data['result']}</div>", unsafe_allow_html=True)
            
            st.markdown("---")
    
    # Tanı bölümü
    st.markdown(f"### {t('diagnosis')}")
    
    if not st.session_state.diagnosis_correct:
        user_diagnosis = st.text_input(t("what_diagnosis"), key="diagnosis_input")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button(t("evaluate_diagnosis"), use_container_width=True, disabled=not user_diagnosis):
                if api_key and user_diagnosis:
                    with st.spinner(t('evaluating')):
                        st.session_state.attempts += 1
                        feedback = get_ai_feedback(api_key, model, case_data, user_diagnosis)
                        st.session_state.diagnosis_feedback = feedback
                        st.session_state.diagnosis_correct = feedback.get("dogru_mu", False)
                        
                        # Tanı doğruysa geçen süreyi hesapla
                        if feedback.get("dogru_mu", False) and st.session_state.start_time is not None:
                            end_time = time.time()
                            st.session_state.elapsed_time = end_time - st.session_state.start_time
                            st.session_state.start_time = None  # Kronometreyi sıfırla
        
        if st.session_state.diagnosis_feedback:
            feedback = st.session_state.diagnosis_feedback
            if feedback.get("dogru_mu", False):
                st.markdown(f"<div style='background-color: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin-top: 20px;'>{t('congratulations')} {case_data['dogru_tani']}</div>", unsafe_allow_html=True)
                st.markdown(f"**{t('explanation')}** {feedback.get('aciklama', '')}")
            else:
                st.markdown(f"<div style='background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; margin-top: 20px;'>{t('wrong_diagnosis')}</div>", unsafe_allow_html=True)
                st.markdown(f"**{t('feedback')}** {feedback.get('aciklama', '')}")
                if "ipucu" in feedback and feedback["ipucu"]:
                    st.markdown(f"<div style='background-color: #fff3cd; color: #856404; padding: 10px; border-radius: 5px; margin-top: 10px;'>💡 **{t('hint')}** {feedback.get('ipucu', '')}</div>", unsafe_allow_html=True)
        
                # Eğer 3 denemeden fazla yapıldıysa pes et butonu göster
                if st.session_state.attempts >= 3:
                    if st.button(t("show_answer"), use_container_width=True):
                        st.markdown(f"<div style='background-color: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin-top: 20px;'>{t('correct_diagnosis')} {case_data['dogru_tani']}</div>", unsafe_allow_html=True)
                        st.session_state.diagnosis_correct = True
                        
                        # Cevabı göster butonu ile vazgeçildiğinde de süreyi hesapla
                        if st.session_state.start_time is not None:
                            end_time = time.time()
                            st.session_state.elapsed_time = end_time - st.session_state.start_time
                            st.session_state.start_time = None  # Kronometreyi sıfırla
    else:
        st.markdown(f"<div style='background-color: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin-top: 20px;'>{t('congratulations')} {case_data['dogru_tani']}</div>", unsafe_allow_html=True)
        
        # Vaka çözüldüyse özet göster
        if st.button(t("show_summary"), use_container_width=True):
            create_case_summary(case_data, st.session_state.tests_performed)                