#!/usr/bin/env python3
"""
YouTube Transcript API Service
Provides REST API for fetching YouTube video transcripts
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS to allow your domains
CORS(app, origins=[
    "http://localhost:5173",
    "https://shake-tools.pages.dev",
    "https://optmzr.tools",
    "https://www.optmzr.tools",
    "https://shake-tools-production.up.railway.app"
])

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "YouTube Transcript API",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Health check",
            "/transcript/<video_id>": "Get transcript for video"
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "transcript-api"})

@app.route('/transcript/<video_id>', methods=['GET'])
def get_transcript(video_id):
    logger.info(f"Fetching transcript for video: {video_id}")
    
    try:
        # Get list of available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to get transcript in this priority order
        transcript = None
        is_generated = False
        
        # 1. Try manual English transcript
        try:
            transcript = transcript_list.find_manually_created_transcript(['en', 'en-US', 'en-GB'])
            is_generated = False
            logger.info(f"Found manual transcript for {video_id}")
        except:
            # 2. Try auto-generated English transcript
            try:
                transcript = transcript_list.find_generated_transcript(['en', 'en-US', 'en-GB'])
                is_generated = True
                logger.info(f"Found auto-generated transcript for {video_id}")
            except:
                # 3. Get any available transcript
                for t in transcript_list:
                    transcript = t
                    is_generated = t.is_generated
                    logger.info(f"Using transcript in {t.language_code} for {video_id}")
                    break
        
        if transcript:
            # Fetch the actual transcript data
            data = transcript.fetch()
            
            # Combine all text segments
            full_text = ' '.join([entry['text'] for entry in data])
            
            # Prepare response
            response = {
                "success": True,
                "video_id": video_id,
                "text": full_text,
                "language": transcript.language_code,
                "is_generated": is_generated,
                "length": len(full_text),
                "segment_count": len(data)
            }
            
            # Include timestamps if requested
            if request.args.get('include_timestamps') == 'true':
                response['timestamps'] = [{
                    'start': entry['start'],
                    'duration': entry['duration'],
                    'text': entry['text']
                } for entry in data[:100]]  # Limit to first 100 for performance
            
            return jsonify(response)
        else:
            logger.warning(f"No transcript found for {video_id}")
            return jsonify({
                "success": False,
                "error": "No transcript available for this video",
                "video_id": video_id
            }), 404
            
    except Exception as e:
        logger.error(f"Error fetching transcript for {video_id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "video_id": video_id
        }), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)