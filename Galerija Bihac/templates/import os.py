import os

# Folder paths for different categories
ARTISTS_FOLDER = "artists_data"
DESCRIPTIONS_FOLDER = "descriptions_data"
ID_CONNECTION_FOLDER = "id_connection"
ARTWORKS_FOLDER = "artworks"

# Function to initialize a folder and its corresponding database text file
def initialize_folder(folder_path, filename="database.txt"):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, filename)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("id,data\n")  # Header line
        print(f"Database initialized in {folder_path}.")

# Function to add a record to a folder's database (artists, descriptions, etc.)
def add_record(folder_path, id, data):
    file_path = os.path.join(folder_path, "database.txt")
    with open(file_path, 'a') as file:
        file.write(f"{id},{data}\n")
    print(f"Record added in {folder_path}: {id}, {data}")

# Function to read all records from a folder's database
def read_records(folder_path):
    file_path = os.path.join(folder_path, "database.txt")
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines[1:]  # Skip the header line

# Function to update a record in a folder's database
def update_record(folder_path, id, new_data):
    file_path = os.path.join(folder_path, "database.txt")
    records = read_records(folder_path)
    updated = False
    with open(file_path, 'w') as file:
        file.write("id,data\n")  # Re-write header
        for record in records:
            record_data = record.strip().split(',')
            if record_data[0] == id:
                # Update record if the ID matches
                record_data[1] = new_data
                updated = True
            file.write(','.join(record_data) + '\n')
    if updated:
        print(f"Record {id} updated in {folder_path}.")
    else:
        print(f"Record {id} not found in {folder_path}.")

# Function to delete a record from a folder's database
def delete_record(folder_path, id):
    file_path = os.path.join(folder_path, "database.txt")
    records = read_records(folder_path)
    with open(file_path, 'w') as file:
        file.write("id,data\n")  # Re-write header
        deleted = False
        for record in records:
            record_data = record.strip().split(',')
            if record_data[0] != id:
                file.write(','.join(record_data) + '\n')
            else:
                deleted = True
        if deleted:
            print(f"Record {id} deleted in {folder_path}.")
        else:
            print(f"Record {id} not found in {folder_path}.")

# Function to connect IDs from different folders (artists, descriptions, and artworks)
def connect_ids():
    # Assuming the ID connection file connects artists, descriptions, and artworks by IDs
    file_path = os.path.join(ID_CONNECTION_FOLDER, "id_connection.txt")
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("id,artist_id,description_id,artwork_id\n")  # Header line
        print("ID connection file initialized.")

# Function to list artworks and their metadata from the artworks folder
def list_artworks():
    artwork_files = []
    for filename in os.listdir(ARTWORKS_FOLDER):
        if filename.endswith(('.jpg', '.png', '.jpeg')):  # Image file types
            metadata_file = filename.rsplit('.', 1)[0] + ".txt"  # Corresponding metadata text file
            metadata_path = os.path.join(ARTWORKS_FOLDER, metadata_file)
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as file:
                    metadata = file.read().strip()
                artwork_files.append((filename, metadata))
    return artwork_files

# Example usage
if __name__ == "__main__":
    # Initialize all folders
    initialize_folder(ARTISTS_FOLDER)
    initialize_folder(DESCRIPTIONS_FOLDER)
    initialize_folder(ID_CONNECTION_FOLDER)
    initialize_folder(ARTWORKS_FOLDER)

    # Add records to each folder
    add_record(ARTISTS_FOLDER, "1", "Leonardo da Vinci")
    add_record(DESCRIPTIONS_FOLDER, "1", "A famous portrait painting.")
    add_record(ARTISTS_FOLDER, "2", "Vincent van Gogh")
    add_record(DESCRIPTIONS_FOLDER, "2", "A famous post-impressionist painting.")
    
    # Connect the records by ID
    connect_ids()
    add_record(ID_CONNECTION_FOLDER, "1", "1,1,1")  # Artist 1, Description 1, Artwork 1

    # List all records from the folders
    print("\nArtists Data:")
    for record in read_records(ARTISTS_FOLDER):
        print(record.strip())
    
    print("\nDescriptions Data:")
    for record in read_records(DESCRIPTIONS_FOLDER):
        print(record.strip())
    
    print("\nID Connections:")
    for record in read_records(ID_CONNECTION_FOLDER):
        print(record.strip())
    
    # List artworks with metadata from the artworks folder
    print("\nArtworks and Metadata:")
    for artwork, metadata in list_artworks():
        print(f"Artwork: {artwork}, Metadata: {metadata}")
    
    # Update a record in Artists folder
    update_record(ARTISTS_FOLDER, "1", "Leonardo da Vinci Updated")

    # Delete a record in Descriptions folder
    delete_record(DESCRIPTIONS_FOLDER, "2")
    
    # Final list of records after updates and deletions
    print("\nFinal Artists Data:")
    for record in read_records(ARTISTS_FOLDER):
        print(record.strip())

    print("\nFinal Descriptions Data:")
    for record in read_records(DESCRIPTIONS_FOLDER):
        print(record.strip())
