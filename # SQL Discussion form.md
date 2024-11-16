# SQL Discussion form

## Administration
* Your name: zhipeng he

* Your discussion partner's name:  Danier

* Commit hash of the code you discussed: 

* Your code's pylint score:8.14

## Discussion
### Pre-set discussion points:
- Start by discussing your DB design choices (tables, data types)
    Split all xml info for 3 tables ,which are Articals, authors and keywords.

- Then go on to your implementation;
  1. How did you split up the work (functions/classes)?
     classes,Danier used functions
     
  2. How long (about) does it take, where is time spent?
     3 weeks, xml file and sqlalchemy

  3. Did you use parallel processing, if so how? If not, why not?
      no.but i tried use array to split the task on slurm, but sometimes didnot work

  4. What was your difference in =pylint= scores? Can you see why?
      some names and coding behavious,Missing docstring

  5. How did the normalization level (table number) influence the code?
       The normalization level table number helps me to undstand and orginise the codes.

  6. Did your choice in database table design make it more or less hard to do the assignment?
       No, I just made three tables, but they have pumbmed_id, i think it will help to analysis.

### Extra points that came up during discussion of your code:
       some error in my output file helps me to know what happened 
### Extra comments about the assignment: