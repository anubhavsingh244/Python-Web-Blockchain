function getChain() {
    fetch('/get_chain')
        .then(response => response.json())
        .then(data => {
            const chainDataDiv = document.getElementById('chainData');
            chainDataDiv.innerHTML = ''; // Clear previous data
            data.chain.forEach(block => {
                chainDataDiv.innerHTML += `
                    <div class="block">
                        <h3>Block ${block.index}</h3>
                        <p>Timestamp: ${block.timestamp}</p>
                        <p>Proof: ${block.proof}</p>
                        <p>Previous Hash: ${block.previous_hash}</p>
                    </div>
                `;
            });
        })
        .catch(error => console.error('Error fetching chain:', error));
}

window.onload = function() {
    getChain();
};