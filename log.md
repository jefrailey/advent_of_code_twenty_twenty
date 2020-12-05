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