using System;
using System.IO;
using System.Linq;
using System.Collections;
using System.Collections.Generic;

class Solution
{
    private readonly Dictionary<char, char> _closingCharactersMap;
    private readonly Dictionary<char, char> _openingCharactersMap;
    private readonly Dictionary<char, int> _syntaxErrorScoreMap;
    private readonly Dictionary<char, int> _autocompleteErrorScoreMap;
    private string[] _lines;

    public Solution(string[] lines)
    {
        _lines = lines;
        _closingCharactersMap = InitialiseClosingCharactersMap();
        _openingCharactersMap = InitialiseOpeningCharactersMap();
        _syntaxErrorScoreMap = InitialiseSyntaxErrorScoreMap();
        _autocompleteErrorScoreMap = InitialiseAutocompleteErrorScoreMap();
    }

    public int SolvePartOne()
    {
        return _lines.Aggregate<string, int>(0, (accumulator, line) =>
        {
            if (!IsCorruptedLine(line))
            {
                return accumulator;
            }

            return accumulator + CalculateSyntaxErrorScoreForLine(line);
        });
    }

    public long SolvePartTwo()
    {
        var autocompleteErrorScores = _lines
            .Where(line => !IsCorruptedLine(line))
            .Select(CalculateAutocompleteErrorScoreForLine)
            .OrderBy(score => score);
        var medianIndex = autocompleteErrorScores.Count() / 2;

        return autocompleteErrorScores.ElementAt(medianIndex);
    }

    private bool IsCorruptedLine(string line)
    {
        var stack = new List<char>();

        foreach (var character in line)
        {
            if (_openingCharactersMap.ContainsKey(character))
            {
                stack.Add(character);
                continue;
            }

            var lastCharacter = stack.Last();
            var expectedCharacter = _closingCharactersMap[character];

            if (lastCharacter.Equals(expectedCharacter))
            {
                stack.RemoveAt(stack.Count - 1);
                continue;
            }

            return true;
        }

        return false;
    }

    private int CalculateSyntaxErrorScoreForLine(string line)
    {
        var syntaxErrorScore = 0;
        var stack = new List<char>();

        foreach (var character in line)
        {
            if (_openingCharactersMap.ContainsKey(character))
            {
                stack.Add(character);
                continue;
            }

            var lastCharacter = stack.Last();
            var expectedCharacter = _closingCharactersMap[character];

            if (!lastCharacter.Equals(expectedCharacter))
            {
                syntaxErrorScore += _syntaxErrorScoreMap[character];
                break;
            }

            stack.RemoveAt(stack.Count - 1);
        }

        return syntaxErrorScore;
    }

    private long CalculateAutocompleteErrorScoreForLine(string line)
    {
        var stack = new List<char>();

        foreach (var character in line)
        {
            if (_openingCharactersMap.ContainsKey(character))
            {
                stack.Add(character);
                continue;
            }

            var lastCharacter = stack.Last();
            var expectedCharacter = _closingCharactersMap[character];

            if (!lastCharacter.Equals(expectedCharacter))
            {
                continue;
            }

            stack.RemoveAt(stack.Count - 1);
        }

        stack.Reverse();

        return stack.Aggregate(0L, (accumulator, character) =>
        {
            var closingCharacter = _openingCharactersMap[character];

            return (accumulator * 5) + _autocompleteErrorScoreMap[closingCharacter];
        });
    }

    private Dictionary<char, char> InitialiseClosingCharactersMap()
    {
        var closingCharactersMap = new Dictionary<char, char>();

        closingCharactersMap.Add(')', '(');
        closingCharactersMap.Add('>', '<');
        closingCharactersMap.Add(']', '[');
        closingCharactersMap.Add('}', '{');

        return closingCharactersMap;
    }

    private Dictionary<char, char> InitialiseOpeningCharactersMap()
    {
        var openingCharactersMap = new Dictionary<char, char>();

        openingCharactersMap.Add('(', ')');
        openingCharactersMap.Add('<', '>');
        openingCharactersMap.Add('[', ']');
        openingCharactersMap.Add('{', '}');

        return openingCharactersMap;
    }

    private Dictionary<char, int> InitialiseSyntaxErrorScoreMap()
    {
        var syntaxErrorScoreMap = new Dictionary<char, int>();

        syntaxErrorScoreMap.Add(')', 3);
        syntaxErrorScoreMap.Add(']', 57);
        syntaxErrorScoreMap.Add('}', 1197);
        syntaxErrorScoreMap.Add('>', 25137);

        return syntaxErrorScoreMap;
    }

    private Dictionary<char, int> InitialiseAutocompleteErrorScoreMap()
    {
        var autocompleteErrorScoreMap = new Dictionary<char, int>();

        autocompleteErrorScoreMap.Add(')', 1);
        autocompleteErrorScoreMap.Add(']', 2);
        autocompleteErrorScoreMap.Add('}', 3);
        autocompleteErrorScoreMap.Add('>', 4);

        return autocompleteErrorScoreMap;
    }
}

class Program
{
    public static void Main(string[] args)
    {
        var lines = File.ReadAllLines($"{Environment.CurrentDirectory}/input.txt");
        var solution = new Solution(lines);

        Console.WriteLine($"Part one: {solution.SolvePartOne()}");
        Console.WriteLine($"Part two: {solution.SolvePartTwo()}");
    }
}