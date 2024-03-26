const texts = ["Face Forward: Attendance in a Blink!",
            "Present with a Smile: Your Face is Your Pass!",
            "Look Here, You're Logged In!",
            "See and Be Seen: Attendance Made Effortless.",
            "Snap to Attend: Where Faces Count.",
            "Counted with a Glance: Welcome to Smart Attendance!",
            "Your Attendance, at Face Value.",
            "Instant Recognition, Instant Attendance.",
            "No Cards, No Codes, Just Your Smile.",
            "Face the Day: Attendance Simplified."];
        const typingSpeed = 100; // Time in milliseconds to type each character
        const displayDuration = 8000; // Duration to wait before starting the next text
        const textDisplayElement = document.getElementById("text-display");
        let currentTextIndex = 0;
        let currentCharIndex = 0;

        function typeText() {
            if (currentCharIndex < texts[currentTextIndex].length) {
                // Get the next character from the current text
                let nextChar = texts[currentTextIndex].charAt(currentCharIndex);

                // If the next character is a space, use a non-breaking space for visibility
                if (nextChar === ' ') {
                    nextChar = '&nbsp;';
                }

                // Append the next character or non-breaking space to the inner HTML of the text display element
                textDisplayElement.innerHTML += nextChar;

                currentCharIndex++;
                setTimeout(typeText, typingSpeed);
            } else {
                // Wait after the full text is displayed before moving to the next
                setTimeout(() => {
                    currentTextIndex = (currentTextIndex + 1) % texts.length; // Cycle through texts
                    currentCharIndex = 0; // Reset character index for the next text
                    textDisplayElement.innerHTML = ''; // Clear the text display for the next message
                    typeText(); // Start typing the next message
                }, displayDuration);
            }
        }

        // Start typing the first text
        typeText();
