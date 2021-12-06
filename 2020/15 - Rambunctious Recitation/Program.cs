using System;
using System.IO;
using System.Text;
using System.Linq;
using System.Collections.Generic;

namespace Rambunctious_Recitation
{
    class Program
    {
        static Dictionary<int, int> GenerateHistory(IEnumerable<int> data)
        {
            return data
              .Select((value, index) => new { Key = value, Value = index + 1 })
              .ToDictionary(row => row.Key, row => row.Value);
        }

        static int ElementAtTurn(IEnumerable<int> data, int turn)
        {
            var history = GenerateHistory(data);
            var elements = history.Values.Count();
            var last = history.Last().Key;

            foreach (var index in Enumerable.Range(elements, turn - elements))
            {
                var next = 0;
                if (history.ContainsKey(last)) next = index - history[last];
                history[last] = index;
                last = next;
            }

            return last;
        }

        static void Main(string[] args)
        {
            var input = File.ReadAllText("./input.txt", Encoding.UTF8);
            var data = input.Split(",").Select(point => Convert.ToInt32(point));
            Console.WriteLine("part_one: " + ElementAtTurn(data, 2020));
            Console.WriteLine("part_two: " + ElementAtTurn(data, 30000000));
        }
    }
}
