#!/usr/local/bin/ve python
import glob
import sys
import os
import pygame as pg
from time import sleep


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


def play_music(music):
  try:
    pg.mixer.music.load(music)
    pg.mixer.music.play()
  except pg.error as e:
    pass

def stop_music():
  pg.mixer.music.stop()

if __name__ == "__main__":
  music_dir = '/home/kevin/Mine/music'
  music = []
  status = 'stop'
  current_song = 'None'
  freq = 44100     # audio CD quality
  bitsize = -16    # unsigned 16 bit
  channels = 2     # 1 is mono, 2 is stereo
  buffer = 2048    # number of samples (experiment to get best sound)
  volume = 1
  pg.mixer.init(freq, bitsize, channels, buffer)
  pg.mixer.music.set_volume(volume)

  while True:
    if pg.mixer.music.get_busy() or status == 'stop':
      command = input()
      if command.startswith('play'):
        current_song = command.split(':')[1]
        music.append(current_song)
        status = 'playing'
      elif command == 'stop':
        stop_music()
        status = 'stop'
      elif command == 'current_song':
        sys.stdout.write(current_song)
      elif command.startswith('set_volume'):
        volume = command.split(':')[1]
        pg.mixer.music.set_volume(volume)
      sys.stdout.flush()

    else:
      if music == []:
        music = load_files(music_dir, True)

      if status == 'playing':
        play_music(music.pop())




