window.addEventListener('DOMContentLoaded', (event) =>{
    getVisitorCount();
})

const functionApiUrl = 'https://getcounter123.azurewebsites.net/api/main';
const localFunctionApi = 'http://localhost:7071/api/main';

const getVisitorCount = () => {
    let count = 5;
    fetch(functionApiUrl).then(response => {
        return response.json()
    }).then(response =>{
        console.log("Website called function API.");
        count =  response.count;
        document.getElementById("counter").innerText = count;
    }).catch(function(error){
        console.log(error);
    });
    return count;
}