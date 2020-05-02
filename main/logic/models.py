# from django.contrib.auth.models import User
# from main.models import Customers, Orders
#
#
# class UserClass(User):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     def initialize(self, user_name, password, email, first_name, last_name):
#         self.username = user_name
#         self.email = email
#         self.password = password
#         self.first_name = first_name
#         self.last_name = last_name
#
#     def register(self, user_name, password, email):
#         self.username = str(user_name)
#         self.email = str(email)
#         self.password = str(password)
#
#     def check_registration(self):
#
#         if self.username != "" and self.email != "" and self.password != "":
#             return True
#         else:
#             return False
#
#     def load(self, data):
#         return
#
#
# class OrderClass(Orders):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     def initialize(self):
#         return
#
#     def load(self, data):
#         return
#
#     def data(self):
#         return
#
#
#
