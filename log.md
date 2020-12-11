01DEC2020
Start: 18:53
Solution at: 19:30
End: 20:08

02DEC2020
Start: 20:12
Solution at: 20:48
End: 20:53
Notes: NamedTuple seems nifty, but it may not have been the best choice for this particular use case. A class that split the instruction line in the initialization method may have been a little cleaner.

03DEC2020
Start: 19:07
Solution at: 19:55
End: 20:17
Notes: I struggled more than I would like to admit massaging the input into the shape I wanted. I forgot the names of a few string methods and how triple quoted strings handle whitespace. I also was quite confused for an embarrassingly long time about an `IndexError` I encountered in the initial implementation. `1 != 0`... I have not recently used a language that starts index positions with `1`, so I'm not sure why I did not catch that quickly. Something I did well was predict the possible complications added by part two. This allowed me to design and implement one algorithm for both parts.

04DEC2020
Start: 18:24
Solution at: 19:51
End: 19:54
Notes: This one seemed to be all about attention to detail. The details I initially missed were:
    - The max valid issue year was 2020. I initially had 2030.
    - Hair color was a `#` followed by exactly six characters. I forgot to include a character count in the regex I used for that.

05DEC2020
Start: 07:24
Solution at: 08:03
End: 08:26
Notes: Identifying that the row and column could be determined using the same algorithm simplified the implementation. My initial attempt at a memory efficient partition algorithm failed--I did not keep that version, so I'm not sure exactly why--so I fell back on something familiar, binary search on a list. I was able to add a version of it within a few minutes of submitting the solution, so the first attempt was likely off by a detail. Pivoting to something I know will work instead of debugging something that is not working is likely a good strategy when minimizing time to a correct solution is a goal.

06DEC2020
Start: 09:09
Solution at: 09:30
End: 10:25
Notes: The primary difference between the algorithms I used for part one and part two was the way in which sets of answers were combined--union in for part one and intersection for part two. After submitting the solution, I attempted to extract the common portions into a separate function. I found the form I arrived at quite unsatisfying. The answering functions shared a lot of code, but both became harder to understand because the operations were split into multiple small functions that seemed to hide the overall algorithm. Perhaps there was a more elegant way to slice it.

07DEC2020
Start: 18:02
Stop: 19:01
Notes: I'm pretty confident the solution involves converting the rules into a graph, which each of the bag colors as nodes and rules dictating the edges and performing an exhaustive search of that graph for the target color from each of the color nodes. However, implementing that is proving more difficult than it "should." I need to review and practice graph creation and traversal.

08DEC2020
Start: 18:19
Solution at: 18:59
End: 19:27
Notes: For part two, I initially forgot to multiply the count of the contents of a child bag by the number of siblings of the same type. E.g. if a light red bag contains 2 muted yellow bags then the number of bags inside the red bag was 2 times the count of one yellow bag. This is, of course, obvious, especially when written out. It suggests I needed to take a little more time to imagine the system that I was modeling. The algorithm I used for counting the contents of the bags for part two included the outermost bag in its count, which made it off by one. I "solved" that the easy way by subtracting one at the end. It works, but seems inelegant. An alternative is to add another function that excludes the count of the current bag and have that function call the recursive function that includes the current bag in its count. I'm not convinced that is much better.

10DEC2020
Start: 18:37
Solution at: 19:25
End: 19:41
Notes: I initially forgot to increment the value of the current instruction for all operations, which caused my simulated console to return `0` for programs that did not start with an `acc`. I spent some time refactoring between part one and two that could have been left until after I had a solution to part two. I found correctly determining if the program had terminated and tracking the current instruction a little difficult. They're both a bit unintuitive because value of the current instruction changes during the evaluation of a statement in the program. So, the current instruction needed to be recorded as evaluated before it was actually evaluated. Likewise, identifying that the final line in the program had been evaluated required either checking if the line to be evaluated was the last line before evaluating it, or identifying that it had been evaluated before attempting to evaluate the next line. This may be improved by tracking the previous instruction and checking that after evaluating each statement.