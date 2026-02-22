# ============================================
# MODELO: Producto
# Representa un producto del inventario
# ============================================
class Producto:
    # ----------- CONSTRUCTOR -----------
    def __init__(self, id_producto, nombre, precio, cantidad, categoria):
        self.__id_producto = id_producto
        self.__nombre = nombre
        self.__precio = precio
        self.__cantidad = cantidad
        self.__categoria = categoria
    
    # ----------- GETTERS -----------
    def get_id(self):
        return self.__id_producto
    
    def get_nombre(self):
        return self.__nombre
    
    def get_precio(self):
        return self.__precio
    
    def get_cantidad(self):
        return self.__cantidad
    
    def get_categoria(self):
        return self.__categoria
    
    # ----------- SETTERS -----------
    def set_nombre(self, nombre):
        self.__nombre = nombre
    
    def set_precio(self, precio):
        if precio > 0:
            self.__precio = precio
        else:
            print("⚠️ Precio inválido")
    
    def set_cantidad(self, cantidad):
        if cantidad >= 0:
            self.__cantidad = cantidad
        else:
            print("⚠️ Cantidad inválida")
    
    def set_categoria(self, categoria):
        self.__categoria = categoria
    
    # ----------- MÉTODO STR -----------
    def __str__(self):
        return (
            f"[{self.__id_producto}] "
            f"{self.__nombre} | "
            f"${self.__precio:.2f} | "
            f"Stock: {self.__cantidad} | "
            f"{self.__categoria}"
        )