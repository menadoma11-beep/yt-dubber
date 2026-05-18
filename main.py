from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from tasks import process_youtube_dubbing
from celery.result import AsyncResult

app = FastAPI(
    title="YouTube Arabic Dubber API",
    description="بوابة دبلجة فيديوهات يوتيوب للعربية وفصل الموسيقى الحرام تلقائياً"
)

# نموذج البيانات لطلب الرابط
class VideoRequest(BaseModel):
    url: str

@app.post("/api/v1/dub")
def start_dubbing(request: VideoRequest):
    """
    هنا تضع رابط اليوتيوب ليقوم السيرفر ببدء الدبلجة وفصل الصوت فوراً في الخلفية
    """
    if not request.url.startswith("https://"):
        raise HTTPException(status_code=400, detail="الرجاء إدخال رابط يوتيوب صحيح")
    
    # إرسال المهمة لـ Celery لتعمل في الخلفية دون تعطيل واجهة المستخدم
    task = process_youtube_dubbing.delay(request.url)
    
    return {
        "message": "تم استلام الرابط بنجاح وجاري بدء الدبلجة وفصل الموسيقى...",
        "task_id": task.id,
        "status_url": f"/api/v1/status/{task.id}"
    }

@app.get("/api/v1/status/{task_id}")
def get_status(task_id: str):
    """
    هنا يمكنك فحص حالة الفيديو لمعرفة هل انتهى أم لا، وسيعطيك الرابط النهائي للمعرض
    """
    task_result = AsyncResult(task_id)
    
    if task_result.state == "PENDING":
        return {"status": "جاري الانتظار في الطابور..."}
    elif task_result.state == "PROGRESS":
        return {"status": "جاري المعالجة والترجمة والدبلجة الآن..."}
    elif task_result.state == "SUCCESS":
        return {
            "status": "مكتمل بنجاح!",
            "result": task_result.result  # سيحتوي على رابط التحميل المباشر للمعرض
        }
    elif task_result.state == "FAILURE":
        return {
            "status": "فشل المعالجة",
            "error": str(task_result.info)
        }
