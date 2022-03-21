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
