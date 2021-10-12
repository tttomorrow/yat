-- @testpoint: create index:模式名为64位：success：自动截取为63位
--创建64位模式
--建表
BEGIN
  for i in 1..10000 LOOP
  end LOOP;
end;
/
--建索引
--两次引用证明模式被截取位63位
--清理数据
