using System;
using System.IO;
using System.Text;
using System.Linq;

namespace Shuttle_Search
{
  class Shuttle
  {
    public long interval { get; set; }
    public long id { get; set; }
    public long next { get; set; }

    public Shuttle(long id, long interval, long next)
    {
      this.id = id;
      this.interval = interval;
      this.next = next;
    }
  }

  class Program
  {
    static Shuttle[] ParseInput(string[] lines)
    {
      var earliest = Convert.ToInt64(lines[0]);
      var routes = lines[1].Split(",");
      return routes.Select((string route, int index) =>
        {
          if (route == "x") return null;
          var interval = Convert.ToInt64(route);
          return new Shuttle(index, interval, interval - earliest % interval);
        }
      ).Where(b => b != null).ToArray();
    }

    static long SolvePartOne(Shuttle[] buses)
    {
      var bus = buses.OrderBy(b => b.next).First();
      return bus.interval * bus.next;
    }

    static long SolvePartTwo(Shuttle[] buses)
    {
      var step = buses.First().interval;
      var result = step;

      foreach (var bus in buses.Skip(1))
      {
        while ((result + bus.id) % bus.interval != 0) result += step;
        step *= bus.interval;
      }

      return result;
    }

    static void Main(string[] args)
    {
      var input = File.ReadAllLines("./input.txt", Encoding.UTF8);
      var buses = ParseInput(input);
      Console.WriteLine("part_one: " + SolvePartOne(buses));
      Console.WriteLine("part_two: " + SolvePartTwo(buses));
    }
  }
}