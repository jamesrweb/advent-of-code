using System.Text.RegularExpressions;

class Solution
{
    private List<Command> commands;

    public Solution(string[] lines)
    {
        commands = ParseCommandsFromLines(lines);
    }

    public long SolvePartOne() => ActiveCubesInRange(50);

    public long SolvePartTwo() => ActiveCubesInRange(int.MaxValue);

    private List<Command> ParseCommandsFromLines(string[] lines)
    {
        return lines.Aggregate(new List<Command>(), (accumulator, line) =>
        {
            var matches = Regex.Matches(line, "[+-]?[0-9]+").Select(match => match.Value).Select(value => Int32.Parse(value)).ToList();

            if (matches.Count != 6)
            {
                throw new Exception($"Invalid line detected: {line}");
            }

            var xRange = new Range(matches[0], matches[1]);
            var yRange = new Range(matches[2], matches[3]);
            var zRange = new Range(matches[4], matches[5]);
            var cuboid = new Cuboid(xRange, yRange, zRange);
            var command = new Command(line.StartsWith("on"), cuboid);

            accumulator.Add(command);

            return accumulator;
        });
    }

    private long ActiveCubesInRange(int range)
    {
        var xRange = new Range(-range, range);
        var yRange = new Range(-range, range);
        var zRange = new Range(-range, range);
        var searchArea = new Cuboid(xRange, yRange, zRange);

        return CountActiveCubesAfterFullCommandRun(commands.Count - 1, searchArea);
    }

    private long CountActiveCubesAfterFullCommandRun(int command_index, Cuboid cuboid)
    {
        if (cuboid.IsEmpty() || command_index < 0)
        {
            return 0;
        }

        var currentCommand = commands[command_index];
        var intersection = cuboid.IntersectionRange(currentCommand.cuboid);
        var activeInRegion = CountActiveCubesAfterFullCommandRun(command_index - 1, cuboid);
        var activeIntersecting = CountActiveCubesAfterFullCommandRun(command_index - 1, intersection);
        var activeNonIntersecting = activeInRegion - activeIntersecting;

        return currentCommand.turnOn ? activeNonIntersecting + intersection.Volume() : activeNonIntersecting;
    }
}