from drf_yasg import openapi

JWT_TOKEN = openapi.Parameter("Authorization", openapi.IN_HEADER, required=True, description="JWT Token of user. "
                                                                                             "Example:\nAuthorization"
                                                                                             ": Bearer"
                                                                                             "<token>",
                              type=openapi.TYPE_STRING)

OAUTH_TOKEN = openapi.Parameter("Authorization", openapi.IN_HEADER, required=True, description="OAuth Token of user. "
                                                                                               "Example:\nAuthorization"
                                                                                               ": Bearer"
                                                                                               "<token>",
                                type=openapi.TYPE_STRING)

CLIENT_ID = openapi.Parameter("client_id", openapi.IN_QUERY, required=True, description="ID of Client",
                              type=openapi.TYPE_STRING)

PAYMENT_ID = openapi.Parameter("payment_id", openapi.IN_QUERY, required=True, description="ID of Payment",
                               type=openapi.TYPE_STRING)

PHONE_NUMBER = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='phone_number'),
    }
),
