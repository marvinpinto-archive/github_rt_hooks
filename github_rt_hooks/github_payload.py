import hashlib
import hmac
import logging

log = logging.getLogger(__name__)
header_key = 'X-Hub-Signature'

def validate_github_paylod(request, github_hook_secret):
    if not does_github_signature_header_exist(request.headers):
        return False
    if not is_github_signature_valid(request.headers, request.data, github_hook_secret):
        return False
    return True


def does_github_signature_header_exist(request_headers):
    if not header_key in request_headers:
        log.warn('HTTP header ' + header_key + ' not found!')
        return False

    signature_header = request_headers[header_key]
    log.debug(header_key + ' header is: ' + str(signature_header))
    return True


def is_github_signature_valid(request_headers, request_data, github_hook_secret):
    if not does_github_signature_header_exist(request_headers):
        return False

    sha_name, signature = request_headers[header_key].split('=')
    if sha_name != 'sha1':
        log.error(
                'Github hash function '
                + str(sha_name)
                + ' is not sha1. Unable to verify Github signature!')
        return False

    mac = hmac.new(
            github_hook_secret,
            msg=request_data,
            digestmod=hashlib.sha1)
    digest = mac.hexdigest()
    log.debug('Computed digest is ' + str(digest) + ', signature is ' + str(signature))
    return_value = (digest == signature)

    if not return_value:
        log.error('Github signature verification failed!')
    else:
        log.debug('Github signature verification passed')

    return return_value

