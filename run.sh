#!/bin/bash
echo "Starting PDF conversion service..."
uvicorn app:app --reload --host 0.0.0.0 --port 8000