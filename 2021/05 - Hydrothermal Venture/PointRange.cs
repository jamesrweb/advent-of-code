namespace AdventOfCodeDay5;

struct PointRange
{
    public readonly Point startPoint;
    public readonly Point endPoint;

    public PointRange(Point start, Point end)
    {
        startPoint = start;
        endPoint = end;
    }

    public static PointRange CreateFromInputLine(string line)
    {
        var points = line.Split(" -> ");
        var p1 = PointHelpers.CreatePointFromCommaSeperatedString(points[0]);
        var p2 = PointHelpers.CreatePointFromCommaSeperatedString(points[1]);

        return new PointRange(p1, p2);
    }
}