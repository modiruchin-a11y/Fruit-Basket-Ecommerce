function getLocation(){

    if(navigator.geolocation){

        navigator.geolocation.getCurrentPosition(success,error);

    }else{

        alert("Geolocation is not supported.");

    }

}

function success(position){

    let latitude = position.coords.latitude;
    let longitude = position.coords.longitude;

    fetch(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${latitude}&lon=${longitude}`)

    .then(response => response.json())

    .then(data => {

        document.getElementById("address").value = data.display_name;

    });

}

function error(){

    alert("Unable to fetch your location.");

}

