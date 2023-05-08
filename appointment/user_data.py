
def get_user_info(self):
    user = {
        'full_name': self.request.user,
        'email': self.request.user.email,

    }
    return user
