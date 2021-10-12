--  @testpoint:比较表达式：IS/IS NOT  DISTINCT

--is distinct
--A和B的数据类型、值不完全相同返回 true
--A和B的数据类型、值完全相同返回 false
--将空值视为相同。
select 1 is distinct from 1,
1 is distinct from 2,
1 is distinct from '1',
'1' is distinct from '1',
1 is distinct from null,
null is distinct from null;

--is not distinct
--A和B的数据类型、值不完全相同返回 false
--A和B的数据类型、值完全相同返回 true
--将空值视为相同。
select 1 is not distinct from 1,
1 is not distinct from 2,
1 is not distinct from '1',
'1' is not distinct from '1',
1 is not distinct from null,
null is not distinct from null;

--unknow类型
select 1 is not distinct from '1';

--清理环境
--no need to clean