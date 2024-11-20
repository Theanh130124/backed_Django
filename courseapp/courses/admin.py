from django.contrib import admin
from django.template.response import TemplateResponse

from .dao import count_courses_by_cate, stats
from .models import Category , Course ,Lesson ,Tag ,Like ,Comment , Rating
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path
from courses import dao


#Ghi đề lại trang admin templates
class CourseAppAdminSite(admin.AdminSite):
    site_header = 'AdminTheAnh'
    # Bổ sung thêm method này để có thể thêm view cho admin
    def get_urls(self):
        return [
            # Đây là  course-stats/ đường dẫn dán vào sau admin/
            path('course-stats/', self.stats_view)
        ] + super().get_urls()
    def stats_view(self, request):
        return TemplateResponse(request, 'admin/stats.html',{
            #Đỗ dữ liệu bên dao qua
            'course_count': count_courses_by_cate, #Gọi hàm chờ thực thi
            'stats':stats,
        })


#Ghi đè lại admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk' ,'name']
    search_fields = ['name']
    list_filter = ['id','name']




class CourseAdmin(admin.ModelAdmin):
    # Chỉ show không sữa
    readonly_fields = ['img']
    def img(self, course):
        if course:
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=course.image.name)
            )
    #Nữa viết lên base cho nó kế thừa
    class Media:
        css = {
            'all': ('/static/css/style.css',)
        }
        # js = ('/static/js/script.js',)

class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Lesson
        fields = '__all__'

# Inline này dùng cho 2N2 giữa Lesson và Tag


class LessonTagInlineAdmin(admin.TabularInline):
    model = Lesson.tags.through

class LessonAdmin(admin.ModelAdmin):
    form = LessonForm
    inlines = [LessonTagInlineAdmin]

class TagAdmin(admin.ModelAdmin):
    inlines = [LessonTagInlineAdmin, ]



admin_site =CourseAppAdminSite(name='TheAnh_App')

admin_site.register(Category,CategoryAdmin)
admin_site.register(Course,CourseAdmin)
admin_site.register(Lesson,LessonAdmin)
admin_site.register(Tag,TagAdmin)
admin_site.register(Like)
admin_site.register(Comment)
admin_site.register(Rating)



