from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import get_list_or_404, get_object_or_404

from .models import Classes, Instances, Videos
from .detector import Detector

import cv2


def start_page(request):
    template = loader.get_template('detector/start_page.html')
    context = {}
    return HttpResponse(template.render(context, request))


def process(request):
    if request.method == 'POST':
        for file in request.FILES.dict():
            file = request.FILES.dict()[file]
            try:
                get_object_or_404(Videos, name=file.name)
            except Http404:
                video = Videos.objects.create(file=file, name=file.name)
                name = video.name
                input_file = "detector/static/detector/videos/{}".format(name)
                det = Detector()
                det.detect(input_file=input_file)
    return HttpResponse("processed")


def detector(request):
    template = loader.get_template('detector/detector.html')
    context = {}
    return HttpResponse(template.render(context, request))


def classes(request):
    template = loader.get_template('detector/classes.html')
    try:
        classes = get_list_or_404(Classes)
        classes.sort(key=lambda cl: cl.name)
        context = {'classes': classes}
    except Http404:
        context = {'classes': []}
    return HttpResponse(template.render(context, request))


def videos(request, class_name):
    template = loader.get_template('detector/videos.html')
    cl = get_object_or_404(Classes, name=class_name)
    try:
        videos = get_list_or_404(Instances, class_id=cl.id)
        videos = {video.video.name for video in videos}
        videos = list(videos)
        videos.sort()
        context = {'class': cl, 'videos': videos}
    except Http404:
        context = {'class': cl, 'videos': []}
    return HttpResponse(template.render(context, request))


def instances(request, class_name, video_name):
    template = loader.get_template('detector/instances.html')
    cl = get_object_or_404(Classes, name=class_name)
    video_id = get_object_or_404(Videos, name=video_name)
    instances = get_list_or_404(Instances, class_id=cl.id, video_id=video_id)
    instances.sort(key=lambda instance: instance.id)
    context = {'instances': instances, 'video': video_name}
    return HttpResponse(template.render(context, request))


def video_fragment(request, class_name, video_name, instance_id):
    template = loader.get_template('detector/video_fragment.html')
    instance = get_object_or_404(Instances, id=instance_id)
    input_file = 'detector/static/detector/videos/{}'.format(video_name)
    cap = cv2.VideoCapture(input_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    poster = '{}.png'.format(instance_id)
    context = {'instance': instance, 'video': video_name, 'poster': poster, 'fps': fps}
    return HttpResponse(template.render(context, request))
