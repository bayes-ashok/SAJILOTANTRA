
import ckeditor.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField()),
                ('start', models.DateField(blank=True, null=True)),
                ('end', models.DateField(blank=True, null=True)),
                ('Location', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('suggestion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='GovernmentProfile',
            fields=[
                ('profile_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('thumbnail', models.ImageField(upload_to='static/thumbnails/')),
                ('description', ckeditor.fields.RichTextField()),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Guidance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', ckeditor.fields.RichTextField()),
                ('thumbnail', models.ImageField(upload_to='static/thumbnails/')),
                ('category', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notice_id', models.AutoField(primary_key=True, serialize=False)),
                ('notice_title', models.CharField(max_length=500)),
                ('notice_description', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('posted_by', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encoded_caption', models.TextField()),
                ('category', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/post_images/')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('like_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('encoding_dict', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReportedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.IntegerField()),
                ('reason', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='static/assets/images/defaultuser.png', upload_to='static/profile_images/')),
                ('cover', models.ImageField(blank=True, default='static/assets/images/default_cover.png', upload_to='static/cover_images/')),
                ('bio', models.CharField(blank=True, max_length=255, null=True)),
                ('forget_password_token', models.CharField(default='', max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='static/feedback_files/')),
                ('feedback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SajilotantraApp.feedback')),
            ],
        ),
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SajilotantraApp.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SajilotantraApp.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SajilotantraApp.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SajilotantraApp.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SajilotantraApp.userprofile'),
        ),
    ]
