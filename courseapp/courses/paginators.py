#Phân trang API

#len django API docs
from  rest_framework.pagination import PageNumberPagination
class CoursePaginator(PageNumberPagination):
    #Số trang
    page_size =  6
#Cài xong thì qua view để thêm vào trong view của Course
