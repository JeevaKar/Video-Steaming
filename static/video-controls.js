(() => {
    const container = document.querySelector(".video-container");
    const player = container?.querySelector(".video-player");
    const controls = container?.querySelector(".video-controls");

    if (!container || !player || !controls) {
        return;
    }

    const playButton = controls.querySelector('[data-action="toggle-play"]');
    const muteButton = controls.querySelector('[data-action="toggle-mute"]');
    const fullscreenButton = controls.querySelector('[data-action="toggle-fullscreen"]');
    const progress = controls.querySelector(".video-progress");
    const volume = controls.querySelector(".video-volume");
    const currentTime = controls.querySelector("[data-current-time]");
    const duration = controls.querySelector("[data-duration]");

    const formatTime = (time) => {
        if (!Number.isFinite(time)) {
            return "0:00";
        }

        const totalSeconds = Math.floor(time);
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        if (hours > 0) {
            return `${hours}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
        }

        return `${minutes}:${String(seconds).padStart(2, "0")}`;
    };

    const updateTime = () => {
        currentTime.textContent = formatTime(player.currentTime);
        duration.textContent = formatTime(player.duration);

        if (Number.isFinite(player.duration) && player.duration > 0) {
            progress.value = String((player.currentTime / player.duration) * 1000);
            progress.disabled = false;
        }
    };

    const updatePlaybackButton = () => {
        const isPlaying = !player.paused;
        playButton.textContent = isPlaying ? "Pause" : "Play";
        playButton.setAttribute("aria-label", isPlaying ? "Pause video" : "Play video");
    };

    const updateMuteButton = () => {
        const isMuted = player.muted || player.volume === 0;
        muteButton.textContent = isMuted ? "Unmute" : "Mute";
        muteButton.setAttribute("aria-label", isMuted ? "Unmute video" : "Mute video");
        muteButton.setAttribute("aria-pressed", String(isMuted));
    };

    const updateFullscreenButton = () => {
        const isFullscreen = document.fullscreenElement === container;
        fullscreenButton.textContent = isFullscreen ? "Exit fullscreen" : "Fullscreen";
        fullscreenButton.setAttribute("aria-label", isFullscreen ? "Exit fullscreen" : "Enter fullscreen");
    };

    playButton.addEventListener("click", () => {
        if (player.paused) {
            player.play().catch(updatePlaybackButton);
        } else {
            player.pause();
        }
    });

    muteButton.addEventListener("click", () => {
        player.muted = !player.muted;
        if (!player.muted && player.volume === 0) {
            player.volume = 0.5;
            volume.value = "0.5";
        }
        updateMuteButton();
    });

    fullscreenButton.addEventListener("click", () => {
        if (document.fullscreenElement === container) {
            document.exitFullscreen?.();
        } else {
            container.requestFullscreen?.();
        }
    });

    progress.addEventListener("input", () => {
        if (Number.isFinite(player.duration)) {
            player.currentTime = (Number(progress.value) / 1000) * player.duration;
            updateTime();
        }
    });

    volume.addEventListener("input", () => {
        player.volume = Number(volume.value);
        player.muted = player.volume === 0;
        updateMuteButton();
    });

    player.addEventListener("loadedmetadata", updateTime);
    player.addEventListener("durationchange", updateTime);
    player.addEventListener("timeupdate", updateTime);
    player.addEventListener("play", updatePlaybackButton);
    player.addEventListener("pause", updatePlaybackButton);
    player.addEventListener("ended", updatePlaybackButton);
    player.addEventListener("volumechange", updateMuteButton);
    document.addEventListener("fullscreenchange", updateFullscreenButton);

    updatePlaybackButton();
    updateMuteButton();
    updateFullscreenButton();
})();