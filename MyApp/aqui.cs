using System;

class Program
{
    
    const int O1 = 50;
    const double O2 = 33.2;
    const int O3 = 100; // 

    static void Main()
    {
        Console.WriteLine("\n--- ingresa los datos  ---");


        Console.Write("\n Ingrese su Nombre: ");
        string nombre = Console.ReadLine();

        Console.Write("\n Ingrese su Apellido: ");
        string apellido = Console.ReadLine();

        Console.Write("\n Ingrese su Edad: ");
        int edad = int.Parse(Console.ReadLine());

        
        Console.WriteLine("\n--- Datos Ingresados ---");
        Console.WriteLine("\n Nombre: " + nombre);
        Console.WriteLine("\n Apellido: " + apellido);
        Console.WriteLine("\n Edad: " + edad);

       
        Console.WriteLine("\n Constante 1: " + O1);
        Console.WriteLine("Constante 2: " + O2);
        Console.WriteLine("Constante 3: " + O3);
    }
}