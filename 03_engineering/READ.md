# Install fastapi
- pip install fastapi uvicorn

# Start RAG AI Agent Service 
- uvicorn api_server:app --reload (console log: "INFO:     Application startup complete.")

# Ubuntu Server
- Open another terminal
- curl -X POST "http://127.0.0.1:8000/chat?user_prompt=What%20is%20Project-X-99?"

# Linux systemd config - user name example, ubuntu
- Log into your Linux service
- sudo vi /etc/systemd/system/rag_agent.service
- Input below:
  [Unit]
  Description=RAG AI Agent Service
  After=network.target

  [Service]
  User=ubuntu
  WorkingDirectory=/home/ubuntu/ai_engineer_journey/03_engineering
  ExecStart=/home/ubuntu/ai_engineer_journey/venv/bin/uvicorn api_server:app --host 0.0.0.0 --port 8000
  Restart=always

  [Install]
  WantedBy=multi-user.target

- Enable and start the service:
  sudo systemctl daemon-reload
  sudo systemctl enable rag_agent
  sudo systemctl start rag_agent

# Windows Browser
- Open Windows cmd and execute "ssh -L 8000:127.0.0.1:8000 username@linux_server_ip"
- Enter password to login
- cd 03_engineering
- Execute "uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload"
- Open Microsoft Edge, input "http://127.0.0.1:8000/docs"
- Click 'chat' and then 'try it out'

