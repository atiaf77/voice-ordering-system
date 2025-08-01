# 🚀 دليل رفع المشروع على GitHub

## الخطوات لرفع المشروع على GitHub:

### 1. إنشاء مستودع على GitHub
1. اذهب إلى [GitHub.com](https://github.com)
2. اضغط على "New repository" أو علامة "+"
3. أدخل اسم المستودع: `voice-ordering-system` أو `نظام-طلب-الطعام-الصوتي`
4. أضف وصف: "Voice-based food and coffee ordering system in Arabic"
5. اجعل المستودع **Public**
6. **لا تضع** علامة على "Initialize with README" (لأننا لدينا README بالفعل)
7. اضغط "Create repository"

### 2. ربط المستودع المحلي بـ GitHub
```bash
# أضف remote للمستودع
git remote add origin https://github.com/atiaf77/voice-ordering-system.git

# تأكد من أن الـ remote مضاف بشكل صحيح
git remote -v
```

### 3. رفع الملفات
```bash
# رفع الملفات إلى GitHub
git push -u origin master
```

### 4. إعداد GitHub Pages (اختياري)
لعرض المشروع كموقع ويب:
1. اذهب إلى Settings في مستودعك
2. انزل إلى "Pages"
3. اختر "Deploy from a branch"
4. اختر "master" branch
5. اضغط Save

## الأوامر الكاملة للنسخ واللصق:

```bash
# تغيير المجلد
cd "C:\Users\Lenovo\Desktop\Convert the audio input to text"

# إضافة remote
git remote add origin https://github.com/atiaf77/voice-ordering-system.git

# رفع الملفات
git push -u origin master
```

## إضافة تحديثات لاحقاً:

```bash
# إضافة التغييرات الجديدة
git add .

# إنشاء commit جديد
git commit -m "وصف التحديث"

# رفع التحديثات
git push
```

## نصائح مهمة:

1. **تأكد من إزالة أي API keys** من الملفات قبل الرفع
2. **راجع ملف .gitignore** للتأكد من عدم رفع ملفات حساسة
3. **أضف screenshots** للمشروع في مجلد `screenshots/`
4. **استخدم commit messages واضحة** باللغة العربية أو الإنجليزية

## روابط مفيدة:
- [دليل Git الأساسي](https://git-scm.com/book/en/v2)
- [دليل GitHub](https://docs.github.com/)
- [دليل Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

---

**تم إعداد المشروع بواسطة:** Atiaf
**تاريخ الإنشاء:** أغسطس 2025
