internal class Program
{
    private static void Main(string[] args)
    {
        var lines = File.ReadAllLines($"{Environment.CurrentDirectory}/input.txt");
        var solution = new Solution(lines);

        Console.WriteLine($"Part one: {solution.SolvePartOne()}");
        Console.WriteLine($"Part two: {solution.SolvePartTwo()}");
    }
}