from drf_yasg import openapi

JWT_TOKEN = openapi.Parameter("Authorization", openapi.IN_HEADER, description="JWT Token of user. "
                                                                              "Example:\nAuthorization: Bearer "
                                                                              "<token>", type=openapi.TYPE_STRING)

PHONE_NUMBER = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='phone_number'),
    }
),
