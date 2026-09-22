const imageInput = document.getElementById("image");

const preview = document.getElementById("imagePreview");

imageInput.addEventListener("change", function(){

    const file = this.files[0];

    if(file){

        const reader = new FileReader();

        reader.onload = function(e){

            preview.src = e.target.result;

        }

        reader.readAsDataURL(file);

    }

});