function getChain() {
    fetch('/get_chain')
        .then(response => response.json())
        .then(data => {
            const chainDataDiv = document.getElementById('chainData');
            chainDataDiv.innerHTML = ''; // Clear previous data
            data.chain.forEach(block => {
                const blockDiv = document.createElement('div');
                blockDiv.className = 'block';

                const h3 = document.createElement('h3');
                h3.textContent = `Block ${block.index}`;
                blockDiv.appendChild(h3);

                const pTimestamp = document.createElement('p');
                pTimestamp.textContent = `Timestamp: ${block.timestamp}`;
                blockDiv.appendChild(pTimestamp);

                const pProof = document.createElement('p');
                pProof.textContent = `Proof: ${block.proof}`;
                blockDiv.appendChild(pProof);

                const pPrevHash = document.createElement('p');
                pPrevHash.textContent = `Previous Hash: ${block.previous_hash}`;
                blockDiv.appendChild(pPrevHash);

                chainDataDiv.appendChild(blockDiv);
            });
        })
        .catch(error => console.error('Error fetching chain:', error));
}

window.onload = function() {
    getChain();
};