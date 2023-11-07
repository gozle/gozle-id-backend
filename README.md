# Gozle ID
The OAuth2 provider and REST Api for Gozle ID.

## Client Registration
New application Client can be registered at https://i.gozle.com.tm/o/admin/applications


## The Authorization Request
Clients will direct a user’s browser to the authorization server to begin the OAuth process. Clients may use either the **authorization code** grant type or the **implicit** grant. Along with the type of grant specified by the _response_type_ parameter, the request will have a number of other parameters to indicate the specifics of the request.

Server-Side Apps describes how clients will build the authorization URL for your service. The first time the authorization server sees the user will be this authorization request, the user will be directed to the server with the query parameters the client has set. At this point, the authorization server will need to validate the request and present the authorization interface, allowing the user to approve or deny the request.
Request Parameters

The following parameters are used to begin the authorization request. For example, if the authorization server URL is https://id.gozle.com.tm/o/authorize then the client will craft a URL like the following and direct the user’s browser to it:
```
https://id.gozle.com.tm/o/authorize?response_type=code
&client_id=29352735982374239857
&redirect_uri=https://mysite.com/api/auth
&scope=create+delete
&state=xcoivjuywkdkhvusuye3kch
```

+ ### response_type
_response_type_ will be set to code, indicating that the application expects to receive an _authorization code_ if successful.

+ ### client_id
The _client_id_ is the public identifier for the app.

+ ### redirect_uri (optional)
The _redirect_uri_ is not required by the spec, but your service should require it. This URL must match one of the URLs the developer registered when creating the application, and the authorization server should reject the request if it does not match.

+ ### scope (optional)
The request may have one or more _scope_ values indicating additional access requested by the application. The authorization server will need to display the requested scopes to the user.

+ ### state (recommended)
The _state_ parameter is used by the application to store request-specific data and/or prevent CSRF attacks. The authorization server must return the unmodified _state_ value back to the application.

+ ### PKCE
If the authorization server supports the PKCE extension (described in PKCE) then the _code_challenge_ and _code_challenge_method_ parameters will also be present. These must be remembered by the authorization server between issuing the authorization code and issuing the access token.

The client first creates a code verifier, "_code_verifier_", for each
OAuth 2.0. Authorization Request, in the following manner:

```
code_verifier = high-entropy cryptographic random STRING
  using the unreserved characters [A-Z] / [a-z] / [0-9] / "-" / "." / "_" / "~"
  with a minimum length of 43 characters and a maximum length of 128 characters
```

The client then creates a code challenge derived from the code
verifier by using one of the following transformations on the code
verifier:
+ plain
    - code_challenge = code_verifier

+ S256
    - code_challenge = BASE64URL-ENCODE(SHA256(ASCII(code_verifier)))

For example in Python3:
```
import random
import string
import base64
import hashlib

code_verifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))

code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')
```

Full url would look like this
```
https://id.gozle.com.tm/o/authorize?response_type=code
&code_challenge=XRi41b-5yHtTojvCpXFpsLUnmGFz6xR15c3vpPANAvM
&code_challenge_method=S256
&client_id=vW1RcAl7Mb0d5gyHNQIAcH110lWoOW2BmWJIero8
&redirect_uri=https://mysite.com/api/auth
```
For the sake if example we used https://mysite.com/api/auth as redirect_uri you will get a Page not found (404) but it worked if you get a url like:
```
https://mysite.com/api/auth?code=uVqLxiHDKIirldDZQfSnDsmYW1Abj2
```
This is the OAuth2 provider trying to give you a code. in this case ***uVqLxiHDKIirldDZQfSnDsmYW1Abj2***.

+ ### Verifying the Authorization Request
The authorization server must first verify that the client_id in the request corresponds to a valid application.

If your server allows applications to register more than one redirect URL, then there are two steps to validating the redirect URL. If the request contains a redirect_uri parameter, the server must confirm it is a valid redirect URL for this application. If there is no redirect_uri parameter in the request, and only one URL was registered, the server uses the redirect URL that was previously registered. Otherwise, if no redirect URL is in the request, and no redirect URL has been registered, this is an error.

If the client_id is invalid, the server should reject the request immediately and display the error to the user rather than redirecting the user back to the application.
