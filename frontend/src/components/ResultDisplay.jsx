import React from 'react';

function ResultDisplay({ content, isLoading, error }) {
    return (
        <div className="result-display">
        <h2>Resultado Generado</h2>
        {isLoading && <p>Cargando...</p>}
        {error && <p className="error-message">Error: {error}</p>}
        {content && !isLoading && !error && (
            <div className="generated-content">
                <pre>{content}</pre>
            </div>
        )}
        {!content && !isLoading && !error && (
            <p>El texto generado por la IA aparecerá aquí.</p>
        )}
        </div>
    );
}

export default ResultDisplay;