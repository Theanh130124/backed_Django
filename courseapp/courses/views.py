from importlib.resources import contents
from pickle import FALSE

from rest_framework.response import Response
from unicodedata import category
from rest_framework.permissions import AllowAny
from courses.models import Category, Course, Lesson, User, Comment , Like
from courses import serializers , paginators
from rest_framework import viewsets, generics, status , parsers , permissions
from rest_framework.decorators import action
from courses.serializers import LessonSerializer
from courses.perms import OwnerAuthenticated


#View trong Django xử lý logic chính của ứng dụng bằng cách:

# Tiếp nhận và xử lý request từ người dùng (GET, POST, PUT, DELETE, v.v.).
# Gọi serializer để xử lý dữ liệu.
# Trả về response (thường ở dạng JSON trong DRF) sau khi xử lý.

# Create your views here.
class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all() #Lọc tất cả danh mục
    serializer_class = serializers.CategorySerializer




class CourseViewSet(viewsets.ViewSet , generics.ListAPIView):
    queryset =  Course.objects.filter(active=True).all() #oojojc danh sách khóa học
    serializer_class =serializers.CourseSerializer
    pagination_class = paginators.CoursePaginator

    #Trước khi queryset trả về thì lấy ra để làm chức năng search
    def get_queryset(self):
        queries = self.queryset #Lấy trên thanh tìm kiếm
        # (hay còn gọi là query string parameters) là thông tin được truyền qua URL sau dấu hỏi ?. Chúng thường được sử dụng để gửi dữ liệu từ client (trình duyệt) tới server, ví dụ như các tham số tìm kiếm, phân trang, lọc,
        q = self.request.query_params.get("q")
        # Nếu co truyền thì chặn lại thêm subject của mình vào
        if q:
            queries  =queries.filter(subject__icontains=q)

        return queries

    #Nếu trong đường dẫn không có {course_id} thì không để pk và detail = True
    #Lấy danh sách bài học thuộc 1 khóa học có pk = ?
    # Nếu k có url_path thì nó sẽ lấy tên get_lessons lên đường dẫn
    @action(methods=['get'],detail=True , url_path='lesson')
    def get_lessons(self ,request, pk ): #Có get_object thì đã lấy đối tượng khóa học theo id rồi / lesson_set nó tự tạo do có khóa ngoại
        lessons = self.get_object().lesson_set.filter(active=True).all()
        serializers_class = serializers.LessonSerializer
#Nhớ import Response -> Do trả ra danh sách nên many = True

        #context = {'request'} để cho trường img được hiêện -> vì ham tu làm
        return Response(serializers.LessonSerializer(lessons , many =True , context={'request':request}).data ,status=status.HTTP_200_OK)


#Do đường dẫn là lesssons/{lessons_id} -> nên tách làm viewset riêng không như ở trên
#Tạo ViewSet mới xong nhớ qua url khai báo -
#Class này chỉ lấy ra 1 đối tượng theo id
# class LessonViewSet(viewsets.ViewSet , generics.RetrieveAPIView):
#     queryset = Lesson.objects.filter(active=True).all()
#     serializers_class = serializers.LessonDetailSerializer
#     #Phải chung thuc mới vào đc API
#     permission_classes =  [AllowAny]
#
#     def get_permissions(self):
#         if self.action in ['add_comment', 'like']:
#             return  [permissions.IsAuthenticated()]
#         return self.permission_classes
#     #Thêm bình luận vào bài học API có {{lesson_id}} nên có detail =True và có pk
#     @action(methods=['post'],url_path='comment' ,detail=True)
#     def add_comment(self, request , pk):
#         # Chỉ user đc chứng thực mới đc bình luạn  / ở bài học nào / nội dung comment
#         request.data
#         c = Comment.objects.create(user = request.user, lesson =self.get_object(), context=request.data.get('contents'))
#
#         return Response(serializers.CourseSerializer(c).data , status=status.HTTP_201_CREATED)
#
#     #Like nằm trong lessson
#     @action(methods=['post'], url_path='like', detail=True)
#     def like(self , request , pk ):
#         like, created =  Like.objects.get_or_create(user = request.user ,lesson =self.get_object())
#         #Lần đầu tiền like còn ở dưới này đã like rồi thì created là false không tính like nữa -> mà là unlike
#         if not created:
#             like.active = not like.active
#             like.save()
#
#         return  Response(serializers.LessonDetailSerializer(self.get_object(), context={'request':request}).data,status=status.HTTP_200_OK)
class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.filter(active=True).all()
    serializer_class = serializers.LessonDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['add_comment', 'like']:
            return [permissions.IsAuthenticated()]

        return self.permission_classes

    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        c = Comment.objects.create(user=request.user, lesson=self.get_object(), content=request.data.get('content'))

        return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        like, created = Like.objects.get_or_create(user=request.user, lesson=self.get_object())
        if not created:
            like.active = not like.active
            like.save()

        return Response(serializers.LessonDetailSerializer(self.get_object(), context={'request': request}).data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet , generics.DestroyAPIView ,generics.UpdateAPIView) :
    queryset =  Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    #Chứng thực quyền mới cho xóa
    permission_classes = [OwnerAuthenticated]



#Sau khi đã tạo serializer
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset =  User.objects.filter(is_active =True).all()
    serializer_class = serializers.UserSerializer
    # Bật upload lên cloudinary
    parsers_classes = [parsers.MultiPartParser]

#Chỉ gọi APi này khi được chứng thực rồi
    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return  [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]


#Không gửi id gì lên cả nên k có detail
    @action(methods=['get'], url_name='current_user',detail=False)
    # request là đối tượng đã đc chứng thực
    def current_user(self,request):
        request.user
        return  Response(serializers.UserSerializer(request.user).data)



