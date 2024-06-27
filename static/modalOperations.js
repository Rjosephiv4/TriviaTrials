document.addEventListener("DOMContentLoaded", function() {
    const modal = document.querySelector(".modalMe");
    const closeModal = document.querySelector('.close-button');

    try{
        closeModal.addEventListener('click', function(event){
            event.preventDefault()
            const checkbox = document.getElementById("deleteDisclaimer");
            const isChecked = checkbox.checked;
            console.log(isChecked);

            const checkDisclaimerData = {deleteDisclaimer: isChecked};

            fetch('/classic',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(checkDisclaimerData)
            })
            .then(response=> {
                if (!response.ok)
                {
                    throw new Error('Network Response was not ok');
                }
                return response.json();
            })
            .then(data =>{
                console.log('Sucess:', data);
            })
            .catch((error) => {
                console.error('Error: ', error);
            });

            modal.close();
        });
    }
    catch(exception)
    {
        console.log("Modal Was Not Oppened")
    }

    try
    {
        modal.showModal(); 
    }
    catch(exception)
    {
        console.log("Modal Was Not Oppened")
    }
});

