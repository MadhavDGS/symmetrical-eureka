"""
Enhanced Spotify API Routes for Manas Wellness
Add these routes to your main app.py file
"""

from integrations.spotify_therapy import spotify_therapy
from flask import request, jsonify

# Add these routes to your app.py file

@app.route('/api/music/crisis-intervention', methods=['POST'])
def get_crisis_music():
    """Get crisis intervention music playlist"""
    try:
        data = request.get_json()
        crisis_level = data.get('crisis_level', 'high')
        duration = data.get('duration_minutes', 15)
        
        playlist = spotify_therapy.get_crisis_intervention_playlist(
            crisis_level=crisis_level,
            duration_minutes=duration
        )
        
        return jsonify({
            'status': 'success',
            'playlist': playlist
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/music/sleep-therapy', methods=['POST'])
def get_sleep_therapy_music():
    """Get sleep therapy sequence"""
    try:
        data = request.get_json()
        sleep_goal = data.get('sleep_goal', 'deep_sleep')
        sequence_length = data.get('sequence_length', 90)
        
        sequence = spotify_therapy.get_sleep_therapy_sequence(
            sleep_goal=sleep_goal,
            sequence_length=sequence_length
        )
        
        return jsonify({
            'status': 'success',
            'sequence': sequence
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/music/study-focus', methods=['POST'])
def get_study_music():
    """Get study and focus music playlist"""
    try:
        data = request.get_json()
        study_type = data.get('study_type', 'concentration')
        duration = data.get('duration_minutes', 60)
        
        playlist = spotify_therapy.get_focus_study_playlist(
            study_type=study_type,
            duration_minutes=duration
        )
        
        return jsonify({
            'status': 'success',
            'playlist': playlist
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/music/cultural-healing', methods=['POST'])
def get_cultural_healing_music():
    """Get cultural healing music playlist"""
    try:
        data = request.get_json()
        culture = data.get('culture', 'western')
        healing_type = data.get('healing_type', 'traditional')
        language = data.get('language', 'english')
        
        playlist = spotify_therapy.get_cultural_healing_music(
            culture=culture,
            healing_type=healing_type,
            language=language
        )
        
        return jsonify({
            'status': 'success',
            'playlist': playlist
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/music/analyze-track', methods=['POST'])
def analyze_track():
    """Analyze therapeutic value of a specific track"""
    try:
        data = request.get_json()
        track_id = data.get('track_id')
        
        if not track_id:
            return jsonify({
                'status': 'error',
                'message': 'track_id is required'
            }), 400
        
        analysis = spotify_therapy.analyze_track_therapeutic_value(track_id)
        
        return jsonify({
            'status': 'success',
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/music/mood-enhanced', methods=['POST'])
def get_enhanced_mood_music():
    """Enhanced mood-based music with additional parameters"""
    try:
        data = request.get_json()
        mood = data.get('mood', 'calm')
        intensity = data.get('intensity', 0.5)
        duration = data.get('duration_minutes', 30)
        therapy_goal = data.get('therapy_goal', 'general_wellness')
        
        # Get base mood playlist
        playlist = spotify_therapy.get_mood_based_playlist(mood, intensity)
        
        # Add enhanced metadata
        playlist['therapy_goal'] = therapy_goal
        playlist['duration_requested'] = duration
        playlist['intensity_level'] = intensity
        
        return jsonify({
            'status': 'success',
            'playlist': playlist
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Frontend Integration Examples for HTML Templates

CRISIS_MUSIC_JS = '''
// Crisis Intervention Music
async function getCrisisMusic(crisisLevel = 'high') {
    try {
        const response = await fetch('/api/music/crisis-intervention', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                crisis_level: crisisLevel,
                duration_minutes: 15
            })
        });
        
        const data = await response.json();
        if (data.status === 'success') {
            displayCrisisPlaylist(data.playlist);
        }
    } catch (error) {
        console.error('Crisis music error:', error);
    }
}

function displayCrisisPlaylist(playlist) {
    const container = document.getElementById('crisis-playlist');
    container.innerHTML = `
        <h3>Crisis Support Music</h3>
        <p><strong>Instructions:</strong> ${playlist.usage_instructions}</p>
        <div class="tracks">
            ${playlist.tracks.map(track => `
                <div class="track-item crisis-track">
                    <div class="track-name">${track.name}</div>
                    <div class="track-artist">${track.artist}</div>
                    <div class="crisis-score">Crisis Score: ${track.crisis_score?.toFixed(2) || 'N/A'}</div>
                    <div class="therapy-benefit">${track.therapy_benefit}</div>
                </div>
            `).join('')}
        </div>
    `;
}
'''

SLEEP_THERAPY_JS = '''
// Sleep Therapy Music
async function getSleepTherapy(sleepGoal = 'deep_sleep') {
    try {
        const response = await fetch('/api/music/sleep-therapy', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                sleep_goal: sleepGoal,
                sequence_length: 90
            })
        });
        
        const data = await response.json();
        if (data.status === 'success') {
            displaySleepSequence(data.sequence);
        }
    } catch (error) {
        console.error('Sleep therapy error:', error);
    }
}

function displaySleepSequence(sequence) {
    const container = document.getElementById('sleep-sequence');
    const phases = ['relaxation', 'transition', 'deep_sleep'];
    
    container.innerHTML = `
        <h3>Sleep Therapy Sequence</h3>
        <p><strong>Instructions:</strong> ${sequence.usage_instructions}</p>
        ${phases.map(phase => {
            const phaseTracks = sequence.tracks.filter(t => t.phase === phase);
            return `
                <div class="sleep-phase">
                    <h4>${phase.toUpperCase()} Phase (${phaseTracks.length} tracks)</h4>
                    ${phaseTracks.map(track => `
                        <div class="track-item sleep-track">
                            <div class="track-name">${track.name}</div>
                            <div class="track-artist">${track.artist}</div>
                            <div class="sleep-score">Sleep Score: ${track.sleep_score?.toFixed(2) || 'N/A'}</div>
                        </div>
                    `).join('')}
                </div>
            `;
        }).join('')}
    `;
}
'''

STUDY_MUSIC_JS = '''
// Study and Focus Music
async function getStudyMusic(studyType = 'concentration') {
    try {
        const response = await fetch('/api/music/study-focus', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                study_type: studyType,
                duration_minutes: 60
            })
        });
        
        const data = await response.json();
        if (data.status === 'success') {
            displayStudyPlaylist(data.playlist);
        }
    } catch (error) {
        console.error('Study music error:', error);
    }
}

function displayStudyPlaylist(playlist) {
    const container = document.getElementById('study-playlist');
    container.innerHTML = `
        <h3>Study Music - ${playlist.study_type.toUpperCase()}</h3>
        <p><strong>Instructions:</strong> ${playlist.usage_instructions}</p>
        <div class="tracks">
            ${playlist.tracks.map(track => `
                <div class="track-item study-track">
                    <div class="track-name">${track.name}</div>
                    <div class="track-artist">${track.artist}</div>
                    <div class="study-score">Study Score: ${track.study_score?.toFixed(2) || 'N/A'}</div>
                    <div class="therapy-benefit">${track.therapy_benefit}</div>
                </div>
            `).join('')}
        </div>
    `;
}
'''

CULTURAL_HEALING_JS = '''
// Cultural Healing Music
async function getCulturalHealing(culture = 'western') {
    try {
        const response = await fetch('/api/music/cultural-healing', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                culture: culture,
                healing_type: 'traditional',
                language: 'english'
            })
        });
        
        const data = await response.json();
        if (data.status === 'success') {
            displayCulturalPlaylist(data.playlist);
        }
    } catch (error) {
        console.error('Cultural healing error:', error);
    }
}

function displayCulturalPlaylist(playlist) {
    const container = document.getElementById('cultural-playlist');
    container.innerHTML = `
        <h3>${playlist.culture.toUpperCase()} Cultural Healing</h3>
        <p><strong>Focus:</strong> ${playlist.therapy_focus}</p>
        <div class="tracks">
            ${playlist.tracks.map(track => `
                <div class="track-item cultural-track">
                    <div class="track-name">${track.name}</div>
                    <div class="track-artist">${track.artist}</div>
                    <div class="cultural-score">Cultural Score: ${track.cultural_score?.toFixed(2) || 'N/A'}</div>
                    <div class="therapy-benefit">${track.therapy_benefit}</div>
                </div>
            `).join('')}
        </div>
    `;
}
'''