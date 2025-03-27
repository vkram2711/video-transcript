import './App.css';
import React, {useRef, useEffect, useState} from 'react';
import axios from 'axios';
import {Button, CircularProgress} from "@mui/material";
import './styles.css';


function App() {
    const fileInputRef = useRef(null);
    const [file, setFile] = useState(null);
    const [fileSelected, setFileSelected] = useState(false);
    const [videoLink, setVideoLink] = useState()
    const [transcribing, setTranscribing] = useState(false);
    const [transcript, setTranscript] = useState('');

    const BASE_URL = 'http://localhost:5003'

    const onChangeFile = () => {
        setFile(fileInputRef.current.files[0])
    };

    const handleFileSelect = () => {
        if (fileInputRef.current) {
            fileInputRef.current.click();
        }
    };

    const handleFileDrop = (event) => {
        event.preventDefault();
        const file = event.dataTransfer.files[0];
        if (file) {
            onChangeFile(file);
            setFileSelected(true); // Set file selected to true
        }
    };


    const connectToWebSocket = () => {

        // Establish WebSocket connection
        const socket = new WebSocket('ws://localhost:5003' + videoLink + '/transcribe');

        // WebSocket event listeners
        socket.onopen = () => {
            console.log('WebSocket connection established');
            setTranscribing(true);
        };

        socket.onmessage = (event) => {
            console.log('Message from server:', event.data);
            setTranscript(prevTranscript => prevTranscript + ' ' + event.data);
        };

        socket.onclose = () => {
            console.log('WebSocket connection closed');
            setTranscribing(false);
        };

        // Clean up function
        return () => {
            socket.close();
        };
    }

    useEffect(() => {
        const fetchAudioFile = async () => {
            if (!file) return;
            const formData = new FormData();
            formData.append("file", file)

            const apiUrl = BASE_URL + '/upload';

            axios
                .post(apiUrl, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    }
                })
                .then((res) => {
                    console.log(res.data)
                    setVideoLink(res.data['video_link'])
                    //setTranscript(res.data)
                }).catch((err) => {
                console.error(err)
            })
        }
        fetchAudioFile()
    }, [file]);

    const handleTranscribe = async () => {
        if (!videoLink) return;
        connectToWebSocket()
        //const apiUrl = videoLink + '/transcribe';
        //axios.post(apiUrl)
        //    .then((res) => {
        //        console.log(res.data)
        //        setTranscript(res.data['transcript'])
        //        setTranscribing(false);
//
        //    }).catch((err) => {
        //    console.error(err)
        //})
    }

    return (
        <div className="container">
            <h1>Video Transcript Extractor</h1>
            {!fileSelected && (
                <div
                    className="file-container"
                    onClick={handleFileSelect}
                    onDrop={handleFileDrop}
                    onDragOver={(event) => event.preventDefault()}
                >
                    <p>Drag & Drop video file here,</p>
                    <p>or click to select</p>
                    <input
                        type="file"
                        ref={fileInputRef}
                        accept="video/*, audio/*"
                        onChange={(e) => {
                            onChangeFile(e.target.files[0]);
                            setFileSelected(true);
                        }}
                        style={{display: 'none'}}
                    />
                    <Button
                        variant="contained"
                        color="secondary"
                        component="label"
                        style={{marginTop: '10px'}}
                    >
                        Select File
                    </Button>
                </div>
            )}
            {fileSelected && (
                <div className={`video-container ${fileSelected ? 'show' : ''}`}>
                    {videoLink && (
                        <video
                            controls
                            src={BASE_URL + videoLink}
                        />
                    )}
                </div>
            )}
            <div className="button-container">
                {transcribing ? (
                    <CircularProgress color="secondary"/>
                ) : (
                    !transcript && (<Button
                        variant="contained"
                        color="secondary"
                        disabled={!fileSelected || transcribing} // Update condition here
                        onClick={handleTranscribe}
                    >
                        Transcribe
                    </Button>)
                )}
            </div>
            {transcript && (
                <div className="transcript-container">
                    <h2>Transcript:</h2>
                    <p>{transcript}</p>
                </div>
            )}
        </div>
    );
}

export default App;
