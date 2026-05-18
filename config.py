import os

class Settings:
    # رابط قاعدة البيانات لتنظيم المهام خلف الكواليس
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # مفتاح ذكاء اصطناعي لتوليد الصوت العربي (ElevenLabs)
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "your_key_here")
    
    # إعدادات السحاب لحفظ الفيديو وإرساله لمعرض هاتفك
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "your_aws_key")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "your_aws_secret")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "your_bucket_name")

settings = Settings()
