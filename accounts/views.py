from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    UserUpdateSerializer
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """User registration endpoint"""
    
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'user': UserSerializer(user).data,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token endpoint with user data"""
    
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UserUpdateSerializer
        return UserSerializer
    
    def get_object(self):
        return self.request.user


class UserDetailView(generics.RetrieveAPIView):
    """Get user details by username"""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [permissions.AllowAny]


class FollowUserView(APIView):
    """Follow/Unfollow a user"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, username):
        try:
            user_to_follow = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if user_to_follow == request.user:
            return Response(
                {'error': 'You cannot follow yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from .models import Follow
        
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        
        if not created:
            follow.delete()
            user_to_follow.followers_count -= 1
            request.user.following_count -= 1
            message = 'Unfollowed successfully'
        else:
            user_to_follow.followers_count += 1
            request.user.following_count += 1
            message = 'Followed successfully'
        
        user_to_follow.save()
        request.user.save()
        
        return Response({
            'message': message,
            'is_following': created
        })


class GoogleAuthView(APIView):
    """Google OAuth authentication endpoint"""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        avatar = request.data.get('avatar', '')
        
        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Check if user exists
            user = User.objects.get(email=email)
            
            # Update user info if needed
            if first_name and not user.first_name:
                user.first_name = first_name
            if last_name and not user.last_name:
                user.last_name = last_name
            # Note: Avatar handling would require additional setup in production
            user.save()
            
            message = 'User signed in successfully with Google'
            
        except User.DoesNotExist:
            # Create new user
            username = email.split('@')[0]  # Use email prefix as username
            counter = 1
            original_username = username
            
            # Ensure unique username
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=''  # Empty password for OAuth users
            )
            
            # Note: Avatar handling would require additional setup in production
            message = 'User created successfully with Google'
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
            'message': message
        }, status=status.HTTP_200_OK)
