# atlas-backend/llm_utils.py

import google.generativeai as genai
from google.generativeai.types import Tool, FunctionDeclaration
from models import AtlasDB

# کلید API خود را اینجا یا در متغیرهای محیطی قرار دهید
genai.configure(api_key="AIzaSyD8Bo7qSCbSmgBleBlOtBmT3T4sWG3npjo")

def get_atlas_tool() -> Tool:
    """
    یک ابزار Gemini Tool از روی مدل AtlasDB Pydantic می‌سازد.
    این تابع ابتدا JSON Schema را از مدل استخراج کرده و سپس
    فیلدهای 'default' که توسط کتابخانه Gemini پشتیبانی نمی‌شوند را حذف می‌کند.
    """
    #  مرحله ۱: استخراج JSON Schema از مدل Pydantic
    schema = AtlasDB.model_json_schema()

    # مرحله ۲: حذف فیلدهای 'default' از پراپرتی‌های اسکیم
    # این کار برای جلوگیری از خطای ValueError در کتابخانه Gemini ضروری است
    if 'properties' in schema:
        for prop_schema in schema['properties'].values():
            prop_schema.pop('default', None)
    
    # مرحله ۳: ساخت ابزار (Tool) برای Gemini
    f_declaration = FunctionDeclaration(
        name="create_atlas_from_text",
        description="اطلاعات ساختاریافته تاریخی را از یک متن استخراج و یک اطلس ایجاد می‌کند.",
        parameters=schema
    )
    
    return Tool(function_declarations=[f_declaration])


# مقداردهی اولیه مدل Gemini با ابزار تمیز شده
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[get_atlas_tool()]
)

def extract_atlas(text: str) -> AtlasDB:
    """Uses Google Gemini with Tool Calling to extract structured atlas data."""
    
    # ارسال متن به مدل و درخواست برای استفاده از ابزار
    result = model.generate_content(
        f"Extract a historical atlas from this text:\n{text}",
        tool_config={'function_calling_config': 'ANY'} # مدل را مجبور به استفاده از ابزار می‌کند
    )

    # استخراج اولین فراخوانی تابع از پاسخ مدل
    function_call = result.candidates[0].content.parts[0].function_call
    
    # تبدیل آرگومان‌های استخراج شده به دیکشنری
    args = {key: value for key, value in function_call.args.items()}
    
    # اعتبارسنجی داده‌ها با مدل Pydantic و بازگرداندن آبجکت
    return AtlasDB.model_validate(args)