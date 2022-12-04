class Solution
{
    private IEnumerable<ElfPair> pairs;

    public Solution(string[] lines)
    {
        pairs = lines.Select((line) =>
        {
            var elfs = line.Split(",");

            return new ElfPair(
                ElfToAssignmentRange(elfs.ElementAt(0)),
                ElfToAssignmentRange(elfs.ElementAt(1))
            );
        });
    }

    public int SolvePartOne()
    {
        return pairs.Aggregate(0, (accumulator, pair) =>
        {
            if (pair.FullyOverlap)
            {
                return accumulator + 1;
            }

            return accumulator;
        });
    }

    public int SolvePartTwo()
    {
        return pairs.Aggregate(0, (accumulator, pair) =>
        {
            if (pair.PartiallyOverlap)
            {
                return accumulator + 1;
            }

            return accumulator;
        });
    }

    private Range ElfToAssignmentRange(string elf)
    {
        var parts = elf.Split("-");
        var start = int.Parse(parts[0]);
        var end = int.Parse(parts[1]);

        return new Range(start, end);
    }
}