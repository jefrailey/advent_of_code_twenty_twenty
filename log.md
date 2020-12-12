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

10DEC2020
Start: 19:42
Solution at: 20:16
End: 20:38
Notes: `deque`'s great. I had forgotten its second argument, `maxlen` existed until my editor reminded me about it. I had some trouble finding the subsequence of addends for the invalid number in part two. I started with a while loop and mismanaged the indexes. Switching to a for loop helped, but felt like giving up. I successfully re-wrote the while loop version after submitting the solution, but I will not be comitting it as I want the repo to represent (for the most part, I am guilty of the occasional post solution variable and function renaming) the implementation that existed when I submitted the solution.

11DEC2020
Start: 06:50
Stop: 08:05
Notes: I found part one fairly straightforward, but I am struggling with part two. I suspect the solution is based on the number of decision points and options at each decision point, but I have not yet determined how to correctly combine those.

11DEC2020
Start: ~18:00
Stop: ~19:00
Notes: I was frustrated and I wrote the times and this note on the 12th, so the times are approximate and the note is a summary from memory. I stopped trying to find the solution to Day 10 Part Two mathematically and switched to modeling the adapters as a graph and traversing it. This works for the small (eight adapters) sample input but not for the larger (31 adapters) sample input, so I likely have an error somewhere. I anticipate that a graph traversal will be prohibitively computationally expensive, but I'd like to at least make it work...

12DEC2020
Start: 08:21
Solution at: 10:07
Notes: I could not get graph traversal to work in the amount of time I was willing to spend on an implementation that I suspected would not be suitable for large inputs. I switched to an dynamic programming algorithm. It worked on the small sample input, but not the larger sample input. I was fairly that this approach should work, but confused that it did not work. I spent a lot of time drawing and writing and verifying small slices of the algorithm. Still, nothing. Finally, I realized that I was not modeling the entire adapter chain correctly because I was excluding the wall outlet. I had initially ignored it because my mental model of the domain only allowed for one path from the wall outlet to the adapters--likely because there's only one path from the adapters to the final device. However, that was incorrect. Depending on the available adapters, there could be up to three paths from the wall outlet to the rest of the adapters. Excluding the wall outlet only changes the number of paths if the set of adapters includes adapters with joltage values of 2 and/or 3, which is why the solution succeed for the small sample but not the large sample. Correcting that modeling error by adding the wall outlet to the set of adapters if not already present allowed the algorithm to produce the correct result in all tested cases.

Things I did well:
    - Identified that this problem likely required dynamic programming early in my first attempt.
    - Persevered. All told, I spent ~4 hours actively working on this and another ~1 hour thinking about it while doing something else.
Things I did poorly:
    - Not acting on my intuition that the solution would require dynamic programming. I may have been able to significantly reduce the time spent if I started with a dynamic programming solution. In part, I may have shied away from it because they tend to involve a lot of index tracking, which is something I do not feel I do well.
    - Modeling the system. Excluding the wall outlet is one. Thinking about the relations between adapters as a tree was another. Incorrectly considering it a tree instead of a more generic graph is likely what led me to spend so much time looking for a "pure" mathematical approach involving permutations.
    - Tracking indices.