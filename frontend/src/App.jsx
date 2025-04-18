import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import PromptForm from './components/PromptForm';
import ResultDisplay from './components/ResultDisplay';
import HistoryList from './components/HistoryList';
import './App.css'; 

const API_URL = 'http://127.0.0.1:8000';

function App() {
  const [prompt, setPrompt] = useState('');
  const [contentType, setContentType] = useState('idea para historia corta');
  const [generatedContent, setGeneratedContent] = useState('');
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Función para obtener el historial
  const fetchHistory = useCallback(async () => {
    // No mostrar error de historial si ya hay un error de generación
    try {
      const response = await axios.get(`${API_URL}/history`);
      setHistory(response.data);
    } catch (err) {
      console.error("Error fetching history:", err);
      // No establecer un error aquí para no sobreescribir errores de generación
    }
  }, []);

  // Cargar historial inicial al montar el componente
  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]); // Depende de fetchHistory

  // Función para manejar la generación de contenido
  const handleGenerate = async (currentPrompt, currentContentType) => {
    setIsLoading(true);
    setError(null); // Limpiar errores anteriores
    setGeneratedContent(''); // Limpiar resultado anterior

    try {
      const response = await axios.post(`${API_URL}/generate`, {
        prompt: currentPrompt,
        content_type: currentContentType,
      });
      setGeneratedContent(response.data.generated_text); // Asume que la API devuelve el objeto Creation
      // Refrescar el historial después de una generación exitosa
      fetchHistory();
    } catch (err) {
      console.error("Error generating content:", err);
      let errorMessage = "Ocurrió un error al generar el contenido.";
      if (err.response) {
        // El backend envió una respuesta con código de error
        console.error("Data:", err.response.data);
        console.error("Status:", err.response.status);
        errorMessage = err.response.data.detail || `Error ${err.response.status}`; // Usa el detalle de FastAPI si está disponible
      } else if (err.request) {
        // La petición se hizo pero no hubo respuesta
        errorMessage = "No se pudo conectar con el servidor. ¿Está ejecutándose?";
      }
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Asistente Creativo AI</h1>

      <PromptForm
        prompt={prompt}
        setPrompt={setPrompt}
        contentType={contentType}
        setContentType={setContentType}
        onGenerate={handleGenerate}
        isLoading={isLoading}
      />

      <ResultDisplay
        content={generatedContent}
        isLoading={isLoading}
        error={error}
      />

      <HistoryList history={history} />
    </div>
  );
}

export default App;