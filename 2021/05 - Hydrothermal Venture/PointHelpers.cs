using System;
using System.Collections.Generic;
using System.Linq;

namespace AdventOfCodeDay5;

class PointHelpers
{
    public static Point CreatePointFromCommaSeperatedString(string input)
    {
        var point = input.Split(",");
        var x = int.Parse(point[0]);
        var y = int.Parse(point[1]);

        return new Point(x, y);
    }

    public static IEnumerable<Point> GeneratePointsWithinPointRange(PointRange points)
    {
        var xDifference = Math.Abs(points.startPoint.x - points.endPoint.x);
        var yDifference = Math.Abs(points.startPoint.y - points.endPoint.y);
        var maxDifferenceInclusive = Math.Max(xDifference, yDifference) + 1;

        return Enumerable.Range(0, maxDifferenceInclusive).Select(position =>
        {
            var x = HorizontalCoordinateForPointRangeDifferentialPosition(points, position);
            var y = VerticalCoordinateForPointRangeDifferentialPosition(points, position);

            return new Point(x, y);
        });
    }

    private static int HorizontalCoordinateForPointRangeDifferentialPosition(PointRange pointRange, int rangePosition)
    {
        if (pointRange.startPoint.x > pointRange.endPoint.x)
        {
            return pointRange.endPoint.x + rangePosition;
        }

        if (pointRange.startPoint.x < pointRange.endPoint.x)
        {
            return pointRange.endPoint.x - rangePosition;
        }

        return pointRange.endPoint.x;
    }

    private static int VerticalCoordinateForPointRangeDifferentialPosition(PointRange pointRange, int rangePosition)
    {
        if (pointRange.startPoint.y > pointRange.endPoint.y)
        {
            return pointRange.endPoint.y + rangePosition;
        }

        if (pointRange.startPoint.y < pointRange.endPoint.y)
        {
            return pointRange.endPoint.y - rangePosition;
        }

        return pointRange.endPoint.y;
    }
}