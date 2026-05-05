 // Function to call the '/mine_block' API and display the mined block's details

function mineBlock() {
    fetch('/mine_block')
        .then(response => response.json())
        .then(data => {
            console.log(data+'RandomString');
            const blockDataDiv = document.getElementById('blockData');

            // Securely create elements instead of using innerHTML
            const blockDiv = document.createElement('div');
            blockDiv.className = 'block';

            const h3 = document.createElement('h3');
            h3.textContent = `Block ${data.index} Mined`;
            blockDiv.appendChild(h3);

            const pTimestamp = document.createElement('p');
            pTimestamp.textContent = `Timestamp: ${data.timestamp}`;
            blockDiv.appendChild(pTimestamp);

            const pProof = document.createElement('p');
            pProof.textContent = `Proof: ${data.proof}`;
            blockDiv.appendChild(pProof);

            const pPrevHash = document.createElement('p');
            pPrevHash.textContent = `Previous Hash: ${data.previous_hash}`;
            blockDiv.appendChild(pPrevHash);

            // Clear previous data if any and append the new block
            blockDataDiv.innerHTML = '';
            blockDataDiv.appendChild(blockDiv);
        })
        .catch(error => console.error('Error mining block:', error));
}

window.onload = function() {
    mineBlock();
};

/* //Event on ready DOM
document.addEventListener("DOMContentLoaded", function () {
    //Fetch data
    fetch('/mine_block')
        .then((response) => response.json())
        .then((json) => {
            //Then json info is here
            console.log(json);

            //You can play here doing a loop and using de iterator "i" for make it at one.
            //Example: document.querySelector(".faq--0" + i + "h1").textContent = json[0].title;
            //Example: document.querySelector(".faq--0" + i + " p").textContent = json[0].answer;
            document.querySelector(".faq--01 h1").textContent = json[0].title;
            document.querySelector(".faq--01 p").textContent = json[0].answer;
        })
}); */

/* fetch('/mine_block')

  .then(response => response.json())

  .then(jsonData => {

    const listIndex = document.getElementById('index');
    const listMessage = document.getElementById('message')

    jsonData.items.forEach(item => {

      const listItem = document.createElement('li');

      listItem.textContent = item.name;

      listElement.appendChild(listItem);

    });

  }); */

