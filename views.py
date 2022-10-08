from django.shortcuts import render
from django.http import HttpResponse
from .forms import AudioForm
import speech_recognition as sr
from .models import Audio_store
import pandas as pd
from googletrans import Translator

import IPython
from scipy.io import wavfile
import noisereduce as nr
import soundfile as sf
from noisereduce.generate_noise import band_limited_noise
import urllib.request
import numpy as np
import io

# Create your views here.
def Audio_sto(request):
    
    if request.method == 'POST': 
        form = AudioForm(request.POST,request.FILES or None) 
        if form.is_valid(): 
            form.save() 
            print('successfully uploaded')
        r = sr.Recognizer()
        r.pause_threshold=99.99
        d=Audio_store.objects.latest('id')
        print("Path of Audio file",d)
        with sr.AudioFile(d.record) as source:
            audio_text = r.listen(source)
            text = r.recognize_google(audio_text)
            print(text)
            translate = Translator()
            lang = translate.detect(text)
            slang=(lang.lang)
            print("-------------------")
            print(type(slang))
            print("-------------------")
            audio = r.listen(source)
            if(type(slang)==list):
                ctext = r.recognize_google(audio_text,language=slang[0])
            else:
                ctext = r.recognize_google(audio_text,language=slang)
            print(ctext)
        return render(request,'aud.html',{'Data1':lang,'Data':ctext})
        return render(request,'aud.html',{})
    else:   
        form = AudioForm() 
        return render(request, 'aud.html', {'form' : form}) 
    return render(request, 'aud.html', {'form' : form}) 



def stringToList(string):
    listRes = list(string.split(" "))
    return listRes