-- ============================================================
-- Slate query web service #1:  "DTD Guess"
-- Custom parameters (all text):  row, col, value
-- Service type: JSON
--
-- The solution grid lives ONLY in this query. The browser gets
-- back {"correct":"true"} or {"correct":"false"} and nothing else.
--
-- Grid (0-indexed row, col, digit):
--   7 3 5
--   2 9 4
--   6 8 1
-- ============================================================
select
  case when exists (
    select 1
    from (values
      (0,0,7),(0,1,3),(0,2,5),
      (1,0,2),(1,1,9),(1,2,4),
      (2,0,6),(2,1,8),(2,2,1)
    ) as s([r],[c],[v])
    where s.[r] = try_cast(@row   as int)
      and s.[c] = try_cast(@col   as int)
      and s.[v] = try_cast(@value as int)
  ) then 'true' else 'false' end as [correct]
for xml path('result'), type
