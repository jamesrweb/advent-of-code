class Cuboid
{
    public Range x;
    public Range y;
    public Range z;

    public Cuboid(Range _x, Range _y, Range _z)
    {
        x = _x;
        y = _y;
        z = _z;
    }

    public bool IsEmpty()
    {
        return x.IsEmpty() || y.IsEmpty() || z.IsEmpty();
    }

    public long Volume()
    {
        return x.Length() * y.Length() * z.Length();
    }

    public Cuboid IntersectionRange(Cuboid that)
    {
        var xRange = this.x.IntersectionRange(that.x);
        var yRange = this.y.IntersectionRange(that.y);
        var zRange = this.z.IntersectionRange(that.z);

        return new Cuboid(xRange, yRange, zRange);
    }
}