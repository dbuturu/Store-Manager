from flask_jwt_extended import get_jwt_claims, verify_jwt_in_request, get_jwt_identity

def requires_permission(s_permission):
    def decorator(fn):
        def decorated(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            if not claims:
                return {"message": "{} only".format(s_permission)}, 403
            l_permissions = claims.get('roles')
            if s_permission is l_permissions:
                return {"message": "{} only".format(s_permission)}, 403
            else:
                return fn(*args, **kwargs)
        return decorated
    return decorator


def owner_required(owner):
    def decorator(fn):
        def decorated(*args, **kwargs):
            identity = get_jwt_identity()
            if owner is identity:
                return fn(*args, **kwargs)
            return {"message": "Admins and Owner only"}, 403
        return decorated
    return decorator