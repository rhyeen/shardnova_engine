""" Container for HttpRequester
"""
import json
from base64 import urlsafe_b64encode
from hashlib import sha256
from time import time, sleep
import requests
import jwt  # pip install pyjwt
from urllib.request import urlopen, Request

class HttpRequester(object):
    """ Simple wrapper over requests to make all simple HTTP requests condensed down into one
        method call.
    """

    @staticmethod
    def construct_url(base_url, endpoint=None, data_center=None):
        """ Constructs a URL based on a given base_url, endpoint, and data_center.
            Overly simplified at this point.
        """
        url = base_url
        if endpoint:
            url += endpoint
        if data_center:
            url = data_center + url
        return url

    @staticmethod
    def get_stream(url,
                   request_body=None,
                   jwt_token=None,
                   additional_headers=None):
        """
        This method allows us to use something like ijson
        to load the response.
        """
        headers = HttpRequester._get_headers(jwt_token=jwt_token,
                                             additional_headers=additional_headers)
        data = None
        if request_body:
            data = json.dumps(request_body)
        request = Request(url, data=data, headers=headers)
        response = urlopen(request)
        return response

    @staticmethod
    def get_response_object(url,
                            request_type,
                            params=None,
                            request_body=None,
                            jwt_token=None,
                            additional_headers=None,
                            prevent_status_error=False,
                            verbose_error=False,
                            retry=0):
        """ A wrapper around the Python requests library
                Args:
                    url (STRING): URL of request. URL parameters should be passed to `params`
                    request_type (STRING): Must be 'GET', 'POST', 'PUT', or 'DELETE'
                    params (DICT, optional): Dict of parameters to pass into the URL
                    request_body (DICT, optional): Dict body. Expected JSON-like object.
                    jwt_token (STRING, optional): JWT-TOKEN, if it exists
                    additional_headers (DICT, optional): Any additional headers beyond
                        `'Content-Type': 'application/json'`.
                        You can provide a `Content-Type` if you'd like to override that default.
                Returns:
                    Response

                Raises:
                    ValueError: If request_type is not a valid type
                    HTTPError: If response status is not 200 OK
                """
        headers = HttpRequester._get_headers(jwt_token=jwt_token,
                                             additional_headers=additional_headers)
        data = None
        if request_body:
            data = json.dumps(request_body)
        try:
            if request_type == 'GET':
                response = requests.get(url, headers=headers, params=params, data=data)
            elif request_type == 'POST':
                response = requests.post(url, headers=headers, params=params, data=data)
            elif request_type == 'PUT':
                response = requests.put(url, headers=headers, params=params, data=data)
            elif request_type == 'DELETE':
                response = requests.delete(url, headers=headers, params=params)
            else:
                raise ValueError(('request_type must be "GET", "POST", "PUT", or "DELETE",'
                                  ' found: {0}').format(request_type))
        # Once in a blue-moon, been getting: 'EOF occurred in violation of protocol (_ssl.c:720)'
        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as exception:
            if retry > 0:
                sleep(30)
                return HttpRequester.get_response_object(url,
                                                         request_type,
                                                         params,
                                                         request_body,
                                                         jwt_token,
                                                         additional_headers,
                                                         prevent_status_error,
                                                         verbose_error,
                                                         retry - 1)
            raise exception
        try:
            if not prevent_status_error:
                response.raise_for_status()
        except requests.exceptions.HTTPError as exception:
            if retry > 0:
                sleep(3)
                return HttpRequester.get_response_object(url,
                                                         request_type,
                                                         params,
                                                         request_body,
                                                         jwt_token,
                                                         additional_headers,
                                                         prevent_status_error,
                                                         verbose_error,
                                                         retry - 1)
            if not verbose_error:
                raise exception
            try:
                message = ('\n\nFailed HTTP Request:\n'
                           'REQUEST: {request_type} {url}\n'
                           'Headers: {headers}\n'
                           'Body:\n'
                           '{request_body}\n\n'
                           'RESPONSE:\n'
                           'Status: {status}\n'
                           'Message: {message}\n'
                           .format(request_type=request_type,
                                   url=response.url,
                                   headers=headers,
                                   request_body=data,
                                   status=response.status_code,
                                   message=response.content))
            except Exception as exception:
                message = 'Unable to Stringify HTTP Request: {0}'.format(str(exception))
            raise requests.exceptions.HTTPError('{0}\nOriginal Error:\n{1}'
                                                .format(message, str(exception)))
        return response

    @staticmethod
    def get_response_json(url,
                          request_type,
                          params=None,
                          request_body=None,
                          jwt_token=None,
                          additional_headers=None,
                          prevent_status_error=False,
                          verbose_error=False,
                          retry=0):
        """ A wrapper around the Python requests library
        Args:
            url (STRING): URL of request. URL parameters should be passed to `params`
            request_type (STRING): Must be 'GET', 'POST', 'PUT', or 'DELETE'
            params (DICT, optional): Dict of parameters to pass into the URL
            request_body (DICT, optional): Dict body. Expected JSON-like object.
            jwt_token (STRING, optional): JWT-TOKEN, if it exists
            additional_headers (DICT, optional): Any additional headers beyond
                `'Content-Type': 'application/json'`.  You can provide a `Content-Type` if you'd
                like to override that default.
        Returns:
            DICT: Returns the json response payload of the provided request.
        Raises:
            ValueError: If request_type is not a valid type
            HTTPError: If response status is not 200 OK
        """
        response = HttpRequester.get_response_object(url,
                                                     request_type,
                                                     params,
                                                     request_body,
                                                     jwt_token,
                                                     additional_headers,
                                                     prevent_status_error,
                                                     verbose_error,
                                                     retry)
        try:
            response_json = response.json()
        except ValueError:
            return response.content
        return response_json

    @staticmethod
    def _get_headers(api_token=None, jwt_token=None, additional_headers=None):
        headers = {
            'Content-Type': 'application/json'
        }
        if jwt_token:
            headers['X-JWT'] = jwt_token
        return HttpRequester._merge_dicts(headers, additional_headers)

    @staticmethod
    def get_jwt_token(secret,
                      request_method=None,
                      aud='qualtrics',
                      iss='qualtrics',
                      set_default_exp=True,
                      additional_payload=None,
                      qualtrics_specific_params=None):
        """
        :param secret: jwt secret string
        :param request_method: 'GET','POST','PUT','DELETE'
        :param aud: audience claim string
        :param iss: issuer claim string
        :param set_default_exp: True to use default expiration, False otherwise
        :param additional_payload: dictionary, could include custom expiration
        :return: jwt token string
        """
        payload = {}
        if aud:
            payload['aud'] = aud
        if iss:
            payload['iss'] = iss
        if request_method:
            payload['method'] = request_method
        if set_default_exp:
            exp = int(round(time()) + 3000)
            payload['exp'] = exp
        if additional_payload:
            payload = HttpRequester._merge_dicts(payload, additional_payload)
        encoded = jwt.encode(payload, secret, algorithm='HS256')
        return encoded

    @staticmethod
    def _merge_dicts(dict1, dict2):
        if not dict1:
            return dict2
        if not dict2:
            return dict1
        final_dict = dict1.copy()
        final_dict.update(dict2)
        return final_dict
