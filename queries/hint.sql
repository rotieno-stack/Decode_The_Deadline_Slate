-- ============================================================
-- Slate query web service #2:  "DTD Hint"
-- Custom parameters (all text):  row, col
-- Service type: JSON
--
-- Returns ONLY parity and primality of one cell, never the digit.
-- Must use the same grid as guess.sql.
-- ============================================================
select
  case when s.[v] % 2 = 1 then 'true' else 'false' end        as [odd],
  case when s.[v] in (2,3,5,7) then 'true' else 'false' end   as [prime]
from (values
  (0,0,7),(0,1,3),(0,2,5),
  (1,0,2),(1,1,9),(1,2,4),
  (2,0,6),(2,1,8),(2,2,1)
) as s([r],[c],[v])
where s.[r] = try_cast(@row as int)
  and s.[c] = try_cast(@col as int)
for xml path('result'), type
