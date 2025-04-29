from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import yt_dlp
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        quality = request.form['quality']

        if not url or not quality:
            flash("Please enter a URL and select a quality.", "danger")
            return redirect(url_for('index'))

        ydl_opts = {
            'format': f'bestvideo[height={quality}]+bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            flash("Download and merge complete.", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")

        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
