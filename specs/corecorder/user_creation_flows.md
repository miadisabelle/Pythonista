# User Creation Flows: Orchestrating Thought Transformation

This section maps the primary user journeys within the `corecorder` application, illustrating how users advance toward their creative goals.

## Flow 1: Idea Capture & Initial Transcription

**Desired Outcome:** To quickly capture a spoken idea and obtain its initial textual representation.

1.  **User Initiates:** User opens the application, optionally sets a base directory and basename for the recording.
2.  **Audio Recording:** User taps the "Record" button, speaks their thoughts, and then taps "Stop".
3.  **Automatic Transcription:** The application automatically processes the recorded audio, transcribing it into text.
4.  **Initial Text Manifestation:** The transcribed text appears in the main `text_view`, and the audio and initial text files are saved.

## Flow 2: Text Refinement & Processing

**Desired Outcome:** To refine, clarify, or transform the transcribed text using AI-powered tools.

1.  **Text Present:** User has text (either freshly transcribed or loaded) displayed in the `text_view`.
2.  **Process Selection:** User taps a processing button (e.g., "DKore" for correction, "Sum" for summarization, "d2s" for detail shaping).
3.  **AI Transformation:** The application sends the current text to an external LLM service for the selected transformation.
4.  **Refined Text Manifestation:** The processed text replaces the previous content in the `text_view`, and the new version is saved, often with a specific suffix.

## Flow 3: Audio Synthesis & Review

**Desired Outcome:** To generate spoken audio from the refined text and review its auditory manifestation.

1.  **Text Present:** User has text in the `text_view` (typically a refined version).
2.  **Voice Selection:** User selects a desired language and voice from the segmented control.
3.  **Synthesis Initiation:** User taps the "Synt" (Synthesize) button.
4.  **Audio Manifestation:** The application sends the text to a text-to-speech service, saves the synthesized audio file, and enables the "Play" button.
5.  **Auditory Review:** User taps the "Play" button to listen to the synthesized audio.

## Flow 4: Iteration & Versioning

**Desired Outcome:** To manage and track different versions and iterations of a creative piece.

1.  **Content Modification:** User directly edits the text in the `text_view` or applies processing (Flow 2).
2.  **Version Saving:** User taps the "Save" button, or a processing step automatically saves the new version.
3.  **Iteration Navigation:** User uses "Previous" and "Next" buttons to navigate through different saved iterations of the content, allowing for review and comparison of the creative progression.