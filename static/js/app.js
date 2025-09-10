function activeMenuOption(href) {
    $(".app-menu .nav-link")
    .removeClass("active")
    .removeAttr('aria-current')

    $(`[href="${(href ? href : "#/")}"]`)
    .addClass("active")
    .attr("aria-current", "page")
}

const app = angular.module("angularjsApp", ["ngRoute"])
app.config(function ($routeProvider, $locationProvider) {
    $locationProvider.hashPrefix("")

    $routeProvider
    .when("/", {
        templateUrl: "/app",
        controller: "appCtrl"
    })
    .when("/productos", {
        templateUrl: "/productos",
        controller: "productosCtrl"
    })
    .when("/etiquetas", {
        templateUrl: "/etiquetas",
        controller: "etiquetasCtrl"
    })
    .when("/decoraciones", {
        templateUrl: "/decoraciones",
        controller: "decoracionesCtrl"
    })
    .when("/cuentas", {
        templateUrl: "/cuentas",
        controller: "cuentasCtrl"
    })
    .when("/notasFinancieras", {
    templateUrl: "/notasFinancieras",
    controller: "notasfinancierasCtrl"
    })
    .otherwise({
        redirectTo: "/"
    })
})
app.run(["$rootScope", "$location", "$timeout", function($rootScope, $location, $timeout) {
    function actualizarFechaHora() {
        lxFechaHora = DateTime
        .now()
        .setLocale("es")

        $rootScope.angularjsHora = lxFechaHora.toFormat("hh:mm:ss a")
        $timeout(actualizarFechaHora, 1000)
    }

    $rootScope.slide = ""

    actualizarFechaHora()

    $rootScope.$on("$routeChangeSuccess", function (event, current, previous) {
        $("html").css("overflow-x", "hidden")
        
        const path = current.$$route.originalPath

        if (path.indexOf("splash") == -1) {
            const active = $(".app-menu .nav-link.active").parent().index()
            const click  = $(`[href^="#${path}"]`).parent().index()

            if (active != click) {
                $rootScope.slide  = "animate__animated animate__faster animate__slideIn"
                $rootScope.slide += ((active > click) ? "Left" : "Right")
            }

            $timeout(function () {
                $("html").css("overflow-x", "auto")

                $rootScope.slide = ""
            }, 1000)

            activeMenuOption(`#${path}`)
        }
    })
}])

app.controller("appCtrl", function ($scope, $http) {
    $("#frmInicioSesion").submit(function (event) {
        event.preventDefault()
        $.post("iniciarSesion", $(this).serialize(), function (respuesta) {
            if (respuesta.length) {
                alert("Iniciaste Sesión")
                window.location = "/#/productos"

                return
            }

            alert("Usuario y/o Contraseña Incorrecto(s)")
        })
    })
})
app.controller("productosCtrl", function ($scope, $http) {
    function buscarProductos() {
        $.get("/tbodyProductos", function (trsHTML) {
            $("#tbodyProductos").html(trsHTML)
        })
    }

    buscarProductos()
    
     // Enable pusher logging - don't include this in production
    Pusher.logToConsole = true;

    var pusher = new Pusher('bc1c723155afce8dd187', {
      cluster: 'us2'
    });

     var channel = pusher.subscribe("canalProductos")
    channel.bind("eventoProductos", function(data) {
        // alert(JSON.stringify(data))
        buscarProductos()
    })
    
    $(document).on("submit", "#frmProducto", function (event) {
        event.preventDefault()

        $.post("/producto", {
            id: "",
            nombre: $("#txtNombre").val(),
            precio: $("#txtPrecio").val(),
            existencias: $("#txtExistencias").val(),
        })
    })

    $(document).on("click", ".btn-ingredientes", function (event) {
        const id = $(this).data("id")

        $.get(`/productos/ingredientes/${id}`, function (html) {
            modal(html, "Ingredientes", [
                {html: "Aceptar", class: "btn btn-secondary", fun: function (event) {
                    closeModal()
                }}
            ])
        })
    })
})



app.controller("decoracionesCtrl", function ($scope, $http) {
    function buscarDecoraciones() {
        $.get("/tbodyDecoraciones", function (trsHTML) {
            $("#tbodyDecoraciones").html(trsHTML)
        })
    }

    buscarDecoraciones()
    
    // Enable pusher logging - don't include this in production
    Pusher.logToConsole = true

    var pusher = new Pusher("e57a8ad0a9dc2e83d9a2", {
      cluster: "us2"
    })

    var channel = pusher.subscribe("canalDecoraciones")
    channel.bind("eventoDecoraciones", function(data) {
        // alert(JSON.stringify(data))
        buscarDecoraciones()
    })

    $(document).on("submit", "#frmDecoracion", function (event) {
        event.preventDefault()

        $.post("/decoracion", {
            id: "",
            nombre: $("#txtNombre").val(),
            precio: $("#txtPrecio").val(),
            existencias: $("#txtExistencias").val(),
        })
    })
})

app.controller("notasfinancierasCtrl", function ($scope, $http) {
    function buscarNotasFinancieras() {
        $.get("/tbodyNotasFinancieras", function (trsHTML) {
            $("#tbodyNotasFinancieras").html(trsHTML)
        })
    }

    buscarNotasFinancieras()
    
    // Enable pusher logging - don't include this in production
    Pusher.logToConsole = true;

    var pusher = new Pusher('bc1c723155afce8dd187', {
      cluster: 'us2'
    });

    var channel = pusher.subscribe("canalNotasFinancieras")
    channel.bind("eventoNotasFinancieras", function(data) {
        // alert(JSON.stringify(data))
        buscarNotasFinancieras()
    })
    
    $(document).on("submit", "#frmNotaFinanciera", function (event) {
        event.preventDefault()

        $.post("/notafinanciera", {
            idNota: "",
            titulo: $("#txtTitulo").val(),
            descripcion: $("#txtDesc").val(),
        })
    })
app.controller("notasfinancierasCtrl", function ($scope, $http) {
    function buscarNotasFinancieras() {
        $.get("/tbodyNotasFinancieras", function (trsHTML) {
            $("#tbodyNotasFinancieras").html(trsHTML)
        })
    }

    buscarNotasFinancieras()
    
    // Enable pusher logging - don't include this in production
    Pusher.logToConsole = true;

    var pusher = new Pusher('bc1c723155afce8dd187', {
      cluster: 'us2'
    });

    var channel = pusher.subscribe("canalNotasFinancieras")
    channel.bind("eventoNotasFinancieras", function(data) {
        buscarNotasFinancieras()
    })
    
    $(document).on("submit", "#frmNotaFinanciera", function (event) {
        event.preventDefault()
        $.post("/notafinanciera", {
            idNota: "",
            titulo: $("#txtTitulo").val(),
            descripcion: $("#txtDesc").val(),
        })
    })

    // ---------------------------
    // NUEVA FUNCIÓN DE ELIMINACIÓN
    // ---------------------------
    $(document).on("click", ".btn-eliminar-nota", function () {
        const idNota = $(this).data("id")  // asumimos que el botón tiene data-id="123"
        
        if (confirm("¿Seguro que quieres eliminar esta nota?")) {
            $.ajax({
                url: `/notafinanciera/${idNota}`,
                type: "DELETE",
                success: function(respuesta) {
                    alert("Nota eliminada")
                    buscarNotasFinancieras() // refresca la tabla
                },
                error: function(err) {
                    alert("Error al eliminar la nota")
                    console.error(err)
                }
            })
        }
    })
})





app.controller("cuentasCtrl", function ($scope, $http) {
    function buscarCuentas() {
        $.get("/tbodyCuentas", function (trsHTML) {
            $("#tbodyCuentas").html(trsHTML)
        })
    }

    buscarCuentas()
    
     // Enable pusher logging - don't include this in production
    Pusher.logToConsole = false;

    var pusher = new Pusher('bc1c723155afce8dd187', {
      cluster: 'us2'
    });

     var channel = pusher.subscribe("canalCuentas")
    channel.bind("eventoCuentas", function(data) {
        buscarCuentas()
    })
    
    $(document).on("submit", "#frmCuenta", function (event) {
        event.preventDefault()

        $.post("/cuenta", {
            id: "",
            nombre: $("#txtNombre").val(),
            balance: $("#txtBalance").val()
        })
    })
})

app.controller("etiquetasCtrl", function ($scope, $http) {
    function buscarEtiquetas() {
        $.get("/tbodyEtiquetas", function (trsHTML) {
            $("#tbodyEtiquetas").html(trsHTML)
        })
    }

    buscarEtiquetas()
    
     // Enable pusher logging - don't include this in production
    Pusher.logToConsole = false;

    var pusher = new Pusher('bc1c723155afce8dd187', {
      cluster: 'us2'
    });

     var channel = pusher.subscribe("canalEtiquetas")
    channel.bind("eventoEtiquetas", function(data) {
        buscarEtiquetas()
    })
    
    $(document).on("submit", "#frmEtiqueta", function (event) {
        event.preventDefault()

        $.post("/etiqueta", {
            id: "",
            nombre: $("#txtNombre").val(),
        })
    })
})


const DateTime = luxon.DateTime
let lxFechaHora

document.addEventListener("DOMContentLoaded", function (event) {
    const configFechaHora = {
        locale: "es",
        weekNumbers: true,
        // enableTime: true,
        minuteIncrement: 15,
        altInput: true,
        altFormat: "d/F/Y",
        dateFormat: "Y-m-d",
        // time_24hr: false
    }

    activeMenuOption(location.hash)
})










