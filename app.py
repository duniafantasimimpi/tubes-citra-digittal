from flask import Flask, render_template, request, redirect, url_for
import base64
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'dataset'

# ========== ROUTES ==========

# 1. Halaman utama - Pendaftaran Wajah (GET)
@app.route('/', methods=['GET'])
@app.route('/wajah', methods=['GET'])
def halaman_wajah():
    return render_template('wajah.html')

# 2. Halaman Absensi Kamera (GET)
@app.route('/absensi', methods=['GET'])
def halaman_absensi():
    return render_template('absensi.html')

# 3. Proses Upload Foto Pendaftaran (POST)
@app.route('/daftar', methods=['POST'])
def proses_daftar():
    nama = request.form.get('nama', '')
    foto = request.files.get('foto')
    
    if foto and nama:
        # Buat nama file unik dengan timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{nama}_{timestamp}.jpg"
        
        # Simpan file ke folder dataset
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        foto.save(path)
        print(f"[SUCCESS] Foto {nama} disimpan sebagai {filename}")
    
    # Redirect ke halaman absensi setelah berhasil
    return redirect(url_for('halaman_absensi'))

# 4. Proses Absensi dari Kamera (POST)
@app.route('/proses', methods=['POST'])
def proses_absensi():
    nama = request.form.get('nama', '')
    image_data = request.form.get('image', '')
    
    if image_data and nama:
        try:
            # Pisahkan header base64
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode base64 ke bytes
            img_bytes = base64.b64decode(image_data)
            
            # Buat nama file dengan timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"absensi_{nama}_{timestamp}.jpg"
            
            # Pastikan folder ada
            os.makedirs('absensi_log', exist_ok=True)
            
            # Simpan gambar
            with open(os.path.join('absensi_log', filename), 'wb') as f:
                f.write(img_bytes)
            
            print(f"[SUCCESS] Absensi {nama} berhasil disimpan")
            hasil = f"✅ Absensi berhasil untuk: {nama}"
            
        except Exception as e:
            print(f"[ERROR] Gagal menyimpan absensi: {e}")
            hasil = f"❌ Error: {str(e)}"
    else:
        hasil = "❌ Data tidak lengkap"
    
    return render_template('hasil.html', hasil=hasil)

# 5. Route untuk menampilkan halaman hasil (GET)
@app.route('/hasil', methods=['GET'])
def halaman_hasil():
    return render_template('hasil.html', hasil="Silahkan lakukan absensi terlebih dahulu")

# ========== RUN APLIKASI ==========
if __name__ == '__main__':
    # Buat folder jika belum ada
    os.makedirs('dataset', exist_ok=True)
    os.makedirs('absensi_log', exist_ok=True)
    
    print("=" * 50)
    print("🚀 APLIKASI ABSENSI KAMERA")
    print("=" * 50)
    print("Akses melalui:")
    print("1. Pendaftaran: http://127.0.0.1:5000/")
    print("2. Absensi:     http://127.0.0.1:5000/absensi")
    print("3. Hasil:       http://127.0.0.1:5000/hasil")
    print("=" * 50)
    
    # Jalankan server
    app.run(debug=True, port=5000)