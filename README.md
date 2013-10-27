biauthorize
===========
Biometrics Authorization Server

## RESTful API

### Establish a user image

#### Description:
Enables a user to sign up to our service. It creates a 
reference image on the server in a well defined location.

#### Call: 
    `POST /reference/<int:userId>`

#### Parameters:
**userId**: The id of the user that is going to be entered to the system

#### Post form:
    {
        image: <Base64 String>
    }

#### Returns:
##### On success:
    {
        response_code: <int: 200>
    }

##### On failure:
    {
        response_code: <int: 500>
    }

### Check a user image

### Description
Checks a a user image that is sent to the server in the post form against
the reference image of the user id.

#### Call:
    `POST /check/<userId>`

#### Paramters:
**userId**: The id of the user that is going to be checked against in the system.

#### Post form:
    {
        image: <Base64 String>
    }

#### Returns:
##### On Success:
    {
        response_code: <int: 200>,
        similarity_metric: <float: f between [0, 1]>,
        hist_similarity: <float: f between [0, 1]>
    }

##### On Failure:
    {
        response_code: <int: 500>
    }

## Directory Layout
    temp/
        <userId>.jpg

    reference/
        <userId>.jpg

