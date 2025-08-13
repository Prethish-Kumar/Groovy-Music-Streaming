from flask import Flask, render_template, request, redirect, url_for,session
import scripts.LoginFlow as LoginFlow
import scripts.SignUpFlow as SignUpFlow
import scripts.CreatorSignup as CreatorSignup
import scripts.Songs_db as Songs_db
import scripts.Album_db as Album_db
import scripts.Playlist_db as Playlist_db
import scripts.Users_db as Users_db
import os

app = Flask(__name__)
app.secret_key = 'IITM'


@app.route('/')
def index():
    return render_template("index.html")

# Sign Up, Login & Logout

@app.route('/signup' , methods = ["GET","POST"])
def signup():
    if request.method == "POST":
        user = request.form["user"]
        email = request.form["email"]
        passw = request.form["passw"]
        passw2 = request.form["passw2"]
        if(passw == passw2):
            SignUpFlow.new_user(user,email,passw)
            return redirect("/login")
        return render_template("usersignup.html")
    return render_template("usersignup.html")

@app.route('/login', methods = ["GET","POST"])
def login():
    if request.method == "POST":
       user = request.form["email"]
       passw = request.form["password"]
       if LoginFlow.login_user(user,passw):
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        session['username'] = LoginFlow.getUserName(user)
        session['role'] = LoginFlow.getRole(user)
        print("User " + session['username'] + " Has Logged In!")
        return redirect("/home")
       else:
           return render_template("userlogin.html")
    else:
        return render_template("userlogin.html")
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")

@app.route('/creatorsignup', methods = ["GET","POST"])
def creatorsignup():
    if request.method == "POST":
        if(session['role'] == 1):
            if(request.form["email"] == session['email'] and request.form["password"] == session['password']):
                CreatorSignup.new_creator(CreatorSignup.get_id(session['username'])[0])
                return 'Form Submitted Successfully - Admin Will Review Your Request & Approve Within 7 Business Days'
            else:
                return 'Error! You Are Either Trying To Apply With A Different Account OR You Have Entered Wrong Details.'
        else:
            return "Error! You are already creator or above. You must be a user to apply for creator account"
    return render_template("creatorsignup.html", username = session['username'])


# Home

@app.route('/home')
def home():
    if 'email' in session:
        username = session['username']
        songs = Songs_db.get()
        albums = Album_db.get()
        playlists = Playlist_db.get_by_creator(session['username'])
        return render_template('home.html', songs=songs,albums = albums ,username=username,playlists=playlists)
    else:
        return redirect("/login")

@app.route('/userdashboard')
def userdashboard():
    if 'role' in session:
        if(session['role'] == 1):
            return render_template("userdashboard.html",username = session['username'])
        if(session['role'] == 2):
            return redirect("/creator")
        if(session['role'] == 3):
            return redirect("/admin")
    return "Unauthorized", 401
    
# Dashboard
@app.route('/showcreators')
def showcreators():
    creators = CreatorSignup.get()
    return render_template("showcreators.html",username = session['username'],creators=creators) 

@app.route('/showusers')
def show_users():
    users = CreatorSignup.get()
    return render_template("showusers.html",username = session['username'],users=users) 

@app.route('/showsongs')
def show_songs():
    songs = Songs_db.get()
    return render_template("showsongs.html",username = session['username'],songs=songs) 

@app.route('/showalbums')
def show_albums():
    albums = Album_db.get()
    return render_template("showalbums.html",username = session['username'],albums=albums) 

@app.route('/search')
def search():
    keyword = request.args.get('q', default='', type=str)
    songs = Songs_db.search(keyword)
    albums = Album_db.search(keyword)
    return render_template("search.html",songs=songs,albums=albums) 

@app.route('/song/<int:song_id>')
def play_song(song_id):
    song = Songs_db.find(song_id)
    playlists = Playlist_db.get_by_creator(session['username'])
    return render_template('playsong.html', username = session['username'],song=song,playlists=playlists)

@app.route('/album/<int:album_id>')
def play_album(album_id):
    album = Album_db.find(album_id)
    songs = Album_db.findsongs(album_id)
    return render_template('album.html', username = session['username'],album=album,songs=songs)

@app.route('/createplaylist')
def createplaylist():
    return render_template("createplaylist.html",username = session['username'])



@app.route('/admin', methods = ["GET","POST"])
def admin():
    songs_data = Songs_db.get()
    album_data = Album_db.get()
    creators = CreatorSignup.get()
    usercount = CreatorSignup.usercount()
    creatorcount = CreatorSignup.creatorcount()  
    songcount = Songs_db.count()
    albumcount = Album_db.count()
    return render_template("admin.html",username = session['username'],songs_data=songs_data,album_data=album_data,creators=creators,usercount=usercount,creatorcount=creatorcount,songcount=songcount,albumcount=albumcount)

@app.route('/playlist/<int:playlist_id>')
def playlist(playlist_id):
    playlist =  Playlist_db.get_by_id(playlist_id)
    songs = Playlist_db.getSongsForPlaylist(playlist_id)
    return render_template("playlist.html",username = session['username'],songs=songs,playlist=playlist) 

@app.route('/creator')
def creator():
    albums = Album_db.get_by_creator(session['username'])
    songs = Songs_db.get_by_creator(session['username'])
    songscount = Songs_db.count_by_username(session['username'])
    albumscount = Album_db.count_by_username(session['username'])
    return render_template("creator.html",username = session['username'],albums = albums,songs=songs,songscount=songscount,albumscount=albumscount) 

@app.route('/newsong', methods = ["GET"])
def newsong():
    return render_template("newsong.html", username = session['username']) 

@app.route('/newalbum', methods = ["GET","POST"])
def newalbum():
    if request.method == "POST":
        albumname = request.form["albumname"]
        Album_db.add(albumname)
        return "Request Sent Successfully!"
    
    return render_template("newalbum.html",username = session['username']) 

MUSIC_UPLOAD_FOLDER = 'static/music'
LYRICS_UPLOAD_FOLDER = 'static/lyrics'

app.config['MUSIC_UPLOAD_FOLDER'] = MUSIC_UPLOAD_FOLDER
app.config['LYRICS_UPLOAD_FOLDER'] = LYRICS_UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp3', 'txt'}

def clean_filename(filename):
    # Replace spaces with hyphens in the filename
    return filename.replace(' ', '-')

@app.route('/newsong', methods=['POST'])
def upload_file():
    
    if 'lyricsFile' not in request.files or 'songFile' not in request.files:
        return 'No file part'

    lyrics_file = request.files['lyricsFile']
    song_file = request.files['songFile']

    if lyrics_file.filename == '' or song_file.filename == '':
        return 'No selected file'

    if not allowed_file(lyrics_file.filename) or not allowed_file(song_file.filename):
        return 'Invalid file format. Allowed formats are: .mp3 for submitting songs & .txt for submitting lyrics'
    
    clean_lyrics_filename = clean_filename(lyrics_file.filename)
    clean_song_filename = clean_filename(song_file.filename)

    lyrics_file_path = os.path.join(app.config['LYRICS_UPLOAD_FOLDER'], clean_lyrics_filename)
    song_file_path = os.path.join(app.config['MUSIC_UPLOAD_FOLDER'], clean_song_filename)

    lyrics_file.save(lyrics_file_path)
    song_file.save(song_file_path)

    print(f"Cleaned Lyrics file saved at: {os.path.abspath(lyrics_file_path)}")
    print(f"Cleaned Song file saved at: {os.path.abspath(song_file_path)}")

    Songs_db.add(session['username'],request.form['songname'],clean_song_filename,clean_lyrics_filename)

    return 'Files uploaded successfully'



# POST REQUESTS

@app.route('/approvesong', methods=['POST'])
def approvesong():
    if request.method == "POST":
        sond_id = request.form['song_id']
        Songs_db.approve(sond_id)
    return redirect("/admin")

@app.route('/approvealbum', methods=['POST'])
def approvealbum():
    if request.method == "POST":
        album_id = request.form['album_id']
        Album_db.approve(album_id)
    return redirect("/admin")

@app.route('/approvecreator', methods=['POST'])
def approvecreator():
    if request.method == "POST":
        creator_id = request.form['creator_id']
        CreatorSignup.approve(creator_id)
    return redirect("/admin")

@app.route('/addtoalbum', methods=['POST'])
def addtoalbum():
    if request.method == "POST":
        album_id = request.form['album_id']
        song_id = request.form['song_id']
        Songs_db.addtoalbum(song_id,album_id)
    return redirect("/admin")

@app.route('/newplaylist', methods=['POST'])
def newplaylist():
    if request.method == "POST":
        playlist_name = request.form['playlistName']
        Playlist_db.add(session['username'],playlist_name)
    return redirect("/home")

@app.route('/addtoplaylist/<int:song_id>', methods=['POST'])
def addtoplaylist(song_id):
    if request.method == "POST":
        playlist_id = request.form['playlist_id']
        Playlist_db.addtoplaylist(song_id,playlist_id)
        return redirect("/song/"+ str(song_id))
    return 'You can only POST to this route.'