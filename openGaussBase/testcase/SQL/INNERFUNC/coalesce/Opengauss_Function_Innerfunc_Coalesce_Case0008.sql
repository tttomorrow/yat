-- @testpoint:case when的嵌套使用
select case when coalesce(11,null,'',33)=11 then 'a' else 'b' end;