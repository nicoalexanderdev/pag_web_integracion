class Carrito:
    
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.user = request.user if request.user.is_authenticated else None
        carrito = self.session.get('carrito')

        if not carrito:
          self.session['carrito'] = {}
          self.carrito = self.session['carrito']
        else:
           self.carrito = carrito 

    def agregar(self, producto):
        id = str(producto.get('id'))  # Usamos get para manejar casos donde 'id' podría no estar presente

        if id and id not in self.carrito.keys():  # Verificamos que 'id' no esté vacío y no esté ya en el carrito
            self.carrito[id] = {
                'producto_id': producto['id'],
                'nombre': producto['nombre'],
                'nombre_marca': producto['marca']['nom_marca'],
                'marca_id': producto['marca']['id'],
                'acumulado': producto['precio'],
                'cantidad': 1,
                'image_url': producto['image_url'],
                'nombre_categoria': producto['categoria']['nom_categoria'],
                'categoria_id': producto['categoria']['id'],
            }
            self.guardar_carrito()
        elif id in self.carrito.keys():
            self.carrito[id]['cantidad'] += 1
            self.carrito[id]['acumulado'] += producto['precio']
            self.guardar_carrito()
       
    def guardar_carrito(self):
        self.session['carrito'] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        id = str(producto['id'])

        if id in self.carrito.keys():
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, producto):
        id = str(producto['id'])

        if id in self.carrito.keys():
            self.carrito[id]['cantidad'] -= 1
            self.carrito[id]['acumulado'] -= producto['precio']

            if self.carrito[id]['cantidad'] <= 0: self.eliminar(producto)
            self.guardar_carrito()

    def limpiar(self):
        self.session['carrito'] = {}
        self.session.modified = True