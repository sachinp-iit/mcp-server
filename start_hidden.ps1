Start-Process `
  -FilePath "C:\Users\sachi\AppData\Local\Programs\Python\Python311\python.exe" `
  -ArgumentList @("C:\Users\sachi\mcp_server\server.py") `
  -WindowStyle Hidden

Start-Process `
  -FilePath "C:\Users\sachi\AppData\Local\Programs\Python\Python311\python.exe" `
  -ArgumentList @("-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000") `
  -WorkingDirectory "C:\Users\sachi\mcp_server" `
  -WindowStyle Hidden

Start-Process `
  -FilePath "C:\Users\sachi\mcp_server\ngrok.exe" `
  -ArgumentList @("http", "5000") `
  -WorkingDirectory "C:\Users\sachi\mcp_server" `
  -WindowStyle Hidden
