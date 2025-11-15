# Quick Start Guide

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JsBrainTwister/vae.git
   cd vae
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your image directory:**
   
   Edit `app.py` and set your local image path:
   ```python
   LOCAL_DATA_PATH = r'C:\Users\32350\Desktop\data'
   ```

## Running the Application

### Production Mode (Recommended)
```bash
python app.py
```
The application will start on `http://localhost:5000` with debug mode **disabled** for security.

### Development Mode
```bash
export FLASK_DEBUG=True  # On Windows: set FLASK_DEBUG=True
python app.py
```

### Testing Mode (with sample images)
```bash
python app_test.py
```
This uses `/tmp/test_images` for testing and has debug enabled by default.

## Usage

1. Open your browser and navigate to `http://localhost:5000`
2. Select an image from the sidebar
3. Adjust the brightness using the slider (0.0 to 2.0)
4. Click "🔄 Sync to Server" to send parameters to the server
5. View sync status in the top bar

## Running Tests

```bash
python test_app.py
```

## Troubleshooting

### Images not loading
- Verify `LOCAL_DATA_PATH` exists and contains images
- Check file permissions
- Supported formats: JPG, PNG, GIF, BMP, WebP

### Port already in use
Edit the port in `app.py`:
```python
app.run(debug=DEBUG, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Permission denied
Make sure the application has read access to the image directory.

## What Gets Synced?

When you click "Sync to Server", only a small JSON payload is sent:
```json
{
  "filename": "image.jpg",
  "brightness": 1.8
}
```

**Size: ~50 bytes** vs megabytes for image files!

The server stores these parameters in `modifications.json` and can apply them to its local copy of the dataset.

## Security Notes

- **Production**: Debug mode is OFF by default for security
- **Testing**: Debug mode is ON by default in `app_test.py`
- For remote deployments, use HTTPS and add authentication
