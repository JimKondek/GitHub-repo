--
-- SQL statement to solve the New York Times "Spelling Bee" puzzle
--
-- This SELECT statement reads a table containing English words and
-- displays those words whose letters match the letters in the daily
-- New York Times "Spelling Bee" puzzle, according to the rules of the
-- game (found at https://www.nytimes.com/puzzles/spelling-bee).  
-- The main rules are:
--
--   There are seven letters in the puzzle that change daily
--   The letter 's' is not used, and no words containing the letter
--   's' are ever valid
--   Letters can be used more than once
--   Each word must be four or more characters long
--   Each word only contains some combination of the "center" letter
--     and one or more of the other six letters.
--   Words with length 4 are worth one point, words of length 5 or 
--   more are worth one point per character (e.g. a six letter
--   word is worth six points)
--   A word that uses all seven characters at least once is called
--   a "pangram" and is worth 14 points.  Pangrams longer than seven
--   characters are awarded one extra point for each extra character
--   (e.g., a ten letter pangram is worth 14 + 3 or 17 points).  There
--   is at least one pangram in each day's puzzle.
--
-- I would like to give credit to https://www.keithv.com/software/wlist/
-- which was the source for my list of English words.  I used the "words
-- in 12 lists" list, although some of the words in this list are
-- not found in the "Spelling Bee" internal word list.  (The "words in
-- 12 lists" lists contains one duplicate - "chaplain".)
--
-- The format of the table (as built in a PostgreSQL 14 database)
-- is as follows:
--   CREATE TABLE words  (
--     id          SERIAL    PRIMARY KEY,
--     word        VARCHAR   UNIQUE,
--     wordlength  INTEGER
--   );
--
-- After loading this table, I delete all the rows where the wordlength is
-- less than 4 or the word contains an "s".
--
-- This SELECT statement works in Oracle 19c and PostgreSQL 14.  The
-- list of words was first loaded into a PostgreSQL 14 table using the
-- psql \copy command, then pulled into an Oracle 19c table using
-- Oracle Heterogeneous Services and a DB link.
--
-- The following statement solves the puzzle for the letters
-- appearing in the March 21, 2022 puzzle.  On this day, the
-- center letter is "v" and the other six letters are "a", "e",
-- "h", "i", "l" and "y".
--
SELECT word FROM words
WHERE word LIKE '%v%'  -- today's "center" letter
AND NOT (
     word LIKE '%b%'
  OR word LIKE '%c%'
  OR word LIKE '%d%'
  OR word LIKE '%f%'
  OR word LIKE '%g%'
  OR word LIKE '%j%'
  OR word LIKE '%k%'
  OR word LIKE '%m%'
  OR word LIKE '%n%'
  OR word LIKE '%o%'
  OR word LIKE '%p%'
  OR word LIKE '%q%'
  OR word LIKE '%r%'
  OR word LIKE '%t%'
  OR word LIKE '%u%'
  OR word LIKE '%w%'
  OR word LIKE '%x%'
  OR word LIKE '%z%'
)
ORDER BY word;

Update: here is some interesting insight on some of the values stored in the "words" table:

According to Spelling Bee rules, each word has to be made up of one or more of the seven letters provided in each day's puzzle.  A word such as "abridgement", which contains ten distinct characters, would never be a valid Spelling Bee word; thus words of eight or more distinct characters would not be needed in the "words" table.  Because the number of rows in the "words" table isn't that much (about 27000), there's little harm in keeping the rows with too-long words.  But if we wanted to delete the too-long words, how could we do it using SQL?

PostgreSQL has a function called string_to_table() which will return a table with a row for every character in a string.  Here is an example:
```sql
postgres=# select string_to_table('PostgreSQL', null);
 string_to_table
-----------------
 P
 o
 s
 t
 g
 r
 e
 S
 Q
 L
(10 rows)
```
The second parameter in the function is a delimiter character.  If null is specified, then one row is created for every character in the string (as in the above example).  In the next example, the character 'g' is used as a delimiter character:
```sql
postgres=# select string_to_table('PostgreSQL', 'g');
 string_to_table
-----------------
 Post
 reSQL
(2 rows)
```
We can use the COUNT DISTINCT function to count the number of distinct characters in the string:
```sql
postgres=# select count(distinct string_to_table) from string_to_table('PostgreSQL', null);
 count
-------
    10
(1 row)
```
Going back to our "words" table, we can do something like this:
```sql
postgres=# select word, string_to_table(word, null) from words limit 20;
    word    | string_to_table
------------+-----------------
 meme       | m
 meme       | e
 meme       | m
 meme       | e
 meze       | m
 meze       | e
 meze       | z
 meze       | e
 abandoning | a
 abandoning | b
 abandoning | a
 abandoning | n
 abandoning | d
 abandoning | o
 abandoning | n
 abandoning | i
 abandoning | n
 abandoning | g
 abba       | a
 abba       | b
(20 rows)
```
Here we create a table containing every word that contains more than seven distinct charaters.  
```sql
create table words_long as 
  select word, count(distinct char) as number_of_distinct_chars
  from (select word, string_to_table(word, null) as char
        from words) as t1
  group by word
  having count(distinct char) > 7;
```
This table can be used in a "DELETE FROM words" statement.  I created such a statement using a WHERE EXISTS clause; I'll let you figure out how to do this.
