# Análisis y Refactorización del Código \- API Flask

Robinson Moscoso Perez  
Patrones de Diseño de Software  
Especialización Ingeniería de Software  
Universidad Tecnológica de Bolívar

## Identificación de Problemas

### **Code Smells y Problemas de Diseño Identificados:**

#### **1\. Inconsistencia en la validación de tokens**

* En `products.py`: token válido es `'abcd12345'`  
* En `categories.py`, `favorites.py`: token válido es `'abcd1234'`  
* **Problema**: Duplicación de lógica y falta de centralización

#### **2\. Violación del principio DRY (Don't Repeat Yourself)**

* La validación de autenticación se repite en cada endpoint  
* El mismo patrón de verificación de token aparece múltiples veces

#### **3\. Alto acoplamiento**

* Cada recurso depende directamente de `DatabaseConnection`  
* Lógica de negocio mezclada con lógica de acceso a datos

#### **4\. Falta de manejo de errores**

* No hay try-catch para operaciones de base de datos  
* Posibles fallos en la lectura/escritura de JSON no son manejados

#### **5\. Violación de Single Responsibility Principle (SRP)**

* `ProductsResource` maneja routing, validación, lógica de negocio y acceso a datos  
* Similar problema en todos los recursos

#### **6\. Código duplicado en autenticación**

* Cada método verifica el token de la misma manera  
* Mensajes de error duplicados

#### **7\. Problemas específicos en `categories.py`**

* En el método `delete()`: se llama a `parser.parse_args()` dos veces  
* Lógica de filtrado incorrecta: `[cat for cat in self.categories_data if cat["name"] != category_to_remove]` debería comparar con el nombre

  #### **8\. Falta de validación de datos**

* No se validan tipos de datos antes de procesarlos  
* No hay límites en longitud de strings o rangos numéricos


## Soluciones propuestas

#### **1\. Decorator Pattern (Comportamiento)**

* Para la autenticación de endpoints  
* Crea un decorador `@token_required` que centralice la validación

#### **2\. Repository Pattern (Estructural)**

* Separar la lógica de acceso a datos de la lógica de negocio  
* Crear repositorios específicos: `ProductRepository`, `CategoryRepository`, `FavoriteRepository`

#### **3\. Factory Pattern (Creacional)**

* Para la creación de conexiones a base de datos  
* Facilita testing y cambio de implementación

#### **4\. Singleton Pattern (Creacional)**

* Para la configuración de autenticación  
* Asegura una única fuente de verdad para tokens y configuración

#### **5\. Service Layer Pattern (Arquitectural)**

* Separar lógica de negocio en servicios  
* `ProductService`, `CategoryService`, `FavoriteService`

## Aplicaciones de los cambios:

Los cambios aplicados se encuentran en el repositorio público:   
[rmoscosp/CourseDesignPatterns: Aplicacion de la clase de patrones de diseño de la UTB](https://github.com/rmoscosp/CourseDesignPatterns) 

Adicional a los cambios realizados las pruebas se hicieron con el complemento  Rest Client de Visual Studio Code, el cual permite crear un archivo con los request a realizar, el archivo de test es: `testClient.http`  
Url del componente de Visual Studio Code: [REST Client \- Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)

## Conclusiones y reflexiones

* El análisis del código reveló problemas estructurales significativos que son comunes en sistemas desarrollados sin consideración de principios de diseño.   
* La violación del principio DRY fue el problema más evidente, con lógica de autenticación duplicada en cada endpoint y validaciones repetidas sin centralización, esto no solo aumenta la probabilidad de errores, sino que dificulta el mantenimiento.  
* El alto acoplamiento entre los recursos y la capa de acceso a datos (`DatabaseConnection`) representa un obstáculo para la escalabilidad y testabilidad del sistema. Cada componente depende directamente de implementaciones concretas en lugar de abstracciones, lo que significa que cualquier cambio en la persistencia requeriría modificaciones en múltiples archivos  
* La violación del principio de responsabilidad única (SRP) es problemática: clases como `products.py` manejan routing, validación, lógica de negocio y acceso a datos simultáneamente. Esto genera código difícil de entender, probar y modificar.  
* La aplicación de patrones de diseño demostró ser altamente efectiva para resolver los problemas identificados.   
* El patrón Decorator para la autenticación eliminó completamente la duplicación de código y centralizó la lógica de seguridad en un único punto.   
* El patrón Repository separó exitosamente las preocupaciones de acceso a datos de la lógica de negocio.   
* El patrón Factory facilitó la creación de objetos de manera consistente y extensible.  
* La refactorización mejoró significativamente la mantenibilidad, testabilidad y claridad del código sin alterar la funcionalidad externa del sistema.  
  