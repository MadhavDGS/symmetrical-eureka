// Enhanced Music Therapy Implementation with Real Spotify API Integration
class EnhancedMusicTherapy {
    constructor() {
        this.currentMood = null;
        this.isPlaying = false;
        this.currentTrackIndex = 0;
        this.currentTracks = [];
        this.spotifyTracks = [];
        this.loadingState = false;
        
        // API endpoints for different therapy types - connected to real backend
        this.apiEndpoints = {
            'happy': '/api/music/mood-enhanced?mood=happy',
            'sad': '/api/music/mood-enhanced?mood=sad', 
            'anxious': '/api/music/crisis-intervention',
            'calm': '/api/music/sleep-therapy',
            'focused': '/api/music/study-focus',
            'motivated': '/api/music/mood-enhanced?mood=energetic'
        };
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.setupAudioContext();
        console.log('Enhanced Music Therapy initialized with real Spotify API integration');
    }
    
    bindEvents() {
        // Mood selector buttons
        document.querySelectorAll('.mood-selector').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.selectMood(btn.dataset.mood, btn);
            });
        });
        
        // Player controls
        document.getElementById('playPauseBtn')?.addEventListener('click', () => {
            this.togglePlayback();
        });
        
        document.getElementById('playPauseMainBtn')?.addEventListener('click', () => {
            this.toggleMainPlayer();
        });
        
        document.getElementById('nextTrackBtn')?.addEventListener('click', () => {
            this.nextTrack();
        });
        
        document.getElementById('prevBtn')?.addEventListener('click', () => {
            this.previousTrack();
        });
    }
    
    selectMood(mood, buttonElement) {
        // Update UI selection
        document.querySelectorAll('.mood-selector').forEach(b => {
            b.classList.remove('bg-white', 'text-gray-800');
        });
        buttonElement.classList.add('bg-white', 'text-gray-800');
        
        this.currentMood = mood;
        this.loadSpotifyTracks(mood);
    }
    
    async loadSpotifyTracks(mood) {
        if (this.loadingState) return;
        
        this.setLoadingState(true);
        this.updateCurrentTrackDisplay(`Finding therapeutic ${mood} music...`);
        
        try {
            const endpoint = this.apiEndpoints[mood] || `/api/music/search?q=${mood} therapy music`;
            console.log('Fetching from endpoint:', endpoint);
            
            const response = await fetch(endpoint);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log('API Response:', data);
            
            if (data.success && data.results && data.results.length > 0) {
                this.spotifyTracks = data.results.slice(0, 12); // Limit to 12 tracks
                this.displaySpotifyTracks();
                this.updateCurrentTrackDisplay(`Found ${this.spotifyTracks.length} ${mood} therapy tracks`);
                this.showTherapyBenefits(mood);
                this.showMusicNotification(`Successfully loaded ${this.spotifyTracks.length} therapeutic tracks`);
            } else {
                console.log('No tracks found, using fallback');
                this.loadFallbackTracks(mood);
            }
            
        } catch (error) {
            console.error('Error loading Spotify tracks:', error);
            this.loadFallbackTracks(mood);
            this.showMusicNotification('Using curated playlists - API temporarily unavailable', 'warning');
        }
        
        this.setLoadingState(false);
    }
    
    setLoadingState(loading) {
        this.loadingState = loading;
        const playPauseBtn = document.getElementById('playPauseBtn');
        if (playPauseBtn) {
            playPauseBtn.innerHTML = loading ? 'Loading...' : 'Play Therapy Music';
            playPauseBtn.disabled = loading;
        }
    }
    
    updateCurrentTrackDisplay(text, track = null) {
        const currentTrack = document.getElementById('currentTrack');
        const trackNameEl = document.getElementById('currentTrackName');
        const trackArtistEl = document.getElementById('currentTrackArtist');
        
        if (currentTrack) {
            currentTrack.textContent = text;
        }
        
        if (track && trackNameEl && trackArtistEl) {
            trackNameEl.textContent = track.name || 'Unknown Track';
            trackArtistEl.textContent = this.getArtistNames(track);
        }
    }
    
    displaySpotifyTracks() {
        const tracksListContainer = document.getElementById('tracksList');
        const spotifyContainer = document.getElementById('spotifyTracksContainer');
        
        if (!tracksListContainer || !this.spotifyTracks.length) return;
        
        const tracksHTML = this.spotifyTracks.map((track, index) => this.createTrackCard(track, index)).join('');
        
        tracksListContainer.innerHTML = tracksHTML;
        spotifyContainer.classList.remove('hidden');
        
        console.log('Displayed tracks:', this.spotifyTracks.length);
    }
    
    createTrackCard(track, index) {
        const artistNames = this.getArtistNames(track);
        const duration = this.formatDuration(track.duration_ms);
        const hasPreview = track.preview_url ? true : false;
        const spotifyUrl = track.external_urls?.spotify;
        
        return `
            <div class="track-card p-4 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 rounded-lg border border-purple-200 dark:border-purple-700 hover:shadow-md transition-all cursor-pointer" onclick="enhancedMusicTherapy.playSpotifyTrack(${index})">
                <div class="flex items-start justify-between">
                    <div class="flex-1">
                        <h4 class="font-bold text-purple-800 dark:text-purple-200 text-sm leading-tight">
                            ${track.name || 'Unknown Track'}
                        </h4>
                        <p class="text-purple-600 dark:text-purple-300 text-xs mt-1">
                            by ${artistNames}
                        </p>
                        <div class="flex items-center space-x-2 mt-2">
                            ${hasPreview ? '<span class="text-green-600 text-xs bg-green-100 px-2 py-1 rounded-full">Preview Available</span>' : ''}
                            <span class="text-gray-500 text-xs">${duration}</span>
                        </div>
                    </div>
                    <div class="flex flex-col items-end space-y-2 ml-4">
                        <button class="bg-purple-500 hover:bg-purple-600 text-white px-3 py-1 rounded-full text-xs transition-colors" onclick="event.stopPropagation(); enhancedMusicTherapy.playSpotifyTrack(${index})">
                            Play
                        </button>
                        ${spotifyUrl ? `
                        <button class="text-green-600 hover:text-green-700 text-xs underline" onclick="event.stopPropagation(); window.open('${spotifyUrl}', '_blank');">
                            Spotify
                        </button>` : ''}
                    </div>
                </div>
                
                ${hasPreview ? `
                <div class="mt-3 pt-2 border-t border-purple-200 dark:border-purple-700">
                    <button class="text-blue-600 hover:text-blue-700 text-xs font-medium underline" onclick="event.stopPropagation(); enhancedMusicTherapy.playPreview('${track.preview_url}', '${track.name.replace(/'/g, "\\'")}');">
                        Play 30s Preview
                    </button>
                </div>` : ''}
            </div>
        `;
    }
    
    getArtistNames(track) {
        if (track.artists && Array.isArray(track.artists)) {
            return track.artists.map(a => a.name).join(', ');
        }
        return track.artist || 'Unknown Artist';
    }
    
    formatDuration(ms) {
        if (!ms || ms === 0) return '0:00';
        const minutes = Math.floor(ms / 60000);
        const seconds = Math.floor((ms % 60000) / 1000);
        return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }
    
    playSpotifyTrack(index) {
        if (!this.spotifyTracks[index]) return;
        
        const track = this.spotifyTracks[index];
        this.currentTrackIndex = index;
        
        console.log('Playing track:', track.name);
        
        // Update UI
        this.updateCurrentTrackDisplay(`Now Playing: ${track.name}`, track);
        this.showMusicPlayer();
        this.updateSpotifyQueue();
        
        // Play the track
        if (track.preview_url) {
            this.playPreview(track.preview_url, track.name);
        } else if (track.external_urls && track.external_urls.spotify) {
            this.showSpotifyEmbed(track);
        } else {
            this.showTrackInfo(track);
        }
        
        // Update session stats
        this.updateMusicTime();
    }
    
    playPreview(previewUrl, trackName) {
        const spotifyPlayer = document.getElementById('spotifyPlayer');
        if (!spotifyPlayer) return;
        
        // Stop any currently playing audio
        this.stopAllAudio();
        
        spotifyPlayer.innerHTML = `
            <div class="bg-gradient-to-r from-green-500 to-green-600 text-white p-4 rounded-lg">
                <h4 class="font-bold mb-3">🎵 Now Playing Preview</h4>
                <p class="text-green-100 mb-3">${trackName}</p>
                <audio controls autoplay class="w-full bg-green-700 rounded">
                    <source src="${previewUrl}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
                <p class="text-green-200 text-sm mt-2">30-second preview courtesy of Spotify</p>
            </div>
        `;
        
        this.isPlaying = true;
        this.updatePlayButton();
        this.showMusicNotification(`Playing preview: ${trackName}`);
    }
    
    showSpotifyEmbed(track) {
        const spotifyPlayer = document.getElementById('spotifyPlayer');
        if (!spotifyPlayer || !track.external_urls || !track.external_urls.spotify) return;
        
        // Extract Spotify ID from URL
        const spotifyUrl = track.external_urls.spotify;
        const trackId = spotifyUrl.split('/track/')[1]?.split('?')[0];
        
        if (trackId) {
            spotifyPlayer.innerHTML = `
                <div class="bg-black rounded-lg overflow-hidden">
                    <iframe src="https://open.spotify.com/embed/track/${trackId}" 
                            width="100%" 
                            height="152" 
                            frameborder="0" 
                            allowtransparency="true" 
                            allow="encrypted-media">
                    </iframe>
                </div>
            `;
            this.isPlaying = true;
            this.updatePlayButton();
        } else {
            this.showTrackInfo(track);
        }
    }
    
    showTrackInfo(track) {
        const spotifyPlayer = document.getElementById('spotifyPlayer');
        if (!spotifyPlayer) return;
        
        const artistNames = this.getArtistNames(track);
        const spotifyUrl = track.external_urls?.spotify;
        
        spotifyPlayer.innerHTML = `
            <div class="bg-gradient-to-r from-purple-500 to-pink-500 text-white p-6 rounded-lg text-center">
                <h4 class="font-bold text-lg mb-2">${track.name}</h4>
                <p class="text-purple-100 mb-4">by ${artistNames}</p>
                ${spotifyUrl ? `
                <button class="bg-white text-purple-600 px-6 py-2 rounded-full font-medium hover:bg-gray-100 transition-colors" onclick="window.open('${spotifyUrl}', '_blank')">
                    🎵 Play Full Track on Spotify
                </button>` : ''}
                <p class="text-purple-200 text-sm mt-3">Complete song available on Spotify Premium</p>
            </div>
        `;
    }
    
    showMusicPlayer() {
        const musicPlayerContainer = document.getElementById('musicPlayerContainer');
        if (musicPlayerContainer) {
            musicPlayerContainer.classList.remove('hidden');
        }
    }
    
    updateSpotifyQueue() {
        const queueContainer = document.getElementById('playlistQueue');
        if (!queueContainer || !this.spotifyTracks.length) return;
        
        queueContainer.innerHTML = this.spotifyTracks.map((track, index) => {
            const isCurrentTrack = index === this.currentTrackIndex;
            const artistNames = this.getArtistNames(track);
            
            return `
                <div class="flex items-center justify-between p-2 rounded cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors ${isCurrentTrack ? 'bg-purple-100 dark:bg-purple-800' : ''}" onclick="enhancedMusicTherapy.playSpotifyTrack(${index})">
                    <div class="flex-1">
                        <div class="font-medium text-sm ${isCurrentTrack ? 'text-purple-800 dark:text-purple-200' : 'text-gray-800 dark:text-gray-200'}">
                            ${track.name}
                        </div>
                        <div class="text-xs text-gray-600 dark:text-gray-400">
                            ${artistNames}
                        </div>
                    </div>
                    <div class="flex items-center space-x-2">
                        <div class="text-xs text-gray-500">${this.formatDuration(track.duration_ms)}</div>
                        ${isCurrentTrack ? '<div class="text-purple-500 text-xs font-bold">♪ Playing</div>' : ''}
                    </div>
                </div>
            `;
        }).join('');
    }
    
    // Player controls
    togglePlayback() {
        if (this.spotifyTracks.length === 0) {
            this.showMusicNotification('Please select a mood first', 'warning');
            return;
        }
        
        if (!this.isPlaying && this.currentTrackIndex >= 0) {
            this.playSpotifyTrack(this.currentTrackIndex);
        } else {
            this.pauseMusic();
        }
    }
    
    toggleMainPlayer() {
        if (this.isPlaying) {
            this.pauseMusic();
        } else {
            this.resumeMusic();
        }
    }
    
    nextTrack() {
        if (this.spotifyTracks.length > 0) {
            this.currentTrackIndex = (this.currentTrackIndex + 1) % this.spotifyTracks.length;
            this.playSpotifyTrack(this.currentTrackIndex);
        }
    }
    
    previousTrack() {
        if (this.spotifyTracks.length > 0) {
            this.currentTrackIndex = this.currentTrackIndex > 0 ? this.currentTrackIndex - 1 : this.spotifyTracks.length - 1;
            this.playSpotifyTrack(this.currentTrackIndex);
        }
    }
    
    pauseMusic() {
        this.isPlaying = false;
        this.stopAllAudio();
        this.updatePlayButton();
        this.showMusicNotification('Music paused');
    }
    
    resumeMusic() {
        if (this.spotifyTracks.length > 0 && this.currentTrackIndex >= 0) {
            this.playSpotifyTrack(this.currentTrackIndex);
        }
    }
    
    stopAllAudio() {
        // Pause all audio elements
        document.querySelectorAll('audio').forEach(audio => {
            audio.pause();
            audio.currentTime = 0;
        });
    }
    
    updatePlayButton() {
        const playBtn = document.getElementById('playPauseMainBtn');
        if (playBtn) {
            playBtn.innerHTML = this.isPlaying ? '⏸️ Pause' : '▶️ Play';
        }
        
        const mainPlayBtn = document.getElementById('playPauseBtn');
        if (mainPlayBtn) {
            mainPlayBtn.innerHTML = this.isPlaying ? '⏸️ Pause Music' : '▶️ Play Music';
        }
    }
    
    updateMusicTime() {
        const musicTimeEl = document.getElementById('musicListenTime');
        if (musicTimeEl) {
            const currentTime = parseInt(musicTimeEl.textContent) || 0;
            musicTimeEl.textContent = currentTime + 1;
        }
    }
    
    // Fallback methods
    loadFallbackTracks(mood) {
        console.log('Loading fallback tracks for mood:', mood);
        
        this.updateCurrentTrackDisplay(`Loading curated ${mood} therapy music...`);
        
        const fallbackPlaylists = {
            happy: {
                name: 'Happy Therapy Music',
                description: 'Uplifting songs to boost your mood and energy',
                url: 'https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd',
                embed: 'https://open.spotify.com/embed/playlist/37i9dQZF1DX0XUsuxWHRQd'
            },
            sad: {
                name: 'Gentle Healing Music',
                description: 'Soothing tracks to help process difficult emotions',
                url: 'https://open.spotify.com/playlist/37i9dQZF1DX3Ogo9pFvBkY',
                embed: 'https://open.spotify.com/embed/playlist/37i9dQZF1DX3Ogo9pFvBkY'
            },
            anxious: {
                name: 'Calming Music for Anxiety',
                description: 'Peaceful sounds to reduce anxiety and stress',
                url: 'https://open.spotify.com/playlist/37i9dQZF1DWZqd5JICZI0u',
                embed: 'https://open.spotify.com/embed/playlist/37i9dQZF1DWZqd5JICZI0u'
            },
            calm: {
                name: 'Peaceful Meditation Music',
                description: 'Serene melodies for relaxation and mindfulness',
                url: 'https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwAYIy1',
                embed: 'https://open.spotify.com/embed/playlist/37i9dQZF1DX4sWSpwAYIy1'
            },
            focused: {
                name: 'Focus & Concentration',
                description: 'Instrumental music to enhance productivity',
                url: 'https://open.spotify.com/playlist/37i9dQZF1DWZeKCadgRdKQ',
                embed: 'https://open.spotify.com/embed/playlist/37i9dQZF1DWZeKCadgRdKQ'
            },
            motivated: {
                name: 'Motivational Music',
                description: 'Energetic tracks to boost motivation and drive',
                url: 'https://open.spotify.com/playlist/37i9dQZF1DX76Wlfdnj7AP',
                embed: 'https://open.spotify.com/embed/playlist/37i9dQZF1DX76Wlfdnj7AP'
            }
        };
        
        const playlist = fallbackPlaylists[mood] || fallbackPlaylists['calm'];
        this.showFallbackPlaylist(playlist, mood);
    }
    
    showFallbackPlaylist(playlist, mood) {
        const spotifyContainer = document.getElementById('spotifyTracksContainer');
        const tracksListContainer = document.getElementById('tracksList');
        
        if (!tracksListContainer) return;
        
        tracksListContainer.innerHTML = `
            <div class="text-center p-6 bg-gradient-to-r from-purple-100 to-pink-100 dark:from-purple-900/20 dark:to-pink-900/20 rounded-lg border border-purple-200 dark:border-purple-700">
                <h3 class="font-bold text-purple-800 dark:text-purple-200 mb-2 text-lg">${playlist.name}</h3>
                <p class="text-purple-600 dark:text-purple-300 text-sm mb-4">
                    ${playlist.description}
                </p>
                <div class="flex flex-col sm:flex-row gap-3 justify-center">
                    <button class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-medium transition-colors" onclick="window.open('${playlist.url}', '_blank')">
                        🎵 Open in Spotify
                    </button>
                    <button class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg font-medium transition-colors" onclick="enhancedMusicTherapy.embedFallbackPlaylist('${playlist.embed}')">
                        ▶️ Play Here
                    </button>
                </div>
                <p class="text-gray-600 dark:text-gray-400 text-xs mt-3">
                    Curated playlist for ${mood} therapy sessions
                </p>
            </div>
        `;
        
        if (spotifyContainer) {
            spotifyContainer.classList.remove('hidden');
        }
        
        this.showTherapyBenefits(mood);
        this.updateCurrentTrackDisplay(`Curated ${mood} therapy playlist ready`);
    }
    
    embedFallbackPlaylist(embedUrl) {
        this.showMusicPlayer();
        
        const spotifyPlayer = document.getElementById('spotifyPlayer');
        if (spotifyPlayer) {
            spotifyPlayer.innerHTML = `
                <div class="bg-black rounded-lg overflow-hidden">
                    <iframe src="${embedUrl}" 
                            width="100%" 
                            height="352" 
                            frameborder="0" 
                            allowtransparency="true" 
                            allow="encrypted-media">
                    </iframe>
                </div>
            `;
        }
        
        this.isPlaying = true;
        this.updatePlayButton();
        this.showMusicNotification('Spotify playlist embedded successfully');
    }
    
    // Therapy benefits and notifications
    showTherapyBenefits(mood) {
        const benefits = {
            'happy': 'Uplifting music releases endorphins and dopamine, naturally enhancing your joy and positive emotions.',
            'sad': 'Gentle, reflective music helps process difficult emotions and provides comfort during challenging times.',
            'anxious': 'Calming rhythms and frequencies can effectively lower cortisol levels and reduce anxiety symptoms.',
            'calm': 'Peaceful melodies synchronize with your relaxed state, promoting deeper mindfulness and inner peace.',
            'focused': 'Instrumental music enhances concentration by providing optimal background stimulation for cognitive tasks.',
            'motivated': 'Energetic beats increase adrenaline and motivation, perfect for achieving your goals and staying driven.'
        };
        
        const benefitText = benefits[mood] || 'Music therapy supports emotional wellness and mental health.';
        
        // Show benefits in a subtle notification
        setTimeout(() => {
            this.showMusicNotification(`💡 Therapy Benefit: ${benefitText}`, 'info', 6000);
        }, 2000);
    }
    
    showMusicNotification(message, type = 'success', duration = 4000) {
        // Remove existing notifications
        document.querySelectorAll('.music-notification').forEach(el => el.remove());
        
        const notification = document.createElement('div');
        notification.className = `music-notification fixed top-20 right-4 px-4 py-2 rounded-lg shadow-lg z-50 transform translate-x-full transition-transform duration-300 max-w-sm`;
        
        // Style based on type
        switch (type) {
            case 'success':
                notification.classList.add('bg-green-600', 'text-white');
                break;
            case 'warning':
                notification.classList.add('bg-yellow-600', 'text-white');
                break;
            case 'info':
                notification.classList.add('bg-blue-600', 'text-white');
                break;
            default:
                notification.classList.add('bg-purple-600', 'text-white');
        }
        
        notification.innerHTML = `
            <div class="flex items-start justify-between">
                <span class="text-sm">${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-white hover:text-gray-200">×</button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);
        
        // Auto-hide notification
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    notification.remove();
                }
            }, 300);
        }, duration);
    }
    
    setupAudioContext() {
        // Setup any audio context if needed for advanced features
        try {
            if (window.AudioContext || window.webkitAudioContext) {
                this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
                console.log('Audio context initialized');
            }
        } catch (error) {
            console.log('Audio context not available:', error);
        }
    }
}

// Initialize enhanced music therapy when DOM is ready
let enhancedMusicTherapy;
document.addEventListener('DOMContentLoaded', function() {
    enhancedMusicTherapy = new EnhancedMusicTherapy();
    
    // Make it globally available for onclick handlers
    window.enhancedMusicTherapy = enhancedMusicTherapy;
    
    console.log('Enhanced Music Therapy System Loaded Successfully');
});