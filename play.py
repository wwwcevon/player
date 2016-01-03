#!/usr/local/bin/ve python
import random
import threading
import glob
import sys
import os
import pygame as pg
from time import sleep

music_dir = '/home/kevin/Mine/music'
music = []
freq = 44100         # audio CD quality
bitsize = -16        # unsigned 16 bit
channels = 2         # 1 is mono, 2 is stereo
buffer = 2048        # number of samples (experiment to get best sound)
volume = 1
pg.mixer.init(freq, bitsize, channels, buffer)
pg.mixer.music.set_volume(volume)
status = 'stop'

def load_files(dir, only_files=False):
    music = []
    if only_files:
        for (dirpath, dirnames, filenames) in os.walk(dir):
            for f in filenames:
                music.append('{}/{}'.format(dirpath, f))
        return music
    for sub_dir in os.listdir(dir):
        _dir = os.path.join(dir, sub_dir)
        music.append({
            'path': sub_dir,
            'files': glob.glob('{}/*.mp3'.format(_dir))
        })

    return music

def play_music(song):
    global status
    if pg.mixer.music.get_busy():
        stop_music()
    player = threading.Thread(target=_play, kwargs={'m':song})
    player.start()
    status = 'playing'


def set_volume(volume):
    pg.mixer.music.set_volume(volume)

def _play(m):
    global status
    other_music = load_files(music_dir, True)
    try:
        pg.mixer.music.load(m)
        pg.mixer.music.play()
        clock = pg.time.Clock()
        while pg.mixer.music.get_busy() and status == 'playing':
            clock.tick(1)

    except pg.error as e:
        pass
    while status == 'playing':
        m = random.choice(other_music)
        try:
            pg.mixer.music.load(m)
            pg.mixer.music.play()
            clock = pg.time.Clock()
            while pg.mixer.music.get_busy():
                clock.tick(1)

        except pg.error as e:
            pass

def stop_music():
    global status
    status = 'stop'
    pg.mixer.music.stop()

def next_music():
    pg.mixer.music.stop()
