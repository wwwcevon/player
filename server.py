import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, jsonify
from play import load_files, play_music, set_volume, stop_music, next_music

app = Flask(__name__)
current_song = ''
music_dir = '/home/kevin/Mine/music'
current_volume = 1

@app.route('/songs', methods=['POST'])
def songs():
  music_files = load_files(music_dir)
  music = []
  for dir in music_files:
    music.append(
        {'dir': dir['path'],
          'files': []}
    )
    for f in dir['files']:
      music[-1]['files'].append(
        {'name': music_name_format(f),
         'file': f}
      )
  return jsonify({'songs': music})


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
  the_music = request.json.get('song')
  global current_song
  current_song = the_music
  play_music(the_music)

  return jsonify({'status': 'success'})

@app.route('/set_volume', methods=['POST'])
def volume():
  global current_volume
  current_volume += float(request.json.get('volume', 0))
  set_volume(current_volume)

  return jsonify({'current_volume': current_volume})

@app.route('/stop', methods=['POST'])
def stop():
  stop_music()
  return jsonify({'status': 'success'})

@app.route('/next', methods=['POST'])
def next():
  next_music()
  return jsonify({'status': 'success'})

def music_name_format(music):
  if type(music) is not list:
    music = [music]
  for idx, m in enumerate(music):
    m = m.split('/')[-1]
    music[idx] = m.replace('.mp3','')
  if len(music) == 1:
    music = music[0]
  return music

if __name__ == "__main__":
  app.debug = True
  app.run(host='0.0.0.0')

