--- Case Type： Comment
--- Case Name： 对类型转换添加注释


--给类型转换添加注释信息
comment on cast(circle as point) is '测试类型转换注释添加成功';

--在相关系统表中查看注释是否添加成功
select description from pg_description where objoid=(select oid from pg_cast where castsource=(select oid from pg_type where typname='circle') and casttarget=(select oid from pg_type where typname='point'));




