from app import app
app.run(
  host=app.config.get("HOST", "127.0.0.1"),
  debug=True)
