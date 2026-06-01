from django.contrib.auth.models import Group

def fix_register():
    with open('/app/courses/api.py', 'r') as f:
        content = f.read()
    
    old_code = '    group, _ = Group.objects.get_or_create(name=data.role)\n    user.groups.add(group)'
    
    new_code = '''    # PERBAIKAN: Jika role teacher, gunakan group instructor
    if data.role == "teacher":
        group_name = "instructor"
    else:
        group_name = data.role
    
    group, _ = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)'''
    
    content = content.replace(old_code, new_code)
    
    with open('/app/courses/api.py', 'w') as f:
        f.write(content)
    
    print('Fix applied!')

fix_register()
