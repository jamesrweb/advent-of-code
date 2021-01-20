using System;
using System.IO;
using System.Text;
using System.Linq;
using System.Collections.Generic;

namespace Combo_Breaker
{
  class Program
  {
    static List<long> ParseLines(string[] lines)
    {
      return lines.Select(line => Int64.Parse(line)).ToList();
    }

    static long EncryptionKey(long subject, long target)
    {
      var loopSize = 0;
      var result = 1;

      while (result != target)
      {
        loopSize += 1;
        result = (result * 7) % 20201227;
      }

      return Enumerable.Range(0, loopSize).Aggregate(1L, (accumulator, _) =>
      {
        return (accumulator * subject) % 20201227;
      });
    }

    static long SolvePartOne(List<long> keys)
    {
      return EncryptionKey(keys[0], keys[1]);
    }

    static string SolvePartTwo()
    {
      return "There is no part two on day 25!";
    }

    static void Main(string[] args)
    {
      var lines = File.ReadAllLines("./input.txt", Encoding.UTF8);
      var keys = ParseLines(lines);
      Console.WriteLine("part_one: " + SolvePartOne(keys));
      Console.WriteLine("part_two: " + SolvePartTwo());
    }
  }
}
