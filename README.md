biauthorize
===========
Biometrics Authorization Server

## RESTful API

### Establish a user image
#### Call: 
    `POST /reference/<int:userId>`

#### Parameters:
**userId**: The id of the user that is going to be entered to the system

#### Post form:
    {
        image: <Base64 String>
    }

#### Returns:
On success:
    '''
    {
        response_code: <int: 200>,
        similarity_metric: <float: f in [0, 1]>,
        hist_similarity: <float: f in [0, 1]>
    }
    '''
On failure:
    {
        response_code: <int: 500>
    }
### Check a user image
    `POST /check/<userId>`
