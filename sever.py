import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, jsonify
from play import load_files

app = Flask(__name__)
current_song = ''
music_dir = '/home/kevin/Mine/music'
player_command = './play.py'
player = subprocess.Popen(
    player_command,
    stdin=subprocess.PIPE, stdout=subprocess.PIPE)


@app.route('/')
def index():
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
  return render_template('index.html',
      music=music,
      current_song=music_name_format(current_song))

@app.route('/play')
def play():
  args = request.args
  the_music = args.get('music')
  global current_song
  current_song = the_music
  command = "play:{}\n".format(the_music)
  player.stdin.write(command.encode())
  player.stdin.flush()

  return redirect('/')

@app.route('/set_volume')
def set_volume():
  volume = request.args.get('volume', 1)
  command = "set_volume:{}\n".format(volume)
  player.stdin.write(command.encode())
  player.stdin.flush()

  return redirect('/')

@app.route('/stop')
def stop():
  command = "stop\n"
  player.stdin.write(command.encode())
  player.stdin.flush()

  return redirect('/')

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

