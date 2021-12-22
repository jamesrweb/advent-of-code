class Range
{
    public int min;
    public int max;

    public Range(int _min, int _max)
    {
        min = _min;
        max = _max;
    }

    public bool IsEmpty()
    {
        return min > max;
    }

    public long Length()
    {
        if (IsEmpty())
        {
            return 0;
        }

        return max - min + 1;
    }

    public Range IntersectionRange(Range other)
    {
        var maxMinRange = Math.Max(min, other.min);
        var minMaxRange = Math.Min(max, other.max);

        return new Range(maxMinRange, minMaxRange);
    }
}