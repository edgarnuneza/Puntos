var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
var ce = Cevent("canvas");
var width = ce.width;
var height = ce.height;
var agregar_puntos = true;

//var myJSON = '[]';
//var puntos = JSON.parse(myJSON);
var color;

window.onload = function() 
{
	const img = new Image()
	img.src = ubicacion_imagen;

	img.onload = () => {
		ce.image(10, 10, img).draw();
		cargarImagen();
		color = "#F10D0D";
	}
}

canvas.addEventListener("mousedown", function(e) 
{ 
	if(agregar_puntos){
		getMousePosition(canvas, e); 
	}

});

ce.bind("circle", {
	focus: function (c, e) {
		if(!agregar_puntos){
	    	c.remove(c.focused);
	    	c.focused = null;
		}
	},
	blur: function(c, e) {
	               
	}
});

/*ce.click("circle", function(c, e) {
	if(!agregar_puntos){

	}
    this.fill = "yellow";
});*/

function randint(i) {
    return parseInt(Math.random()*i);
}

function randcolor() {
    return "rgb(" + [randint(255), randint(255), randint(255)] + ")";
}

function cargarImagen()
{
	for (var i = puntos.length - 1; i >= 0; i--) {
		ce.circle(puntos[i].x, puntos[i].y, 5).attr("fill", puntos[i].color).draw();
	}
}
            
function borrar()
{
	agregar_puntos = false;
}

function agregar()
{
	agregar_puntos = true;
}

function getMousePosition(canvas, event) 
{ 
    let rect = canvas.getBoundingClientRect(); 
    let x = event.clientX - rect.left; 
    let y = event.clientY - rect.top; 
    dibujar(x, y); 
}

function dibujar(x, y)
{
	console.log(color)
	ce.circle(x, y, 5).attr("fill", color).draw();
}

function cambiarColor(nuevoColor)
{
	console.log("Se cambio el color");
	color = nuevoColor;
}
        
function guardar()
{
	puntos = [];
	var nuevoPunto;
	for (var i = 1; i < ce._shapes.length; i++)
	{
		nuevoPunto = {x:ce._shapes[i].x, y:ce._shapes[i].y, color:ce._shapes[i].fill};
		puntos.push(nuevoPunto);
	}
	var asJSON = JSON.stringify(puntos);
	console.log(asJSON);
}

function cambiarImagen(nombreImagen)
{
	input = document.getElementById("nombre_imagen");
	input.value = nombreImagen;
}
        /*ce.keydown("del", function(c, e){

        	console.log(c);
            if (c.focused) {
                c.remove(c.focused);
                c.focused = null;
            }
        }).draw();*/

        