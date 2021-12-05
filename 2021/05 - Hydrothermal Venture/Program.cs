using System;
using System.IO;

namespace AdventOfCodeDay5;

class Program
{
    static void Main(string[] args)
    {
        var lines = File.ReadAllLines($"{Environment.CurrentDirectory}/input.txt");
        var solution = new Solution();

        Console.WriteLine($"Part one: {solution.SolvePartOne(lines)}");
        Console.WriteLine($"Part two: {solution.SolvePartTwo(lines)}");
    }
}