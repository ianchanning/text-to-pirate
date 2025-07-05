#!/bin/bash

curl https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini-tts",
    "input": "Today is a wonderful day to build something people love!",
    "voice": "coral",
    "instructions": "Speak in a cheerful and positive tone."
    "response_format": "wav"
  }' \
  --output speech.wav

# curl https://api.openai.com/v1/audio/speech \
#   -H "Authorization: Bearer $OPENAI_API_KEY" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "model": "gpt-4o-mini-tts",
#     "input": "Today is a wonderful day to build something people love!",
#     "voice": "coral",
#     "instructions": "Speak in a cheerful and positive tone.",
#     "response_format": "wav"
#   }' | ffplay -i -
