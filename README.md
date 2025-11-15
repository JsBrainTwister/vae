# Local Image Visualization with Parameter Sync

A Flask application that enables local image visualization and editing with parameter synchronization to a server. Users can adjust image brightness locally without transferring large image files, and only the adjustment parameters are sent to the server for synchronization.

## Features

- 🖼️ **Local Image Loading**: Load images from a local directory (`C:\Users\32350\Desktop\data`)
- ✨ **Local Brightness Adjustment**: Adjust image brightness in real-time using a slider, all processing happens client-side
- 🔄 **Parameter Sync**: Only adjustment parameters (brightness values) are sent to the server
- 📊 **Sync Status**: Real-time display of sync status and modification history
- 💾 **Data Integrity**: Maintains modification history and ensures consistency between local and remote copies
- 🎨 **Modern UI**: Clean, responsive interface with visual feedback

## Architecture

The application follows a client-server architecture:

1. **Client Side (Browser)**:
   - Loads images from local filesystem via Flask server
   - Applies CSS filters for brightness adjustment (no image manipulation)
   - Sends only adjustment parameters to server

2. **Server Side (Flask)**:
   - Serves the web interface
   - Provides API endpoints for image listing and parameter sync
   - Stores modification history in `modifications.json`
   - Can apply modifications to server's local dataset

## Installation

1. Clone the repository:
```bash
git clone https://github.com/JsBrainTwister/vae.git
cd vae
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the local data path:
   - By default, the application looks for images in `C:\Users\32350\Desktop\data`
   - To change this, edit the `LOCAL_DATA_PATH` variable in `app.py`:
   ```python
   LOCAL_DATA_PATH = r'C:\Your\Path\To\Images'
   ```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. **Using the Application**:
   - The left sidebar shows all available images from your local directory
   - Click on an image to view it
   - Use the brightness slider to adjust the image brightness (0.0 to 2.0)
   - Changes are applied instantly using CSS filters (no image data is modified locally)
   - Click "Sync to Server" to send the brightness parameter to the server
   - The server records the modification and can apply it to its local copy
   - View sync status and statistics in the top bar

## API Endpoints

### GET `/api/images`
Lists all available images from the local directory.

**Response:**
```json
{
  "status": "success",
  "images": [
    {
      "filename": "image1.jpg",
      "path": "C:\\Users\\32350\\Desktop\\data\\image1.jpg",
      "size": 123456,
      "modifications": {}
    }
  ],
  "count": 1
}
```

### POST `/api/sync_parameters`
Syncs brightness parameters to the server.

**Request:**
```json
{
  "filename": "image1.jpg",
  "brightness": 1.5
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Parameters synced successfully",
  "filename": "image1.jpg",
  "brightness": 1.5,
  "timestamp": "2025-11-15T17:52:59.123456",
  "server_applied": true
}
```

### GET `/api/sync_status`
Gets current sync status and modification history.

**Response:**
```json
{
  "status": "success",
  "total_images_modified": 3,
  "total_modifications": 5,
  "modifications": {
    "image1.jpg": [
      {
        "brightness": 1.5,
        "timestamp": "2025-11-15T17:52:59.123456",
        "synced": true
      }
    ]
  },
  "server_data_path": "/path/to/server_data",
  "local_data_path": "C:\\Users\\32350\\Desktop\\data"
}
```

## File Structure

```
vae/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── modifications.json      # Modification history (auto-generated)
├── templates/
│   └── index.html         # Web interface
├── static/                # Static assets (if needed)
└── server_data/           # Server's local dataset (auto-created)
```

## How It Works

### No Image Transfer
- Images are loaded from the local filesystem through the Flask server
- Brightness adjustments are applied using CSS filters (`filter: brightness(value)`)
- Only when "Sync to Server" is clicked, the brightness parameter is sent

### Parameter Synchronization
- When syncing, only a small JSON payload is sent:
  ```json
  {"filename": "image.jpg", "brightness": 1.5}
  ```
- This is typically less than 100 bytes vs. megabytes for image files

### Data Integrity
- All modifications are logged with timestamps
- Modification history is persisted in `modifications.json`
- Server maintains a record of all parameter changes
- Sync status is displayed in real-time

## Configuration

### Local Data Path
Edit `LOCAL_DATA_PATH` in `app.py`:
```python
LOCAL_DATA_PATH = r'C:\Users\32350\Desktop\data'
```

### Server Data Path
Edit `SERVER_DATA_PATH` in `app.py`:
```python
SERVER_DATA_PATH = os.path.join(os.path.dirname(__file__), 'server_data')
```

### Port Configuration
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- WebP (.webp)

## Security Considerations

- The application runs locally by default
- For production deployment, disable debug mode
- Consider adding authentication for the sync endpoints
- Validate and sanitize all file paths
- Use HTTPS for remote deployments

## Troubleshooting

### Images Not Loading
- Verify the `LOCAL_DATA_PATH` exists and contains images
- Check file permissions
- Ensure supported image formats

### Sync Not Working
- Check the Flask server is running
- Verify network connectivity
- Check browser console for errors

### Modifications Not Persisting
- Ensure write permissions for `modifications.json`
- Check disk space

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.