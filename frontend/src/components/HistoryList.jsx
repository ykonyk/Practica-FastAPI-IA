import React from 'react';

function HistoryList({ history }) {
    return (
        <div className="history-list">
        <h2>Historial de Creaciones</h2>
        {history.length === 0 ? (
            <p>No hay historial todavía.</p>
        ) : (
            <ul>
            {history.map((item) => (
                <li key={item.id}>
                <strong>Prompt ({item.content_type}):</strong> {item.prompt}
                <br />
                <em>Generado ({new Date(item.timestamp).toLocaleString()}):</em>
                <pre className="history-content">{item.generated_text || '(No generado)'}</pre>
                </li>
            ))}
            </ul>
        )}
        </div>
    );
}

export default HistoryList;