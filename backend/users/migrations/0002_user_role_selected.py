from django.db import migrations, models

def mark_existing_users_established(apps, schema_editor):
    apps.get_model('users', 'User').objects.update(role_selected=True)

class Migration(migrations.Migration):
    dependencies = [('users', '0001_initial')]
    operations = [
        migrations.AddField(model_name='user', name='role_selected', field=models.BooleanField(default=False)),
        migrations.RunPython(mark_existing_users_established, migrations.RunPython.noop),
    ]
