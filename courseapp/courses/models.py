from tkinter.constants import CASCADE

from django.db import models
from django.contrib.auth.models import  AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


# Create your models here.

class User(AbstractUser):
    #Thêm mới 1 truong vào phải để null =True -> avatar này đc bổ sung vào sau khi bảng đã c dữu liệu rồi
    avatar = CloudinaryField('avatar' , null=True)

class BaseModel(models.Model):
    # Thêm null= True vì do thêm BaseModel sau nên các cột Category đã tạo rồi yêu cầu thêm các cột này
    created_date = models.DateField(auto_now_add=True ,null=True)
    # Cứ mỗi lần cập nhật là sửa ngày giờ
    updated_date = models.DateField(auto_now=True , null=True)
    active = models.BooleanField(default=True)
    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=50 , null=False)

    def __str__(self):
        return  self.name

class Course(BaseModel):
    subject = models.CharField(max_length=255 , null=False)
    description = RichTextField()
    image = models.ImageField(upload_to="courses/%Y/%m")
    # Category xóa -> thì bị xóa theo
    category = models.ForeignKey(Category,on_delete=models.CASCADE , related_query_name ='course')
    tags = models.ManyToManyField('Tag')
    def __str__(self):
        return self.subject
    #Mỗi course chỉ có mỗi 1 -> 2 thằng này không trùng
    class Meta:
        unique_together = ('subject','category')

class Lesson(BaseModel):
    subject = models.CharField(max_length=255,null=False)
    content =RichTextField()
    image = models.ImageField(upload_to='lesson/%Y/%m')
    course = models.ForeignKey(Course , on_delete=models.CASCADE)
    #Do để trước Tag nên phải bỏ trong nháy .
    tags = models.ManyToManyField('Tag')
    def __str__(self):
        return self.subject
    class Meta:
        unique_together = ('subject','course')

class Tag(BaseModel):
    name = models.CharField(max_length=50 , unique=True)

    def __str__(self):
        return self.name

class Interraction(BaseModel):
    user = models.ForeignKey(User , on_delete=models.CASCADE, null=False)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE, null=False)

    class Meta:
        abstract = True

class Comment(Interraction):
    content = models.CharField(max_length=255, null=False)

class Like(Interraction):
    active = models.BooleanField(default=True)
    class Meta:
        # Mỗi người dùng chỉ tính 1 lượt like cho lessson
        unique_together = ('user', 'lesson')

class Rating(Interraction):
    rate = models.SmallIntegerField(default=0)