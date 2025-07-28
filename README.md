# Wish Discord Bot Dashboard

A modern web interface to view and manage Discord bot Wish data, with a Discord-inspired design.

## 🚀 Features

- **Complete Dashboard**: Overview of all database tables
- **Table Visualization**: Advanced filters for date, time and user
- **Chat Interface**: Discord-like message view with channel sidebar
- **Message Management**: Toggle for `to_maintain` field with real-time updates
- **Dark Theme**: Modern design inspired by Discord
- **Responsive**: Optimized for desktop and mobile
- **Advanced Filters**: For date, time, user and message status

## 📋 Prerequisites

- Python 3.8+
- SQLite3
- Access to `wish_data.db` database

## 🛠️ Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd wish_discord_bot_page
```

2. **Configure Git** (security):
```bash
# .gitignore is already configured to exclude sensitive files
# Verify that config.env is not tracked by Git
git status
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure the database**:
   - Create the `config.env` file with the correct database path:
```env
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DATABASE_PATH=/path/to/your/wish_data.db
DEBUG=False
```

**Complete example of `config.env` file**:
```env
# Flask Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# SQLite Database Path
DATABASE_PATH=/path/to/your/wish_data.db

# Debug Mode (True for development, False for production)
DEBUG=False

# Additional configurations (optional)
# SECRET_KEY=your-secret-key-here
# LOG_LEVEL=INFO
```

## 🚀 Startup

1. **Start the application**:
```bash
python run.py
```

2. **Access the interface**:
   - Open your browser and go to `http://localhost:5000`
   - For remote access: `http://<server-ip>:5000`

## 📊 Database Structure

The application supports the following tables:

- **messages**: Discord messages with channels and users
- **events**: Bot events
- **commands**: Executed commands
- **errors**: Bot errors
- **verification**: Verification processes
- **welcome**: Welcome messages

## 🎯 Main Features

### Dashboard (`/`)
- Overview of all tables
- Record counters for each table
- Quick navigation

### Table Visualization (`/table/<table_name>`)
- Date and time filters
- Pagination (50 records per page)
- User filter (if available)
- `to_maintain` status filter (for messages table)

### Messages Interface (`/messages`)
- **Channel Sidebar**: Channel list with emojis and counters
- **Chat Area**: Discord-style message view
- **Advanced Filters**: Date, time, user, status
- **`to_maintain` Toggle**: Real-time updates
- **Auto-refresh**: Automatic update every 30 seconds

## 🎨 Design

- **Dark Theme**: Discord-inspired colors
- **Modern Font**: Inter font family
- **Icons**: Font Awesome 6
- **Responsive**: Optimized for all devices
- **Animations**: Smooth transitions and visual feedback

## 🔧 Advanced Configuration

### Environment Variables (`config.env`)

```env
# Flask Configuration
FLASK_HOST=0.0.0.0          # Listening host (0.0.0.0 for external access)
FLASK_PORT=5000              # Server port
DATABASE_PATH=/path/to/db     # SQLite database path
DEBUG=False                   # Debug mode (True for development, False for production)

# Additional configurations (optional)
# SECRET_KEY=your-secret-key-here
# LOG_LEVEL=INFO
```

**Configuration notes**:
- `FLASK_HOST=0.0.0.0`: Allows external access (required for remote access)
- `FLASK_PORT=5000`: Standard Flask port (change if occupied)
- `DATABASE_PATH`: Absolute path to `.db` file
- `DEBUG=False`: Disables debug in production

### Customization

- **Colors**: Modify `app/static/css/style.css`
- **Layout**: Customize templates in `app/templates/`
- **Functionality**: Extend routes in `app/routes/`

## 🔒 Security

- Local access only (via VPN)
- No authentication required
- Server-side input validation
- Data sanitization
- `.env` files excluded from Git (see `.gitignore`)
- Sensitive configurations protected

## 📱 Compatibility

- **Browsers**: Chrome, Firefox, Safari, Edge
- **Devices**: Desktop, tablet, mobile
- **Systems**: Windows, macOS, Linux, Raspberry Pi

## 🐛 Troubleshooting

### Database Error
```
Error: database file not found
```
**Solution**: Check the path in `config.env`

### Port Error
```
Error: Address already in use
```
**Solution**: Change `FLASK_PORT` in `config.env`

### Permission Error
```
Error: Permission denied
```
**Solution**: Check database file permissions

## 🔄 Updates

1. **Database backup** before updates
2. **Test in development environment**
3. **Restart application** after changes

## 📞 Support

For issues or requests:
1. Check application logs
2. Verify configuration
3. Test database connection

## 📄 License

Private project for internal use.

---

**Developed for Discord bot Wish** 🤖 