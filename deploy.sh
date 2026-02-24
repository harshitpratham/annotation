#!/bin/bash
# Deploy script - run this ON THE VM to pull latest code and restart the app
# Usage: ./deploy.sh (or: bash deploy.sh)
#
# To deploy from local machine via SSH:
#   ssh ubuntu@<VM_IP> 'cd /home/ubuntu/data-annotation && git pull origin main && sudo systemctl restart data-annotation || (pkill -f streamlit; sleep 2; nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &)'
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📥 Pulling latest from git..."
git pull origin main

echo "🔄 Restarting Streamlit app..."
if systemctl is-active --quiet data-annotation 2>/dev/null; then
    sudo systemctl restart data-annotation
    echo "Restarted via systemd"
else
    pkill -f "streamlit run" 2>/dev/null || true
    sleep 2
    (nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &)
    sleep 2
    echo "Restarted via direct process"
fi

echo "✅ Deploy complete! App should be running."
