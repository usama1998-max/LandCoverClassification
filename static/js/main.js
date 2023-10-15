// CSRF TOKEN
$.ajaxSetup({
    headers: {
        'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val(),
    },
});

// NAVBAR
var nav_drop_btn = document.querySelector("#drop-btn");
var nav_drop_btn_content = document.querySelector(".dropdown-content");
var toggle = true;

if(nav_drop_btn)
    nav_drop_btn.addEventListener('click', function(){
        console.log("EVENT");
        if(toggle === true){
            nav_drop_btn_content.style.display = "flex";
            toggle = false;
        }

         else if(toggle === false){
            nav_drop_btn_content.style.display = "none";
            toggle = true;
        }
});


// TYPE WRITE ANIMATION
var TxtType = function(el, toRotate, period) {
    this.toRotate = toRotate;
    this.el = el;
    this.loopNum = 0;
    this.period = parseInt(period, 10) || 2000;
    this.txt = '';
    this.tick();
    this.isDeleting = false;
};

TxtType.prototype.tick = function() {
    var i = this.loopNum % this.toRotate.length;
    var fullTxt = this.toRotate[i];

    if (this.isDeleting) {
    this.txt = fullTxt.substring(0, this.txt.length - 1);
    } else {
    this.txt = fullTxt.substring(0, this.txt.length + 1);
    }

    this.el.innerHTML = '<span class="wrap">'+this.txt+'</span>';

    var that = this;
    var delta = 200 - Math.random() * 100;

    if (this.isDeleting) { delta /= 2; }

    if (!this.isDeleting && this.txt === fullTxt) {
    delta = this.period;
    this.isDeleting = true;
    } else if (this.isDeleting && this.txt === '') {
    this.isDeleting = false;
    this.loopNum++;
    delta = 500;
    }

    setTimeout(function() {
    that.tick();
    }, delta);
};

window.onload = function() {
    var elements = document.getElementsByClassName('typewrite');
    for (var i=0; i<elements.length; i++) {
        var toRotate = elements[i].getAttribute('data-type');
        var period = elements[i].getAttribute('data-period');
        if (toRotate) {
          new TxtType(elements[i], JSON.parse(toRotate), period);
        }
    }
    // INJECT CSS
    var css = document.createElement("style");
    css.type = "text/css";
    css.innerHTML = ".typewrite > .wrap { border-right: 0.08em solid #fff}";
    document.body.appendChild(css);
};


// DASHBOARD
var img_c_panel = document.querySelector("#img-c");
var img_s_panel = document.querySelector("#img-s");
var rec_img_panel = document.querySelector("#rec-img");
var dash_nav_btn = document.querySelectorAll(".dash-nav-btn");


//function get_data(){
//    $.ajax({
//        type: "GET",
//        headers: { "X-CSRFToken": csrf },
//        url: "/dashboard/",
//        dataType: "json",
//        contentType: "application/json",
//        success: function(res){
//            location.reload();
//        },
//        error: function(res){
//            console.log(res);
//        }
//    });
//}


for(var i=0;i<dash_nav_btn.length;i++){
    dash_nav_btn[i].addEventListener('click', function(e){
        $.ajax({
            type: "POST",
            url: "/dashboard/",
            dataType: "json",
            data: {dash_panel: e.target.value},
            success: function(res){

                location.reload();

            },
            error: function(res){
                console.log(res);
            }
        });

    });
}


// IMAGE INPUT
var img_c_input = document.querySelector("#img-classify-input");

// IMAGE CLASSIFY
var img_c_file = document.querySelector("#img-classify");

if(img_c_file !== null){
    img_c_file.addEventListener("dragenter", function(e){
        e.preventDefault();
        console.log('DRAG OVER EVENT');
        img_c_file.style.border = "2px dashed #007bff";
    });

    img_c_file.addEventListener("dragover", (e) => {
        e.preventDefault();
    });

    img_c_file.addEventListener("dragleave", function(e){
        console.log('DRAG LEAVE EVENT');
        img_c_file.style.border = "2px solid #6c757d";
    });

    img_c_file.addEventListener("drop", function(e){
        e.preventDefault();
        e.stopPropagation();

        let droppedFile = e.dataTransfer.files[0];
        if (droppedFile) {
            img_c_input.value = droppedFile.name;
            console.log("IMAGE DROPPED" + droppedFile.name);
        }

        console.log('DROP EVENT');
    });
}


// IMAGE SEGMENT
var img_c_file = document.querySelector("#img-classify");


var img_s_input = document.querySelector("#image-segment-input");

if(img_s_file !== null){
    img_c_file.addEventListener("dragenter", function(e){
        e.preventDefault();
        console.log('DRAG OVER EVENT');
        img_c_file.style.border = "2px dashed #007bff";
    });

    img_c_file.addEventListener("dragover", (e) => {
        e.preventDefault();
    });

    img_c_file.addEventListener("dragleave", function(e){
        console.log('DRAG LEAVE EVENT');
        img_c_file.style.border = "2px solid #6c757d";
    });

    img_c_file.addEventListener("drop", function(e){
        e.preventDefault();
        e.stopPropagation();

        let droppedFile = e.dataTransfer.files[0];
        if (droppedFile) {
            img_c_input.value = droppedFile.name;
            console.log("IMAGE DROPPED" + droppedFile.name);
        }

        console.log('DROP EVENT');
    });
}


