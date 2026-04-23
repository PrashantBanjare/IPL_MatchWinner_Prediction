--1. High pressure performance - Which teams perform best under high pressure?
SELECT batting_team,
       ROUND(AVG(result)*100,2) AS win_rate
FROM final_df
WHERE rrr > 10
GROUP BY batting_team
ORDER BY win_rate DESC;



--2. Low pressure performance - Win rate when RRR < 6
SELECT batting_team,
       ROUND(AVG(result)*100,2) AS win_rate
FROM final_df
WHERE rrr < 6
GROUP BY batting_team
ORDER BY win_rate DESC;


--3. Wickets impact - Win rate based on wickets left
SELECT wickets_left,
       ROUND(AVG(result)*100,2) AS win_rate
FROM final_df
GROUP BY wickets_left
ORDER BY wickets_left DESC;



--4. Match finishing ability - Teams winning with low wickets (finishing strength)
SELECT batting_team,
       ROUND(AVG(result)*100,2) AS win_rate
FROM final_df
WHERE wickets_left <= 3
GROUP BY batting_team
ORDER BY win_rate DESC;



--5. Clutch situations - Performance in last 2 overs (balls_left <= 12)
SELECT batting_team,
       ROUND(AVG(result)*100,2) AS win_rate
FROM final_df
WHERE balls_left <= 12
GROUP BY batting_team
ORDER BY win_rate DESC;


-- 6. Which teams perform best when very few balls are left?
SELECT batting_team,
       ROUND(AVG(result) * 100, 2) AS win_rate_few_balls_left
FROM final_df
WHERE balls_left <= 18
GROUP BY batting_team
ORDER BY win_rate_few_balls_left DESC;


-- 7. Which teams handle very high targets better?
SELECT batting_team,
       ROUND(AVG(result) * 100, 2) AS win_rate_high_target
FROM final_df
WHERE target >= 180
GROUP BY batting_team
ORDER BY win_rate_high_target DESC;


-- 8. Which cities are toughest for chasing under pressure?
SELECT city,
       ROUND(AVG(result) * 100, 2) AS win_rate_under_pressure
FROM final_df
WHERE rrr > 10
GROUP BY city
ORDER BY win_rate_under_pressure DESC;


-- 9. What is the win rate when teams have both low wickets and high pressure?
SELECT batting_team,
       ROUND(AVG(result) * 100, 2) AS win_rate_tough_situation
FROM final_df
WHERE wickets_left <= 3
  AND rrr > 10
GROUP BY batting_team
ORDER BY win_rate_tough_situation DESC;


-- 10. Which bowling teams are best at defending in the death overs?
SELECT bowling_team,
       ROUND((1 - AVG(result)) * 100, 2) AS defending_success_rate
FROM final_df
WHERE balls_left <= 18
GROUP BY bowling_team
ORDER BY defending_success_rate DESC;