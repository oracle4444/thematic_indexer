from django.db import models


class Classes(models.Model):
    c_name = models.CharField(name='name', max_length=200)

    def __str__(self):
        return self.name


class Videos(models.Model):
    v_name = models.CharField(name='name', max_length=200)
    v_file = models.FileField(name='file', upload_to='detector/static/detector/videos')


class Instances(models.Model):
    i_video = models.ForeignKey(Videos, name='video', on_delete=models.CASCADE)
    i_class = models.ForeignKey(Classes, name='class', on_delete=models.CASCADE)
    i_first_frame = models.IntegerField(name='first_frame')
    i_last_frame = models.IntegerField(name='last_frame')
    i_track_number = models.IntegerField(name='track_number')
