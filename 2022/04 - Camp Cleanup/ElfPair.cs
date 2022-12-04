record ElfPair(Range elfOneAssignmentRange, Range elfTwoAssignmentRange)
{
    private IEnumerable<int> elfOneAssignmentRangeValues = Enumerable.Range(elfOneAssignmentRange.Start.Value, elfOneAssignmentRange.End.Value - elfOneAssignmentRange.Start.Value + 1);
    private IEnumerable<int> elfTwoAssignmentRangeValues = Enumerable.Range(elfTwoAssignmentRange.Start.Value, elfTwoAssignmentRange.End.Value - elfTwoAssignmentRange.Start.Value + 1);

    public bool FullyOverlap => (
        elfOneAssignmentRangeValues.All(x => elfTwoAssignmentRangeValues.Contains(x)) ||
        elfTwoAssignmentRangeValues.All(y => elfOneAssignmentRangeValues.Contains(y))
    );

    public bool PartiallyOverlap => (
        elfOneAssignmentRangeValues.Any(x => elfTwoAssignmentRangeValues.Contains(x)) ||
        elfTwoAssignmentRangeValues.Any(y => elfOneAssignmentRangeValues.Contains(y))
    );
}
