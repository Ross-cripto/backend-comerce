"""
  Views module of users
"""

from django.conf import settings 
import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from django.core.mail import send_mail
from datetime import timedelta
from .models import VerificationCode
from utils.generate_code import generate_verification_code
from rest_framework import status
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserRegisterSerializer, UserChangePasswordSerializer
from .tokens import (
    MyTokenObtainPairSerializer,
)   
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

User = get_user_model()


class ChangePasswordView(generics.UpdateAPIView):
    """
    Class to change password for the user.
    """
    serializer_class = UserChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response({"message": "Password Change successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Registrar el error con nivel de severidad ERROR
            logging.error(f"Error occurred during registration: {str(e)}")

            # Devolver respuesta de error con el mensaje de excepción
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ManageUserView(generics.RetrieveUpdateAPIView):
    """
        class to manage users.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data)



class LoginView(TokenObtainPairView):
    """
        Create the token for user login
    """
    serializer_class = MyTokenObtainPairSerializer



class RegisterUserAPIView(APIView):
    """
    Class for the register user.
    """
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        try:
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()

                # Generar código de verificación de 6 dígitos
                verification_code = generate_verification_code()
                VerificationCode.objects.create(user=user, code=verification_code)

                # Reutilizar la función para enviar el correo electrónico
                send_verification_email(user, verification_code)

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logging.error(f"Error occurred during registration: {str(e)}")
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyCodeView(APIView):
    """
    Class to verify the code 
    """
    throttle_classes = [UserRateThrottle]
    
    def post(self, request):
        try: 
            email = request.data.get('email')
            code = request.data.get('code')
            resend = request.data.get('resend', False)

            if not email:
                return Response({'error': 'Email is required'}, status=400)

            user = User.objects.filter(email=email).first()
            if not user:
                return Response({'error': 'User not found'}, status=404)

            # Manejo del reenvío de código con límite de tiempo
            if resend:
                verification_code = VerificationCode.objects.filter(user=user).first()

                if verification_code:
                        # Limitar el reenvío del código a un mínimo de 5 minutos
                    if verification_code.created_at + timedelta(minutes=5) > now():
                        return Response({'error': 'You can only resend the code every 5 minutes'}, status=429)

                    # Generar nuevo código y actualizar
                    verification_code.code = generate_verification_code()
                    verification_code.save()
                else:
                    verification_code = VerificationCode.objects.create(user=user, code=generate_verification_code())

                # Reutilizar la función para enviar el correo electrónico
                send_verification_email(user, verification_code.code)
                return Response({'message': 'Verification code resent successfully!'}, status=200)

            # Validar el código de verificación
            verification_code = VerificationCode.objects.filter(user=user, code=code).first()
            if not verification_code:
                return Response({'error': 'Invalid code'}, status=401)

            if verification_code.created_at + timedelta(minutes=10) < now():
                return Response({'error': 'Code has expired'}, status=401)

            # Activar usuario
            user.is_active = True
            user.save()
            return Response({'message': 'Account activated successfully!'}, status=200)

        except Exception as e:
            logging.error(f"Error occurred during verification: {str(e)}")
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""
  module to send email verification
"""

def send_verification_email(user, code):
    """
    Enviar correo electrónico de verificación.
    """
    try:
        send_mail(
            'Verifica tu correo electrónico',
            f'Por favor, ingresa el siguiente código de verificación para activar tu cuenta: {code}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
    except BadHeaderError:
        logging.error('Invalid header found while sending email.')
        return HttpResponse('Invalid header found.')
    except Exception as e:
        logging.error(f"Error sending verification email: {str(e)}")
        raise  # Lanza la excepción para que pueda ser manejada en la vista