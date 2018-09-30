from flask import g, request
from flask_allows import Allows, Requirement

from .errors.exceptions import UserIdFieldIsMissed


allows = Allows(identity_loader=lambda: g.current_user_id)


class UserRequirementMixin(object):
    def is_profile_owner(self, identity):
        return identity == request.view_args['user_id']

    def fulfill(self, identity):
        return self.is_profile_owner(identity)


class CanUpdateProfile(UserRequirementMixin, Requirement):
    pass


class CanDeleteProfile(UserRequirementMixin, Requirement):
    pass
