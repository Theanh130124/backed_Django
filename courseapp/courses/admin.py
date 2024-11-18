from django.contrib import admin
from .models import Category , Course ,Lesson ,Tag
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

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


admin.site.register(Category,CategoryAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Lesson,LessonAdmin)
admin.site.register(Tag,TagAdmin)




