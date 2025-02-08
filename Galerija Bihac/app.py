from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Folder paths
ARTISTS_FOLDER = "artists_data"
ARTIST_BIOGRAPHIES_FOLDER = "artist_biographies"
DESCRIPTIONS_FOLDER = "descriptions_data"
ID_CONNECTION_FOLDER = "id_connection"
ARTWORKS_FOLDER = "artworks"
UPLOAD_FOLDER = 'static/uploads'  # Folder for uploaded files
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}  # Allowed image types

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key'  # Change this to a more secure key

# Helper function to read records from a text file
def read_records(folder_path):
    file_path = os.path.join(folder_path, "database.txt")
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines[1:]  # Skip the header line

# Helper function to get artwork metadata
def list_artworks():
    artwork_files = []
    for filename in os.listdir(ARTWORKS_FOLDER):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            metadata_file = filename.rsplit('.', 1)[0] + ".txt"
            metadata_path = os.path.join(ARTWORKS_FOLDER, metadata_file)
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as file:
                    metadata = file.read().strip()
                artwork_files.append((filename, metadata))
    return artwork_files

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Fetch room images correctly
    room_images = [
        "static/images/room1.jpg", "static/images/room2.jpg",
        "static/images/room3.jpg", "static/images/room4.jpg",
        "static/images/room5.jpg", "static/images/room6.jpg",
        "static/images/room7.jpg", "static/images/room8.jpg",
        "static/images/room9.jpg", "static/images/room10.jpg",
        "static/images/room11.jpg", "static/images/room12.jpg"
    ]

    # Fetch artwork details
    artworks_data = []
    
    # Read all artworks
    artwork_records = read_records(ARTWORKS_FOLDER)
    artwork_dict = {}  # Store artworks as {id: file_path}
    for artwork in artwork_records:
        parts = artwork.strip().split(',', 1)
        if len(parts) == 2:
            artwork_id, file_path = parts
            artwork_dict[artwork_id] = file_path  # Store in dictionary

    # Read artist names
    artist_records = read_records(ARTISTS_FOLDER)
    artist_dict = {}  # Store artists as {id: name}
    for artist in artist_records:
        parts = artist.strip().split(',', 1)
        if len(parts) == 2:
            artist_id, artist_name = parts
            artist_dict[artist_id] = artist_name  # Store in dictionary

    # Read descriptions
    description_records = read_records(DESCRIPTIONS_FOLDER)
    description_dict = {}  # Store descriptions as {id: text}
    for desc in description_records:
        parts = desc.strip().split(',', 1)
        if len(parts) == 2:
            desc_id, desc_text = parts
            description_dict[desc_id] = desc_text  # Store in dictionary

    # Read connections (artist - description - artwork)
    connection_records = read_records(ID_CONNECTION_FOLDER)
    for conn in connection_records:
        parts = conn.strip().split(',')
        if len(parts) == 4:
            _, artist_id, description_id, artwork_id = parts
            if artwork_id in artwork_dict:
                artworks_data.append({
                    "file_path": artwork_dict[artwork_id],
                    "artist_name": artist_dict.get(artist_id, "Unknown Artist"),
                    "description": description_dict.get(description_id, "No Description")
                })

    return render_template('index.html', room_images=room_images, artworks=artworks_data)

def get_artist_name(artist_id):
    with open("artists_data/database.txt", "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 2:  # Ensure the line has ID and name
                id_, name = parts
                if id_ == artist_id:
                    return name
    return "Unknown Artist"  # Fallback if ID not found

def get_description(artwork_id):
    with open("descriptions_data/database.txt", "r") as f:
        for line in f:
            parts = line.strip().split(",", 1)
            if len(parts) == 2:  # Ensure line has ID and description
                id_, description = parts
                if id_ == artwork_id:
                    return description
    return "No description available"  # Fallback if ID not found

def get_artwork_path(artwork_id):
    try:
        artwork_id = str(int(artwork_id))  # Ensure ID is a valid integer as a string
    except ValueError:
        return None  # Return nothing if the ID isn't an integer

    with open("artworks/database.txt", "r") as f:
        for line in f:
            parts = line.strip().split(",", 1)
            if len(parts) == 2:  # Ensure line has ID and file path
                id_, file_path = parts
                if id_ == artwork_id:
                    return file_path
    return None  # Return nothing if the ID is not found



@app.route('/artists')
def artists():
    # Read artist records
    artist_records = read_records(ARTISTS_FOLDER)

    # Read biography records
    biography_records = read_records(ARTIST_BIOGRAPHIES_FOLDER)

    combined_records = []
    
    for artist in artist_records:
        artist = artist.strip()  # Remove leading/trailing spaces
        if not artist or ',' not in artist:  # Skip empty or malformed lines
            continue
        
        try:
            artist_id, artist_name = artist.split(',', 1)  # Ensure we only split into two parts
        except ValueError:
            continue  # Skip invalid lines
        
        # Find matching biography (default: "Not available" for DOB, "No description" for biography)
        biography = next(
            (bio.strip().split(',', 2)[1:] for bio in biography_records if bio.startswith(artist_id + ',')),
            ("Not available", "No description")
        )

        combined_records.append((artist_id, artist_name, *biography))

    return render_template('artists.html', records=combined_records)



@app.route('/descriptions')
def descriptions():
    records = read_records(DESCRIPTIONS_FOLDER)
    return render_template('descriptions.html', records=records)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/art")
def art():
    artwork_list = []
    with open("artworks/database.txt", "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 2:  # Ensure it has ID and file path
                _, file_path = parts
                if file_path == "data":
                    continue
                artwork_list.append({"file_path": file_path})
    
    return render_template("art.html", artworks=artwork_list)

@app.route("/artworks")
def artworks():
    artwork_list = []
    with open("id_connection/database.txt", "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 4:
                _, artist_id, description_id, artwork_id = parts
                artist_name = get_artist_name(artist_id)
                description = get_description(description_id)
                file_path = get_artwork_path(artwork_id)
                artwork_list.append({
                    "file_path": file_path,
                    "artist_name": artist_name,
                    "description": description
                })
    
    return render_template("artworks.html", artworks=artwork_list)


@app.route('/add_artist', methods=['GET', 'POST'])
def add_artist():
    if request.method == 'POST':
        artist_name = request.form['artist_name']

        file_path = os.path.join(ARTISTS_FOLDER, "database.txt")

        # Ensure the file exists
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write("id,data\n")  # Header

        # Determine the next available ID
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Filter out empty lines and header
        valid_lines = [line.strip() for line in lines if line.strip() and not line.startswith("id,")]

        if not valid_lines:
            next_id = 1
        else:
            next_id = int(valid_lines[-1].split(',')[0]) + 1

        # Append the new artist with a newline before it
        with open(file_path, 'a') as file:
            file.write(f"\n{next_id},{artist_name}")

        flash('Artist added successfully!', 'success')
        return redirect(url_for('artists'))

    return render_template('add_artist.html')


@app.route('/update_artist/<id>', methods=['GET', 'POST'])
def update_artist(id):
    if request.method == 'POST':
        new_name = request.form['new_name']
        records = read_records(ARTISTS_FOLDER)
        with open(os.path.join(ARTISTS_FOLDER, "database.txt"), 'w') as file:
            file.write("id,data\n")  # Re-write header
            for record in records:
                record_data = record.strip().split(',')
                if record_data[0] == id:
                    record_data[1] = new_name
                file.write(','.join(record_data) + '\n')
        return redirect(url_for('artists'))
    return render_template('update_artist.html', id=id)

@app.route('/delete_artist/<int:artist_id>')
def delete_artist(artist_id):
    artist_file = os.path.join(ARTISTS_FOLDER, "database.txt")
    biography_file = os.path.join(ARTIST_BIOGRAPHIES_FOLDER, "database.txt")

    # Read all artists
    with open(artist_file, 'r') as file:
        lines = file.readlines()

    # Preserve the header and filter out the deleted artist
    header = lines[0]  # Keep "id,data"
    artists = [line.strip().split(',', 1) for line in lines[1:] if line.strip()]

    # Remove the artist with the matching ID
    updated_artists = [artist for artist in artists if int(artist[0]) != artist_id]

    # Reassign IDs sequentially
    with open(artist_file, 'w') as file:
        file.write(header)  # Write back the header
        for index, artist in enumerate(updated_artists, start=1):
            file.write(f"{index},{artist[1]}\n")  # Assign new ID sequentially

    # Update biographies (remove the deleted artist and reassign IDs)
    with open(biography_file, 'r') as file:
        bio_lines = file.readlines()

    bio_header = bio_lines[0]  # Keep "id,dob,desc"
    biographies = [line.strip().split(',', 2) for line in bio_lines[1:] if line.strip()]

    # Remove the biography entry of the deleted artist
    updated_biographies = [bio for bio in biographies if int(bio[0]) != artist_id]

    # Reassign IDs for biographies
    with open(biography_file, 'w') as file:
        file.write(bio_header)  # Write back the header
        for index, bio in enumerate(updated_biographies, start=1):
            file.write(f"{index},{bio[1]},{bio[2]}\n")  # Assign new ID sequentially

    flash('Artist and associated biography deleted successfully!', 'success')
    return redirect(url_for('artists'))




@app.route('/art_connection', methods=['GET', 'POST'])
def art_connection():
    if request.method == 'POST':
        artist_id = request.form['artist_id']
        artwork_id = request.form['artwork_id']

        # Ensure description_id matches artwork_id
        description_id = artwork_id

        # Path to the connection database
        connection_file = os.path.join(ID_CONNECTION_FOLDER, "database.txt")

        # Ensure the connection file exists
        if not os.path.exists(connection_file):
            with open(connection_file, 'w') as file:
                file.write("id,artist_id,description_id,artwork_id\n")

        # Get the next auto-incremented connection ID
        with open(connection_file, 'r') as file:
            lines = file.readlines()
            next_connection_id = 1 if len(lines) == 1 else int(lines[-1].split(',')[0]) + 1

        # Save the connection
        with open(connection_file, 'a') as file:
            file.write(f"{next_connection_id},{artist_id},{description_id},{artwork_id}\n")

        flash('Artwork connection created successfully!', 'success')
        return redirect(url_for('art_connection'))

    # Get available artists (ID, Full Name)
    artists = []
    artist_records = read_records(ARTISTS_FOLDER)
    for artist in artist_records:
        parts = artist.strip().split(',', 1)
        if len(parts) == 2:
            artist_id, artist_name = parts
            artists.append((artist_id, artist_name))

    # Get available artworks (ID, File Location)
    artworks = []
    artwork_records = read_records(ARTWORKS_FOLDER)
    for artwork in artwork_records:
        parts = artwork.strip().split(',', 1)
        if len(parts) == 2:
            artwork_id, file_path = parts
            artworks.append((artwork_id, file_path))

    return render_template('art_connection.html', artists=artists, artworks=artworks)


@app.route('/gallery', methods=['GET'])
def gallery():
    artwork_records = read_records(ARTWORKS_FOLDER)
    artworks = []

    for artwork in artwork_records:
        parts = artwork.strip().split(',', 1)
        if len(parts) == 2:
            artwork_id, file_path = parts
            artworks.append((artwork_id, file_path))  # Correctly store (ID, file_path)

    return render_template('gallery.html', artworks=artworks)  # Pass artworks as a list



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        description = request.form['description']
        image = request.files['image']

        if image and allowed_file(image.filename):
            # Secure filename and save image
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

            # Generate new auto-incremented IDs
            descriptions_file = os.path.join(DESCRIPTIONS_FOLDER, "database.txt")
            artworks_file = os.path.join(ARTWORKS_FOLDER, "database.txt")

            # Ensure description database exists
            if not os.path.exists(descriptions_file):
                with open(descriptions_file, 'w') as file:
                    file.write("id,description\n")

            # Ensure artworks database exists
            if not os.path.exists(artworks_file):
                with open(artworks_file, 'w') as file:
                    file.write("id,file_path\n")

            # Get the next description ID
        
            with open(descriptions_file, 'r') as file:
                lines = file.readlines()
    
                # Remove any empty lines and header lines
                lines = [line.strip() for line in lines if line.strip() and not line.startswith("id,")]
    
                # If there are no valid lines, the next ID is 1
                if not lines:
                    next_description_id = 1
                else:
                # Otherwise, get the ID from the last valid line
                    next_description_id = int(lines[-1].split(',')[0]) + 1


            # Save description
            with open(descriptions_file, 'a') as file:
                file.write(f"{next_description_id},{description}\n")

            # Get the next artwork ID
            with open(artworks_file, 'r') as file:
                lines = file.readlines()
                next_artwork_id = 1 if len(lines) == 1 else int(lines[-1].split(',')[0]) + 1

            # Save artwork metadata
            with open(artworks_file, 'a') as file:
                file.write(f"{next_artwork_id},static/uploads/{filename}\n")

            flash('Artwork and description uploaded successfully!', 'success')
            return redirect(url_for('upload'))

        flash('Invalid file type. Please upload an image file.', 'danger')

    return render_template('upload.html')





# Helper function to read artist biographies
def read_biographies():
    file_path = os.path.join(ARTIST_BIOGRAPHIES_FOLDER, "database.txt")
    
    # Ensure file exists
    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    return lines[1:]  # Skip the header line


@app.route('/add_biography', methods=['GET', 'POST'])
def add_biography():
    if request.method == 'POST':
        dob = request.form['dob']
        description = request.form['description']

        file_path = os.path.join(ARTIST_BIOGRAPHIES_FOLDER, "database.txt")

        # Ensure the file exists
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write("id,dob,desc\n")

        # Determine the next available ID
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Filter out empty lines and header
        valid_lines = [line.strip() for line in lines if line.strip() and not line.startswith("id,")]

        if not valid_lines:
            next_id = 1
        else:
            next_id = int(valid_lines[-1].split(',')[0]) + 1

        # Append the new biography with a newline before it
        with open(file_path, 'a') as file:
            file.write(f"\n{next_id},{dob},{description}")

        flash('Biography added successfully!', 'success')
        return redirect(url_for('biographies'))

    return render_template('add_biography.html')



@app.route('/update_biography/<int:artist_id>', methods=['GET', 'POST'])
def update_biography(artist_id):
    file_path = os.path.join(ARTIST_BIOGRAPHIES_FOLDER, "database.txt")

    if request.method == 'POST':
        dob = request.form.get('dob', '')
        description = request.form.get('description', '')

        # Read existing biographies
        with open(file_path, 'r') as file: 
            lines = file.readlines()

        # Update the biography
        with open(file_path, 'w') as file:
            file.write(lines[0])  # Keep header
            for line in lines[1:]:
                record = line.strip().split(',')
                if record[0] == str(artist_id):
                    file.write(f"{artist_id},{dob},{description}\n")
                else:
                    file.write(line)

        flash('Biography updated successfully!', 'success')
        return redirect(url_for('biographies'))

    # Get the current biography data
    biography = None
    with open(file_path, 'r') as file:
        for line in file.readlines()[1:]:
            record = line.strip().split(',')
            if record[0] == str(artist_id):
                biography = record
                break

    return render_template('update_biography.html', artist_id=artist_id, biography=biography)


@app.route('/biographies')
def biographies():
    records = read_biographies()
    return render_template('biographies.html', records=records)


@app.route('/delete_biography/<artist_id>')
def delete_biography(artist_id):
    records = read_biographies()
    file_path = os.path.join(ARTIST_BIOGRAPHIES_FOLDER, "database.txt")

    with open(file_path, 'w') as file:
        file.write("id,dob,desc\n")  # Keep header
        for record in records:
            record_data = record.strip().split(',')
            if record_data[0] != artist_id:
                file.write(','.join(record_data) + '\n')

    flash('Biography deleted successfully!', 'success')
    return redirect(url_for('biographies'))


if __name__ == '__main__':
    app.run(debug=True)
