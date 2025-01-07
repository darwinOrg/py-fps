export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_FALLBACK_LIBRARY_PATH
uvicorn app:app --reload --host=0.0.0.0 --port=9999