#Truy vấn dữ liệu
from itertools import count

from django.db.models import Count
from django.utils.timezone import activate

from .models import Category, Course

# params truyền là tuple
def load_courses(params={}):
    # lấy activate
    q = Course.objects.filer(activate=True)

    kw = params.get('kw')
    # Lọc ra môn học không phân biệt hoa thường
    if kw:
        q = q.filter(subject__icontains=kw)
    cate_id = params.get('cate_id')
    if cate_id:
         q = q.filter(category_id=cate_id)
    return q

# Nếu viết là course__id -> thì nó sẽ là truy vấn ngược về khóa ngoại .
#order_by(kw) +kw sắp xếp tăng -kw sắp xếp giảm
def count_courses_by_cate():
    return  Category.objects.annotate(count=Count('course__id')).values("id", "name", "count").order_by('-count')

def stats():
    pass