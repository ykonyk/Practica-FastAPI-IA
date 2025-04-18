import React from 'react';

function PromptForm({ prompt, setPrompt, contentType, setContentType, onGenerate, isLoading }) {

    const handleSubmit = (event) => {
        event.preventDefault();
        if (!prompt.trim()) {
            alert("Por favor, introduce un prompt.");
            return;
        }
        onGenerate(prompt, contentType);
    };

    return (
        <form onSubmit={handleSubmit} className="prompt-form">
            <label htmlFor="prompt-input">Tu Idea o Tema:</label>
            <textarea
                id="prompt-input"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Ej: Un gato astronauta descubre un planeta de queso..."
                rows={4}
                disabled={isLoading}
                required
            />
            <label htmlFor="content-type-select">Tipo de Contenido:</label>
            <select
                id="content-type-select"
                value={contentType}
                onChange={(e) => setContentType(e.target.value)}
                disabled={isLoading}
            >
            <option value="idea para historia corta">Idea para Historia Corta</option>
            <option value="descripción de producto">Descripción de Producto</option>
            <option value="tweet">Tweet</option>
            <option value="poema simple">Poema Simple</option>
            <option value="general">General / Otro</option>
            </select>
            <button type="submit" disabled={isLoading}>
                {isLoading ? 'Generando...' : 'Generar'}
            </button>
        </form>
    );
}
export default PromptForm;