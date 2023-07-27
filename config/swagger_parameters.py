from drf_yasg import openapi

JWT_TOKEN = openapi.Parameter("Authorization", openapi.IN_HEADER, description="JWT Token of user. "
                                                                              "Example:\nAuthorization: Bearer "
                                                                              "<token>", type=openapi.TYPE_STRING)

PHONE_NUMBER = openapi.Parameter("phone_number", openapi.IN_FORM, description="Phone number", type=openapi.TYPE_STRING)

VERIFICATION_CODE = openapi.Parameter("verification-code", openapi.IN_FORM, description="Verification code",
                                      type=openapi.TYPE_STRING)
