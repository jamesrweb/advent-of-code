
using System;

namespace AdventOfCodeDay5;

struct Point
{
    public readonly int x;
    public readonly int y;

    public Point(int xPosition, int yPosition)
    {
        x = xPosition;
        y = yPosition;
    }

    public readonly Tuple<int, int> AsTuple => new Tuple<int, int>(this.x, this.y);
}