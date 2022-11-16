
# from django.dispatch import receiver
# from django.db.models.signals import pre_save, post_save

# from django.contrib.auth.models import Group, Permission
# from django.core.exceptions import ObjectDoesNotExist

# from yuugen.apps.core.profile import  get_or_create_store_proxy_user

# from yuugen.apps.users.models import (
#     UserCreation,
#     CustomerBillingDetail,
#     CustomerShippingDetail,
#     CustomerMarketingDetail,

# )


# @receiver(pre_save, sender=UserCreation)
# def customer_pre_save_created_by(sender, instance, *args, **kwargs):
#     '''
#     Deal with foreignkey on self UserCreation with django pre_save method for customer registration
#     get or create a proxy user for the store with the function get_or_create_store_proxy_user()
#     check if instance email is from the proxy user as this user already have admin as created by
#     will be extended for other apps
#     '''
#     print(f'signals pre_save hitted')
#     print(f'instance email: {instance.email}')
#     print(f'instance staff: {instance.is_staff}')
#     print(f'instance manager: {instance.is_manager}')
#     print(f'instance id: {instance.id}')
#     if not instance.is_staff and not instance.is_manager and instance.id is None and instance.email != 'store@email.com':
#         store_proxy = get_or_create_store_proxy_user()
#         try:
#             instance.created_by = UserCreation.objects.get(email = store_proxy.email)
#         except Exception as e:
#             print(f"user_pre_save_receiver sent error as {e}")
#     else:
#         pass


# @receiver(post_save, sender=UserCreation)
# def customer_post_save_groups(sender, instance, *args, **kwargs):
#     if instance.url_creation:
#         print(f'post save hitted, path = {instance.url_creation}')
#         group = Group.objects.get_or_create(name=instance.url_creation)
#         if group:
#             accreditation = Group.objects.get(name=group[0])
#             print(f'accreditation : {accreditation.id}')
#         try:
#             instance.groups.add(Group.objects.get(id = accreditation.id))
#         except Exception as e:
#             print(f"user_pre_save_receiver sent error as {e}")

