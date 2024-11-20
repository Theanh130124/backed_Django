#Đinh nghĩa các permission như Del với Câjp nhật dùng cho chứng thực quyền trong API
from rest_framework import permissions

class OwnerAuthenticated(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        #Chỉ có tài khoản comment mới đc xóa comment của chính cái tài khoản đó
        return self.has_permission(request, view) and request.user == obj.user