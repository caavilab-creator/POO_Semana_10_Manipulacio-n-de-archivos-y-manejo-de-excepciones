# ============================================
# SERVICIO: Gestión del Inventario
# CRUD de Productos con persistencia en archivo
# ============================================
import os
from modelos.producto import Producto

class InventarioServicio:
    def __init__(self, ruta_archivo: str = None):
        base_dir = os.path.dirname(__file__)
        ruta_archivo = os.path.join(
            base_dir,
            "registros",
            "inventario.txt"
        )
        self.ruta_archivo = ruta_archivo
        self.productos = []  # Lista de productos
        self.cargar_desde_archivo()
    
    # ----------- CARGAR DESDE ARCHIVO -----------
    def asegurar_archivo(self):
        """Crea la carpeta y el archivo si no existen"""
        carpeta = os.path.dirname(self.ruta_archivo)
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        if not os.path.exists(self.ruta_archivo):
            with open(self.ruta_archivo, "w", encoding="utf-8") as f:
                pass
    
    def cargar_desde_archivo(self) -> None:
        """
        Lee inventario.txt y carga self.productos.
        Si el archivo no existe, lo crea.
        """
        self.asegurar_archivo()
        self.productos.clear()
        
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    producto = self._linea_a_producto(linea)
                    if producto:
                        self.productos.append(producto)
        except FileNotFoundError:
            print("⚠️ Archivo de inventario no encontrado. Se creará uno nuevo.")
        except PermissionError:
            print("❌ Error: No hay permisos para leer el archivo de inventario.")
        except Exception as e:
            print(f"❌ Error al cargar el inventario: {e}")
    
    def guardar_en_archivo(self) -> None:
        """
        Guarda la lista de productos en inventario.txt.
        """
        try:
            self.asegurar_archivo()
            with open(self.ruta_archivo, "w", encoding="utf-8") as f:
                for p in self.productos:
                    f.write(self._producto_a_linea(p) + "\n")
            print("✅ Inventario guardado correctamente")
        except PermissionError:
            print("❌ Error: No hay permisos para escribir en el archivo de inventario.")
        except Exception as e:
            print(f"❌ Error al guardar el inventario: {e}")
    
    def _producto_a_linea(self, producto: Producto) -> str:
        """
        Convierte un Producto a una línea TXT: id|nombre|precio|cantidad|categoria
        """
        # Reemplazos simples para no romper el separador |
        nombre = producto.get_nombre().replace("|", "/")
        categoria = producto.get_categoria().replace("|", "/")
        return f"{producto.get_id()}|{nombre}|{producto.get_precio()}|{producto.get_cantidad()}|{categoria}"
    
    def _linea_a_producto(self, linea: str):
        """
        Convierte una línea TXT a Producto.
        Maneja errores sin romper el programa.
        """
        try:
            partes = linea.split("|")
            if len(partes) != 5:  # id|nombre|precio|cantidad|categoria
                return None
            id_p = int(partes[0])
            nombre = partes[1]
            precio = float(partes[2])
            cantidad = int(partes[3])
            categoria = partes[4]
            return Producto(id_p, nombre, precio, cantidad, categoria)
        except Exception:
            return None
    
    # ----------- AGREGAR -----------
    def agregar_producto(self):
        """Agrega un nuevo producto al inventario"""
        try:
            id_p = int(input("ID: "))
            nombre = input("Nombre: ")
            precio = float(input("Precio: "))
            cantidad = int(input("Cantidad: "))
            categoria = input("Categoría: ")
            
            # Validar duplicado
            if self.buscar_por_id(id_p):
                print("⚠️ Ya existe un producto con ese ID")
                return
            
            nuevo = Producto(id_p, nombre, precio, cantidad, categoria)
            self.productos.append(nuevo)
            self.guardar_en_archivo()
            print("✅ Producto agregado exitosamente")
        except ValueError:
            print("⚠️ Error en los datos ingresados")
    
    # ----------- LISTAR -----------
    def listar_productos(self):
        """Muestra todos los productos del inventario"""
        if not self.productos:
            print("📭 No hay productos registrados")
            return
        
        print("\n📋 INVENTARIO DE PRODUCTOS")
        print("=" * 60)
        for p in self.productos:
            print(p)
        print("=" * 60)
    
    # ----------- BUSCAR -----------
    def buscar_por_id(self, id_producto):
        """Busca un producto por su ID"""
        for p in self.productos:
            if p.get_id() == id_producto:
                return p
        return None
    
    # ----------- ACTUALIZAR -----------
    def actualizar_producto(self):
        """Actualiza la información de un producto existente"""
        try:
            id_p = int(input("ID a actualizar: "))
            producto = self.buscar_por_id(id_p)
            
            if not producto:
                print("❌ Producto no encontrado")
                return
            
            nuevo_nombre = input("Nuevo nombre: ")
            nuevo_precio = float(input("Nuevo precio: "))
            nueva_cantidad = int(input("Nueva cantidad: "))
            nueva_categoria = input("Nueva categoría: ")
            
            producto.set_nombre(nuevo_nombre)
            producto.set_precio(nuevo_precio)
            producto.set_cantidad(nueva_cantidad)
            producto.set_categoria(nueva_categoria)
            
            self.guardar_en_archivo()
            print("✅ Producto actualizado exitosamente")
        except ValueError:
            print("⚠️ Datos inválidos")
    
    # ----------- ELIMINAR -----------
    def eliminar_producto(self):
        """Elimina un producto del inventario"""
        try:
            id_p = int(input("ID a eliminar: "))
            producto = self.buscar_por_id(id_p)
            
            if not producto:
                print("❌ Producto no encontrado")
                return
            
            self.productos.remove(producto)
            self.guardar_en_archivo()
            print("🗑️ Producto eliminado exitosamente")
        except ValueError:
            print("⚠️ ID inválido")