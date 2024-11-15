To solve this task has been used following prompt:

Your task it to find the way from starting point to finish point of the matrix:
- Matrix has 6 columns (A-F)
- Matrix has 4 rows (1-4)
- Starting point is A4
- Finish point is F4
- FORBIDDEN FIELDS : B1, B3, B4, D2, D3
- You have to avoid FORBIDDEN FIELDS
- Move just using command: UP, DOWN, LEFT, RIGHT
- print result in following format <RESULT>{"steps":"... ,..., ..."}</RESULT>
- before printing <RESULT></RESULT> print your thinking about proper path
- Check all possible solution, count the steps ot each and return solution with the lowest value of steps
- The best way have to count 9 steps
Example of result format:
<RESULT>
{
"steps":"UP, DOWN, LEFT, RIGHT"
}
</RESULT>