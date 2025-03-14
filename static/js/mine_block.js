 // Function to call the '/mine_block' API and display the mined block's details

function mineBlock() {
    fetch('/mine_block')
        .then(response => response.json())
        .then(data => {
            console.log(data+'RandomString');
            const blockDataDiv = document.getElementById('blockData');
            blockDataDiv.innerHTML = `
                <div class="block">
                    <h3>Block ${data.index} Mined</h3>
                    <p>Timestamp: ${data.timestamp}</p>
                    <p>Proof: ${data.proof}</p>
                    <p>Previous Hash: ${data.previous_hash}</p>
                </div>
            `;
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
          //Example: document.querySelector(".faq--0" + i + "h1").innerHTML = json[0].title;
            //Example: document.querySelector(".faq--0" + i + " p").innerHTML = json[0].answer;
            document.querySelector(".faq--01 h1").innerHTML = json[0].title;
            document.querySelector(".faq--01 p").innerHTML = json[0].answer;
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

