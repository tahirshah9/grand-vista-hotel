#!/bin/bash
pkill -9 -f streamlit || true
pkill -9 -f python3 || true
exec python3 -m streamlit run main.py --server.port 3000 --server.address 0.0.0.0 --server.headless true --server.enableCORS false --server.enableXsrfProtection false --browser.gatherUsageStats false > streamlit.log 2>&1
