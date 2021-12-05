
using System.Collections.Generic;
using System.Linq;

namespace AdventOfCodeDay5;

class Solution
{
    public int SolvePartOne(string[] lines)
    {
        var ranges = ParsePointRangesFromInputLines(lines);
        var filteredRanges = ranges.Where(
            points => points.startPoint.x == points.endPoint.x || points.startPoint.y == points.endPoint.y
        );

        return Solve(filteredRanges);
    }

    public int SolvePartTwo(string[] lines)
    {
        var ranges = ParsePointRangesFromInputLines(lines);

        return Solve(ranges);
    }

    public IEnumerable<PointRange> ParsePointRangesFromInputLines(string[] lines)
    {
        return lines
            .Where(line => !string.IsNullOrEmpty(line))
            .Select(PointRange.CreateFromInputLine);
    }

    private int Solve(IEnumerable<PointRange> ranges)
    {
        return ranges
            .SelectMany(PointHelpers.GeneratePointsWithinPointRange)
            .GroupBy(point => point.AsTuple)
            .Count(group => Enumerable.Count(group) >= 2);
    }
}