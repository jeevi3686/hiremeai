# Lab Assessment Report
## Online Voice-Enabled Chatbot Using Speech Recognition and Deep Learning

**Project Name:** HireMeAI — Voice-Enabled AI Chatbot  
**Student Name:** Jeevitesh  
**Institution:** Vellore Institute of Technology  
**Course Assessment:** Lab Assessment — 20 Marks

### 1. Objective

The objective of this project is to develop and deploy an online chatbot that accepts voice input, converts speech into text, processes the user's query using a deep-learning-based language model, and generates an appropriate response. The application displays the recognized speech and chatbot response and supports spoken output.

### 2. Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python and FastAPI
- **Speech Recognition:** Browser Web Speech API (`SpeechRecognition` / `webkitSpeechRecognition`)
- **Deep Learning-Based Chatbot:** Pretrained language model accessed through the Groq API (`openai/gpt-oss-120b`)
- **Speech Output:** Browser Speech Synthesis API
- **Deployment:** Render
- **Version Control:** Git and GitHub

### 3. Dataset

The application uses candidate portfolio information and resume content as contextual information for answering relevant user questions. User queries and manually selected test prompts can be used to evaluate the chatbot's behavior.

The current implementation does not train a separate intent-classification model on a custom labeled dataset. Instead, it uses a pretrained language model to understand and respond to natural-language queries. Therefore, no custom model-training dataset or training accuracy is claimed.

### 4. Model Architecture

The system follows a client-server architecture:

1. **Speech input layer:** Captures the user's speech through the browser microphone.
2. **Speech-to-text layer:** The Web Speech API recognizes the speech and converts it into text.
3. **Backend layer:** FastAPI receives the recognized text and handles the chatbot request.
4. **Language-model layer:** The Groq API provides access to the pretrained `openai/gpt-oss-120b` language model, which processes the query using the supplied instructions and relevant candidate information.
5. **Response layer:** The generated response is streamed back to the frontend and displayed to the user.
6. **Speech output layer:** The browser Speech Synthesis API can read the response aloud.

The speech-recognition and speech-synthesis components are browser APIs. The deep-learning-based language model is accessed remotely through Groq; it is not trained locally by this application.

### 5. Methodology

1. The user opens the publicly deployed application.
2. The user enables microphone access and speaks a query.
3. The browser's speech-recognition API converts the speech into text.
4. The recognized text is displayed in the interface.
5. The frontend sends the query to the FastAPI backend.
6. The backend invokes the configured language model with the relevant context and instructions.
7. The generated answer is returned to the frontend.
8. The answer is displayed and can be spoken aloud using speech synthesis.

The application can also accept typed questions. This provides an alternative when microphone access or browser speech recognition is unavailable.

### 6. Results and Testing

The following functional tests should be performed on the deployed application:

| Test | Expected outcome |
|---|---|
| Microphone access | The browser requests microphone permission |
| Speech recognition | Spoken input is converted into text |
| Transcript display | Recognized text appears in the interface |
| Chatbot response | A relevant answer is generated |
| Response display | The chatbot answer appears in the interface |
| Speech synthesis | The answer is read aloud when enabled |
| Online deployment | The application is accessible through its public URL |

The application supports voice input, language-model-based responses, and spoken output. Final test outcomes should be recorded after testing the deployed version. No quantitative accuracy or latency measurements are claimed without formal measurement.

### 7. Limitations

- Browser speech-recognition support varies by browser and device.
- Microphone access requires user permission and a supported browser environment.
- Responses depend on the availability of the hosted language-model API.
- The current application does not contain a separately trained intent-classification model.

### 8. Conclusion

HireMeAI demonstrates an online voice-enabled chatbot by combining browser-based speech recognition, a FastAPI backend, a pretrained deep-learning language model, and browser-based speech synthesis. The application is deployed online and can be accessed through a public URL. The project demonstrates the integration of speech processing and conversational AI in a web application.

### 9. Submission Links

- **Live Application:** https://hiremeai-v04a.onrender.com/
- **Source Code:** https://github.com/jeevi3686/hiremeai
